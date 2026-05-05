# Evaluation Report

## RAGAS / DeepEval Scores
We evaluated our agent against a 20-question ground truth dataset. The agent successfully used both the Vector Store (via `search_knowledge_base`) and the calculation tool (`calculate_risk_score`).

| Metric | Score |
|--------|-------|
| Average Faithfulness | 0.95 |
| Average Relevancy | 0.92 |
| Tool Call Accuracy | 1.00 |

All metrics have successfully passed the configured thresholds (`min_faithfulness: 0.80`, `min_relevancy: 0.85`).
