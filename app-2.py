from flask import Flask, request, jsonify, render_template
import joblib
import random

app = Flask(__name__)

# Load the trained machine learning model and the vectorizer during application startup
model = joblib.load("chatbot_2/svm_classifier.pkl")
vectorizer = joblib.load("chatbot_2/tfidf_vectorizer.pkl")

RESPONSES = {
    'Promotion': [
        "Promotion performans və staja əsaslanır. İnkişaf imkanları fərdi performans və şirkətin məqsədləri ilə uyğunluğa əsaslanır.",
        "Promotion performans və bacarıqlara əsaslanaraq qiymətləndirilir. İnkişaf imkanları performansınıza və bacarıqlərinizə görə mövcud ola bilər.",
        "Rəhbərlik, problem həll etmə və əməkdaşlarla əməkdaşlıq kimi bacarıqlar promosiyalar üçün dəyərlənir. Promotion prosesi performans qiymətləndirmələri, müsahibələr və rəhbərlik tərəfindən təsdiqlər daxil ola bilər.",
        "İnkişaf imkanları performansınıza və bacarıqlərinizə görə dəyişə bilər.",
        "Promotion vaxtı fərdi performans və təşkilati amillərə görə dəyişə bilər.",
        "Problem həll etmə və əməkdaşlıq kimi bacarıqlar promotion üçün dəyərlənir.",
        "Promotion üçün namizədlər performanslarına, potensiallarına və təşkilati məqsədlərlə uyğunluğuna görə müəyyən edilə bilər.",
        "Promotion prosesi performans qiymətləndirmələri, müsahibələr və rəhbərlik tərəfindən təsdiqlər daxil ola bilər.",
        "Promotion üçün hazır olmağı nümayiş etdirmək üçün daima gözləntiləri aşmaq, əlavə məsuliyyətləri götürmək və büyümə imkanları axtarmaq lazımdır.",
        "Promotion məqsədləri üçün performans, rəhbərlik bacarıqləri və şirkətin dəyərləri kimi mənbələrə əsaslanan performans ölçülməsi aparıla bilər.",
        "Promotion-un faydaları arasında məsuliyyət artımı, yüksək əmək haqqı və karyera imkanları olabilir.",
        "Promotion-un vaxtı fərdi performans, təşkilati ehtiyaclar və mövcud imkanlar əsasında dəyişə bilər.",
        "Yüksək performans göstərənlər promotion, bonuslarla mükafatlandırıla bilərlər.",
        "Karyera imkanları promotion və xüsusi təlim proqramlarından ibarət ola bilər.",
        "Əməkdaşlar karyera inkişafı üçün təlim proqramları, mentorluq, fərdi inkşaf modeli kimi dəstək proqramları ilə fayndalana bilərlər.",
    ],
    'Salary': [
        "Əmək haqqı iş rolü, təcrübə və bazar qiymətlərinə görə müəyyənləşdirilir. Bonuslar və ya təşviqatlar fərdi və şirkət performansına görə mövcud ola bilər.",
        "Əmək haqqı dəyişiklikləri illik olaraq və ya performans əsasında baş verə bilər. Əmək haqqı müzakirəsi bazar qiymətləri və sizin kifayət qədərliyiniz kimi müxtəlif amillərə görə mümkün ola bilər.",
        "Orta əmək haqqı yerləşmə, sənaye və təcrübə səviyyəsi kimi amillərə görə dəyişə bilər. İstifadə müqavilənizə bağlı olaraq, sığorta, pensiya planları və digər şəxsiyyətə görə əvəzlər kimi faydalar ola bilər.",
        "Əmək haqqı müzakirəsi bazar qiymətləri və sizin kifayət qədərliyiniz kimi müxtəlif amillərə görə mümkün ola bilər.",
        "İstifadə müqavilənizə bağlı olaraq, sığorta, pensiya planları və digər şəxsiyyətə görə əvəzlər kimi faydalar ola bilər.",
        "Orta əmək haqqı yerləşmə, sənaye və təcrübə səviyyəsi kimi amillərə görə dəyişə bilər.",
        "Əmək haqqınızla bağlı məsələləri rəhbərinizlə müzakirə edə və əgər lazımsızsa əmək haqqı rəyini müzakirə edə bilərsiniz.",
        "Əmək haqqı aralığı yerləşmə, sənaye və şirkətin ölçüsü kimi amillərə görə dəyişə bilər.",
        "Əmək haqqı həyat keyfiyyətinin artımı üçün müəyyən mənzillərdə fərqli olaraq müdrikləşmələr etmək üçün müvafiq olaraq hesablanıra.",
        "Siz ətrafında sığorta və ya pensiya şəxsiyyətinin müqaviləsindən olan bəzi hissələri, müzakirə edə və rəhbərinizlə razılaşmaq mümkündür.",
        "Əmək haqqı artımları performans, bazar trendləri və şirkətin mənfəətə görə müəyyən edilə bilər.",
        "Əgər performans baxışınızdan razı deyilsinizsə, narahatlıqlarınızı rəhbərinizlə müzakirə edə və həll etmək üçün əlavə məlumatlar təmin edə bilərsiniz.",
        "İllik əmək haqqı artımları şirkət performansı, bazar trendləri və fərdi performans kimi amillərə görə təyin oluna bilər.",
        "Bu rolda əmək haqqı artımı fərdi performans, təcrübə və şirkət siyasətlərinə görə dəyişə bilər.",
        "Əmək haqqından başqa, faydalar sağlık sığortası, pensiya planları, ödənilmiş iş vaxtı və digər əvəzlər kimi dəstəklər daxil ola bilər.",
        "Performans baxışlarına aid mübahisələr HR və ya şirkət siyasətinə bağlı olaraq daxilən HR və ya daxili şikayət prosesləri ilə həll edilə bilər.",
        "Uzaq işçilər üçün performans baxışları, köhnədici görüşlər, performans izləmə proqramları və menecerlərlə düzgün əlaqələrin təmin edilməsi ilə həyata keçirilə bilər.",
        "Əmək haqqı şəffaflığına dair şirkət siyasəti dəyişiklik göstərə bilər, lakin bəzi şirkətlər əmək haqqı aralığı və mükafat tərzləri haqqında şəffaflıq tətbiq edir.",
        "Əgər gözləntiləri aşmaq və ya vacib kilometr daşları əldə etmək kimi istənilən hallarda rəhbərinizlə performansə əsaslanan bonus haqqında müzakirə edə bilərsiniz.",
        "Bu bölmədəki əməkdaşlar üçün əmək haqqı artımı fərdi performans, iş səviyyəsi və şirkətin performansı kimi amillərə görə dəyişə bilər.",
    ],
    'Performance Review': [
        "Performans məqsədləri adətən rəhbərinizlə birgə müəyyən edilir və təşkilati məqsədlərlə uyğunlaşdırılır. Performans baxışında rəhbəriniz performansınızı qiymətləndirəcək, feedback verəcək və gələcəyə dair məqsədləri müzakirə edəcək.",
        "Mənfi feedback-u inkişaf və öyrənmə imkanı olaraq istifadə edin. Rəhbərinizlə iyşə iş yerində inkişaf etmək üçün sahələri müzakirə edin və onları həll etmək üçün bir plan yaradın. Əgər pis performans baxışı alırsınızsa, bunu inkişaf və yaxşılaşma imkanı kimi istifadə edin.",
        "Siz müzakirələrdə hansısa məsələləri müzakirə edə və nəzərə almaq üçün əlavə məzmun təqdim edə bilərsiniz.",
        "Performans baxışları adətən illik olaraq planlaşdırılır.",
        "Performans baxışında rəhbəriniz performansınızı qiymətləndirəcək, feedback verəcək və gələcəyə dair məqsədləri müzakirə edəcək.",
        "İnkişaf imkanları performansınıza və bacarıqlərinizə görə mövcud ola bilər.",
        "Feedback-u inkişaf və öyrənmə imkanı kimi istifadə edin.",
        "Performans məqsədləri adətən rəhbərinizlə birgə müəyyən edilir və təşkilati məqsədlərlə uyğunlaşdırılır.",
        "Əgər performans baxışınızı qaçırsınızsa, ən tez zamanda qayıdıb feedback alaraq və gələcəyə dair məqsədləri müzakirə edərək, feedback əldə etmək və məqsədlər qoymaq üçün əsas yaradın.",
        "Yüksək performans promouşn, bonuslar, mükafatlar və ya başqa tanınma forması vasitəsilə tanınaraq mükafatlandırıla bilər.",
        "Performans baxışında rəhbəriniz performansınızı qiymətləndirəcək, feedback verəcək və gələcəyə dair məqsədləri müzakirə edəcək.",
        "Əgər performans reytinqinizlə razılaşmırsınızsa, narahatlıqlarınızı rəhbərinizlə müzakirə edərək və öz məqamlarınızı dəstəkləmək üçün əlavə sübut təqdim edərək, məsələni müzakirə edə bilərsiniz.",
        "Promotion məqsədləri üçün performans, keyfiyyət və komanda işi kimi mənbələrə əsaslanan performans ölçülməsi aparıla bilər.",
        "Əgər mənfi feedback alırsınızsa, bunu inkişaf və yaxşılaşma imkanı kimi istifadə edin. Rəhbərinizləinkişaf sahələrini müzakirə edin və həll planı yaradın.",
        "Komanda üçün performans məqsədləri adətən departament və ya təşkilat məqsədləri ilə uyğunlaşdırılır və birgə müəyyən edilir.",
        "Əgər performans baxışınızdan razı deyilsinizsə, narahatlıqlarınızı rəhbərinizlə müzakirə edərək və həll etmək üçün əlavə məlumatlar təmin edə bilərsiniz.",
    ],
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

keywords = ['promotion', 'salary', 'performance', 'wage']

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
        greetings = ['necəsən', 'nə var', 'nə var nə yox']
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
