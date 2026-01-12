"""Web Browser Tool for web navigation and interaction"""
from typing import Dict, List, Optional
import httpx
from urllib.parse import urljoin, urlparse
import re


class Browser:
    """Basic web browser tool for navigation and content extraction"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the Browser
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)
        self.current_url: Optional[str] = None
        self.page_content: Optional[str] = None
    
    async def goto(self, url: str) -> Dict[str, any]:
        """
        Navigate to a URL
        
        Args:
            url: URL to navigate to
            
        Returns:
            Dict with page content and metadata
        """
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            self.current_url = str(response.url)
            self.page_content = response.text
            
            return {
                "status": "success",
                "url": self.current_url,
                "title": self._extract_title(response.text),
                "content": response.text[:5000],  # Limit content
                "status_code": response.status_code,
                "headers": dict(response.headers)
            }
        except httpx.HTTPError as e:
            return {
                "status": "error",
                "url": url,
                "error": str(e),
                "content": ""
            }
    
    async def extract_links(self) -> List[Dict[str, str]]:
        """
        Extract all links from current page
        
        Returns:
            List of dictionaries with 'text' and 'url' keys
        """
        if not self.page_content:
            return []
        
        links = []
        # Pattern to match <a> tags with href attributes
        pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        matches = re.findall(pattern, self.page_content, re.IGNORECASE | re.DOTALL)
        
        for url, text_html in matches:
            # Extract text from link
            text = self._strip_html(text_html).strip()
            if not text:
                text = url  # Use URL as text if no text found
            
            # Convert relative URLs to absolute
            if self.current_url:
                absolute_url = urljoin(self.current_url, url)
            else:
                absolute_url = url
            
            links.append({
                "text": text[:200],  # Limit text length
                "url": absolute_url
            })
        
        return links
    
    async def extract_text(self, selector: Optional[str] = None) -> str:
        """
        Extract text from current page
        
        Args:
            selector: CSS selector (basic support for common tags)
            
        Returns:
            Extracted text
        """
        if not self.page_content:
            return ""
        
        if selector:
            # Basic selector support (simplified)
            # For full CSS selector support, would need BeautifulSoup or similar
            if selector.startswith('#'):
                # ID selector
                pattern = f'id="{selector[1:]}"'
                # Simple extraction - in production, use proper HTML parser
                return self._simple_extract(pattern)
            elif selector.startswith('.'):
                # Class selector
                pattern = f'class="{selector[1:]}"'
                return self._simple_extract(pattern)
            else:
                # Tag selector
                return self._extract_tag(selector)
        else:
            # Extract all text (remove HTML tags)
            return self._strip_html(self.page_content)
    
    def _extract_title(self, html: str) -> str:
        """Extract page title from HTML"""
        match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return self._strip_html(match.group(1)).strip()
        return ""
    
    def _strip_html(self, html: str) -> str:
        """Remove HTML tags from text"""
        # Simple HTML tag removal
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_tag(self, tag: str) -> str:
        """Extract content from specific HTML tag"""
        pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
        matches = re.findall(pattern, self.page_content, re.IGNORECASE | re.DOTALL)
        return '\n'.join([self._strip_html(match) for match in matches])
    
    def _simple_extract(self, pattern: str) -> str:
        """Simple pattern-based extraction"""
        # This is a simplified version - in production, use BeautifulSoup
        return self._strip_html(self.page_content)
    
    async def search(self, query: str, search_engine: str = "duckduckgo") -> List[Dict[str, any]]:
        """
        Search the web (basic implementation using DuckDuckGo)
        
        Args:
            query: Search query
            search_engine: Search engine to use (default: duckduckgo)
            
        Returns:
            List of search results
        """
        # Use DuckDuckGo HTML search (no API key needed)
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        
        try:
            response = await self.client.get(search_url)
            response.raise_for_status()
            
            # Parse search results (simplified)
            results = self._parse_search_results(response.text)
            return results
        except Exception as e:
            return [{
                "title": "Error",
                "url": "",
                "snippet": f"Search failed: {str(e)}"
            }]
    
    def _parse_search_results(self, html: str) -> List[Dict[str, any]]:
        """Parse search results from HTML (simplified)"""
        results = []
        
        # Simple regex-based parsing (in production, use BeautifulSoup)
        # DuckDuckGo result pattern
        pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        
        for url, title_html in matches[:10]:  # Limit to 10 results
            title = self._strip_html(title_html)
            if title and url:
                results.append({
                    "title": title[:200],
                    "url": url,
                    "snippet": ""  # Would need more parsing for snippets
                })
        
        return results
    
    async def close(self):
        """Close the browser client"""
        await self.client.aclose()
    
    def get_current_url(self) -> Optional[str]:
        """Get current URL"""
        return self.current_url
    
    def get_page_content(self) -> Optional[str]:
        """Get current page content"""
        return self.page_content

