from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from pydantic.error_wrappers import ValidationError

from src import events
from src.exception_handlers import validation_error_handler
from src.utils.openapi import CustomOpenAPIGenerator
from src.frontend.routers import router as frontend_router
from src.admin.routers import router as admin_router
from src.internal_auth.routers import router as internal_auth_router
from src.external_auth.routers import router as external_auth_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.title = 'Service for authentication by graphical password'
    app.description = ''
    app.version = '1.0.0'
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.include_router(router=frontend_router)
    app.include_router(router=admin_router, prefix='/api/v1')
    app.include_router(router=internal_auth_router, prefix='/api/v1')
    app.include_router(router=external_auth_router, prefix='/api/v1')
    app.add_event_handler('startup', events.on_startup)
    app.add_event_handler('shutdown', events.on_shutdown)
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.openapi = CustomOpenAPIGenerator(app)
    return app


app = get_app()
