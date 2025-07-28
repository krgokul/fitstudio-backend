from fastapi import FastAPI
from app import models, database
from app.routes import user_route

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FitStudio Booking API")

app.include_router(user_route.router, prefix="/api/users")
