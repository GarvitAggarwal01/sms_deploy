import streamlit as st
import pickle
import string
import nltk
nltk.download("punkt")
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
import sklearn
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_main = load_lottieurl("https://lottie.host/bc9cf743-e3b3-4cde-a34a-c8aca6a2fe09/xo91NWpTfe.json")
lottie_spam = load_lottieurl("https://lottie.host/fbf24f9f-0914-4409-acc6-d0770ff3cc91/XenJUhUC0q.json")
lottie_not = load_lottieurl("https://lottie.host/060e922f-a915-4d06-861a-bb7eaa4bdd8f/ssO0x6GqDL.json")

def text_transform(text):
    text = text.lower()  # converterd  to lower case
    text = nltk.word_tokenize(text)  # tokenized text

    y = []
    for i in text:
        if i.isalnum():  # only alpha numeric
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words("english") and i not in string.punctuation:  # only non stopwords and punctuations
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open("vectorizer.pkl","rb"))
model = pickle.load(open("model.pkl","rb"))

st.set_page_config(page_title="Spam_dectector",page_icon=":envelope:")

st_lottie(lottie_main,height=200)

st.title("SMS Spam Dectector")

input_text = st.text_area("enter the message to detect")

if st.button("Analyse"):
    processed_text=text_transform(input_text)

    vectorized_text=tfidf.transform([processed_text])

    solution=model.predict(vectorized_text)[0]

    if solution==1:
        left_column,right_column=st.columns(2)
        with left_column:
            st.header("This message is SPAM")
        with right_column:
            st_lottie(lottie_spam,height=100)
    else:
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("This message is GENUINE")
        with right_column:
            st_lottie(lottie_not, height=130)
