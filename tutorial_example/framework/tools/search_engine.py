"""Search Engine Tool for web search and information retrieval"""
from typing import List, Dict, Optional
import httpx
import re


class SearchEngine:
    """Search engine tool for web search"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the Search Engine
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, any]]:
        """
        Search the web
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, snippet
        """
        # Use DuckDuckGo HTML search (no API key needed)
        search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        
        try:
            response = await self.client.get(search_url)
            response.raise_for_status()
            
            results = self._parse_search_results(response.text, num_results)
            return results
        except Exception as e:
            return [{
                "title": "Search Error",
                "url": "",
                "snippet": f"Search failed: {str(e)}"
            }]
    
    async def search_and_summarize(self, query: str, max_results: int = 5) -> str:
        """
        Search and provide a summary of results
        
        Args:
            query: Search query
            max_results: Maximum number of results to summarize
            
        Returns:
            Summary of search results
        """
        results = await self.search(query, num_results=max_results)
        
        if not results:
            return f"No results found for query: {query}"
        
        summary = f"Search Results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   URL: {result['url']}\n"
            if result.get('snippet'):
                summary += f"   {result['snippet'][:200]}\n"
            summary += "\n"
        
        return summary
    
    def _parse_search_results(self, html: str, num_results: int) -> List[Dict[str, any]]:
        """Parse search results from HTML"""
        results = []
        
        # DuckDuckGo HTML result patterns
        # Result links
        link_pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
        snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>'
        
        links = re.findall(link_pattern, html, re.IGNORECASE | re.DOTALL)
        snippets = re.findall(snippet_pattern, html, re.IGNORECASE | re.DOTALL)
        
        for i, (url, title_html) in enumerate(links[:num_results]):
            title = self._strip_html(title_html)
            snippet = self._strip_html(snippets[i]) if i < len(snippets) else ""
            
            if title and url:
                results.append({
                    "title": title[:200],
                    "url": url,
                    "snippet": snippet[:300]
                })
        
        return results
    
    def _strip_html(self, html: str) -> str:
        """Remove HTML tags from text"""
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    async def close(self):
        """Close the search engine client"""
        await self.client.aclose()

