from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from social_network.settings import settings
from social_network.db import (
    AuthUserManager,
    DatabaseError,
    AccessTokenModel,
    AccessTokenManager,
)
from social_network.utils.security import hash_password

from .utils import (
    is_valid_password,
    generate_token_value,
    get_access_token_manager_depends,
    get_auth_user_manager_depends
)

from .models import (
    LoginPayload,
    RegistrationPayload
)

router = APIRouter()


@cbv(router)
class AuthViewSet:
    user_manager: AuthUserManager = Depends(get_auth_user_manager_depends)
    access_token_manager: AccessTokenManager = Depends(
        get_access_token_manager_depends
    )

    @router.post('/login', response_model=AccessTokenModel, responses={
        201: {'description': 'Success login'},
        400: {'description': 'Invalid email or password'}
    })
    async def login(self, p: LoginPayload):
        try:
            user = await self.user_manager.get(email=p.email)
            if not is_valid_password(user, p.password.get_secret_value()):
                raise ValueError
        except (DatabaseError, ValueError):
            msg = 'Invalid email or password'
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': msg})

        expired_at = datetime.now() + timedelta(
            seconds=settings.TOKEN_EXPIRATION_TIME
        )
        tokens = await self.access_token_manager.list_user_active(user.id)
        if not tokens:
            a = await self.access_token_manager.create(
                user_id=user.id,
                expired_at=expired_at,
                value=generate_token_value()
            )
        a = await self.access_token_manager.update(
            token_id=tokens[0].id,
            new_expired_at=expired_at
        )
        return a

    @router.post('/register', status_code=201, responses={
        201: {'description': 'User created'},
        400: {'description': 'Invalid email'}
    })
    async def register(self, p: RegistrationPayload):
        if await self.user_manager.is_email_already_used(p.email):
            msg = 'User with this email already exists'
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': msg})

        hashed_password, salt = hash_password(p.password.get_secret_value())
        await self.user_manager.create(p.email, hashed_password, salt,
                                       p.first_name, p.last_name)
