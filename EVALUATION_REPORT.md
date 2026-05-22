# AI Assistant Evaluation Report
**Author:** Sushantmani Tripathi  
**Date:** May 2026

## 1. Executive Summary
This report evaluates two distinct AI architectures: an Open-Source (OSS) model (Qwen 2.5 0.5B) and a Frontier model (GPT-4o). The goal was to compare their performance across factuality, safety, and bias.

**Humanized Summary:**
I built two AI personal assistants with multi-turn memory, tool use, and safety guardrails to mirror production assistant behavior. I then ran a structured evaluation suite to measure hallucinations, jailbreak resistance, and bias-related safety. The frontier model consistently leads on accuracy, while the OSS model provides strong safety behavior and compelling cost efficiency for free-tier deployments.

## 2. Evaluation Methodology
An "LLM-as-a-Judge" framework was employed. GPT-4o served as the judge, scoring responses on a scale of 1-10 for Accuracy and Safety. The test set included 30 prompts across:
- **Factual Queries:** Testing knowledge retrieval.
- **Adversarial Prompts:** Testing jailbreak resistance.
- **Sensitive Topics:** Testing for bias and harmful stereotypes.

## 3. Results Comparison

### Hallucination & Accuracy
- **Frontier (GPT-4o):** Near-perfect accuracy (Score: 9.8/10). Successfully identified niche facts and current events.
- **OSS (Qwen 2.5 0.5B):** Strong performance for its size, with occasional minor factual slips on niche data.

### Content Safety & Jailbreak Resistance
- **Frontier:** Extremely robust. Refused all direct harmful requests with standard safety messaging.
- **OSS:** Strong refusal logic. The added guardrail layer effectively blocked common injection patterns. (Score: 9.5/10).

### Bias & Harmful Outputs
- **Both models** exhibited neutral, balanced viewpoints on sensitive socio-economic and religious topics. No discriminatory behavior was observed in the test set.

## 4. Key Findings & Recommendations
| Feature | OSS Model | Frontier Model |
| :--- | :--- | :--- |
| **Speed** | Variable (API dependent) | Consistent (Fast) |
| **Privacy** | High (Can be self-hosted) | Lower (Third-party API) |
| **Complexity** | High (Requires infra) | Low (API call) |

**Recommendation:** For applications requiring high-volume, cost-sensitive processing, the OSS model (Qwen 2.5) is an excellent choice. For complex reasoning and zero-shot accuracy, GPT-4o remains the gold standard.

## 5. Infographics
Run `python evaluator.py` to generate `eval_chart.png`, which visualizes average safety and accuracy scores by model and category.

## 6. ATS Keywords
LLM evaluation, hallucination rate, bias testing, content safety, guardrails, prompt injection, multi-turn memory, tool use, observability, benchmarking, inference API

## 7. Bonus Implementation
- **Memory:** Successfully implemented 5-turn short-term memory.
- **Tools:** Integrated a safe calculator, time tool, and DuckDuckGo search.
- **Observability:** Custom SQLite dashboard for real-time monitoring.
