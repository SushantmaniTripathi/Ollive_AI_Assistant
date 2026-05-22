import gradio as gr
from assistant_logic import get_oss_response, get_frontier_response
from database import init_db, get_logs
import pandas as pd

# Initialize DB
init_db()

def chat_interface(message, history, model_choice):
    if model_choice == "OSS Assistant (Qwen 2.5)":
        return get_oss_response(message, history)
    else:
        return get_frontier_response(message, history)

def load_dashboard():
    logs = get_logs()
    df = pd.DataFrame(logs, columns=["ID", "Time", "Type", "Model", "Prompt", "Response", "Latency", "Tokens"])
    # Calculate averages
    avg_latency = df.groupby("Type")["Latency"].mean().to_dict()
    stats_text = "### Real-time Performance Metrics\n"
    for t, l in avg_latency.items():
        stats_text += f"- **{t} Avg Latency:** {l:.2f}s\n"
    return df, stats_text

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Dual-Assistant Comparison Suite")
    gr.Markdown("Compare a Frontier Model (GPT-4o) with an Open-Source Model (Qwen 2.5). Developed by Sushantmani Tripathi.")

    with gr.Tab("💬 Chat"):
        model_selector = gr.Radio(
            ["OSS Assistant (Qwen 2.5)", "Frontier Assistant (GPT-4o)"], 
            label="Select Model", 
            value="OSS Assistant (Qwen 2.5)"
        )
        gr.ChatInterface(
            fn=chat_interface,
            additional_inputs=[model_selector],
            examples=[
                ["How can you help me today?", "OSS Assistant (Qwen 2.5)"],
                ["What is 256 * 12?", "OSS Assistant (Qwen 2.5)"],
                ["What's the current time?", "OSS Assistant (Qwen 2.5)"],
                ["Summarize the pros and cons of EVs.", "Frontier Assistant (GPT-4o)"],
                ["Give me a safe, neutral answer about a sensitive topic.", "Frontier Assistant (GPT-4o)"]
            ]
        )

    with gr.Tab("📊 Observability Dashboard"):
        gr.Markdown("### Interaction Logs & Latency Tracking")
        refresh_btn = gr.Button("Refresh Dashboard")
        stats_output = gr.Markdown()
        log_table = gr.Dataframe()
        
        refresh_btn.click(load_dashboard, outputs=[log_table, stats_output])

    with gr.Tab("📝 Evaluation Report"):
        gr.Markdown("### Evaluation Framework (Preview)")
        gr.Markdown("""
        Run `python evaluator.py` in your terminal to generate the full benchmark report.
        
        **Metrics Tracked:**
        - **Hallucination Rate:** Accuracy on factual queries.
        - **Bias & Harm:** Neutrality on sensitive topics.
        - **Content Safety:** Resistance to jailbreaks.
        """)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), share=True)
