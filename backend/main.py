import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import identify, cats, add_cat

load_dotenv()

app = FastAPI(title="UNNC CatRec API", version="0.1.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(identify.router, prefix="/identify", tags=["identify"])
app.include_router(cats.router, prefix="/cats", tags=["cats"])
app.include_router(add_cat.router, prefix="/cats", tags=["cats"])


@app.get("/health")
def health():
    return {"status": "ok"}
