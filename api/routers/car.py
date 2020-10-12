from fastapi import APIRouter


router = APIRouter()


@router.get("/test/car", tags=["car"])
async def car():
    return [{"name": "Mazda"}, {"model": "3"}]