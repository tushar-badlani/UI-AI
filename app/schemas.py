from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str


class SuggestIN(BaseModel):
    prompt: str
    html: str
