from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
from botocore.exceptions import ClientError
from app import models
from app.db import engine
from app.routers import users, auth, layouts, components
from app.schemas import Prompt, SuggestIN
from app.util import generate_html_css, generate_inline, generate_finetuned, generate_suggestion
import json
from datetime import datetime

# Get current timestamp in a readable format, e.g., 2025-08-26_14-30-45
timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

origins = ["*"]

s3_client = boto3.client('s3')
BUCKET_NAME = "html-ui-ai"

def upload_to_s3(content: str, filename: str, bucket: str) -> bool:
    try:
        s3_client.put_object(Bucket=bucket, Key=filename, Body=content, ContentType='text/html')
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False

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
    data = json.loads(response)
    html_content = data.get("html")
    if not html_content:
        return {"error": "No html content in response"}

    # Define filename, e.g. prompt-based or timestamp-based
    
    filename = f"generated_page_{timestamp}.html"

    # Upload html_content to S3 as a .html file
    success = upload_to_s3(html_content, filename, BUCKET_NAME)
    if not success:
        return {"error": "Failed to upload to S3"}

    return {"message": f"HTML file uploaded to S3 as {filename}"}
    


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
app.include_router(layouts.router)
app.include_router(auth.router)
app.include_router(components.router)
