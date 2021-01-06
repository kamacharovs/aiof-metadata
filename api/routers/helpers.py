import aiof.helpers as helpers

from aiof.data.asset import Asset

from typing import List
from fastapi import APIRouter


router = APIRouter()


@router.post("/assets/to/df")
async def mortgage_calc(req: List[Asset]):
    return helpers.assets_to_df(req)