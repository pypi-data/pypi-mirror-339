"""Repositories module for FastAPI."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import SQLModel, func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from .exceptions import CreateObjectError, ObjectNotFoundError
from .filtering import Filter
from .pagination import Page, Params, paginate

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)
PK = Any


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base Repository with default methods to Create, Read, Update, Delete (CRUD).

    /// info | Usage Documentation
    [Repositories](../concepts/repositories.md#baserepository)
    ///

    Attributes:
        model (type[ModelType]): The model to be used in the Repository.
        db (AsyncSession | None): The database session to be used. Defaults to None.
    """

    def __init__(self, model: type[ModelType], db: AsyncSession | None = None) -> None:
        """Repository with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            model (type[ModelType]): The model to be used in the Repository.
            db (AsyncSession, optional): The database session to be used. Defaults to None.

        Returns:
            None
        """
        self.model = model
        self.db = db

    async def get(self, *, id: PK, db_session: AsyncSession | None = None) -> ModelType:
        """Get a single object by ID."""
        session = self._get_db_session(db_session)
        response = await session.get(self.model, id)
        if response is None:
            raise ObjectNotFoundError(obj=self.model.__name__, id=id)
        return response

    async def get_by_ids(
        self,
        *,
        list_ids: list[PK],
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Get a list of objects by IDs."""
        session = self._get_db_session(db_session)
        response = await session.exec(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.all()

    async def get_count(
        self, db_session: AsyncSession | None = None
    ) -> ModelType | None:
        """Get the total count of objects."""
        session = self._get_db_session(db_session)
        response = await session.exec(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.one_or_none()

    async def get_multi(
        self,
        *,
        query: T | Select[T] | None = None,
        page_params: Params | None = None,
        filter_by: Filter | None = None,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Get multiple objects with optional filtering."""
        session = self._get_db_session(db_session)
        query = self._validate_query(query)
        query = self._apply_query_filter(query, filter_by)
        query = self._apply_query_pagination(query, page_params)
        response = await session.exec(query)
        return response.all()

    async def get_multi_paginated(
        self,
        *,
        query: T | Select[T] | None = None,
        page_params: Params | None = None,
        filter_by: Filter | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        """Get multiple objects with pagination."""
        session = self._get_db_session(db_session)
        page_params = page_params or Params()
        query = self._validate_query(query)
        query = self._apply_query_filter(query, filter_by)
        output = await paginate(session, query, page_params)
        return output

    async def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        db_session: AsyncSession | None = None,
        **extra_data: Any,
    ) -> ModelType:
        """Create a new object."""
        session = self._get_db_session(db_session)
        db_obj = self.model.model_validate(obj_in, update=extra_data)

        try:
            session.add(db_obj)
            # Don't commit here - let the middleware handle the transaction
            await session.flush()  # Just flush to get generated values
        except exc.IntegrityError as err:
            raise CreateObjectError(
                obj=self.model.__name__, **db_obj.model_dump()
            ) from err
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        """Update an existing object."""
        session = self._get_db_session(db_session)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(
                exclude_unset=True,
            )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        session.add(obj_current)
        # Don't commit here - let the middleware handle the transaction
        await session.flush()
        return obj_current

    async def remove(
        self, *, id: PK | str, db_session: AsyncSession | None = None
    ) -> None:
        """Delete an object."""
        session = self._get_db_session(db_session)
        obj = await session.get(self.model, id)
        if obj is None:
            raise ObjectNotFoundError(obj=self.model.__name__, id=id)
        await session.delete(obj)
        # Don't commit here - let the middleware handle the transaction
        await session.flush()
        return None

    # noinspection PyMethodMayBeStatic
    def _validate_query(self, query: T | Select[T]) -> T | Select[T]:
        """Validate the query."""
        if not isinstance(query, (Select, SelectOfScalar)):
            query = select(self.model)
        return query

    # noinspection PyMethodMayBeStatic
    def _apply_query_filter(
        self, query: T | Select[T], filter_by: Filter | None
    ) -> T | Select[T]:
        """Get the query with the filter applied."""
        if filter_by is not None:
            query = filter_by.filter(query)
            if getattr(filter_by, filter_by.Constants.ordering_field_name, None):
                query = filter_by.sort(query)
        return query

    # noinspection PyMethodMayBeStatic
    def _apply_query_pagination(
        self, query: T | Select[T], page_params: Params
    ) -> T | Select[T]:
        """Apply pagination to the query."""
        if page_params:
            query = query.limit(page_params.size).offset(
                page_params.size * (page_params.page - 1)
            )
        return query

    def _get_db_session(self, db_session: AsyncSession | None = None) -> AsyncSession:
        """Get the database session."""
        session = db_session or self.db
        if session is None:
            raise ValueError("Database session is not set.")
        return session
