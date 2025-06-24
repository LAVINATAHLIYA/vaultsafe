import os
import time
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from utils import encrypt_note, decrypt_note, encrypt_file, decrypt_file

# Initialize app
app = Flask(__name__)
app.secret_key = 'vaultsafe-secret-key'

UPLOAD_FOLDER = 'uploads'
DECRYPTED_FOLDER = 'decrypted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            flash("Login failed. Please sign in if you're new.")
            return redirect(url_for('login'))

        session['user'] = user['email']
        session['name'] = user['name']
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if existing_user:
            flash('User already exists')
        else:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                         (name, email, hashed_password))
            conn.commit()
            flash('Account created! Please log in.')
            return redirect(url_for('login'))

        conn.close()
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    files = []
    for fname in os.listdir(UPLOAD_FOLDER):
        files.append({
            'title': fname.replace('.enc', ''),
            'filename': fname
        })
    return render_template('dashboard.html', files=files)

@app.route('/notes', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note = request.form['note_content']
        key = request.form.get('key') or "defaultnote"
        encrypted = encrypt_note(note, key)
        filename = f"note_{int(time.time())}.enc"
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(encrypted)
        flash('Note saved and encrypted!')
        return redirect(url_for('dashboard'))
    return render_template('notes.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        key = request.form.get('key') or "defaultfile"
        if file:
            encrypted_data = encrypt_file(file, key)
            filename = f"{int(time.time())}_{file.filename}.enc"
            with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
                f.write(encrypted_data)
            flash('File uploaded and encrypted!')
            return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    filename = request.form.get('filename')
    key = request.form.get('decryptionKey')

    if not filename or not key:
        flash("Missing file or key.")
        return redirect(url_for('dashboard'))

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        if filename.startswith("note_"):
            with open(file_path, 'rb') as f:
                encrypted = f.read()
            content = decrypt_note(encrypted, key)
            return render_template('decrypted.html', title=filename, content=content)
        else:
            decrypted = decrypt_file(file_path, key)
            if decrypted:
                output_path = os.path.join(DECRYPTED_FOLDER, filename.replace('.enc', ''))
                with open(output_path, 'wb') as f:
                    f.write(decrypted)
                return send_file(output_path, as_attachment=True)
            else:
                flash("Failed to decrypt file.")
    except Exception as e:
        flash(f"Error: {str(e)}")

    return redirect(url_for('dashboard'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        flash("File deleted.")
    except:
        flash("File not found or couldn't be deleted.")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
