from flask import request, jsonify
from app import app
import requests
from bs4 import BeautifulSoup

@app.route('/')
def index():
    return "Welcome to the Wikipedia scraper app!"

@app.route('/scrape/<search_term>')
def scrape_wikipedia(search_term):
    try:
        if not search_term:
            return jsonify({'error': 'Invalid search term'}), 400
        
        wikipedia_api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={search_term}"
        response = requests.get(wikipedia_api_url)
        data = response.json()
        search_results = data['query']['search']
        
        scraped_data = [{'title': result['title'], 'snippet': result['snippet']} for result in search_results]
        return jsonify(scraped_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
