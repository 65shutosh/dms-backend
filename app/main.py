from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import auth 

app = FastAPI(title=settings.APP_NAME)

# Include versioned API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Delivery Management System API is running"}
