import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

from backend.talk import speak
from backend.credentials import credential_manager

class WebAutomation:
    def __init__(self, browser="edge"):
        self.browser = browser
        self.driver = None
    
    def _init_driver(self):
        try:
            print(f"🌐 Initializing {self.browser} browser...")
            
            if self.browser == "edge":
                try:
                    options = EdgeOptions()
                    options.add_argument('--start-maximized')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
                    options.add_experimental_option('useAutomationExtension', False)
                    
                    if WEBDRIVER_MANAGER_AVAILABLE:
                        service = EdgeService(EdgeChromiumDriverManager().install())
                        self.driver = webdriver.Edge(service=service, options=options)
                    else:
                        self.driver = webdriver.Edge(options=options)
                    
                    print("✅ Edge browser initialized successfully")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Edge failed: {e}")
                    print("🔄 Trying Chrome instead...")
                    self.browser = "chrome"
            
            if self.browser == "chrome":
                try:
                    options = ChromeOptions()
                    options.add_argument('--start-maximized')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
                    options.add_experimental_option('useAutomationExtension', False)
                    
                    if WEBDRIVER_MANAGER_AVAILABLE:
                        service = ChromeService(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=service, options=options)
                    else:
                        self.driver = webdriver.Chrome(options=options)
                    
                    print("✅ Chrome browser initialized successfully")
                    return True
                    
                except Exception as e:
                    print(f"❌ Chrome also failed: {e}")
                    speak("Could not open browser. Please make sure Chrome or Edge is installed.")
                    return False
            
            return False
            
        except Exception as e:
            print(f"❌ Browser initialization error: {e}")
            speak("Could not open browser")
            return False
    
    def close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                print("✅ Browser closed")
            except Exception as e:
                print(f"Error closing browser: {e}")
    
    def login_website(self, website_name):
        try:
            website_name = website_name.lower()
            
            creds = credential_manager.get_credential(website_name)
            if not creds:
                speak(f"No saved credentials for {website_name}. Please save them first.")
                return False
            
            if not self._init_driver():
                return False
            
            speak(f"Logging into {website_name}")
            
            if "facebook" in website_name:
                return self._login_facebook(creds)
            elif "instagram" in website_name:
                return self._login_instagram(creds)
            elif "twitter" in website_name or "x.com" in website_name:
                return self._login_twitter(creds)
            elif "linkedin" in website_name:
                return self._login_linkedin(creds)
            elif "github" in website_name:
                return self._login_github(creds)
            elif "codeforces" in website_name:
                return self._login_codeforces(creds)
            elif "codechef" in website_name:
                return self._login_codechef(creds)
            elif "leetcode" in website_name:
                return self._login_leetcode(creds)
            elif "indigo" in website_name:
                return self._login_indigo(creds)
            else:
                speak("This website is not supported yet")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            speak("Login failed")
            return False
    
    def _login_facebook(self, creds):
        try:
            self.driver.get("https://www.facebook.com")
            time.sleep(2)
            
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "pass")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into Facebook successfully")
            return True
        except Exception as e:
            print(f"Facebook login error: {e}")
            speak("Facebook login failed")
            return False
    
    def _login_instagram(self, creds):
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.NAME, "password")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into Instagram successfully")
            return True
        except Exception as e:
            print(f"Instagram login error: {e}")
            speak("Instagram login failed")
            return False
    
    def _login_twitter(self, creds):
        try:
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(3)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            username_field.send_keys(creds['username'])
            username_field.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            pass_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into Twitter successfully")
            return True
        except Exception as e:
            print(f"Twitter login error: {e}")
            speak("Twitter login failed")
            return False
    
    def _login_linkedin(self, creds):
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "password")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into LinkedIn successfully")
            return True
        except Exception as e:
            print(f"LinkedIn login error: {e}")
            speak("LinkedIn login failed")
            return False
    
    def _login_github(self, creds):
        try:
            self.driver.get("https://github.com/login")
            time.sleep(2)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login_field"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "password")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into GitHub successfully")
            return True
        except Exception as e:
            print(f"GitHub login error: {e}")
            speak("GitHub login failed")
            return False
    
    def _login_codeforces(self, creds):
        try:
            self.driver.get("https://codeforces.com/enter")
            time.sleep(2)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "handleOrEmail"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "password")
            pass_field.send_keys(creds['password'])
            
            remember_checkbox = self.driver.find_element(By.ID, "remember")
            remember_checkbox.click()
            
            login_button = self.driver.find_element(By.CLASS_NAME, "submit")
            login_button.click()
            
            time.sleep(3)
            speak("Logged into Codeforces successfully")
            return True
        except Exception as e:
            print(f"Codeforces login error: {e}")
            speak("Codeforces login failed")
            return False
    
    def _login_codechef(self, creds):
        try:
            self.driver.get("https://www.codechef.com/login")
            time.sleep(2)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "edit-name"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "edit-pass")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into CodeChef successfully")
            return True
        except Exception as e:
            print(f"CodeChef login error: {e}")
            speak("CodeChef login failed")
            return False
    
    def _login_leetcode(self, creds):
        try:
            self.driver.get("https://leetcode.com/accounts/login/")
            time.sleep(2)
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id_login"))
            )
            username_field.send_keys(creds['username'])
            
            pass_field = self.driver.find_element(By.ID, "id_password")
            pass_field.send_keys(creds['password'])
            pass_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            speak("Logged into LeetCode successfully")
            return True
        except Exception as e:
            print(f"LeetCode login error: {e}")
            speak("LeetCode login failed")
            return False
    
    def _login_indigo(self, creds):
        try:
            speak("Logging into Indigo")
            
            try:
                login_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Log in')]"))
                )
                login_btn.click()
                time.sleep(2)
                
                mobile_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @placeholder='Mobile Number' or contains(@placeholder,'mobile')]"))
                )
                mobile_input.clear()
                mobile_input.send_keys(creds['username'])
                
                continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
                continue_btn.click()
                time.sleep(2)
                
                speak("Please enter the OTP manually within 30 seconds")
                print("⏳ Waiting for OTP entry...")
                time.sleep(30)
                
                speak("Login attempted")
                return True
                
            except Exception as e:
                print(f"Login error: {e}")
                speak("Could not login, continuing without login")
                return False
                
        except Exception as e:
            print(f"Indigo login error: {e}")
            return False

