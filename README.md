# Autonomous Competitive Intelligence Agent

An end-to-end agentic AI system that autonomously monitors competitor companies and delivers structured strategic intelligence reports. Point it at any company — it scrapes their website, tracks news mentions, analyzes hiring patterns, and uses Google Gemini to reason over everything and produce boardroom-quality insights.

---

## The Problem It Solves

Every product team needs to know what competitors are doing — new feature launches, pricing changes, hiring trends, strategic moves. Right now this is done manually by someone spending hours every week trawling websites, news, and job boards. This agent does it automatically, continuously, and with genuine reasoning — not just raw data aggregation.

---

## Architecture

```
User (Streamlit Dashboard)          n8n (Scheduled Automation)
           |                                    |
           └──────────────┬─────────────────────┘
                          ▼
                       api.py
                    (FastAPI Backend — Coordinator)
                          |
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   scrape_website()  scrape_news()  scrape_jobs()
          └───────────────┴───────────────┘
                          |
                    scraper/scraper.py
                    (Data Collection Layer)
                          |
                          ▼
                 rag_engine/memory.py
               (ChromaDB Vector Storage)
                          |
                          ▼
                 rag_engine/analyst.py
                 (Reasoning + Prompting)
                          |
                          ▼
                    Google Gemini API
                    (Strategic Analysis)
                          |
                          ▼
              Structured Intelligence Report
```

---

## What Each File Does

| File | Role | Description |
|------|------|-------------|
| `scraper/scraper.py` | Data Collection | Scrapes competitor website, fetches top 5 news articles via Google News RSS, and collects hiring signals — all as raw text |
| `rag_engine/memory.py` | Vector Storage | Stores scraped data in ChromaDB as vector embeddings. Enables semantic search — finds relevant content by meaning, not just keywords |
| `rag_engine/analyst.py` | Reasoning Layer | Retrieves relevant chunks from ChromaDB across 3 intelligence angles, builds a structured prompt, sends to Gemini, returns the report |
| `api.py` | Backend API | FastAPI wrapper that exposes the full pipeline as an HTTP endpoint so n8n can trigger it automatically |
| `app.py` | Frontend Dashboard | Streamlit dashboard for manual use — enter any company name and URL, get a full intelligence report in seconds |

---

## Intelligence Report Structure

Every report produced contains 6 sections:

1. **Executive Summary** — 2-3 sentence overview of the most important developments
2. **Key Developments** — 3-5 significant recent events with strategic context
3. **Strategic Direction** — What the company is clearly moving towards based on evidence
4. **Threats and Opportunities** — Competitive threats posed and weaknesses visible
5. **Watch List** — Specific things competitors should monitor in coming months
6. **Hiring Intelligence** — What job posting patterns reveal about unannounced future strategy

---

## Tech Stack

- **Python** — Core application language
- **BeautifulSoup4** — HTML parsing and text extraction from websites
- **Google News RSS** — Real-time news and hiring signal collection
- **ChromaDB** — Vector database for semantic storage and retrieval (RAG)
- **Google Gemini API** (`gemini-2.5-flash-lite`) — LLM reasoning and report generation
- **FastAPI** — REST API backend for programmatic access
- **Streamlit** — Interactive web dashboard
- **n8n** — Workflow orchestration and daily schedule automation
- **python-dotenv** — Secure API key management

---

## How RAG Works Here

RAG (Retrieval Augmented Generation) is the core intelligence pattern:

1. Scraped text is converted into vector embeddings by ChromaDB
2. When analysis runs, 3 semantic searches retrieve the most relevant chunks (product intelligence, financial intelligence, strategy/hiring intelligence)
3. Only the relevant chunks — not all stored data — are sent to Gemini
4. Gemini reasons over focused, relevant context rather than noisy raw data

This means the system finds insights by **meaning**, not just keyword matching. Searching for "AI products" surfaces documents about "machine learning launches" and "neural network hiring" even without exact word overlap.

---

## Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js v22+
- n8n installed globally (`npm install -g n8n`)

### Installation

```bash
# Clone the repository
git clone https://github.com/Shreya-516/competitive_intel_agent.git
cd competitive_intel_agent

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install requests beautifulsoup4 chromadb google-genai streamlit python-dotenv fastapi uvicorn langchain langchain-community
```

### Configuration

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com)

---

## Running the Project

### Option 1 — Streamlit Dashboard (Manual Use)

```bash
streamlit run app.py
```

Open `http://localhost:8501`, enter a company name and URL, click Run.

### Option 2 — API + n8n (Automated)

**Terminal 1 — Start the API server:**
```bash
uvicorn api:app --reload --port 8000
```

**Terminal 2 — Start n8n:**
```bash
n8n start
```

Open `http://localhost:5678` to configure the automated daily schedule workflow.

**API endpoint:**
```
POST http://localhost:8000/analyze
Body: { "company_name": "Netflix", "company_url": "https://www.netflix.com" }
```

---

## Example Output

Input: `Netflix` / `https://www.netflix.com`

The agent autonomously produces a structured report including findings like:

> *"Netflix's recent acquisition of an AI film technology company signals a strategic push toward AI-generated content pipelines, potentially reducing production costs significantly. Hiring patterns in ML infrastructure roles suggest proprietary recommendation system development ahead of a public announcement..."*

---

## Known Limitations and Future Improvements

- **Historical data:** The current implementation clears and refreshes data on each run. A production improvement would retain all historical data to enable trend detection over time — e.g. "Netflix has been hiring ML engineers for 6 consecutive weeks."
- **Email delivery:** n8n workflow currently stores reports in execution logs. Adding a Gmail/Slack node would enable fully autonomous morning delivery to stakeholders.
- **Job posting depth:** Currently uses news signals as a proxy for hiring patterns. Direct integration with LinkedIn Jobs or Greenhouse API would provide richer hiring intelligence.
- **Website scraping limits:** Some modern websites block scrapers or require JavaScript rendering. Adding Playwright for JS-rendered pages would improve coverage.

---

## Project Structure

```
competitive_intel_agent/
│
├── scraper/
│   └── scraper.py          # Web scraping, news, and hiring signal collection
│
├── rag_engine/
│   ├── memory.py            # ChromaDB vector storage and semantic retrieval
│   └── analyst.py           # Gemini prompting and report generation
│
├── api.py                   # FastAPI backend — exposes pipeline as REST endpoint
├── app.py                   # Streamlit dashboard — interactive frontend
├── .env                     # API keys (not committed to version control)
├── .gitignore               # Excludes venv, .env, memory_db, __pycache__
└── README.md
```

---

## Author

Shreya | B.Tech CSE | [GitHub](https://github.com/Shreya-516)