from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .friendships import router as friend_requests_manager
from .hobbies import router as hobbies_router
from .messages import router as messages_router
from .news import router as news_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth')
router.include_router(users_router, prefix='/users')
router.include_router(friend_requests_manager, prefix='/friendships')
router.include_router(hobbies_router, prefix='/hobbies')
router.include_router(messages_router, prefix='/messages')
router.include_router(news_router, prefix='/news')
