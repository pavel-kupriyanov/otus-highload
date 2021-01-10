from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .friend_requests import router as friend_requests_manager
from .friendship import router as friendship_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth')
router.include_router(users_router, prefix='/users')
router.include_router(friend_requests_manager, prefix='/friend_requests')
router.include_router(friendship_router, prefix='/friendships')
