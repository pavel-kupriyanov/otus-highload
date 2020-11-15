from typing import Optional, Tuple

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi_utils.cbv import cbv

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field
)

from social_network.db import (
    get_connector,
    get_user_manager,
    BaseDatabaseConnector,
    UserManager
)
from social_network.utils.security import (
    serialize,
    make_hash,
    get_salt,
)

router = APIRouter()


def get_manager(connector: BaseDatabaseConnector = Depends(get_connector)) \
        -> UserManager:
    return get_user_manager(connector)


class RegistrationPayload(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=255)
    first_name: str = Field(..., min_length=2, max_length=255)
    last_name: Optional[str] = Field(None, min_length=2, max_length=255)


@cbv(router)
class AuthViewSet:
    user_manager: UserManager = Depends(get_manager)

    @router.get('/hello')
    async def hello(self):
        # a, b = self.connector, self.manager
        return 'Hello'

    @router.post('/register', status_code=201, responses={
        201: {'description': 'User created'},
        400: {'description': 'Invalid email'}
    })
    async def register(self, p: RegistrationPayload):
        if await self.user_manager.is_email_already_used(p.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='User with this email already exists')

        hashed_password, salt = hash_password(p.password.get_secret_value())
        await self.user_manager.create(p.email, hashed_password, salt,
                                       p.first_name, p.last_name)


def hash_password(raw_password: str) -> Tuple[str, str]:
    salt = get_salt()
    return make_hash(raw_password, salt), serialize(salt)
