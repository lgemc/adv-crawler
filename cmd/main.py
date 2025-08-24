#!/usr/bin/env python3
"""
Web Crawler CLI - Main entry point
"""

import argparse
import sys
import logging
from pathlib import Path

# Add parent directory to path to import crawler module
sys.path.insert(0, str(Path(__file__).parent.parent))

from crawler.core.crawler import WebCrawler
from crawler.core.pipeline import CrawlerPipeline
from crawler.utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(description='Web Crawler Tool')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Start crawling a website')
    crawl_parser.add_argument('url', help='The starting URL to crawl')
    crawl_parser.add_argument('--depth', type=int, default=3, help='Maximum crawl depth (default: 3)')
    crawl_parser.add_argument('--max-pages', type=int, default=100, help='Maximum number of pages to crawl (default: 100)')
    crawl_parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    crawl_parser.add_argument('--output-dir', default='sites', help='Output directory for crawled content (default: sites)')
    crawl_parser.add_argument('--user-agent', help='Custom User-Agent string')
    crawl_parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    crawl_parser.add_argument('--follow-external', action='store_true', help='Follow external links')
    crawl_parser.add_argument('--include-assets', action='store_true', help='Download CSS, JS, and image files')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'crawl':
        # Setup logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logger = setup_logger(log_level)
        
        # Configure crawler
        config = {
            'start_url': args.url,
            'max_depth': args.depth,
            'max_pages': args.max_pages,
            'delay': args.delay,
            'output_dir': args.output_dir,
            'user_agent': args.user_agent,
            'follow_external': args.follow_external,
            'include_assets': args.include_assets
        }
        
        try:
            # Initialize and run the crawler pipeline
            logger.info(f"Starting crawl of {args.url}")
            pipeline = CrawlerPipeline(config)
            pipeline.run()
            logger.info("Crawling completed successfully")
            
        except KeyboardInterrupt:
            logger.info("Crawling interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Crawling failed: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()