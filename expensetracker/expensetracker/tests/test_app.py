"""
Generated by 'esmerald createproject' using Esmerald 2.0.3.
"""
from esmerald.testclient import EsmeraldTestClient

from ..main import get_application


def create_app():
    app = get_application()
    return app


def get_client():
    return EsmeraldTestClient(create_app())

# Add your tests here