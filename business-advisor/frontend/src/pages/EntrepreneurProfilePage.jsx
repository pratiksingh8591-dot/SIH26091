export default function EntrepreneurProfilePage({ form, updateField, onBack, onNext }) {
  return (
    <div className="panel">
      <h2>Entrepreneur Profile</h2>
      <div className="grid">
        <label>Age<input type="number" value={form.age} onChange={(e) => updateField('age', Number(e.target.value))} /></label>
        <label>Gender<select value={form.gender} onChange={(e) => updateField('gender', e.target.value)}><option>Female</option><option>Male</option><option>Other</option></select></label>
        <label>Social Category<select value={form.social_category} onChange={(e) => updateField('social_category', e.target.value)}><option>General</option><option>OBC</option><option>SC</option><option>ST</option><option>Women</option></select></label>
        <label>Annual Family Income<input type="number" value={form.annual_family_income} onChange={(e) => updateField('annual_family_income', Number(e.target.value))} /></label>
        <label>Education<select value={form.education} onChange={(e) => updateField('education', e.target.value)}><option>Below 10th</option><option>10th</option><option>12th</option><option>Diploma</option><option>Graduate</option></select></label>
        <label>Experience<input type="number" value={form.experience} onChange={(e) => updateField('experience', Number(e.target.value))} /></label>
      </div>
      <div className="actions">
        <button className="secondary-btn" onClick={onBack}>Back</button>
        <button className="primary-btn" onClick={onNext}>Next</button>
      </div>
    </div>
  );
}
