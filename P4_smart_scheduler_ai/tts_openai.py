import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from summerizer import summerizer

load_dotenv()
openai = AsyncOpenAI()

async def main() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=summerizer(),
        instructions="Voice: High-energy, upbeat, and encouraging, projecting enthusiasm and motivation.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

while True:
    if __name__ == "__main__":
        asyncio.run(main())
