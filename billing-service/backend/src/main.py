from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.jwt import AuthJWT, AuthJWTException, authjwt_exception_handler
from src.api.v1.routers import v1_router
from src.config.config import settings

app = FastAPI(
    title=settings.app.name,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(v1_router)


@AuthJWT.load_config
def get_config():
    """Сервисная функция библиотеки fastapi-jwt-auth для загрузки настроек."""
    return settings.jwt


app.add_exception_handler(AuthJWTException, authjwt_exception_handler)