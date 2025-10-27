
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=ENV_PATH)
except Exception:
    # If python-dotenv isn't installed, os.getenv will still work if the OS env var is set
    pass

# Assistant Configuration
ASSISTANT_NAME = "F.R.I.D.A.Y"

# Porcupine Hotword Detection
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "").strip()

# Weather API (OpenWeatherMap)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

# News API
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()

# Wolfram Alpha
WOLFRAMALPHA_APP_ID = os.getenv("WOLFRAMALPHA_APP_ID", "").strip()

# Email Configuration (Gmail)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()

# Google Calendar API
GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "credentials.json").strip()

# Geocoding API (Optional)
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY", "").strip()

# Validate critical keys and provide warnings
if not PORCUPINE_ACCESS_KEY:
    print("⚠️  Warning: PORCUPINE_ACCESS_KEY not found in .env file")

if not OPENWEATHER_API_KEY:
    print("⚠️  Warning: OPENWEATHER_API_KEY not found in .env file (Weather feature disabled)")

if not NEWS_API_KEY:
    print("⚠️  Warning: NEWS_API_KEY not found in .env file (News feature disabled)")

if not WOLFRAMALPHA_APP_ID:
    print("⚠️  Warning: WOLFRAMALPHA_APP_ID not found in .env file (Wolfram Alpha disabled)")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("⚠️  Warning: EMAIL credentials not found in .env file (Email feature disabled)")

# Debug: Print loaded configuration (optional, comment out in production)
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("CONFIGURATION LOADED")
    print("=" * 50)
    print(f"Assistant Name: {ASSISTANT_NAME}")
    print(f"Porcupine Key: {'✅ Loaded' if PORCUPINE_ACCESS_KEY else '❌ Missing'}")
    print(f"Weather API: {'✅ Loaded' if OPENWEATHER_API_KEY else '❌ Missing'}")
    print(f"News API: {'✅ Loaded' if NEWS_API_KEY else '❌ Missing'}")
    print(f"Wolfram Alpha: {'✅ Loaded' if WOLFRAMALPHA_APP_ID else '❌ Missing'}")
    print(f"Email Config: {'✅ Loaded' if EMAIL_ADDRESS and EMAIL_PASSWORD else '❌ Missing'}")
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=ENV_PATH)
except Exception:
    # If python-dotenv isn't installed, os.getenv will still work if the OS env var is set
    pass

# Assistant Configuration
ASSISTANT_NAME = "F.R.I.D.A.Y"

# Porcupine Hotword Detection
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "").strip()

# Weather API (OpenWeatherMap)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

# News API
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()

# Wolfram Alpha
WOLFRAMALPHA_APP_ID = os.getenv("WOLFRAMALPHA_APP_ID", "").strip()

# Email Configuration (Gmail)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()

# Google Calendar API
GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "credentials.json").strip()

# Geocoding API (Optional)
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY", "").strip()

# Validate critical keys and provide warnings
if not PORCUPINE_ACCESS_KEY:
    print("⚠️  Warning: PORCUPINE_ACCESS_KEY not found in .env file")

if not OPENWEATHER_API_KEY:
    print("⚠️  Warning: OPENWEATHER_API_KEY not found in .env file (Weather feature disabled)")

if not NEWS_API_KEY:
    print("⚠️  Warning: NEWS_API_KEY not found in .env file (News feature disabled)")

if not WOLFRAMALPHA_APP_ID:
    print("⚠️  Warning: WOLFRAMALPHA_APP_ID not found in .env file (Wolfram Alpha disabled)")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("⚠️  Warning: EMAIL credentials not found in .env file (Email feature disabled)")

# Debug: Print loaded configuration (optional, comment out in production)
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("CONFIGURATION LOADED")
    print("=" * 50)
    print(f"Assistant Name: {ASSISTANT_NAME}")
    print(f"Porcupine Key: {'✅ Loaded' if PORCUPINE_ACCESS_KEY else '❌ Missing'}")
    print(f"Weather API: {'✅ Loaded' if OPENWEATHER_API_KEY else '❌ Missing'}")
    print(f"News API: {'✅ Loaded' if NEWS_API_KEY else '❌ Missing'}")
    print(f"Wolfram Alpha: {'✅ Loaded' if WOLFRAMALPHA_APP_ID else '❌ Missing'}")
    print(f"Email Config: {'✅ Loaded' if EMAIL_ADDRESS and EMAIL_PASSWORD else '❌ Missing'}")