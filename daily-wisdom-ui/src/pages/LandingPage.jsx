import React from 'react';
import WisdomCard from '../components/WisdomCard/WisdomCard';

function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-page__header">
        <h1>Daily Wisdom</h1>
        <p>Your daily dose of inspiration</p>
      </header>
      
      <main className="landing-page__main">
        <WisdomCard />
      </main>
      
      <footer className="landing-page__footer">
        <p>© 2026 Daily Wisdom. Spreading inspiration daily.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
