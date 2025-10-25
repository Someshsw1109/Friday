# import multiprocessing


# def startJarvis():
#     print ("Process 1 Starting...")
#     from main import start
#     start()
    
# def listenHotword():
#     print ("Process 2 Starting...")
#     from backend.feature import hotword
#     hotword()
    
# if __name__ == "__main__":
#     process1 = multiprocessing.Process(target=startJarvis)
#     process2 = multiprocessing.Process(target=listenHotword)
#     process1.start()
#     process2.start()
#     process1.join()
    
#     if process2.is_alive():
#         process2.terminate()
#         print("Process 2 terminated.")
#         process2.join()
        
#     print("System is terminated.")

import multiprocessing
import os
import sys
import json
import time
import traceback

def ensure_cookie_file():
    """Ensure the cookie file exists before starting"""
    cookie_path = os.path.join('backend', 'cookie.json')
    try:
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        if not os.path.exists(cookie_path):
            with open(cookie_path, 'w') as f:
                json.dump({}, f)
            print(f"Created cookie file at {cookie_path}")
    except Exception as e:
        print(f"Error creating cookie file: {e}")

def ensure_database():
    """Ensure the database file exists"""
    db_path = "jarvis.db"
    if not os.path.exists(db_path):
        print(f"Warning: Database file {db_path} not found")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''CREATE TABLE IF NOT EXISTS sys_command
                            (id INTEGER PRIMARY KEY, name TEXT, path TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS web_command
                            (id INTEGER PRIMARY KEY, name TEXT, url TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY, name TEXT, Phone TEXT)''')
            
            conn.commit()
            conn.close()
            print(f"Created database at {db_path}")
        except Exception as e:
            print(f"Error creating database: {e}")

def startJarvis():
    """Main process that runs the Eel application"""
    try:
        print("Process 1 Starting...")
        from main import start
        start()
    except Exception as e:
        print(f"Error in startJarvis: {e}")
        traceback.print_exc()

def listenHotword():
    """Hotword detection process"""
    try:
        print("Process 2 Starting...")
        # Add delay to ensure main process is ready
        time.sleep(5)
        from backend.feature import hotword
        hotword()
    except Exception as e:
        print(f"Error in listenHotword: {e}")
        traceback.print_exc()

def main():
    """Main function with proper process management"""
    # Set multiprocessing start method (important for Windows)
    if sys.platform == 'win32':
        try:
            multiprocessing.set_start_method('spawn', force=True)
        except RuntimeError:
            pass  # Already set
    
    # Ensure required files exist
    ensure_cookie_file()
    ensure_database()
    
    # Create processes
    process1 = multiprocessing.Process(target=startJarvis)
    process2 = multiprocessing.Process(target=listenHotword)
    
    try:
        # Start both processes
        process1.start()
        print("Main process started")
        
        # Give the main process time to initialize Eel
        time.sleep(3)
        
        process2.start()
        print("Hotword process started")
        
        # Wait for the main process to complete
        process1.join()
        
        # If main process ends, terminate the hotword process
        if process2.is_alive():
            print("Terminating hotword process...")
            process2.terminate()
            process2.join(timeout=5)
            
            # Force kill if it doesn't terminate gracefully
            if process2.is_alive():
                print("Force killing hotword process...")
                process2.kill()
                process2.join()
        
        print("Process 2 terminated.")
                
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down...")
        
        # Gracefully terminate processes
        if process1.is_alive():
            print("Terminating main process...")
            process1.terminate()
            process1.join(timeout=5)
            
        if process2.is_alive():
            print("Terminating hotword process...")
            process2.terminate()
            process2.join(timeout=5)
            
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()
        
        # Clean up processes on error
        if process1.is_alive():
            process1.terminate()
            
        if process2.is_alive():
            process2.terminate()
            
    finally:
        print("System terminated.")

if __name__ == "__main__":
    main()