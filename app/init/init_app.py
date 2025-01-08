from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config.setting import settings
from app.core.context_manager import context
from app.core.error_handler import DeniedError, CommonServerError
from app.items.response_item import error_response

app = FastAPI(
    title=settings.app.name,
    description=settings.app.desc,
    version="1.0.0",
    lifespan=context,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常捕获
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Internal Server Error"}
    )


@app.exception_handler(CommonServerError)
async def common_error_handler(request: Request, e: CommonServerError):
    """
    自定义异常捕获
    :param request:
    :param e:
    :return:
    """
    return JSONResponse(content=error_response(e.code, e.message, e.error_msg).dict())


@app.exception_handler(DeniedError)
async def denied_error_handler(request: Request, e: DeniedError):
    """
    自定义异常捕获
    :param request:
    :param e:
    :return:
    """
    return JSONResponse(status_code=403, content=error_response(e.code, e.message, e.error_msg).dict())
