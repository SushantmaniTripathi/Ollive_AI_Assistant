
# 🤖 Dual AI Assistant Suite

Developed by **Sushantmani Tripathi**  
GitHub: [SushantmaniTripathi](https://github.com/SushantmaniTripathi)  
HF Space: [Sushant-Tripathi04/oss-assistant](https://huggingface.co/spaces/Sushant-Tripathi04/oss-assistant)
Evaluation_Pdf:  ai-assistant-project/eval_report.pdf

## 🌟 Overview
This project implements and evaluates two AI assistants:
1.  **Open Source Assistant:** Powered by `Qwen 2.5 (0.5B)` via Hugging Face Inference API.
2.  **Frontier Assistant:** Powered by `OpenAI GPT-4o`.

The suite includes a unified Gradio UI, real-time observability via SQLite, and an automated "LLM-as-a-Judge" evaluation framework.

** Summary :**
This project delivers a dual AI personal assistant system with multi-turn memory, tool use, and safety guardrails. It compares an open-source model with a hosted frontier model using a structured evaluation that measures hallucination rate (accuracy), content safety, and bias. The system includes observability logging, automated benchmarks, and a report-ready infographic to support hiring and compliance reviews.

---

## 🛠️ Features
-   **Multi-turn Memory:** Maintains short-term conversational context.
-   **Bonus Tools:** **Calculator**, **World Time**, and **DuckDuckGo Search**.
-   **Safety Guardrails:** Pre-processing layer to detect and block prompt injection.
-   **Observability:** SQLite dashboard tracking latency, prompts, and model performance.
-   **Automated Evaluation:** Factual, Adversarial, and Bias benchmarks scored by GPT-4o.

**ATS Keywords:** LLM evaluation, hallucination rate, bias testing, safety guardrails, prompt injection, multi-turn memory, tool use, observability, benchmarking, inference API, Gradio, SQLite, Hugging Face, OpenAI

---

## 🚀 Setup Instructions (Windows)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/SushantmaniTripathi/your-repo-name.git
    cd ai-assistant-project
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    -   Rename `.env.example` to `.env`.
    -   Add your `OPENAI_API_KEY` and `HF_API_TOKEN`.

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Access the UI at `http://127.0.0.1:7860`.

5.  **Run Evaluations:**
    ```bash
    python evaluator.py
    ```

---

## 📊 Comparison & Bonus Deliverables

### Cost + Latency Table (OSS Deployment)
| Metric | OSS (Qwen 2.5 0.5B) | Frontier (GPT-4o) |
| :--- | :--- | :--- |
| **Hosting** | HF Spaces (Free Tier) | OpenAI API |
| **Cost** | $0.00 (Inference API) | ~$0.01 / 1k tokens |
| **Avg Latency** | ~0.25s | ~2.45s |

### Architecture Decisions
-   **Gradio:** Chosen for rapid prototyping and native support for chat state.
-   **SQLite:** Used for lightweight, zero-config observability.
-   **Qwen 2.5 (0.5B):** Selected for reliable performance on the free CPU tier and fast inference.

---

## 📈 Evaluation Summary
Detailed metrics can be found in `eval_results.json`, `eval_summary.json`, and `eval_chart.png`.

---

## 💡 Future Improvements
-   **Long-term Memory:** Integrate Vector DB (ChromaDB) for RAG-based persistence.
-   **Fine-tuning:** SFT on specific safety datasets to improve OSS jailbreak resistance.
-   **Advanced Guardrails:** Integrate Llama-Guard or NeMo Guardrails.
