from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
import os
# import pandas as pd  # Временно отключено для тестирования
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import random
# from PIL import Image, ImageDraw  # Временно отключено для тестирования
from config import Config

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Create data directory if it doesn't exist
os.makedirs(app.config['DATA_FILES']['crypto_images'], exist_ok=True)


# Context processor to inject current year into templates
@app.context_processor
def inject_now():
    return {
        'current_year': datetime.now().year,
        'now': datetime.now()
    }


# Generate mock data if files don't exist
if app.config['MOCK_DATA']:
    for file_type, file_path in app.config['DATA_FILES'].items():
        if file_type != 'crypto_images' and not os.path.exists(file_path):
            if file_type == 'clients':
                # Generate client data - временно отключено pandas
                print(f"Mock data generation for {file_type} temporarily disabled")
                pass

            elif file_type == 'hot_leads':
                # Generate hot leads data - временно отключено pandas
                print(f"Mock data generation for {file_type} temporarily disabled")
                pass

    # Create mock crypto images - временно отключено Pillow
    crypto_dir = app.config['DATA_FILES']['crypto_images']
    if not os.listdir(crypto_dir):
        print("Mock image generation temporarily disabled")
        pass

# User credentials for authentication
users = {
    'admin': generate_password_hash('admin123'),
    'manager': generate_password_hash('manager123')
}


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# Application routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/clients')
@login_required
def show_clients():
    # Временно отключено для тестирования развертывания
    return render_template('clients.html', table="<p>Функция временно недоступна - тестирование развертывания</p>", error=None)


@app.route('/hot-leads')
@login_required
def show_hot_leads():
    # Временно отключено для тестирования развертывания
    return render_template('hot_lead.html', table="<p>Функция временно недоступна - тестирование развертывания</p>", error=None)


@app.route('/crypto-report')
def show_crypto_report():
    try:
        image_dir = app.config['DATA_FILES']['crypto_images']
        images = [f for f in os.listdir(image_dir)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        images.sort()
        return render_template('crypto_report.html', images=images)
    except Exception as e:
        return f"Помилка завантаження зображень: {str(e)}", 500


@app.route('/crypto-images/<filename>')
def get_crypto_image(filename):
    return send_from_directory(
        app.config['DATA_FILES']['crypto_images'],
        filename
    )


@app.route('/crypto-images/<filename>')
@login_required
def serve_crypto_image(filename):
    return send_from_directory(app.config['DATA_FILES']['crypto_images'], filename)


def analyze_images(image_folder='static/crypto-images'):
    images_data = []
    formats = set()

    for filename in os.listdir(image_folder):
        filepath = os.path.join(image_folder, filename)

        if not os.path.isfile(filepath):
            continue

        try:
            with Image.open(filepath) as img:
                width, height = img.size
                fmt = img.format or 'Невідомий формат'
                formats.add(fmt)

            size_kb = round(os.path.getsize(filepath) / 1024, 2)
            modified_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%d.%m.%Y %H:%M')

            img_data = {
                'filename': filename,
                'width': width,
                'height': height,
                'size_kb': size_kb,
                'format': fmt,  # виправлено: тут має бути результат image.format, а не метод str.format
                'modified': modified_time
            }

            images_data.append(img_data)
        except Exception as e:
            print(f"Помилка при обробці зображення '{filename}': {e}")
            continue

    stats = {
        'total': len(images_data),
        'formats': sorted(formats),
        'last_update': datetime.now().strftime('%d.%m.%Y %H:%M')
    }

    return images_data, stats

@app.route('/crypto-report')
def crypto_report():
    image_dir = 'data/crypto-images'
    images = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(image_dir, filename)
            with Image.open(path) as img:
                width, height = img.size
            images.append({
                'name': filename,
                'size': f"{round(os.path.getsize(path)/1024, 1)} KB",
                'dimensions': f"{width}×{height}",
                'format': filename.split('.')[-1].upper(),
                'modified': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d.%m.%Y %H:%M')
            })

    stats = {
        'total': len(images),
        'formats': sorted(set(img['format'] for img in images)),
        'last_update': datetime.now().strftime('%d.%m.%Y %H:%M')
    }

    return render_template('crypto_report.html', images=images, stats=stats)


@login_required  # або без, якщо не потрібна авторизація

@app.route('/crypto-images/<path:filename>')
def get_image(filename):
    return send_from_directory('static/crypto-images', filename)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

# Налаштування шляхів
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'data' / 'crypto-images'
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = BASE_DIR / 'static'
STATIC_DIR.mkdir(exist_ok=True)

def get_image_data():
    """Отримує дані про всі зображення у папці"""
    images = []
    for img_file in IMAGE_DIR.glob('*'):
        if img_file.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
            try:
                with Image.open(img_file) as img:
                    images.append({
                        'name': img_file.name,
                        'size': f"{os.path.getsize(img_file)/1024:.1f} KB",
                        'width': img.width,
                        'height': img.height,
                        'format': img.format,
                        'modified': datetime.fromtimestamp(
                            os.path.getmtime(img_file)).strftime('%d.%m.%Y %H:%M')
                    })
            except Exception as e:
                print(f"Помилка обробки {img_file.name}: {e}")
    return sorted(images, key=lambda x: x['name'])

@app.route('/')
def index():
    images, stats = analyze_images()
    now = datetime.now()
    return render_template('index.html', images=images, stats=stats, now=now)

IMAGE_FOLDER = 'static/images'

def get_images():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            path = os.path.join(IMAGE_FOLDER, filename)
            stat = os.stat(path)
            size_kb = round(stat.st_size / 1024, 2)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
            # Для розмірів картинки можна використовувати PIL (Pillow)
            try:
                from PIL import Image
                with Image.open(path) as img:
                    width, height = img.size
                    format = img.format
            except ImportError:
                width = height = format = 'N/A'
            images.append({
                'filename': filename,
                'size_kb': size_kb,
                'modified': modified,
                'width': width,
                'height': height,
                'format': format
            })
    return images

@app.route('/gallery')
def gallery():
    images = get_images()
    stats = {
        'total': len(images),
        'formats': list(set(img['format'] for img in images if img['format'] != 'N/A'))
    }
    now = datetime.now()
    return render_template('gallery.html', images=images, stats=stats, now=now)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)