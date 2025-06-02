from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()
@app.get("/")
async def root():
    return RedirectResponse(url="/docs/")
    

@app.get("/health")
async def health():
    return {"status": "healthy"}
 






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)