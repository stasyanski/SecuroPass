# Securopass.py includes software logic

# --- Importing the required from main.py ---

from main import uppercase, symbols, numbers, password_length, phrase

# --- Check user preference ---

def user_preference(uppercase, symbols, numbers, password_length, phrase):
    preferences = {
        "Uppercase": uppercase,
        "Symbols": symbols,
        "Numbers": numbers,
        "Password length": password_length if password_length != 16 else "Default",
        "Phrase": phrase if phrase is not None else "blank"
    }

    for preference, value in preferences.items():
        print(f"{preference} is set to {value}")

# --- Main function ---

if __name__ == "__main__":
    user_preference(uppercase, symbols, numbers, password_length, phrase)