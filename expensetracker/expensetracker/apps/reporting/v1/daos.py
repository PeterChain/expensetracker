from typing import Any, List
from datetime import datetime

from esmerald import AsyncDAOProtocol
from esmerald.exceptions import NotFound, ValidationErrorException, NotAuthorized
from saffier.exceptions import DoesNotFound, ValidationError

from account.v1.models import User
from transaction.v1.models import Transaction
from expensetracker.apps.base_enum import TrxType
from .schemas import *


class TrxReportingDAO(AsyncDAOProtocol):
    model: Transaction = Transaction

    async def get_agg_by_category(
        self, 
        data: TrxAggregateCatgInSchema, 
        user: User
    ) -> List[TrxAggregateCatgOutSchema]:
        """
        Gets the aggregate transactions per category
        """
        if not data.expenses and not data.incomes:
            raise ValidationErrorException("Income and/or expenses must be selected")

        if data.date_from > data.date_to:
            raise ValidationErrorException("Date from must be inferior or equal to date to")
        
        filter_cond = {"user":user.id,
                       "trx_date__gte":data.date_from,
                       "trx_date__lte":data.date_to}
        

        try:
            if data.expenses == True and not data.incomes:
                filter_cond["trx_type"] = TrxType.EXPENSE
            if data.incomes == True and not data.expenses:
                filter_cond["trx_type"] = TrxType.INCOME
            trx_list = await self.model \
                                 .query \
                                 .filter(**filter_cond) \
                                 .group_by("id", "trx_type", "category")

            return self.from_orm(trx_list)
        except DoesNotFound:
            return []
    
    def from_orm(self, trx_list: List[Transaction]) -> TrxAggregateCatgOutSchema:
        """
        Converts ORM to detail schema
        """
        result = {}
        for e in trx_list:
            if e.category.id in result:
                result[e.category.id].amount += float(e.amount)
            else:
                result[e.category.id] = TrxAggregateCatgOutSchema(
                                        trx_type=str(e.trx_type),
                                        amount=e.amount,
                                        category=e.category.id,
                                    )
        return list(result.values())