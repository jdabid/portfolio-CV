from fastapi import APIRouter

from .create_profile import router as create_profile_router
from .get_profile import router as get_profile_router

router = APIRouter(prefix="/profile")
router.include_router(create_profile_router)
router.include_router(get_profile_router)
