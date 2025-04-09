import os
from openai import OpenAI
from dotenv import load_dotenv
from robot.api.deco import keyword

load_dotenv()  # Load environment variables from .env

class AILibrary:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("API key is required for AILibrary")
        
        self.client = OpenAI(api_key=api_key)
    
    @keyword("Ask Gpt")
    def ask_gpt(self , prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role" : "user" , "content" : prompt }]
        )
        return response.choices[0].message.content.strip()

    @keyword("Classify Text")    
    def classify_text(self, text):
        prompt = f"Classify the following message as either 'Issue' or 'OK':\n\n{text}"
        response = self.client.chat.completions.create(
            model= "gpt-4o",
            messages=[{"role" :"user" , "content" : prompt}]
        )
        return response.choices[0].message.content.strip()