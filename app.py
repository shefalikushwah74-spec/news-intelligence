import os
from datetime import datetime
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"

st.set_page_config(
    page_title="Signal | AI News",
    page_icon="✦",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #f8fafc;
            color: #15243b;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.8rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #dbe5f0;
        }

        [data-testid="stSidebar"] * {
            color: #15243b;
        }

        .eyebrow {
            color: #1b719f;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .hero {
            color: #10233f;
            font-size: clamp(3rem, 7vw, 5.5rem);
            font-weight: 800;
            letter-spacing: -0.07em;
            line-height: 0.9;
            margin: 0.5rem 0 1rem;
        }

        .intro {
            color: #425a77;
            font-size: 1.13rem;
            line-height: 1.6;
            max-width: 47rem;
        }

        .brief-card {
            background: #ffffff;
            border: 1px solid #d9e5f1;
            border-radius: 20px;
            box-shadow: 0 10px 28px rgba(28, 67, 111, 0.07);
            padding: 1.4rem 1.65rem;
        }

        .source-card {
            background: #ffffff;
            border: 1px solid #d9e5f1;
            border-radius: 14px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.7rem;
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #d9e5f1;
            border-radius: 16px;
            padding: 1rem;
        }

        [data-testid="stMetricLabel"] {
            color: #526b87;
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: #142b4a;
            font-size: 1.15rem;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background: #c9efff;
            border: 1px solid #86cae9;
            border-radius: 10px;
            color: #102846;
            font-weight: 800;
            min-height: 2.75rem;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background: #afe4fb;
            border-color: #5db5dd;
            color: #102846;
        }

        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] > div {
            background: #ffffff;
            border-color: #b8cadd;
            color: #15243b;
        }

        label,
        .stCaption,
        [data-testid="stWidgetLabel"] p {
            color: #38536f !important;
            font-weight: 650;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def read_private_setting(name: str) -> str:
    value = os.getenv(name)

    if value:
        return value

    try:
        return str(st.secrets.get(name, ""))
    except Exception:
        return ""


def configure_services() -> bool:
    tavily_key = read_private_setting("TAVILY_API_KEY")
    groq_key = read_private_setting("GROQ_API_KEY")

    if not tavily_key or not groq_key:
        return False

    os.environ["TAVILY_API_KEY"] = tavily_key
    os.environ["GROQ_API_KEY"] = groq_key

    return True


def make_source_packet(results: list[dict[str, Any]]) -> str:
    entries = []

    for result in results:
        entries.append(
            f"""
TITLE: {result.get("title", "Untitled")}
URL: {result.get("url", "")}
CONTENT: {result.get("content", "")}
"""
        )

    return "\n\n---\n\n".join(entries)


@st.cache_data(ttl=900, show_spinner=False)
def build_briefing(query: str, result_count: int):
    search_tool = TavilySearchResults(
        max_results=result_count,
        search_depth="basic",
    )

    results = search_tool.invoke({"query": query})

    if isinstance(results, dict):
        results = results.get("results", [])

    sources = [item for item in results if isinstance(item, dict)]

    if not sources:
        raise ValueError("No relevant news found.")

    prompt = ChatPromptTemplate.from_template(
        """
You are a precise AI-news analyst.

Use only the source material below.

Write 4 to 6 concise Markdown bullet points.
Each bullet must describe a separate news development.
Do not invent facts.
Do not add a title.
Do not include links.

Finish with exactly one bullet beginning with:

**Why it matters:**

SOURCE MATERIAL:
{sources}
"""
    )

    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2,
    )

    chain = prompt | llm | StrOutputParser()

    summary = chain.invoke(
        {
            "sources": make_source_packet(sources),
        }
    )

    return summary, sources


with st.sidebar:
    st.markdown("## ✦ Signal")
    st.caption("A focused AI-news desk")

    st.divider()

    with st.form("news_form", border=False):
        st.markdown("### Build your briefing")

        
        query = st.text_input(
    "What do you want to know?",
    placeholder="Example: Latest AI breakthroughs in 2026",
)

        source_count = st.slider(
            "Number of sources",
            min_value=3,
            max_value=8,
            value=5,
        )

        generate = st.form_submit_button(
            "Generate briefing",
            use_container_width=True,
        )

    st.divider()

    st.caption(
        "Briefings are generated from live web sources. "
        "Verify important information independently."
    )

topic = query.strip()

st.markdown(
    '<div class="eyebrow">AI NEWS / LIVE RESEARCH</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero">A clearer view<br>of what changed.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="intro">Signal searches live web sources and turns them into a fast, readable AI news briefing.</div>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("Focus", topic or "Select a topic")
col2.metric("Source scan", f"{source_count} sources")
col3.metric("Edition", datetime.now().strftime("%d %b %Y"))

st.markdown("<br>", unsafe_allow_html=True)

if generate:
    if not topic:
        st.warning("Enter a custom topic first.")

    elif not configure_services():
        st.error("This app has not been configured by its administrator.")

    else:
        try:
            with st.spinner("Researching current AI news..."):
                briefing, sources = build_briefing(
                    topic,
                    source_count,
                )

            st.session_state["briefing"] = briefing
            st.session_state["sources"] = sources
            st.session_state["topic"] = topic
            st.session_state["generated_at"] = datetime.now().strftime("%H:%M")

        except Exception:
            st.error("Unable to create a briefing right now. Please try again.")

if "briefing" in st.session_state:
    st.markdown("### Your briefing")

    st.caption(
        f"{st.session_state['topic']} · "
        f"Generated at {st.session_state['generated_at']} · "
        f"{len(st.session_state['sources'])} sources reviewed"
    )

    st.markdown('<div class="brief-card">', unsafe_allow_html=True)
    st.markdown(st.session_state["briefing"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "Download briefing",
        data=st.session_state["briefing"],
        file_name="signal-ai-briefing.md",
        mime="text/markdown",
    )

    with st.expander("Read the sources"):
        for source in st.session_state["sources"]:
            title = source.get("title", "Untitled source")
            url = source.get("url", "")
            content = source.get("content", "")

            st.markdown('<div class="source-card">', unsafe_allow_html=True)

            if url:
                st.markdown(f"[{title}]({url})")
            else:
                st.markdown(f"**{title}**")

            st.caption(content)
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Select a focus in the sidebar, then generate a live briefing.")