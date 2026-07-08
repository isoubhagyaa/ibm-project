# 🥗 AI-Powered Nutrition Agent

> An IBM Langflow / IBM Orchestrate-powered multi-agent system for personalized dietary guidance, meal planning, food tracking, and preventive health management.

---

## 📋 Overview

The Nutrition Agent addresses the challenge of scattered, non-personalized dietary guidance by combining a **Multi-Agent Architecture** with **IBM AI models** and **RAG-based food data retrieval** to deliver:

- 🍽️ **Personalized Diet Plans** — Based on age, health conditions, allergies, cultural preferences, and fitness goals
- 🔍 **Food Data RAG Retrieval** — Real-time nutritional values from reliable sources
- 📊 **Diet Tracking & Feedback** — Log meals via text, images, or voice with instant analysis
- 💊 **Preventive Health Focus** — Chronic disease management (diabetes, heart health, etc.)
- 📈 **Visualization Dashboard** — Daily/weekly nutrient intake, deficiencies, and goal progress

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    IBM Orchestrate Orchestrator                   │
│                  (Routes queries to sub-agents)                   │
└──────────┬──────────────┬──────────────┬───────────┬────────────┘
           │              │              │           │
    ┌──────▼──────┐ ┌─────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
    │  Nutrition  │ │   Diet     │ │  Health  │ │  Food Log   │
    │  Knowledge  │ │ Recommend. │ │ Advisory │ │  Feedback   │
    │   Agent     │ │   Agent    │ │  Agent   │ │   Agent     │
    └──────┬──────┘ └─────┬──────┘ └───┬──────┘ └──┬──────────┘
           │              │            │            │
    ┌──────▼──────────────▼────────────▼────────────▼────────────┐
    │              IBM watsonx.ai (granite-13b-chat)               │
    │           Vector Store (Chroma) + USDA FoodData API          │
    └─────────────────────────────────────────────────────────────┘
```

---

## 🤖 Multi-Agent System

| Agent | Role | IBM Model |
|-------|------|-----------|
| **Nutrition Knowledge Agent** | Fetches & summarizes nutritional data via RAG | `ibm/granite-13b-chat-v2` |
| **Diet Recommendation Agent** | Generates personalized meal plans | `ibm/granite-13b-instruct-v2` |
| **Health Advisory Agent** | Preventive health & chronic disease diet guidance | `ibm/granite-13b-chat-v2` |
| **Food Log & Feedback Agent** | Meal logging, analysis, and progress tracking | `ibm/granite-3-8b-instruct` |

---

## 📁 Project Structure

```
nutrition-agent/
├── agents/
│   ├── nutrition_knowledge_agent.json   # RAG-based food data fetcher
│   ├── diet_recommendation_agent.json   # Personalized meal planner
│   ├── health_advisory_agent.json       # Preventive health advisor
│   └── food_log_feedback_agent.json     # Meal tracker & analyzer
│
├── flows/
│   ├── main_orchestrator.json           # IBM Langflow master flow
│   ├── rag_food_data_flow.json          # RAG pipeline for food DB
│   └── meal_planning_flow.json          # Meal plan generation flow
│
├── config/
│   ├── watsonx_config.yaml              # IBM watsonx.ai credentials
│   ├── vector_store_config.yaml         # ChromaDB / Milvus config
│   └── api_keys.yaml.example            # API key template (do not commit secrets)
│
├── data/
│   ├── food_database/                   # Seeded nutritional knowledge base
│   │   ├── usda_foods_sample.json
│   │   └── disease_diet_guidelines.json
│   └── user_profiles/                   # Sample user profiles
│       └── sample_profiles.json
│
├── dashboard/
│   └── index.html                       # Visualization dashboard (standalone)
│
├── scripts/
│   ├── seed_vector_store.py             # Load food data into ChromaDB
│   └── test_agents.py                   # Agent integration tests
│
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Orchestration** | IBM Langflow · IBM watsonx Orchestrate |
| **LLM** | IBM watsonx.ai — `granite-13b-chat-v2`, `granite-13b-instruct-v2` |
| **RAG / Vector DB** | ChromaDB · LangChain Document Loaders |
| **Food Data API** | USDA FoodData Central API |
| **Frontend Dashboard** | HTML5 · Chart.js · Vanilla JS |
| **Backend API** | Python FastAPI |
| **Auth** | IBM App ID |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install langflow ibm-watsonx-ai chromadb langchain fastapi uvicorn
```

### 1. Configure IBM watsonx credentials

```bash
cp config/api_keys.yaml.example config/api_keys.yaml
# Edit config/api_keys.yaml with your IBM Cloud API key and project ID
```

### 2. Seed the vector store

```bash
python scripts/seed_vector_store.py
```

### 3. Launch Langflow

```bash
langflow run --host 0.0.0.0 --port 7860
# Import flows/main_orchestrator.json into the Langflow UI
```

### 4. Open the Dashboard

Open `dashboard/index.html` in any browser.

---

## 🔒 Security Notes

- Never commit `config/api_keys.yaml` — it is `.gitignore`d
- Use IBM App ID for user authentication in production
- All PII (user health data) should be encrypted at rest using IBM Key Protect

---

## 📄 License

MIT — See LICENSE for details.
