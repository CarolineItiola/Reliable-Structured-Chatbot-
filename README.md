# Reliable-Structured-Chatbot-
Reliable Structured Chatbot with Prompt Caching

A portfolio project demonstrating a production-ready customer support chatbot for The AI Workshop, a UK tech company making AI education accessible to everyone.
Built using the Claude API, few-shot prompting, prompt caching, and structured
JSON output validation.

What This Project Does

This chatbot handles student enquiries for AI Workshop and returns every
response as a validated JSON object with a consistent structure. It covers
five intent categories: general enquiries, bootcamp sessions, enrolment,
technical support, and complaints.

The chatbot is deployed live on Streamlit Cloud and can be used directly
in a browser without any setup.

Techniques Used

Few-Shot Prompting — Before each student query, the chatbot is shown
three worked examples covering general, bootcamp, and technical intents.
This teaches Claude the exact response format required without any model
fine-tuning.

Prompt Caching — The system prompt and few-shot examples are marked
with cache_control: ephemeral. This means Claude stores them in memory
after the first call, reducing token usage and response time on every
subsequent message. Cache hits and misses are tracked and displayed.

Structured JSON Output — Every response follows a fixed schema with
five required fields: intent, response_text, suggested_actions, confidence,
and needs_human. This makes the output predictable and easy to process
downstream.

JSON Validation with Retry Logic — After each API call, the response
is parsed with json.loads(). If parsing fails, the chatbot retries
automatically up to three times before returning None. This ensures
reliability even if Claude returns unexpected formatting.

Human Escalation — When a query is too complex for the chatbot to
handle confidently, it sets needs_human: true and directs the student
to contact Caroline directly by email for personal assistance.

Response Schema

Every chatbot response returns the following JSON structure:

json{
    "intent": "enrolment|technical|bootcamp|complaint|general",
    "response_text": "Professional response to the student",
    "suggested_actions": ["action 1", "action 2"],
    "confidence": 0.95,
    "needs_human": false
}

Test Suite

A test suite of 10 edge case queries validates the chatbot across all
intent categories, including short vague messages, multiple questions
at once, frustrated students, off-topic questions, and prerequisite
enquiries. All 10 tests passed, confirming consistent schema output
across every scenario.

How to Run Locally


Clone the repository
Install dependencies:


pip install anthropic python-dotenv streamlit


Create a .env file and add your Anthropic API key:


ANTHROPIC_API_KEY=your-key-here


Run the Streamlit app:


streamlit run app.py


To run the test suite:


python test_chatbot.py

Security

The API key is stored in a .env file protected by .gitignore and
is never pushed to GitHub. For the live deployment, the key is stored
securely in Streamlit Secrets.

Skills Demonstrated


Claude API integration using the Anthropic Python SDK
Few-shot prompting for consistent structured output
Prompt caching with cache hit and miss tracking
JSON schema validation and retry logic
Human escalation routing
Streamlit frontend and cloud deployment
Automated test suite with edge case coverage