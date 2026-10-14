export default function HomePage({ onStart }) {
  return (
    <div className="panel hero-panel">
      <div>
        <p className="eyebrow">SIH Business Advisory System</p>
        <h1>Hyper-Local Business Advisory for Rural Micro-Entrepreneurs</h1>
        <p className="subtext">
          Assess the viability of a business idea, estimate financial readiness, and discover suitable government schemes with a simple rule-based advisory engine.
        </p>
        <button className="primary-btn" onClick={onStart}>Start Analysis</button>
      </div>
    </div>
  );
}
