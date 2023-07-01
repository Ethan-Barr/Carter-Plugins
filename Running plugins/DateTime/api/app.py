from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Response
from typing import Optional
import uvicorn

from datetime import datetime
import dotenv
import os

from models import PluginRequest, PluginResponse, EmptyData


app = FastAPI()

dotenv.load_dotenv()
DevID = os.environ["DevID"]


@app.get("/")
def api():
    return "Running on Vercel"


class PluginException(Exception):
    def __init__(self, error: str, forced_response: Optional[str] = None):
        self.error = error
        self.forced_response = forced_response


@app.exception_handler(PluginException)
def plugin_exception_handler(request: Request, exc: PluginException):
    return JSONResponse(
        status_code=200,
        content=PluginResponse[None](
            success=False,
            data=None,
            error=exc.error,
            forced_response=(exc.forced_response if exc.forced_response is not None
                            else None)).dict(exclude_none=True))


@app.middleware("http")
async def verify_secret_token(request: Request, call_next):
    print("Active22")
    secret_token = os.getenv('CARTER_PLUGIN_SECRET_TOKEN')
    if secret_token is not None and request.url.path not in [
        "/carterplugin.json", "/docs", "/openapi.json"
    ]:
        if "X-Carter-Plugin-Secret-Token" not in request.headers:
            return Response(status_code=401)
        if request.headers["X-Carter-Plugin-Secret-Token"] != secret_token:
            return Response(status_code=403)
    return await call_next(request)


@app.get("/carterplugin.json")
async def manifest():
    return {
        "manifest_version": "1",
        "developer_id": DevID,
        "version": "1.1.1",
        "name": "datetime",
        "name_for_human": "Datetime Plugin",
        "name_for_machine": "datetime",
        "description_for_human": "Get the current date and time.",
        "description_for_machine": "Get the current date and time.",
        "author_name": "Ethan Barr",
        "contact_email": "ethanwbarr07@gmail.com",
        "api": {
            "base_url": "https://carter-plugins-datetime.vercel.app/api",
            "endpoints": [
                {
                    "name": "get_current_time_uk",
                    "description": "Get the current date and time.",
                    "path": "/get_current_time_uk",
                    "input": [
                        {
                            "name": "current_time",
                            "type": "string",
                            "required": True,
                            "description": "Collecting the current time",
                            "example": "What is the time"
                        }
                    ],
                    "output": [
                        {
                            "name": "current_time",
                            "type": "string",
                            "description": "The current date and time in ISO 8601 format.",
                            "example": "2023-06-30T15:25:00"
                        }
                    ]
                },
                {
                    "name": "get_current_date_uk",
                    "description": "Get the current date.",
                    "path": "/get_current_date_uk",
                    "input": [],
                    "output": [
                        {
                            "name": "current_date",
                            "type": "string",
                            "description": "The current date in ISO 8601 format.",
                            "example": "2023-06-30"
                        }
                    ]
                }
            ]
        }
    }


# Plugin code
@app.post("/api/get_current_time_uk", response_model=PluginResponse, response_model_exclude_none=True)
async def get_current_time_uk(request: PluginRequest[EmptyData]):
    current_datetime = datetime.now().strftime("%H:%M:%S")
    response = PluginResponse(
        success=True, data={"current_time": current_datetime})
    return response


@app.post("/api/get_current_date_uk", response_model=PluginResponse, response_model_exclude_none=True)
async def get_current_date_uk(request: PluginRequest[EmptyData]):
    current_date = datetime.now().strftime("%Y-%m-%d")
    response = PluginResponse(
        success=True, data={"current_date": current_date})
    return response



# if __name__ == '__main__':
#     uvicorn.run("app:app", host="0.0.0.0", port=5002, reload=True)
