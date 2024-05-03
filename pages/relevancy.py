import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PyPDF2 import PdfReader
st.write("""
# Job Relevancy 
""")

label = "Job Description"

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token) > 1]
    return tokens

def extract_text_from_pdf(cv_pdf):
    text = ""
    pdf_reader = PdfReader(cv_pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_similarity_score(job_description, cv_text):
    vectorizer = TfidfVectorizer(tokenizer=preprocess_text)
    job_description = vectorizer.fit_transform([job_description])
    cv_text = vectorizer.transform([cv_text])
    cosine_sim = cosine_similarity(job_description, cv_text)
    return cosine_sim[0][0]
def extract_keywords(text):
    tokens = preprocess_text(text)
    # keywords = preprocess_text(tokens)
    return tokens
job_description = st.text_area(label, value="", height=None, max_chars=20000, key=None, placeholder="Enter Your Job Descripttion Here")

cv_pdf = st.file_uploader('Pick Your Resume....')

submitButton = st.button("Submit", type="primary")

if submitButton:
    cv_text = extract_text_from_pdf(cv_pdf)
    relevancy_score = get_similarity_score(job_description, cv_text)
    st.write("Relevancy Score:", relevancy_score * 100)

    st.write("Common Keywords:")
    job_keywords = extract_keywords(job_description)
    cv_keywords = extract_keywords(cv_text)
    common_keywords = set(job_keywords).intersection(set(cv_keywords))
    # st.write(common_keywords)

    keyword_counts = {}
    for keyword in common_keywords:
        keyword_counts[keyword] = job_keywords.count(keyword) + cv_keywords.count(keyword)

    fig, ax = plt.subplots()
    ax.bar(keyword_counts.keys(), keyword_counts.values())
    plt.xticks(rotation=45)
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Common Keywords')
    total_keywords = len(job_keywords) + len(cv_keywords)
    keywords_text = ' '.join(common_keywords)

    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    # st.pyplot(fig)
    top_n = 10  
    top_keywords = dict(sorted_keywords[:top_n])

    total_keywords = sum(top_keywords.values())

    keyword_percentages = {keyword: (count / total_keywords) * 100 for keyword, count in top_keywords.items()}

    fig2, ax = plt.subplots()
    ax.pie(keyword_percentages.values(), labels=keyword_percentages.keys(), autopct='%1.1f%%')
    ax.set_title('Top {} Common Keywords'.format(top_n))
    st.pyplot(fig2)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords_text)

    fig3, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title('Common Keywords Word Cloud')
    ax.axis('off')
    st.pyplot(fig3)
   
    

    
   