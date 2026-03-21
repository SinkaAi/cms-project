"""
CMS Project - Landing Page + Blog + Admin
A blank canvas that will grow into a full CMS
"""
import os
import json
import markdown
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, abort, session, flash, send_from_directory
from urllib.parse import unquote
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'cms-secret-key-change-in-production'

# Simple password (change this!)
ADMIN_PASSWORD = 'sinkaiscool'

# Blog posts directory
POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

# Static pages directory
PAGES_DIR = os.path.join(os.path.dirname(__file__), 'pages')

# Views tracking file
VIEWS_FILE = os.path.join(os.path.dirname(__file__), 'views.json')

# Subscribers file for newsletter
SUBSCRIBERS_FILE = os.path.join(os.path.dirname(__file__), 'subscribers.json')

# Courses data
COURSES = [
    {
        'id': 'vray-lighting',
        'title': 'V-Ray Lighting for Architectural Visualization',
        'short_desc': 'Master artificial and natural lighting setups for stunning arch-viz renders',
        'description': 'Learn professional lighting techniques used in architectural visualization. This comprehensive course covers HDRI setups, artificial lights, sun/sky systems, and post-production lighting adjustments.',
        'price': '$49',
        'original_price': '$79',
        'level': 'Intermediate',
        'thumbnail': 'http://www.dkcgi.net/wp-content/uploads/2019/03/Slider_Course.jpg',
        'url': 'https://gum.co/VrayArchVizLighting',
        'badge': 'BESTSELLER',
        'duration': '8 hours',
        'lectures': 24,
        'features': ['HDRI Lighting', 'Artificial Lights', 'Sun/Sky Systems', 'Post-Production Tips']
    },
    {
        'id': 'vray-materials',
        'title': 'The Ultimate V-Ray Materials Course',
        'short_desc': 'Create photorealistic materials from scratch — wood, metal, fabric, glass and more',
        'description': 'Stop downloading textures and start creating your own photorealistic V-Ray materials. Covers everything from basic diffuse materials to complex layered shaders.',
        'price': '$59',
        'original_price': '$99',
        'level': 'Beginner',
        'thumbnail': 'http://www.dkcgi.net/wp-content/uploads/2019/09/Materials_Banner.jpg',
        'url': 'https://gumroad.com/l/PAAah',
        'badge': None,
        'duration': '12 hours',
        'lectures': 36,
        'features': ['Wood & Flooring', 'Metals & Finishes', 'Fabric & Upholstery', 'Glass & Transparency']
    }
]

def get_views():
    """Load view counts from JSON file"""
    try:
        with open(VIEWS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_views(views):
    """Save view counts to JSON file"""
    with open(VIEWS_FILE, 'w') as f:
        json.dump(views, f, indent=2)

def get_subscribers():
    """Load subscribers from JSON file"""
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_subscribers(subscribers):
    """Save subscribers to JSON file"""
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subscribers, f, indent=2)

def increment_view(slug):
    """Increment view count for a post"""
    views = get_views()
    views[slug] = views.get(slug, 0) + 1
    save_views(views)

