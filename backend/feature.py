import os
import re
import json
from shlex import quote
import struct
import subprocess
import time
import datetime
import webbrowser
import eel
from pathlib import Path
import asyncio
import socket

try:
    from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
    EDGEGPT_AVAILABLE = True
except ImportError as e:
    Chatbot = None
    ConversationStyle = None
    EDGEGPT_AVAILABLE = False
    print(f"Warning: EdgeGPT not installed - {str(e)}")

try:
    import pvporcupine
except ImportError as e:
    pvporcupine = None
    print(f"Warning: Missing dependency - {str(e)}")

try:
    import pyaudio
except ImportError as e:
    pyaudio = None
    print(f"Warning: Missing dependency - {str(e)}")

try:
    import pyautogui
except ImportError as e:
    pyautogui = None
    print(f"Warning: Missing dependency - {str(e)}")

try:
    import pywhatkit as kit
except ImportError as e:
    kit = None
    print(f"Warning: Missing dependency - {str(e)}")

try:
    import pygame
except ImportError as e:
    pygame = None
    print(f"Warning: Missing dependency - {str(e)}")

try:
    import wikipedia
except ImportError as e:
    wikipedia = None
    print(f"Warning: wikipedia not installed - {str(e)}")

try:
    import pyjokes
except ImportError as e:
    pyjokes = None
    print(f"Warning: pyjokes not installed - {str(e)}")

try:
    import psutil
except ImportError as e:
    psutil = None
    print(f"Warning: psutil not installed - {str(e)}")

try:
    import requests
except ImportError as e:
    requests = None
    print(f"Warning: requests not installed - {str(e)}")

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    BeautifulSoup = None
    print(f"Warning: BeautifulSoup not installed - {str(e)}")

try:
    import PyPDF2
except ImportError as e:
    PyPDF2 = None
    print(f"Warning: PyPDF2 not installed - {str(e)}")

try:
    import instaloader
except ImportError as e:
    instaloader = None
    print(f"Warning: instaloader not installed - {str(e)}")

from backend.talk import speak
from backend.config import ASSISTANT_NAME, EMAIL_ADDRESS, EMAIL_PASSWORD, NEWS_API_KEY, OPENWEATHER_API_KEY, PORCUPINE_ACCESS_KEY, WOLFRAMALPHA_APP_ID
import sqlite3
from backend.helper import extract_yt_term, remove_words

conn = None
cursor = None
try:
    conn = sqlite3.connect("jarvis.db", check_same_thread=False)
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to database: {str(e)}")

try:
    if pygame:
        pygame.mixer.init()
except Exception as e:
    print(f"Warning: pygame mixer initialization failed: {e}")

@eel.expose
def play_assistant_sound():
    try:
        if not pygame:
            print("pygame not available")
            return {"status": "error", "message": "pygame not available"}
        
        sound_file = Path("frontend/assets/audio/start_sound.mp3")
        if not sound_file.exists():
            print(f"Warning: Sound file not found at {sound_file}")
            return {"status": "error", "message": "Sound file not found"}
        
        pygame.mixer.music.load(str(sound_file))
        pygame.mixer.music.play()
        return {"status": "success"}
        
    except Exception as e:
        print(f"Error playing sound: {str(e)}")
        return {"status": "error", "message": str(e)}

