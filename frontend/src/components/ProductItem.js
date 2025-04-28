import React, { useState } from 'react';

const ProductItem = ({ product }) => {
  const { title, price, website, url } = product;
  const [isHovered, setIsHovered] = useState(false);

  // Generate a random accent color for the website tag
  const getWebsiteColor = () => {
    const websites = {
      'eBay': { bg: 'linear-gradient(45deg, #e53935, #e35d5b)', icon: '🛒' },
      'Newegg': { bg: 'linear-gradient(45deg, #ff7e5f, #feb47b)', icon: '💻' },
      'B&H Photo Video': { bg: 'linear-gradient(45deg, #5433ff, #20bdff)', icon: '📷' }
    };
    
    return websites[website] || { bg: 'linear-gradient(45deg, var(--accent-color), var(--secondary-color))', icon: '🔍' };
  };

  const websiteStyle = {
    background: getWebsiteColor().bg
  };

  return (
    <div 
      className="product-card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <span className="product-website" style={websiteStyle}>
        {getWebsiteColor().icon} {website}
      </span>
      <h3 className="product-title">{title}</h3>
      <div className="product-price">
        {price}
        {isHovered && <span className="price-tag">Best Deal!</span>}
      </div>
      <a 
        href={url} 
        className="product-link" 
        target="_blank" 
        rel="noopener noreferrer"
      >
        View Product {isHovered ? '🚀' : '→'}
      </a>
    </div>
  );
};

export default ProductItem;