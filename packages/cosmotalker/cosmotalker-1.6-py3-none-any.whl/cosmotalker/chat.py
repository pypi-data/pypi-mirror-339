import os
import sys

# Ensure the script finds local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get import get
from apod import apod
from celestrak import celestrak
from search import search
from feedback import feedback
from spacex import spacex

def chat():
    chat_data_file = "chat_data.txt"
    
    print("CosmoTalker Chat started. Type 'exit' to end the session.")
    
    common_phrases = {
        "tell me about": "define ",
        "what is": "define ",
        "who is": "define ",
        "explain": "define ",
        "describe": "define "
    }
    
    common_words = {"a", "an", "the", "is", "of", "and", "on", "in", "to", "for", "with"}
    
    while True:
        try:
            user_input = input("You: ").strip().lower()
        
            if user_input == "exit":
                print("Goodbye!")
                break
        
            # Convert common phrases to structured queries
            for phrase, replacement in common_phrases.items():
                if user_input.startswith(phrase):
                    user_input = user_input.replace(phrase, replacement, 1).strip()
                    break
        
            # Remove common words
            user_input = " ".join([word for word in user_input.split() if word not in common_words])
        
            # Store conversation history
            with open(chat_data_file, "a", encoding="utf-8") as file:
                file.write(f"User: {user_input}\n")
        
            # Determine response
            response = "I'm not sure about that. Try asking in a different way."
            
            if user_input in {"hi", "hello", "hey"}:
                response = "Hello! How can I assist you?"
            elif user_input.startswith("define "):
                query = user_input.replace("define ", "").strip()
                result = get(query)
                response = f"I found these in my data library: {result}" if result else "I couldn't find anything relevant."
            elif "apod" in user_input:
                response = apod()
            elif "track" in user_input or "satellite" in user_input:
                response = celestrak()
            elif "search" in user_input:
                query = user_input.replace("search ", "").strip()
                result = search(query)
                response = f"Here are your search results: {result}" if result else "No matches found."
            elif "feedback" in user_input:
                response = feedback(user_input.replace("feedback ", "").strip())
            elif "spacex" in user_input:
                response = spacex()
            else:
                print('''\tI found these in my data library''')
                response = get(user_input)
        
            print(f"CosmoTalker: {response}")
        
            # Store bot response
            with open(chat_data_file, "a", encoding="utf-8") as file:
                file.write(f"CosmoTalker: {response}\n")
        
        except Exception as e:
            print(f"Error: {e}")
chat()
