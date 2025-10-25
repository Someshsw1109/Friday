import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=ENV_PATH)
except Exception:
    # If python-dotenv isn't installed, os.getenv will still work if the OS env var is set
    pass

ASSISTANT_NAME = "F.R.I.D.A.Y"

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "").strip()