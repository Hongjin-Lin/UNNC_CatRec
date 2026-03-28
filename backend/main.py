import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from routers import identify, cats, add_cat

load_dotenv()

app = FastAPI(title="UNNC CatRec API", version="0.1.0")

# Serve campus cat photos as static files
_library = Path(__file__).parent.parent / "campus_cats_library"
if _library.exists():
    app.mount("/static/cats", StaticFiles(directory=str(_library)), name="cat_photos")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")  #允许哪些网站访问后端,从环境变量/.env读取

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
