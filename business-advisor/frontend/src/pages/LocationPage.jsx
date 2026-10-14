export default function LocationPage({ form, updateField, onBack, onNext }) {
  return (
    <div className="panel">
      <h2>Location</h2>
      <div className="grid">
        <label>State<input type="text" value={form.state} onChange={(e) => updateField('state', e.target.value)} /></label>
        <label>District<input type="text" value={form.district} onChange={(e) => updateField('district', e.target.value)} /></label>
        <label>City/Village<input type="text" value={form.city_or_village} onChange={(e) => updateField('city_or_village', e.target.value)} /></label>
        <label>Pincode<input type="text" value={form.pincode} onChange={(e) => updateField('pincode', e.target.value)} /></label>
      </div>
      <div className="actions">
        <button className="secondary-btn" onClick={onBack}>Back</button>
        <button className="primary-btn" onClick={onNext}>Next</button>
      </div>
    </div>
  );
}
