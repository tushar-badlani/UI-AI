import os

from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def generate(prompt):
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=prompt
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            properties = {
                "html": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "css": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "js": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(
                text="""I will give you a prompt describing an ui componennt you will return an html and css code for that component, do not include anything else in the output
"""
            ),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )

    print(response.text, end="")

    return response.text


