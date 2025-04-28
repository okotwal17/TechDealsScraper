import React, { useState, useEffect } from 'react';

const SearchForm = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [placeholderIndex, setPlaceholderIndex] = useState(0);

  // Example product suggestions that rotate in the placeholder
  const placeholders = [
    "MacBook Pro",
    "RTX 3080",
    "Sony WH-1000XM4",
    "iPhone 15 Pro",
    "Samsung Galaxy S23",
    "iPad Air",
    "Nintendo Switch",
    "LG OLED TV"
  ];

  // Rotate through placeholder suggestions
  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholderIndex((prevIndex) => (prevIndex + 1) % placeholders.length);
    }, 3000);
    
    return () => clearInterval(interval);
  }, [placeholders.length]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
      // Keep the query in the input after search
    }
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    setIsTyping(true);
    // Reset typing state after a delay
    setTimeout(() => setIsTyping(false), 1000);
  };

  return (
    <div className="search-form">
      <h2 className="search-title">Find the Best Tech Deals</h2>
      <p className="search-subtitle">Compare prices across eBay, Newegg, and B&H Photo Video</p>
      
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          <div className="col-md-10">
            <div className="input-wrapper">
              <input
                type="text"
                className={`form-control form-control-lg ${isTyping ? 'is-typing' : ''}`}
                placeholder={`Try searching for ${placeholders[placeholderIndex]}...`}
                value={query}
                onChange={handleInputChange}
                aria-label="Search query"
                required
              />
              <span className="search-icon"><span role="img" aria-label="magnifying glass">🔍</span></span>
            </div>
          </div>
          <div className="col-md-2">
            <button type="submit" className="btn btn-primary btn-lg w-100">
              <span className="button-text">Search</span>
              <span className="button-icon"><span role="img" aria-label="rocket">🚀</span></span>
            </button>
          </div>
        </div>
      </form>
      
      <div className="popular-searches">
        <span className="popular-label">Popular searches:</span>
        {placeholders.slice(0, 4).map((item, index) => (
          <button 
            key={index}
            className="popular-item"
            onClick={() => {
              setQuery(item);
              onSearch(item);
            }}
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SearchForm;