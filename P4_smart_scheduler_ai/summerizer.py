from tools import speech_recognizer
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)
def summerizer():
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are a helpful AI assistant. The input you receive comes from another AI. Your job is to summarize it clearly and briefly so a human can easily understand it. Keep the summary short, simple, and easy to say aloud. 
                
                Note: Avoid using links, URLs, unusual symbols, or hard-to-pronounce words"""},
                {
                    "role": "user",
                    "content": speech_recognizer(),
                },
            ],
        )

        # print(completion.choices[0].message.content)
        return (completion.choices[0].message.content)
    except:
        return "You havn't say anything"
# while True:
#     summerizer()