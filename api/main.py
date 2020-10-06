import os
import aiof.config as config
import aiof.helpers as helpers

from aiof.data.asset import ComparableAsset
from api.routers import fi, car

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from functools import lru_cache


app = FastAPI()


@lru_cache()
def settings():
    return config.Settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().cors_origins,
    allow_credentials=True,
    allow_methods=settings().cors_allowed_methods,
    allow_headers=settings().cors_allowed_headers,
)


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
    return helpers._frequency


@app.get("/api/app/settings")
async def info(settings: config.Settings = Depends(settings)):
    return {
        "aiof_portal_url": settings.aiof_portal_url,
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
