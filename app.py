from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# 🔑 Replace with your own News API key
API_KEY = "YOUR_NEWS_API_KEY"

NEWS_URL = "https://newsapi.org/v2/everything"

def get_accident_news():
    params = {
        "q": "road accident OR traffic accident OR vehicle crash",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(NEWS_URL, params=params)
    data = response.json()

    articles = []

    if "articles" in data:
        for news in data["articles"][:10]:
            articles.append({
                "title": news["title"],
                "source": news["source"]["name"],
                "url": news["url"],
                "published": news["publishedAt"]
            })

    return articles


@app.route("/")
def home():
    news = get_accident_news()
    return render_template("index.html", news=news)


@app.route("/api/accidents")
def api_accidents():
    return jsonify(get_accident_news())


if __name__ == "__main__":
    app.run(debug=True)
