#!/usr/bin/env python3
from app import app
import re

with app.test_client() as client:
    response = client.get('/blog/modeling-infinity-mirror-3ds-max-vray')
    html = response.data.decode()
    
    # Count article elements in related section
    related_section = re.search(r'<section class="related-posts">.*?</section>', html, re.DOTALL)
    if related_section:
        section_html = related_section.group(0)
        # Count actual article tags within the related-posts-grid
        articles = re.findall(r'<article class="related-post-card">', section_html)
        print(f'Number of related post articles: {len(articles)}')
        
        # Extract titles
        titles = re.findall(r'<h4><a href="/blog/[^"]+">([^<]+)</a></h4>', section_html)
        print(f'Related post titles: {titles}')
    else:
        print('No related posts section found')
    
    # Verify author bio
    print(f'Author bio present: {"author-bio" in html}')
    print(f'Denis Keman present: {"Denis Keman" in html}')
    print(f'YouTube link present: {"Denis Keman on YouTube" in html}')
    
    # Verify share buttons still work
    print(f'Share buttons present: {"share-buttons" in html}')
    print(f'View count present: {"view-count" in html}')
