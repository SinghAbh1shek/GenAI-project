### 🔧 Setup Instructions

#### 1. Install `uv` (if not installed)

`uv` is a fast Python package manager. To install it:



```bash
pip install uv
```

---

#### 2. Install Dependencies

```bash
uv sync
```

This will install all dependencies listed in `pyproject.toml`.

---

#### 3. Set Environment Variables

Create a .env file using the .env.sample as a reference. Add your Gemini and OpenAI API keys to it. Make sure the environment file contains the required variable names exactly as shown in the sample.

---

#### 4. Run the Script

```bash
uv run text-to-speech.py
```

This will run the main text-to-speech functionality.

