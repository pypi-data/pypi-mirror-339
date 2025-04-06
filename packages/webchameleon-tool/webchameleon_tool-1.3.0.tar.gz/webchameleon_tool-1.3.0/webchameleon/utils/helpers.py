from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
from typing import Dict, Any


def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def sanitize_data(data: Dict) -> Dict:
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = re.sub(r"[\n\r\t]", " ", value).strip()
        elif isinstance(value, dict):
            sanitized[key] = sanitize_data(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_data(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            sanitized[key] = value
    return sanitized


def extract_features(structure: Dict) -> Dict:
    return {
        "dynamic_content": structure.get("dynamic_elements", {}).get(
            "xhr_detected", False
        ),
        "nav_depth": len(structure.get("navigation", {}).get("main_menu", [])),
        "block_count": len(structure.get("content_blocks", [])),
    }
