from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
import os

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