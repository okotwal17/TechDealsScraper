from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
import time

# Import scrapers
from scrapers.ebay import scrape_ebay
from scrapers.newegg import scrape_newegg
from scrapers.bhphotovideo import scrape_bhphotovideo

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/search', methods=['POST'])
def search():
    """
    Endpoint to search for products across multiple websites.
    Accepts a POST request with a JSON body containing a 'query' field.
    Returns a JSON list of products with website, title, price, and url.
    """
    # Get the search query from the request
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    query = data['query']
    
    # Use ThreadPoolExecutor to run scrapers in parallel
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit scraping tasks
        ebay_future = executor.submit(scrape_ebay, query)
        newegg_future = executor.submit(scrape_newegg, query)
        bhphoto_future = executor.submit(scrape_bhphotovideo, query)
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed([ebay_future, newegg_future, bhphoto_future]):
            try:
                result = future.result()
                results.extend(result)
            except Exception as e:
                print(f"Scraper error: {e}")
    
    # Sort results by price (assuming price is a float)
    results.sort(key=lambda x: float(x.get('price', '999999').replace('$', '').replace(',', '')) 
                 if x.get('price') and x.get('price').replace('$', '').replace(',', '').replace('.', '', 1).isdigit() 
                 else 999999)
    
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "timestamp": time.time()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)