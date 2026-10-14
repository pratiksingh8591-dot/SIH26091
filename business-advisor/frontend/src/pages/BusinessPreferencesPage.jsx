export default function BusinessPreferencesPage({ form, updateField, onBack, onSubmit, loading, error }) {
  return (
    <div className="panel">
      <h2>Business Preferences</h2>
      <div className="grid">
        <label>Business Category<select value={form.business_category} onChange={(e) => updateField('business_category', e.target.value)}><option>Food & Beverage</option><option>Retail</option><option>Services</option><option>Repair & Services</option><option>Agriculture & Allied</option></select></label>
        <label>Preferred Business<input type="text" value={form.preferred_business} onChange={(e) => updateField('preferred_business', e.target.value)} /></label>
        <label>Expected Monthly Income<input type="number" value={form.expected_monthly_income} onChange={(e) => updateField('expected_monthly_income', Number(e.target.value))} /></label>
        <label>Risk Preference<select value={form.risk_preference} onChange={(e) => updateField('risk_preference', e.target.value)}><option>Low</option><option>Medium</option><option>High</option></select></label>
      </div>
      <div className="actions">
        <button className="secondary-btn" onClick={onBack}>Back</button>
        <button className="primary-btn" onClick={onSubmit} disabled={loading}>{loading ? 'Analyzing...' : 'Generate Report'}</button>
      </div>
      {error && <div className="error-box">{error}</div>}
    </div>
  );
}
