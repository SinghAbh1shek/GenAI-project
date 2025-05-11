import os
from dotenv import load_dotenv
from speech_module import speech_recognizer
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("❌ GOOGLE_API_KEY not found in .env file.")

client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

class messageType(BaseModel):
    res: str

def message():
    systemPrompt = """
    You are an helpful AI assistant who specialised in summarize user prompt in meaningful way.

    Instruction:
        - Always gives output in string
        - Always gives output meaningful because I have to pass that in voice model
        - Always gives output that contain maximum 20 words
    
    Example:
        Input: The `write_file` function is supposed to create the file. Can you check your file system to see if the file exists? If it doesn't, there may be a problem with the underlying system's file access permissions or a bug in the `write_file` function itself (which is outside my control).
        Output: Check if the file already exist or has bugs causing system to fails.

        Input: I have created an empty file named `test.py`.  Do you want me to add any content to it?
        Output: I have created the file. Do you want me to add content?
    """

    try:
        user_input = speech_recognizer()
        if not user_input:
            return "❌ No input captured from speech."

        print("🎙️ Recognized Speech:", user_input)

        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": user_input}
            ]
        )

        try:
            content = response.choices[0].message.content.strip()
            validated = messageType(res=content)
            return validated.res
        except (AttributeError, IndexError, ValidationError) as parse_error:
            return f"❌ Response parsing failed: {parse_error}"

    except Exception as e:
        return f"❌ Unexpected error: {e}"
