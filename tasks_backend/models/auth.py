from uuid import UUID

from tasks_backend.models.shared import AccessTokenResponse
from tasks_backend.models.users import UserBase


class LoginResponse(UserBase, AccessTokenResponse):
    id: UUID