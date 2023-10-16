from typing import Any, List

from esmerald import AsyncDAOProtocol
from esmerald.exceptions import NotFound, ValidationErrorException
from saffier.exceptions import DoesNotFound, ValidationError

from expensetracker.apps.base_enum import TrxType
from account.v1.models import User
from transaction.v1.models import Transaction
from .models import TrxCategory
from .schemas import CategoryOutSchema, CategoryCreateSchema


class CategoryDAO(AsyncDAOProtocol):
    model: TrxCategory = TrxCategory

    async def create(
        self, 
        data: CategoryCreateSchema,
        user: User
    ) -> CategoryOutSchema:
        """
        Creates a new transaction category in the system
        """
        existing_trx = await TrxCategory.query.filter(
            cat_type=data.cat_type,
            description=data.description,
            user=user
        )
        if existing_trx:
            raise ValidationErrorException("Category with description already exists")

        try:
            db_cat = await TrxCategory.query.create(
                cat_type=data.cat_type,
                description=data.description,
                user=user
            )

            return self.from_orm(db_cat)
        except ValidationError as error:
            raise ValidationErrorException(f"Creation of category failed") from error

    async def get(self, obj_id: int) -> CategoryOutSchema:
        """
        Get a category by ID
        """
        try:
            db_cat = await self.model.query.get(id=obj_id)
            return self.from_orm(db_cat)
        except DoesNotFound:
            raise NotFound(f"Category with ID '{obj_id}' not found.")
        
    async def get_categories_by_type(
        self, 
        user: User,
        cat_type: str
    ) -> List[CategoryOutSchema]:
        """
        Get all categories of a user by type
        """
        try:
            cats = await self.model.query.filter(user=user,          
                                                 cat_type=cat_type)
            return [self.from_orm(e) for e in cats]
        except DoesNotFound:
            return []

    async def update(self, obj_id: int, **kwargs: Any) -> None:
        """
        Updates a category from the system.
        """
        try:
            db_cat = await self.model.query.get(id=obj_id)
            db_cat.query.update(
                description=kwargs.get("description")
            )
        except DoesNotFound as nf_error:
            raise NotFound(f"Category {obj_id} not found") from nf_error
        except ValidationError as int_error:
            raise ValidationError(f"Update of category {obj_id} failed") from int_error

    async def delete(self, obj_id: int) -> None:
        """
        Deletes a category
        """
        try:
            trx_num = await Transaction.query.filter(category=obj_id).count()
            if trx_num > 0:
                raise ValidationErrorException(f"Category {obj_id} is already in use in {trx_num} transactions")

            await self.model.query.get(id=obj_id).delete()
            
        except DoesNotFound as nf_error:
            raise NotFound(f"Category {obj_id} not found") from nf_error

    def from_orm(self, model: TrxCategory) -> CategoryOutSchema:
        """
        Maps ORM category to Pydantic
        """
        return CategoryOutSchema(
            id=model.id,
            cat_type=model.cat_type,
            description=model.description
        )
