import time
import aiof.config as config
import aiof.helpers as help

from aiof.data.asset import ComparableAsset
from api.routers import helpers, fi, car, analytics, market, property, retirement, goal

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from logzero import logger


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=config.get_settings().cors_allowed_methods,
    allow_headers=config.get_settings().cors_allowed_headers,
)


@app.exception_handler(ValueError)
async def unicorn_exception_handler(req: Request, ve: ValueError):
    return write_exception_response(status_code=400, message=ve)

def write_exception_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "code": status_code,
            "message": f"{message}"
            },
    )

@app.middleware("http")
async def exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(e)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = int(round((time.time() - start_time) * 1000))
    logger.info("Request Host={0} | Url={1} | Time={2}ms".format(request.client.host, request.url, str(process_time)))
    return response


@app.get("/health")
async def health_check():
    return "Healthy"


@app.post("/api/asset/breakdown")
async def asset_breakdown(asset: ComparableAsset):
    return help.asset_breakdown(asset)


@app.get("/api/frequencies")
async def frequencies():
    return config.get_settings().Frequencies

@app.get("/api/frequencies/map")
async def frequencies_map():
    return config.get_settings().FrequenciesMap

@app.get("/api/app/settings")
async def info(settings: config.Settings = Depends(config.get_settings)):
    return settings


app.include_router(
    helpers.router,
    prefix="/api/helpers",
    tags=["helpers"])

app.include_router(
    fi.router,
    prefix="/api/fi",
    tags=["fi"])

app.include_router(
    car.router, 
    prefix="/api/car",
    tags=["car"])

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["analytics"])

app.include_router(
    market.router,
    prefix="/api/market",
    tags=["market"])

app.include_router(
    property.router,
    prefix="/api/property",
    tags=["property"])

app.include_router(
    retirement.router,
    prefix="/api/retirement",
    tags=["retirement"])
    
app.include_router(
    goal.router,
    prefix="/api/goal",
    tags=["goal", "goals"])