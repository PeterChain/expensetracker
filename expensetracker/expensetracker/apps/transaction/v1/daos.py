from typing import Any, List

from loguru import logger
from esmerald import AsyncDAOProtocol
from esmerald.exceptions import NotFound, ValidationErrorException, NotAuthorized
from saffier.exceptions import DoesNotFound, ValidationError

from account.v1.models import User
from category.v1.models import TrxCategory
from .models import Transaction
from .schemas import *


class TransactionDAO(AsyncDAOProtocol):
    model: Transaction = Transaction

    async def create(
        self, 
        data: TransactionCreateSchema,
        user: User
    ) -> TransactionOutDetailSchema:
        """
        Creates a new transaction in the system
        """
        if not data.amount or data.amount <= 0:
            raise ValueError("Amount must be positive")

        try:
            category = await TrxCategory.query.get(id=data.category)
        except DoesNotFound:
            raise ValidationErrorException(f"Category {data.category} does not exist")

        try:
            db_trx = await self.model.query.create(
                trx_type=data.trx_type,
                amount=data.amount,
                currency=data.currency,
                trx_date=data.trx_date,
                notes=data.notes,
                category=category,
                user=user
            )

            return self.from_orm_detail(db_trx)
        except ValidationError as error:
            logger.error(str(error))
            raise ValidationErrorException(f"Creation of transaction failed") from error

    async def get(self, obj_id: int, user: User) -> TransactionOutDetailSchema:
        """
        Get a transaction by ID
        """
        try:
            db_trx = await self.model.query.get(id=obj_id)
            if db_trx.user.id != user.id:
                raise NotAuthorized(f"Transaction ID {obj_id} is not valid")

            return self.from_orm_detail(db_trx)
        except DoesNotFound:
            raise NotFound(f"Transaction with ID '{obj_id}' not found.")
        
    async def get_user_transactions(
        self, 
        user: User,
    ) -> List[TransactionOutListSchema]:
        """
        Get all transactions of a user
        """
        try:
            trxs = await self.model.query.filter(user=user)
            return [self.from_orm_list(e) for e in trxs]
        except DoesNotFound:
            return []

    async def update(self, obj_id: int, data: TransactionUpdateSchema) -> None:
        """
        Updates a transaction from the system.
        """
        if data.amount is not None and data.amount <= 0:
            raise ValidationErrorException("Amount must be positive")

        try:
            if data.category:
                await TrxCategory.query.get(id=data.category)
        except DoesNotFound:
            raise ValidationErrorException(f"Category {data.category} does not exist")

        try:
            db_trx = await self.model.query.get(id=obj_id)
            if data.trx_type:
                db_trx.trx_type = data.trx_type
            if data.amount:
                db_trx.amount = data.amount
            if data.currency:
                db_trx.currency = data.currency
            if data.trx_date:
                db_trx.trx_date = data.trx_date
            if data.notes:
                db_trx.notes = data.notes
            if data.category:
                db_trx.category = data.category
            await db_trx.save()
        except DoesNotFound as nf_error:
            logger.error(str(nf_error))
            raise NotFound(f"Transaction {obj_id} not found") from nf_error
        except ValidationError as int_error:
            logger.error(str(int_error))
            raise ValidationErrorException(f"Update of transaction {obj_id} failed") from int_error

    async def delete(self, obj_id: int) -> None:
        """
        Deletes a transaction
        """
        try:
            db_trx = await self.model.query.get(id=obj_id)
            await db_trx.delete()
        except DoesNotFound as nf_error:
            logger.error(str(nf_error))
            raise NotFound(f"Transaction {obj_id} not found")
    
    def from_orm_detail(self, trx: Transaction) -> TransactionOutDetailSchema:
        """
        Converts ORM to detail schema
        """
        return TransactionOutDetailSchema(
            id=trx.id,
            trx_type=str(trx.trx_type),
            amount=trx.amount,
            currency=trx.currency,
            trx_date=str(trx.trx_date),
            category=trx.category.id,
            user=trx.user.id,
            notes=trx.notes
        )
    
    def from_orm_list(self, trx: Transaction) -> TransactionOutListSchema:
        """
        Converts ORM to list schema
        """
        return TransactionOutListSchema(
            id=trx.id,
            trx_type=str(trx.trx_type),
            amount=trx.amount,
            currency=trx.currency
        )
