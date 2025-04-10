"""Middlewares module."""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from fastapi_async_sql.exceptions import (
    MissingArgsError,
    MultipleArgsError,
)


class AsyncSQLModelMiddleware(BaseHTTPMiddleware):
    """Middleware to handle the database session.

    /// info | Usage Documentation
    [Middlewares](../concepts/middlewares.md#asyncsqlmodelmiddleware)
    ///

    Attributes:
        app (ASGIApp): The ASGI app.
        db_url (str | None): The database URL. Defaults to None.
        custom_engine (AsyncEngine | None): The custom engine. Defaults to None.
        session_options (dict | None): The session options. Defaults to None.
        engine_options (dict | None): The engine options. Defaults to None.
    """

    def __init__(
        self,
        app: ASGIApp,
        db_url: str | None = None,
        custom_engine: AsyncEngine | None = None,
        session_options: dict | None = None,
        engine_options: dict | None = None,
    ):
        super().__init__(app)

        if not db_url and not custom_engine:
            raise MissingArgsError("db_url", "custom_engine")
        if db_url and custom_engine:
            raise MultipleArgsError("db_url", "custom_engine")

        if not custom_engine:
            self.engine = create_async_engine(db_url, **engine_options or {})
        else:
            self.engine = custom_engine

        # Modify session defaults to keep session active
        default_session_options = {
            "expire_on_commit": False,  # Prevent expiring objects after commit
            "autoflush": True,
        }
        if session_options:
            default_session_options.update(session_options)

        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            **default_session_options,
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """Method to dispatch the request."""
        async with self.async_session() as session:
            # Begin transaction
            async with session.begin():
                request.state.db = session
                response = await call_next(request)
                # Transaction will be committed automatically when exiting context
                # Only if no exceptions occurred
                return response
