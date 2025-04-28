import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p className="mt-3">Searching across multiple websites for the best deals...</p>
    </div>
  );
};

export default LoadingSpinner;