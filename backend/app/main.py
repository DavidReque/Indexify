from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from api.routes.routes import router

load_dotenv()

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL"),
    os.getenv("FRONTEND_URL_LOCAL"),
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Rutas
@app.get("/")
async def root():
    return {"message": "API running"}

app.include_router(router)  # Use router instead of routes