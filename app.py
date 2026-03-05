import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.scraper import scrape_website, scrape_news, scrape_jobs
from rag_engine.memory import store_data, clear_company_data
from rag_engine.analyst import analyze_competitor
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Competitive Intelligence Agent",
    page_icon=None,
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #1a1a2e;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #16213e;
    }
    .report-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 1rem;
    }
    .section-divider {
        border-top: 2px solid #e0e0e0;
        margin: 1.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("## Competitive Intelligence Agent")
st.markdown("Autonomous AI-powered competitor monitoring and strategic analysis")
st.divider()

# Sidebar for input
with st.sidebar:
    st.markdown("### Target Company")
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Google, Apple, Netflix",
        help="Enter the competitor company you want to analyze"
    )
    company_url = st.text_input(
        "Company Website URL",
        placeholder="e.g. https://www.google.com",
        help="Enter the competitor's main website URL"
    )
    
    st.divider()
    analyze_button = st.button(
        "Run Intelligence Report",
        type="primary",
        use_container_width=True
    )
    
    st.divider()
    st.markdown("### How It Works")
    st.markdown("""
    1. Scrapes the company website  
    2. Fetches latest news articles  
    3. Stores data in RAG memory  
    4. Analyzes with Gemini AI  
    5. Delivers structured strategic insights  
    """)

# Main content area
if analyze_button:
    if not company_name or not company_url:
        st.error("Please enter both a company name and website URL to proceed.")
    else:
        with st.status("Collecting intelligence...", expanded=True) as status:
            st.write(f"Visiting {company_url}...")
            website_data = scrape_website(company_url)
            st.write(f"Collected {len(website_data['content'])} characters from website.")

            st.write(f"Fetching latest news about {company_name}...")
            news_data = scrape_news(company_name)
            st.write(f"Found {len(news_data)} recent news articles.")
            st.write(f"Scanning job postings for {company_name}...")
            jobs_data = scrape_jobs(company_name)
            st.write(f"Found {len(jobs_data)} job related signals.")

            st.write("Storing intelligence in RAG memory...")
            clear_company_data(company_name)
            store_data([website_data], company_name)
            store_data(news_data, company_name)
            store_data(jobs_data, company_name)
            st.write("Intelligence stored successfully.")

            st.write("Sending to Gemini AI for analysis...")
            status.update(label="Analyzing...", state="running")

            report = analyze_competitor(company_name)
            status.update(label="Analysis complete.", state="complete")

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Intelligence Report")
            st.markdown(report)

        with col2:
            st.markdown("### Latest News")
            for i, news in enumerate(news_data):
                with st.expander(f"{news.get('title', 'Article')[:60]}..."):
                     st.write(news.get('description', 'No description available.'))
                     st.caption(f"Published: {news.get('published', 'Unknown')}")
    
            st.markdown("### Hiring Intelligence")
            for i, job in enumerate(jobs_data):
                with st.expander(f"{job.get('title', 'Job Signal')[:60]}..."):
                    st.write(job.get('description', 'No description available.'))
                    st.caption(f"Published: {job.get('published', 'Unknown')}")

            st.markdown("### Raw Website Data")
            with st.expander("View scraped content"):
                st.text(website_data['content'][:1000] + "...")

else:
    st.markdown("### Enter a target company in the sidebar to generate an intelligence report.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Web Scraping**\n\nAutomatically visits and reads competitor websites in real time.")
    with col2:
        st.info("**RAG Memory**\n\nStores intelligence using vector embeddings for semantic search.")
    with col3:
        st.info("**AI Analysis**\n\nGemini reasons over collected data to produce strategic insights.")
