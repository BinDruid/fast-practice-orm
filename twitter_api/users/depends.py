from typing import Annotated

from fastapi import Depends, Request

from twitter_api.core import exceptions
from twitter_api.core.middleware import AuthenticatedUser
from twitter_api.database import DbSession

from .models import Followership, User


def get_current_user(request: Request) -> AuthenticatedUser:
    if request.state.user.is_anonymous:
        raise exceptions.NotAuthenticated
    return request.state.user


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]


def get_user_by_name(username: str, db_session: DbSession) -> User:
    user = db_session.query(User).filter(User.username == username).one_or_none()
    if user is None:
        raise exceptions.NotFound(detail=f'User {username} not found')
    return user


UserByName = Annotated[User, Depends(get_user_by_name)]


def get_user_by_id(user_id: int, db_session: DbSession) -> User:
    user = db_session.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise exceptions.NotFound(detail=f'User {user_id} not found')
    return user


UserByID = Annotated[User, Depends(get_user_by_id)]


def get_follower_by_follower_id_and_user(follower_user_id: int, user: UserByID, db_session: DbSession) -> Followership:
    follower = (
        db_session.query(Followership)
        .filter(Followership.follower_id == follower_user_id, Followership.following_id == user.id)
        .one_or_none()
    )
    if not follower:
        raise exceptions.NotFound(detail=f'User #{follower_user_id} does not follow user #{user.id}')
    return follower


FollowerByID = Annotated[Followership, Depends(get_follower_by_follower_id_and_user)]


def get_following_by_following_user_id_and_user(
    following_user_id: int, user: UserByID, db_session: DbSession
) -> Followership:
    following = (
        db_session.query(Followership)
        .filter(Followership.following_id == following_user_id, Followership.follower_id == user.id)
        .one_or_none()
    )
    if not following:
        raise exceptions.NotFound(detail=f'User #{user.id} does not follow user #{following_user_id}')
    return following


FollowingByID = Annotated[Followership, Depends(get_following_by_following_user_id_and_user)]
