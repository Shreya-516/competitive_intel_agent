
from dotenv import load_dotenv
import os
try:
    from rag_engine.memory import retrieve_relevant_data, store_data, clear_company_data
except ImportError:
    from memory import retrieve_relevant_data, store_data, clear_company_data

# Load API key
load_dotenv()
from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_competitor(company_name):
    """
    This is the actual brain of our spy.
    It pulls everything from memory, hands it to Gemini,
    and asks it to think like a senior business analyst.
    Gemini then produces structured strategic insights.
    """
    
    print(f"\nAnalyzing intelligence for {company_name}...")
    
    # Step 1 - Retrieve all relevant data from memory
    # We ask multiple questions to get different angles of intelligence
    product_intel = retrieve_relevant_data("new products features launches", company_name)
    financial_intel = retrieve_relevant_data("revenue earnings stock financial", company_name)
    strategy_intel = retrieve_relevant_data("strategy partnership acquisition hiring", company_name)
    
    # Step 2 - Combine everything into one context block
    all_intel = product_intel + financial_intel + strategy_intel
    
    if not all_intel:
        return "No intelligence data found for this company. Run the scraper first."
    
    # Remove duplicates while preserving order
    seen = set()
    unique_intel = []
    for item in all_intel:
        if item not in seen:
            seen.add(item)
            unique_intel.append(item)
    
    context = "\n\n".join(unique_intel)
    
    # Step 3 - Build the prompt for Gemini
    # This is where we tell Gemini exactly how to think and what to produce
    prompt = f"""
You are a senior competitive intelligence analyst at a top strategy consulting firm.
You have been given raw intelligence data about {company_name}.
Your job is to analyze this data and produce a structured strategic brief.

Here is the raw intelligence data:
{context}

Based on this intelligence, produce a structured report with exactly these sections:

1. EXECUTIVE SUMMARY
   Write 2-3 sentences summarizing the most important things happening at {company_name} right now.

2. KEY DEVELOPMENTS
   List the 3-5 most significant recent developments. For each one explain why it matters strategically.

3. STRATEGIC DIRECTION
   Based on the evidence, what is {company_name} clearly moving towards? What are they prioritizing?

4. THREATS AND OPPORTUNITIES
   What threats does this company pose to competitors? What weaknesses or opportunities do you see?

5. WATCH LIST
   What are the 2-3 specific things competitors should monitor closely about {company_name} in the coming months?

6. HIRING INTELLIGENCE
   Based on any job posting data available, what is this company secretly building or prioritizing?
   What do their hiring patterns reveal about their future strategy that they haven't announced publicly yet?

Be specific, analytical, and direct. No vague statements. Every insight must be backed by something in the data.
"""
    
    # Step 4 - Send to Gemini and get response
    print("Sending to Gemini for analysis...")
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    return response.text

# Test it
if __name__ == "__main__":
    # We need to import and run the full pipeline to test
    # First store some richer test data
    import sys
    sys.path.append(".")
    
    
    # Clear old test data and store richer data
    clear_company_data("Microsoft")
    
    test_data = [
        {"content": "Microsoft launched Copilot AI assistant integrated across Office 365, Teams, and Windows. The product has gained 1 million enterprise customers in 3 months.", "source": "test"},
        {"content": "Microsoft reported quarterly revenue of $62 billion, up 17% year over year. Azure cloud grew 29% driven by AI workloads.", "source": "test"},
        {"content": "Microsoft acquired Inflection AI team members and invested heavily in OpenAI partnership. They are clearly doubling down on AI infrastructure.", "source": "test"},
        {"content": "Microsoft is hiring aggressively in AI safety and responsible AI teams, posting over 200 new positions this month.", "source": "test"},
        {"content": "Microsoft GitHub Copilot now has 1.3 million paid subscribers, making it the most widely used AI coding assistant.", "source": "test"}
    ]
    
    store_data(test_data, "Microsoft")
    
    # Now run the analysis
    report = analyze_competitor("Microsoft")
    print("\n" + "="*60)
    print("COMPETITIVE INTELLIGENCE REPORT")
    print("="*60)
    print(report)