def openCommand(query):
    try:
        query = query.lower()
        query = query.replace("jarvis", "").replace("friday", "")
        query = query.replace(ASSISTANT_NAME.lower(), "")
        query = query.replace("open", "").replace("start", "").replace("launch", "")
        query = query.strip()
        
        if not query:
            speak("What would you like me to open?")
            return
        
        print(f"Processed query: '{query}'")
        
        common_apps = {
            "notepad": "notepad.exe", "calculator": "calc.exe", "paint": "mspaint.exe",
            "chrome": "chrome.exe", "google chrome": "chrome.exe", "edge": "msedge.exe",
            "microsoft edge": "msedge.exe", "browser": "msedge.exe", "word": "winword.exe",
            "microsoft word": "winword.exe", "excel": "excel.exe", "microsoft excel": "excel.exe",
            "powerpoint": "powerpnt.exe", "task manager": "taskmgr.exe", "control panel": "control.exe",
            "cmd": "cmd.exe", "command prompt": "cmd.exe", "file explorer": "explorer.exe",
            "explorer": "explorer.exe", "settings": "ms-settings:", "camera": "microsoft.windows.camera:",
        }
        
        common_websites = {
            "youtube": "https://www.youtube.com", "google": "https://www.google.com",
            "gmail": "https://mail.google.com", "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com", "instagram": "https://www.instagram.com",
            "github": "https://www.github.com", "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com", "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com", "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
        }
        
        if query in common_apps:
            speak(f"Opening {query}")
            try:
                subprocess.Popen(common_apps[query], shell=True)
                return
            except Exception as e:
                print(f"Error opening {query}: {e}")
        
        elif query in common_websites:
            speak(f"Opening {query}")
            webbrowser.open(common_websites[query])
            return
        
        elif cursor is not None:
            try:
                cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
                results = cursor.fetchall()
                
                if results:
                    speak(f"Opening {query}")
                    os.startfile(results[0][0])
                    return
                
                cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
                results = cursor.fetchall()
                
                if results:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])
                    return
                    
            except Exception as e:
                print(f"Database error: {e}")
        
        speak(f"Trying to open {query}")
        try:
            os.system(f'start {query}')
        except Exception as e:
            speak(f"Sorry, I couldn't find {query}")
            print(f"Error: {e}")
            
    except Exception as e:
        print(f"Error in openCommand: {str(e)}")
        speak("Something went wrong")

def PlayYoutube(query):
    try:
        search_term = extract_yt_term(query) if query else query
        speak("Playing " + search_term + " on YouTube")
        
        if kit:
            kit.playonyt(search_term)
        else:
            print("pywhatkit not available")
            speak("YouTube playback not available")
            
    except Exception as e:
        print(f"Error in PlayYoutube: {e}")
        speak("Error playing YouTube video")

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    try:
        if not pvporcupine or not pyaudio:
            print("Hotword dependencies missing (pvporcupine or pyaudio)")
            return
        
        if not PORCUPINE_ACCESS_KEY:
            print("Porcupine access key missing in config")
            return
        
        print("Initializing hotword detection...")
        
        try:
            porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=["jarvis"])
            print("Porcupine initialized successfully")
        except Exception as e:
            print(f"Error initializing Porcupine: {str(e)}")
            return
        
        try:
            paud = pyaudio.PyAudio()
            audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
            print("Audio stream opened successfully")
        except Exception as e:
            print(f"Error initializing audio: {str(e)}")
            if porcupine:
                porcupine.delete()
            return
        
        print("Listening for hotword 'Friday'...")
        
        try:
            while True:
                try:
                    pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                    keyword_index = porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        print("Hotword 'Friday' detected!")
                        try:
                            if pyautogui:
                                pyautogui.keyDown("win")
                                pyautogui.press("j")
                                time.sleep(2)
                                pyautogui.keyUp("win")
                                print("Hotkey triggered (Win+J)")
                        except Exception as e:
                            print(f"Error triggering hotkey: {str(e)}")
                            
                except KeyboardInterrupt:
                    print("Hotword detection stopped by user")
                    break
                except Exception as e:
                    print(f"Error processing audio frame: {str(e)}")
                    time.sleep(0.1)
                    continue
                    
        finally:
            print("Cleaning up hotword detection resources...")
            if audio_stream is not None:
                audio_stream.stop_stream()
                audio_stream.close()
            if paud is not None:
                paud.terminate()
            if porcupine is not None:
                porcupine.delete()
            print("Hotword detection cleanup complete")
            
    except Exception as e:
        print(f"Error in hotword: {str(e)}")

