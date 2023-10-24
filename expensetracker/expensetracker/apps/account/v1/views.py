"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from typing import Union
from esmerald import Request
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.exceptions import NotAuthorized
from esmerald.routing.gateways import Gateway, WebSocketGateway
from esmerald.routing.views import APIView
from esmerald.routing.handlers import get, post, put

from expensetracker.middleware.authentication import CustomJWTMidleware
from .daos import UserDAO
from .schemas import *


class UserView(APIView):
    """
    User management API View
    """
    path = "/users"

    @post(
        path="/",
        tags=["User"],
        summary="Create a user",
        description="Creates a new user in the system",
        responses={
            200: OpenAPIResponse(model=UserOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response")
        }
    )
    async def create(self, data: UserCreateSchema) -> UserOutSchema:
        dao = UserDAO()
        return await dao.create(**data.model_dump())

    @get(
        path="/",
        middleware=[CustomJWTMidleware],
        tags=["User"],
        summary="Get user",
        description="Returns the logged user",
        responses={
            200: OpenAPIResponse(model=UserOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def get_current(self, request: Request) -> UserOutSchema:
        dao = UserDAO()
        return await dao.get(obj_id=request.user)

    @put(
        path="/{id:int}",
        middleware=[CustomJWTMidleware],
        tags=["User"],
        summary="Update user",
        description="Updates the logged user",
        responses={
            200: OpenAPIResponse(model=UserOutSchema),
            400: OpenAPIResponse(model=ErrorSchema, description="Bad response"),
            401: OpenAPIResponse(model=ErrorSchema, description="Not autorized")
        }
    )
    async def update_user(
        self, 
        request: Request,
        id: int,
        data: UserUpdatechema
    ) -> None:
        if request.user != id:
            raise NotAuthorized()

        dao = UserDAO()
        await dao.update(id, data)
