import pytest
from fastapi.testclient import TestClient
from twitter_api.database import Base, engine
from twitter_api.database.depends import get_db_session
from twitter_api.main import api

from .configs import Session
from .factories import FollowershipFactory, UserFactory


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session(db):
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def test_api(session):
    api.dependency_overrides[get_db_session] = lambda: session
    return api


@pytest.fixture()
def client(test_api):
    base_url = 'http://localhost:8000/api/v1'
    yield TestClient(app=test_api, base_url=base_url)


@pytest.fixture()
def auth_user():
    return UserFactory(username='bindruid', email='abharya.dev@gmail.com')


@pytest.fixture()
def auth_header(auth_user):
    return {'Authorization': f'Bearer {auth_user.token}'}


@pytest.fixture()
def user_as_follower(auth_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=auth_user, following=other_user)


@pytest.fixture()
def user_as_following(auth_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=other_user, following=auth_user)
