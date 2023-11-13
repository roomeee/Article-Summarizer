from flask import Flask, render_template, request
import requests


app = Flask(__name__)

import os
api_key = os.getenv("API_KEY")

def get_article_summary(article_url, summary_length=3):
    url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize"

    querystring = {
        "url": article_url,
        "length": str(summary_length)
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get('summary')  # Extract the 'summary' key
    else:
        return f"Error: {response.status_code} - {response.text}"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        article_url = request.form['article_url']
        summary_length = int(request.form['summary_length'])

        summary = get_article_summary(article_url, summary_length)
        return render_template('index.html', article_url=article_url, summary_length=summary_length, summary=summary)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
