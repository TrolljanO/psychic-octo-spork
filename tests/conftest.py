# tests/conftest.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')  # Passamos 'testing' para usar a configuração de teste
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
