import os
from datetime import datetime

POSTS_DIR = "_posts"
TODAY = datetime.now().strftime("%Y-%m-%d")

def create_jekyll_post():
    """Creates a new HTML post file"""
    filename = f"{POSTS_DIR}/{TODAY}-auto-post.html"  # Changed to .html
    
    # HTML content with Jekyll front matter
    content = """---
layout: post
title: "Daily Post {date}"
date: {datetime}
categories: [daily]
---

<p>This is an <strong>automated HTML post</strong>.</p>
<!-- Your HTML content here -->
""".format(
        date=TODAY,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
    )
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created HTML post: {filename}")

if __name__ == "__main__":
    create_jekyll_post()
