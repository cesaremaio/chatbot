from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.routes import chat_route, db_route, qdrant_route, env_route, auth_route
from src.app_settings import settings   
import uvicorn

app = FastAPI()

HOST = str( settings.host )
PORT = str( settings.port )

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://127.0.0.1:{PORT}", f"http://{HOST}:{PORT}"],  # Add your frontend origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/health")
async def health():
    return {"status": "healthy"}
 
app.include_router(chat_route.router)
app.include_router(qdrant_route.router)
app.include_router(env_route.router)
app.include_router(db_route.router)
app.include_router(auth_route.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
# Serve the main frontend page

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))