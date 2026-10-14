const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value);
};

export default function FinancialRoadmap({ financialData }) {
  const {
    available_margin_capital,
    project_cost,
    maximum_loan,
    scheme_name,
    interest_rate,
    tenure_years,
    moratorium_months,
    emi,
    repayment_schedule
  } = financialData;

  return (
    <div style={{ marginTop: '30px' }}>
      <h3>Financial Roadmap</h3>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '25px' }}>
        <div style={{ padding: '20px', background: '#e3f2fd', borderRadius: '8px', border: '1px solid #90caf9' }}>
          <div style={{ fontSize: '12px', color: '#1976d2', marginBottom: '5px', fontWeight: 500 }}>Available Margin Capital</div>
          <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#0d47a1' }}>{formatCurrency(available_margin_capital)}</div>
          <div style={{ fontSize: '11px', color: '#1976d2', marginTop: '5px' }}>10% of project cost</div>
        </div>

        <div style={{ padding: '20px', background: '#f3e5f5', borderRadius: '8px', border: '1px solid #ce93d8' }}>
          <div style={{ fontSize: '12px', color: '#7b1fa2', marginBottom: '5px', fontWeight: 500 }}>Project Cost</div>
          <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#4a148c' }}>{formatCurrency(project_cost)}</div>
          <div style={{ fontSize: '11px', color: '#7b1fa2', marginTop: '5px' }}>Total investment needed</div>
        </div>

        <div style={{ padding: '20px', background: '#fff3e0', borderRadius: '8px', border: '1px solid #ffb74d' }}>
          <div style={{ fontSize: '12px', color: '#e65100', marginBottom: '5px', fontWeight: 500 }}>Maximum Loan</div>
          <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#bf360c' }}>{formatCurrency(maximum_loan)}</div>
          <div style={{ fontSize: '11px', color: '#e65100', marginTop: '5px' }}>90% of project cost</div>
        </div>

        <div style={{ padding: '20px', background: '#e8f5e9', borderRadius: '8px', border: '1px solid #81c784' }}>
          <div style={{ fontSize: '12px', color: '#2e7d32', marginBottom: '5px', fontWeight: 500 }}>Monthly EMI</div>
          <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#1b5e20' }}>{formatCurrency(emi)}</div>
          <div style={{ fontSize: '11px', color: '#2e7d32', marginTop: '5px' }}>After moratorium</div>
        </div>
      </div>

      {/* Scheme Details */}
      <div style={{ padding: '25px', background: '#ffffff', borderRadius: '8px', border: '2px solid #2563eb', marginBottom: '25px' }}>
        <h4 style={{ marginTop: 0, color: '#2563eb', fontSize: '20px' }}>Selected Scheme: {scheme_name}</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px', marginTop: '15px' }}>
          <div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Interest Rate</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{interest_rate}% p.a.</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Tenure</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{tenure_years} years</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Moratorium</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{moratorium_months} months</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Total Months</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{tenure_years * 12} months</div>
          </div>
        </div>
      </div>

      {/* Repayment Schedule Table */}
      <div>
        <h4>Repayment Schedule (First 12 Months)</h4>
        <div style={{ overflowX: 'auto', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
            <thead>
              <tr style={{ background: '#f5f5f5' }}>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #e0e0e0' }}>Month</th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #e0e0e0' }}>Payment</th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #e0e0e0' }}>Principal</th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #e0e0e0' }}>Interest</th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #e0e0e0' }}>Balance</th>
              </tr>
            </thead>
            <tbody>
              {repayment_schedule.slice(0, 12).map((item) => (
                <tr key={item.month} style={{ borderBottom: '1px solid #f0f0f0' }}>
                  <td style={{ padding: '12px' }}>
                    {item.month}
                    {item.month <= moratorium_months && <span style={{ marginLeft: '8px', fontSize: '11px', color: '#f59e0b', fontWeight: 500 }}>(Moratorium)</span>}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'right', fontWeight: 500 }}>{formatCurrency(item.payment)}</td>
                  <td style={{ padding: '12px', textAlign: 'right' }}>{formatCurrency(item.principal)}</td>
                  <td style={{ padding: '12px', textAlign: 'right' }}>{formatCurrency(item.interest)}</td>
                  <td style={{ padding: '12px', textAlign: 'right', fontWeight: 500 }}>{formatCurrency(item.balance)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: '10px', fontSize: '12px', color: '#666' }}>
          Showing first 12 months. Total repayment schedule: {repayment_schedule.length} months
        </div>
      </div>
    </div>
  );
}
