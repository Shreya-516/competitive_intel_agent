import chromadb
from dotenv import load_dotenv
import os

# Load our API key from .env file
load_dotenv()

# Initialize ChromaDB - this is our memory bank
# Think of this as setting up a filing cabinet on your computer
client = chromadb.PersistentClient(path="./memory_db")

# Create a collection - think of this as a drawer inside the filing cabinet
# specifically for competitor intelligence
collection = client.get_or_create_collection(
    name="competitor_intel",
    metadata={"description": "Stores all competitor intelligence data"}
)

def store_data(data_list, company_name):
    """
    Takes scraped data and stores it in ChromaDB.
    Think of this as the spy filing their report into the cabinet.
    Each piece of information gets stored with a label so we can find it later.
    """
    documents = []
    metadatas = []
    ids = []

    for i, data in enumerate(data_list):
        # Handle both website data and news data
        if isinstance(data, dict):
            if "content" in data:
                # This is website data
                text = data["content"]
                source = data.get("source", "unknown")
            else:
                # This is news data
                text = f"{data.get('title', '')} {data.get('description', '')}"
                source = data.get('published', 'news')
        else:
            text = str(data)
            source = "unknown"

        if text.strip():  # Only store non-empty content
            documents.append(text)
            metadatas.append({
                "company": company_name,
                "source": source
            })
            ids.append(f"{company_name}_{i}_{len(documents)}")

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully stored {len(documents)} pieces of intelligence about {company_name}")

def retrieve_relevant_data(query, company_name, n_results=5):
    """
    Searches the memory bank for information relevant to a query.
    Think of this as asking the filing cabinet 'find everything related to X'.
    ChromaDB searches by MEANING not just keywords - so asking about
    'new products' will also find documents mentioning 'launched features'.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"company": company_name}
        )
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []

def clear_company_data(company_name):
    """
    Clears old data for a company before storing fresh data.
    Think of this as throwing away last week's spy report before filing this week's.
    """
    try:
        existing = collection.get(where={"company": company_name})
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
            print(f"Cleared old data for {company_name}")
    except Exception as e:
        print(f"Clear error: {e}")

# Test it
if __name__ == "__main__":
    print("Testing memory system...")
    
    # Store some test data
    test_data = [
        {"content": "Microsoft launched a new AI assistant called Copilot integrated into Office 365", "source": "test"},
        {"content": "Microsoft stock dropped 5% after earnings report disappointed investors", "source": "test"},
        {"content": "Microsoft acquired a new gaming studio for 2 billion dollars", "source": "test"}
    ]
    
    store_data(test_data, "Microsoft")
    
    # Now retrieve relevant data using a meaning-based search
    print("\nSearching memory for 'AI products'...")
    results = retrieve_relevant_data("AI products", "Microsoft")
    for r in results:
        print(f"Found: {r[:150]}...")
