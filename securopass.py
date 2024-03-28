# Securopass.py includes software logic

# --- Importing the required from main.py ---

from main import pref

# --- Check user preference ---
def user_preference(pref):
    
    
    preferences = {
        "Uppercase": pref.uppercase,
        "Symbols": pref.symbols,
        "Numbers": pref.numbers,
        "Password length": pref.length if pref.length != 16 else "default",
        "Phrase": pref.phrase if pref.phrase is not None else "blank"
    }

    for preference, value in preferences.items():
        print(f"{preference} is set to {value}")

user_preference(pref)