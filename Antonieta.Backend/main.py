from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
import os
from controllers.beneficiary_controller import router as beneficiary_router
from controllers.ration_controller import router as ration_router
from controllers.distribution_controller import router as distribution_router

app = FastAPI(title="Antonieta API", version="1.0.0")

# Create database tables on startup
create_tables()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(beneficiary_router)
app.include_router(ration_router)
app.include_router(distribution_router)