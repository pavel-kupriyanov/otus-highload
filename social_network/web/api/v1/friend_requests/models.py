from pydantic import BaseModel


class FriendRequestPostPayload(BaseModel):
    user_id: int
