# 🧠 Smart Scheduler AI Agent

An intelligent, voice-enabled chatbot that helps you schedule meetings by talking naturally—just like a real assistant. It understands vague requests, checks your Google Calendar, suggests available times, and speaks back to you.

---

## 🎯 Features

* 🎤 **Voice Interaction**: Talk to the assistant using your microphone.
* 🗣️ **Natural-Sounding Voice Reply**: Uses OpenAI's real-time TTS to reply with spoken feedback.
* 📅 **Google Calendar Integration**: Schedules events, checks availability, and avoids conflicts.
* 🧠 **Memory Management**: Maintains conversation context using `LangGraph`’s `InMemorySaver`.
* ✍️ **Smart Summarization**: Summarizes the conversation in plain, speakable language before voicing.
* 🕒 **Smart Time Understanding**: Parses vague times like "later this week" or "after my last meeting".

---

## 🛠 Tech Stack

| Layer                      | Tool / Service                                       |
| -------------------------- | ---------------------------------------------------- |
| LLM (Conversational Brain) | OpenAI GPT-4o-mini (via `langchain`)                      |
| Memory Management          | LangGraph `InMemorySaver`                            |
| Calendar Access            | Google Calendar API via `langchain_google_community` |
| Speech-to-Text (STT)       | `speech_recognition` (Google Speech API)             |
| Text-to-Speech (TTS)       | OpenAI `gpt-4o-mini-tts`                             |

---

## 📦 Installation & Setup

### 1. Clone the Project

```bash
git clone https://github.com/SinghAbh1shek/GenAI-project.git
cd GenAI-project
cd P4_smart_scheduler_ai
```

---

### 2. Install Dependencies (Recommended: `uv`)

#### ✅ Option A: Using [`uv`](https://github.com/astral-sh/uv) (Fast & Secure)

1. Install `uv` (only once):

```bash
pip install uv
```

2. Sync dependencies from `pyproject.toml` (if present) or auto-resolve from the environment:

```bash
uv sync
```

> ⚡ `uv` is faster, more secure, and handles dependency resolution better than `pip`.

---

#### 🐍 Option B: Using `pip` (Fallback)

If you prefer or need to use `pip`, simply run:

```bash
pip install -r requirements.txt
```

> Ensure you're using Python **3.10 or newer**.

---

#### 🧩 Option C: Manual Installation

If any package fails to install or is missing, you can manually install it by running:

```bash
pip install <module-name>
```

> ⚠️ **Note:** Some packages like `pyaudio` may require extra system dependencies to be installed separately (e.g., PortAudio on Linux or Windows).

---
## 🔑 Google Calendar API Setup

This project uses OAuth2 to securely access your calendar.

### Steps to Generate `credentials.json`:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Calendar API**.
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials → OAuth client ID**.

   * Choose **Desktop App**.
6. Download the `credentials.json` file.
7. Place it in your project root folder.
8. Configure the OAuth consent screen:
    
    * Add your email as a Test User.

    * Add any other Google accounts that will be used to test calendar access as Test Users.

9. Share your Google Calendar with the test account email(s) you added, so the agent can access and manage events during testing.

10. On first run, a browser window will prompt you to authorize access with your Google account. After approval, a token.json file will be created automatically to store your access tokens.

---

## 📁 Project Structure

```
smart-scheduler-ai/
├── tools.py             # Calendar tool + speech recognizer + LangChain agent
├── summerizer.py        # Summarizes LLM output for TTS
├── tts_openai.py              # Runs TTS playback with OpenAI Audio API
├── credentials.json     # Your Google OAuth credentials (generated manually)
├── token.json           # Automatically created on first OAuth login
├── .env                 # Your OpenAI API key
├── README.md            # You're here
```

---

## ⚙️ .env Configuration

Create a `.env` file in your project folder:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ How to Use

### Run the voice assistant:

```bash
uv run .\tts_openai.py 
#or
python tts_openai.py
```

### Example Conversation Flow:

> 🧑 You: "I need to schedule a meeting."

> 🤖 Bot: "Okay! How long should the meeting be?"

> 🧑 You: "1 hour."

> 🤖 Bot: "Got it. Do you prefer any day or time?"

> 🧑 You: "Maybe Tuesday afternoon."

> 🤖 Bot: "You have 2 PM or 4:30 PM available. Which works?"

---

## 🧠 How It Works

### 1. `tools.py`

* Uses `speech_recognition` to convert your voice into text.
* Builds a **LangChain + LangGraph** agent that:

  * Uses GPT-4o-mini to manage scheduling logic.
  * Connects to Google Calendar via `CalendarToolkit`.
  * Uses `InMemorySaver` to persist conversation state.

### 2. `summerizer.py`

* Sends the bot's full response to GPT-4o again for summarization.
* This ensures replies are short, clear, and easy to say aloud.

### 3. `tts_openai.py`

* Streams the summarized message via OpenAI’s TTS (voice: `alloy`).
* Plays the audio locally using `LocalAudioPlayer`.

---

## ✅ Key Advantages

* 🧠 **Stateful Conversations**: Remembers previous user input like duration, time preferences, or context shifts.
* 🎧 **Natural Experience**: You speak, it listens. It speaks, you reply. No typing.
* 🗓 **Real Calendar Logic**: Confirms slot availability before scheduling.

---

## 🧪 Test Phrases

Try speaking these to test the assistant:

* "Book me for 45 minutes before my 6 PM meeting Friday."
* "Find time for a check-in after the kickoff event."
* "Let's do our usual sync-up next week."
* "I'm free late in the week, but not Friday."



---

## 🚀 Future Improvements

* **Add a Frontend UI:** Develop a web or mobile interface for a more intuitive and user-friendly experience, complementing the terminal-based voice assistant.
* **Enhanced Voice Interaction:** Integrate real-time voice input/output directly in the frontend for seamless conversations.
* **Visual Calendar View:** Show available slots and scheduled meetings visually for easier selection and management.
* **User Authentication & Profiles:** Allow multiple users to securely manage their calendars within the app.
* **Cross-Platform Support:** Extend accessibility across devices like smartphones, tablets, and desktops.

---