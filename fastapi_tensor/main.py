from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from router import home

app = FastAPI()

app.include_router(home.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)