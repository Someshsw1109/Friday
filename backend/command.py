import time
import speech_recognition as sr
import eel
import threading
from backend.talk import speak, safe_eel_call 

LISTENING = False 
CONTINUOUS_MODE = False
PROCESSING = False

def takecommand():    
    global PROCESSING
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 I'm listening...")
            safe_eel_call('DisplayMessage', "I'm listening...")
            safe_eel_call('updateStatus', 'listening')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
    except Exception as e:
        print(f"❌ Microphone error: {str(e)}")
        return None
    
    try:    
        print("🔍 Recognizing...")
        safe_eel_call('DisplayMessage', "Recognizing...")
        safe_eel_call('updateStatus', 'processing')
        query = r.recognize_google(audio, language='en-US')
        print(f"✅ User said: {query}\n")
        safe_eel_call('DisplayMessage', query)
        return query.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        safe_eel_call('DisplayMessage', "Sorry, I didn't catch that")
        return None
    except sr.RequestError as e:
        print(f"❌ Google API error: {str(e)}")
        safe_eel_call('DisplayMessage', "API error")
        return None
    except Exception as e:
        print(f"❌ Error in takecommand: {str(e)}")
        return None

@eel.expose
def takeAllCommands(message=None):
    global LISTENING, PROCESSING
    
    try:
        query = None
        PROCESSING = True
        safe_eel_call('updateStatus', 'processing')
        
        if message is None:
            query = takecommand()
            if not query:
                PROCESSING = False
                safe_eel_call('updateStatus', 'listening' if CONTINUOUS_MODE else 'inactive')
                return
            safe_eel_call('senderText', query)
        else:
            query = message
            safe_eel_call('senderText', query)
        
        if query:
            # ✅ SLEEP MODE COMMANDS
            if "time to sleep" in query or "go to sleep" in query or "sleep friday" in query or "stop listening" in query or "sleep mode" in query:
                speak("Okay, going to sleep mode. Say 'wake up Friday' or click my icon to activate me again.")
                stop_assistant()
                PROCESSING = False
                return
            
            # ✅ WAKE UP COMMANDS (if in sleep mode)
            if not LISTENING:
                if "wake up" in query or "hello friday" in query or "hey friday" in query or "activate" in query:
                    LISTENING = True
                    speak("I'm awake and ready to help!")
                    safe_eel_call('updateStatus', 'listening')
                    PROCESSING = False
                    return
                else:
                    print("🔴 SLEEP MODE - Ignoring command")
                    PROCESSING = False
                    return
            
            # ✅ EXECUTE COMMANDS
            try:
                from backend.feature import (
                    openCommand, PlayYoutube, findContact, whatsApp, chatBot,
                    greet_user, tell_time, tell_date, get_weather, get_system_status,
                    search_wikipedia, google_search, get_news, play_music, calculate,
                    take_note, tell_joke, get_ip_address, switch_window, take_screenshot,
                    read_file, close_application, hide_file, unhide_file, delete_file,
                    get_instagram_info, ask_wolframalpha, send_email
                )
                
                if "hello" in query or "hi friday" in query or "hey friday" in query or "hello friday" in query:
                    greet_user()
                elif "time" in query:
                    tell_time()
                elif "date" in query and ("what" in query or "today" in query or "tell" in query):
                    tell_date()
                elif "weather" in query:
                    city = query.replace("weather", "").replace("in", "").replace("what", "").replace("is", "").replace("the", "").strip()
                    get_weather(city if city else None)
                elif "system status" in query or "battery" in query or ("cpu" in query and "usage" in query) or ("ram" in query and "usage" in query):
                    get_system_status()
                elif "wikipedia" in query:
                    search_query = query.replace("wikipedia", "").replace("search", "").strip()
                    search_wikipedia(search_query)
                elif "who is" in query:
                    search_query = query.replace("who is", "").strip()
                    search_wikipedia(search_query)
                elif "what is" in query and not any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide']):
                    search_query = query.replace("what is", "").strip()
                    search_wikipedia(search_query)
                elif "google search" in query or "search for" in query or "search on google" in query:
                    search_query = query.replace("google search", "").replace("search for", "").replace("search on google", "").replace("google", "").strip()
                    google_search(search_query)
                elif "news" in query or "headlines" in query:
                    get_news()
                elif "play music" in query:
                    play_music()
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
                elif "calculate" in query or ("what is" in query and any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide'])):
                    calculate(query)
                elif "ask wolfram" in query or "wolfram" in query:
                    question = query.replace("ask wolfram", "").replace("wolfram", "").strip()
                    ask_wolframalpha(question)
                elif any(word in query for word in ["population", "capital", "distance", "convert", "how far", "how many"]):
                    ask_wolframalpha(query)
                elif "take note" in query or "make note" in query or "remember this" in query:
                    speak("What should I note down?")
                    note = takecommand()
                    if note:
                        take_note(note)
                elif "joke" in query or "make me laugh" in query:
                    tell_joke()
                elif "ip address" in query or "my ip" in query:
                    get_ip_address()
                elif "switch window" in query or "change window" in query:
                    switch_window()
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
                elif "read file" in query or ("read" in query and "file" in query):
                    speak("Which file should I read? Please provide the full path.")
                    filepath = takecommand()
                    if filepath:
                        read_file(filepath)
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
                elif "instagram" in query and ("profile" in query or "information" in query or "info" in query):
                    speak("Which Instagram username?")
                    username = takecommand()
                    if username:
                        get_instagram_info(username)
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
                elif "how are you" in query:
                    speak("I'm doing great! Thank you for asking. How can I help you today?")
                elif "thank you" in query or "thanks" in query:
                    speak("You're welcome! I'm always here to help.")
                elif "good job" in query or "well done" in query:
                    speak("Thank you! I'm glad I could help. Is there anything else you need?")
                else:
                    chatBot(query)
            except Exception as e:
                print(f"❌ Error in command: {str(e)}")
                speak("Something went wrong")
                    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        PROCESSING = False
        if CONTINUOUS_MODE and LISTENING:
            safe_eel_call('updateStatus', 'listening')
        else:
            safe_eel_call('updateStatus', 'inactive')

# ✅ CONTINUOUS LISTENING LOOP
def assistant_loop():
    global CONTINUOUS_MODE, LISTENING, PROCESSING
    
    print("🔄 Assistant loop started!")
    
    while True:
        try:
            if CONTINUOUS_MODE and LISTENING and not PROCESSING:
                print("🎤 Continuous mode: Waiting for command...")
                takeAllCommands()
                time.sleep(0.5)
            else:
                time.sleep(0.3)
        except Exception as e:
            print(f"❌ Error in assistant_loop: {e}")
            time.sleep(1)

@eel.expose
def start_assistant():
    """Start continuous listening mode"""
    global LISTENING, CONTINUOUS_MODE
    
    print("🚀 start_assistant() called!")
    LISTENING = True
    CONTINUOUS_MODE = True
    
    # Start the loop in a separate thread
    thread = threading.Thread(target=assistant_loop, daemon=True)
    thread.start()
    print("✅ Listening thread started!")
    
    speak("Continuous mode activated. I'm listening.")
    safe_eel_call('enableContinuousMode')
    safe_eel_call('updateStatus', 'listening')
    
@eel.expose
def stop_assistant():
    """Stop continuous listening mode"""
    global LISTENING, CONTINUOUS_MODE
    
    print("🛑 stop_assistant() called!")
    CONTINUOUS_MODE = False
    LISTENING = False
    
    speak("Continuous mode deactivated.")
    safe_eel_call('disableContinuousMode')
    safe_eel_call('updateStatus', 'inactive')

@eel.expose
def wakeup_by_ui():
    """Wake up assistant by UI click"""
    start_assistant()