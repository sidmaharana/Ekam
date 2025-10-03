import google.generativeai as genai
import os
from dotenv import load_dotenv

def list_generative_models():
    """Lists the available generative models for the configured API key."""
    # Load environment variables from .env file in the parent directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found. Make sure your .env file is in the project root.")
        return

    try:
        genai.configure(api_key=api_key)
        
        print("Finding available models for your API key...")
        print("---------------------------------------------")
        
        found_models = False
        for model in genai.list_models():
            # Check if the model supports the 'generateContent' method
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")
                found_models = True

        if not found_models:
            print("No models supporting 'generateContent' were found for your API key.")
        else:
            print("---------------------------------------------")
            print("Please copy one of the model names from the list above and provide it.")

    except Exception as e:
        print(f"An error occurred while trying to list the models: {e}")

if __name__ == "__main__":
    list_generative_models()
