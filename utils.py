# utils.py
from duckduckgo_search import DDGS

def search_web(query, num_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results):
            results.append(f"{r['title']}: {r['body']} ({r['href']})")
    return results
