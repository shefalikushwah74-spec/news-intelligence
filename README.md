# News Intelligence

An AI-powered news research and summarisation application that searches live web sources and generates concise, source-grounded briefings based on user queries.

## Overview

News Intelligence allows users to enter a custom topic or question and receive a focused briefing based on current web sources. The application combines web search, large language models, and an interactive Streamlit interface to make news research faster and easier to understand.

## Features

* 🔎 Custom user queries for flexible news research
* 🌐 Live web search using Tavily
* 🤖 AI-generated summaries using Groq
* 📰 Concise, source-grounded news briefings
* 📚 Expandable source section with article links
* 📥 Downloadable briefing in Markdown format
* 🎨 Clean and responsive Streamlit interface
* 🔐 Environment-based API key configuration

## Tech Stack

* Python
* Streamlit
* LangChain
* Tavily Search
* Groq
* dotenv

## How It Works

```text
User Query
    ↓
Tavily Web Search
    ↓
Relevant News Sources
    ↓
LangChain Prompt
    ↓
Groq LLM
    ↓
AI-Generated News Briefing
```

## Project Structure

```text
news-intelligence/
│
├── app.py
├── newssummariser.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── README.md
└── .gitignore
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/shefalikushwah74-spec/news-intelligence.git
cd news-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Using pip:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file or expose API keys publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Example Queries

* Latest developments in AI agents
* Recent AI research breakthroughs
* AI applications in drug discovery
* New developments in generative AI
* AI policy and regulation updates

## Disclaimer

News briefings are generated from live web sources. Important information should be independently verified.

## Author

**Shefali Kushwah**

GitHub: [@shefalikushwah74-spec](https://github.com/shefalikushwah74-spec)
