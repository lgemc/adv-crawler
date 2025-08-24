"""
URL utilities for the crawler
"""

from urllib.parse import urlparse, urljoin, urlunparse
from typing import Optional


class URLUtils:
    """Utility functions for URL handling"""
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize a URL for consistent comparison"""
        parsed = urlparse(url.lower())
        
        # Remove default ports
        netloc = parsed.netloc
        if parsed.port == 80 and parsed.scheme == 'http':
            netloc = parsed.hostname
        elif parsed.port == 443 and parsed.scheme == 'https':
            netloc = parsed.hostname
        
        # Remove trailing slash from path
        path = parsed.path.rstrip('/')
        if not path:
            path = '/'
        
        # Remove fragment
        normalized = urlunparse((
            parsed.scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        return normalized
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if a URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def is_same_domain(url: str, domain: str) -> bool:
        """Check if a URL belongs to the same domain"""
        try:
            parsed = urlparse(url)
            url_domain = parsed.netloc.lower()
            domain = domain.lower()
            
            # Remove www. prefix for comparison
            url_domain = url_domain.replace('www.', '')
            domain = domain.replace('www.', '')
            
            return url_domain == domain or url_domain.endswith(f'.{domain}')
        except:
            return False
    
    @staticmethod
    def get_domain(url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return None
    
    @staticmethod
    def make_absolute(base_url: str, relative_url: str) -> str:
        """Convert a relative URL to absolute"""
        return urljoin(base_url, relative_url)
    
    @staticmethod
    def is_crawlable(url: str) -> bool:
        """Check if URL should be crawled (exclude certain file types)"""
        # File extensions to skip
        skip_extensions = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.tar', '.gz', '.7z',
            '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
            '.exe', '.dmg', '.pkg', '.deb', '.rpm'
        }
        
        parsed = urlparse(url.lower())
        path = parsed.path
        
        for ext in skip_extensions:
            if path.endswith(ext):
                return False
        
        return True