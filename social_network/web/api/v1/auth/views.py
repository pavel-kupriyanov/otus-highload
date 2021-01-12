from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from social_network.settings import settings
from social_network.db.models import AccessToken, AuthUser
from social_network.db.managers import (
    AuthUserManager,
    AccessTokenManager
)
from social_network.db.excpetions import RowsNotFoundError
from social_network.utils.security import hash_password

from .utils import (
    is_valid_password,
    generate_token_value,
)

from .models import (
    LoginPayload,
    RegistrationPayload
)

from ..depends import (
    get_access_token_manager_depends,
    get_auth_user_manager_depends
)

router = APIRouter()


@cbv(router)
class AuthViewSet:
    user_manager: AuthUserManager = Depends(get_auth_user_manager_depends)
    access_token_manager: AccessTokenManager = Depends(
        get_access_token_manager_depends
    )

    # TODO: return endpoint types
    @router.post('/login', status_code=201, response_model=AccessToken,
                 responses={
                     201: {'description': 'Success login'},
                     400: {'description': 'Invalid email or password'}
                 })
    async def login(self, p: LoginPayload):
        user = await self.user_manager.get_by_email(email=p.email)
        if not is_valid_password(user, p.password.get_secret_value()):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'detail': 'Invalid email or password'}
            )

        expired_at = datetime.now() + timedelta(
            seconds=settings.TOKEN_EXPIRATION_TIME
        )
        tokens = await self.access_token_manager.list_user_active(user.id)
        if not tokens:
            return await self.access_token_manager.create(
                user_id=user.id,
                expired_at=expired_at,
                value=generate_token_value()
            )
        return await self.access_token_manager.update(
            token_id=tokens[0].id,
            new_expired_at=expired_at
        )

    # TODO: add hobbies to user
    @router.post('/register', status_code=201, response_model=AuthUser,
                 responses={
                     201: {'description': 'User created'},
                     400: {'description': 'Invalid email'}
                 })
    async def register(self, p: RegistrationPayload):
        try:
            await self.user_manager.get_by_email(p.email)
        except RowsNotFoundError:
            pass
        else:
            msg = 'User with this email already exists'
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'detail': msg})

        hashed_password, salt = hash_password(p.password.get_secret_value())
        return await self.user_manager.create(email=p.email,
                                              hashed_password=hashed_password,
                                              salt=salt,
                                              age=p.age,
                                              first_name=p.first_name,
                                              last_name=p.last_name,
                                              city=p.city,
                                              gender=p.gender)
