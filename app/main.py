from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.db import engine
from app.routers import users, auth
from app.schemas import Prompt, SuggestIN
from app.util import generate_html_css, generate_inline, generate_finetuned, generate_suggestion

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
@app.get("/")
async def root():
    return {"message": "welcome to my api!!"}


@app.post("/html")
async def generate_component(prompt: Prompt):
    response = generate_html_css(prompt.prompt)

    return eval(response)


@app.post("/inline")
async def generate_inline_components(prompt: Prompt):
    response = generate_inline(prompt.prompt)

    return eval(response)


@app.post("/finetuned")
async def generated_using_finetune(prompt: Prompt):
    response = generate_finetuned(prompt.prompt)
    result = {"html": response}
    return result


@app.post("/suggest")
async def suggest(prompt: SuggestIN):
    response = generate_suggestion(prompt.prompt, prompt.html)

    return eval(response)


app.include_router(users.router)

app.include_router(auth.router)
