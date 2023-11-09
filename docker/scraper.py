# scraper.py

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_google():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter missing."})

    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Your User Agent Here",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/url?q='):
                results.append({"url": href[7:], "source": "Google"})

        return jsonify({"results": results})
    else:
        return jsonify({"error": "Failed to retrieve search results."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
