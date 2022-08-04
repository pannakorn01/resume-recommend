import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, redirect, url_for, session ,flash
import pickle
from PIL import Image
import pytesseract
import re
from nltk.tokenize import TweetTokenizer
from PyPDF2 import PdfFileReader
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
import pytesseract
# import logging


app = Flask(__name__)
app.secret_key = 'your secret key'
# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)

@app.route("/")
def HomePage():
    return render_template('index.html')

# OCR_PDF_File
def ocr_pdf(filename):
    text = PyPDF2.PdfFileReader(filename)
    text2 = text.getPage(0)
    text3 = text2.extractText()
    return text3
#  End OCR_PDF_File

#stopwords_english
stopwords_english = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz",'000',]
# functions text cleaning & stopwords_english & tokenizer
def process_text(text):
    text2 = re.sub('https:\/\/.*[\r\n]*','', text)
    text3 = re.sub(r'[^\w\s]','', text2)
    text4 = re.sub('#S+', '', text3)  
    text5 = re.sub('@S+', '  ', text4)  
    text6 = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), ' ', text5)  
    text7 = re.sub(r'[^\x00-\x7F]',r' ', text6) 
    text8 = re.sub('[0-9]+','',text7)
    tokenizer = TweetTokenizer()
    text_mots = tokenizer.tokenize(text8)
    text_mots_lower = [word.lower() for word in text_mots]
    text_clean = [word for word in text_mots_lower if (word not in stopwords_english and len(word)>2)]
    return ' '.join(text_clean)


def classify(utt):
   # เรียกใช้ fuction tf-idf
    loaded_vectorizer = pickle.load(open('models/Vectorizer.pickle', 'rb'))
    # เรียกใช้ Model
    loaded_model = pickle.load(open("models/mlp.pkl", "rb"))
    # นำคำตอบเข้าไปประมวลผลโมเดล
    p = loaded_model.predict(loaded_vectorizer.transform([utt]))
    return ' '.join(p)

def job_api(data):
    skill = data
    jobthai = "https://www.jobthai.com"
    html_text = requests.get('https://www.jobthai.com/th/jobs?keyword='+skill)
    soup = BeautifulSoup(html_text.content,'lxml')
    company_ = []
    skills_ = []
    salary_ = []
    workplace_ = []
    link_ = []
    img_ = []
    icons_ = []
    money_ = []
    date_ = []
    jobthai = "https://www.jobthai.com"
    moneys = soup.find_all('div',class_ = 'msklqa-7 iiPXgT', limit=1)
    jobs = soup.find_all('div',class_ = 'ant-row msklqa-8 hQCzHL')
    imgs = soup.find_all('div',class_ = 'ant-col ant-col-xs-0 ant-col-sm-0 ant-col-md-6 ant-col-lg-6 ant-col-xl-6')
    for el in soup.find_all('h2',class_ = 'ohgq7e-0 gWWIiL'):
        data_company = el.get_text()
        company_.append(data_company)
    for el2 in soup.find_all('h2',class_='ohgq7e-0 frNqfE'):
        data_skills = el2.get_text()
        skills_.append(data_skills)
    for el3 in soup.find_all('span',class_='ohgq7e-0 msklqa-5 gfpnRh', id="salary-text"):
        data_salary = el3.get_text()
        salary_.append(data_salary)
    for el4 in soup.find_all('h3',class_='ohgq7e-0 ijtKqG'):
        data_workplace = el4.get_text()
        workplace_.append(data_workplace)
    for job in jobs:
        link = job.a['href']
        links = jobthai+link
        link_.append(links)
    for img_w in imgs:
        data_imgs = img_w.picture.source['srcset']
        img_.append(data_imgs)
    for icon in jobs:
        icons = icon.img['src']
        data_icon = jobthai+icons
        icons_.append(data_icon)
    for money in moneys:
        money_link = money.img['src']
        data_money = jobthai + money_link
        money_.append(data_money)
    for dates in soup.find_all('span',class_='ohgq7e-0 msklqa-6 itKEax'):
        data_date = dates.get_text()
        date_.append(data_date)
    return company_, skills_, salary_, workplace_, link_ ,img_ , icons_ ,money_ ,date_


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    msg_empty = '* กรุณาอัพโหลดไฟล์ .pdf *'
    job_title = 'ตำแหน่งงานที่ระบบแนะนำสำหรับคุณ : '
    company = 'บริษัทที่เปิดรับตำแหน่งงานของคุณ'
    if request.method == 'POST':
        if 'resumefile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resumefile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            resume_path = "./resume/" + file.filename      
            file.save(resume_path)
            # resume_path = file.read()   
            resume = ocr_pdf(resume_path)
            resume_process = process_text(resume)
            resume_model = classify(resume_process)
            data = job_api(resume_model)      
            return render_template('index.html',data = data , skill = resume_model,job_title = job_title,company=company)
    return render_template('index.html',msg_empty = msg_empty)

# Code Run Port
if __name__ == "__main__":        
    app.run(debug=True)
