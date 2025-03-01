import os

from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def generate_html_css(prompt):
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
            type=genai.types.Type.OBJECT,
            required=["html", "css"],
            properties={
                "html": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "css": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "js": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(
                text="""I will provide you with prompts describing UI components, and you will generate the complete, 
                functional code implementation. Follow the style guidelines mentioned in prompt as strictly as 
                possible .Return only the necessary HTML, CSS, and JavaScript code without any explanations or 
                additional. Return empty string if html or css or  js is not needed in their part in json .The code should be modern, responsive, and follow best practices. Include proper 
                semantic HTML5 elements, CSS with flexbox/grid layouts, and clean JavaScript with ES6+ features where 
                appropriate. All code should be properly formatted and cross-browser compatible. Do not use any 
                external dependencies."""
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


def generate_inline(prompt):
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
            type=genai.types.Type.OBJECT,
            required=["html"],
            properties={
                "html": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(
                text="""I will provide you with prompts describing UI components, and you will generate the complete, 
                functional code implementation. Follow the style guidelines mentioned in prompt as strictly as 
                possible. Return the necessary HTML, CSS, and JavaScript code with inline css without any explanations or 
                additional.The code should be modern, responsive, and follow best practices. Include proper 
                semantic HTML5 elements, CSS with flexbox/grid layouts, and clean JavaScript with ES6+ features where 
                appropriate. All code should be properly formatted and cross-browser compatible. Do not use any 
                external dependencies."""
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
