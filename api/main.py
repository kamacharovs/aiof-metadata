import time
from warnings import catch_warnings
import aiof.config as config
import aiof.helpers as helpers

from aiof.data.asset import ComparableAsset
from api.routers import fi, car, analytics, market, house

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from logzero import logger


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=config.get_settings().cors_allowed_methods,
    allow_headers=config.get_settings().cors_allowed_headers,
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
    return helpers.asset_breakdown(asset)

@app.get("/api/asset/breakdown/csv")
async def export_asset_fv_breakdown_as_table_to_csv():
    df = helpers.asset_fv_breakdown_as_table(
        asset_value=15957,
        contribution=500,
        years=15,
        rate=(8/100)/12,
        frequency=12,
    )
    response = StreamingResponse(helpers.export_to_csv(df),
                                media_type="text/csv")
    return response 


@app.get("/api/frequencies")
async def frequencies():
    return config.get_settings().Frequencies
@app.get("/api/frequencies/map")
async def frequencies_map():
    return config.get_settings().FrequenciesMap


@app.get("/api/app/settings")
async def info(settings: config.Settings = Depends(config.get_settings)):
    return {
        "cors_origins": settings.cors_origins,
    }


app.include_router(
    fi.router,
    prefix="/api/fi",
    tags=["fi"]
)

app.include_router(
    car.router, 
    prefix="/api/car",
    tags=["car"])

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["analytics"]
)

app.include_router(
    market.router,
    prefix="/api/market",
    tags=["market"])

app.include_router(
    house.router,
    prefix="/api/house",
    tags=["house"])