from __future__ import annotations

import abc
import asyncio
import base64
import binascii
import dataclasses
import datetime
import hashlib
import hmac
import typing

import blinker
import click
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
)
from starlette.authentication import (
    AuthenticationError as StarletteAuthenticationError,
)
from starlette.authentication import (
    BaseUser as StarletteBaseUser,
)
from starlette.middleware import Middleware as StarletteMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response

from kupala.applications import Kupala
from kupala.database.extension import SQLAlchemy
from kupala.database.manager import on_commit
from kupala.database.models import Base, WithTimestamps
from kupala.dependencies import VariableResolver
from kupala.exceptions import HTTPException, NotAuthenticated
from kupala.passwords import PasswordHasher
from kupala.responses import JSONErrorResponse

user_authenticated = blinker.signal("user-authenticated", doc="User authenticated by an authenticator.")
user_registered = blinker.signal("user-registered", doc="User registered.")
user_logged_out = blinker.signal("user-logged-out", doc="User logged out.")
user_logged_in = blinker.signal("user-logged-in", doc="User interactively logged in.")
user_login_failed = blinker.signal("user-login-failed", doc="Interactive login failed.")
user_deactivated = blinker.signal("user-deactivated", doc="User deactivated.")
user_reactivated = blinker.signal("user-reactivated", doc="User reactivated.")
user_password_changed = blinker.signal("user-password-changed", doc="User password changed.")
user_password_reset = blinker.signal("user-password-reset", doc="User password reset.")
user_email_confirmed = blinker.signal("user-email-confirmed", doc="User email confirmed.")


class BaseUser(Base, StarletteBaseUser, WithTimestamps):
    """Base class for user objects."""

    __abstract__ = True
    __tablename__ = "users"
    __table_args__ = (sa.Index("users_email_udx", sa.func.lower(sa.literal_column("email")), unique=True),)

    email: Mapped[str] = mapped_column(doc="Email address.")
    password: Mapped[str] = mapped_column(doc="Password hash.")
    deactivated_at: Mapped[datetime.datetime | None] = mapped_column(doc="Deactivation timestamp.")
    email_verified_at: Mapped[datetime.datetime | None] = mapped_column(doc="Email verification timestamp.")

    @property
    def identity(self) -> str:
        return self.email

    @property
    def display_name(self) -> str:
        return self.email

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return self.deactivated_at is None

    @property
    def is_email_confirmed(self) -> bool:
        return self.email_verified_at is not None

    def get_password_hash(self) -> str:
        return self.password

    def get_scopes(self) -> list[str]:
        return []

    @classmethod
    async def register(
        cls, dbsession: AsyncSession, *, email: str, password_hash: str, **attrs: typing.Any
    ) -> typing.Self:
        user = cls(email=email, password=password_hash, **attrs)
        dbsession.add(user)
        await dbsession.flush()

        def _after_commit() -> None:
            asyncio.create_task(user_registered.send_async(cls, user=user))

        on_commit(dbsession, _after_commit)
        return user

    def __str__(self) -> str:
        return self.display_name


type ByIDLoader = typing.Callable[[HTTPConnection, str], typing.Awaitable[BaseUser | None]]
type ByUserNameLoader = typing.Callable[[HTTPConnection, str], typing.Awaitable[BaseUser | None]]
type ByAPITokenLoader = typing.Callable[[HTTPConnection, str], typing.Awaitable[BaseUser | None]]

SESSION_IDENTITY_KEY = "kupala.identity"
SESSION_HASH_KEY = "kupala.identity_hash"


_U = typing.TypeVar("_U", bound=BaseUser, default=BaseUser)


class AuthenticationError(HTTPException, StarletteAuthenticationError):
    """Base class for authentication errors."""


class NotAuthenticatedError(AuthenticationError, NotAuthenticated):
    """User is not authenticated."""


@dataclasses.dataclass
class Identity(typing.Generic[_U]):
    id: str
    user: _U
    scopes: typing.Sequence[str]
    authenticator: type[Authenticator]


