# PRD: Intelligent Supply Chain Risk Mitigation Agent (SCRM)

## 1. Problem Statement
Global supply chains are currently reactive. When a disruption occurs (e.g., a port strike, a factory fire, or a sudden price surge), logistics managers spend hours manually checking contracts, searching news feeds, and querying inventory databases to assess the impact. 

The **SCRM Agent** moves from reactive to proactive. It doesn't just "chat"; it monitors external feeds, reasons through internal inventory levels, and executes mitigation strategies (like drafting re-orders or rerouting shipments).

## 2. User Personas
*   **Primary User:** Logistics Operations Manager (needs quick impact assessments and action plans).
*   **Secondary User:** Procurement Officer (needs to approve alternative supplier suggestions).

## 3. Tool & Data Inventory
The agent interacts with the following "External World":

### Knowledge Sources (Perceive)
*   **Internal Inventory DB (SQL):** Real-time stock levels and warehouse locations.
*   **Supplier Contracts (PDFs/RAG):** Terms of service, lead times, and force majeure clauses.
*   **Live Logistics News API:** RSS feeds or news APIs filtering for "shipping," "strikes," or "weather."

### Action Tools (Execute)
*   `get_inventory_status(part_id)`: Python function to query the SQL database.
*   `search_alternative_suppliers(part_id)`: API call to a supplier directory or internal ERP.
*   `draft_slack_alert(message, channel)`: Sends a summary of the risk and proposed solution to the team.
*   `calculate_rerouting_cost(origin, destination)`: Python logic to estimate cost impacts of new routes.

## 4. Success Metrics
*   **MTTA (Mean Time to Awareness):** Time from an external event to a generated impact report (Target: < 5 minutes).
*   **Decision Accuracy:** Percentage of agent-proposed reroutes accepted by humans without modification (Target: > 80%).
*   **Manual Touchpoints:** Reduction in manual database queries performed by managers.
