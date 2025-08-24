# Web Crawler

A scalable web crawler built with Python and Crawlee that downloads websites page by page and stores them as markdown files.

## Features

- 🕷️ Asynchronous crawling using Crawlee and Playwright
- 📝 Saves pages as structured markdown files
- 🗂️ Organizes content in directory structure matching website hierarchy
- 🔗 Tracks internal and external links
- 📊 Configurable crawl depth and page limits
- ⏱️ Polite crawling with configurable delays
- 📦 Optional asset tracking (CSS, JS, images)

## Project Structure

```
adv-crawler/
├── cmd/
│   └── main.py              # CLI entry point
├── crawler/
│   ├── core/
│   │   ├── crawler.py       # Main crawler implementation
│   │   └── pipeline.py      # Pipeline orchestrator
│   ├── storage/
│   │   └── writer.py        # Markdown file writer
│   └── utils/
│       ├── url_utils.py     # URL utilities
│       └── logger.py        # Logging configuration
├── config/
│   └── default_config.yaml  # Default configuration
├── sites/                   # Output directory (created on first run)
├── requirements.txt         # Python dependencies
└── setup.py                # Package setup
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd adv-crawler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. (Optional) Install package in development mode:
```bash
pip install -e .
```

## Usage

### Basic crawling:
```bash
python cmd/main.py crawl https://example.com
```

### With options:
```bash
python cmd/main.py crawl https://example.com \
    --depth 5 \
    --max-pages 200 \
    --delay 2.0 \
    --output-dir custom_output \
    --verbose
```

### Available options:
- `--depth`: Maximum crawl depth (default: 3)
- `--max-pages`: Maximum number of pages to crawl (default: 100)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--output-dir`: Output directory for crawled content (default: sites)
- `--user-agent`: Custom User-Agent string
- `--verbose`: Enable verbose logging
- `--follow-external`: Follow external links
- `--include-assets`: Download and track CSS, JS, and image files

## Output Structure

Crawled content is saved in the following structure:
```
sites/
└── example.com/
    ├── metadata.json        # Crawl metadata
    ├── index.md            # Homepage
    ├── about.md            # /about page
    ├── products/
    │   ├── index.md        # /products page
    │   └── item1.md        # /products/item1 page
    └── blog/
        ├── post1.md        # /blog/post1 page
        └── post2.md        # /blog/post2 page
```

Each markdown file contains:
- Page title
- Original URL
- Crawl timestamp
- Page content (converted from HTML)
- List of discovered links
- Optional: Asset references (CSS, JS, images)

## Configuration

You can customize the crawler behavior by modifying `config/default_config.yaml` or passing command-line arguments.

## Development

### Running tests:
```bash
python -m pytest tests/
```

### Adding new features:
1. Extend the `WebCrawler` class in `crawler/core/crawler.py`
2. Add new storage formats in `crawler/storage/`
3. Add new utilities in `crawler/utils/`

## Requirements

- Python 3.8+
- Crawlee with Playwright support
- html2text for markdown conversion

## License

MIT License