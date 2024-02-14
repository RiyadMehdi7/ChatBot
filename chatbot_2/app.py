from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import joblib
import random
from fuzzywuzzy import process
from Levenshtein import ratio

app = Flask(__name__)
app.secret_key = 'riyadmehdiyev'

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
    ],
    'Kim tərəfindən təyin olunur': [""" - Direktor/ şöbə rəisi: İdarə Heyəti (Maliyyə menecmenti departamentinin təklifi ilə)
                                    - Direktor müavini: Struktur bölmə rəhbəri (Əlavə ƏFG təyin olunmadığı təqdirdə direktorun ƏFG-na bərabər götürülür)
                                    - Menecer/ baş mütəxəssis/ bölmə rəhbəri/ qrup rəhbəri (aylıq/rüblük mükafat alan əməkdaşlar istisna edilməklə): Struktur bölmə rəhbəri/n
                                    - Struktur bölmə rəhbəri: Şöbədə çalışan digər əməkdaşlar Çalışdığı strukturun ƏFG və hədəflərinə bərabər götürülür"""],
    'Rotasiya halında ƏFG': ["Ənənəvi iş metodu ilə çalışan əməkdaşlar, onların bankdakı iş stajına uyğun olaraq il ərzində 50%-dən çox hansı struktur bölmədə çalışıbsa, həmin strukturun yekun əsas fəaliyyət göstəriciləri və fərdi əsas fəaliyyət göstəriciləri (əgər varsa) nəzərə alınır."]
    
}


chats = []

model = joblib.load("chatbot_2/svm_classifier.pkl")
vectorizer = joblib.load("chatbot_2/tfidf_vectorizer.pkl")

keywords = ['rəhbər', 'birbaşa rəhbər', 'kpi', 'əfg', 'kompetensiya', 'yekun fəaliyyət balı', 'rotasiya']

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

def valid_login(username, password):
    return username == 'admin' and password == 'secret'

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/initial_message")
def initial_message():
    return jsonify({"initial_message": "Salam, sizə necə kömək göstərə bilərəm?"})

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
        response = random.choice(RESPONSES.get(predicted_category, ["Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz"]))
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
