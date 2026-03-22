import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API = 'http://127.0.0.1:8000';

// ── Star Rating Component ──────────────────────────────
function StarRating({ rating }) {
  return (
    <div className="stars">
      {[1,2,3,4,5].map(star => (
        <span key={star} className={star <= Math.round(rating) ? 'star filled' : 'star'}>★</span>
      ))}
      <span className="rating-num">({rating})</span>
    </div>
  );
}

// ── Product Card Component ─────────────────────────────
function ProductCard({ item, type }) {
  const [added, setAdded] = useState(false);

  const handleAddToCart = () => {
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  return (
    <div className="product-card">
      {/* Rank Badge */}
      <div className="rank-badge">#{item.rank}</div>

      {/* Product Image */}
      <div className="product-image-container">
        <img
          src={item.image}
          alt={item.name}
          className="product-image"
          onError={e => e.target.src='https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=400'}
        />
      </div>

      {/* Product Info */}
      <div className="product-info">
        <span className="product-category">{item.category}</span>
        <h3 className="product-name">{item.name}</h3>
        <span className="product-brand">{item.brand}</span>
        <StarRating rating={item.rating} />
        <p className="product-description">{item.description}</p>

        {/* Score Badges */}
        <div className="score-badges">
          {type === 'popular' && (
            <span className="badge green">🏆 Score: {item.score}</span>
          )}
          {type === 'collaborative' && (
            <span className="badge blue">🤝 Match: {(item.cf_score * 100).toFixed(0)}%</span>
          )}
          {type === 'hybrid' && (
            <>
              <span className="badge green">🔀 {item.hybrid_score}</span>
              <span className="badge blue">📈 {item.popularity_score}</span>
              <span className="badge coral">🤝 {item.cf_score}</span>
            </>
          )}
        </div>

        {/* Price + Button */}
        <div className="product-footer">
          <span className="product-price">${item.price}</span>
          <button
            className={added ? 'btn-cart added' : 'btn-cart'}
            onClick={handleAddToCart}
          >
            {added ? '✅ Added!' : '🛒 Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main App ───────────────────────────────────────────
function App() {
  const [activeTab, setActiveTab]     = useState('popular');
  const [popularData, setPopularData] = useState([]);
  const [cfData, setCfData]           = useState([]);
  const [hybridData, setHybridData]   = useState([]);
  const [userId, setUserId]           = useState('');
  const [inputId, setInputId]         = useState('');
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState('');
  const [cartCount, setCartCount]     = useState(0);

  useEffect(() => { fetchPopular(); }, []);

  const fetchPopular = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.get(`${API}/recommendations/popular?top_n=10`);
      setPopularData(res.data.recommendations);
    } catch {
      setError('Backend not running. Start FastAPI server first.');
    }
    setLoading(false);
  };

  const fetchPersonalized = async () => {
    if (!inputId.trim()) {
      setError('Please enter a User ID');
      return;
    }
    setLoading(true);
    setError('');
    setUserId(inputId);
    try {
      const [cfRes, hybridRes] = await Promise.all([
        axios.get(`${API}/recommendations/collaborative/${inputId}?top_n=10`),
        axios.get(`${API}/recommendations/hybrid/${inputId}?top_n=10`)
      ]);
      setCfData(cfRes.data.recommendations);
      setHybridData(hybridRes.data.recommendations);
      setActiveTab('hybrid');
    } catch {
      setError('User not found. Try: ADLVFFE4VBT8');
    }
    setLoading(false);
  };

  const currentData = activeTab === 'popular' ? popularData
                    : activeTab === 'collaborative' ? cfData
                    : hybridData;

  return (
    <div className="app">

      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-brand">
          <span className="nav-logo">🤖</span>
          <span className="nav-title">TechShop AI</span>
        </div>
        <div className="nav-search">
          <input
            placeholder="Enter User ID for personalized recommendations..."
            value={inputId}
            onChange={e => setInputId(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && fetchPersonalized()}
          />
          <button onClick={fetchPersonalized} disabled={loading}>
            {loading ? '⏳' : '🔍'}
          </button>
        </div>
        <div className="nav-cart">
          🛒 Cart <span className="cart-count">{cartCount}</span>
        </div>
      </nav>

      {/* Hero Banner */}
      <div className="hero">
        <div className="hero-content">
          <h1>🤖 AI-Powered Electronics Store</h1>
          <p>Personalized recommendations powered by Machine Learning</p>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-num">7.8M+</span>
              <span className="stat-label">Reviews Analyzed</span>
            </div>
            <div className="stat">
              <span className="stat-num">3</span>
              <span className="stat-label">ML Models</span>
            </div>
            <div className="stat">
              <span className="stat-num">145K+</span>
              <span className="stat-label">Products</span>
            </div>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && <div className="error-banner">{error}</div>}

      {/* Tabs */}
      <div className="tabs-container">
        <div className="tabs">
          {[
            {id:'popular',       label:'🏆 Popular',       desc:'Top rated products'},
            {id:'collaborative', label:'🤝 For You',        desc:'Based on similar users'},
            {id:'hybrid',        label:'🔀 AI Recommended', desc:'Best of both models'}
          ].map(tab => (
            <button
              key={tab.id}
              className={activeTab === tab.id ? 'tab-btn active' : 'tab-btn'}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-label">{tab.label}</span>
              <span className="tab-desc">{tab.desc}</span>
            </button>
          ))}
        </div>

        {/* User ID hint */}
        {activeTab !== 'popular' && !userId && (
          <div className="hint-box">
            💡 Enter a User ID above to get personalized recommendations.
            Try: <strong>ADLVFFE4VBT8</strong>
          </div>
        )}
        {userId && activeTab !== 'popular' && (
          <div className="user-banner">
            🎯 Showing recommendations for: <strong>{userId}</strong>
          </div>
        )}
      </div>

      {/* Products Grid */}
      <div className="products-section">
        {loading ? (
          <div className="loading-screen">
            <div className="loading-spinner">🤖</div>
            <p>AI is computing your recommendations...</p>
          </div>
        ) : currentData.length === 0 ? (
          <div className="empty-state">
            <p>🔍 Enter a User ID and click search to get personalized recommendations</p>
          </div>
        ) : (
          <>
            <h2 className="section-title">
              {activeTab === 'popular' && '🏆 Top 10 Popular Products'}
              {activeTab === 'collaborative' && `🤝 Recommended For You`}
              {activeTab === 'hybrid' && `🔀 AI Recommended Products`}
            </h2>
            <div className="products-grid">
              {currentData.map(item => (
                <ProductCard
                  key={item.product_id}
                  item={item}
                  type={activeTab}
                />
              ))}
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>🤖 TechShop AI — Powered by ML Recommendation Engine</p>
        <p>Built with Python • FastAPI • React • MongoDB</p>
        <p>Internship Project by Amey Kalsapnavar</p>
      </footer>
    </div>
  );
}

export default App;