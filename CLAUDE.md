# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the crawler
```bash
# Basic crawl
python cmd/main.py crawl https://example.com

# With options
python cmd/main.py crawl https://example.com --depth 5 --max-pages 200 --delay 2.0
```

### Installation and setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for crawling)
playwright install chromium

# Install package in development mode
pip install -e .
```

### Testing
```bash
# Run tests (when implemented)
python -m pytest tests/
```

## Architecture

This is a web crawler built with Crawlee and Playwright that downloads websites and saves them as markdown files.

### Core Components

**CrawlerPipeline** (`crawler/core/pipeline.py`): Orchestrates the crawling process, handling async execution and lifecycle management.

**WebCrawler** (`crawler/core/crawler.py`): Main crawler implementation using Crawlee's PlaywrightCrawler. Manages URL discovery, depth tracking, and page processing.

**MarkdownWriter** (`crawler/storage/writer.py`): Handles conversion of HTML to markdown and file storage, organizing content to match website hierarchy.

### Key Design Patterns

- **Async Architecture**: Built on asyncio with Crawlee's async crawler framework
- **Pipeline Pattern**: CrawlerPipeline coordinates the crawling workflow with pre/post-crawl hooks
- **Storage Strategy**: Saves pages as markdown files in a directory structure matching the website's URL hierarchy under `sites/domain.com/`

### Configuration Flow

1. CLI arguments parsed in `cmd/main.py`
2. Config dictionary passed to CrawlerPipeline
3. WebCrawler initialized with config (max_depth, max_pages, delay, etc.)
4. Crawler uses PlaywrightCrawler for browser automation

### Important Implementation Notes

- Uses Playwright for JavaScript rendering
- Respects crawl depth and page limits
- Implements polite crawling with configurable delays
- Tracks visited URLs to avoid duplicates
- Can optionally follow external links and download assets