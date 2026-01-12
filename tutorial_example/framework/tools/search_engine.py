# """Search Engine Tool for web search and information retrieval"""


"""Multi-Provider Search Engine with Reliable Free Options"""
from typing import List, Dict, Optional, Union, Literal, overload
import httpx
import re
import asyncio
import random
import json
from urllib.parse import quote_plus, urlencode
from concurrent import futures

# Try to import ddgs library (duckduckgo_search was renamed to ddgs)
try:
    try:
        from ddgs import DDGS
        DDG_AVAILABLE = True
    except ImportError:
        # Fallback to old package name
        from duckduckgo_search import DDGS
        DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False
    DDGS = None
    # Note: Install with: pip install ddgs (or pip install duckduckgo-search for old version)


class SearchEngine:
    """Search engine with multiple free providers for reliability"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, timeout: int = 30, preferred_provider: str = "auto", proxy: Optional[str] = None):
        """
        Initialize Search Engine
        
        Args:
            timeout: Request timeout in seconds
            preferred_provider: "auto", "ddg", "searxng", "brave", "qwant"
            proxy: Optional proxy for requests
        """
        self.timeout = timeout
        self.preferred_provider = preferred_provider
        self.proxy = proxy
        # httpx uses 'proxy' parameter, not 'proxies'
        client_kwargs = {"timeout": timeout, "follow_redirects": True}
        if proxy:
            client_kwargs["proxy"] = proxy
        self.client = httpx.AsyncClient(**client_kwargs)
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.executor: Optional[futures.Executor] = None
        
        # Public SearXNG instances (fallback)
        self.searxng_instances = [
            "https://searx.be",
            "https://searx.work",
            "https://search.sapti.me",
            "https://searx.tiekoetter.com",
        ]
        
        # DuckDuckGo will be initialized lazily (like MetaGPT)
    
    @overload
    async def run(
        self,
        query: str,
        max_results: int = 8,
        as_string: Literal[True] = True,
    ) -> str:
        ...
    
    @overload
    async def run(
        self,
        query: str,
        max_results: int = 8,
        as_string: Literal[False] = False,
    ) -> List[Dict[str, str]]:
        ...
    
    async def run(
        self,
        query: str,
        max_results: int = 8,
        as_string: bool = True,
    ) -> Union[str, List[Dict[str, str]]]:
        """
        Run a search query (MetaGPT-compatible interface)
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            as_string: If True, return JSON string; if False, return list of dicts
            
        Returns:
            Search results as string or list of dictionaries
        """
        results = await self.search(query, num_results=max_results)
        
        if as_string:
            return json.dumps(results, ensure_ascii=False, indent=2)
        return results
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, any]]:
        """
        Search the web using multiple providers with automatic fallback
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, snippet
        """
        if not query or not query.strip():
            return []
        
        providers = self._get_provider_order()
        
        for provider in providers:
            try:
                results = await self._search_with_provider(provider, query, num_results)
                # Validate results - must have valid URLs and titles
                validated_results = self._validate_results(results)
                if validated_results and len(validated_results) > 0:
                    return validated_results[:num_results]
                await asyncio.sleep(0.3)  # Brief pause before trying next provider
            except Exception as e:
                # Log error for debugging but continue to next provider
                # Only log if it's not a common expected error
                if "API key" not in str(e) and "not found" not in str(e).lower():
                    pass  # Silent fail for common issues
                continue
        
        # If all providers failed, return empty list
        # Note: For best results, install: pip install duckduckgo-search
        return []
    
    def _get_provider_order(self) -> List[str]:
        """Get order of providers to try"""
        if self.preferred_provider != "auto":
            providers = [self.preferred_provider]
            other_providers = ["ddg", "searxng", "brave", "qwant"]
            providers.extend([p for p in other_providers if p != self.preferred_provider])
            return providers
        
        # Auto mode: try DuckDuckGo library first (most reliable), then fallbacks
        if DDG_AVAILABLE:
            return ["ddg", "searxng", "qwant", "brave"]
        else:
            return ["searxng", "qwant", "brave", "ddg_lite"]
    
    async def _search_with_provider(self, provider: str, query: str, num_results: int) -> List[Dict[str, any]]:
        """Search with specific provider"""
        if provider == "ddg":
            return await self._search_duckduckgo(query, num_results)
        elif provider == "searxng":
            return await self._search_searxng(query, num_results)
        elif provider == "brave":
            return await self._search_brave(query, num_results)
        elif provider == "qwant":
            return await self._search_qwant(query, num_results)
        elif provider == "ddg_lite":
            return await self._search_duckduckgo_lite(query, num_results)
        return []
    
    @property
    def ddgs(self):
        """Get DuckDuckGo search instance (lazy initialization like MetaGPT)"""
        if not DDG_AVAILABLE:
            return None
        # Use proxy parameter (singular) for httpx compatibility
        if self.proxy:
            return DDGS(proxies=self.proxy)
        return DDGS()
    
    async def _search_duckduckgo(self, query: str, num_results: int) -> List[Dict[str, any]]:
        """
        Search using DuckDuckGo library (like MetaGPT)
        Most reliable method - uses official duckduckgo_search package
        """
        if not DDG_AVAILABLE:
            return []
        
        try:
            loop = self.loop or asyncio.get_event_loop()
            future = loop.run_in_executor(
                self.executor,
                self._search_from_ddgs,
                query,
                num_results,
            )
            search_results = await future
            return search_results
        except Exception:
            return []
    
    def _search_from_ddgs(self, query: str, max_results: int) -> List[Dict[str, any]]:
        """
        Synchronous search using DuckDuckGo library
        Called from executor to avoid blocking (like MetaGPT)
        """

        try:
            ddgs_instance = self.ddgs
            if not ddgs_instance:
                return []
            
            results = []
            # Try to search with English region/language
            # The ddgs package supports region parameter to get English results
            try:
                # Try with region parameter (new ddgs package format)
                search_iter = ddgs_instance.text(query, region='us-en', safesearch='moderate', max_results=max_results)
            except TypeError:
                # Fallback: old package or region not supported, try without region
                try:
                    search_iter = ddgs_instance.text(query, max_results=max_results)
                except TypeError:
                    # Very old package, no max_results parameter
                    search_iter = ddgs_instance.text(query)
            
            # Use zip pattern like MetaGPT for safety
            for i, item in zip(range(max_results), search_iter):
                # DuckDuckGo returns: title, href, body
                title = item.get("title", "").strip()
                url = item.get("href", "").strip()
                snippet = item.get("body", "").strip()
                
                # Validate result
                if not url or not url.startswith(('http://', 'https://')):
                    continue
                if not title or len(title) < 3:
                    continue
                
                results.append({
                    "title": title[:200],
                    "url": url,
                    "snippet": snippet[:300]
                })
            
            return results
        except Exception:
            return []
    
    async def _search_searxng(self, query: str, num_results: int) -> List[Dict[str, any]]:
        """
        Search using SearXNG (Most Reliable)
        SearXNG is a metasearch engine that aggregates results from multiple sources
        """
        # Shuffle instances for load balancing
        instances = self.searxng_instances.copy()
        random.shuffle(instances)
        
        for instance in instances:
            try:
                search_url = f"{instance}/search"
                params = {
                    "q": query,
                    "format": "json",
                    "language": "en"
                }
                
                headers = {
                    "User-Agent": random.choice(self.USER_AGENTS),
                    "Accept": "application/json",
                }
                
                response = await self.client.get(
                    search_url, 
                    params=params, 
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results = []
                        
                        # SearXNG returns results in "results" key
                        search_results = data.get("results", [])
                        if not search_results:
                            continue
                        
                        for item in search_results[:num_results * 2]:  # Get extra for validation
                            title = item.get("title", "").strip()
                            url = item.get("url", "").strip()
                            
                            # Validate result
                            if not url or not url.startswith(('http://', 'https://')):
                                continue
                            if not title or len(title) < 3:
                                continue
                            
                            results.append({
                                "title": title[:200],
                                "url": url,
                                "snippet": item.get("content", item.get("snippet", "")).strip()[:300]
                            })
                        
                        if results:
                            return results
                    except (json.JSONDecodeError, KeyError, TypeError):
                        continue
                        
            except (httpx.TimeoutException, httpx.RequestError):
                continue
            except Exception:
                continue
        
        return []
    
    async def _search_brave(self, query: str, num_results: int) -> List[Dict[str, any]]:
        """
        Search using Brave Search API (Free tier: 2000 queries/month)
        More reliable than scraping, requires API key but has generous free tier
        
        To use: Set BRAVE_API_KEY environment variable
        Get free API key at: https://brave.com/search/api/
        """
        import os
        api_key = os.environ.get("BRAVE_API_KEY")
        
        if not api_key:
            # Silent skip - no need to print
            return []
        
        try:
            search_url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": api_key
            }
            params = {
                "q": query,
                "count": num_results
            }
            
            response = await self.client.get(search_url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("web", {}).get("results", [])[:num_results]:
                    results.append({
                        "title": item.get("title", "")[:200],
                        "url": item.get("url", ""),
                        "snippet": item.get("description", "")[:300]
                    })
                
                return results
                
        except Exception:
            # Silent fail
            pass
        
        return []
    
    async def _search_qwant(self, query: str, num_results: int) -> List[Dict[str, any]]:
        """
        Search using Qwant (European search engine, no API key needed)
        More reliable than DuckDuckGo scraping
        """
        try:
            search_url = "https://api.qwant.com/v3/search/web"
            params = {
                "q": query,
                "count": min(num_results * 2, 20),  # Get extra for validation
                "locale": "en_US",
                "offset": 0,
                "device": "desktop"
            }
            
            headers = {
                "User-Agent": random.choice(self.USER_AGENTS),
                "Accept": "application/json",
            }
            
            response = await self.client.get(search_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    results = []
                    
                    # Qwant structure: data.result.items
                    result_data = data.get("data", {})
                    if not result_data:
                        return []
                    
                    result_obj = result_data.get("result", {})
                    if not result_obj:
                        return []
                    
                    items = result_obj.get("items", [])
                    if not items:
                        return []
                    
                    for item in items:
                        title = item.get("title", "").strip()
                        url = item.get("url", "").strip()
                        
                        # Validate result
                        if not url or not url.startswith(('http://', 'https://')):
                            continue
                        if not title or len(title) < 3:
                            continue
                        
                        results.append({
                            "title": title[:200],
                            "url": url,
                            "snippet": item.get("desc", item.get("description", "")).strip()[:300]
                        })
                        
                        if len(results) >= num_results:
                            break
                    
                    if results:
                        return results
                except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                    pass
                    
        except (httpx.TimeoutException, httpx.RequestError):
            pass
        except Exception:
            pass
        
        return []
    
    async def _search_duckduckgo_lite(self, query: str, num_results: int) -> List[Dict[str, any]]:
        """Search using DuckDuckGo Lite (fallback option)"""
        search_url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
        
        headers = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html",
        }
        
        try:
            response = await self.client.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Check if we got valid HTML
                if len(html) < 1000:
                    return []
                
                results = []
                
                # Multiple patterns for DuckDuckGo Lite
                patterns = [
                    r'<tr>.*?<td[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*class="result-link"[^>]*>(.*?)</a>',
                    r'<a[^>]*href="(https?://[^"]+)"[^>]*class="result-link"[^>]*>(.*?)</a>',
                    r'<a[^>]*class="result-link"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
                    
                    for match in matches:
                        if isinstance(match, tuple):
                            url = match[0].strip()
                            title_html = match[1] if len(match) > 1 else ""
                        else:
                            url = match.strip()
                            title_html = ""
                        
                        # Validate URL
                        if not url or not url.startswith(('http://', 'https://')):
                            continue
                        if 'duckduckgo.com' in url.lower():
                            continue
                        if any(skip in url.lower() for skip in ['javascript:', 'mailto:', '#', 'about:']):
                            continue
                        
                        # Extract and validate title
                        title = self._strip_html(title_html).strip() if title_html else ""
                        if not title or len(title) < 3:
                            # Try to extract from URL
                            title = url.split('/')[-1].replace('-', ' ').replace('_', ' ').replace('.html', '').strip()
                            if not title or len(title) < 3:
                                continue
                        
                        # Skip duplicates
                        if any(r['url'] == url for r in results):
                            continue
                        
                        results.append({
                            "title": title[:200],
                            "url": url,
                            "snippet": ""
                        })
                        
                        if len(results) >= num_results:
                            break
                    
                    if results:
                        break
                
                return results
                
        except (httpx.TimeoutException, httpx.RequestError):
            pass
        except Exception:
            pass
        
        return []
    
    def _validate_results(self, results: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Validate and filter search results"""
        if not results:
            return []
        
        validated = []
        seen_urls = set()
        
        for result in results:
            # Skip error messages
            if result.get('title') in ['Search Failed', 'Search Error']:
                continue
            
            url = result.get('url', '').strip()
            title = result.get('title', '').strip()
            
            # Must have valid URL
            if not url or not url.startswith(('http://', 'https://')):
                continue
            
            # Must have valid title
            if not title or len(title) < 3:
                continue
            
            # Skip duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Skip invalid domains
            skip_domains = ['duckduckgo.com', 'javascript:', 'mailto:', '#', 'about:', 'data:']
            if any(skip in url.lower() for skip in skip_domains):
                continue
            
            validated.append({
                "title": title[:200],
                "url": url,
                "snippet": result.get('snippet', '').strip()[:300]
            })
        
        return validated
    
    def _strip_html(self, html: str) -> str:
        """Remove HTML tags and clean text"""
        if not html:
            return ""
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        return text.strip()
    
    async def search_and_summarize(self, query: str, max_results: int = 5) -> str:
        """Search and provide a summary of results"""
        results = await self.search(query, num_results=max_results)
        
        # Validate results - must have at least one valid result
        if not results:
            return f"No results found for query: {query}"
        
        # Filter out any invalid results
        valid_results = [r for r in results if r.get('url') and r.get('title')]
        if not valid_results:
            return f"No results found for query: {query}"
        
        summary = f"Search Results for '{query}':\n\n"
        for i, result in enumerate(valid_results, 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   URL: {result['url']}\n"
            if result.get('snippet'):
                summary += f"   {result['snippet'][:200]}\n"
            summary += "\n"
        
        return summary
    
    async def close(self):
        """Close the search engine client"""
        await self.client.aclose()


# Example usage:
"""
# Install duckduckgo_search for best results:
# pip install duckduckgo-search

# Basic usage (auto provider selection - tries DuckDuckGo library first)
engine = SearchEngine()
results = await engine.search("python programming")

# Use MetaGPT-compatible run() method
results = await engine.run("python programming", max_results=5, as_string=False)

# Prefer specific provider
engine = SearchEngine(preferred_provider="ddg")  # Use DuckDuckGo library
results = await engine.search("python programming")

# With Brave API key (most reliable if you have it)
import os
os.environ["BRAVE_API_KEY"] = "your_api_key_here"
engine = SearchEngine(preferred_provider="brave")
results = await engine.search("python programming")
"""