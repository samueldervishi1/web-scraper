
# Web Scraper - Reddit

This project is a Flask-based web scraper that fetches the top posts from various popular subreddits on Reddit. It uses the Reddit API to get the top posts and displays them on a webpage. The scraper retrieves a list of posts and allows the user to load more posts dynamically with a "Show More" button.

## Features

- **Top Posts Display**: Displays the top posts from multiple subreddits.
- **Dynamic Loading**: Fetches additional posts when the "Show More" button is clicked.
- **Caching**: Results are cached to reduce the number of API calls to Reddit and improve performance.
- **Rate Limiting**: There is a delay between successive requests to prevent overwhelming the Reddit API.

## Setup

### Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.10
- pip (Python package installer)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samueldervishi1/web-scraper.git
   cd web-scraper
   ```

2. **Create a Virtual Environment**:
   It is recommended to create a virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root of the project and add the following variables:
   ```
   CLIENT_ID=your_reddit_client_id
   CLIENT_SECRET=your_reddit_client_secret
   USER_AGENT=your_user_agent
   ```
   You can obtain your Reddit API credentials (CLIENT_ID, CLIENT_SECRET) from [Reddit's API](https://www.reddit.com/prefs/apps).

5. **Run the Application**:
   Start the Flask development server:
   ```bash
   python app.py
   ```
   The application will be accessible at [http://localhost:5001/scrap/reddit](http://localhost:5001).

## How It Works

- **Reddit API Authentication**: The `authenticate()` function sends a request to Reddit's API to obtain an access token using client credentials.
- **Fetching Top Posts**: The `get_top_posts()` function fetches the top posts from a given subreddit using the access token.
- **Threaded Scraping**: The `scrape_reddit()` function uses a `ThreadPoolExecutor` to scrape multiple subreddits concurrently, reducing the overall scraping time.
- **Dynamic Loading of Posts**: The front-end uses JavaScript to dynamically load more posts when the "Show More" button is clicked. It fetches the next set of posts from the backend without refreshing the page.

## Show More Button and Rate Limiting

The "Show More" button allows users to load additional posts dynamically. To prevent hitting the Reddit API too frequently, a caching mechanism is used with a default cache timeout of 10 minutes (600 seconds). This means the first time a user loads the posts, they will be fetched from the API, and subsequent requests within 10 minutes will use the cached data.

The delay between clicking the "Show More" button and fetching more posts is managed by the backend. This ensures that multiple rapid requests do not overload the Reddit API.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/MIT) file for details.
