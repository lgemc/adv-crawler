"""
Crawler pipeline orchestrator
"""

import asyncio
import logging
from typing import Dict

from .crawler import WebCrawler


class CrawlerPipeline:
    """Orchestrates the crawling pipeline"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.crawler = WebCrawler(config)
    
    def run(self) -> None:
        """Run the crawler pipeline"""
        try:
            # Run the async crawler
            asyncio.run(self._run_async())
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            raise
    
    async def _run_async(self) -> None:
        """Async pipeline execution"""
        self.logger.info("Starting crawler pipeline...")
        
        # Pre-crawl setup
        await self._pre_crawl()
        
        # Run the crawler
        await self.crawler.crawl()
        
        # Post-crawl cleanup
        await self._post_crawl()
        
        self.logger.info("Pipeline completed successfully")
    
    async def _pre_crawl(self) -> None:
        """Pre-crawl setup and validation"""
        self.logger.debug("Running pre-crawl setup...")
        # Add any pre-crawl validation or setup here
        pass
    
    async def _post_crawl(self) -> None:
        """Post-crawl cleanup and reporting"""
        self.logger.debug("Running post-crawl cleanup...")
        # Add any post-crawl cleanup or reporting here
        pass