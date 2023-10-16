from typing import Any

from account.v1.models import User
from asyncpg.exceptions import UniqueViolationError
from esmerald import AsyncDAOProtocol
from saffier.exceptions import DoesNotFound, ValidationError

from .schemas import UserOutSchema


class UserDAO(AsyncDAOProtocol):
    model: User = User

    async def create(self, **kwargs: Any) -> User:
        """
        Creates a user in the system
        """
        try:
            return self.model.query.create_user(**kwargs)
        except UniqueViolationError as e:
            raise ValueError(str(e)) from e

    async def get(self, obj_id: Any, **kwargs: Any) -> UserOutSchema:
        """
        Get the information of a user by ID.
        """
        try:
            user = await self.model.query.get(id=obj_id)
            return UserOutSchema.model_validate(user, from_attributes=True)
        except DoesNotFound:
            raise ValueError(f"User with ID '{obj_id}' not found.")
        
    async def get_by_username(self, username: Any) -> UserOutSchema:
        """
        Get the information of a user by username.
        """
        try:
            user = await self.model.query.get(username=username)
            return UserOutSchema.model_validate(user, from_attributes=True)
        except DoesNotFound:
            raise ValueError(f"Username '{username}' not found.")

    async def delete(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Deletes a user from the system by ID.
        """
        try:
            user = await self.model.query.get(id=obj_id)
            await user.delete()
        except DoesNotFound:
            raise ValueError(f"User with ID '{obj_id}' not found.")

    async def update(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Updates a user from the system.
        """
        try:
            db_user = await User().query.filter(id=obj_id)
            db_user.query.update(
                username=kwargs.get("username"),
                first_name=kwargs.get("first_name"),
                last_name=kwargs.get("last_name")
            )
            if kwargs.get("password"):
                db_user.set_password(kwargs.get("password"))
        except DoesNotFound as nf_error:
            raise ValueError(f"User {obj_id} not found") from nf_error
        except ValidationError as int_error:
            raise ValueError(f"Update of user {obj_id} failed") from int_error

    async def check_credentials(
        self,
        username: str,
        password: str
    ) -> bool:
        """
        Checks the credentials received with those in system
        """
        try:
            db_users = await self.model.query.filter(username=username)
            if not db_users:
                raise ValueError(f"Username {username} not found")
            return db_users[0].check_password(password)
        except DoesNotFound as error:
            raise ValueError(f"Username {username} not found") from error