def findContact(query):
    try:
        if cursor is None:
            speak('Database connection error')
            return 0, 0
        
        words_to_remove = [ASSISTANT_NAME, 'jarvis', 'friday', 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
        query = remove_words(query, words_to_remove)
        query = query.strip().lower()
        
        if not query:
            speak('No contact name provided')
            return 0, 0
        
        try:
            cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
            results = cursor.fetchall()
            
            if results:
                mobile_number_str = str(results[0][0])
                if not mobile_number_str.startswith('+91'):
                    mobile_number_str = '+91' + mobile_number_str
                return mobile_number_str, query
            else:
                speak('Contact not found')
                return 0, 0
                
        except Exception as e:
            print(f"Database query error: {str(e)}")
            speak('Error searching contacts')
            return 0, 0
            
    except Exception as e:
        print(f"Error in findContact: {str(e)}")
        speak('Something went wrong')
        return 0, 0

def whatsApp(Phone, message, flag, name):
    try:
        if flag == 'message':
            target_tab = 12
            jarvis_message = "message sent successfully to " + name
        elif flag == 'call':
            target_tab = 7
            message = ''
            jarvis_message = "calling " + name
        else:
            target_tab = 6
            message = ''
            jarvis_message = "starting video call with " + name
        
        try:
            encoded_message = quote(message)
            whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
            full_command = f'start "" "{whatsapp_url}"'
            
            subprocess.run(full_command, shell=True)
            time.sleep(5)
            subprocess.run(full_command, shell=True)
            
            if pyautogui:
                pyautogui.hotkey('ctrl', 'f')
                for _ in range(1, target_tab):
                    pyautogui.press('tab')
                pyautogui.press('enter')
            
            speak(jarvis_message)
            
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            speak("Error sending message")
            
    except Exception as e:
        print(f"Error in whatsApp: {str(e)}")

async def chatBot_async(query):
    try:
        if not EDGEGPT_AVAILABLE:
            print("EdgeGPT not available")
            return "I cannot connect to Bing Chat. Please install EdgeGPT using: pip install EdgeGPT"
        
        user_input = query.strip()
        if not user_input:
            return "I didn't receive any input."
        
        cookie_path = Path("backend/cookie.json")
        
        if not cookie_path.exists():
            print(f"Error: Cookie file not found at {cookie_path}")
            return "Bing Chat is not configured. Please add cookie.json file with valid Bing cookies."
        
        cookies = None
        try:
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                
            if not cookies or len(cookies) == 0:
                print("Cookie file is empty")
                return "Cookie file is empty. Please add valid Bing cookies."
                
            has_u_cookie = any(c.get('name') == '_U' for c in cookies if isinstance(c, dict))
            if not has_u_cookie:
                print("Missing critical _U cookie")
                return "Cookie file is missing the required _U cookie. Please update your cookies."
                
        except json.JSONDecodeError as e:
            print(f"Error parsing cookies JSON: {e}")
            return "Cookie file is not valid JSON format."
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return "Could not load cookie file."
        
        bot = None
        try:
            print(f"Creating Bing chatbot with {len(cookies)} cookies...")
            bot = await Chatbot.create(cookies=cookies)
            print(f"Asking Bing: {user_input}")
            
            response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.balanced)
            
            response_text = None
            
            if response:
                print(f"Response type: {type(response)}")
                
                if isinstance(response, dict):
                    if 'text' in response:
                        response_text = response['text']
                    elif 'messages' in response:
                        for msg in reversed(response['messages']):
                            if msg.get('author') == 'bot':
                                response_text = msg.get('text', '')
                                break
                    elif 'item' in response:
                        messages = response.get('item', {}).get('messages', [])
                        for msg in reversed(messages):
                            if msg.get('author') == 'bot':
                                response_text = msg.get('text', '')
                                break
                    
                    if not response_text:
                        def find_text(obj):
                            if isinstance(obj, dict):
                                if 'text' in obj and obj['text']:
                                    return obj['text']
                                for value in obj.values():
                                    result = find_text(value)
                                    if result:
                                        return result
                            elif isinstance(obj, list):
                                for item in obj:
                                    result = find_text(item)
                                    if result:
                                        return result
                            return None
                        
                        response_text = find_text(response)
                
                elif isinstance(response, str):
                    response_text = response
                
                if response_text:
                    response_text = response_text.strip()
                    print(f"Bing response: {response_text[:100]}...")
                    return response_text
                else:
                    print(f"Could not extract text from response: {response}")
                    return "I got a response from Bing but couldn't understand the format."
            else:
                print("No response from Bing")
                return "I didn't get a response from Bing."
                
        except Exception as e:
            error_msg = str(e)
            print(f"Bing Chat error: {error_msg}")
            
            if "401" in error_msg or "Unauthorized" in error_msg:
                return "Your Bing cookies have expired. Please update cookie.json with fresh cookies from bing.com"
            elif "throttled" in error_msg.lower() or "429" in error_msg:
                return "Bing Chat is rate limiting. Please wait a moment and try again."
            elif "timeout" in error_msg.lower():
                return "Connection to Bing timed out. Please check your internet connection."
            else:
                return f"Error communicating with Bing: {error_msg}"
            
        finally:
            if bot:
                try:
                    await bot.close()
                    print("Bing chatbot closed")
                except Exception as e:
                    print(f"Error closing bot: {e}")
                    
    except Exception as e:
        print(f"Error in chatBot_async: {str(e)}")
        import traceback
        traceback.print_exc()
        return "Something went wrong with the chatbot."

