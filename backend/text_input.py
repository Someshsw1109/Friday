import eel
import time

user_input_result = None
waiting_for_input = False

@eel.expose
def submit_text_input(text):
    global user_input_result, waiting_for_input
    user_input_result = text
    waiting_for_input = False
    print(f"✅ Received input: {text[:3]}***")
    return True

def get_text_input(prompt_message, is_password=False):
    global user_input_result, waiting_for_input
    
    try:
        user_input_result = None
        waiting_for_input = True
        
        eel.showTextInputPrompt(prompt_message, is_password)
        
        timeout = 60
        elapsed = 0
        
        while waiting_for_input and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1
        
        if user_input_result is None:
            print("⚠️ Text input timeout")
            return None
        
        result = user_input_result
        user_input_result = None
        waiting_for_input = False
        
        return result
        
    except Exception as e:
        print(f"Error in get_text_input: {e}")
        return None