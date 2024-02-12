from flask import Flask, request, jsonify, render_template
import joblib
import random

app = Flask(__name__)

# Load the trained machine learning model and the vectorizer during application startup
model = joblib.load("chatbot_2/svm_classifier.pkl")
vectorizer = joblib.load("chatbot_2/tfidf_vectorizer.pkl")

RESPONSES = {
    'Əsas fəaliyyət göstəriciləri (KPİ)': [
        "KPİ-lər, əməkdaşların hər birinin vəzifələrinə uyğun olaraq təyin olunan məqsədlərə necə nail olduğunu qiymətləndirməyə kömək edir.",
        "ƏFG-lər, şirkətin əsas məqsədlərinə nail olmaq üçün hər bir əməkdaşın performansını izləmək üçün istifadə olunan rəsmi göstəricilərdir.",
        "KPİ-lər, əməkdaşların hər birinin iş performansını, məqsədlərə nail olmaqda necə yardım etdiklərini və işlərinin effektivliyini qiymətləndirmək üçün istifadə olunan müvafiq parametrlərdir.",
        "ƏFG-lər, əməkdaşların iş performansını, şirkətin əsas hədəflərinə uyğunluğunu və effektivliyini ölçmək üçün təyin olunan əsas göstəricilərdir.",
        "KPİ-lər, əməkdaşların iş performansını izləmək və şirkətin nailiyyətini ölçmək üçün istifadə olunan müəyyən məlumat və rəqəmlərdən ibarətdir.",
        "ƏFG-lər, əməkdaşların işdəki məhsuldarlığını və verimliliyini ölçmək üçün müəyyən edilmiş dəyərlərdən ibarətdir.",
        "KPİ-lər, əməkdaşların iş təcrübəsini, performansını və əməkdaşlığını qiymətləndirmək üçün təyin olunan standart göstəricilərdən ibarətdir.",
        "ƏFG-lər, əməkdaşların şirkətin əsas məqsədlərinə necə nail olduğunu izləmək üçün müəyyən edilmiş göstəricilərdir.",
        "KPİ-lər, əməkdaşların işdəki məhsuldarlığını ölçmək, işlərə necə yanaşdığını izləmək və şirkətin ümumi nailiyyətini qiymətləndirmək üçün istifadə olunan əsas məlumatlardır."
    ],
    'Kompetensiya': [
        "Kompetensiyalar hər hansı bir vəzifənin icrası üçün tələb olunan səriştələr toplusudur. Əməkdaşların hər hansı bir vəzifədə fəaliyyət göstərməsi və müvəffəqiyyətli olması üçün ehtiyac duyulan səriştələrdir.",
        "Kompetensiyalar, hər hansı bir vəzifənin icrası üçün tələb olunan səriştələr toplusudur və əməkdaşların müvəffəqiyyətli olması üçün vacibdir.",
        "Kompetensiyalar, əməkdaşların müvəffəqiyyətli iş icrası üçün tələb olunan səriştələr və bacarıqlər toplusudur.",
        "Kompetensiyalar, hər hansı bir vəzifənin icrası üçün tələb olunan səriştələr və bacarıqlər toplusudur.",
        "Kompetensiyalar, əməkdaşların müvəffəqiyyətli iş icrası üçün tələb olunan səriştələr və bacarıqlər toplusudur.",
        "Kompetensiyalar, əməkdaşların hər hansı bir vəzifədə müvəffəqiyyətli iş icrası üçün tələb olunan səriştələr və bacarıqlər toplusudur."
    ],
    'Yekun fəaliyyət balı': [
        "Yekun fəaliyyət balı, əməkdaşın ƏFG və kompetensiyalar üzrə yekun qiymətləndirmə nəticəsində formalaşan göstəricidir.",
        "Yekun fəaliyyət balı, əməkdaşın ƏFG və kompetensiyalar üzrə yekun qiymətləndirməsinin nəticəsində formalaşan bir göstəricidir."
    ],
    'Birbaşa rəhbər': [
        "Birbaşa rəhbər, əməkdaşın bilavasitə tabe olduğu ilkin rəhbərdir.",
        "Birbaşa rəhbər, əməkdaşın doğrudan tabe olduğu ilkin rəhbərdir.",
        "Birbaşa rəhbər, əməkdaşın ən yaxın rəhbəri, onun doğrudan tabe olduğu ilkin rəhbərdir.",
        "Birbaşa rəhbər, əməkdaşın doğrudan tabe olduğu ilkin rəhbərdir və onunla ən yaxın əlaqə saxlayan şəxsdir.",
        "Birbaşa rəhbər, əməkdaşın doğrudan tabe olduğu ilkin rəhbərdir və iş əlaqələrində ən yaxın şəxsdir.",
        "Birbaşa rəhbər, əməkdaşın doğrudan tabe olduğu ilkin rəhbərdir və işlə bağlı ən yaxın dəstək verən şəxsdir."
    ]
}

from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

app.secret_key = 'riyadmehdiyev'  # replace with your secret key

chats = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        message = request.form['message']
        chats.append({'username': session['username'], 'message': message})
    return render_template('index.html')

@app.route('/get_chats', methods=['GET'])
def get_chats():
    if 'username' not in session:
        return redirect(url_for('login'))
    return jsonify(chats)

def valid_login(username, password):
    # Replace with your actual login check
    return username == 'admin' and password == 'secret'

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

from fuzzywuzzy import process

keywords = ['rəhbər', 'birbaşa rəhbər', 'kpi', 'əfg', 'kompetensiya', 'yekun fəaliyyət balı']

def get_closest_match(input_word):
    closest_match = process.extractOne(input_word, keywords)
    return closest_match[0] if closest_match[1] > 80 else None

def check_keywords(question):
    words = question.lower().split()
    for word in words:
        closest_match = get_closest_match(word)
        if closest_match:
            return None
    return "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz"

def predict_category(question):
    # Transform the question into a vector
    question_vector = vectorizer.transform([question])

    # Predict the category of the user question using the loaded model
    return model.predict(question_vector)[0]

@app.route("/initial_message")
def initial_message():
    return jsonify({"initial_message": "Salam, sizə necə kömək göstərə bilərəm?"})

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Get the user question from the request
        question = request.json.get("question", "").lower()

        # Check if the question is a greeting
        greetings = ['hello', 'salam', 'hi']
        if question in greetings:
            return jsonify({"response": "Salam! Sizə necə kömək edim?"})

        # check if the question is a Necəsən
        greetings = ['necəsən', 'nə var', 'nə var nə yox','necəsən?']
        if question in greetings:
            return jsonify({"response": "Mən yaxşıyam, təşəkkürlər! Sizə necə kömək edə bilərəm?"})

        # Check if the question contains any of the keywords
        default_response = check_keywords(question)
        if default_response:
            return jsonify({"response": default_response})

        # Predict the category of the user question
        predicted_category = predict_category(question)

        # Get a random response for the predicted category
        response = random.choice(RESPONSES.get(predicted_category, ["Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz"]))

        # Return the response to the client
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message with status code 500 in case of exception
    
if __name__ == "__main__":
    app.run(debug=True)
