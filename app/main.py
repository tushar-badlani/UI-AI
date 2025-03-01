from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.util import generate

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


@app.post("/generate")
async def generate_component(prompt: str):
    return generate(prompt)
