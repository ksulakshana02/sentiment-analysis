from flask import Flask, render_template, request, redirect
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info('Flask server started')

data = dict()
reviews = []
positive = 0
negative = 0

@app.route("/")
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative
    return render_template('index.html', data=data)


@app.route("/", methods=["POST"])
def my_post():
    text = request.form['text']
    logging.info(f'Text: {text}')

    preprocessed_text = preprocessing(text)
    logging.info(f'preprocessed: {preprocessed_text}')

    vectorized_text = vectorizer(preprocessed_text)
    logging.info(f'vectorized: {vectorized_text}')

    prediction = get_prediction(vectorized_text)
    logging.info(f'prediction: {prediction}')

    if prediction == 'negative':
        global negative
        negative += 1
    else:
        global positive
        positive += 1
    
    reviews.insert(0,text)
    return redirect(request.url)

if __name__ == "__main__":
    app.run()

