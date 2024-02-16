from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import joblib
import random
from Levenshtein import ratio
import sys
sys.path.append('chatbot_2')
from responses import RESPONSES

app = Flask(__name__)
app.secret_key = 'riyadmehdiyev'

chats = []

model = joblib.load("chatbot_2/svm_classifier.pkl")
vectorizer = joblib.load("chatbot_2/tfidf_vectorizer.pkl")

keywords = ['rəhbər', 'birbaşa rəhbər', 'kpi', 'əfg', 'kompetensiya', 'yekun fəaliyyət balı', 'rotasiya','şkala','qiymətləndirmə','kompetensiyalar','təyin olunur','şkalası','karyera','dəyişiklik','intizam tənbehi','töhmət', 'kiçik mütəxəssis',
            'texniki bacarıq','qrupdaxili yerdəyişmə', 'qrupdaxili keçid']

keyword_responses = {
    'rəhbər': 'Birbaşa rəhbər',
    'birbaşa rəhbər': 'Birbaşa rəhbər',
    'kpi': 'Əsas fəaliyyət göstəriciləri (KPİ)',
    'əfg': 'Əsas fəaliyyət göstəriciləri (KPİ)',
    'kompetensiya': 'Kompetensiya',
    'yekun fəaliyyət balı': 'Yekun fəaliyyət balı',
    'rotasiya': 'Rotasiya halında ƏFG',
    'qiymətləndirmə': 'Yekun fəaliyyət balı',
    'kompetensiyalar': 'Kompetensiya',
    'təyin olunur': 'Kim tərəfindən təyin olunur',
    'karyera': 'Karyera istiqamətini dəyişmiş əməkdaşın artımı',
    'dəyişiklik': 'Karyera istiqamətində dəyişiklik',
    'intizam tənbehi': 'Karyera inkişafı meyarlarında intizam tənbeh',
    'töhmət': 'Karyera inkişafı meyarlarında intizam tənbeh',
    'kiçik mütəxəssis': 'Kiçik mütəxəssislərin vəzifə artımı',
    'texniki bacarıq': 'Texniki bacarıqlar',
    'qrupdaxili yerdəyişmə': 'Qrupdaxili yerdəyişmə',
    'qrupdaxili keçid': 'Qrupdaxili yerdəyişmə'
}

def get_closest_match(input_word):
    threshold = 0.6  # Set a threshold for the Levenshtein ratio
    closest_match = max(keywords, key=lambda keyword: ratio(input_word, keyword))
    if ratio(input_word, closest_match) >= threshold:
        return closest_match
    else:
        return None

def check_keywords(question):
    words = question.lower().split()
    for word in words:
        closest_match = get_closest_match(word)
        if closest_match and closest_match in keyword_responses:
            category = keyword_responses[closest_match]
            return random.choice(RESPONSES[category])
    return "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz"

def predict_category(question):
    words = question.lower().split()
    for word in words:
        closest_match = get_closest_match(word)
        if closest_match and closest_match in keyword_responses:
            return keyword_responses[closest_match]
    question_vector = vectorizer.transform([question])
    return model.predict(question_vector)[0]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        message = request.form['message']
        chats.append({'username': session['username'], 'message': message})
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
        for keyword in keywords:
            if keyword in question:
                category = keyword_responses[keyword]
                response = random.choice(RESPONSES[category])
                return jsonify({"response": response})
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
