import uvicorn
from fastapi import FastAPI

from app.routers import candidates_routers, applications_routers

app = FastAPI()


app.include_router(candidates_routers.router)
app.include_router(applications_routers.router)


@app.get("/")
async def root():
    return {
        "name": "BBB API",
        "version": "0.1.0",
        "author": "Samuel Edson",
        "author_email": "samueledson.ti@gmail.com",
        "description": "API de inscrições para o Big Brother Brasil"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

