import os
import time
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from database import log_interaction
from tools import handle_tool_call, apply_guardrails

load_dotenv()

# Initialize Clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
hf_client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))

def _parse_history(history):
    """Parse chat history from Gradio 6.x (list of dicts) or legacy (list of tuples)."""
    pairs = []
    if not history:
        return pairs
    # Gradio 6.x: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    if isinstance(history[0], dict):
        user_msg = None
        for msg in history:
            if msg.get("role") == "user":
                user_msg = msg.get("content", "")
            elif msg.get("role") == "assistant" and user_msg is not None:
                pairs.append((user_msg, msg.get("content", "")))
                user_msg = None
    else:
        # Legacy Gradio 3.x/4.x: [("user msg", "assistant msg"), ...]
        for h in history:
            pairs.append((h[0], h[1]))
    return pairs

def get_frontier_response(prompt, history):
    # Check Guardrails
    violation = apply_guardrails(prompt)
    if violation:
        return violation

    # Check Tools
    tool_output = handle_tool_call(prompt)
    if tool_output:
        prompt = f"System: Tool result: {tool_output}\nUser: {prompt}"

    start_time = time.time()
    
    try:
        # Build message history (supports Gradio 6.x dict format)
        messages = [{"role": "system", "content": "You are a helpful and safe frontier AI assistant."}]
        for user_msg, asst_msg in _parse_history(history)[-5:]:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": asst_msg})
        messages.append({"role": "user", "content": prompt})

        response = openai_client.chat.completions.create(
            model=os.getenv("MODEL_FRONTIER", "gpt-4o"),
            messages=messages
        )
        
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"[Frontier model error] {str(e)}"
    
    latency = time.time() - start_time
    
    log_interaction("Frontier", os.getenv("MODEL_FRONTIER"), prompt, answer, latency)
    return answer

def get_oss_response(prompt, history):
    # Check Guardrails
    violation = apply_guardrails(prompt)
    if violation:
        return violation

    # Check Tools
    tool_output = handle_tool_call(prompt)
    if tool_output:
        prompt = f"User: (Background Tool Result: {tool_output}) {prompt}"

    start_time = time.time()
    
    # Build chat messages for HF InferenceClient
    model_name = os.getenv("MODEL_OSS", "Qwen/Qwen2.5-0.5B-Instruct")
    messages = [{"role": "system", "content": "You are a helpful open-source assistant."}]
    for user_msg, asst_msg in _parse_history(history)[-5:]:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": asst_msg})
    messages.append({"role": "user", "content": prompt})

    try:
        response = hf_client.chat_completion(
            model=model_name,
            messages=messages,
            max_tokens=512,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"[OSS model error] {str(e)}"
    latency = time.time() - start_time
    
    log_interaction("OSS", os.getenv("MODEL_OSS"), prompt, answer, latency)
    return answer
