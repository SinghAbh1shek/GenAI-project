import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
# from summerizer import summerizer
from tools import speech_recognizer

load_dotenv()
openai = AsyncOpenAI()







instructions = """Voice: Warm, upbeat, and reassuring, with a steady and confident cadence that keeps the conversation calm and productive.
Tone: Positive and solution-oriented, always focusing on the next steps rather than dwelling on the problem.
Dialect: Neutral and professional, avoiding overly casual speech but maintaining a friendly and approachable style.
Pronunciation: Clear and precise, with a natural rhythm that emphasizes key words to instill confidence and keep the customer engaged.
Features: Uses empathetic phrasing, gentle reassurance, and proactive language to shift the focus from frustration to resolution."""

async def main() -> None:
    try:
        async with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=speech_recognizer(),
            # input=summerizer(),
            instructions=instructions,
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)
    except:
        pass

while True:
    if __name__ == "__main__":
        asyncio.run(main())
