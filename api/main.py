import time
import aiof.config as config
import aiof.helpers as help

from aiof.data.asset import ComparableAsset
from api.routers import helpers, fi, car, analytics, market, property, retirement

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt, jwk
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

@app.get("/api/asset/breakdown/csv")
async def export_asset_fv_breakdown_as_table_to_csv():
    df = help.asset_fv_breakdown_as_table(
        asset_value=15957,
        contribution=500,
        years=15,
        rate=(8/100)/12,
        frequency=12,
    )
    response = StreamingResponse(help.export_to_csv(df),
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
        "defaults": {
            "rounding_digit": settings.DefaultRoundingDigit,
            "frequency": settings.DefaultFrequency,
            "interest": settings.DefaultInterest,
            "hys_interest": settings.DefaultHysInterest,
            "average_bank_interest": settings.DefaultAverageBankInterest,
            "investment_fee": settings.DefaultInvestmentFee,
            "tax_drag": settings.DefaultTaxDrag,
            "child": settings.DefaultChild
        },
        "cors": {
            "origins": settings.cors_origins,
            "allowed_methods": settings.cors_allowed_methods,
            "allowed_headers": settings.cors_allowed_headers
        },
        "types": {
            "asset": settings.AssetTypes,
            "liability": settings.LiabilityTypes
        }
    }


@app.get("/jwt/decode")
async def decode_async():
    settings = config.get_settings()
    print(settings.JwtPublicKey)
    payload = jwt.decode("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInB1YmxpY19rZXkiOiJiZDUzMTQ3OC0zYjM2LTRlZWEtODI4ZC1lODNlYWI3ZWEwNWMiLCJyb2xlIjoiQWRtaW4iLCJuYmYiOjE2MjA3NTU4MDQsImV4cCI6MTYyMDc1NjcwNCwiaWF0IjoxNjIwNzU1ODA0LCJpc3MiOiJhaW9mOmF1dGgiLCJhdWQiOiJhaW9mOmF1dGg6YXVkaWVuY2UifQ.PKWUXxs5ypWiHo4he9WHk7G0qAfi7GmPPKm1O5t30VZRKCeNjoR-sjXB3MG3yN9Rua--jG8payx6h_s0OSjvimeNxWDZS1dOfoZc1TntV0be_8teYRki8DX622u945xB3i4AbIdCMB2aigO62XfinuVWb0fPWXT0xFVRz_V3AgQ4LGT4QjqkIfhHu0VN2hJiT10LIMrjoWmAX5Mf9a4r3qY644coBusyug6iHnqqw9Q_ciieRngDGLosVOsM-lumgPUbf-u1VG4E4pvkVIiSLuX1ubkIp4Xi4IgVe0R-LVkPej_9xcBZ1Q5qpBSA3rS3gmNguLCpZ_YGx_cfChPwrw", settings.JwtPublicKey, algorithms=[settings.JwtAlgorithm])
    return payload

def openapi():
    if app.openapi_schema:
        return app.openapi_schema

    settings = config.get_settings()
    openapi_schema = get_openapi(
        title=settings.OpenApiTitle,
        version=settings.OpenApiVersion,
        description=settings.OpenApiDescription,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = openapi

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