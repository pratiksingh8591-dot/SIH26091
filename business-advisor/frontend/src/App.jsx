import { useState, useEffect } from 'react';
import { analyzeBusiness, getBusinessCategories, getHealth } from './services/api';
import LocationSelectionPage from './pages/LocationSelectionPage';
import FeasibilityDashboardPage from './pages/FeasibilityDashboardPage';
import LoadingState from './components/LoadingState';

export default function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'location', 'loading', 'results'
  const [categories, setCategories] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('Checking...');

  useEffect(() => {
    // Load categories and check backend on mount
    loadCategories();
    checkBackend();
  }, []);

  const loadCategories = async () => {
    try {
      const cats = await getBusinessCategories();
      setCategories(cats);
    } catch (err) {
      console.error('Failed to load categories:', err);
      // Use fallback categories if backend fails
      setCategories([
        { key: 'restaurant', name: 'Restaurant', osm_tags: ['amenity=restaurant'] },
        { key: 'bakery', name: 'Bakery', osm_tags: ['shop=bakery'] },
        { key: 'cafe', name: 'Cafe', osm_tags: ['amenity=cafe'] },
        { key: 'grocery', name: 'Grocery', osm_tags: ['shop=supermarket'] },
        { key: 'pharmacy', name: 'Pharmacy', osm_tags: ['amenity=pharmacy'] },
        { key: 'clothing', name: 'Clothing', osm_tags: ['shop=clothes'] },
      ]);
    }
  };

  const checkBackend = async () => {
    try {
      const data = await getHealth();
      setBackendStatus(data.status === 'ok' ? '✓ Backend Online' : '✓ Connected');
    } catch (err) {
      setBackendStatus('✗ Backend Unavailable');
    }
  };

  const handleAnalyze = async (analysisData) => {
    setCurrentView('loading');
    setError('');

    try {
      const result = await analyzeBusiness(analysisData);
      setAnalysisResult(result);
      setCurrentView('results');
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
      setCurrentView('location');
      alert(`Analysis failed: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleBack = () => {
    setCurrentView('location');
    setAnalysisResult(null);
    setError('');
  };

  const renderHome = () => (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      padding: '20px',
    }}>
      <div style={{ maxWidth: '800px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>
          Hyper-Local Business Advisory
        </h1>
        <p style={{ fontSize: '20px', marginBottom: '10px', opacity: 0.95 }}>
          For Rural Micro-Entrepreneurs
        </p>
        <p style={{ fontSize: '16px', marginBottom: '40px', opacity: 0.85, lineHeight: '1.6' }}>
          Assess business viability, analyze local competition, estimate financial feasibility,
          and discover suitable government schemes using real market data from OpenStreetMap.
        </p>
        <button
          onClick={() => setCurrentView('location')}
          style={{
            padding: '18px 40px',
            fontSize: '18px',
            fontWeight: 600,
            background: 'white',
            color: '#667eea',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          }}
        >
          Start Analysis
        </button>
        <div style={{ marginTop: '30px', fontSize: '14px', opacity: 0.8 }}>
          SIH 2026 - Problem Statement #26091
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      {/* Header */}
      {currentView !== 'home' && (
        <header style={{
          background: 'white',
          borderBottom: '1px solid #e5e7eb',
          padding: '15px 30px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <div>
            <div style={{ fontSize: '12px', color: '#6b7280', fontWeight: 500 }}>SIH 2026</div>
            <h2 style={{ margin: '5px 0 0 0', fontSize: '20px' }}>Business Advisor</h2>
          </div>
          <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
            <button
              onClick={checkBackend}
              style={{
                padding: '8px 16px',
                background: '#f3f4f6',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              Check Backend
            </button>
            <span style={{
              padding: '6px 12px',
              background: backendStatus.includes('✓') ? '#d1fae5' : '#fee2e2',
              color: backendStatus.includes('✓') ? '#065f46' : '#991b1b',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 500,
            }}>
              {backendStatus}
            </span>
          </div>
        </header>
      )}

      {/* Main Content */}
      <main>
        {currentView === 'home' && renderHome()}
        {currentView === 'location' && (
          <LocationSelectionPage onAnalyze={handleAnalyze} categories={categories} />
        )}
        {currentView === 'loading' && (
          <div style={{ padding: '60px 20px' }}>
            <LoadingState />
          </div>
        )}
        {currentView === 'results' && analysisResult && (
          <FeasibilityDashboardPage analysisResult={analysisResult} onBack={handleBack} />
        )}
      </main>
    </div>
  );
}
