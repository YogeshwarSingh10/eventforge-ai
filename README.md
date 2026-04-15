# EventForge AI

EventForge is a multi-agent conference planning system built using **LangGraph**.  
It decomposes conference organization into specialized AI agents that run in parallel and coordinate through a shared state.

---

## 🚀 Overview

Planning a large conference involves multiple independent but interconnected decisions — sponsors, speakers, venue, pricing, etc.

EventForge models this as a **Directed Acyclic Graph (DAG)** of agents:
- Each agent solves a specific subproblem
- Agents run **asynchronously and in parallel**
- Dependencies are explicitly modeled
- Outputs are merged into a final structured plan

---

## 🧠 Architecture

```text
.
├── app.py                  # (optional UI entry point)
├── docs/                   # engineering notes
├── notebooks/              # experimentation (pricing, etc.)
├── pyproject.toml
├── src/eventforge/
│   ├── agents/             # all agent implementations
│   │   ├── base/           # BaseAgent abstraction
│   │   ├── sponsor_agent.py
│   │   ├── speaker_agent.py
│   │   ├── venue_agent.py
│   │   ├── pricing_agent.py
│   │   └── final_agent.py
│   │
│   ├── graph/              # LangGraph DAG builder
│   │   └── builder.py
│   │
│   ├── models/             # schemas + state definitions
│   │   ├── schemas.py
│   │   └── state.py
│   │
│   ├── tools/              # external tools (web search, etc.)
│   │
│   ├── utils/              # logging, LLM client
│   │
│   └── main.py             # CLI entry point
```
---


### Execution Logic

- **Parallel stage**: Sponsor, Speaker, Venue  
- **Dependent stage**: Pricing (requires venue)  
- **Aggregation stage**: Final agent combines all outputs  

---

## ⚙️ Tech Stack

- **LangGraph** → DAG orchestration  
- **LangChain** → prompts, tools, chaining  
- **Pydantic** → strict structured outputs  
- **Async Python** → concurrency  
- **LLM APIs** → reasoning + generation  
- **Custom Tools** → web search integration  

---

## 🔧 System Components

### Agents

| Agent | Responsibility |
|------|--------|
| SponsorAgent | Find & rank sponsors |
| SpeakerAgent | Curate speakers |
| VenueAgent | Select venues |
| PricingAgent | Generate pricing tiers |
| FinalAgent | Aggregate outputs |

---

### State Management

All agents interact through a shared state:

- `input` → immutable user input  
- `outputs` → agent outputs (merged)  
- `agent_meta` → execution status  
- `shared_memory` → optional intermediate storage  
- `errors` → collected failures  

LangGraph reducers handle merging safely across parallel nodes.

---

### Tools

Agents use tools for external grounding:

- `search_sponsors`
- `search_speakers`
- `search_venues`

These abstract web search and can be extended to real APIs (Tavily, SerpAPI, etc.)

---

## ▶️ Running the Project

```bash
pip install -e .
python src/eventforge/main.py
