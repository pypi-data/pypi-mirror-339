from fastapi import FastAPI
from app.routes.chunking_routes import router as chunking_router
from app.routes.root_routes import router as root_router

app = FastAPI()

app.include_router(chunking_router)
app.include_router(root_router)
