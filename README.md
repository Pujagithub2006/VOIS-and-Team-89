# VOIS Companion (Elderly-friendly Chatbot)

Simple Flask + static frontend chatbot designed for older users.

Quick start

1. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows PowerShell
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the backend (serves the frontend too):

```bash
python backend/app.py
```

4. Open the app in your browser:

http://127.0.0.1:5000/

Troubleshooting
- If you see an import error for `flask_cors`, run `pip install Flask-Cors`.
- If the page doesn't load, check terminal output for traceback; common cause is port already in use.

Files of interest
- `backend/app.py` — Flask server and `/chat` API.
- `frontend/test.html` — Chat UI.
interface.

Next improvements
- Add audio input for users who prefer speaking.
- Add persistent message history or caregiver notifications for emergency phrases.
