from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.scraper import scrape_website, scrape_news, scrape_jobs
from rag_engine.memory import store_data, clear_company_data
from rag_engine.analyst import analyze_competitor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Competitive Intelligence Agent API")

class CompanyRequest(BaseModel):
    company_name: str
    company_url: str

@app.get("/")
def root():
    return {"status": "Competitive Intelligence Agent is running"}

@app.post("/analyze")
def analyze(request: CompanyRequest):
    company_name = request.company_name
    company_url = request.company_url
    
    print(f"Starting analysis for {company_name}...")
    
    website_data = scrape_website(company_url)
    news_data = scrape_news(company_name)
    jobs_data = scrape_jobs(company_name)
    
    clear_company_data(company_name)
    store_data([website_data], company_name)
    store_data(news_data, company_name)
    store_data(jobs_data, company_name)
    
    report = analyze_competitor(company_name)
    
    return {
        "company": company_name,
        "report": report,
        "news_count": len(news_data),
        "jobs_count": len(jobs_data),
        "status": "success"
    }