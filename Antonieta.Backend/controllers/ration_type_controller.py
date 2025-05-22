from fastapi import APIRouter
from routes.ration_type_routes import router as ration_type_routes

router = APIRouter(prefix="/ration_type", tags=["ration_type"])
router.include_router(ration_type_routes)