import requests
from bs4 import BeautifulSoup
from logging import basicConfig, info, INFO, warning, error

# Configure logging
basicConfig(level=INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_fun_facts(url):
    """Fetches fun facts from a website and returns them as a list."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        error(f"Error fetching the webpage: {e}")
        return []

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract facts (Modify the selector based on the website structure)
    facts = []
    for fact in soup.select("li"):  # Adjust the selector for the right HTML element
        text = fact.get_text(strip=True)
        if text and len(text) > 10:  # Ensure meaningful facts
            facts.append(text)

    info(f"Extracted {len(facts)} fun facts.")
    return facts


def chunk_facts(facts, chunk_size=5):
    """Splits the facts into smaller chunks."""
    return [facts[i:i + chunk_size] for i in range(0, len(facts), chunk_size)]


if __name__ == "__main__":
    # Example website with fun facts (change if needed)
    url = "https://kids.niehs.nih.gov/games/riddles/jokes/fun-facts-and-trivia"

    facts = fetch_fun_facts(url)

    if facts:
        chunked_facts = chunk_facts(facts, chunk_size=5)
        for i, chunk in enumerate(chunked_facts, 1):
            print(f"\nChunk {i}: {chunk}")
    else:
        warning("No facts found.")
