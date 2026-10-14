export default function LoadingState() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '400px',
      gap: '20px'
    }}>
      <div style={{
        width: '60px',
        height: '60px',
        border: '4px solid #f0f0f0',
        borderTop: '4px solid #2563eb',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }}></div>
      <h3>Analyzing market conditions...</h3>
      <p style={{ color: '#666', textAlign: 'center' }}>
        Fetching competitor data from OpenStreetMap<br/>
        Calculating geospatial metrics<br/>
        Processing financial analysis
      </p>
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
