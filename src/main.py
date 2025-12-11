#환경 변수
from config import settings

#FastAPI
from fastapi import FastAPI
from src.routers import health

import uvicorn



## 서버실행
PORT_NUM = settings.PORT_NUM

app = FastAPI()
app.include_router(health.router)

@app.get("/")
async def root():
    return ("message: Server is running")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=PORT_NUM, reload=True)
    