class FlightBooking:
    def __init__(self):
        self.automation = WebAutomation()
    
    def login_indigo(self):
        try:
            creds = credential_manager.get_credential('indigo')
            
            if not creds:
                speak("No saved credentials for Indigo. You can continue without login or save credentials first.")
                return False
            
            speak("Logging into Indigo")
            time.sleep(3)
            
            try:
                login_btn = WebDriverWait(self.automation.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Log in')]"))
                )
                login_btn.click()
                time.sleep(3)
                
                print("🔍 Looking for mobile number field...")
                mobile_input = WebDriverWait(self.automation.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @placeholder='Mobile Number' or contains(@placeholder,'mobile')]"))
                )
                mobile_input.clear()
                mobile_input.send_keys(creds['username'])
                time.sleep(1)
                
                continue_btn = self.automation.driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Proceed')]")
                continue_btn.click()
                time.sleep(3)
                
                speak("Please enter the OTP manually within 45 seconds")
                print("⏳ Waiting for OTP entry...")
                
                for i in range(45):
                    try:
                        if "home" in self.automation.driver.current_url.lower() or "booking" in self.automation.driver.current_url.lower():
                            speak("Login successful")
                            return True
                    except:
                        pass
                    time.sleep(1)
                
                speak("Login completed")
                return True
                
            except Exception as e:
                print(f"Login error: {e}")
                speak("Could not login. Continuing without login.")
                return False
                
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def fill_from_city(self, city):
        try:
            print(f"🔍 Filling 'From' city: {city}")
            speak(f"Selecting {city} as departure city")
            
            from_input = WebDriverWait(self.automation.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'From') or contains(@id,'from') or contains(@name,'from')]"))
            )
            
            from_input.click()
            time.sleep(2)
            
            from_input.clear()
            time.sleep(1)
            
            for char in city:
                from_input.send_keys(char)
                time.sleep(0.2)
            
            time.sleep(3)
            
            print("📍 Looking for city options...")
            try:
                city_options = WebDriverWait(self.automation.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']//li | //div[@class='autoSuggest-list']//div | //div[contains(@class,'autocomplete')]//li"))
                )
                
                if city_options:
                    print(f"✅ Found {len(city_options)} city options")
                    city_options[0].click()
                    time.sleep(2)
                    speak(f"{city} selected as departure city")
                    return True
                else:
                    from_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    return True
                    
            except Exception as e:
                print(f"Dropdown selection failed: {e}")
                from_input.send_keys(Keys.ENTER)
                time.sleep(2)
                return True
                
        except Exception as e:
            print(f"❌ From city error: {e}")
            import traceback
            traceback.print_exc()
            speak("Could not fill departure city. Please select it manually.")
            time.sleep(5)
            return False
    
    def fill_to_city(self, city):
        try:
            print(f"🔍 Filling 'To' city: {city}")
            speak(f"Selecting {city} as destination city")
            
            to_input = WebDriverWait(self.automation.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'To') or contains(@id,'to') or contains(@name,'to')]"))
            )
            
            to_input.click()
            time.sleep(2)
            
            to_input.clear()
            time.sleep(1)
            
            for char in city:
                to_input.send_keys(char)
                time.sleep(0.2)
            
            time.sleep(3)
            
            print("📍 Looking for city options...")
            try:
                city_options = WebDriverWait(self.automation.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']//li | //div[@class='autoSuggest-list']//div | //div[contains(@class,'autocomplete')]//li"))
                )
                
                if city_options:
                    print(f"✅ Found {len(city_options)} city options")
                    city_options[0].click()
                    time.sleep(2)
                    speak(f"{city} selected as destination")
                    return True
                else:
                    to_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    return True
                    
            except Exception as e:
                print(f"Dropdown selection failed: {e}")
                to_input.send_keys(Keys.ENTER)
                time.sleep(2)
                return True
                
        except Exception as e:
            print(f"❌ To city error: {e}")
            import traceback
            traceback.print_exc()
            speak("Could not fill destination city. Please select it manually.")
            time.sleep(5)
            return False
    
    def select_date(self, date_str=None):
        try:
            print("📅 Opening date picker...")
            speak("Selecting travel date")
            
            date_input = WebDriverWait(self.automation.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'Departure') or contains(@placeholder,'departure') or contains(@id,'departure')]"))
            )
            date_input.click()
            time.sleep(2)
            
            if date_str:
                try:
                    import re
                    day = re.findall(r'\d+', date_str)
                    if day:
                        day = day[0]
                        
                        date_element = WebDriverWait(self.automation.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//div[@class='DayPicker-Day' and text()='{day}'] | //td[text()='{day}' and not(contains(@class,'disabled'))]"))
                        )
                        date_element.click()
                        time.sleep(2)
                        speak(f"Selected date {day}")
                        return True
                except Exception as e:
                    print(f"Date selection error: {e}")
            
            speak("Please select the travel date manually within 10 seconds")
            print("⏳ Waiting for manual date selection...")
            time.sleep(10)
            return True
            
        except Exception as e:
            print(f"❌ Date picker error: {e}")
            speak("Please select the date manually")
            time.sleep(10)
            return True
    
    def set_passengers(self, count):
        try:
            if count <= 1:
                return True
            
            print(f"👥 Setting {count} passengers...")
            speak(f"Setting {count} passengers")
            
            passenger_btn = WebDriverWait(self.automation.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'passenger') or contains(text(),'Passenger')]"))
            )
            passenger_btn.click()
            time.sleep(2)
            
            for i in range(count - 1):
                try:
                    plus_btn = self.automation.driver.find_element(By.XPATH, "(//button[contains(@class,'plus') or contains(text(),'+')])[1]")
                    plus_btn.click()
                    time.sleep(1)
                except Exception as e:
                    print(f"Plus button error: {e}")
                    break
            
            try:
                done_btn = self.automation.driver.find_element(By.XPATH, "//button[contains(text(),'Done') or contains(text(),'done')]")
                done_btn.click()
                time.sleep(2)
            except:
                pass
            
            speak(f"{count} passengers set")
            return True
            
        except Exception as e:
            print(f"Passenger error: {e}")
            speak("Please set passenger count manually")
            time.sleep(5)
            return True
    
    def search_flights(self):
        try:
            print("🔍 Clicking search button...")
            speak("Searching for flights")
            
            search_btn = WebDriverWait(self.automation.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search') or contains(@class,'search-btn') or contains(@class,'search')]"))
            )
            search_btn.click()
            
            speak("Please wait while I search for flights")
            time.sleep(15)
            
            return True
            
        except Exception as e:
            print(f"❌ Search button error: {e}")
            speak("Could not click search. Please click search button manually.")
            time.sleep(10)
            return False
    
    def get_available_flights(self):
        try:
            speak("Looking for available flights")
            time.sleep(10)
            
            print("🔍 Searching for flight cards...")
            
            possible_selectors = [
                "//div[contains(@class,'flight-card')]",
                "//div[contains(@class,'FlightCard')]",
                "//div[contains(@class,'flight-list-item')]",
                "//div[contains(@class,'flight-item')]",
                "//div[contains(@class,'fare-card')]",
            ]
            
            flight_elements = []
            for selector in possible_selectors:
                try:
                    elements = self.automation.driver.find_elements(By.XPATH, selector)
                    if len(elements) > 0:
                        flight_elements = elements
                        print(f"✅ Found {len(elements)} flights using: {selector}")
                        break
                except:
                    continue
            
            if not flight_elements:
                speak("I can see the flights page. Please select a flight manually and I'll continue from there.")
                print("⏳ Waiting for manual flight selection...")
                time.sleep(30)
                return []
            
            flights = []
            for idx, flight in enumerate(flight_elements[:5], 1):
                try:
                    text = flight.text
                    if text:
                        print(f"\n✈️ Flight {idx}:\n{text[:200]}\n")
                        flights.append({
                            'index': idx,
                            'element': flight,
                            'text': text
                        })
                except:
                    continue
            
            if flights:
                speak(f"Found {len(flights)} flights. Please check the screen.")
                for f in flights:
                    speak(f"Option {f['index']}")
                    time.sleep(1)
                
                return flights
            else:
                speak("Please select a flight manually")
                time.sleep(30)
                return []
                
        except Exception as e:
            print(f"❌ Flight fetch error: {e}")
            speak("Please select a flight manually")
            time.sleep(30)
            return []
    
    def select_flight_by_number(self, number):
        try:
            speak(f"Selecting flight number {number}")
            time.sleep(2)
            
            book_buttons = [
                f"(//button[contains(text(),'Book') or contains(text(),'Select')])[{number}]",
                f"(//button[contains(@class,'book')])[{number}]",
                f"(//a[contains(text(),'Book')])[{number}]",
            ]
            
            for btn_xpath in book_buttons:
                try:
                    btn = WebDriverWait(self.automation.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, btn_xpath))
                    )
                    btn.click()
                    speak("Flight selected")
                    time.sleep(5)
                    return True
                except:
                    continue
            
            speak("Could not click book button. Please select manually.")
            time.sleep(10)
            return True
            
        except Exception as e:
            print(f"Selection error: {e}")
            return False
    
    def proceed_to_payment(self):
        try:
            speak("Proceeding to payment")
            time.sleep(5)
            
            continue_keywords = ['Continue', 'Proceed', 'Next', 'Continue to Book']
            for keyword in continue_keywords:
                try:
                    btn = WebDriverWait(self.automation.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{keyword}')]"))
                    )
                    btn.click()
                    speak(f"Clicking {keyword}")
                    time.sleep(3)
                except:
                    continue
            
            skip_keywords = ['Skip', 'No thanks', 'Skip Seat', 'Skip Meal']
            for keyword in skip_keywords:
                try:
                    btns = self.automation.driver.find_elements(By.XPATH, f"//button[contains(text(),'{keyword}')]")
                    for btn in btns:
                        try:
                            btn.click()
                            time.sleep(2)
                        except:
                            continue
                except:
                    continue
            
            payment_keywords = ['Pay', 'Payment', 'Proceed to Pay', 'Make Payment']
            for keyword in payment_keywords:
                try:
                    btn = WebDriverWait(self.automation.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{keyword}')]"))
                    )
                    btn.click()
                    speak("Opening payment portal")
                    time.sleep(5)
                    break
                except:
                    continue
            
            speak("Payment page is open. Please complete payment manually for security.")
            return True
            
        except Exception as e:
            print(f"Payment error: {e}")
            speak("Please proceed to payment manually")
            return True

