import aiof.market.core as mt

from fastapi import APIRouter


router = APIRouter()


@router.get("/spy")
async def get_spy():
    return mt.get_spy()