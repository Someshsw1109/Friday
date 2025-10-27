import os
import eel
from pathlib import Path

try:
    from backend.auth import recoganize
    from backend.auth.recoganize import AuthenticateFace
    from backend.feature import play_assistant_sound
    from backend.talk import speak
    from backend.command import start_assistant  # ✅ IMPORT THIS
except ImportError as e:
    print(f"Error importing modules: {str(e)}")
    exit(1)

frontend_path = Path("frontend")
if not frontend_path.exists():
    print(f"Error: Frontend directory not found at {frontend_path}")
    exit(1)

eel.init("frontend")

@eel.expose
def init():
    """Initialize the assistant with face authentication"""
    try:
        print("=" * 50)
        print("Init function called from JavaScript")
        print("=" * 50)
        
        try:
            eel.hideLoader()
        except Exception as e:
            print(f"Error hiding loader: {e}")
        
        print("About to speak: Welcome to Friday")
        speak("Welcome to Friday")
        print("Finished speaking: Welcome to Friday")
        
        print("About to speak: Ready for Face Authentication")
        speak("Ready for Face Authentication")
        print("Finished speaking: Ready for Face Authentication")
        
        print("Starting face authentication...")
        flag = recoganize.AuthenticateFace()
        print(f"Face authentication result: {flag}")
        
        if flag == 1:
            print("Authentication successful")
            speak("Face recognized successfully")
            
            try:
                eel.hideFaceAuth()
            except Exception as e:
                print(f"Error hiding face auth: {e}")
            
            try:
                eel.hideFaceAuthSuccess()
            except Exception as e:
                print(f"Error hiding face auth success: {e}")
            
            speak("Welcome to Your Assistant")
            
            try:
                eel.hideStart()
            except Exception as e:
                print(f"Error hiding start: {e}")
            
            try:
                play_assistant_sound()
            except Exception as e:
                print(f"Error playing sound: {e}")
            
            # ✅ AUTOMATICALLY START CONTINUOUS MODE
            print("🚀 Starting continuous listening mode...")
            try:
                start_assistant()  # This will start the continuous loop
                print("✅ Continuous mode activated!")
            except Exception as e:
                print(f"Error starting assistant: {e}")
            
            return {"status": "success", "authenticated": True}
        else:
            print("Authentication failed")
            speak("Face not recognized. Please try again")
            return {"status": "success", "authenticated": False}
            
    except Exception as e:
        print(f"Error in init: {str(e)}")
        import traceback
        traceback.print_exc()
        speak("Authentication failed")
        return {"status": "error", "message": str(e)}

def start():
    """Start the Eel application"""
    try:
        try:
            play_assistant_sound()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")
        
        try:
            os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
        except Exception as e:
            print(f"Error starting browser: {str(e)}")
        
        try:
            eel.start("index.html", mode=None, host="localhost", port=8000, block=True)
        except Exception as e:
            print(f"Error starting eel server: {str(e)}")
            
    except Exception as e:
        print(f"Error in start: {str(e)}")

if __name__ == "__main__":
    start()