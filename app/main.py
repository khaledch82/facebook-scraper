from fastapi import FastAPI
import router as scraperApi

app = FastAPI()
app.include_router(scraperApi.app)