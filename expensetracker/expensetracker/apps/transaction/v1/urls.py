"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from esmerald import Gateway

from .views import TransactionView

route_patterns = [
    Gateway(handler=TransactionView, path="/v1")
]
