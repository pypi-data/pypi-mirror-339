import uuid
from typing import TypeVar, Type, Generic, Optional, List, Dict, Literal, Union
from sqlalchemy import select, delete, update, and_, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, InstrumentedAttribute

from rb_commons.http.exceptions import NotFoundException
from rb_commons.orm.exceptions import DatabaseException, InternalException

ModelType = TypeVar('ModelType', bound=declarative_base())

def with_transaction_error_handling(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Database error: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise InternalException(f"Unexpected error: {str(e)}") from e
    return wrapper

class BaseManager(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.data = None
        self.filters = []
        self._filtered = False

    async def _persist(self, instance: ModelType) -> Optional[ModelType]:
        self.session.add(instance)
        await self.session.flush()
        return await self._smart_commit(instance)

    async def _smart_commit(self, instance: Optional[ModelType] = None) -> Optional[ModelType]:
        if not self.session.in_transaction():
            await self.session.commit()

        if instance:
            await self.session.refresh(instance)
            return instance

    async def get(self, pk: Union[str, int, uuid.UUID]) -> Optional[ModelType]:
        """
           get object based on conditions
       """
        query = select(self.model).filter_by(id=pk)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise NotFoundException(
                message="Object does not exist",
                status=404,
                code="0001",
            )

        return instance

    def filter(self, **kwargs) -> 'BaseManager[ModelType]':
        """
           Apply filtering conditions dynamically.

           Supports:
           - `field__eq`: Equal (`=`)
           - `field__ne`: Not Equal (`!=`)
           - `field__gt`: Greater Than (`>`)
           - `field__lt`: Less Than (`<`)
           - `field__gte`: Greater Than or Equal (`>=`)
           - `field__lte`: Less Than or Equal (`<=`)
           - `field__in`: IN Query
           - `field__contains`: LIKE Query
       """
        self._filtered = True
        self.filters = []

        for key, value in kwargs.items():
            if '__' in key:
                field_name, operator = key.split('__', 1)
            else:
                field_name, operator = key, 'eq'

            column = getattr(self.model, field_name, None)
            if column is None or not isinstance(column, InstrumentedAttribute):
                raise ValueError(f"Invalid filter field: {field_name}")

            if operator == "eq":
                self.filters.append(column == value)
            elif operator == "ne":
                self.filters.append(column != value)
            elif operator == "gt":
                self.filters.append(column > value)
            elif operator == "lt":
                self.filters.append(column < value)
            elif operator == "gte":
                self.filters.append(column >= value)
            elif operator == "lte":
                self.filters.append(column <= value)
            elif operator == "in" and isinstance(value, list):
                if not isinstance(value, list):
                    raise ValueError(f"`{field_name}__in` requires a list, got {type(value)}")

                self.filters.append(column.in_(value))
            elif operator == "contains":
                self.filters.append(column.ilike(f"%{value}%"))

        return self

    def _ensure_filtered(self):
        """Ensure that `filter()` has been called before using certain methods."""
        if not self._filtered:
            raise RuntimeError("You must call `filter()` before using this method.")

    async def all(self) -> List[ModelType]:
        """Return all results based on applied filters."""
        self._ensure_filtered()

        query = select(self.model)
        if self.filters:
            query = query.filter(and_(*self.filters))

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def first(self) -> Optional[ModelType]:
        """Return the first matching object, or None."""
        self._ensure_filtered()

        query = select(self.model).filter(and_(*self.filters))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def count(self) -> int:
        """Return the count of matching records."""

        self._ensure_filtered()
        query = select(func.count()).select_from(self.model).filter(and_(*self.filters))
        result = await self.session.execute(query)
        return result.scalar_one()

    @with_transaction_error_handling
    async def create(self, **kwargs) -> ModelType:
        """
               Create a new object
        """
        obj = self.model(**kwargs)

        self.session.add(obj)
        await self.session.flush()
        return await self._smart_commit(obj)

    @with_transaction_error_handling
    async def delete(self):
        """
        Delete object(s) with flexible filtering options

        :return: Number of deleted records or None
        """
        self._ensure_filtered()

        try:
            delete_stmt = delete(self.model).where(and_(*self.filters))
            result = await self.session.execute(delete_stmt)
            await self.session.commit()
            return result.rowcount
        except NoResultFound:
            return False

    @with_transaction_error_handling
    async def bulk_delete(self) -> int:
        """
            Bulk delete with flexible filtering.

            Automatically commits if not inside a transaction.

            :return: Number of deleted records
        """
        self._ensure_filtered()

        delete_stmt = delete(self.model).where(and_(*self.filters))
        result = await self.session.execute(delete_stmt)
        await self._smart_commit()
        return result.rowcount  # ignore

    @with_transaction_error_handling
    async def update_by_filters(self, filters: Dict, **update_fields) -> Optional[ModelType]:
        """
        Update object(s) with flexible filtering options

        :param filters: Conditions for selecting records to update
        :param update_fields: Fields and values to update
        :return: Number of updated records
        """
        if not update_fields:
            raise InternalException("No fields provided for update")

        update_stmt = update(self.model).filter_by(**filters).values(**update_fields)
        await self.session.execute(update_stmt)
        await self.session.commit()
        updated_instance = await self.get(**filters)
        return updated_instance

    @with_transaction_error_handling
    async def update(self, instance: ModelType, **update_fields) -> Optional[ModelType]:
        """
        Update an existing database instance with new fields

        :param instance: The database model instance to update
        :param update_fields: Keyword arguments of fields to update
        :return: The updated instance

        :raises InternalException: If integrity violation
        :raises DatabaseException: For database-related errors
        """
        # Validate update fields
        if not update_fields:
            raise InternalException("No fields provided for update")

        # Apply updates directly to the instance
        for key, value in update_fields.items():
            setattr(instance, key, value)

        self.session.add(instance)
        await self._smart_commit()

        return instance

    @with_transaction_error_handling
    async def save(self, instance: ModelType) -> Optional[ModelType]:
        """
        Save instance

        :param instance: The database model instance to save
        :return: The saved instance

        Automatically commits if not inside a transaction.

        :raises InternalException: If integrity violation
        :raises DatabaseException: For database-related errors
        """
        self.session.add(instance)
        await self.session.flush()
        return await self._smart_commit(instance)

    async def is_exists(self, **kwargs) -> bool:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @with_transaction_error_handling
    async def bulk_save(self, instances: List[ModelType]) -> None:
        """
        Bulk save a list of instances into the database.

        If inside a transaction, flushes only.
        If not in a transaction, commits after flush.

        :param instances: List of instances
        :raises DatabaseException: If any database error occurs
        :raises InternalException: If any unexpected error occurs
        """
        if not instances:
            return

        self.session.add_all(instances)
        await self.session.flush()

        if not self.session.in_transaction():
            await self.session.commit()
