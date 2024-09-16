from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# HTML templates with embedded CSS
home_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1em 0;
            text-align: center; 
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 1em;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        nav {
            margin-bottom: 1em;
        }
        nav a {
            margin: 0 1em;
            color: #333;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .intro {
            margin-bottom: 2em;
        }
        .features {
            display: flex;
            justify-content: space-around;
        }
        .feature {
            width: 30%;
            background-color: #e2e2e2;
            padding: 1em;
            border-radius: 8px;
            text-align: center;
        }
        footer {
            text-align: center;
            padding: 1em;
            background-color: #333;
            color: #fff;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>My Flask Application</h1>
    </header>
    <div class="container">
        <nav>
            <a href="{{ url_for('home') }}">Home</a> | 
            <a href="{{ url_for('about') }}">About</a> | 
            <a href="{{ url_for('contact') }}">Contact</a> |
            {% if 'username' in session %}
                <a href="{{ url_for('logout') }}">Logout ({{ session['username'] }})</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a> |
                <a href="{{ url_for('register') }}">Register</a>
            {% endif %}
        </nav>
        <div class="intro">
            <h2>Welcome to My Flask App!</h2>
            <p>This application showcases Flask's capabilities with dynamic routes, forms, user authentication, and database integration.</p>
        </div>
        <div class="features">
            <div class="feature">
                <h2>Dynamic Routing</h2>
                <p>Learn how to handle different URLs and render dynamic content.</p>
            </div>
            <d
            iv class="feature">
                <h2>Form Handling</h2>
                <p>Submit and process forms with ease.</p>
            </div>
            <div class="feature">
                <h2>Database Integration</h2>
                <p>Store and retrieve data using an SQLite database.</p>
            </div>
        </div>
    </div>
    <footer>
        &copy; 2024 My Flask App
    </footer>
</body>
</html>
'''

about_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>About</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1em 0;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 1em;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        nav {
            margin-bottom: 1em;
        }
        nav a {
            margin: 0 1em;
            color: #333;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .team-member {
            display: flex;
            align-items: center;
            margin-bottom: 1em;
        }
        .team-member img {
            border-radius: 50%;
            margin-right: 1em;
        }
        footer {
            text-align: center;
            padding: 1em;
            background-color: #333;
            color: #fff;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>My Flask Application</h1>
    </header>
    <div class="container">
        <nav>
            <a href="{{ url_for('home') }}">Home</a> | 
            <a href="{{ url_for('about') }}">About</a> | 
            <a href="{{ url_for('contact') }}">Contact</a> |
            {% if 'username' in session %}
                <a href="{{ url_for('logout') }}">Logout ({{ session['username'] }})</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a> |
                <a href="{{ url_for('register') }}">Register</a>
            {% endif %}
        </nav>
        <h1>About This Project</h1>
        <p>This application demonstrates Flask's ability to handle routing, forms, user authentication, and database operations all in one file. It also includes embedded CSS for styling, making it a self-contained example of a Flask project.</p>
        
        <h2>Our Team</h2>
       <div>
                <h2>Saurabh Kulkarni</h2>
                <p>Lead Developer</p>
            </div>      
        <h2>User Messages</h2>
        <ul>
            {% for message in messages %}
                <li><strong>{{ message.name }}:</strong> {{ message.message }}</li>
            {% endfor %}
        </ul>
    </div>
    <footer>
        &copy; 2024 My Flask App
    </footer>
</body>
</html>
'''

contact_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1em 0;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 1em;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        nav {
            margin-bottom: 1em;
        }
        nav a {
            margin: 0 1em;
            color: #333;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 0.5em;
        }
        input, textarea {
            margin-bottom: 1em;
            padding: 0.5em;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 0.5em;
            background-color: #333;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #555;
        }
        footer {
            text-align: center;
            padding: 1em;
            background-color: #333;
            color: #fff;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>My Flask Application</h1>
    </header>
    <div class="container">
        <nav>
            <a href="{{ url_for('home') }}">Home</a> | 
            <a href="{{ url_for('about') }}">About</a> | 
            <a href="{{ url_for('contact') }}">Contact</a> |
            {% if 'username' in session %}
                <a href="{{ url_for('logout') }}">Logout ({{ session['username'] }})</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a> |
                <a href="{{ url_for('register') }}">Register</a>
            {% endif %}
        </nav>
        <h1>Contact Us</h1>
        <form method="post" action="{{ url_for('contact') }}">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <label for="message">Message:</label>
            <textarea id="message" name="message" required></textarea>
            <button type="submit">Send</button>
        </form>
    </div>
    <footer>
        &copy; 2024 My Flask App
    </footer>
</body>
</html>
'''

result_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submission Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1em 0;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 1em;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        nav {
            margin-bottom: 1em;
        }
        nav a {
            margin: 0 1em;
            color: #333;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        footer {
            text-align: center;
            padding: 1em;
            background-color: #333;
            color: #fff;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>My Flask Application</h1>
    </header>
    <div class="container">
        <h1>Thank You for Your Message!</h1>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Message:</strong> {{ message }}</p>
        <nav>
            <a href="{{ url_for('home') }}">Home</a> | 
            <a href="{{ url_for('about') }}">About</a> | 
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </div>
    <footer>
        &copy; 2024 My Flask App
    </footer>
</body>
</html>
'''

# Routes
@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/about')
def about():
    messages = Message.query.all()
    return render_template_string(about_template, messages=messages)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return render_template_string(result_template, name=name, email=email, message=message)
    return render_template_string(contact_template)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Register</button>
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid username or password'
    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404 - Page Not Found</h1><p>The page you are looking for does not exist.</p>', 404
 
def create_db():
    with app.app_context():
        db.create_all()  # Create database tables

if __name__ == '__main__':
    create_db()  # Create database tables
    app.run(debug=True)
