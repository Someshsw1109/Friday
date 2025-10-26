import time
import pyttsx3
import speech_recognition as sr
import eel

# ✅ Global flag for continuous listening
LISTENING = True

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
    """Take voice command without speaking it back"""
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
            # ✅ DON'T speak back the command
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
    """Process commands - can be called from UI or continuous listening"""
    global LISTENING
    
    try:
        query = None
        
        if message is None:
            query = takecommand()
            if not query:
                safe_eel_call('ShowHood')
                return  # ✅ Don't stop, just return
            print(query)
            safe_eel_call('senderText', query)
        else:
            query = message
            print(f"Message received: {query}")
            safe_eel_call('senderText', query)
        
        if query:
            try:
                # ✅ CHECK FOR SLEEP/WAKE COMMANDS FIRST
                if "time to sleep" in query or "go to sleep" in query or "sleep friday" in query or "stop listening" in query or "sleep mode" in query:
                    speak("Okay, going to sleep mode. Say 'wake up Friday' or 'hello Friday' to activate me again.")
                    LISTENING = False
                    safe_eel_call('ShowHood')
                    return
                
                # ✅ CHECK FOR WAKE UP COMMAND
                if not LISTENING:
                    if "wake up" in query or "hello friday" in query or "hey friday" in query or "activate" in query:
                        LISTENING = True
                        speak("I'm awake and ready to help!")
                        safe_eel_call('ShowHood')
                        return
                    else:
                        # In sleep mode, ignore other commands
                        print("🔴 SLEEP MODE - Ignoring command")
                        return
                
                # Import all feature functions
                from backend.feature import (
                    openCommand, PlayYoutube, findContact, whatsApp, chatBot,
                    greet_user, tell_time, tell_date, get_weather, get_system_status,
                    search_wikipedia, google_search, get_news, play_music, calculate,
                    take_note, tell_joke, get_ip_address, switch_window, take_screenshot,
                    read_file, close_application, hide_file, unhide_file, delete_file,
                    get_instagram_info, ask_wolframalpha, send_email
                )
                
                # 1. GREET
                if "hello" in query or "hi friday" in query or "hey friday" in query or "hello friday" in query:
                    greet_user()
                
                # 2. TIME AND DATE
                elif "time" in query:
                    tell_time()
                
                elif "date" in query and ("what" in query or "today" in query or "tell" in query):
                    tell_date()
                
                # 5. WEATHER
                elif "weather" in query:
                    city = query.replace("weather", "").replace("in", "").replace("what", "").replace("is", "").replace("the", "").strip()
                    get_weather(city if city else None)
                
                # 7. SYSTEM STATUS
                elif "system status" in query or "battery" in query or ("cpu" in query and "usage" in query) or ("ram" in query and "usage" in query):
                    get_system_status()
                
                # 9. WIKIPEDIA
                elif "wikipedia" in query:
                    search_query = query.replace("wikipedia", "").replace("search", "").strip()
                    search_wikipedia(search_query)
                
                elif "who is" in query:
                    search_query = query.replace("who is", "").strip()
                    search_wikipedia(search_query)
                
                elif "what is" in query and not any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide']):
                    search_query = query.replace("what is", "").strip()
                    search_wikipedia(search_query)
                
                # 10. GOOGLE SEARCH
                elif "google search" in query or "search for" in query or "search on google" in query:
                    search_query = query.replace("google search", "").replace("search for", "").replace("search on google", "").replace("google", "").strip()
                    google_search(search_query)
                
                # 12. NEWS
                elif "news" in query or "headlines" in query:
                    get_news()
                
                # 13. PLAY MUSIC
                elif "play music" in query:
                    play_music()
                
                # 14. SEND EMAIL
                elif "send email" in query or ("email" in query and "send" in query):
                    speak("To whom should I send the email?")
                    recipient = takecommand()
                    if recipient:
                        speak("What is the subject?")
                        subject = takecommand()
                        if subject:
                            speak("What should I write in the email?")
                            content = takecommand()
                            if content:
                                send_email(recipient, subject, content)
                
                # 15. CALCULATE
                elif "calculate" in query or ("what is" in query and any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide'])):
                    calculate(query)
                
                # 16. WOLFRAM ALPHA
                elif "ask wolfram" in query or "wolfram" in query:
                    question = query.replace("ask wolfram", "").replace("wolfram", "").strip()
                    ask_wolframalpha(question)
                
                elif any(word in query for word in ["population", "capital", "distance", "convert", "how far", "how many"]):
                    ask_wolframalpha(query)
                
                # 17. TAKE NOTE
                elif "take note" in query or "make note" in query or "remember this" in query:
                    speak("What should I note down?")
                    note = takecommand()
                    if note:
                        take_note(note)
                
                # 18. JOKE
                elif "joke" in query or "make me laugh" in query:
                    tell_joke()
                
                # 19. IP ADDRESS
                elif "ip address" in query or "my ip" in query:
                    get_ip_address()
                
                # 20. SWITCH WINDOW
                elif "switch window" in query or "change window" in query:
                    switch_window()
                
                # 21. SCREENSHOT
                elif "screenshot" in query or "screen shot" in query or "take screenshot" in query:
                    if "name" in query or "save as" in query:
                        speak("What should I name the file?")
                        filename = takecommand()
                        if filename:
                            take_screenshot(filename + ".png")
                        else:
                            take_screenshot()
                    else:
                        take_screenshot()
                
                # 23. CLOSE APPLICATION
                elif "close" in query:
                    if "chrome" in query:
                        close_application("chrome")
                    elif "notepad" in query:
                        close_application("notepad")
                    elif "calculator" in query:
                        close_application("calc")
                    elif "edge" in query:
                        close_application("msedge")
                    elif "word" in query:
                        close_application("winword")
                    elif "excel" in query:
                        close_application("excel")
                
                # 32. READ FILE
                elif "read file" in query or ("read" in query and "file" in query):
                    speak("Which file should I read? Please provide the full path.")
                    filepath = takecommand()
                    if filepath:
                        read_file(filepath)
                
                # 33. FILE OPERATIONS
                elif "hide file" in query:
                    speak("Which file should I hide?")
                    filepath = takecommand()
                    if filepath:
                        hide_file(filepath)
                
                elif "show file" in query or "unhide file" in query:
                    speak("Which file should I unhide?")
                    filepath = takecommand()
                    if filepath:
                        unhide_file(filepath)
                
                elif "delete file" in query:
                    speak("Which file should I delete? Please confirm.")
                    filepath = takecommand()
                    if filepath:
                        speak("Are you sure you want to delete this file? Say yes to confirm.")
                        confirmation = takecommand()
                        if confirmation and "yes" in confirmation:
                            delete_file(filepath)
                        else:
                            speak("File deletion cancelled")
                
                # 24. INSTAGRAM
                elif "instagram" in query and ("profile" in query or "information" in query or "info" in query):
                    speak("Which Instagram username?")
                    username = takecommand()
                    if username:
                        get_instagram_info(username)
                
                # EXISTING COMMANDS
                elif "open" in query:
                    openCommand(query)
                
                elif "send message" in query or "whatsapp message" in query:
                    Phone, name = findContact(query)
                    if Phone != 0:
                        speak("What message should I send?")
                        message_text = takecommand()
                        if message_text:
                            whatsApp(Phone, message_text, 'message', name)
                
                elif "call" in query and "video" not in query:
                    Phone, name = findContact(query)
                    if Phone != 0:
                        whatsApp(Phone, "", 'call', name)
                
                elif "video call" in query:
                    Phone, name = findContact(query)
                    if Phone != 0:
                        whatsApp(Phone, "", 'video', name)
                
                elif "on youtube" in query or "play on youtube" in query:
                    PlayYoutube(query)
                
                # EMOTIONS
                elif "how are you" in query:
                    speak("I'm doing great! Thank you for asking. How can I help you today?")
                
                elif "thank you" in query or "thanks" in query:
                    speak("You're welcome! I'm always here to help.")
                
                elif "good job" in query or "well done" in query:
                    speak("Thank you! I'm glad I could help. Is there anything else you need?")
                
                # DEFAULT: CHATBOT
                else:
                    chatBot(query)
                    
            except ImportError as e:
                print(f"Module import error: {str(e)}")
                speak("Feature not available. Some dependencies might be missing.")
            except Exception as e:
                print(f"Command execution error: {str(e)}")
                import traceback
                traceback.print_exc()
                speak("Sorry, something went wrong.")
        
    except Exception as e:
        print(f"Error in takeAllCommands: {str(e)}")
        import traceback
        traceback.print_exc()
        speak("An error occurred. Please try again.")
    finally:
        safe_eel_call('ShowHood')

# ✅ NEW: Continuous listening function
def continuous_listening():
    """Continuously listen for commands without hotword"""
    global LISTENING
    
    speak("Friday is now active in continuous listening mode. I'm ready to help!")
    speak("You can say 'time to sleep Friday' to put me in sleep mode.")
    
    while True:
        try:
            if LISTENING:
                print("🟢 ACTIVE - Listening for commands...")
                # Automatically take commands without manual trigger
                takeAllCommands()
                # Small delay to prevent overwhelming the system
                time.sleep(0.5)
            else:
                print("🔴 SLEEP MODE - Say 'wake up Friday' to activate")
                # In sleep mode, only listen for wake up command
                query = takecommand()
                if query:
                    if "wake up" in query or "hello friday" in query or "hey friday" in query:
                        LISTENING = True
                        speak("I'm awake and ready!")
                    else:
                        print(f"Ignoring command in sleep mode: {query}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            speak("Shutting down Friday. Goodbye!")
            break
        except Exception as e:
            print(f"Error in continuous listening: {e}")
            time.sleep(1)
            continue

# ✅ Function to get listening status
@eel.expose
def get_listening_status():
    """Return current listening status"""
    global LISTENING
    return {"listening": LISTENING}

# ✅ Function to toggle listening from UI
@eel.expose
def toggle_listening():
    """Toggle listening mode from UI"""
    global LISTENING
    LISTENING = not LISTENING
    
    if LISTENING:
        speak("Listening mode activated")
        return {"status": "active", "listening": True}
    else:
        speak("Sleep mode activated")
        return {"status": "sleep", "listening": False}