"""
Generated by 'esmerald createapp' using Esmerald 2.0.3.
"""
from esmerald import Gateway

from .views import CategoryView

route_patterns = [
    Gateway(handler=CategoryView, path="/v1")
]