import saffier
from esmerald.conf import settings

from expensetracker.apps.account.v1.models import User
from expensetracker.apps.category.v1.models import TrxCategory
from expensetracker.apps.base_enum import TrxType


_, registry = settings.db_access

class Transaction(saffier.Model):
    id = saffier.IntegerField(primary_key=True)
    trx_type = saffier.ChoiceField(TrxType)
    amount = saffier.DecimalField(7, 2)
    currency = saffier.CharField(max_length=3)
    trx_date = saffier.DateTimeField()
    notes = saffier.CharField(max_length=100)
    user = saffier.ForeignKey(User, null=False, on_delete=saffier.CASCADE)
    category = saffier.ForeignKey(TrxCategory, null=True, on_delete=saffier.CASCADE)

    class Meta:
        registry = registry