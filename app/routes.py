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

        url = f"{SUGGESTION_URL + search_term}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        suggestions = []
        for i in range(len(data[1])):
            suggestion = {
                "name": data[1][i],
                "image": data[3][i],
                "description": get_description(data[1][i]),
            }
            suggestions.append(suggestion)
        
        return jsonify(suggestions)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})


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
            []
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_description(title):
    try:
        response = requests.get(f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('p').text.strip()
        return description
    except requests.exceptions.RequestException:
        return ""
