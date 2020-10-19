from fastapi import APIRouter


router = APIRouter()


@router.get("/test/car")
async def car():
    return [{"name": "Mazda"}, {"model": "3"}]