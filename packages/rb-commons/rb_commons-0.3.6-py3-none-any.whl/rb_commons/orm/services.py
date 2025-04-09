from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from rb_commons.http.exceptions import ForbiddenException
from rb_commons.schemes.jwt import Claims


class BaseService:
    def __init__(self, claims: Claims, session: AsyncSession):
        self.claims = claims
        self.session = session

    def _verify_shop_permission(self, target: Any, raise_exception: bool = True) -> bool:
        if self.claims.shop_id != getattr(target, "shop_id", None):
            if raise_exception:
                raise ForbiddenException("You are not allowed to access this resource")
            return False
        return True
