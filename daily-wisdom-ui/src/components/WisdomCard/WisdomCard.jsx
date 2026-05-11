import React, { useState } from 'react';
import { useWisdom } from '../../hooks/useWisdom';
import './WisdomCard.css';

function WisdomCard() {
  const { data: wisdom, isLoading, error, refetch } = useWisdom();
  const [copySuccess, setCopySuccess] = useState(false);
  
  const handleCopy = async () => {
    if (!wisdom) return;
    
    try {
      await navigator.clipboard.writeText(`${wisdom.title}\n\n${wisdom.description}`);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = `${wisdom.title}\n\n${wisdom.description}`;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };
  
  if (isLoading) {
    return (
      <div className="wisdom-card wisdom-card--loading">
        <div className="wisdom-card__skeleton">
          <div className="wisdom-card__skeleton-title"></div>
          <div className="wisdom-card__skeleton-description"></div>
          <div className="wisdom-card__skeleton-button"></div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="wisdom-card wisdom-card--error">
        <div className="wisdom-card__error">
          <h3>Wisdom Unavailable</h3>
          <p>{error.message}</p>
          <button onClick={refetch} className="wisdom-card__retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }
  
  if (!wisdom) {
    return (
      <div className="wisdom-card wisdom-card--empty">
        <div className="wisdom-card__empty">
          <h3>No Wisdom Today</h3>
          <p>Check back later for today's wisdom!</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="wisdom-card">
      <div className="wisdom-card__content">
        <h2 className="wisdom-card__title">{wisdom.title}</h2>
        <p className="wisdom-card__description">{wisdom.description}</p>
      </div>
      <div className="wisdom-card__actions">
        <button 
          onClick={handleCopy}
          className={`wisdom-card__copy-button ${copySuccess ? 'wisdom-card__copy-button--success' : ''}`}
        >
          {copySuccess ? 'Copied!' : 'Copy Wisdom'}
        </button>
      </div>
    </div>
  );
}

export default WisdomCard;
