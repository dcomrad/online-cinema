from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException

from .permissions import SUPERUSER_PERMISSION


def login_required(required_permission: None | str = None):
    """Декоратор для авторизации пользователя по jwt токену. Если установлен
    параметр required_permission, то в случае отсутствия указанного разрешения
    в списке разрешений пользователя, находящемся в jwt токене, выбрасывается
    исключение."""
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            authorize = kwargs.get('authorize')
            if authorize is None:
                msg = ('Set "authorize: AuthJWT = Depends()" as the '
                       f'"{func.__name__}" function parameter')
                raise ValueError(msg)

            await authorize.jwt_required()

            if required_permission:
                raw_jwt = await authorize.get_raw_jwt()
                user_permissions = raw_jwt.get('perm')
                _check_permission(user_permissions, required_permission)

            return await func(*args, **kwargs)
        return inner
    return wrapper


def _check_permission(
        user_permissions: str | list[str],
        required_permission: str
) -> None:
    """Проверяет наличие требуемого разрешения, среди списка
    пользовательских."""
    allowed_permissions = {SUPERUSER_PERMISSION, required_permission}
    user_permissions = [user_permissions] if isinstance(user_permissions, str) else user_permissions  # noqa:E501

    if not allowed_permissions & set(user_permissions):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Permission denied'
        )
