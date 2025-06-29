import React, { useState, useEffect } from 'react';
import { apiPost } from '../../api/apiClient';

function LogModal({ open, onClose, logText, onSave, saving, error }) {
  const [text, setText] = useState(logText);
  useEffect(() => { setText(logText); }, [logText]);
  if (!open) return null;
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.7)', zIndex: 1000 }}>
      <div style={{ background: '#222', color: '#fff', maxWidth: 500, margin: '10vh auto', padding: 24, borderRadius: 8, boxShadow: '0 0 16px #000' }}>
        <h3>Edit Log Entry</h3>
        <textarea value={text} onChange={e => setText(e.target.value)} rows={7} style={{ width: '100%', background: '#111', color: '#fff', marginTop: 8 }} />
        {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
        <div style={{ marginTop: 12, textAlign: 'right' }}>
          <button onClick={onClose} style={{ marginRight: 8 }}>Cancel</button>
          <button onClick={() => onSave(text)} disabled={saving} style={{ background: '#38a169', color: '#fff', padding: '6px 16px', borderRadius: 4 }}>{saving ? 'Saving...' : 'Save to Session'}</button>
        </div>
      </div>
    </div>
  );
}

export default function MeaningOracle({ chaos }) {
  const [question, setQuestion] = useState('');
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState(null);
  const [flavorText, setFlavorText] = useState('');
  const [loading, setLoading] = useState(false);
  const [showLogModal, setShowLogModal] = useState(false);
  const [logError, setLogError] = useState(null);
  const [logSaving, setLogSaving] = useState(false);

  useEffect(() => {
    apiPost('/oracle/meaning/tables')
      .then(response => {
        if (response.success) {
          setTables(response.data || []);
        } else {
          console.error("Failed to fetch tables:", response.error);
          setTables([]);
        }
      })
      .catch(error => {
        console.error("Error fetching tables:", error);
        setTables([]);
      });
  }, []);

  const handleMeaning = async () => {
    setLoading(true);
    setFlavorData(null);
    setOutput('');
    setFlavorText('');
    try {
      const res = await apiPost('/oracle/meaning', { question, table: selectedTable });
      const response = await res.json();
      if (response.success) {
        const data = response.data;
        setOutput(`Key words: ${data.keywords.join(', ')}\nRolls: ${data.rolls.join(', ')}`);
        setFlavorData({ question, keywords: data.keywords });
      } else {
        console.error("Failed to get meaning:", response.error);
        setOutput("Error: Failed to get meaning");
      }
    } catch (error) {
      console.error("Error getting meaning:", error);
      setOutput("Error: Failed to get meaning");
    } finally {
      setLoading(false);
    }
  };

  const handleFlavor = async () => {
    if (!flavorData) return;
    setLoading(true);
    try {
      const res = await apiPost('/oracle/meaning/flavor', flavorData);
      const response = await res.json();
      if (response.success) {
        const data = response.data;
        setOutput((prev) => `${prev}\n\n${data.narration}`);
        setFlavorText(data.narration);
        setFlavorData(null);
      } else {
        console.error("Failed to get flavor:", response.error);
      }
    } catch (error) {
      console.error("Failed to fetch flavor for meaning:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLog = () => {
    setShowLogModal(true);
    setLogError(null);
  };

  const handleSaveLog = async (text) => {
    setLogSaving(true);
    setLogError(null);
    try {
      const res = await apiPost('/session/log', { content: text, type: 'oracle' });
      const data = await res.json();
      if (data.success) {
        setShowLogModal(false);
      } else {
        setLogError('Failed to save log.');
      }
    } catch {
      setLogError('Failed to save log.');
    } finally {
      setLogSaving(false);
    }
  };

  let logText = '';
  if (output) {
    logText = `Oracle Question: ${question}\n\n${output}`;
    if (flavorText) logText += `\n\n${flavorText}`;
  }

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

      {output && (
        <button onClick={handleLog} className="mt-2 px-3 py-1 bg-purple-700 text-white rounded">Log to Session</button>
      )}
      <LogModal open={showLogModal} onClose={() => setShowLogModal(false)} logText={logText} onSave={handleSaveLog} saving={logSaving} error={logError} />
    </section>
  );
}
