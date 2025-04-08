from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from functools import wraps
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.utils.logger import Logger

class BaseExceptions:
    @staticmethod
    async def validation_exception_handler(request:Request, exc:RequestValidationError):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=BaseGeneralResponsesSchemas.ValidationError(other=exc.errors()).model_dump())

    @staticmethod
    async def http_exception_handler(request:Request, exc:StarletteHTTPException):
        if exc.status_code == 404:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=BaseGeneralResponsesSchemas.NotFoundError().model_dump())

        #* Handle other HTTP exceptions normally
        return None

    @staticmethod
    def database_exception_handler(
        operation:str,
        logger:Logger,
        fail_result_class:type[BaseServiceQueryResults.Fail] = BaseServiceQueryResults.Fail
    ):
        """Decorator to handle database-related exceptions consistently."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError as e:
                    logger.error("Database error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"A database error occurred while {operation}. Please try again later or contact administrator.",
                        other="Database operation failed"
                    )
                except Exception as e:
                    logger.error("Unexpected error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator.",
                        other="Internal processing error"
                    )
            return wrapper
        return decorator

    @staticmethod
    def service_exception_handler(
        operation:str,
        logger:Logger,
        fail_result_class:type[BaseServiceGeneralResults.Fail] = BaseServiceGeneralResults.Fail
    ):
        """Decorator to handle service-related exceptions consistently."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error("Unexpected error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator.",
                        other="Internal processing error"
                    )
            return wrapper
        return decorator