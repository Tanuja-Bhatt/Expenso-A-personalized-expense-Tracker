import cohere
from dotenv import load_dotenv
import os

load_dotenv()
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def get_budget_insights(user_query, transactions_text):
    prompt = f"""
You are an expert financial advisor. Given the user’s transactions:
{transactions_text}

User question: {user_query}

Provide a concise, actionable answer in 2–3 sentences.
"""
    try:
        # Use the Chat API with a single message string
        response = co.chat(
            model='command-xlarge-nightly',
            message=prompt
            # stream=False
        )
        # Extract the assistant’s reply
        return response.text.strip()

    except cohere.errors.UnauthorizedError:
        return "Error: Invalid Cohere API key."

    except Exception as e:
        return f"Error fetching advice: {e}"
