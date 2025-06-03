from fastapi import APIRouter
import os
from src.app_settings import settings


router = APIRouter(prefix="/env", tags=["env"])

@router.get("/")
def read_env_variable():
    return {key: getattr(settings, key) for key in vars(settings)}
