from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from errors import AppException
from logger import log_error

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handle(request: Request, exc: AppException):
    log_error(exc.message, request.url.path)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error(str(exc), request.url.path)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "path": request.url.path
        }
    )

@app.get("/safe")
def safe():
    return {"message": "All good 🚀"}


@app.get("/user-error")
def user_error():
    raise AppException("Invalid input provided", 400)


@app.get("/server-error")
def server_error():
    return 1 / 0