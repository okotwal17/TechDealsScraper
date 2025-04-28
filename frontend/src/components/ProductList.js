import React, { useState, useEffect } from 'react';
import ProductItem from './ProductItem';

const ProductList = ({ products }) => {
  const [sortedProducts, setSortedProducts] = useState([]);
  const [sortOption, setSortOption] = useState('price-asc');
  const [websiteFilter, setWebsiteFilter] = useState('all');
  
  // Initialize sortedProducts with products on mount and when products change
  useEffect(() => {
    if (products && products.length > 0) {
      setSortedProducts([...products]);
    }
  }, [products]);

  // Get unique websites from products
  const websites = ['all', ...new Set(products.map(product => product.website))];
  
  // Sort and filter products when products, sortOption, or websiteFilter changes
  useEffect(() => {
    if (!products || products.length === 0) {
      setSortedProducts([]);
      return;
    }
    
    let filtered = [...products];
    
    // Apply website filter
    if (websiteFilter !== 'all') {
      filtered = filtered.filter(product => product.website === websiteFilter);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      // Extract numeric price values - handle various formats
      const extractPrice = (priceStr) => {
        if (!priceStr) return 999999;
        
        // Remove currency symbols, commas, and any other non-numeric characters except decimal point
        const cleanPrice = priceStr.replace(/[^0-9.]/g, '');
        
        // Handle cases where there might be multiple decimal points
        const parts = cleanPrice.split('.');
        if (parts.length > 2) {
          // If there are multiple decimal points, join all but the last part
          return parseFloat(parts.slice(0, -1).join('') + '.' + parts.slice(-1));
        }
        
        return parseFloat(cleanPrice);
      };
      
      const priceA = extractPrice(a.price);
      const priceB = extractPrice(b.price);
      
      // Handle NaN values
      if (isNaN(priceA)) return 1;
      if (isNaN(priceB)) return -1;
      if (isNaN(priceA) && isNaN(priceB)) return 0;
      
      switch (sortOption) {
        case 'price-asc':
          return priceA - priceB;
        case 'price-desc':
          return priceB - priceA;
        case 'website':
          return a.website.localeCompare(b.website);
        default:
          return 0;
      }
    });
    
    setSortedProducts(filtered);
  }, [products, sortOption, websiteFilter]);
  
  const handleSortChange = (e) => {
    setSortOption(e.target.value);
  };
  
  const handleFilterChange = (e) => {
    setWebsiteFilter(e.target.value);
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2 className="results-title">
          Search Results 
          <span className="results-count">{products.length} products found</span>
        </h2>
        
        <div className="results-controls">
          <div className="control-group">
            <label htmlFor="website-filter">Filter by:</label>
            <select 
              id="website-filter" 
              value={websiteFilter} 
              onChange={handleFilterChange}
              className="select-control"
            >
              {websites.map(site => (
                <option key={site} value={site}>
                  {site === 'all' ? 'All Websites' : site}
                </option>
              ))}
            </select>
          </div>
          
          <div className="control-group">
            <label htmlFor="sort-options">Sort by:</label>
            <select 
              id="sort-options" 
              value={sortOption} 
              onChange={handleSortChange}
              className="select-control"
            >
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
              <option value="website">Website</option>
            </select>
          </div>
        </div>
      </div>
      
      {sortedProducts.length > 0 ? (
        <div className="product-list">
          {sortedProducts.map((product, index) => (
            <ProductItem key={`${product.website}-${index}`} product={product} />
          ))}
        </div>
      ) : (
        <div className="no-results">
          <p>No products match your filter criteria. Try changing your filters.</p>
        </div>
      )}
      
      <div className="results-footer">
        <p className="results-tip"><span role="img" aria-label="light bulb">💡</span> Tip: Click on a product card to see more details!</p>
      </div>
    </div>
  );
};

export default ProductList;