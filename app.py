import streamlit as st
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
import sklearn
nltk.downlord("punkt")


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

st.title("SMS Spam Dectector")

input_text = st.text_area("enter the message to detect")

if st.button("Analyse"):
    processed_text=text_transform(input_text)

    vectorized_text=tfidf.transform([processed_text])

    solution=model.predict(vectorized_text)[0]

    if solution==1:
        st.header("This message is SPAM")
    else:
        st.header("This message is NOT-SPAM")
