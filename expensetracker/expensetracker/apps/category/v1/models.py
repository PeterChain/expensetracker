import saffier
from esmerald.conf import settings

from expensetracker.apps.account.v1.models import User
from expensetracker.apps.base_enum import TrxType


_, registry = settings.db_access

class TrxCategory(saffier.Model):
    id = saffier.IntegerField(primary_key=True)
    description = saffier.CharField(max_length=100)
    cat_type = saffier.ChoiceField(TrxType)
    user = saffier.ForeignKey(User, null=False, on_delete=saffier.CASCADE)

    class Meta:
        registry = registry