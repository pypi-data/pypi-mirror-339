from typing import Any, Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession

from rb_commons.http.exceptions import ForbiddenException
from rb_commons.schemes.jwt import Claims


class BaseService:
    def __init__(self, claims: Claims, session: AsyncSession):
        self.claims = claims
        self.session = session
        self._feign_clients = {}

    def register_feign_client(self, name: str, init_func: Callable[[], Awaitable[Any]]):
        """
            Dynamically adds a get_<name>() method that lazy-loads the client.
        """
        attr_name = f"_{name}"

        async def getter(self):
            if getattr(self, attr_name, None) is None:
                client = await init_func()
                setattr(self, attr_name, client)
            return getattr(self, attr_name)

        method_name = f"get_{name}"
        bound_method = getter.__get__(self, self.__class__)
        setattr(self, method_name, bound_method)

    def _verify_shop_permission(self, target: Any, raise_exception: bool = True) -> bool:
        if self.claims.shop_id != getattr(target, "shop_id", None):
            if raise_exception:
                raise ForbiddenException("You are not allowed to access this resource")
            return False
        return True
