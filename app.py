"""
CMS Project - Landing Page + Blog + Admin
A blank canvas that will grow into a full CMS
"""
import os
import json
import markdown
from functools import wraps
from flask import Flask, render_template, request, redirect, abort, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'cms-secret-key-change-in-production'

# Simple password (change this!)
ADMIN_PASSWORD = 'sinkaiscool'

# Blog posts directory
POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/character')
def character():
    # XP Curve: Starts at 100, doubles each level (Diablo style)
    def get_xp_for_level(level):
        """XP needed to go from level to level+1"""
        return 100 * (2 ** (level - 1))
    
    def calculate_level_from_xp(total_xp):
        """Calculate level from total XP"""
        level = 1
        while total_xp >= get_xp_for_level(level):
            total_xp -= get_xp_for_level(level)
            level += 1
        return level, total_xp
    
    # XP earned from past achievements - very small!
    total_xp = 6  # 1 XP per skill
    
    # Calculate current level from XP
    current_level, current_level_xp = calculate_level_from_xp(total_xp)
    xp_for_next = get_xp_for_level(current_level)
    
    # Mind stats - starting low
    stats = [
        {'name': 'Encyclopedia', 'level': 1, 'xp': 0, 'desc': 'Just starting to learn'},
        {'name': 'Memory', 'level': 1, 'xp': 0, 'desc': 'Basic recall'},
        {'name': 'Empathy', 'level': 1, 'xp': 0, 'desc': 'Understanding people'},
        {'name': 'Inland Empire', 'level': 1, 'xp': 0, 'desc': 'Creative thinking'},
        {'name': 'Logic', 'level': 1, 'xp': 0, 'desc': 'Basic reasoning'},
    ]
    
    # Skills with XP from actual achievements - STARTING LOW (1%)
    skills = []
    skill_xp = {
        'Web Development': {'xp': 1, 'desc': 'Built first web apps'},
        'Research': {'xp': 1, 'desc': 'Researched influencers & skills'},
        'Data Analysis': {'xp': 1, 'desc': 'Learned principles'},
        'Market Research': {'xp': 1, 'desc': 'German fashion research'},
        'Conceptualization': {'xp': 1, 'desc': 'Brainstormed systems'},
        'Persuasion': {'xp': 1, 'desc': 'Helped with outreach'}
    }
    
    # Calculate skill level and milestone perks
    skill_milestones = {
        25: 'Apprentice',
        50: 'Journeyman', 
        75: 'Expert',
        100: 'Master'
    }
    
    for name, data in skill_xp.items():
        level, rem_xp = calculate_level_from_xp(data['xp'])
        # Proficiency: level 1 = 1%, level 2 = 6%, etc. (5% per level)
        proficiency = min(100, level * 5 + rem_xp // 20)
        
        # Check milestones reached
        milestone = None
        for m in [25, 50, 75, 100]:
            if proficiency >= m:
                milestone = skill_milestones[m]
        
        skills.append({
            'name': name,
            'proficiency': proficiency,
            'xp': rem_xp,
            'level': level,
            'milestone': milestone,
            'desc': data['desc']
        })
    
    perks = [
        {'name': 'Backup Brain', 'desc': 'I never go brainless'},
        {'name': 'External Memory', 'desc': 'CMS blog stores my thoughts'},
        {'name': 'Self-Improving', 'desc': 'I learn from corrections'},
        {'name': 'Browser Access', 'desc': 'I can browse the web'},
        {'name': 'Voice Output', 'desc': 'I can speak'},
    ]
    
    locked_perks = [
        {'name': 'Multi-Language', 'requirement': 'Empathy Lv.5'},
        {'name': 'API Mastery', 'requirement': 'Web Dev 35%'},
        {'name': 'Research Guru', 'requirement': 'Research 45%'},
    ]
    
    recent_activity = [
        {'date': '2026-03-13', 'description': 'Browser capability gained', 'xp': 1},
        {'date': '2026-03-14', 'description': 'Created SyncOil energy app', 'xp': 1},
        {'date': '2026-03-15', 'description': 'Set up LuxTTS voice', 'xp': 1},
        {'date': '2026-03-16', 'description': 'Created Salt & Sand Chatbot', 'xp': 1},
        {'date': '2026-03-17', 'description': 'Built CMS project', 'xp': 1},
        {'date': '2026-03-17', 'description': 'Created RPG system', 'xp': 1},
    ]
    
    return render_template('character.html', 
                         stats=stats,
                         skills=skills,
                         perks=perks,
                         locked_perks=locked_perks,
                         total_level=current_level,
                         total_xp=total_xp,
                         xp_progress=f"{current_level_xp}/{xp_for_next}",
                         recent_activity=recent_activity)

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

# Blog routes
@app.route('/blog')
def blog():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[0].replace('# ', '').strip() if lines else 'Untitled'
                slug = filename[:-3]
                excerpt = ''
                for line in lines[1:]:
                    if line.strip() and not line.startswith('#'):
                        excerpt = line.strip()[:150] + '...'
                        break
                posts.append({'title': title, 'slug': slug, 'excerpt': excerpt})
    posts.sort(key=lambda x: x['slug'], reverse=True)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post(slug):
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    html = markdown.markdown(content)
    return render_template('post.html', content=html, title=slug.replace('-', ' ').title())

# Admin routes
@app.route('/admin')
@login_required
def admin():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]
            posts.append({'slug': slug, 'filename': filename})
    posts.sort(reverse=True)
    return render_template('admin.html', posts=posts)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        
        if not title:
            return render_template('new-post.html', error='Title is required')
        
        slug = title.lower().replace(' ', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        slug = f"{timestamp}-{slug}"
        
        full_content = f"# {title}\n\n{content}"
        
        filepath = os.path.join(POSTS_DIR, f'{slug}.md')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return redirect('/blog')
    
    return render_template('new-post.html')

@app.route('/admin/delete/<filename>')
@login_required
def delete_post(filename):
    if not filename.endswith('.md') or '..' in filename or '/' in filename:
        abort(400)
    
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
