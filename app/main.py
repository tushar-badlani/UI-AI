from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import Prompt
from app.util import generate_html_css, generate_inline

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