# Media uploads directory
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_post_file(filepath):
    """Parse a markdown post file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    title = ''
    categories = []
    thumbnail = ''
    author = ''
    date = ''
    excerpt = ''
    body_lines = []
    past_frontmatter = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Title (first # heading)
        if i == 0 and line.startswith('# '):
            title = line[2:].strip()
            continue
        
        # Detect frontmatter delimiter
        if line_stripped in ['---', '***', '___']:
            if not past_frontmatter:
                past_frontmatter = True
                continue
        
        # Before frontmatter delimiter: parse metadata lines
        if not past_frontmatter:
            if line_stripped.startswith('*Categories:'):
                cats_str = line_stripped.replace('*Categories:', '').strip().rstrip('*')
                categories = [c.strip() for c in cats_str.split(',') if c.strip()]
            elif line_stripped.startswith('*Thumbnail:'):
                thumbnail = line_stripped.replace('*Thumbnail:', '').strip().rstrip('*')
            elif '**By' in line_stripped:
                # **By Denis Keman | February 8, 2021**
                match = re.search(r'\*\*By\s+([^|]+)\|?\s*([^*]*)\*\*', line_stripped)
                if match:
                    author = match.group(1).strip()
                    date = match.group(2).strip()
            continue
        
        # After frontmatter delimiter: collect body content
        # Collect excerpt from first non-heading paragraph
        if not excerpt and line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('*') and not line_stripped.startswith('<'):
            excerpt = line_stripped[:150] + ('...' if len(line_stripped) > 150 else '')
        body_lines.append(line)
    
    return {
        'title': title,
        'categories': categories,
        'thumbnail': thumbnail,
        'author': author,
        'date': date,
        'excerpt': excerpt,
        'body': '\n'.join(body_lines).strip()
    }

def process_youtube_embeds(html_content):
    """Convert {{youtube:VIDEO_ID}} tags to embedded iframes."""
    # Pattern for our custom {{youtube:VIDEO_ID}} format
    html_content = re.sub(
        r'\{\{youtube:([a-zA-Z0-9_-]+)\}\}',
        r'<div class="youtube-embed"><iframe src="https://www.youtube.com/embed/\1" frameborder="0" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>',
        html_content
    )
    
    return html_content

def extract_youtube_id(text):
    """Extract YouTube video ID from text content."""
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

# Settings file
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

def load_settings():
    """Load site settings from JSON file"""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'site_title': 'DKCGI',
            'site_tagline': 'Personal Digital HQ',
            'site_description': 'A personal space for learning, building, and growing.',
            'author_name': 'Sinka & Denis',
            'youtube_url': '',
            'twitter_url': '',
            'github_url': '',
            'contact_email': '',
            'featured_post': '',
            'posts_per_page': 10
        }

def save_settings(settings):
    """Save site settings to JSON file"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Pages
