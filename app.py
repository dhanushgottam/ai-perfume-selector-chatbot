from flask import Flask, render_template, request, jsonify, redirect
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.0-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    prompt = user_message.strip()
    try:
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        reply = f"Oops! Something went wrong: {str(e)}"
    return jsonify({'reply': reply})

# ✅ Login route must be above app.run
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "123":
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')
#sign up page 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # You can add DB logic here later
        return redirect('/login')
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
