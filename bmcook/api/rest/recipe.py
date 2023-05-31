from fastapi import APIRouter

from .sample_data import RECIPES

router = APIRouter()


@router.get("/")
def get_recipes():
    return RECIPES