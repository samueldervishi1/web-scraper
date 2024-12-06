from flask import Flask, render_template, jsonify
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT') #example: appName/1.0 by yourRedditUsername

auth_url = "https://www.reddit.com/api/v1/access_token"

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 600
cache = Cache(app)


def authenticate():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'User-Agent': USER_AGENT
    }
    response = requests.post(auth_url, auth=auth, data=data, headers=headers)
    token = response.json()['access_token']
    return token


def get_top_posts(subreddit, limit=5):
    token = authenticate()
    url = f'https://oauth.reddit.com/r/{subreddit}/top?limit={limit}'
    headers = {
        'Authorization': f'bearer {token}',
        'User-Agent': USER_AGENT
    }
    response = requests.get(url, headers=headers)
    posts = response.json()['data']['children']
    return posts


def scrape_reddit():
    subreddits = [
        "learnpython", "Python", "dataisbeautiful", "programming", "technology",
        "worldnews", "news", "movies", "science", "gaming", "askreddit",
        "aww", "funny", "memes", "todayilearned", "humor", "Showerthoughts",
        "formula1", "apple", "samsung", "java", "football", "soccer", "nba",
        "cryptocurrency", "stocks", "art", "photography", "music", "history",
        "space", "politics", "travel", "food", "fitness", "health", "books",
        "technologynews", "startup", "entrepreneur", "business"
    ]

    all_posts = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_subreddit, subreddit) for subreddit in subreddits]
        for future in futures:
            all_posts.extend(future.result())

    return all_posts


def process_subreddit(subreddit):
    posts = get_top_posts(subreddit)
    return [{
        'subreddit': subreddit,
        'title': post['data']['title'],
        'url': post['data']['url'],
        'score': post['data']['score']
    } for post in posts]


@app.route('/scrap/reddit')
@cache.cached(timeout=600)
def home():
    all_posts = scrape_reddit()
    return render_template('index.html', data=all_posts[:5])


@app.route('/load_more/<int:start>')
@cache.cached(timeout=600)
def load_more(start):
    all_posts = scrape_reddit()
    return jsonify(all_posts[start:start + 5])


if __name__ == '__main__':
    app.run(port=5001, debug=True)