# Multi-Agent Research Assistant

A Python-based Multi-Agent Research System that automates the process of researching a topic, gathering information from the web, scraping relevant content, generating a structured report, and reviewing the report for quality improvements.

## Features

### Search Agent

* Performs web searches on the given topic.
* Collects recent and relevant information.
* Returns summarized search results.

### Scraper Agent

* Extracts detailed information from the most relevant sources.
* Provides deeper context beyond search snippets.

### Writer Agent

* Generates a comprehensive research report.
* Combines search results and scraped content.
* Produces a well-structured final document.

### Critic Agent

* Reviews the generated report.
* Identifies weaknesses, missing information, and improvement opportunities.
* Provides constructive feedback.

---

## Project Workflow

```text
User Topic
     │
     ▼
Search Agent
     │
     ▼
Scrape Agent
     │
     ▼
Writer Chain
     │
     ▼
Research Report
     │
     ▼
Critic Chain
     │
     ▼
Feedback
```

---

## Project Structure

```text
project/
│
├── agents.py
├── pipeline.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

If using OpenAI:

```env
OPENAI_API_KEY=your_api_key
```

---

## Running the Application

```bash
python pipeline.py
```

Example:

```text
Enter a research topic:
Artificial Intelligence in Healthcare
```

---

## Sample Output

```text
==================================================
Step 1 - Search agent is working...
==================================================

Search Results:
...

==================================================
Step 2 - Scrape agent is working...
==================================================

Scraped Content:
...

==================================================
Step 3 - Writer is drafting the report...
==================================================

Final Report:
...

==================================================
Step 4 - Critic is reviewing the report...
==================================================

Critique:
...
```

---

## Technologies Used

* Python
* LangChain
* LangGraph (optional)
* Tavily Search
* Web Scraping Tools
* LLMs (Groq/OpenAI/Ollama)

---

## Future Improvements

* Multi-step reflection loops
* Citation generation
* PDF report export
* Streamlit web interface
* Vector database integration (ChromaDB/FAISS)
* Human-in-the-loop approval workflow

---

## Author

Prajwal Tripathi

Built as a GenAI Multi-Agent Research Assistant project for learning Agentic AI systems, LangChain, LangGraph, and LLM orchestration.
