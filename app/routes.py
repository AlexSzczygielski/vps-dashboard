from flask import Blueprint, request, current_app, render_template, session, redirect, url_for, flash, abort, send_from_directory
import datetime
import json
import os
import uuid
from functools import wraps

main = Blueprint('main', __name__)

# --- PASTEBIN HELPERS & DECORATOR ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config.get('PASTEBIN_ENABLED'):
            abort(404) # Hide pastebin if not enabled
        if 'logged_in' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_paste_path(paste_id):
    pastes_dir = os.path.join(current_app.root_path, 'pastes')
    # Security: ensure paste_id is a safe filename and prevent path traversal
    if not all(c.isalnum() or c == '-' for c in paste_id):
        return None
    return os.path.join(pastes_dir, paste_id)

# --- DASHBOARD ---

def load_dashboard_config():
    config_path = os.path.join(current_app.root_path, '..', 'dashboard_config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default config if file is missing or corrupt
        return {
            "greeting_name": "User",
            "background_image_url": "https://source.unsplash.com/random/1920x1080/?nature",
            "link_groups": [
                {
                    "name": "Error",
                    "links": [{"name": "Could not load dashboard_config.json", "url": "#"}]
                }
            ]
        }

@main.route('/')
def index():
    # Load dashboard config
    config = load_dashboard_config()
    pastebin_enabled = current_app.config.get('PASTEBIN_ENABLED', False)

    return render_template(
        'index.html',
        greeting_name=config.get("greeting_name", "User"),
        day_background_image_url=config.get("day_background_image_url"),
        night_background_image_url=config.get("night_background_image_url"),
        link_groups=config.get("link_groups", []),
        pastebin_enabled=pastebin_enabled
    )

# --- PASTEBIN ROUTES ---

@main.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config.get('PASTEBIN_ENABLED'):
        abort(404)
    if 'logged_in' in session:
        return redirect(url_for('main.paste'))

    if request.method == 'POST':
        password = request.form.get('password')
        if password == current_app.config['PASTEBIN_PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('main.paste'))
        else:
            flash('Incorrect password')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.index'))

@main.route('/paste', methods=['GET', 'POST'])
@login_required
def paste():
    pastes_dir = os.path.join(current_app.root_path, 'pastes')
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            paste_id = str(uuid.uuid4())
            path = get_paste_path(paste_id)
            if path:
                with open(path, 'w') as f:
                    f.write(content)
                return redirect(url_for('main.view_paste', paste_id=paste_id))
    
    # List existing pastes
    all_pastes = []
    if not os.path.exists(pastes_dir):
        os.makedirs(pastes_dir)
        
    for filename in os.listdir(pastes_dir):
        path = os.path.join(pastes_dir, filename)
        if os.path.isfile(path):
            try:
                timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
                all_pastes.append({'id': filename, 'timestamp': timestamp})
            except Exception:
                continue # Ignore files with bad data
    
    # Sort by most recent
    all_pastes.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('paste.html', pastes=all_pastes)

@main.route('/paste/<paste_id>')
@login_required
def view_paste(paste_id):
    path = get_paste_path(paste_id)
    if not path or not os.path.exists(path):
        abort(404)
    
    with open(path, 'r') as f:
        content = f.read()
        
    return render_template('paste.html', single_paste=True, paste_id=paste_id, content=content)

# --- DEMO ASSETS ROUTES ---
@main.route('/demo_assets/<asset_name>')
def get_demo_asset(asset_name):
    """Used to return pics stored as demo_assets - e.g. for github uses."""
    folder = os.path.join(current_app.root_path, 'static', 'demo_assets')

    # Security: prevent directory traversal
    if '..' in asset_name or asset_name.startswith('/'):
        abort(400)

    # Check if file exists
    file_path = os.path.join(folder, asset_name)
    if not os.path.isfile(file_path):
        print("Asset not found")
        abort(404)

    # Serve the file
    return send_from_directory(folder, asset_name)