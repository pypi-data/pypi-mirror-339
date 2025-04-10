"""Base models."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import AwareDatetime, ConfigDict
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel

from fastapi_async_sql.utils.string import to_camel, to_snake_plural

from .typing import TimeStamp


class BaseSQLModel(AsyncAttrs, SQLModel):
    """Base SQL model with automatic __tablename__ generation.

    /// info | Usage Documentation
    [Models](../concepts/models.md#basesqlmodel)
    ///

    Attributes:
        __tablename__ (str): The table name for the model.
        model_config (ConfigDict): The configuration for the model.
    """

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically."""
        return to_snake_plural(cls.__name__)

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_assignment=True,
        populate_by_name=True,
        extra="forbid",
    )


class BaseTimestampModel:
    """Base model with created_at and updated_at fields.

    /// info | Usage Documentation
    [Models](../concepts/models.md#basetimestampmodel)
    ///
    """

    created_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        sa_type=TimeStamp(timezone=True),
    )

    updated_at: AwareDatetime | None = Field(
        default=None,
        sa_type=TimeStamp(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(tz=timezone.utc)},
    )


class BaseUUIDModel:
    """Base model with UUID primary key.

    /// info | Usage Documentation
    [Models](../concepts/models.md#baseuuidmodel)
    ///
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
