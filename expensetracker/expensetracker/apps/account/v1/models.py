from esmerald.contrib.auth.saffier.base_user import AbstractUser


from esmerald.conf import settings

_, registry = settings.db_access


class User(AbstractUser):
    class Meta:
        registry = registry