class DatabaseUserLoader(typing.Generic[_U]):
    def __init__(
        self,
        model_class: type[_U],
        where_builder: typing.Callable[[str], sa.ColumnElement[bool]],
    ) -> None:
        self.model_class = model_class
        self.where_builder = where_builder

    async def __call__(self, request: HTTPConnection, identity: str) -> _U | None:
        dbsession: AsyncSession = request.state.dbsession
        stmt = sa.select(self.model_class).where(self.where_builder(identity))
        result = await dbsession.scalars(stmt)
        return result.one_or_none()


def make_session_auth_hash(user: _U, secret_key: str) -> str:
    """Compute current user session auth hash."""
    key = hashlib.sha256(("kupala.auth." + secret_key).encode()).digest()
    return hmac.new(key, msg=user.get_password_hash().encode(), digestmod=hashlib.sha256).hexdigest()


def update_session_auth_hash(connection: HTTPConnection, user: _U, secret_key: str) -> None:
    """Update session auth hash.
    Call this function each time you change user's password.
    Otherwise, the session will be instantly invalidated."""
    connection.session[SESSION_HASH_KEY] = make_session_auth_hash(user, secret_key)


def validate_session_auth_hash(connection: HTTPConnection, session_auth_hash: str) -> bool:
    """Validate session auth hash."""
    return hmac.compare_digest(connection.session.get(SESSION_HASH_KEY, ""), session_auth_hash)


class Authenticator(abc.ABC):
    """Base class for authenticators."""

    @abc.abstractmethod
    async def authenticate(self, conn: HTTPConnection) -> Identity | None:
        raise NotImplementedError


class SessionAuthenticator(Authenticator):
    """Authenticates users based on session information.
    This authenticator looks for the user's ID in the session and loads the
    corresponding user object. It also validates the session authentication hash
    if the user object supports password hashing.
    """

    def __init__(self, user_loader: ByIDLoader) -> None:
        self.user_loader = user_loader

    async def authenticate(self, conn: HTTPConnection) -> Identity | None:
        user_id: str = conn.session.get(SESSION_IDENTITY_KEY, "")
        if not user_id:
            return None

        user = await self.user_loader(conn, user_id)
        if not user:
            return None

        # avoid authentication if session hash is invalid
        # this may happen when user changes password OR session is hijacked
        secret_key = conn.app.secret_key
        if conn.session.get(SESSION_HASH_KEY):
            if not validate_session_auth_hash(conn, make_session_auth_hash(user, secret_key)):
                return None

        scopes = user.get_scopes()

        return Identity(id=user.identity, user=user, scopes=scopes, authenticator=self.__class__)