class YouTubeAutomation:
    def __init__(self):
        self.driver = None
    
    def play_video(self, search_query):
        try:
            print(f"🎵 Opening YouTube for: {search_query}")
            
            try:
                options = EdgeOptions()
                options.add_argument('--start-maximized')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                
                if WEBDRIVER_MANAGER_AVAILABLE:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=service, options=options)
                else:
                    self.driver = webdriver.Edge(options=options)
                    
                print("✅ Browser opened")
            except:
                try:
                    options = ChromeOptions()
                    options.add_argument('--start-maximized')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--no-sandbox')
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    
                    if WEBDRIVER_MANAGER_AVAILABLE:
                        service = ChromeService(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=service, options=options)
                    else:
                        self.driver = webdriver.Chrome(options=options)
                        
                    print("✅ Browser opened (Chrome)")
                except Exception as e:
                    print(f"❌ Could not open browser: {e}")
                    speak("Could not open browser")
                    return False
            
            speak(f"Searching for {search_query} on YouTube")
            
            self.driver.get("https://www.youtube.com")
            time.sleep(2)
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            first_video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
            )
            first_video.click()
            
            speak(f"Playing {search_query}")
            return True
            
        except Exception as e:
            print(f"YouTube automation error: {e}")
            speak("Could not play video on YouTube")
            return False

