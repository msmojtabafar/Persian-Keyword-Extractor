# Persian Keyword Extractor 📝✨

A simple and efficient web application built with **Flask** for extracting keywords from Persian texts.  
This project supports two popular keyword extraction methods: **TF-IDF** and **RAKE**.

---

## Features 🚀
- Extract keywords from one or multiple Persian texts  
- Choose between TF-IDF and RAKE algorithms  
- Display both overall corpus keywords and keywords for each individual text  
- Clean, user-friendly web interface with full RTL support for Persian language  
- Customize the number of keywords to extract  

---

## How It Works ⚙️

### 1. TF-IDF (Term Frequency - Inverse Document Frequency)  
This method calculates the importance of each word based on its frequency in a document and its rarity across the entire corpus.

Formulas:  

- **Term Frequency (TF):**  
\[
TF(t,d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t',d}}
\]  
where \(f_{t,d}\) is the number of times term \(t\) appears in document \(d\).

- **Inverse Document Frequency (IDF):**  
\[
IDF(t, D) = \log \frac{N}{|\{d \in D : t \in d\}|}
\]  
where:  
- \(N\) is the total number of documents in the corpus  
- \(|\{d \in D : t \in d\}|\) is the number of documents where term \(t\) appears

- **TF-IDF Score:**  
\[
TFIDF(t,d,D) = TF(t,d) \times IDF(t,D)
\]

---

### 2. RAKE (Rapid Automatic Keyword Extraction)  
RAKE extracts candidate keyword phrases by analyzing word co-occurrences and stopwords in the text.

The key steps are:  
- Split the text into candidate phrases based on stopwords  
- Calculate the **degree** of each word as the total number of co-occurrences with other words  
- Calculate the **frequency** of each word in the candidate phrases  
- Compute the score of each word:  
\[
score(w) = \frac{degree(w)}{frequency(w)}
\]  
- Assign each candidate phrase a score equal to the sum of scores of its words  

---

## Usage 💻

1. Clone this repository:  
```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create and activate a Python virtual environment:  
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS  
venv\Scripts\activate      # Windows  
```

3. Install dependencies:  
```bash
pip install -r requirements.txt
```

4. Run the application:  
```bash
python main.py
```

5. Open your browser and visit:  
```
http://127.0.0.1:5000
```

6. Paste your Persian text(s), select the extraction method, and get keywords instantly!

---

## Requirements 📋
- Python 3.7+  
- Flask  
- scikit-learn  

---

## License 📄  
This project is licensed under the **MIT License**.

---

## Feedback & Contributions 🤝  
Feel free to open issues or submit pull requests. Your feedback and contributions are highly welcome!

---

> **Note:** The texts are preprocessed by removing Persian stopwords and punctuation to improve keyword extraction accuracy.