class HTTPBasicAuthenticator(Authenticator):
    """
    A basic HTTP authentication authenticator.

    This authenticator implements the HTTP Basic Authentication scheme as specified in RFC 7617.
    It extracts credentials from the Authorization header, decodes them from base64, and validates
    the username/password against a provided user loader.

    If a session is available, the authentication hash will be updated in the session.
    """

    def __init__(self, user_loader: ByIDLoader) -> None:
        self.user_loader = user_loader

    async def authenticate(self, conn: HTTPConnection) -> Identity | None:
        auth = self.get_authorization_header(conn).split()

        if not auth or auth[0].lower() != "basic":
            return None

        if len(auth) == 1:
            raise AuthenticationError("Invalid basic header. No credentials provided.")

        if len(auth) > 2:
            raise AuthenticationError("Invalid basic header. No spaces allowed.")

        try:
            auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            identity, password = auth_decoded.split(":", 1)
        except (TypeError, ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic header. Credentials not correctly base64 encoded.")

        return await self.authenticate_credentials(conn, identity, password)

    def get_authorization_header(self, conn: HTTPConnection) -> str:
        return conn.headers.get("Authorization", "")

    async def authenticate_credentials(self, conn: HTTPConnection, identity: str, password: str) -> Identity | None:
        user = await self.user_loader(conn, identity)
        if not user:
            return None

        password_hasher = Authentication.of(conn.app).passwords
        if not await password_hasher.averify(password, user.get_password_hash()):
            return None

        if "session" in conn.scope:
            secret_key = conn.app.secret_key
            update_session_auth_hash(conn, user, secret_key)

        scopes = user.get_scopes()

        return Identity(id=user.identity, user=user, scopes=scopes, authenticator=self.__class__)


class ChainAuthenticator(Authenticator):
    """Authenticate user using multiple authenticators."""

    def __init__(self, *authenticators: Authenticator) -> None:
        self.authenticators = authenticators

    async def authenticate(self, conn: HTTPConnection) -> Identity | None:
        for authenticator in self.authenticators:
            if identity := await authenticator.authenticate(conn):
                return identity
        return None


class AuthenticatorBackend(AuthenticationBackend):
    """Integrates authenticators with Starlette's authentication middleware."""

    def __init__(self, authenticator: Authenticator) -> None:
        self.authenticator = authenticator

    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        if identity := await self.authenticator.authenticate(conn):
            await user_authenticated.send_async(self.__class__, user=identity.user)
            return AuthCredentials(scopes=identity.scopes), identity.user
        return None


# TODO: OpenID connect authenticators: google, github, etc.
# TODO: run authorization as route middleware


class Authentication:
    def __init__(
        self,
        authenticator: Authenticator,
        password_hasher: PasswordHasher,
        user_model_class: type[_U],
    ) -> None:
        self.authenticator = authenticator
        self.passwords = password_hasher
        self.user_model_class = user_model_class

    def configure(self, app: Kupala) -> None:
        app.state[Authentication] = self
        app.commands.append(passwords_command)
        app.commands.append(users_command)
        app.dependencies.registry[PasswordHasher] = VariableResolver(self.passwords)
        app.asgi_middleware.append(
            StarletteMiddleware(
                AuthenticationMiddleware,
                backend=AuthenticatorBackend(self.authenticator),
            )
        )

    @classmethod
    def of(cls, app: Kupala) -> typing.Self:
        return typing.cast(typing.Self, app.state[Authentication])


def authentication_error_json_handler(request: Request, exc: Exception) -> Response:
    return JSONErrorResponse(message="Not authenticated.", status_code=401)


passwords_command = click.Group("passwords", help="Password management commands.")
users_command = click.Group("users", help="User management commands.")


@passwords_command.command("hash")
@click.argument("password")
@click.pass_obj
def hash_password_command(app: Kupala, password: str) -> None:
    """Hash a password."""
    passwords = Authentication.of(app).passwords
    click.echo(passwords.make(password))


@passwords_command.command("verify")
@click.argument("hashed_password")
@click.argument("plain_password")
@click.pass_obj
def verify_password_command(app: Kupala, hashed_password: str, plain_password: str) -> None:
    """Verify a password."""
    passwords = Authentication.of(app).passwords
    valid, new_hash = passwords.verify_and_migrate(plain_password, hashed_password)
    click.echo(
        "Valid: {valid}".format(valid=click.style("yes", fg="green") if valid else click.style("no", fg="yellow"))
    )
    if valid:
        click.echo(
            "Needs migration: {value}".format(
                value=click.style("yes", fg="yellow") if new_hash else click.style("no", fg="green")
            )
        )


@users_command.command("new")
@click.argument("email")
@click.argument("password")
@click.option("--dbname", default="default", help="Database name.")
@click.pass_obj
async def new_user_command(app: Kupala, email: str, password: str, dbname: str) -> None:
    """Create a new user."""
    passwords = Authentication.of(app).passwords
    user_model_class = Authentication.of(app).user_model_class
    database = SQLAlchemy.of(app).get_database(dbname)
    async with database.session() as dbsession, dbsession:
        user = await user_model_class.register(
            dbsession,
            email=email,
            password_hash=passwords.make(password),
        )
        await dbsession.commit()

    click.echo(
        "User {user} created, id={id}".format(
            user=click.style(user, fg="yellow"), id=click.style(user.identity, fg="green")
        )
    )


def _read_user_from_request(request: Request) -> BaseUser:
    user = request.user
    if not user.is_authenticated:
        raise NotAuthenticatedError("User is not authenticated.")
    return typing.cast(BaseUser, user)


type CurrentUser[_U] = typing.Annotated[_U, _read_user_from_request]
