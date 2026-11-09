from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
import os
import uvicorn
from controllers.beneficiary_controller import router as beneficiary_router
from controllers.ration_stock_controller import router as ration_stock_router
from controllers.distribution_controller import router as distribution_router
from controllers.auth_controller import router as auth_router
from controllers.ration_input_controller import router as ration_input_router
from controllers.dashboard_controller import router as dashboard_router
from controllers.user_controller import router as user_router
from controllers.audit_controller import router as audit_router
from controllers.report_controller import router as report_router
from services.auth_service import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

load_dotenv()

port = int(getenv('PORT', 5000))

app = FastAPI(
    title="Antonieta API", version="1.0.0",
    docs_url=None, redoc_url=None, openapi_url=None,
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(status_code=409, content={
        "detail": "A operação conflita com um registro existente ou vinculado."
    })

# CORS Configuration
origins = [origin.strip() for origin in getenv('CORS_ORIGINS', 'http://localhost:3000').split(',') if origin.strip()]
if '*' in origins:
    raise ValueError('CORS_ORIGINS deve listar origens explícitas')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

app.include_router(auth_router)
protected_router = APIRouter(dependencies=[Depends(get_current_user)])
protected_router.include_router(user_router)
protected_router.include_router(audit_router)
protected_router.include_router(beneficiary_router)
protected_router.include_router(ration_stock_router)
protected_router.include_router(distribution_router)
protected_router.include_router(ration_input_router)
protected_router.include_router(dashboard_router)
protected_router.include_router(report_router)
app.include_router(protected_router)


if __name__ == "__main__":
    uvicorn.run(app, host=(os.getenv('HOST')), port=int(os.getenv('PORT')))
