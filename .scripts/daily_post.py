import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

POSTS_DIR = "_posts"
TODAY = datetime.now().strftime("%Y-%m-%d")

def scrape_virgool_content():
    # ... (scraping code from above) ...

def create_jekyll_post():
    filename = f"{POSTS_DIR}/{TODAY}-auto-post.html"
    scraped_html = scrape_virgool_content()
    
    content = f"""---
layout: post
title: "Daily Post {TODAY}"
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")}
categories: [daily]
---

{scraped_html}
"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    create_jekyll_post()