class FileSearcher:
    def __init__(self):
        self.search_paths = [
            Path.home() / "Desktop",
            Path.home() / "Documents",
            Path.home() / "Downloads",
            Path.home() / "Pictures",
            Path.home() / "Videos",
            Path.home() / "Music",
        ]
    
    def search_file(self, filename):
        try:
            speak(f"Searching for {filename}")
            print(f"🔍 Searching for: {filename}")
            
            found_files = []
            
            for search_path in self.search_paths:
                if search_path.exists():
                    print(f"📁 Searching in: {search_path}")
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if filename.lower() in file.lower():
                                full_path = Path(root) / file
                                found_files.append(full_path)
                                print(f"✅ Found: {full_path}")
            
            if found_files:
                speak(f"Found {len(found_files)} file{'s' if len(found_files) > 1 else ''}")
                
                first_file = found_files[0]
                speak(f"Opening {first_file.name}")
                os.startfile(str(first_file))
                
                if len(found_files) > 1:
                    print("\n📋 All found files:")
                    for i, file_path in enumerate(found_files, 1):
                        print(f"{i}. {file_path}")
                
                return True
            else:
                speak(f"Could not find {filename}")
                return False
                
        except Exception as e:
            print(f"File search error: {e}")
            speak("Error searching for file")
            return False
    
    def search_and_list(self, filename):
        try:
            found_files = []
            
            for search_path in self.search_paths:
                if search_path.exists():
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if filename.lower() in file.lower():
                                full_path = Path(root) / file
                                found_files.append(str(full_path))
            
            return found_files
        except Exception as e:
            print(f"Search error: {e}")
            return []

web_automation = WebAutomation()
youtube_automation = YouTubeAutomation()
file_searcher = FileSearcher()
flight_booking = FlightBooking()