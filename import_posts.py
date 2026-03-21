#!/usr/bin/env python3
"""Import all posts from dkcgi.net WordPress REST API"""

import requests
import re
import os
import json
from datetime import datetime

POSTS_DIR = '/home/vile/.openclaw/workspace/cms-project/posts'
os.makedirs(POSTS_DIR, exist_ok=True)

def clean_content(html_content):
    """Convert HTML content to clean markdown-like format"""
    if not html_content:
        return ""
    
    content = html_content
    
    # Remove WordPress block comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Convert YouTube embeds to our format
    youtube_pattern = r'<iframe[^>]*src="https://www\.youtube\.com/embed/([^"]+)"[^>]*>.*?</iframe>'
    content = re.sub(youtube_pattern, r'{{youtube:\1}}', content, flags=re.DOTALL)
    
    # Convert paragraph tags
    content = re.sub(r'<p[^>]*>', '\n\n', content)
    content = re.sub(r'</p>', '', content)
    
    # Convert line breaks
    content = re.sub(r'<br\s*/?>', '\n', content)
    
    # Convert bold/strong
    content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', content, flags=re.DOTALL)
    
    # Convert italic/em
    content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', content, flags=re.DOTALL)
    
    # Convert headings
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', content, flags=re.DOTALL)
    
    # Convert unordered lists
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', content, flags=re.DOTALL)
    
    # Convert links
    content = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
    
    # Convert remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up HTML entities
    content = content.replace('&#8217;', "'")
    content = content.replace('&#8216;', "'")
    content = content.replace('&#8211;', '–')
    content = content.replace('&#8212;', '—')
    content = content.replace('&#8220;', '"')
    content = content.replace('&#8221;', '"')
    content = content.replace('&amp;', '&')
    content = content.replace('&nbsp;', ' ')
    content = content.replace('&hellip;', '...')
    content = content.replace('&#039;', "'")
    
    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content

def get_categories(api_url, category_ids):
    """Fetch category names from API"""
    if not category_ids:
        return []
    try:
        cats = []
        for cat_id in category_ids[:5]:  # Limit to 5 categories
            resp = requests.get(f"https://dkcgi.net/wp-json/wp/v2/categories/{cat_id}", timeout=10)
            if resp.status_code == 200:
                cats.append(resp.json().get('name', ''))
        return cats
    except:
        return []

def slugify(text):
    """Convert title to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

# Fetch all posts
print("Fetching posts from dkcgi.net...")
response = requests.get(
    "https://dkcgi.net/wp-json/wp/v2/posts",
    params={'per_page': 100},
    headers={'User-Agent': 'DKCGI Importer/1.0'},
    timeout=30
)

if response.status_code != 200:
    print(f"Error: HTTP {response.status_code}")
    exit(1)

posts = response.json()
print(f"Found {len(posts)} posts")

# Track what we import
imported = 0
skipped = 0

for post in posts:
    try:
        title = post['title']['rendered']
        slug = post['slug']
        date_str = post['date_gmt']
        
        # Parse date
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        formatted_date = dt.strftime('%B %d, %Y')
        
        # Get content
        html_content = post['content']['rendered']
        clean_text = clean_content(html_content)
        
        # Get thumbnail
        thumbnail = post.get('jetpack_featured_media_url', '')
        if thumbnail:
            thumbnail = thumbnail.replace('?fit=1500%2C750&ssl=1', '?maxresdefault.jpg')
            thumbnail = thumbnail.replace('?resize=1500%2C750', '?maxresdefault.jpg')
            # Extract YouTube ID if it's a YouTube thumbnail
            if 'i' in thumbnail and 'wp.com' in thumbnail:
                # Convert WordPress CDN thumbnail to maxres
                thumbnail = re.sub(r'\?.*', '?maxresdefault.jpg', thumbnail)
        
        # Get categories
        category_ids = post.get('categories', [])
        categories = get_categories("https://dkcgi.net/wp-json/wp/v2/categories/", category_ids)
        cat_str = ', '.join(categories) if categories else 'Tutorial'
        
        # Check if post already exists
        filepath = os.path.join(POSTS_DIR, f"{slug}.md")
        if os.path.exists(filepath):
            print(f"  Skipping (exists): {title[:50]}...")
            skipped += 1
            continue
        
        # Build markdown content
        md_content = f"# {title}\n\n"
        md_content += f"**By Denis | {formatted_date}**\n\n"
        md_content += f"*Categories: {cat_str}*\n\n"
        if thumbnail:
            md_content += f"*Thumbnail: {thumbnail}*\n\n"
        md_content += "---\n\n"
        md_content += clean_text
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        imported += 1
        print(f"  Imported: {title[:50]}...")
        
    except Exception as e:
        print(f"  Error with post: {e}")
        continue

print(f"\nDone! Imported: {imported}, Skipped: {skipped}")
