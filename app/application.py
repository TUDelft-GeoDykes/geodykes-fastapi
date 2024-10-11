#!/usr/bin/env python
from dotenv import load_dotenv


load_dotenv()  # This line must come before importing any modules that use environment variables

from fastapi import Depends, FastAPI

from app import exceptions
from app.apps.dykes.views import router as dykes_router
from app.db.deps import set_db
from app.db.exceptions import DatabaseValidationError
from app.settings import settings


def get_app() -> FastAPI:
    _app = FastAPI(
        title=settings.service_name,
        debug=settings.debug,
        dependencies=[Depends(set_db)],
    )

    _app.include_router(dykes_router, prefix="/api")

    _app.add_exception_handler(
        DatabaseValidationError,
        exceptions.database_validation_exception_handler,  # type: ignore[arg-type]
    )

    return _app


application = get_app()
