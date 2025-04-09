# Music Search Tool

This project provides a powerful and efficient **Music Search Tool** that helps users find `.mp3` files based on search queries. Leveraging the **Codern** library for performing searches and **BeautifulSoup** for web scraping, this tool extracts `.mp3` links and metadata from websites.

## Features
- Search for `.mp3` files by song name or artist.
- Scrape web pages to fetch `.mp3` links and corresponding titles.
- Easy-to-use API for developers.

## Installation
You can install the package using pip:

```bash
pip install music_search
```

```pyton
from music_search import search

# Perform a music search
result = search("دانلود آهنگ بهزاد جباری آواره")
print(result)
```