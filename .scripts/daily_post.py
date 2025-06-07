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

def debug_log(message):
    """Helper function for debug logging"""
    print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')} - {message}")

def get_top_post_url():
    """Get URL of the newest top post from topic page"""
    try:
        debug_log(f"Fetching topic page: {TOPIC_URL}")
        response = requests.get(TOPIC_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        debug_log("Parsed topic page HTML")
        
        # Find all post links - VIRGOOL SPECIFIC SELECTOR
        posts = soup.select('a.stream-item__title')  # Updated selector
        if not posts:
            debug_log("No posts found with selector 'a.stream-item__title'")
            posts = soup.select('a[href^="/p/"]')  # Fallback selector
            if not posts:
                raise Exception("No posts found with any selector")
        
        post_link = posts[0]
        post_url = urljoin(BASE_URL, post_link['href'])
        post_title = post_link.get_text(strip=True)
        
        debug_log(f"Found post: {post_title}")
        debug_log(f"Post URL: {post_url}")
        
        return post_url, post_title
        
    except Exception as e:
        debug_log(f"Error finding top post: {str(e)}")
        return None, None

def get_post_content(post_url):
    """Get full HTML content of a post"""
    try:
        debug_log(f"Fetching post content from: {post_url}")
        response = requests.get(post_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        debug_log("Parsed post page HTML")
        
        # VIRGOOL CONTENT SELECTOR - UPDATED
        content = soup.find('div', class_='widget-post__content') or soup.find('article')
        
        if content:
            debug_log("Successfully extracted content")
            # Clean unnecessary elements
            for element in content.select('.post-actions, .comments-section'):
                element.decompose()
            return str(content)
        else:
            raise Exception("Content div not found")
            
    except Exception as e:
        debug_log(f"Error fetching post content: {str(e)}")
        return None

def create_daily_post():
    """Main function to create the daily post"""
    debug_log("Starting daily post creation")
    
    # Step 1: Get post URL from topic page
    post_url, post_title = get_top_post_url()
    
    if not post_url:
        post_title = f"Programming Post {datetime.now().strftime('%Y-%m-%d')}"
        content = "<p>Could not fetch today's post URL</p>"
    else:
        # Step 2: Fetch content from the post URL
        content = get_post_content(post_url) or "<p>Could not fetch post content</p>"
    
    # Step 3: Generate filename with random number
    random_num = random.randint(1000, 9999)
    filename = f"{POSTS_DIR}/{datetime.now().strftime('%Y-%m-%d')}-{random_num}.html"
    
    # Step 4: Create the post file
    post_content = f"""---
title: "{post_title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')}
source_url: "{post_url if post_url else 'N/A'}"
---

{content}
"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    debug_log(f"Successfully created: {filename}")
    print(f"✔ Created new post: {filename}")

if __name__ == "__main__":
    create_daily_post()
