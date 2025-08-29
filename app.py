from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session handling

# Dummy user store (in-memory, for demo purposes)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Save user in dummy store
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('quiz'))
        else:
            return "<h3>Invalid credentials. <a href='/login'>Try again</a></h3>"
    return render_template('login.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        total = 2

        # Static answer checking
        if request.form.get('q1') == 'Paris':
            score += 1
        if request.form.get('q2') == 'Shakespeare':
            score += 1

        username = session.get('username', 'Guest')
        return render_template('result.html', score=score, total=total, username=username)

    return render_template('quiz.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)