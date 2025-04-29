# Tech Deals Scraper

A full-stack application that lets users search for tech products and find the best prices across multiple websites (eBay, Newegg, and B&H Photo Video).

## Features

- Search for products across multiple e-commerce websites
- View product listings with prices, titles, and links
- Sort results by price
- Clean, responsive UI
- Loading spinner while results are being fetched
- Easily extensible backend for adding more websites

## Project Structure

```
tech-deals-scraper/
├── backend/               # Flask backend
│   ├── scrapers/          # Web scrapers for different websites
│   │   ├── __init__.py
│   │   ├── ebay.py        # eBay scraper
│   │   ├── newegg.py      # Newegg scraper
│   │   └── bhphotovideo.py # B&H Photo Video scraper
│   ├── app.py             # Main Flask application
│   └── requirements.txt   # Python dependencies
└── frontend/              # React frontend
    ├── public/            # Static files
    │   └── index.html     # HTML template
    ├── src/               # React source code
    │   ├── components/    # React components
    │   │   ├── SearchForm.js
    │   │   ├── ProductList.js
    │   │   ├── ProductItem.js
    │   │   └── LoadingSpinner.js
    │   ├── App.js         # Main React component
    │   ├── App.css        # App-specific styles
    │   ├── index.js       # React entry point
    │   └── index.css      # Global styles
    └── package.json       # Node.js dependencies
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14.0 or higher
- npm or yarn

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. If you plan to use Selenium for scraping JavaScript-heavy websites, you'll need to install the appropriate WebDriver for your browser. The code uses webdriver-manager to handle this automatically.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```
   or if you're using yarn:
   ```
   yarn install
   ```

## Running the Application

### Start the Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Start the Flask server:
   ```
   python app.py
   ```
   The backend will run on http://localhost:5000

### Start the Frontend


1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Start the React development server:
   ```
   npm start
   ```
   or if you're using yarn:
   ```
   yarn start
   ```
   The frontend will run on http://localhost:3000

## How to Use the App

1. Open your browser and navigate to http://localhost:3000
2. Enter a product name (e.g., "MacBook Pro", "RTX 3080", "Sony WH-1000XM4") in the search box
3. Click the "Search" button
4. Wait for the results to load (you'll see a loading spinner)
5. Browse through the product listings from different websites
6. Click "View Product" to open the product page in a new tab

## Adding New Website Scrapers

To add a new website scraper:

1. Create a new file in the `backend/scrapers` directory (e.g., `amazon.py`)
2. Implement a function that takes a search query and returns a list of products in the same format as the existing scrapers:
   ```python
   def scrape_amazon(query):
       # Scraping logic here
       return [
           {
               'website': 'Amazon',
               'title': 'Product Title',
               'price': '$999.99',
               'url': 'https://amazon.com/product-url'
           },
           # More products...
       ]
   ```
3. Import the new scraper in `backend/scrapers/__init__.py`
4. Add the new scraper to the ThreadPoolExecutor in `backend/app.py`

## Troubleshooting

- If you encounter CORS issues, make sure the Flask backend is running and the frontend is configured to proxy requests to the correct backend URL.
- If a website's structure changes, the scrapers may need to be updated to match the new HTML structure.
- Some websites may block scraping attempts. In such cases, you may need to implement more sophisticated scraping techniques or use a headless browser like Selenium.

- Link to Video on how it works: https://youtu.be/wuGeVZaVbPo

## License

This project is open source and available under the [MIT License](LICENSE).
