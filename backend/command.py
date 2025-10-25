import time
import pyttsx3
import speech_recognition as sr
import eel

def safe_eel_call(func_name, *args):
    try:
        func = getattr(eel, func_name, None)
        if func:
            func(*args)
    except Exception as e:
        print(f"Eel call error ({func_name}): {str(e)}")

def speak(text):
    try:
        text = str(text)
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            if len(voices) > 2:
                engine.setProperty('voice', voices[2].id)
            engine.setProperty('rate', 174)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
        
        safe_eel_call('DisplayMessage', text)
        safe_eel_call('receiverText', text)
    except Exception as e:
        print(f"Error in speak: {str(e)}")

def takecommand():
    try:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("I'm listening...")
                safe_eel_call('DisplayMessage', "I'm listening...")
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, 10, 8)
        except Exception as e:
            print(f"Microphone error: {str(e)}")
            safe_eel_call('DisplayMessage', "Microphone error")
            return None
        
        try:
            print("Recognizing...")
            safe_eel_call('DisplayMessage', "Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
            safe_eel_call('DisplayMessage', query)
            speak(query)
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            safe_eel_call('DisplayMessage', "Sorry, I didn't catch that")
            return None
        except sr.RequestError as e:
            print(f"Google API error: {str(e)}")
            safe_eel_call('DisplayMessage', "API error")
            return None
    except Exception as e:
        print(f"Error in takecommand: {str(e)}")
        return None



@eel.expose
def takeAllCommands(message=None):
    try:
        query = None
        
        if message is None:
            query = takecommand()
            if not query:
                safe_eel_call('ShowHood')
                return
            print(query)
            safe_eel_call('senderText', query)
        else:
            query = message
            print(f"Message received: {query}")
            safe_eel_call('senderText', query)
        
        if query:
            try:
                if "open" in query:
                    from backend.feature import openCommand
                    openCommand(query)
                elif "send message" in query or "call" in query or "video call" in query:
                    from backend.feature import findContact, whatsApp
                    Phone, name = findContact(query)
                    if Phone != 0:
                        flag = ""
                        if "send message" in query:
                            flag = 'message'
                            speak("What message to send?")
                            message_text = takecommand()
                            if message_text:
                                query = message_text
                        elif "call" in query:
                            flag = 'call'
                        else:
                            flag = 'video call'
                        whatsApp(Phone, query, flag, name)
                elif "on youtube" in query:
                    from backend.feature import PlayYoutube
                    PlayYoutube(query)
                else:
                    from backend.feature import chatBot
                    chatBot(query)
            except ImportError as e:
                print(f"Module import error: {str(e)}")
                speak("Feature not available")
            except Exception as e:
                print(f"Command execution error: {str(e)}")
                speak("Sorry, something went wrong.")
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"Error in takeAllCommands: {str(e)}")
        speak("An error occurred. Please try again.")
    finally:
        safe_eel_call('ShowHood')
