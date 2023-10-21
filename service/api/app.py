from fastapi import FastAPI
from . import views

app = FastAPI()

app.include_router(views.router)
