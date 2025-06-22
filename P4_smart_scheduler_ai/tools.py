from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)
import datetime
from langgraph.checkpoint.memory import InMemorySaver
import speech_recognition as sr
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create in-memory storage for agent memory
checkpointer = InMemorySaver() 

# Get Google Calendar credentials
credentials = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="credentials.json",
)

# Build the calendar API service
api_resource = build_resource_service(credentials=credentials)

# Create a calendar toolkit with the API
toolkit = CalendarToolkit(api_resource=api_resource)


# Get calendar tools
tools = toolkit.get_tools()


# Initialize the GPT-4o-mini model
llm = init_chat_model("gpt-4o-mini", model_provider="openai", api_key = OPENAI_API_KEY)

# Create an agent with the LLM, tools, and memory
agent_executor = create_react_agent(llm, tools, checkpointer=checkpointer)

# Configuration for thread ID (used for saving memory per session)
config = {
    "configurable": {
        "thread_id": "1"  
    }
}

# System prompt to guide the assistant’s behavior
system_prompt = f"""You are a helpful assistant that helps users manage their schedule. 
        Current time is {datetime.datetime.now()} use this time instead of call, and you Indian, Kolkata timezone.
        Before schedule any events always check if the slot available. If slot not available just response user with 'you are not available in that time'.
        If user doesn't give any title just make the best title by youself with helps of user input.
        

        Example:
        Input: "I need to schedule a meeting."
        Output: "Okay! How long should the meeting be?"
        Input: "1 hour."
        Output: "Got it. I'm checking for 1-hour slots. Do you have a preferred day or time?"
        Input: "Sometime on Tuesday afternoon." 
        Output: "Great. I have 2:00 PM or 4:30 PM available on Tuesday. Which one works for you?"

        Note: Keep your response short, simple, and easy to say aloud. Avoid using links, URLs, unusual symbols, or hard-to-pronounce words
        """

# Function to recognize speech and handle scheduling
def speech_recognizer():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:

            # Adjust for background noise
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2

            print("Say something!")
            # Listen to user's voice input
            audio = r.listen(source)

            # Convert speech to text
            sst = r.recognize_google(audio)
            print("Processing audio...")
            print("You Said:", sst)

        # Send user input to the agent for response
        events = agent_executor.invoke(
            {"messages": [("system", system_prompt), 
                    ("user", sst)]},
                    config

        )
        print(events['messages'][-1].content)
        return (events['messages'][-1].content)



    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# while True:      
#     speech_recognizer()