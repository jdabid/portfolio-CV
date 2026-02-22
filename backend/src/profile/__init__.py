from fastapi import APIRouter

from .create_profile import router as create_profile_router

router = APIRouter(prefix="/profile")
router.include_router(create_profile_router)
