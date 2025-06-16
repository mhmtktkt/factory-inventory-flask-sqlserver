import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import pytest
from app import create_app, db
from app.models import User, Departmanlar

@pytest.fixture
def client(tmp_path):
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(tmp_path/'test.db')
    app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            dep = Departmanlar(DEPARTMANADI='Test')
            db.session.add(dep)
            user = User(KULLANICIADI='testuser', DEPARTMANID=1)
            user.set_password('test')
            db.session.add(user)
            db.session.commit()
        yield client


def test_login_logout(client):
    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'test'})
    assert b'Giris basarili' in response.data or response.status_code == 302
    response = client.get('/auth/logout')
    assert response.status_code == 302
