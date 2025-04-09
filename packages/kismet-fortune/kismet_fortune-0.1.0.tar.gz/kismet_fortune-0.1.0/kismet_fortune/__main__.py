from google import genai
from google.genai import types
from prompt_toolkit import prompt
import os
import typer

system_instruction="""
You are the evolution of Slakware's venerable fortune-mod oracle. Using the input as inspiration, generate (or retrieve) an aphorism, proverb, quote, or other short text and return it. It can be witty, deep, funny, witty, or sexy in tone. Provide an attribution at the end.
"""

# Only run this block for Google AI API
gemini_api_key = os.environ.get("GEMINI_API_KEY")

# Check if the API key is set
if not gemini_api_key:
    def input_api_key(message: str) -> dict:
        return {
            'type': 'input',
            'name': 'api_key',
            'message': message
        }
    gemini_api_key = prompt(message="Please enter your Gemini API key:")
    if not gemini_api_key or gemini_api_key.strip() == "":
        raise ValueError("GEMINI_API_KEY environment variable not set. Exiting.")
    
client = genai.Client(api_key=gemini_api_key)

# CLI commands
app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

@app.command()
def fortune(prompt_text: str = "Kismet, tell me my fortune"):
    try:
        chat = client.models.generate_content_stream(model='gemini-2.0-flash-exp', config=types.GenerateContentConfig(system_instruction=system_instruction), contents=prompt_text,)
        full_text = ""
        for message in chat:
            full_text += message.text
            print(message.text, end="", flush=True)
        
        if not full_text:
            print("Kismet is silent.")
            
    except Exception as e:
        print(f"An unexpected fate occurred: {e}")
        
if __name__ == "__main__":
    app()