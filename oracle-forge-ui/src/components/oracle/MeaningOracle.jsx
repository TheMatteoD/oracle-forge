import React, { useState, useEffect } from 'react';
import config from "../../config";

const API = config.SERVER_URL;

export default function MeaningOracle({ chaos }) {
  const [question, setQuestion] = useState('');
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/oracle/meaning/tables`)
      .then(res => res.json())
      .then(setTables);
  }, []);

  const handleMeaning = async () => {
    setLoading(true);
    setFlavorData(null);
    setOutput('');
    const res = await fetch(`${API}/oracle/meaning`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, table: selectedTable })
    });
    const data = await res.json();
    setOutput(`Key words: ${data.keywords.join(', ')}\nRolls: ${data.rolls.join(', ')}`);
    setFlavorData({ question, keywords: data.keywords });
    setLoading(false);
  };

  const handleFlavor = async () => {
    if (!flavorData) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/oracle/meaning/flavor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      const data = await res.json();
      setOutput((prev) => `${prev}\n\n${data.narration}`);
      setFlavorData(null);
    } catch (error) {
      console.error("Failed to fetch flavor for meaning:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section style={{ marginBottom: '2em' }}>
      <h2>Meaning Oracle</h2>

      <label>
        Question:
        <input value={question} onChange={(e) => setQuestion(e.target.value)} />
      </label>

      <label>
        Table:
        <select value={selectedTable} onChange={(e) => setSelectedTable(e.target.value)}>
          {tables.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </label>

      <button onClick={handleMeaning} disabled={loading}>Get Meaning</button>
      {flavorData && <button onClick={handleFlavor} disabled={loading}>Generate Flavor</button>}
      {loading && <div className="loader">Generating...</div>}

      <pre style={{
        background: '#222',
        padding: '1em',
        marginTop: '1em',
        borderLeft: '4px solid #6b46c1',
        whiteSpace: 'pre-wrap'
      }}>{output}</pre>
    </section>
  );
}
