from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from utils.log import logger
from starlette.middleware.cors import CORSMiddleware
from app.core.initialize_bots import bots_set_webhook
from app.handler.chat import router
from utils.pulse_error import *


@asynccontextmanager
async def request_lifespan(fastapp: FastAPI):
	logger.info("ready start app, init msg...")
	await bots_set_webhook()
	yield
	logger.info("init msg finish, start app...")


app = FastAPI(
	lifespan=request_lifespan
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(router, tags=['Chat'])


@app.exception_handler(TGUserError)
async def validation_exception_handler(request: Request, exc: TGUserError):
	logger.debug(str(exc))
	return JSONResponse(content={})


@app.exception_handler(TGTypeError)
async def validation_exception_handler(request: Request, exc: TGTypeError):
	logger.debug(str(exc))
	return JSONResponse(content={})


@app.exception_handler(TGMessageError)
async def validation_exception_handler(request: Request, exc: TGMessageError):
	logger.debug(str(exc))
	return JSONResponse(content={})


@app.exception_handler(TGBotError)
async def validation_exception_handler(request: Request, exc: TGBotError):
	logger.error(str(exc))
	return JSONResponse(content={})


@app.exception_handler(OSPServerError)
async def validation_exception_handler(request: Request, exc: OSPServerError):
	logger.error(str(exc))
	return JSONResponse(content={})


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
	import traceback
	logger.error(traceback.print_exc())
	return JSONResponse(content={})


if __name__ == "__main__":
	import uvicorn
	
	uvicorn.run(app, host="0.0.0.0", port=8443)
