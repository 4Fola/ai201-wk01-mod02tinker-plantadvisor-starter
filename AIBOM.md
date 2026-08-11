# AI Bill of Materials (AIBOM) - Plant Advisor

## 1. System Overview
- **System Name**: Plant Advisor Agent
- **Version**: 1.0.0
- **Purpose**: Autonomous AI agent assisting users with indoor plant care, incorporating tool calling for database lookups and seasonal context.

## 2. Model & API Dependencies
- **Primary LLM**: Groq API (`llama-3.3-70b-versatile` / `llama3-8b-8192`)
- **API Functionality**: Tool Calling / Function Calling enabled via Chat Completions
- **Max Tool Rounds**: 5 iterations per turn

## 3. Tool Inventory
| Tool Name | Source Function | Input Arguments | Output Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| `lookup_plant` | `tools.lookup_plant` | `plant_name` (str) | JSON (`found`, `plant`/`message`) | Queries local JSON database by slug, display name, or alias. |
| `get_seasonal_conditions` | `tools.get_seasonal_conditions` | `season` (optional str) | JSON (`season`, `temperature`, `humidity`, etc.) | Computes current or specified seasonal environmental factors. |

## 4. Data Assets
- **Local Database**: `data/plants.json`
  - **Sensitivity**: Public / Non-PII
  - **Data Structure**: Key-value JSON mapping plant slugs to care requirements and aliases.

## 5. Security & Risk Profile
- **STRIDE Analysis Summary**:
  - *Spoofing*: Mitigated via Groq API Key authentication stored in environment variables (`.env`).
  - *Tampering*: Input sanitization and casing normalization on tool inputs.
  - *Information Disclosure*: Minimal (public plant data); strict system prompts prevent prompt injection leakage.
  - *Denial of Service*: Capped loop executions via `MAX_TOOL_ROUNDS = 5`.