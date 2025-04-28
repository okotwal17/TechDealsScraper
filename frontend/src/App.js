import React, { useState } from 'react';
import axios from 'axios';
import SearchForm from './components/SearchForm';
import ProductList from './components/ProductList';
import LoadingSpinner from './components/LoadingSpinner';
import './App.css';

function App() {
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    
    try {
      const response = await axios.post('/search', { query });
      setSearchResults(response.data);
    } catch (err) {
      console.error('Error searching for products:', err);
      setError('Failed to fetch results. Please try again later.');
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1 className="app-title">Tech Deals Scraper</h1>
          <p>Find the best prices for tech products across multiple websites</p>
        </div>
      </header>
      
      <main className="container">
        <SearchForm onSearch={handleSearch} />
        
        {isLoading ? (
          <LoadingSpinner />
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        ) : hasSearched && searchResults.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No products found. Try a different search term.
          </div>
        ) : (
          <ProductList products={searchResults} />
        )}
      </main>
      
      <footer className="container mt-5 text-center text-muted">
        <p>© 2025 Tech Deals Scraper - Prices from eBay, Newegg, and B&H Photo Video</p>
      </footer>
    </div>
  );
}

export default App;