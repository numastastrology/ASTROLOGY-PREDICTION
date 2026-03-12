from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from astro_predictor_app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Backend for Astrology Prediction App"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from astro_predictor_app.app.routes import input, prediction, report, profiles

app.include_router(input.router)
app.include_router(prediction.router)
app.include_router(report.router)
app.include_router(profiles.router)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="astro_predictor_app/app/static"), name="static")

from fastapi.responses import HTMLResponse

@app.get("/")
def read_root():
    with open('astro_predictor_app/app/static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"})
