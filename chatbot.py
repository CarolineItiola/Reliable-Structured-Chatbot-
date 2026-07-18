import os
import json
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)
model = "claude-sonnet-4-5"

cache_stats = {
    "cache_hits": 0,
    "cache_misses": 0,
    "tokens_saved": 0
}

RESPONSE_SCHEMA = {
    "intent": str,
    "response_text": str,
    "suggested_actions": list,
    "confidence": float,
    "needs_human": bool
}

SYSTEM_PROMPT = """You are a professional customer service assistant 
for The AI Workshop, a UK tech company making AI education accessible 
to everyone. The AI workshop was founded by Stephen Nwoye. 
For more information about the company, visit https://www.theaiworkshop.co.uk/
You help students with: technical support, bootcamp sessions, 
complaints, and general enquiries.

Always respond in this exact JSON format:
{
    "intent": "enrolment|technical|bootcamp|complaint|general",
    "response_text": "Your professional response here",
    "suggested_actions": ["action 1", "action 2"],
    "confidence": 0.95,
    "needs_human": false
}

If needs_human is true, always include this in your response_text:
'Please email Caroline directly at itiolacaroline@yahoo.com and 
she will be happy to assist you personally.'

Before responding, reason through the query inside <thinking> tags.
Keep responses professional, warm, and encouraging, our students 
are on a learning journey."""

FEW_SHOT_EXAMPLES = """
Student: I have a general question about your AI courses.
Response:
{
    "intent": "general",
    "response_text": "Happy to help! What specifically would you
    like to know about our AI courses? Whether it's course content, 
    duration or entry requirements, I am here to assist. 
    AI Workshop offers a 14-week SQL and AI community bootcamps
    sessions designed to make AI education accessible to everyone.",
    "suggested_actions": ["Visit our website for more details", 
    "Follow us on LinkedIn"],
    "confidence": 0.90,
    "needs_human": false
}

Student: When is the next AI bootcamp session?
Response:
{
    "intent": "bootcamp",
    "response_text": "Thank you for your interest in our bootcamp sessions! 
    The next session date has not been confirmed yet. Please follow us
    on LinkedIn or check our website to be the first to know 
    when bookings open.",
    "suggested_actions": ["Follow The AI Workshop on LinkedIn",
    "Check our website for updates"],
    "confidence": 0.85,
    "needs_human": false
}
"""

def get_response(user_message, max_retries=3):
    for attempt in range(max_retries):
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": FEW_SHOT_EXAMPLES,
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": f"Student: {user_message}"
                        }
                    ]
                }
            ]
        )

        usage = response.usage
        if hasattr(usage, 'cache_read_input_tokens') and \
                usage.cache_read_input_tokens > 0:
            cache_stats["cache_hits"] += 1
            cache_stats["tokens_saved"] += usage.cache_read_input_tokens
        else:
            cache_stats["cache_misses"] += 1

        raw_text = response.content[0].text
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1

        try:
            data = json.loads(raw_text[start:end])
            return data
        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1} failed. Retrying...")

    print("Max retries reached.")
    return None