import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import quote_plus

def scrape_bhphotovideo(query):
    """
    Scrape B&H Photo Video for products based on the search query.
    
    Args:
        query (str): The search query
        
    Returns:
        list: A list of dictionaries containing product information
    """
    products = []
    
    # If scraping fails, return some mock data for testing
    mock_data = [
        {
            'website': 'B&H Photo Video',
            'title': f'{query} - Professional Model (Mock Data)',
            'price': '$1,499.99',
            'url': f'https://www.bhphotovideo.com/c/search?q={quote_plus(query)}'
        },
        {
            'website': 'B&H Photo Video',
            'title': f'{query} - Standard Model (Mock Data)',
            'price': '$1,099.99',
            'url': f'https://www.bhphotovideo.com/c/search?q={quote_plus(query)}'
        },
        {
            'website': 'B&H Photo Video',
            'title': f'{query} - Budget Model (Mock Data)',
            'price': '$799.99',
            'url': f'https://www.bhphotovideo.com/c/search?q={quote_plus(query)}'
        }
    ]
    
    try:
        # Format the search query for the URL
        formatted_query = quote_plus(query)
        url = f"https://www.bhphotovideo.com/c/search?q={formatted_query}"
        
        # Add more realistic browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.bhphotovideo.com/',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'DNT': '1'
        }
        
        # Implement retry logic
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Make the request with a longer timeout
                response = requests.get(url, headers=headers, timeout=20)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, 'lxml')
                break  # If successful, break out of the retry loop
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                print(f"B&H Photo Video scraping attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:  # If not the last attempt
                    sleep_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print("All retry attempts failed. Using mock data.")
                    return mock_data
        
        # Find all product listings
        listings = soup.select('.productCard')
        
        # Process each listing
        for listing in listings[:10]:  # Limit to first 10 results
            # Extract product title
            title_element = listing.select_one('.productNameText')
            if not title_element:
                continue
            title = title_element.get_text(strip=True)
                
            # Extract product URL
            url_element = listing.select_one('a.productCard-link')
            if not url_element:
                continue
            product_url = 'https://www.bhphotovideo.com' + url_element.get('href')
            
            # Extract product price
            price_element = listing.select_one('.price_1DPoToKrLP8uWvruGqgtaY')
            if not price_element:
                # Try alternative price selector
                price_element = listing.select_one('.price')
                if not price_element:
                    continue
            
            price_text = price_element.get_text(strip=True)
            
            # Clean up price text
            if not any(c.isdigit() for c in price_text):
                continue
            
            # Add the product to the list
            products.append({
                'website': 'B&H Photo Video',
                'title': title,
                'price': price_text,
                'url': product_url
            })
            
            # Add a small delay to avoid being blocked
            time.sleep(random.uniform(0.1, 0.3))
            
    except Exception as e:
        print(f"Error scraping B&H Photo Video: {e}")
        
    return products