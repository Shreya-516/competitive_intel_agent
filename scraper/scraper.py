import requests
from bs4 import BeautifulSoup
import datetime

def scrape_website(company_url):
    """
    Visits the competitor's website and extracts all visible text.
    Think of this as the spy reading the enemy's notice board.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(company_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements - we only want readable text
        for tag in soup(["script", "style"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        return {
            "source": company_url,
            "content": text[:5000],  # First 5000 characters is enough
            "scraped_at": str(datetime.datetime.now())
        }
    except Exception as e:
        return {"source": company_url, "content": f"Error: {e}", "scraped_at": str(datetime.datetime.now())}

def scrape_news(company_name):
    """
    Searches Google News for recent mentions of the competitor.
    Think of this as the spy reading the newspaper for enemy mentions.
    """
    try:
        query = company_name.replace(" ", "+") + "+news"
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "xml")
        
        items = soup.find_all("item")[:5]  # Get top 5 news items
        news_list = []
        for item in items:
            news_list.append({
                "title": item.title.text if item.title else "No title",
                "description": item.description.text[:300] if item.description else "No description",
                "published": item.pubDate.text if item.pubDate else "Unknown date"
            })
        
        return news_list
    except Exception as e:
        return [{"title": f"Error fetching news: {e}", "description": "", "published": ""}]
    
def scrape_jobs(company_name):
    """
    Searches for recent job postings from the competitor.
    This is the most powerful intelligence source — what a company
    is hiring for tells you exactly what they are building next,
    often months before any public announcement.
    """
    try:
        query = company_name.replace(" ", "+") + "+jobs+hiring+2025"
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "xml")
        
        items = soup.find_all("item")[:5]
        jobs_list = []
        for item in items:
            jobs_list.append({
                "title": item.title.text if item.title else "No title",
                "description": item.description.text[:300] if item.description else "No description",
                "published": item.pubDate.text if item.pubDate else "Unknown date"
            })
        
        return jobs_list
    except Exception as e:
        return [{"title": f"Error fetching jobs: {e}", "description": "", "published": ""}]


# Test it out
if __name__ == "__main__":
    print("Testing scraper...")
    
    # Test website scraping
    result = scrape_website("https://techcrunch.com")
    print(f"\nWebsite scrape successful!")
    print(f"Characters collected: {len(result['content'])}")
    print(f"Preview: {result['content'][:200]}...")
    
    # Test news scraping
    print("\nFetching news...")
    news = scrape_news("Microsoft")
    for i, item in enumerate(news):
        print(f"\nNews {i+1}: {item['title']}")

