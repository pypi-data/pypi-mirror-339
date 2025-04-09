"""Web scraping module for LlamaDoc2PDF."""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

# Optional dependencies with proper error handling
try:
    import aiohttp

    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    from bs4 import BeautifulSoup

    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    from shot_scraper import ShotScraper

    SHOT_SCRAPER_AVAILABLE = True
except ImportError:
    SHOT_SCRAPER_AVAILABLE = False

try:
    import datakund as dk

    DATAKUND_AVAILABLE = True
except ImportError:
    DATAKUND_AVAILABLE = False


# --- Dummy Placeholder for missing import ---
class CommandEngine:
    """Dummy CommandEngine."""

    pass


LLM_CMD_AVAILABLE = True  # Assume available if we define dummy
# --- End Dummy Placeholder ---

logger = logging.getLogger("llamadoc2pdf.scraper")


class WebScraper:
    """Basic web scraper."""

    def __init__(self):
        """Initialize the scraper."""
        self.session = None
        self.graph = nx.DiGraph() if NETWORKX_AVAILABLE else None

    async def initialize(self):
        """Initialize the scraper."""
        if AIOHTTP_AVAILABLE and not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close the scraper."""
        if self.session:
            await self.session.close()
            self.session = None

    async def scrape(self, url: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Scrape a URL.

        Args:
            url: The URL to scrape
            options: Optional scraping options

        Returns:
            Scraped content
        """
        options = options or {}

        await self.initialize()

        if not self.session:
            raise RuntimeError("Failed to initialize scraper session (aiohttp may be missing)")

        try:
            async with self.session.get(url) as response:
                html = await response.text()

                # Parse with BeautifulSoup if available
                if BS4_AVAILABLE:
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.text if soup.title else ""
                    links = [a["href"] for a in soup.find_all("a", href=True)]
                else:
                    title = ""
                    links = []

                # Update graph if available
                if NETWORKX_AVAILABLE and self.graph is not None:
                    parsed_url = urlparse(url)
                    self.graph.add_node(url, domain=parsed_url.netloc)

                    for link in links:
                        self.graph.add_edge(url, link)

                return {"url": url, "html": html, "title": title, "links": links}
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {"url": url, "error": str(e)}


class EnhancedScraper(WebScraper):
    """Enhanced scraper with additional capabilities."""

    def __init__(self):
        """Initialize the enhanced scraper."""
        super().__init__()

        # Initialize optional components
        self.shot_scraper = ShotScraper() if SHOT_SCRAPER_AVAILABLE else None
        self.datakund = dk.DataKund() if DATAKUND_AVAILABLE else None
        self.cmd_engine = CommandEngine() if LLM_CMD_AVAILABLE else None

    async def capture_screenshot(self, url: str, output_path: str = None) -> Optional[str]:
        """
        Capture a screenshot of a URL.

        Args:
            url: The URL to capture
            output_path: Optional output path

        Returns:
            Path to the screenshot or None if failed
        """
        if not self.shot_scraper:
            logger.warning("shot-scraper not available, cannot capture screenshot")
            return None

        if not output_path:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace(".", "_")
            output_path = f"screenshots/{domain}.png"

        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            self.shot_scraper.take_shot(url, output_path)
            return output_path
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
