import re


def extract_yt_term(command):
    try:
        if not command:
            return None
        pattern = r'play\s+(.*?)\s+on\s+youtube'
        match = re.search(pattern, command, re.IGNORECASE)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error extracting YouTube term: {str(e)}")
        return None


def remove_words(input_string, words_to_remove):
    try:
        if not input_string:
            return ""
        if not words_to_remove:
            return input_string
        
        words = input_string.split()
        filtered_words = [word for word in words if word.lower() not in words_to_remove]
        result_string = ' '.join(filtered_words)
        
        return result_string
    except Exception as e:
        print(f"Error removing words: {str(e)}")
        return input_string
