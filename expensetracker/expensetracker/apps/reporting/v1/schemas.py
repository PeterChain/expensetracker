"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel, field_serializer
from expensetracker.apps.base_enum import TrxType



class TrxAggregateCatgInSchema(BaseModel):
    """
    Input schema for category aggregation
    """
    date_from: Optional[date]
    date_to: Optional[date]
    expenses: bool = True
    incomes: bool = True


class TrxAggregateCatgOutSchema(BaseModel):
    """
    Aggregate transaction report output schema
    """
    trx_type: str
    category: int
    amount: float