import os
import sys
from fastapi import FastAPI
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
    from auth import auth_router
    app.include_router(auth_router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
