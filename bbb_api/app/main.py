from fastapi import FastAPI

from app.routers import candidates_routers, applications_routers, questions_routers, answers_routers

app = FastAPI(
    title="BBB API",
    description="API de inscrições para o Big Brother Brasil",
    version="0.1.0",
    contact={
        "name": "Samuel Edson",
        "email": "samueledson.ti@gmail.com"
    }
)

# Incluindo os routers
app.include_router(candidates_routers.router)
app.include_router(applications_routers.router)
app.include_router(answers_routers.router)
app.include_router(questions_routers.router)
