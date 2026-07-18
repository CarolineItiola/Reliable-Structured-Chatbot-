"""
Test Suite: The AI Workshop Reliable Structured Chatbot
10 edge case queries validating structured JSON output
and schema reliability.
"""
 
from chatbot import get_response, cache_stats
 
VALID_INTENTS = {
    "enrolment",
    "technical",
    "bootcamp",
    "complaint",
    "general"
}
 
REQUIRED_FIELDS = [
    "intent",
    "response_text",
    "suggested_actions",
    "confidence",
    "needs_human"
]
 
TEST_CASES = [
    {
        "id": 1,
        "description": "Basic general enquiry about AI Workshop",
        "query": "Tell me about the AI Workshop.",
        "expected_intent": "general"
    },
    {
        "id": 2,
        "description": "Bootcamp session date query",
        "query": "When is the next bootcamp session starting?",
        "expected_intent": "bootcamp"
    },
    {
        "id": 3,
        "description": "Enrolment, how to sign up",
        "query": "How do I enrol on the AI bootcamp?",
        "expected_intent": "enrolment"
    },
    {
        "id": 4,
        "description": "Technical support, cannot access materials",
        "query": (
            "I signed up but I cannot access "
            "any of my course materials."
        ),
        "expected_intent": "technical"
    },
    {
        "id": 5,
        "description": "Edge case, very short vague message",
        "query": "Hi",
        "expected_intent": "general"
    },
    {
        "id": 6,
        "description": "Edge case, asking about prerequisites",
        "query": (
            "Do I need any prior experience "
            "to join the bootcamp?"
        ),
        "expected_intent": "bootcamp"
    },
    {
        "id": 7,
        "description": "Edge case, asking about certificate",
        "query": (
            "Will I receive a certificate "
            "when I complete the course?"
        ),
        "expected_intent": "general"
    },
    {
        "id": 8,
        "description": "Edge case, frustrated student",
        "query": (
            "I have emailed three times and nobody "
            "has replied. This is very frustrating."
        ),
        "expected_intent": "complaint"
    },
    {
        "id": 9,
        "description": "Edge case, multiple questions at once",
        "query": (
            "How long is the bootcamp, is it free, "
            "and can I join if I am a complete beginner?"
        ),
        "expected_intent": "bootcamp"
    },
    {
        "id": 10,
        "description": "Edge case, off-topic question",
        "query": "Can you help me write my CV?",
        "expected_intent": "general"
    },
]
 
 
def validate_response(response):
    errors = []
 
    if response is None:
        errors.append(
            "Response was None, "
            "API call failed or JSON could not be parsed"
        )
        return errors
 
    for field in REQUIRED_FIELDS:
        if field not in response:
            errors.append("Missing field: " + field)
 
    if "intent" in response:
        if response["intent"] not in VALID_INTENTS:
            errors.append(
                "Invalid intent: " + str(response["intent"])
            )
 
    if "confidence" in response:
        try:
            c = float(response["confidence"])
            if not (0.0 <= c <= 1.0):
                errors.append(
                    "Confidence out of range: " + str(c)
                    + ", must be between 0.0 and 1.0"
                )
        except (TypeError, ValueError):
            errors.append(
                "Confidence is not a number: "
                + str(response["confidence"])
            )
 
    if "needs_human" in response:
        if not isinstance(response["needs_human"], bool):
            errors.append(
                "needs_human must be boolean, got: "
                + type(response["needs_human"]).__name__
            )
 
    if "suggested_actions" in response:
        if not isinstance(response["suggested_actions"], list):
            errors.append("suggested_actions must be a list")
 
    if "response_text" in response:
        if not isinstance(response["response_text"], str):
            errors.append("response_text must be a string")
 
    return errors
 
 
def run_tests():
    print("")
    print("=" * 55)
    print("The AI Workshop Chatbot, Test Suite (10 Edge Cases)")
    print("=" * 55)
    print("")
 
    passed = 0
    failed = 0
 
    for test in TEST_CASES:
        print(
            "Test " + str(test["id"])
            + ": " + test["description"]
        )
        print("  Query: " + test["query"])
 
        response = get_response(test["query"])
        errors = validate_response(response)
 
        if errors:
            print("  FAIL")
            for e in errors:
                print("    x " + e)
            failed += 1
        else:
            intent = response.get("intent", "unknown")
            confidence = response.get("confidence", 0)
            needs_human = response.get("needs_human", False)
            expected = test["expected_intent"]
            print("  PASS")
            print(
                "    Intent: " + intent
                + " (expected: " + expected + ")"
            )
            print("    Confidence: " + str(confidence))
            print("    Needs human: " + str(needs_human))
            print("    Schema valid")
            passed += 1
 
        print("")
 
    print("=" * 55)
    print("  RESULTS: " + str(passed) + "/10 passed")
    print(
        "  Passed: " + str(passed)
        + "  |  Failed: " + str(failed)
    )
    print("=" * 55)
 
    print("")
    print("Cache Performance:")
    print("  Cache hits:   " + str(cache_stats["cache_hits"]))
    print("  Cache misses: " + str(cache_stats["cache_misses"]))
    print("  Tokens saved: " + str(cache_stats["tokens_saved"]))
    print("")
 
 
if __name__ == "__main__":
    run_tests()