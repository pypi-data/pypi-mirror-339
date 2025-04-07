import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
from sentence_transformers import SentenceTransformer, util

#custom imports
from .quick_rag import _model_cache

#fake User-Agent generator
ua = UserAgent()

def get_random_headers():
    """Returns headers with a randomly generated User-Agent."""
    return {"User-Agent": ua.random}

def search_urls(query, num_results=5, region=None):
    """Searches DuckDuckGo for the query and returns top result links/URLs."""
    base_url = "https://html.duckduckgo.com/html/?q=" + query

    # If region is provided, append it as a `kl` parameter
    if region:
        base_url += f"&kl={region}"

    headers = get_random_headers()

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return [f"Error searching DuckDuckGo: {e}"]

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.find_all("a", class_="result__a", limit=num_results):
        url = link["href"]

        # Fix DuckDuckGo redirect URLs
        if "/l/?uddg=" in url:
            url = url.split("/l/?uddg=")[1].split("&")[0]
            url = requests.utils.unquote(url)

        results.append(url)

    return results

def scrape_website(url, paragraphs=5, min_delay=2, max_delay=5,verify_ssl = True):
    """
    scrapes website, fetches text from a URL with rotating User-Agents & random delay.:
    - paragraphs=-1 → All text
    - paragraphs=N → First N paragraphs
    
    Returns:
        Extracted text or error message
    """
    headers = get_random_headers()
    time.sleep(random.uniform(min_delay, max_delay))  # Random delay before request

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=verify_ssl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        if paragraphs == -1:
            return soup.get_text(separator="\n", strip=True)
        
        return "\n".join(
            p.get_text(strip=True) 
            for p in soup.find_all("p")[:paragraphs]
        )

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def get_online_results(query, num_results=5,paragraphs=5, min_delay=2, max_delay=5,verify_ssl= True,region=None):
    """Searches DuckDuckGo and extracts content from top results with configurable scraping.
    
    Args:
        query: Search term to look up.
        num_results: Number of search results to process (default: 5).
        paragraphs: Number of paragraphs to extract per page. 
                   Use -1 to extract all text (default: 5).
        min_delay: Minimum delay between requests in seconds (anti-throttling, default: 2).
        max_delay: Maximum delay between requests in seconds (anti-throttling, default: 5).
        verify_ssl: Whether to verify SSL certificates (default: True).
                   Disable for sites with self-signed certificates.
        region: Country code for region-specific results (e.g., 'us', 'fr', 'jp').
                None for global results (default: None).
    
    Returns:
        Dictionary mapping URLs to extracted content (or error messages if scraping failed).
        Example:
        {
            "https://example.com/page1": "Extracted paragraph text...",
            "https://example.com/page2": "Error scraping https://..."
        }
    
    Raises:
        ValueError: If num_results <= 0 or min_delay > max_delay.
    """
    sources = search_urls(query, num_results,region=region)
    results = {}

    for url in sources:
        results[url] = scrape_website(url, paragraphs=paragraphs, min_delay= min_delay, max_delay=max_delay,verify_ssl=verify_ssl)

    return results

if "all-MiniLM-L6-v2" not in _model_cache:
    _model_cache["all-MiniLM-L6-v2"] = SentenceTransformer("all-MiniLM-L6-v2")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_best_answer(query, answers_dict:dict):
    """
    Given multiple web-sourced answers, ranks them based on semantic similarity to the query.
    
    Args:
        query (str): The original question.
        answers_dict (dict): {source_url: extracted_text}
    
    Returns:
        Tuple: (best_source, best_content)
    """
    if not answers_dict:
        return None, None  # No data, return nothing
    
    query_embedding = embedding_model.encode(query, convert_to_numpy=True)
    best_source, best_content = None, None
    best_score = -1  # Track highest similarity score

    for source, content in answers_dict.items():
        if not content.strip():  # Skip empty responses
            continue
        
        content_embedding = embedding_model.encode(content, convert_to_numpy=True)
        similarity_score = util.pytorch_cos_sim(query_embedding, content_embedding).item()

        if similarity_score > best_score:
            best_score = similarity_score
            best_source = source
            best_content = content

    return best_source, best_content