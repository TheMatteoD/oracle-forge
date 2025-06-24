import React, { useState } from 'react';
import config from "../../config";

const API = config.SERVER_URL;

export default function YesNoOracle({ chaos }) {
  const [question, setQuestion] = useState('');
  const [odds, setOdds] = useState('50/50');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    setFlavorData(null);
    setOutput('');
    const res = await fetch(`${API}/oracle/yesno`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, odds, chaos })
    });
    const data = await res.json();

    setOutput(`Q: ${data.question}\nRoll: ${data.roll}\nResult: ${data.result}\n${data.event_trigger || ''}`);
    setFlavorData({
      question,
      result: data.result,
      event_trigger: data.event_trigger
    });
    setLoading(false);
  };

  const handleFlavor = async () => {
    if (!flavorData) return;

    setLoading(true);
    try {
      const res = await fetch(`${API}/oracle/yesno/flavor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      const data = await res.json();
      setOutput((prev) => `${prev}\n\n${data.narration}`);
      setFlavorData(null);
    } catch (error) {
      console.error("Failed to fetch flavor:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section style={{ marginBottom: '2em' }}>
      <h2>Yes/No Oracle</h2>

      <label>
        Question:
        <input value={question} onChange={(e) => setQuestion(e.target.value)} />
      </label>

      <label>
        Odds:
        <select value={odds} onChange={(e) => setOdds(e.target.value)}>
          {["Certain", "Nearly Certain", "Very Likely", "Likely", "50/50", "Unlikely", "Very Unlikely", "Nearly Impossible", "Impossible"].map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>

      <button onClick={handleAsk} disabled={loading}>Ask Oracle</button>
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