@app.route('/')
def index():
    settings = load_settings()
    
    # Get featured post if set
    featured_post = None
    if settings.get('featured_post'):
        featured_slug = settings['featured_post']
        filepath = os.path.join(POSTS_DIR, f'{featured_slug}.md')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[0].replace('# ', '').strip() if lines else 'Untitled'
                thumbnail = ''
                for line in lines[1:]:
                    if line.strip().startswith('*Thumbnail:'):
                        thumb_content = line.strip().replace('*Thumbnail:', '').strip()
                        thumbnail = thumb_content.strip('*')
                        break
                featured_post = {'slug': featured_slug, 'title': title, 'thumbnail': thumbnail}
    
    # Get latest post for "Latest from Blog" section
    latest_post = None
    latest_posts = None
    posts_list = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]
            filepath = os.path.join(POSTS_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].replace('# ', '').strip() if lines else 'Untitled'
                    thumbnail = ''
                    date_str = ''
                    excerpt = ''
                    import re
                    content_lines = []
                    past_header = False
                    for line in lines[1:]:
                        line_stripped = line.strip()
                        if line_stripped in ['---', '***', '___']:
                            past_header = True
                            continue
                        if not past_header:
                            if line_stripped.startswith('*Thumbnail:'):
                                thumb_content = line_stripped.replace('*Thumbnail:', '').strip()
                                thumbnail = thumb_content.strip('*')
                            elif '|' in line_stripped and 'By' in line_stripped:
                                date_match = re.search(r'\|\s*([A-Za-z]+\s+\d+,\s+\d{4})', line_stripped)
                                if date_match:
                                    date_str = date_match.group(1).strip()
                        elif line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('*') and len(content_lines) < 3:
                            content_lines.append(line_stripped)
                    
                    if content_lines:
                        excerpt = ' '.join(content_lines)[:300] + '...'
                    
                    posts_list.append({'slug': slug, 'title': title, 'thumbnail': thumbnail, 'date': date_str, 'excerpt': excerpt})
            except:
                pass
    
    if posts_list:
        # Sort by date descending (newest first)
        from datetime import datetime
        def get_sort_key(post):
            date_str = post.get('date', '')
            if date_str:
                try:
                    return datetime.strptime(date_str, '%B %d, %Y')
                except:
                    pass
            return datetime.min
        posts_list.sort(key=get_sort_key, reverse=True)
        latest_posts = posts_list[:3]
    
    return render_template('index.html', settings=settings, featured_post=featured_post, latest_posts=latest_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tutorials')
def tutorials():
    # Tutorial categories (will be expanded with actual content)
    categories = [
        {'name': '3ds Max Modeling', 'icon': '🎯', 'desc': 'Master polygon modeling, Boolean operations, and complex geometry creation.'},
        {'name': 'Lighting & Rendering', 'icon': '💡', 'desc': 'Studio lighting setups, HDRI, V-Ray configurations, and render optimization.'},
        {'name': 'UVW Unwrapping', 'icon': '🗺️', 'desc': 'Learn UV mapping, peeling, stitching, and RizomUV workflows.'},
        {'name': 'Texturing', 'icon': '🎨', 'desc': 'Material creation, procedural textures, and substance painter techniques.'},
        {'name': 'Post-Production', 'icon': '✨', 'desc': 'Color correction, compositing, and finishing touches in Photoshop.'},
    ]
    return render_template('tutorials.html', categories=categories)

# Character page moved to Sinka Character CMS (http://192.168.10.107:5001)

@app.route('/courses')
def courses():
    settings = load_settings()
    return render_template('courses.html', settings=settings, courses=COURSES)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash('Incorrect password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Newsletter route
@app.route('/newsletter', methods=['POST'])
def newsletter():
    email = request.form.get('email', '').strip()
    success = False
    
    if email:
        # Load existing subscribers
        subscribers = []
        try:
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
        except:
            pass
        
        # Add new email if not already subscribed
        if email not in subscribers:
            subscribers.append(email)
            with open(SUBSCRIBERS_FILE, 'w') as f:
                json.dump(subscribers, f, indent=2)
            success = True
    
    # Redirect back to blog with success message
    if success:
        flash('Thanks for subscribing!', 'success')
    else:
        flash('Invalid email address.', 'error')
    return redirect('/blog')

# Blog routes
def get_all_posts():
    """Get all published posts with metadata."""
    import re
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            slug = filename[:-3]
            parsed = parse_post_file(filepath)
            status = 'published'
            date_str = ''
            
            # Read file to find date and status
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line_stripped = line.strip()
                    if line_stripped.startswith('*Status:'):
                        status = line_stripped.replace('*Status:', '').strip().lower()
                    elif '|' in line_stripped and 'By' in line_stripped:
                        # Extract date from format "**By Denis Keman | Month Day, Year**"
                        date_match = re.search(r'\|\s*([A-Za-z]+\s+\d+,\s+\d{4})', line_stripped)
                        if date_match:
                            date_str = date_match.group(1).strip()
            
            if status != 'draft':
                posts.append({
                    'title': parsed['title'] or slug.replace('-', ' ').title(),
                    'slug': slug,
                    'excerpt': parsed['excerpt'],
                    'thumbnail': parsed['thumbnail'],
                    'categories': parsed['categories'],
                    'date': date_str
                })
    return posts

@app.route('/blog')
def blog():
    settings = load_settings()
    posts_per_page = settings.get('posts_per_page', 10)
    page = request.args.get('page', 1, type=int)
    
    # Get all posts for sidebar data
    all_posts = get_all_posts()
    
    # Sort by date descending (newest first)
    from datetime import datetime
    def get_sort_key(post):
        date_str = post.get('date', '')
        if date_str:
            try:
                return datetime.strptime(date_str, '%B %d, %Y')
            except:
                pass
        # Fallback to slug for posts without dates
        return datetime.min
    all_posts_sorted = sorted(all_posts, key=get_sort_key, reverse=True)
    
    # Recent posts (last 5)
    recent_posts = all_posts_sorted[:5]
    
    # All categories
    all_categories = []
    for post in all_posts:
        for cat in post['categories']:
            if cat not in all_categories:
                all_categories.append(cat)
    all_categories = sorted(all_categories)
    
    # Popular posts (top 5 by views)
    views = get_views()
    popular_posts = sorted(all_posts, key=lambda x: views.get(x['slug'], 0), reverse=True)[:5]
    
    # Pagination
    total_posts = len(all_posts)
    total_pages = max(1, (total_posts + posts_per_page - 1) // posts_per_page)
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    start_idx = (page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    paginated_posts = all_posts_sorted[start_idx:end_idx]
    
    return render_template('blog.html', 
                           posts=paginated_posts, 
                           page=page, 
                           total_pages=total_pages,
                           total_posts=total_posts,
                           recent_posts=recent_posts,
                           all_categories=all_categories,
                           popular_posts=popular_posts)

# Public Search route
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    all_categories = []
    
    if query:
        query_lower = query.lower()
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md'):
                filepath = os.path.join(POSTS_DIR, filename)
                slug = filename[:-3]
                parsed = parse_post_file(filepath)
                
                # Search in title and content
                title_lower = parsed['title'].lower()
                body_lower = parsed['body'].lower() if parsed['body'] else ''
                
                if query_lower in title_lower or query_lower in body_lower:
                    status = 'published'
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().startswith('*Status:'):
                                status = line.strip().replace('*Status:', '').strip().lower()
                                break
                    
                    if status != 'draft':
                        excerpt = parsed['excerpt'] or ''
                        if query_lower in body_lower and not excerpt:
                            idx = body_lower.find(query_lower)
                            start = max(0, idx - 50)
                            end = min(len(parsed['body']), idx + len(query) + 50)
                            excerpt = ('...' if start > 0 else '') + parsed['body'][start:end] + ('...' if end < len(parsed['body']) else '')
                        
                        results.append({
                            'title': parsed['title'] or slug.replace('-', ' ').title(),
                            'slug': slug,
                            'excerpt': excerpt,
                            'thumbnail': parsed['thumbnail'],
                            'categories': parsed['categories']
                        })
        
        results.sort(key=lambda x: x['slug'], reverse=True)
    
    # Get all categories for sidebar
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            parsed = parse_post_file(os.path.join(POSTS_DIR, filename))
            for cat in parsed['categories']:
                if cat not in all_categories:
                    all_categories.append(cat)
    all_categories = sorted(all_categories)
    
    return render_template('search.html', results=results, query=query, all_categories=all_categories)

# Admin Search route
@app.route('/admin/search')
@login_required
def admin_search():
    query = request.args.get('q', '').strip().lower()
    results = []
    
    if query:
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md'):
                filepath = os.path.join(POSTS_DIR, filename)
                slug = filename[:-3]
                parsed = parse_post_file(filepath)
                
                # Search in title and content
                title_lower = parsed['title'].lower()
                body_lower = parsed['body'].lower() if parsed['body'] else ''
                
                if query in title_lower or query in body_lower:
                    status = 'published'
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().startswith('*Status:'):
                                status = line.strip().replace('*Status:', '').strip().lower()
                                break
                    
                    # Highlight the match in excerpt
                    excerpt = parsed['excerpt'] or ''
                    if query in body_lower and not excerpt:
                        # Find the relevant snippet in body
                        idx = body_lower.find(query)
                        start = max(0, idx - 50)
                        end = min(len(parsed['body']), idx + len(query) + 50)
                        excerpt = ('...' if start > 0 else '') + parsed['body'][start:end] + ('...' if end < len(parsed['body']) else '')
                    
                    results.append({
                        'title': parsed['title'] or slug.replace('-', ' ').title(),
                        'slug': slug,
                        'excerpt': excerpt,
                        'thumbnail': parsed['thumbnail'],
                        'categories': parsed['categories']
                    })
    
    results.sort(key=lambda x: x['slug'], reverse=True)
    return render_template('admin-search.html', results=results, query=query)

@app.route('/category/<category>')
def category_posts(category):
    """Show all posts in a specific category."""
    settings = load_settings()
    posts_per_page = settings.get('posts_per_page', 10)
    page = request.args.get('page', 1, type=int)
    
    # URL-decode the category (handles spaces encoded as %20)
    category = unquote(category)
    posts = []
    all_cats = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            slug = filename[:-3]
            parsed = parse_post_file(filepath)
            
            # Track all categories for sidebar
            for cat in parsed['categories']:
                if cat not in all_cats:
                    all_cats.append(cat)
            
            # Check if this post has the requested category
            if any(cat.lower() == category.lower() for cat in parsed['categories']):
                status = 'published'
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('*Status:'):
                            status = line.strip().replace('*Status:', '').strip().lower()
                            break
                if status != 'draft':
                    posts.append({
                        'title': parsed['title'] or slug.replace('-', ' ').title(),
                        'slug': slug,
                        'excerpt': parsed['excerpt'],
                        'thumbnail': parsed['thumbnail'],
                        'categories': parsed['categories']
                    })
    posts.sort(key=lambda x: x['slug'], reverse=True)
    
    # Pagination
    total_posts = len(posts)
    total_pages = max(1, (total_posts + posts_per_page - 1) // posts_per_page)
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    start_idx = (page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    paginated_posts = posts[start_idx:end_idx]
    
    return render_template('blog.html', 
                           posts=paginated_posts, 
                           category_filter=category, 
                           all_categories=all_cats,
                           page=page, 
                           total_pages=total_pages,
                           total_posts=total_posts)

def get_all_categories():
    """Get all unique categories from all posts."""
    categories = set()
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            parsed = parse_post_file(filepath)
            for cat in parsed['categories']:
                categories.add(cat)
    return sorted(list(categories))

@app.route('/blog/<slug>')
def post(slug):
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    if not os.path.exists(filepath):
        abort(404)
    
    # Increment view count
    increment_view(slug)
    views = get_views().get(slug, 0)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_post_file(filepath)
    html = markdown.markdown(parsed['body'] if parsed['body'] else content)
    html = process_youtube_embeds(html)
    
    # Extract YouTube video ID from content for related videos section
    video_id = extract_youtube_id(parsed.get('body', '') or content)
    
    # Get related posts (same category, excluding current post)
    related_posts = []
    current_categories = parsed['categories']
    if current_categories:
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md') and filename[:-3] != slug:
                post_slug = filename[:-3]
                post_filepath = os.path.join(POSTS_DIR, filename)
                post_parsed = parse_post_file(post_filepath)
                
                # Check for status - only include published posts
                status = 'published'
                with open(post_filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('*Status:'):
                            status = line.strip().replace('*Status:', '').strip().lower()
                            break
                
                if status == 'draft':
                    continue
                
                # Check if any category matches
                if any(cat in post_parsed['categories'] for cat in current_categories):
                    related_posts.append({
                        'slug': post_slug,
                        'title': post_parsed['title'] or post_slug.replace('-', ' ').title(),
                        'thumbnail': post_parsed['thumbnail'],
                        'categories': post_parsed['categories']
                    })
                    if len(related_posts) >= 3:
                        break
    
    return render_template('post.html', 
                          content=html, 
                          title=parsed['title'] or slug.replace('-', ' ').title(), 
                          categories=parsed['categories'],
                          views=views,
                          related_posts=related_posts,
                          video_id=video_id)

# Admin routes
@app.route('/admin')
@login_required
def admin():
    posts = []
    views_data = get_views()
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]
            # Read post metadata
            status = 'published'
            is_featured = False
            categories = []
            title = slug.replace('-', ' ').title()
            date = ''
            with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    line_stripped = line.strip()
                    if line_stripped.startswith('*Status:'):
                        status = line_stripped.replace('*Status:', '').strip().lower()
                    elif line_stripped.startswith('*Featured:'):
                        is_featured = True
                    elif line_stripped.startswith('*Categories:'):
                        cats = line_stripped.replace('*Categories:', '').strip()
                        categories = [c.strip() for c in cats.split(',')]
                    elif line_stripped.startswith('**By'):
                        # Extract date: "**By Denis | March 20, 2026**"
                        match = re.search(r'\| (.+?) \*\*', line_stripped)
                        if match:
                            date = match.group(1).strip()
                    elif line_stripped.startswith('# '):
                        title = line_stripped[2:].strip()
            
            posts.append({
                'slug': slug, 
                'filename': filename,
                'status': status,
                'is_featured': is_featured,
                'categories': categories,
                'title': title,
                'date': date,
                'views': views_data.get(slug, 0)
            })
    posts.sort(key=lambda x: x['slug'], reverse=True)
    
    # Get counts
    total_posts = len(posts)
    total_views = sum(views_data.values())
    total_categories = len(get_all_categories())
    
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            subscribers = json.load(f)
        total_subscribers = len(subscribers)
    except:
        total_subscribers = 0
    
    return render_template('admin.html', 
                         posts=posts,
                         total_posts=total_posts,
                         total_views=total_views,
                         total_categories=total_categories,
                         total_subscribers=total_subscribers)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        settings_data = {
            'site_title': request.form.get('site_title', 'DKCGI'),
            'site_tagline': request.form.get('site_tagline', ''),
            'site_description': request.form.get('site_description', ''),
            'author_name': request.form.get('author_name', ''),
            'youtube_url': request.form.get('youtube_url', ''),
            'twitter_url': request.form.get('twitter_url', ''),
            'github_url': request.form.get('github_url', ''),
            'contact_email': request.form.get('contact_email', ''),
            'featured_post': request.form.get('featured_post', ''),
            'posts_per_page': int(request.form.get('posts_per_page', 10))
        }
        save_settings(settings_data)
        flash('Settings saved!', 'success')
        return redirect('/admin')
    
    current_settings = load_settings()
    
    # Get list of published posts for featured post dropdown
    available_posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]
            available_posts.append(slug)
    available_posts.sort(reverse=True)
    
    return render_template('settings.html', settings=current_settings, posts=available_posts)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        categories = request.form.get('categories', '').strip()
        status = request.form.get('status', 'published')
        featured = request.form.get('featured', '') == 'true'
        thumbnail = request.form.get('thumbnail', '').strip()
        
        if not title:
            return render_template('new-post.html', error='Title is required')
        
        slug = title.lower().replace(' ', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        slug = f"{timestamp}-{slug}"
        
        # Build header with metadata
        header_parts = [f"# {title}"]
        header_parts.append(f"*Status: {status}*")
        if featured:
            header_parts.append("*Featured: true*")
        if categories:
            header_parts.append(f"*Categories: {categories}*")
        if thumbnail:
            header_parts.append(f"*Thumbnail: {thumbnail}*")
        header_parts.append("")
        header_parts.append("---")
        header_parts.append("")
        
        full_content = "\n".join(header_parts) + content
        
        filepath = os.path.join(POSTS_DIR, f'{slug}.md')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return redirect('/blog')
    
    return render_template('new-post.html')

@app.route('/admin/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    
    if not os.path.exists(filepath):
        abort(404)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        categories = request.form.get('categories', '').strip()
        status = request.form.get('status', 'published')
        featured = request.form.get('featured', '') == 'true'
        thumbnail = request.form.get('thumbnail', '').strip()
        
        if not title:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            return render_template('edit-post.html', slug=slug, title=title, content=content, error='Title is required')
        
        # Build header with metadata
        header_parts = [f"# {title}"]
        header_parts.append(f"*Status: {status}*")
        if featured:
            header_parts.append("*Featured: true*")
        if categories:
            header_parts.append(f"*Categories: {categories}*")
        if thumbnail:
            header_parts.append(f"*Thumbnail: {thumbnail}*")
        header_parts.append("")
        header_parts.append("---")
        header_parts.append("")
        
        full_content = "\n".join(header_parts) + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        flash('Post updated successfully!', 'success')
        return redirect('/admin')
    
    # GET request - load the post
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    lines = raw_content.split('\n')
    title = ''
    content_lines = []
    status = 'published'
    featured = False
    categories = ''
    thumbnail = ''
    
    # Parse header
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
        elif line.strip().startswith('*Status:'):
            status = line.strip().replace('*Status:', '').replace('*', '').strip()
        elif line.strip().startswith('*Featured:'):
            featured = True
        elif line.strip().startswith('*Categories:'):
            categories = line.strip().replace('*Categories:', '').replace('*', '').strip()
        elif line.strip().startswith('*Thumbnail:'):
            thumbnail = line.strip().replace('*Thumbnail:', '').replace('*', '').strip()
        elif line.strip() == '---' or line.strip() == '***':
            content_lines = []  # Reset - we're past header
        elif not title and line.startswith('#'):
            continue  # Skip other markdown headers in content
        else:
            content_lines.append(line)
    
    content = '\n'.join(content_lines).strip()
    
    return render_template('edit-post.html', 
                           slug=slug, 
                           title=title, 
                           content=content,
                           status=status,
                           featured=featured,
                           categories=categories,
                           thumbnail=thumbnail)

@app.route('/admin/delete/<filename>')
@login_required
def delete_post(filename):
    if not filename.endswith('.md') or '..' in filename or '/' in filename:
        abort(400)
    
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    return redirect('/admin')

# Static Pages Routes
@app.route('/contact')
def contact():
    settings = load_settings()
    return render_template('contact.html', settings=settings)

@app.route('/page/<page_slug>')
def static_page(page_slug):
    """Render a static page from the pages directory."""
    # Security: prevent directory traversal
    page_slug = page_slug.replace('../', '').replace('..', '')
    filepath = os.path.join(PAGES_DIR, f'{page_slug}.html')
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        page_content = f.read()
    return render_template('page.html', content=page_content, title=page_slug.replace('-', ' ').title())

# Admin: Static Pages Management
@app.route('/admin/pages')
@login_required
def admin_pages():
    """List all static pages."""
    pages = []
    if os.path.exists(PAGES_DIR):
        for filename in os.listdir(PAGES_DIR):
            if filename.endswith('.html'):
                slug = filename[:-5]
                # Try to extract title from file
                with open(os.path.join(PAGES_DIR, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    title_match = re.search(r'<title>([^<]+)</title>', content)
                    title = title_match.group(1) if title_match else slug
                pages.append({'slug': slug, 'title': title, 'filename': filename})
    pages.sort(key=lambda x: x['slug'])
    return render_template('admin-pages.html', pages=pages)

@app.route('/admin/pages/new', methods=['GET', 'POST'])
@login_required
def admin_new_page():
    """Create a new static page."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or title.lower().replace(' ', '-')
        content = request.form.get('content', '')
        
        if not title:
            flash('Title is required', 'error')
            return redirect('/admin/pages/new')
        
        # Sanitize slug
        slug = ''.join(c for c in slug if c.isalnum() or c == '-').lower()
        
        # Create pages directory if needed
        os.makedirs(PAGES_DIR, exist_ok=True)
        
        filepath = os.path.join(PAGES_DIR, f'{slug}.html')
        if os.path.exists(filepath):
            flash('A page with this slug already exists', 'error')
            return redirect('/admin/pages/new')
        
        # Create the page file with proper HTML structure
        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DKCGI</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="scanline"></div>
    <header>
        <nav>
            <a href="/" class="logo">
                <span class="nexus-logo">
                    <span class="nexus-ring"></span>
                    <span class="nexus-text">DKCGI</span>
                </span>
            </a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/tutorials">Tutorials</a></li>
                <li><a href="/blog">Blog</a></li>
                <li><a href="/character">Character</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/admin">Admin</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="static-page">
            <h1>{title}</h1>
            <div class="page-content">
                {content}
            </div>
            <a href="/" class="btn">← Back to Home</a>
        </section>
    </main>
    <footer>
        <p>&copy; 2026 <span class="footer-nexus">DKCGI</span>. Built with 🧠 by Sinka.</p>
    </footer>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_html)
        
        flash(f'Page "{title}" created successfully!', 'success')
        return redirect('/admin/pages')
    
    return render_template('admin-edit-page.html', page=None)

@app.route('/admin/pages/edit/<slug>', methods=['GET', 'POST'])
@login_required
def admin_edit_page(slug):
    """Edit an existing static page."""
    import re  # Import at function level
    slug = slug.replace('../', '').replace('..', '')
    filepath = os.path.join(PAGES_DIR, f'{slug}.html')
    
    if not os.path.exists(filepath):
        abort(404)
    
    if request.method == 'POST':
        content = request.form.get('content', '')
        
        # Read current file and update content section
        with open(filepath, 'r', encoding='utf-8') as f:
            page_html = f.read()
        
        # Replace content between page-content div
        pattern = r'<div class="page-content">(.*?)</div>\s*<a href="/"'
        replacement = f'<div class="page-content">{content}</div>\\n            <a href="/"'
        new_html = re.sub(pattern, replacement, page_html, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        flash('Page updated successfully!', 'success')
        return redirect('/admin/pages')
    
    # GET - load page content
    with open(filepath, 'r', encoding='utf-8') as f:
        page_html = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', page_html)
    title = title_match.group(1).replace(' | DKCGI', '') if title_match else slug
    
    # Extract content from page-content div
    content_match = re.search(r'<div class="page-content">(.*?)</div>', page_html, re.DOTALL)
    content = content_match.group(1).strip() if content_match else ''
    
    return render_template('admin-edit-page.html', page={'slug': slug, 'title': title, 'content': content})

@app.route('/admin/pages/delete/<slug>')
@login_required
def admin_delete_page(slug):
    """Delete a static page."""
    slug = slug.replace('../', '').replace('..', '')
    filepath = os.path.join(PAGES_DIR, f'{slug}.html')
    
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('Page deleted successfully!', 'success')
    
    return redirect('/admin/pages')

# Media Upload Routes
@app.route('/admin/media')
@login_required
def admin_media():
    """List all uploaded media files."""
    files = []
    if os.path.exists(UPLOADS_DIR):
        for filename in os.listdir(UPLOADS_DIR):
            filepath = os.path.join(UPLOADS_DIR, filename)
            if os.path.isfile(filepath):
                # Get file info
                stat = os.stat(filepath)
                ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'is_image': ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                })
    # Sort by modified date, newest first
    files.sort(key=lambda x: x['modified'], reverse=True)
    return render_template('admin-media.html', files=files)

@app.route('/admin/media/upload', methods=['POST'])
@login_required
def admin_upload_media():
    """Handle file upload."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect('/admin/media')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect('/admin/media')
    
    if file and allowed_file(file.filename):
        # Ensure uploads directory exists
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        
        filename = secure_filename(file.filename)
        # Add timestamp to avoid duplicates
        import time
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = f"{name}_{int(time.time())}.{ext}" if ext else f"{name}_{int(time.time())}"
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        file.save(filepath)
        flash(f'File "{filename}" uploaded successfully!', 'success')
    else:
        flash('File type not allowed. Allowed: png, jpg, jpeg, gif, webp, svg', 'error')
    
    return redirect('/admin/media')

@app.route('/admin/media/delete/<filename>')
@login_required
def admin_delete_media(filename):
    """Delete an uploaded file."""
    # Security checks
    if '..' in filename or '/' in filename:
        abort(400)
    
    filepath = os.path.join(UPLOADS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'File "{filename}" deleted successfully!', 'success')
    
    return redirect('/admin/media')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(UPLOADS_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
