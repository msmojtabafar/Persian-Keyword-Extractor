from flask import Flask, render_template, request
import re
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

stopwords = set([
    "و", "در", "به", "از", "که", "برای", "با", "را", "این", "آن",
    "اما", "یا", "یک", "هم", "تا", "بر", "بود", "نیز", "شود",
    "کرد", "کند", "می", "بر", "بین", "شد", "است", "های", "باشد"
])

def simple_tokenizer(text):
    words = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
    return [w for w in words.split() if w not in stopwords and len(w) > 2]

def extract_keywords_tfidf(texts, num_keywords=5):
    vectorizer = TfidfVectorizer(tokenizer=simple_tokenizer)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    corpus_scores = tfidf_matrix.mean(axis=0).A1
    sorted_indices = corpus_scores.argsort()[::-1]
    corpus_keywords = [(feature_names[i], corpus_scores[i]) for i in sorted_indices[:num_keywords]]

    keywords_per_text = []
    for row in tfidf_matrix:
        scores = row.toarray()[0]
        sorted_idx = scores.argsort()[::-1]
        keywords = [(feature_names[i], scores[i]) for i in sorted_idx[:num_keywords]]
        keywords_per_text.append(keywords)

    return corpus_keywords, keywords_per_text

def split_sentences(text):
    sentences = re.split(r'[.!؟\n]', text)
    return [s.strip() for s in sentences if s.strip()]

def rake_keyword_extraction(text, min_char_length=2, min_keyword_freq=1):
    sentences = split_sentences(text)
    phrase_list = []

    for sentence in sentences:
        words = re.split(r'\W+', sentence)
        phrase = []
        for word in words:
            w = word.strip()
            if w and w not in stopwords:
                phrase.append(w)
            else:
                if phrase:
                    phrase_list.append(' '.join(phrase))
                    phrase = []
        if phrase:
            phrase_list.append(' '.join(phrase))

    freq = {}
    for phrase in phrase_list:
        if len(phrase) >= min_char_length:
            freq[phrase] = freq.get(phrase, 0) + 1

    keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [k for k in keywords if k[1] >= min_keyword_freq]

    return keywords

@app.route('/', methods=['GET', 'POST'])
def index():
    input_texts = ""
    method = "tfidf" 
    corpus_keywords = []
    per_text_keywords = []
    num_keywords = 5 

    if request.method == 'POST':
        input_texts = request.form.get('texts', '')
        method = request.form.get('method', 'tfidf')
        num_keywords_str = request.form.get('count', '5')
        try:
            num_keywords = int(num_keywords_str)
            if num_keywords < 1:
                num_keywords = 5
        except ValueError:
            num_keywords = 5

        texts = [t.strip() for t in input_texts.split('\n') if t.strip()]

        if texts:
            if method == 'tfidf':
                corpus_keywords, per_text_keywords = extract_keywords_tfidf(texts, num_keywords=num_keywords)
            elif method == 'rake':
                per_text_keywords = []
                for t in texts:
                    kws = rake_keyword_extraction(t)
                    kws = kws[:num_keywords]
                    per_text_keywords.append(kws)
                corpus_keywords = []

    return render_template('index.html',
                           input_texts=input_texts,
                           method=method,
                           corpus_keywords=corpus_keywords,
                           per_text_keywords=per_text_keywords,
                           num_keywords=num_keywords,
                           enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
