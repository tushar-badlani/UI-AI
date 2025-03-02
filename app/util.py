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



def generate_finetuned(prompt):
    client = genai.Client(
        api_key=api_key,
    )

    model = "tunedModels/ui-generator-2-icy8snjkqmwa"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=""""I will provide you with prompts describing UI components, and you will generate the complete, 
                functional code implementation. Follow the style guidelines mentioned in prompt as strictly as 
                possible. Return the necessary HTML, CSS, and JavaScript code with inline css without any explanations or 
                additional.The code should be modern, responsive, and follow best practices. Include proper 
                semantic HTML5 elements, CSS with flexbox/grid layouts, and clean JavaScript with ES6+ features where 
                appropriate. All code should be properly formatted and cross-browser compatible. Do not use any 
                external dependencies.""" + prompt
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )

    print(response.text, end="")

    return response.text


def generate_suggestion(prompt, html):
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=prompt + html
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=1000,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["suggestion"],
            properties={
                "suggestion": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(
                text="""I will provide you with a JSON file containing two parts: a prompt section and HTML code. 
                Please analyze both components and provide comprehensive UI/UX improvement suggestions. Focus on:

1. Visual hierarchy and layout optimization
2. Color scheme and typography recommendations
3. Accessibility improvements (WCAG compliance)
4. Responsive design considerations
5. User interaction patterns and navigation flow
6. Loading performance and optimization
7. Form design and input validation (if applicable)
8. Content organization and readability
9. Mobile-first approach suggestions
10. Interactive elements and micro-interactions

Please provide your suggestions in natural language, organized by priority, with clear explanations for each 
recommendation and their potential impact on user experience. Keep your suggestions concise and actionable."""
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
