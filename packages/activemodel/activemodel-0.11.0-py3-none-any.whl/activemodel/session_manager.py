"""
Class to make managing sessions with SQL Model easy. Also provides a common entrypoint to make it easy to mutate the
database environment when testing.
"""

import contextlib
import contextvars
import json
import typing as t

from decouple import config
from pydantic import BaseModel
from sqlalchemy import Connection, Engine
from sqlmodel import Session, create_engine


def _serialize_pydantic_model(model: BaseModel | list[BaseModel] | None) -> str | None:
    """
    Pydantic models do not serialize to JSON. You'll get an error such as:

    'TypeError: Object of type TranscriptEntry is not JSON serializable'

    https://github.com/fastapi/sqlmodel/issues/63#issuecomment-2581016387

    This custom serializer is passed to the DB engine to properly serialize pydantic models to
    JSON for storage in a JSONB column.
    """

    # TODO I bet this will fail on lists with mixed types

    if isinstance(model, BaseModel):
        return model.model_dump_json()
    if isinstance(model, list):
        # not everything in a list is a pydantic model
        def dump_if_model(m):
            if isinstance(m, BaseModel):
                return m.model_dump()
            return m

        return json.dumps([dump_if_model(m) for m in model])
    else:
        return json.dumps(model)


class SessionManager:
    _instance: t.ClassVar[t.Optional["SessionManager"]] = None
    "singleton instance of SessionManager"

    session_connection: Connection | None
    "optionally specify a specific session connection to use for all get_session() calls, useful for testing and migrations"

    @classmethod
    def get_instance(cls, database_url: str | None = None) -> "SessionManager":
        if cls._instance is None:
            assert database_url is not None, (
                "Database URL required for first initialization"
            )
            cls._instance = cls(database_url)

        return cls._instance

    def __init__(self, database_url: str):
        self._database_url = database_url
        self._engine = None

        self.session_connection = None

    # TODO why is this type not reimported?
    def get_engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(
                self._database_url,
                # NOTE very important! This enables pydantic models to be serialized for JSONB columns
                json_serializer=_serialize_pydantic_model,
                # TODO move to a constants area
                echo=config("ACTIVEMODEL_LOG_SQL", cast=bool, default=False),
                # https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic
                pool_pre_ping=True,
                # some implementations include `future=True` but it's not required anymore
            )

        return self._engine

    def get_session(self):
        "get a new database session, respecting any globally set sessions"

        if gsession := _session_context.get():

            @contextlib.contextmanager
            def _reuse_session():
                yield gsession

            return _reuse_session()

        # a connection can generate nested transactions
        if self.session_connection:
            return Session(bind=self.session_connection)

        return Session(self.get_engine())


def init(database_url: str):
    "configure activemodel to connect to a specific database"
    return SessionManager.get_instance(database_url)


def get_engine():
    "alias to get the database engine without importing SessionManager"
    return SessionManager.get_instance().get_engine()


def get_session():
    "alias to get a database session without importing SessionManager"
    return SessionManager.get_instance().get_session()


_session_context = contextvars.ContextVar[Session | None](
    "session_context", default=None
)
"""
This is a VERY important ContextVar, it sets a global session to be used across all ActiveModel operations by default
and ensures get_session() uses this session as well.

contextvars must be at the top-level of a module! You will not get a warning if you don't do this.
ContextVar is implemented in C, so it's very special and is both thread-safe and asyncio safe. This variable gives us
a place to persist a session to use globally across the application.
"""


@contextlib.contextmanager
def global_session():
    """
    Generate a session shared across all activemodel calls.

    Alternatively, you can pass a session to use globally into the context manager, which is helpful for migrations
    and testing.
    """

    if _session_context.get() is not None:
        raise RuntimeError("global session already set")

    with SessionManager.get_instance().get_session() as s:
        token = _session_context.set(s)

        try:
            yield s
        finally:
            _session_context.reset(token)


async def aglobal_session():
    """
    Use this as a fastapi dependency to get a session that is shared across the request:

    >>> APIRouter(
    >>>     prefix="/internal/v1",
    >>>     dependencies=[
    >>>         Depends(aglobal_session),
    >>>     ]
    >>> )
    """

    if _session_context.get() is not None:
        raise RuntimeError("global session already set")

    with SessionManager.get_instance().get_session() as s:
        token = _session_context.set(s)

        try:
            yield
        finally:
            _session_context.reset(token)
