import React, { useEffect, useState } from 'react';

export default function Dashboard() {
  const [findings, setFindings] = useState([]);

  useEffect(() => {
    // Mock fetch to API
    fetch('http://localhost:8000/api/v1/findings')
      .then(res => res.json())
      .then(data => setFindings(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Continuous Operational Governance</h1>
      <div className="grid grid-cols-3 gap-4">
        {findings.map(f => (
          <div key={f.id} className="border p-4 rounded shadow">
            <h3 className="font-semibold">{f.rule_name}</h3>
            <p className="text-sm text-gray-600">Severity: {f.severity}</p>
            <p className="mt-2 text-sm">{f.finding}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
