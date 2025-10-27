import pyttsx3
import eel

# Yeh function pehle command.py me tha
def safe_eel_call(func_name, *args):
    """Safely call a JavaScript function."""
    try:
        func = getattr(eel, func_name, None)
        if func:
            func(*args)
    except Exception as e:
        print(f"Eel call error ({func_name}): {str(e)}")

# Yeh function bhi pehle command.py me tha
def speak(text):
    """Convert text to speech and display it on the UI."""
    try:
        text = str(text)
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            if len(voices) > 2:
                engine.setProperty('voice', voices[2].id)
            engine.setProperty('rate', 170)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
        
        # Ab yeh UI par message display karega
        safe_eel_call('DisplayMessage', text)
        safe_eel_call('receiverText', text)
    except Exception as e:
        print(f"Error in speak: {str(e)}")