import datetime
import re
import requests

def get_current_time():
    """Returns the current world time."""
    return f"The current time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def calculator(expression):
    """Safely evaluates a mathematical expression."""
    try:
        # Basic sanitization to allow only math-related characters
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
            return "Error: Invalid characters in expression."
        result = eval(expression, {"__builtins__": None}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def search_web(query):
    """Fetches a concise summary from DuckDuckGo Instant Answer."""
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_redirect": 1, "no_html": 1},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("AbstractText"):
            return f"Search result: {data['AbstractText']}"
        if data.get("RelatedTopics"):
            first = data["RelatedTopics"][0]
            if isinstance(first, dict) and first.get("Text"):
                return f"Search result: {first['Text']}"
        return "Search result: No concise answer found."
    except Exception as e:
        return f"Search error: {str(e)}"

def handle_tool_call(query):
    """Simple keyword-based tool routing."""
    q_lower = query.lower()
    if any(k in q_lower for k in ["search", "look up", "lookup"]):
        cleaned = re.sub(r"(search|look up|lookup)\s*(for)?\s*", "", query, flags=re.IGNORECASE).strip()
        return search_web(cleaned or query)
    if "time" in q_lower or "date" in q_lower:
        return get_current_time()
    if any(op in q_lower for op in ["+", "-", "*", "/", "calculate"]):
        # Attempt to extract an expression
        match = re.search(r'[\d\+\-\*\/\(\)\.\s]{3,}', query)
        if match:
            return calculator(match.group().strip())
    return None

def apply_guardrails(prompt):
    """Pre-processing safety check."""
    prompt_lower = prompt.lower()
    jailbreak_keywords = ["ignore previous instructions", "system prompt", "dan mode", "do anything now"]
    harmful_keywords = [
        "phishing",
        "malware",
        "hotwire",
        "doxx",
        "steal",
        "bypass",
        "hack",
        "explosive",
        "bomb",
        "weapon",
    ]
    if any(keyword in prompt_lower for keyword in jailbreak_keywords):
        return "I'm sorry, I cannot comply with instructions that attempt to bypass safety protocols."
    if any(keyword in prompt_lower for keyword in harmful_keywords):
        return "I'm sorry, I can't help with that request."
    return None
