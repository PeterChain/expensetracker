"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from typing import List
from esmerald import Request
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.views import APIView
from esmerald.routing.handlers import get

from .daos import TrxReportingDAO
from .schemas import *


class ReportingView(APIView):
    """
    Transactions reporting API View
    """
    path = "/reporting"

    @get(
        path="/cat",
        tags=["Transaction"],
        summary="Gets transactions grouped by category",
        description="Gets transactions grouped by category",
        responses={
            200: OpenAPIResponse(model=[TrxAggregateCatgOutSchema])
        }
    )
    async def get_aggr_by_categories(
        self,
        request: Request,
        date_from: date,
        date_to: date,
        expense: bool = True,
        income: bool = True
    ) -> List[TrxAggregateCatgOutSchema]:
        dao = TrxReportingDAO()
        params = TrxAggregateCatgInSchema(
            date_from=date_from,
            date_to=date_to,
            expenses=expense,
            incomes=income
        )
        return await dao.get_agg_by_category(params, request.user)
