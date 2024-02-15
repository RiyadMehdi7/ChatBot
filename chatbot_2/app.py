from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
import joblib
import random
from Levenshtein import ratio
import sys
sys.path.append('chatbot_2')
from responses import RESPONSES

app = Flask(__name__)
app.secret_key = 'riyadmehdiyev'

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://riyadmehdi17:<Rmn2707>@chatbot.yi4rkdu.mongodb.net/?retryWrites=true&w=majority"  # replace with your MongoDB URI
mongo = PyMongo(app)

chats = []

model = joblib.load("chatbot_2/svm_classifier.pkl")
vectorizer = joblib.load("chatbot_2/tfidf_vectorizer.pkl")

keywords = ['rəhbər', 'birbaşa rəhbər', 'kpi', 'əfg', 'kompetensiya', 'yekun fəaliyyət balı', 'rotasiya','şkala','qiymətləndirmə','kompetensiyalar','təyin olunur','şkalası']

def get_closest_match(input_word):
    closest_match = max(keywords, key=lambda keyword: ratio(input_word, keyword))
    return closest_match if ratio(input_word, closest_match) > 0.8 else None

def check_keywords(question):
    words = question.lower().split()
    for word in words:
        closest_match = get_closest_match(word)
        if closest_match:
            return None
    return "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz"

def predict_category(question):
    question_vector = vectorizer.transform([question])
    return model.predict(question_vector)[0]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            session['username'] = username
            # Store login information in MongoDB
            mongo.db.logins.insert_one({'username': username, 'password': password})
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        message = request.form['message']
        # Store chat message in MongoDB
        mongo.db.chats.insert_one({'username': session['username'], 'message': message})
    # Retrieve chat messages from MongoDB
    chats = list(mongo.db.chats.find())
    return render_template('index.html', chats=chats)

def valid_login(username, password):
    return username == 'admin' and password == 'secret'

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/initial_message")
def initial_message():
    return jsonify({"initial_message": "Salam, sizə necə kömək edə bilərəm?"})

def get_response(predicted_category):
    responses = RESPONSES.get(predicted_category, [])
    return random.choice(responses)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.json.get("question", "").lower()
        greetings = ['hello', 'salam', 'hi']
        if question in greetings:
            return jsonify({"response": "Salam! Sizə necə kömək edim?"})
        greetings = ['necəsən', 'nə var', 'nə var nə yox','necəsən?']
        if question in greetings:
            return jsonify({"response": "Mən yaxşıyam, təşəkkürlər! Sizə necə kömək edə bilərəm?"})
        default_response = check_keywords(question)
        if default_response:
            return jsonify({"response": default_response})
        predicted_category = predict_category(question)
        response = get_response(predicted_category)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
