import time
import aiof.config as config
import aiof.helpers as help

from aiof.data.asset import ComparableAsset
from api.routers import helpers, fi, car, analytics, market, property, retirement

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt
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
async def uvicorn_exception_handler(req: Request, ve: ValueError):
    return write_exception_response(status_code=400, message=ve)

@app.exception_handler(JWTError)
async def unauthorized_handler_async(req: Request, jwte: JWTError):
    return write_exception_response(status_code=401, message="Unauthorized")

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
    except JWTError as jwte:
        logger.exception(jwte)


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
    payload = jwt.decode("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInB1YmxpY19rZXkiOiI1ODFmM2NlNi1jZjJhLTQyYTUtODI4Zi0xNTdhMmJmYWI3NjMiLCJyb2xlIjoiQWRtaW4iLCJuYmYiOjE2MjEzNjExNTksImV4cCI6MTYyMTM2MjA1OSwiaWF0IjoxNjIxMzYxMTU5LCJpc3MiOiJhaW9mOmF1dGgiLCJhdWQiOiJhaW9mOmF1dGg6YXVkaWVuY2UifQ.bPwWseUPSK-dIf3JkOL8xAwc1NgWM_WDpLIA6FCBJarWSJuch8UXAM08JyIJ0G1p6UWKnolRxSTPda69z0bOh2B2Qfj9tYkr6CmChA5cfsoau6gvHriXvOW4xO_M_fJ4FHN1fypcPddZpuFdvDq_55kiHVz0NLLAky38_q_GPDxMtrMXdxtJVmhuQqmrOHGCzixCaaJCF0NByQiVEo7LI9ZONHK3rORWVzQm73CyDPERdLnYgWv1mT7NSEhH-7QVEhvSSVJ1b5x2MH0alCRV9ciuxqrme1MHHNxPXIUUvUsBB0peSwwd-ZV2SYbhtahwqNSCqG6wwlmjRjVMEhUSwA", settings.JwtPublicKey, algorithms=[settings.JwtAlgorithm])
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