def chatBot(query):
    try:
        loop = None
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        print(f"Running chatbot for query: {query}")
        response = loop.run_until_complete(chatBot_async(query))
        
        if response:
            speak(response)
            return response
        else:
            speak("I didn't get a response from Bing")
            return None
            
    except Exception as e:
        print(f"Error in chatBot wrapper: {str(e)}")
        import traceback
        traceback.print_exc()
        speak("Something went wrong with the chatbot")
        return None

def greet_user():
    try:
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        speak(f"{greeting}! I'm Friday, your personal AI assistant. How may I help you today?")
        return greeting
    except Exception as e:
        print(f"Error in greet_user: {e}")
        return None

def tell_time():
    try:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        return current_time
    except Exception as e:
        print(f"Error in tell_time: {e}")
        return None

def tell_date():
    try:
        today = datetime.datetime.now()
        date_str = today.strftime("%A, %B %d, %Y")
        speak(f"Today is {date_str}")
        return date_str
    except Exception as e:
        print(f"Error in tell_date: {e}")
        return None

def get_weather(city=None):
    try:
        if not requests:
            speak("Requests library not available")
            return None
        
        if not OPENWEATHER_API_KEY:
            speak("Weather API key not configured. Please add it to your dot env file")
            return None
            
        if city is None:
            city = "London"
        
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={OPENWEATHER_API_KEY}&q={city}"
        
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = round(main["temp"] - 273.15, 2)
            humidity = main["humidity"]
            
            weather_report = f"Temperature in {city} is {temperature} degrees celsius with {weather_desc}. Humidity is {humidity} percent."
            speak(weather_report)
            return weather_report
        else:
            speak("City not found")
            return None
            
    except Exception as e:
        print(f"Error in get_weather: {e}")
        speak("Unable to fetch weather information")
        return None

def get_system_status():
    try:
        if not psutil:
            speak("Psutil library not available")
            return None
            
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        ram_usage = memory.percent
        ram_available = round(memory.available / (1024**3), 2)
        
        battery = psutil.sensors_battery()
        if battery:
            battery_percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            battery_status = f"Battery is at {battery_percent} percent and {plugged}"
        else:
            battery_status = "No battery found"
        
        status = f"CPU usage is {cpu_usage} percent. RAM usage is {ram_usage} percent with {ram_available} gigabytes available. {battery_status}."
        speak(status)
        
        return {"cpu": cpu_usage, "ram": ram_usage, "battery": battery_percent if battery else None}
        
    except Exception as e:
        print(f"Error in get_system_status: {e}")
        speak("Unable to fetch system status")
        return None

