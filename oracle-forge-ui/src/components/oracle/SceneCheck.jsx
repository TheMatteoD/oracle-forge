import React, { useState } from 'react';
import { apiPost } from '../../api/apiClient';

function LogModal({ open, onClose, logText, onSave, saving, error }) {
  const [text, setText] = useState(logText);
  React.useEffect(() => { setText(logText); }, [logText]);
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

export default function SceneCheck({ chaos }) {
  const [expectation, setExpectation] = useState('');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState(null);
  const [flavorText, setFlavorText] = useState('');
  const [loading, setLoading] = useState(false);
  const [showLogModal, setShowLogModal] = useState(false);
  const [logError, setLogError] = useState(null);
  const [logSaving, setLogSaving] = useState(false);

  const handleScene = async () => {
    const res = await apiPost('/oracle/scene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chaos, flavor: false })
    });
    const data = await res.json();

    let out = `Expected: ${expectation}\nRoll: ${data.roll}\nResult: ${data.result}`;
    if (data.event_focus) {
      out += `\n\nEvent Focus: ${data.event_focus.result}\n${data.event_focus.description}`;
    }

    setFlavorData({
      expectation,
      focus: data.event_focus?.result || '',
      description: data.event_focus?.description || ''
    });

    setOutput(out);
    setFlavorText('');
  };

  const handleFlavor = async () => {
    setLoading(true);
    try {
      const res = await apiPost('/oracle/scene/flavor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      const data = await res.json();
      setOutput((prev) => `${prev}\n\n${data.narration}`);
      setFlavorText(data.narration);
      setFlavorData(null);
    } catch (error) {
      console.error("Failed to fetch scene flavor:", error);
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
      const res = await apiPost('/session/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text, type: 'oracle' })
      });
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
    logText = `Scene Expectation: ${expectation}\n\n${output}`;
    if (flavorText) logText += `\n\n${flavorText}`;
  }

  return (
    <section style={{ marginBottom: '2em' }}>
      <h2>Scene Check</h2>
      <label>
        What do you expect the scene to be?
        <input value={expectation} onChange={(e) => setExpectation(e.target.value)} />
      </label>

      <button onClick={handleScene}>Run Scene Test</button>
      {flavorData && <button onClick={handleFlavor}>Generate Scene Flavor</button>}
      {loading && <div className="loader">Generating narration...</div>}

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
