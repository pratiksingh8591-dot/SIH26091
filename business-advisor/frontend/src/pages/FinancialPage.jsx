export default function FinancialPage({ form, updateField, onBack, onNext }) {
  return (
    <div className="panel">
      <h2>Financial Information</h2>
      <div className="grid">
        <label>Available Capital<input type="number" value={form.available_capital} onChange={(e) => updateField('available_capital', Number(e.target.value))} /></label>
        <label>Desired Loan Amount<input type="number" value={form.desired_loan_amount} onChange={(e) => updateField('desired_loan_amount', Number(e.target.value))} /></label>
        <label>Monthly Household Expenses<input type="number" value={form.monthly_household_expenses} onChange={(e) => updateField('monthly_household_expenses', Number(e.target.value))} /></label>
      </div>
      <div className="actions">
        <button className="secondary-btn" onClick={onBack}>Back</button>
        <button className="primary-btn" onClick={onNext}>Next</button>
      </div>
    </div>
  );
}
