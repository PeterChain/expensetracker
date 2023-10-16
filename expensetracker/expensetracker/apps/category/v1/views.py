"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from esmerald import Request
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.conf import settings
from esmerald.exceptions import NotAuthorized, ValidationErrorException
from esmerald.routing.views import APIView
from esmerald.routing.handlers import get, post, put
from saffier.exceptions import DoesNotFound, ValidationError
from typing import List

from expensetracker.apps.base_enum import TrxType
from .models import TrxCategory
from .schemas import *
from .daos import CategoryDAO


class CategoryView(APIView):
    """
    Transaction category API View
    """
    path = "/categories"

    @post(
        path="/",
        tags=["Category"],
        summary="Create a category",
        description="Creates a new category for a user",
        responses={
            200: OpenAPIResponse(model=CategoryOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response")
        }
    )
    async def create(
        self, 
        data: CategoryCreateSchema,
        request: Request
    ) -> CategoryOutSchema:
        dao = CategoryDAO()
        return await dao.create(data, request.user)

    @get(
        path="/{id:int}",
        tags=["Category"],
        summary="Get a category",
        description="Returns the logged user",
        responses={
            200: OpenAPIResponse(model=CategoryOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def get_category(self, id: int) -> CategoryOutSchema:
        dao = CategoryDAO()
        return await dao.get(id)

    @get(
        path="/inc",
        tags=["Category"],
        summary="Get all income categories",
        description="Returns income categories",
        responses={
            200: OpenAPIResponse(model=CategoryOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def get_income_by_user(self, request: Request) -> List[CategoryOutSchema]:
        dao = CategoryDAO()
        return await dao.get_categories_by_type(user=request.user, cat_type=TrxType.INCOME)

    @get(
        path="/exp",
        tags=["Category"],
        summary="Get all expenses categories",
        description="Returns expenses categories",
        responses={
            200: OpenAPIResponse(model=[CategoryOutSchema]),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def get_expense_by_user(self, request: Request) -> [CategoryOutSchema]:
        dao = CategoryDAO()
        return dao.get_categories_by_type(user=request.user, cat_type=TrxType.EXPENSE)

    @put(
        path="/{id:int}",
        tags=["Category"],
        summary="Update a category",
        description="Update a category by ID",
        responses={
            200: OpenAPIResponse(model=CategoryOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def update(self, id: int, data: CategoryUpdateSchema) -> None:
        dao = CategoryDAO()
        dao.update(id, data)

