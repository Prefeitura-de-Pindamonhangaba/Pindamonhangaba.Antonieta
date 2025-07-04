from fastapi import FastAPI
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

load_dotenv()

port = int(getenv('PORT', 5000))

app = FastAPI(title="Antonieta API", version="1.0.0")

# CORS Configuration
origins = getenv('CORS_ORIGINS').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

app.include_router(auth_router)
app.include_router(beneficiary_router)
app.include_router(ration_stock_router)
app.include_router(distribution_router)
app.include_router(ration_input_router)
app.include_router(dashboard_router)


if __name__ == "__main__":
    uvicorn.run(app, host=(os.getenv('HOST')), port=int(os.getenv('PORT')))