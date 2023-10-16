from datetime import timedelta, datetime
from esmerald.conf import settings
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.exceptions import NotAuthorized
from esmerald.routing.views import APIView
from esmerald.routing.handlers import post
from esmerald.security.jwt.token import Token

from account.v1.daos import UserDAO
from .schemas import LoginSchema, ErrorSchema


class LoginView(APIView):
    """
    Login API view
    """
    path = "/login"

    @post(
        path="/",
        tags=["Authentication"],
        summary="Login",
        description="Logins a user, returns a JWT Token"
    )
    async def login(self, data: LoginSchema) -> str:
        dao = UserDAO()
        
        if not await dao.check_credentials(
            data.username,
            data.password
        ):
            raise NotAuthorized

        user = await dao.get_by_username(data.username)
        
        expiration_date = datetime.now() + timedelta(minutes=30)
        token = Token(exp=expiration_date, sub=user.id)

        return token.encode(
            key=settings.jwt_config.signing_key,
            algorithm=settings.jwt_config.algorithm
        )