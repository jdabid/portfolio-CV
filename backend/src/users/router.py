from fastapi import APIRouter

from src.users.get_profile.endpoint import router as get_profile_router
from src.users.login.endpoint import router as login_router
from src.users.register.endpoint import router as register_router

router = APIRouter(prefix="/api/users", tags=["users"])
router.include_router(register_router)
router.include_router(login_router)
router.include_router(get_profile_router)