def search_wikipedia(query):
    try:
        if not wikipedia:
            speak("Wikipedia library not available")
            return None
            
        speak(f"Searching Wikipedia for {query}")
        result = wikipedia.summary(query, sentences=3)
        speak(result)
        return result
    except Exception as e:
        print(f"Error in search_wikipedia: {e}")
        speak("Unable to search Wikipedia")
        return None

def google_search(query):
    try:
        speak(f"Searching Google for {query}")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return url
    except Exception as e:
        print(f"Error in google_search: {e}")
        return None

def get_news():
    if not requests:
        speak("Requests library not available. Please install it to use the news feature.")
        return None
    
    if not NEWS_API_KEY:
        speak("News API key is not configured. Please add it to your dot env file to get news updates.")
        return None

    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    
    try:
        print("Fetching news from API...")
        response = requests.get(url)
        news_data = response.json()

        if news_data.get("status") == "ok":
            
            articles = news_data.get("articles", [])
            
            if not articles:
                speak("Sorry, I couldn't find any news articles at the moment.")
                return None

            speak("Here are the top 5 headlines from India.")
            
            for i, article in enumerate(articles[:5]):
                title = article.get('title', 'No title available')
                
                print(f"Headline {i+1}: {title}")
                
                speak(f"Headline number {i+1}. {title}")
            
            return [article.get('title') for article in articles[:5]]
            
        else:
            error_message = news_data.get("message", "Unknown API error.")
            print(f"News API Error: {error_message}")
            speak("Sorry, I couldn't fetch the news. The API reported an error.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching news: {e}")
        speak("I am unable to connect to the news service. Please check your internet connection.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in get_news: {e}")
        speak("An unexpected error occurred while trying to get the news.")
        return None

def play_music():
    try:
        music_dir = Path.home() / "Music"
        
        if music_dir.exists():
            songs = list(music_dir.glob("*.mp3"))
            
            if songs:
                song = str(songs[0])
                os.startfile(song)
                speak("Playing music")
                return song
            else:
                speak("No music files found")
                return None
        else:
            speak("Music folder not found")
            return None
            
    except Exception as e:
        print(f"Error in play_music: {e}")
        speak("Unable to play music")
        return None

def calculate(expression):
    try:
        expression = expression.replace("calculate", "").replace("what is", "").strip()
        expression = expression.replace("plus", "+").replace("minus", "-")
        expression = expression.replace("multiply", "*").replace("divide", "/")
        expression = expression.replace("x", "*")
        
        result = eval(expression)
        speak(f"The answer is {result}")
        return result
        
    except Exception as e:
        print(f"Error in calculate: {e}")
        speak("Unable to calculate")
        return None

def take_note(note):
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Note_{date}.txt"
        filepath = Path.home() / "Documents" / filename
        
        with open(filepath, 'w') as f:
            f.write(note)
        
        speak(f"Note saved as {filename}")
        os.startfile(str(filepath))
        return str(filepath)
        
    except Exception as e:
        print(f"Error in take_note: {e}")
        speak("Unable to save note")
        return None

def tell_joke():
    try:
        if not pyjokes:
            speak("Pyjokes library not available")
            return None
            
        joke = pyjokes.get_joke()
        speak(joke)
        return joke
    except Exception as e:
        print(f"Error in tell_joke: {e}")
        speak("Unable to tell a joke")
        return None

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        speak(f"Your IP address is {ip_address}")
        return ip_address
    except Exception as e:
        print(f"Error in get_ip_address: {e}")
        speak("Unable to fetch IP address")
        return None

def switch_window():
    try:
        if not pyautogui:
            speak("Pyautogui not available")
            return False
            
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")
        speak("Switching window")
        return True
    except Exception as e:
        print(f"Error in switch_window: {e}")
        return False

def take_screenshot(filename=None):
    try:
        if not pyautogui:
            speak("Pyautogui not available")
            return None
            
        if filename is None:
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = Path.home() / "Pictures" / filename
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        speak(f"Screenshot saved as {filename}")
        return str(filepath)
    except Exception as e:
        print(f"Error in take_screenshot: {e}")
        speak("Unable to take screenshot")
        return None

