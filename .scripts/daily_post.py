import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# Configuration
VIRGOOL_TOPIC_URL = "https://virgool.io/topic/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3%DB%8C"
POSTS_DIR = "_posts"
TODAY = datetime.now().strftime("%Y-%m-%d")

def get_top_post():
    """Fetches the top post from Virgool programming topic"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get the topic page
        response = requests.get(VIRGOOL_TOPIC_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first post - UPDATED SELECTOR
        post_card = soup.find('div', class_='post-card')
        if not post_card:
            raise Exception("No post cards found")
            
        post_link = post_card.find('a', href=True)
        if not post_link:
            raise Exception("No post links found")
            
        post_url = urljoin(VIRGOOL_TOPIC_URL, post_link['href'])
        post_title = post_link.get_text(strip=True)
        
        # Get the post content - UPDATED SELECTOR
        post_response = requests.get(post_url, headers=headers, timeout=10)
        post_soup = BeautifulSoup(post_response.text, 'html.parser')
        content_div = post_soup.find('article') or post_soup.find('div', class_='content')
        
        return post_title, str(content_div) if content_div else None
        
    except Exception as e:
        print(f"Scraping error: {e}")
        return None, None

def create_post():
    """Creates the daily post file"""
    title, content = get_top_post()
    
    if not title or not content:
        title = f"Programming Post {TODAY}"
        content = f"<p>Failed to fetch content from {VIRGOOL_TOPIC_URL}</p>"
    
    filename = f"{POSTS_DIR}/{TODAY}-programming.html"
    post_content = f"""---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")}
categories: [programming]
---

{content}
"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post_content)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_post()
