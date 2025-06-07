import os
from datetime import datetime

POSTS_DIR = "_posts"
TODAY = datetime.now().strftime("%Y-%m-%d")

def create_jekyll_post():
    """Creates a new HTML post with front matter"""
    filename = f"{POSTS_DIR}/{TODAY}-auto-post.html"
    
    content = """---
title: "Daily Post {date}"
---

<div class="post-content">
<p>Automated HTML content goes here.</p>
</div>
""".format(date=TODAY)
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_jekyll_post()
