import { useState } from 'react';
import CompetitorMap from '../components/CompetitorMap';
import FinancialRoadmap from '../components/FinancialRoadmap';

const ScoreCard = ({ label, score, color }) => {
  const displayScore = score !== null && score !== undefined ? score.toFixed(1) : 'N/A';
  const bgColor = score !== null ? color : '#f5f5f5';

  return (
    <div style={{ padding: '20px', background: bgColor, borderRadius: '8px', textAlign: 'center' }}>
      <div style={{ fontSize: '12px', color: '#666', marginBottom: '8px', fontWeight: 500 }}>{label}</div>
      <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#1a1a1a' }}>{displayScore}</div>
      {score === null && <div style={{ fontSize: '11px', color: '#999', marginTop: '5px' }}>Data unavailable</div>}
    </div>
  );
};

export default function FeasibilityDashboardPage({ analysisResult, onBack }) {
  const { input, market, feasibility, financial, data_sources, limitations, analytics } = analysisResult;

  const getScoreColor = (score) => {
    if (score === null || score === undefined) return '#f5f5f5';
    if (score >= 75) return '#d1fae5';
    if (score >= 50) return '#fef3c7';
    return '#fee2e2';
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={onBack}
          style={{
            padding: '10px 20px',
            background: '#f3f4f6',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            cursor: 'pointer',
            marginBottom: '20px',
          }}
        >
          ← New Analysis
        </button>
        <h2 style={{ marginTop: '10px', marginBottom: '10px' }}>Business Feasibility Analysis</h2>
        <div style={{ color: '#666', fontSize: '14px' }}>
          {input.business.name} ({input.business.category}) at {input.location.name}
        </div>
      </div>

      {/* Overall Feasibility Score */}
      <div style={{
        padding: '40px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '12px',
        color: 'white',
        marginBottom: '30px',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '16px', marginBottom: '10px', opacity: 0.9 }}>Overall Feasibility Score</div>
        <div style={{ fontSize: '72px', fontWeight: 'bold' }}>{feasibility.feasibility_score.toFixed(1)}</div>
        <div style={{ fontSize: '14px', opacity: 0.9, marginTop: '10px' }}>
          Confidence: {feasibility.confidence.toFixed(0)}% | Based on {data_sources.length} data source(s)
        </div>
      </div>

      {/* Individual Scores */}
      <div style={{ marginBottom: '30px' }}>
        <h3>Feasibility Indicators</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <ScoreCard label="Demand Score" score={feasibility.demand_score} color={getScoreColor(feasibility.demand_score)} />
          <ScoreCard label="Competition Score" score={feasibility.competition_score} color={getScoreColor(feasibility.competition_score)} />
          <ScoreCard label="Purchasing Power" score={feasibility.purchasing_power_score} color={getScoreColor(feasibility.purchasing_power_score)} />
          <ScoreCard label="Market Access" score={feasibility.market_access_score} color={getScoreColor(feasibility.market_access_score)} />
          <ScoreCard label="Supply Score" score={feasibility.supply_score} color={getScoreColor(feasibility.supply_score)} />
          <ScoreCard label="Risk Score" score={feasibility.risk_score} color={getScoreColor(feasibility.risk_score)} />
          <ScoreCard label="Capital Fit" score={feasibility.capital_fit_score} color={getScoreColor(feasibility.capital_fit_score)} />
        </div>
      </div>

      {/* Explanations */}
      <div style={{ padding: '20px', background: '#f8f9fa', borderRadius: '8px', marginBottom: '30px' }}>
        <h4 style={{ marginTop: 0 }}>Score Explanations</h4>
        <ul style={{ fontSize: '14px', lineHeight: '1.8' }}>
          <li><strong>Demand Score:</strong> Based on population in the area (higher population = higher demand potential)</li>
          <li><strong>Competition Score:</strong> Based on competitor density (lower density = less competition = higher score)</li>
          <li><strong>Purchasing Power:</strong> Estimated based on population size and urban classification</li>
          <li><strong>Market Access:</strong> Based on distance to nearest competitors and market positioning</li>
          <li><strong>Supply Score:</strong> Supply chain analysis (not yet integrated - future enhancement)</li>
          <li><strong>Risk Score:</strong> Combined assessment of capital adequacy and competition risk</li>
          <li><strong>Capital Fit:</strong> How well your available capital matches the project requirements</li>
        </ul>
      </div>

      {/* Market Data */}
      <div style={{ marginBottom: '30px' }}>
        <h3>Market Analysis</h3>
        <div style={{
          padding: '12px 16px',
          marginBottom: '16px',
          borderRadius: '8px',
          background: market.competitor_search_status === 'unavailable' ? '#fff1f2' : '#f0fdf4',
          color: market.competitor_search_status === 'unavailable' ? '#991b1b' : '#166534',
        }}>
          <strong>Competitor search: </strong>
          {market.competitor_search_status === 'found' && 'completed and competitors were found.'}
          {market.competitor_search_status === 'completed_empty' && 'completed successfully; no mapped competitors were found.'}
          {market.competitor_search_status === 'incomplete' && 'returned incomplete data; the competitor count may be understated.'}
          {market.competitor_search_status === 'unavailable' && 'unavailable. A zero count is not a confirmed empty market.'}
          {market.competitor_search_message && (
            <div style={{ fontSize: '12px', marginTop: '4px' }}>{market.competitor_search_message}</div>
          )}
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px', marginBottom: '20px' }}>
          <div style={{ padding: '20px', background: '#fff', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Population</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
              {market.population ? market.population.toLocaleString('en-IN') : 'N/A'}
            </div>
            {market.population_source && (
              <div style={{ fontSize: '11px', color: '#999', marginTop: '5px' }}>{market.population_source}</div>
            )}
          </div>

          <div style={{ padding: '20px', background: '#fff', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Search Radius</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{input.radius_km} km</div>
          </div>
        </div>

        {/* Competitor Map */}
        <CompetitorMap
          userLocation={input.location}
          competitors={market.competitors}
          radiusKm={input.radius_km}
          marketData={market}
        />
      </div>

      {/* Financial Roadmap */}
      <FinancialRoadmap financialData={financial} />

      <BusinessIntelligence analytics={analytics} />

      {/* Data Sources and Limitations */}
      <div style={{ marginTop: '40px', padding: '20px', background: '#fffbeb', border: '1px solid #fbbf24', borderRadius: '8px' }}>
        <h4 style={{ marginTop: 0, color: '#92400e' }}>Data Sources & Limitations</h4>
        <div style={{ marginBottom: '15px' }}>
          <strong style={{ fontSize: '13px' }}>Data Sources:</strong>
          <ul style={{ margin: '5px 0', paddingLeft: '20px', fontSize: '13px' }}>
            {data_sources.map((source, idx) => (
              <li key={idx}>{source}</li>
            ))}
          </ul>
        </div>
        {limitations.length > 0 && (
          <div>
            <strong style={{ fontSize: '13px' }}>Limitations:</strong>
            <ul style={{ margin: '5px 0', paddingLeft: '20px', fontSize: '13px' }}>
              {limitations.map((limitation, idx) => (
                <li key={idx}>{limitation}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

function BusinessIntelligence({ analytics }) {
  const clustering = analytics?.clustering;
  const prediction = analytics?.business_prediction;
  const locations = clustering?.locations || [];
  const [selectedCluster, setSelectedCluster] = useState('all');
  const visibleLocations = selectedCluster === 'all'
    ? locations
    : locations.filter((location) => String(location.cluster_id) === selectedCluster);

  return (
    <section style={{ marginTop: '40px', padding: '24px', background: '#eff6ff', borderRadius: '12px' }}>
      <h3 style={{ marginTop: 0 }}>Business Intelligence &amp; Location Analytics</h3>
      {!clustering ? (
        <p>Location clustering is unavailable for this analysis.</p>
      ) : (
        <>
          <p style={{ color: '#4b5563' }}>
            K-Means groups the project&apos;s population records using the population feature after
            scaling. Labels are derived from fitted centroid populations, not cluster IDs.
          </p>
          <div style={{ marginBottom: '16px' }}>
            <label>
              Explore cluster
              <select value={selectedCluster} onChange={(event) => setSelectedCluster(event.target.value)}>
                <option value="all">All clusters</option>
                {clustering.summaries.map((summary) => (
                  <option key={summary.cluster_id} value={summary.cluster_id}>
                    {summary.cluster_label} ({summary.location_count})
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead><tr><th>Location</th><th>Population</th><th>Cluster</th><th>Why</th></tr></thead>
              <tbody>
                {visibleLocations.map((location) => (
                  <tr key={location.location_name}>
                    <td>{location.location_name}</td>
                    <td>{location.population.toLocaleString('en-IN')}</td>
                    <td>{location.cluster_id}: {location.cluster_label}</td>
                    <td>{location.explanation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p style={{ fontSize: '13px', color: '#4b5563' }}>
            Silhouette score: {clustering.evaluation.silhouette_score ?? 'Not meaningful for this dataset size'}.
          </p>
        </>
      )}
      <div style={{ marginTop: '20px', padding: '16px', background: '#fff', borderRadius: '8px' }}>
        <h4 style={{ marginTop: 0 }}>Business Success Prediction</h4>
        <p>
          {prediction?.status === 'unavailable'
            ? prediction.reason
            : 'A trained model-based estimate is available.'}
        </p>
        <small>
          No probability is shown until labelled historical business outcomes are added.
          The existing feasibility score is rule-based and is not a success probability.
        </small>
      </div>
    </section>
  );
}
