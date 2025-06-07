import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# Configuration
BASE_URL = "https://virgool.io"
TOPIC_URL = "https://virgool.io/topic/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3%DB%8C"
POSTS_DIR = "_posts"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_top_post_url():
    """Get URL of the newest top post from topic page"""
    try:
        response = requests.get(TOPIC_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all post links - UPDATE THIS SELECTOR IF BROKEN
        posts = soup.select('a.post-preview') or soup.select('a[href^="/p/"]')
        if not posts:
            raise Exception("No posts found on page")
            
        # Get the first (newest) post
        post_link = posts[0]
        return urljoin(BASE_URL, post_link['href']), post_link.find('h3').get_text(strip=True)
        
    except Exception as e:
        print(f"Error finding top post: {e}")
        return None, None

def get_post_content(post_url):
    """Get full HTML content of a post"""
    try:
        response = requests.get(post_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find main content - UPDATE THIS SELECTOR IF BROKEN
        content = soup.find('article') or soup.find('div', class_='post-content')
        return str(content) if content else None
        
    except Exception as e:
        print(f"Error fetching post content: {e}")
        return None

def create_daily_post():
    """Create new post with random filename"""
    post_url, post_title = get_top_post_url()
    
    if not post_url:
        post_title = f"Programming Post {datetime.now().strftime('%Y-%m-%d')}"
        content = "<p>Could not fetch today's post</p>"
    else:
        content = get_post_content(post_url) or "<p>Could not fetch post content</p>"
    
    # Generate random filename with date
    random_num = random.randint(1000, 9999)
    filename = f"{POSTS_DIR}/{datetime.now().strftime('%Y-%m-%d')}-{random_num}.html"
    
    # Create post with front matter
    post_content = f"""---
title: "{post_title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')}
---

{content}
"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post_content)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_daily_post()
