import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import './App.css';

const API = 'http://127.0.0.1:8000';

// ── Product Card Component ─────────────────────────────
function ProductCard({ item, type }) {
  return (
    <div className="card">
      <div className="card-rank">#{item.rank}</div>
      <div className="card-product-id">{item.product_id}</div>
      <div className="card-scores">
        {type === 'popular' && (
          <>
            <span className="score-badge blue">⭐ {item.avg_rating}</span>
            <span className="score-badge gray">📊 {item.rating_count} ratings</span>
            <span className="score-badge green">🏆 {item.score}</span>
          </>
        )}
        {type === 'collaborative' && (
          <span className="score-badge blue">🤝 CF Score: {item.cf_score}</span>
        )}
        {type === 'hybrid' && (
          <>
            <span className="score-badge green">🔀 {item.hybrid_score}</span>
            <span className="score-badge blue">📈 {item.popularity_score}</span>
            <span className="score-badge coral">🤝 {item.cf_score}</span>
          </>
        )}
      </div>
    </div>
  );
}

// ── Main App ───────────────────────────────────────────
function App() {
  const [activeTab, setActiveTab]         = useState('popular');
  const [popularData, setPopularData]     = useState([]);
  const [cfData, setCfData]               = useState([]);
  const [hybridData, setHybridData]       = useState([]);
  const [userId, setUserId]               = useState('ADLVFFE4VBT8');
  const [inputUserId, setInputUserId]     = useState('ADLVFFE4VBT8');
  const [loading, setLoading]             = useState(false);
  const [error, setError]                 = useState('');

  // Load popular on startup
  useEffect(() => {
    fetchPopular();
  }, []);

  const fetchPopular = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.get(`${API}/recommendations/popular?top_n=10`);
      setPopularData(res.data.recommendations);
    } catch (e) {
      setError('Failed to load popular products. Is the backend running?');
    }
    setLoading(false);
  };

  const fetchPersonalized = async () => {
    setLoading(true);
    setError('');
    setUserId(inputUserId);
    try {
      const [cfRes, hybridRes] = await Promise.all([
        axios.get(`${API}/recommendations/collaborative/${inputUserId}?top_n=10`),
        axios.get(`${API}/recommendations/hybrid/${inputUserId}?top_n=10`)
      ]);
      setCfData(cfRes.data.recommendations);
      setHybridData(hybridRes.data.recommendations);
      setActiveTab('hybrid');
    } catch (e) {
      setError('User not found or backend error. Try a different User ID.');
    }
    setLoading(false);
  };

  // Chart data
  const chartData = hybridData.slice(0, 5).map(item => ({
    name: item.product_id.slice(-6),
    Hybrid: item.hybrid_score,
    Popularity: item.popularity_score,
    CF: item.cf_score,
  }));

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <h1>🤖 AI Product Recommender</h1>
        <p>Powered by Machine Learning — Amazon Electronics Dataset</p>
      </header>

      {/* User Input */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Enter User ID..."
          value={inputUserId}
          onChange={e => setInputUserId(e.target.value)}
        />
        <button onClick={fetchPersonalized} disabled={loading}>
          {loading ? '⏳ Loading...' : '🔍 Get Recommendations'}
        </button>
      </div>

      {/* Error */}
      {error && <div className="error">{error}</div>}

      {/* Tabs */}
      <div className="tabs">
        <button
          className={activeTab === 'popular' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('popular')}
        >
          🏆 Popular
        </button>
        <button
          className={activeTab === 'collaborative' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('collaborative')}
        >
          🤝 Collaborative
        </button>
        <button
          className={activeTab === 'hybrid' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('hybrid')}
        >
          🔀 Hybrid
        </button>
      </div>

      {/* Loading */}
      {loading && <div className="loading">⏳ Computing recommendations...</div>}

      {/* Popular Tab */}
      {activeTab === 'popular' && !loading && (
        <div className="results">
          <h2>🏆 Top 10 Popular Products</h2>
          <p className="subtitle">Based on weighted rating formula — same for all users</p>
          <div className="cards-grid">
            {popularData.map(item => (
              <ProductCard key={item.product_id} item={item} type="popular" />
            ))}
          </div>
        </div>
      )}

      {/* Collaborative Tab */}
      {activeTab === 'collaborative' && !loading && (
        <div className="results">
          <h2>🤝 Collaborative Filtering for {userId}</h2>
          <p className="subtitle">Based on similar users' behavior</p>
          {cfData.length === 0 ? (
            <p className="empty">Enter a User ID and click Get Recommendations</p>
          ) : (
            <div className="cards-grid">
              {cfData.map(item => (
                <ProductCard key={item.product_id} item={item} type="collaborative" />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Hybrid Tab */}
      {activeTab === 'hybrid' && !loading && (
        <div className="results">
          <h2>🔀 Hybrid Recommendations for {userId}</h2>
          <p className="subtitle">Combines Popularity (40%) + Collaborative Filtering (60%)</p>
          {hybridData.length === 0 ? (
            <p className="empty">Enter a User ID and click Get Recommendations</p>
          ) : (
            <>
              {/* Chart */}
              {chartData.length > 0 && (
                <div className="chart-container">
                  <h3>📊 Score Breakdown — Top 5 Products</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis domain={[0, 1]} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="Hybrid" fill="#4CAF50" />
                      <Bar dataKey="Popularity" fill="#2196F3" />
                      <Bar dataKey="CF" fill="#FF5722" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
              <div className="cards-grid">
                {hybridData.map(item => (
                  <ProductCard key={item.product_id} item={item} type="hybrid" />
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>AI Product Recommendation System — Internship Project by Amey Kalsapnavar</p>
      </footer>
    </div>
  );
}

export default App;