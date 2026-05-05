# Drift & Failure Analysis Report

## Findings
Based on an automated analysis of 10 recent interactions flagged with a `Thumbs Down` (-1 score), we have identified the following primary failure categories:

1. **Out-of-Scope Mishandling (60%)**: Users asked non-supply chain questions (e.g., IT support, password resets). Instead of declining the request gracefully, the agent forced the `calculate_risk_score` tool, producing nonsensical risk metrics for IT problems.
2. **Tone Issues (40%)**: When handling handover from the Logistics Researcher to the Manager, the agent's internal thought process was exposed directly to the user, creating a confusing and unprofessional user experience.

## Recommendation
The `Manager` node's system prompt must be updated to explicitly decline out-of-scope requests rather than attempting to calculate risk for them.
