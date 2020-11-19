import aiof.house.core as house

from fastapi import APIRouter


router = APIRouter()


@router.get("/mortgage")
async def mortgage_calc():
    return house.mortgage_calc()