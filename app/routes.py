from flask import request, jsonify
from app import app
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

SUGGESTION_URL = os.getenv("SUGGESTION_URL")
WIKIPEDIA_URL = os.getenv("WIKIPEDIA_URL")

@app.route('/')
def index():
    return "Welcome to the Wikipedia scraper app!"

@app.route('/suggestion/<search_term>')
def suggetion_wikipedia(search_term):
    try:
        if not search_term:
            return jsonify({'error': 'Invalid search term'}), 400
        wikipedia_api_url = f"{SUGGESTION_URL + search_term}"
        response = requests.get(wikipedia_api_url)
        data = response.json()
        search_results = data['query']['search']
        
        scraped_data = [{'title': result['title'], 'snippet': result['snippet']} for result in search_results]
        print("here : ",scraped_data)
        return jsonify(scraped_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/scrape/<search_term>')
def scrape_wikipedia(search_term):
    try:
        if not search_term:
            return jsonify({'error': 'Invalid search term'}), 400
        
        wikipedia_api_url = f"{WIKIPEDIA_URL + search_term}"
        response = requests.get(wikipedia_api_url)
        temp = BeautifulSoup(response.text,"html.parser")

        for paragraph in temp.select("p"):
            print("hello",paragraph.getText())
        
        return jsonify(
            "hi"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
