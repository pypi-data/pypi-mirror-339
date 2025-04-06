# WebChameleon

![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Version](https://img.shields.io/badge/version-1.3.0-brightgreen)

**WebChameleon** is a powerful tool for web scraping and API reversal, designed for developers, data researchers, and tech professionals. With features like dynamic structure analysis, automatic API detection, and graph-based relation mapping, WebChameleon enables efficient and ethical data extraction from various websites.

## Key Features

- **Dynamic Structure Analysis**: Automatically understands website layouts with semantic analysis using NLTK.
- **Automatic API Detection**: Discovers hidden API endpoints using Playwright simulation and heuristic approaches.
- **Graph-Based Relation Mapping**: Builds relationship graphs between entities with community analysis using the Louvain method.
- **Adaptive Error Handling**: Automatic retry mechanisms, adaptive rate limiting, and recovery strategies when blocked.
- **Flexible Storage**: Saves data in JSON, CSV, or SQLite formats with compression options.
- **Disguise and Authentication**: Supports multiple disguise modes (browser, bot, API client) and authentication via headers/cookies.

#### Prerequisites
- **Python 3.7+**: Ensure Python is installed. [Download it here](https://www.python.org/downloads/).
- **pip**: Installed by default with Python.
- **Git**: Optional, used for cloning the repository.

#### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/mrivky67/webchameleon.git
cd webchameleon
```

2. **Create a Virtual Environment (Recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Playwright Browsers**
```bash
playwright install
```

5. **Download NLTK Data**
```python
import nltk
nltk.download('punkt')
```

6. **Verify Installation**
```bash
python examples/reverse_api_example.py
```

#### Troubleshooting
- **Error: "Can not decode content-encoding: brotli"**
  ```bash
  pip install brotli
  ```
- **Error: "Playwright browser not found"**
  Ensure you've run `playwright install`.
- **Error: "NLTK data not found"**
  Run `nltk.download('punkt')` again.

#### Installing as a Package
```bash
pip install -e .
```
You can now import WebChameleon from anywhere:
```python
from webchameleon import WebChameleon
```

---

### Usage Guide

This guide provides examples for website scraping and API reverse-engineering.

#### Scraping a Website

1. **Define the Target**
Choose a website, e.g., `https://scrapethissite.com/pages/simple/`.

2. **Inspect HTML Structure**
Use Chrome DevTools. Example classes:
- `.country-name`
- `.country-capital`
- `.country-population`

3. **Write the Script**
```python
import asyncio
from webchameleon import WebChameleon

async def main():
    chameleon = WebChameleon(
        target="https://scrapethissite.com/pages/simple/",
        disguise_as="default",
        auto_learn=True,
        max_concurrent=5
    )

    structure = await chameleon.analyze_structure()
    print("Structure:", structure)

    data = await chameleon.scrape(
        target_elements={
            "country_name": ".country-name",
            "capital": ".country-capital",
            "population": ".country-population"
        },
        depth=3,
        adaptive_depth=True
    )
    await chameleon.save(data, "countries_data.json", format="json", compress=True)

if __name__ == "__main__":
    asyncio.run(main())
```

4. **Run the Script**
```bash
python examples/scrape_forum.py
```

#### Detecting APIs (Reverse API)

1. **Target a Site with APIs**
Example: `https://reqres.in`

2. **Write the Script**
```python
import asyncio
from webchameleon import WebChameleon

async def main():
    chameleon = WebChameleon(
        target="https://reqres.in",
        disguise_as="python_requests"
    )

    api_data = await chameleon.reverse_api(use_playwright=True, max_depth=4, interactive_mode=True)
    if api_data:
        await chameleon.save(api_data, "reqres_api_data.json", format="json", compress=True)
        print("API Data:", api_data)
    else:
        print("No API detected.")

if __name__ == "__main__":
    asyncio.run(main())
```

3. **Run the Script**
```bash
python examples/reverse_api_example.py
```

#### Mapping Relations
```python
relations = await chameleon.map_relations(data, "relations.graphml", weight_threshold=0.6)
```

#### Key Parameters
- `disguise_as`: e.g., `default`, `googlebot`, `python_requests`
- `max_concurrent`: Controls concurrency.
- `auth_config`: Pass authentication headers.
```python
auth_config={"headers": {"Authorization": "Bearer your_api_key"}}
```
- `use_playwright`: Set to `True` for dynamic sites.

---

### API Reference

#### WebChameleon Class

```python
chameleon = WebChameleon(
    target: str,
    disguise_as: str = "default",
    auto_learn: bool = True,
    max_concurrent: int = 5,
    auth_config: Optional[Dict] = None,
    custom_settings: Optional[Dict] = None
)
```

#### Methods
- `analyze_structure()` → `Optional[Dict]`
- `scrape(target_elements: Dict, depth: int, adaptive_depth: bool)` → `List[Dict]`
- `reverse_api(use_playwright: bool, max_depth: int, interactive_mode: bool)` → `Optional[Dict]`
- `map_relations(data: List[Dict], output_file: str, weight_threshold: float)` → `Optional[Dict]`
- `save(data: List[Dict], filename: str, format: str, compress: bool)`
- `status()` → `Dict`

#### Supporting Classes
- `StructureAnalyzer`
- `ApiReverser`
- `RelationMapper`
- `DisguiseManager`
- `StorageManager`


