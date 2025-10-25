import os
import re
import json
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
from pathlib import Path
import asyncio

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

from backend.command import speak
from backend.config import ASSISTANT_NAME, PORCUPINE_ACCESS_KEY
import sqlite3

from backend.helper import extract_yt_term, remove_words

# Initialize database connection
conn = None
cursor = None
try:
    conn = sqlite3.connect("jarvis.db", check_same_thread=False)
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to database: {str(e)}")

# Initialize pygame mixer
try:
    if pygame:
        pygame.mixer.init()
except Exception as e:
    print(f"Warning: pygame mixer initialization failed: {e}")

@eel.expose
def play_assistant_sound():
    """Play the assistant sound"""
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
    """Open applications or websites"""
    try:
        # Remove common wake words and command words
        query = query.lower()
        query = query.replace("alexa", "").replace("friday", "").replace("jarvis", "")
        query = query.replace(ASSISTANT_NAME.lower(), "")
        query = query.replace("open", "").replace("start", "").replace("launch", "")
        query = query.strip()
        
        if not query:
            speak("What would you like me to open?")
            return
        
        print(f"Processed query: '{query}'")
        
        # Common applications with their commands
        common_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "browser": "msedge.exe",
            "word": "winword.exe",
            "microsoft word": "winword.exe",
            "excel": "excel.exe",
            "microsoft excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "settings": "ms-settings:",
            "camera": "microsoft.windows.camera:",
            "calculator": "calc.exe",
            "calendar": "outlookcal:",
            "mail": "outlookmail:",
        }
        
        # Common websites
        common_websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "github": "https://www.github.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
        }
        
        # Check if it's a common app
        if query in common_apps:
            speak(f"Opening {query}")
            try:
                subprocess.Popen(common_apps[query], shell=True)
                return
            except Exception as e:
                print(f"Error opening {query}: {e}")
        
        # Check if it's a common website
        elif query in common_websites:
            speak(f"Opening {query}")
            webbrowser.open(common_websites[query])
            return
        
        # Try database (if available)
        elif cursor is not None:
            try:
                # Check system commands
                cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
                results = cursor.fetchall()
                
                if results:
                    speak(f"Opening {query}")
                    os.startfile(results[0][0])
                    return
                
                # Check web commands
                cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
                results = cursor.fetchall()
                
                if results:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])
                    return
                    
            except Exception as e:
                print(f"Database error: {e}")
        
        # Last resort: try as system command
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
    """Play video on YouTube"""
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
    """Listen for hotword (Alexa) and trigger action"""
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
            porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=["alexa"]
            )
            print("Porcupine initialized successfully")
        except Exception as e:
            print(f"Error initializing Porcupine: {str(e)}")
            return
        
        try:
            paud = pyaudio.PyAudio()
            audio_stream = paud.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )
            print("Audio stream opened successfully")
        except Exception as e:
            print(f"Error initializing audio: {str(e)}")
            if porcupine:
                porcupine.delete()
            return
        
        print("Listening for hotword 'Alexa'...")
        
        try:
            while True:
                try:
                    pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                    
                    keyword_index = porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        print("Hotword 'Alexa' detected!")
                        
                        # Trigger the hotkey to activate Friday
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
    """Find contact in database"""
    try:
        if cursor is None:
            speak('Database connection error')
            return 0, 0
        
        words_to_remove = [ASSISTANT_NAME, 'alexa', 'friday', 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
        query = remove_words(query, words_to_remove)
        query = query.strip().lower()
        
        if not query:
            speak('No contact name provided')
            return 0, 0
        
        try:
            cursor.execute(
                "SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                ('%' + query + '%', query + '%')
            )
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
    """Send WhatsApp message or make call"""
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
    """Async Bing Chat function"""
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
        
        # Load cookies from file
        cookies = None
        try:
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                
            if not cookies or len(cookies) == 0:
                print("Cookie file is empty")
                return "Cookie file is empty. Please add valid Bing cookies."
                
            # Check for critical _U cookie
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
            
            # Create chatbot with cookies (pass cookies list directly)
            bot = await Chatbot.create(cookies=cookies)
            
            print(f"Asking Bing: {user_input}")
            
            # Ask question with balanced conversation style
            response = await bot.ask(
                prompt=user_input,
                conversation_style=ConversationStyle.balanced
            )
            
            # Extract text from response
            response_text = None
            
            if response:
                print(f"Response type: {type(response)}")
                
                # Try different response formats
                if isinstance(response, dict):
                    # Method 1: Direct text field
                    if 'text' in response:
                        response_text = response['text']
                    
                    # Method 2: Messages array
                    elif 'messages' in response:
                        for msg in reversed(response['messages']):
                            if msg.get('author') == 'bot':
                                response_text = msg.get('text', '')
                                break
                    
                    # Method 3: Item.messages structure
                    elif 'item' in response:
                        messages = response.get('item', {}).get('messages', [])
                        for msg in reversed(messages):
                            if msg.get('author') == 'bot':
                                response_text = msg.get('text', '')
                                break
                    
                    # Method 4: Look for any text field recursively
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
                    # Clean up the response
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
            
            # Check for common errors
            if "401" in error_msg or "Unauthorized" in error_msg:
                return "Your Bing cookies have expired. Please update cookie.json with fresh cookies from bing.com"
            elif "throttled" in error_msg.lower() or "429" in error_msg:
                return "Bing Chat is rate limiting. Please wait a moment and try again."
            elif "timeout" in error_msg.lower():
                return "Connection to Bing timed out. Please check your internet connection."
            else:
                return f"Error communicating with Bing: {error_msg}"
            
        finally:
            # Always close the bot
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
    """Chat with Bing AI (synchronous wrapper)"""
    try:
        # Get or create event loop
        loop = None
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run async function
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