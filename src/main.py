from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from src.routes import chat_route, db_route, qdrant_route, env_route    
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    # return RedirectResponse(url="/docs/")
    return FileResponse("static/index.html")
    

@app.get("/health")
async def health():
    return {"status": "healthy"}
 
app.include_router(chat_route.router)
# app.include_router(db_route.router)
app.include_router(qdrant_route.router)
app.include_router(env_route.router)


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)