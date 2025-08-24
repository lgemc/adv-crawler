"""
Core web crawler implementation using crawlee
"""

import asyncio
from typing import Dict, Set, Optional
from urllib.parse import urljoin, urlparse
import logging

from crawlee import PlaywrightCrawler
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from crawlee.storages import RequestQueue
from playwright.async_api import Page

from ..storage.writer import MarkdownWriter
from ..utils.url_utils import URLUtils


class WebCrawler:
    """Main web crawler class using crawlee and playwright"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.start_url = config['start_url']
        self.max_depth = config.get('max_depth', 3)
        self.max_pages = config.get('max_pages', 100)
        self.delay = config.get('delay', 1.0)
        self.output_dir = config.get('output_dir', 'sites')
        self.follow_external = config.get('follow_external', False)
        self.include_assets = config.get('include_assets', False)
        
        self.visited_urls: Set[str] = set()
        self.page_count = 0
        self.base_domain = urlparse(self.start_url).netloc
        
        self.logger = logging.getLogger(__name__)
        self.writer = MarkdownWriter(self.output_dir, self.base_domain)
        
        # Initialize crawler
        self.crawler = None
        self._setup_crawler()
    
    def _setup_crawler(self):
        """Setup the crawlee playwright crawler"""
        self.crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_pages,
            request_handler=self._handle_request,
            failed_request_handler=self._handle_failed_request,
            max_request_retries=2,
            request_handler_timeout_secs=30,
            browser_pool_options={
                'use_fingerprints': False,
            },
            playwright_launch_options={
                'headless': True,
            },
            use_session_pool=False,
        )
    
    async def _handle_request(self, context: PlaywrightCrawlingContext) -> None:
        """Handle each crawled page"""
        page = context.page
        request = context.request
        url = request.url
        
        # Check if we've reached the maximum number of pages
        if self.page_count >= self.max_pages:
            self.logger.info(f"Reached maximum page limit ({self.max_pages})")
            return
        
        # Mark URL as visited
        self.visited_urls.add(url)
        self.page_count += 1
        
        self.logger.info(f"Crawling [{self.page_count}/{self.max_pages}]: {url}")
        
        # Extract page content
        try:
            # Get page title
            title = await page.title()
            
            # Get page HTML
            html_content = await page.content()
            
            # Extract text content for markdown
            text_content = await self._extract_text_content(page)
            
            # Extract links
            links = await self._extract_links(page, url)
            
            # Extract assets if requested
            assets = []
            if self.include_assets:
                assets = await self._extract_assets(page, url)
            
            # Save page content as markdown
            await self.writer.save_page(
                url=url,
                title=title,
                content=text_content,
                html=html_content,
                links=links,
                assets=assets
            )
            
            # Add delay between requests
            await asyncio.sleep(self.delay)
            
            # Enqueue new URLs
            await self._enqueue_links(context, links, url)
            
        except Exception as e:
            self.logger.error(f"Error processing {url}: {e}")
    
    async def _handle_failed_request(self, context: PlaywrightCrawlingContext, error: Exception) -> None:
        """Handle failed requests"""
        self.logger.error(f"Failed to crawl {context.request.url}: {error}")
    
    async def _extract_text_content(self, page: Page) -> str:
        """Extract readable text content from the page"""
        # Remove script and style elements
        await page.evaluate('''() => {
            const scripts = document.querySelectorAll('script, style');
            scripts.forEach(el => el.remove());
        }''')
        
        # Get text content
        text_content = await page.evaluate('''() => {
            return document.body ? document.body.innerText : '';
        }''')
        
        return text_content
    
    async def _extract_links(self, page: Page, current_url: str) -> list:
        """Extract all links from the page"""
        links = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a[href]'));
            return links.map(link => ({
                href: link.href,
                text: link.textContent.trim()
            }));
        }''')
        
        # Process and filter links
        processed_links = []
        for link in links:
            href = link.get('href', '')
            if href:
                absolute_url = urljoin(current_url, href)
                processed_links.append({
                    'url': absolute_url,
                    'text': link.get('text', ''),
                    'is_external': not URLUtils.is_same_domain(absolute_url, self.base_domain)
                })
        
        return processed_links
    
    async def _extract_assets(self, page: Page, current_url: str) -> list:
        """Extract asset URLs (CSS, JS, images)"""
        assets = await page.evaluate('''() => {
            const results = {
                css: Array.from(document.querySelectorAll('link[rel="stylesheet"]')).map(el => el.href),
                js: Array.from(document.querySelectorAll('script[src]')).map(el => el.src),
                images: Array.from(document.querySelectorAll('img[src]')).map(el => el.src)
            };
            return results;
        }''')
        
        # Convert relative URLs to absolute
        for asset_type in assets:
            assets[asset_type] = [urljoin(current_url, url) for url in assets[asset_type]]
        
        return assets
    
    async def _enqueue_links(self, context: PlaywrightCrawlingContext, links: list, current_url: str) -> None:
        """Add discovered links to the crawl queue"""
        current_depth = context.request.user_data.get('depth', 0)
        
        if current_depth >= self.max_depth:
            return
        
        for link_data in links:
            url = link_data['url']
            is_external = link_data['is_external']
            
            # Skip if already visited
            if url in self.visited_urls:
                continue
            
            # Skip external links if not following them
            if is_external and not self.follow_external:
                continue
            
            # Skip non-HTTP(S) URLs
            if not url.startswith(('http://', 'https://')):
                continue
            
            # Add to queue
            await context.add_requests([{
                'url': url,
                'user_data': {'depth': current_depth + 1}
            }])
    
    async def crawl(self) -> None:
        """Start the crawling process"""
        # Add the starting URL to the queue
        await self.crawler.add_requests([{
            'url': self.start_url,
            'user_data': {'depth': 0}
        }])
        
        # Run the crawler
        await self.crawler.run()
        
        self.logger.info(f"Crawling completed. Visited {self.page_count} pages.")