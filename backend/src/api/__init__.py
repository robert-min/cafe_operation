import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

api_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(api_path, os.path.pardir))
lib_path = os.path.abspath(os.path.join(src_path, 'lib'))
if api_path not in sys.path:
    sys.path.append(api_path)
if lib_path not in sys.path:
    sys.path.append(lib_path)


def create_app():
    app = FastAPI()
    
    # router
    from auth import auth_router
    from item import item_router
    app.include_router(auth_router)
    app.include_router(item_router)

    # error handler
    @app.exception_handler(CustomHttpException)
    async def http_custom_exception_handler(request: Request, exc: CustomHttpException):
        content = {
            "meta": {
                "code": exc.code,
                "error": str(exc.error),
                "message": str(exc.error) + exc.message
            },
            "data": None

        }
        return JSONResponse(status_code=exc.code, content=content)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


class CustomHttpException(Exception):
    def __init__(self, code: int, error: Exception, message: str = "") -> None:
        self.code = code
        self.error = error
        self.message = message
