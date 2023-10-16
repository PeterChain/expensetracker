from esmerald.contrib.auth.saffier.middleware import JWTAuthMiddleware

from apps.account.v1.models import User
from esmerald.conf import settings

jwt_config = settings.jwt_config


class CustomJWTMidleware(JWTAuthMiddleware):
    def __init__(self, app: "ASGIApp"):
        
        super().__init__(app, config=jwt_config, user_model=User)