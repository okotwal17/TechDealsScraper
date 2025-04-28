import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import quote_plus

def scrape_newegg(query):
    """
    Scrape Newegg for products based on the search query.
    
    Args:
        query (str): The search query
        
    Returns:
        list: A list of dictionaries containing product information
    """
    products = []
    
    # If scraping fails, return some mock data for testing
    mock_data = [
        {
            'website': 'Newegg',
            'title': f'{query} - Gaming Laptop (Mock Data)',
            'price': '$1,199.99',
            'url': f'https://www.newegg.com/p/pl?d={quote_plus(query)}'
        },
        {
            'website': 'Newegg',
            'title': f'{query} - Desktop Computer (Mock Data)',
            'price': '$899.99',
            'url': f'https://www.newegg.com/p/pl?d={quote_plus(query)}'
        },
        {
            'website': 'Newegg',
            'title': f'{query} - Accessories Bundle (Mock Data)',
            'price': '$149.99',
            'url': f'https://www.newegg.com/p/pl?d={quote_plus(query)}'
        }
    ]
    
    try:
        # Format the search query for the URL
        formatted_query = quote_plus(query)
        url = f"https://www.newegg.com/p/pl?d={formatted_query}"
        
        # Add more realistic browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.newegg.com/',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'Cookie': 'NV%5FGPDR=0; NV%5FCONFIGURATION=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22w58%22%3A%221%22%7D%2C%22Exp%22%3A%2214400%22%7D%7D%7D'
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
                print(f"Newegg scraping attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:  # If not the last attempt
                    sleep_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print("All retry attempts failed. Using mock data.")
                    return mock_data
        
        # Find all product listings
        listings = soup.select('.item-cell')
        
        # Process each listing
        for listing in listings[:10]:  # Limit to first 10 results
            # Extract product title
            title_element = listing.select_one('.item-title')
            if not title_element:
                continue
            title = title_element.get_text(strip=True)
                
            # Extract product URL
            url_element = listing.select_one('a.item-title')
            if not url_element:
                continue
            product_url = url_element.get('href')
            
            # Extract product price
            price_element = listing.select_one('.price-current')
            if not price_element:
                continue
            
            # Newegg sometimes splits the price into dollars and cents
            price_dollars = price_element.select_one('strong')
            price_cents = price_element.select_one('sup')
            
            if price_dollars and price_cents:
                price_text = f"${price_dollars.get_text(strip=True)}.{price_cents.get_text(strip=True)}"
            else:
                price_text = price_element.get_text(strip=True).replace('–', '').strip()
                # If we couldn't extract the price properly, try to find it in the text
                if not any(c.isdigit() for c in price_text):
                    continue
            
            # Add the product to the list
            products.append({
                'website': 'Newegg',
                'title': title,
                'price': price_text,
                'url': product_url
            })
            
            # Add a small delay to avoid being blocked
            time.sleep(random.uniform(0.1, 0.3))
            
    except Exception as e:
        print(f"Error scraping Newegg: {e}")
        
    return products