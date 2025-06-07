import os
from datetime import datetime
import frontmatter

POSTS_DIR = "_posts"
TODAY = datetime.now().strftime("%Y-%m-%d")

def create_jekyll_post():
    """Creates a simple post if scraping fails."""
    filename = f"{POSTS_DIR}/{TODAY}-auto-post.md"
    content = "This post was created automatically!\n\nCustomize me later."
    
    post = frontmatter.Post(content)
    post.metadata = {
        'title': f"Auto Post {TODAY}",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S %z"),
        'layout': 'post'
    }
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_jekyll_post()
