# CMS Project Development Log

**Date:** March 17, 2026
**Status:** In progress - basic blog working

## Stack
- Flask (Python) web framework
- Markdown for blog posts
- Simple file-based storage

## Files
- `app.py` - Main Flask app with routing
- `templates/` - HTML templates (base, index, about, blog, post)
- `static/style.css` - Styling
- `posts/` - Markdown blog posts

## Current Routes
- `/` - Landing page
- `/about` - About page
- `/blog` - Blog listing
- `/blog/<slug>` - Individual posts

## Running
Local server at: http://192.168.10.108:5000

## Next Steps (when needed)
- Admin panel for writing posts via web
- Deploy to Render
- Add categories/tags
- Database integration
- User authentication

## Notes
- GitHub token expired - need to re-authenticate for deployment
- Posts sorted by filename (newest first)
- Markdown converted to HTML using `markdown` library