def read_file(filepath):
    try:
        path = Path(filepath)
        
        if not path.exists():
            speak("File not found")
            return None
        
        if path.suffix in ['.txt', '.log', '.md']:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                speak(f"Reading {path.name}")
                speak(content[:500])
                return content
        
        elif path.suffix == '.pdf' and PyPDF2:
            with open(path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                
                speak(f"Reading PDF with {num_pages} pages")
                page = pdf_reader.pages[0]
                text = page.extract_text()
                speak(text[:500])
                return text
        else:
            speak("Unsupported file format")
            return None
            
    except Exception as e:
        print(f"Error in read_file: {e}")
        speak("Unable to read file")
        return None

def close_application(app_name):
    try:
        os.system(f"taskkill /f /im {app_name}.exe")
        speak(f"Closed {app_name}")
        return True
    except Exception as e:
        print(f"Error closing app: {e}")
        speak(f"Could not close {app_name}")
        return False

def hide_file(filepath):
    try:
        import ctypes
        path = Path(filepath)
        
        if path.exists():
            ctypes.windll.kernel32.SetFileAttributesW(str(path), 2)
            speak(f"Hidden {path.name}")
            return True
        else:
            speak("File not found")
            return False
    except Exception as e:
        print(f"Error hiding file: {e}")
        speak("Unable to hide file")
        return False

def unhide_file(filepath):
    try:
        import ctypes
        path = Path(filepath)
        
        if path.exists():
            ctypes.windll.kernel32.SetFileAttributesW(str(path), 128)
            speak(f"Unhidden {path.name}")
            return True
        else:
            speak("File not found")
            return False
    except Exception as e:
        print(f"Error unhiding file: {e}")
        speak("Unable to unhide file")
        return False

def delete_file(filepath):
    try:
        path = Path(filepath)
        
        if path.exists():
            if path.is_file():
                path.unlink()
                speak(f"Deleted {path.name}")
                return True
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                speak(f"Deleted folder {path.name}")
                return True
        else:
            speak("File not found")
            return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        speak("Unable to delete file")
        return False

def get_instagram_info(username):
    try:
        if not instaloader:
            speak("Instaloader library not available")
            return None
            
        L = instaloader.Instaloader()
        speak(f"Fetching Instagram profile for {username}")
        
        profile = instaloader.Profile.from_username(L.context, username)
        
        info = f"{username} has {profile.followers} followers and {profile.followees} following. Total posts: {profile.mediacount}."
        speak(info)
        
        return {
            "username": username,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount
        }
        
    except Exception as e:
        print(f"Error in get_instagram_info: {e}")
        speak("Unable to fetch Instagram profile")
        return None
    
def ask_wolframalpha(query):
    try:
        try:
            import wolframalpha
        except ImportError:
            speak("Wolfram Alpha library not installed. Please run: pip install wolframalpha")
            return None
        
        if not WOLFRAMALPHA_APP_ID:
            speak("Wolfram Alpha API not configured. Please add your App ID to the dot env file")
            return None
            
        client = wolframalpha.Client(WOLFRAMALPHA_APP_ID)
        
        speak(f"Asking Wolfram Alpha: {query}")
        res = client.query(query)
        
        try:
            answer = next(res.results).text
            speak(answer)
            return answer
        except StopIteration:
            speak("No results found from Wolfram Alpha")
            return None
            
    except Exception as e:
        print(f"Error in ask_wolframalpha: {e}")
        speak("Unable to get answer from Wolfram Alpha")
        return None
    
def send_email(to, subject, content):
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            speak("Email credentials not configured in dot env file")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(content, 'plain'))
        
        speak("Sending email...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to, text)
        server.quit()
        
        speak("Email sent successfully")
        return True
        
    except Exception as e:
        print(f"Error in send_email: {e}")
        speak("Unable to send email. Please check your email configuration")
        return False