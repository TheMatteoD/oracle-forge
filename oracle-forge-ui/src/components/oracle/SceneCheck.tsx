import React, { useState } from 'react';
import { useSceneCheckMutation } from '../../api/oracleApi';

interface SceneCheckProps {
  chaos: number;
}

function LogModal({ open, onClose, logText, onSave, saving, error }: any) {
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
          <button onClick={() => onSave(text)} disabled={saving} style={{ background: '#38a169', color: '#fff', padding: '6px 16px', borderRadius: 4 }}>
            {saving ? 'Saving...' : 'Save to Session'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function SceneCheck({ chaos }: SceneCheckProps) {
  const [expectation, setExpectation] = useState('');
  const [flavorData, setFlavorData] = useState<any>(null);
  const [flavorText, setFlavorText] = useState('');
  const [showLogModal, setShowLogModal] = useState(false);
  const [logError, setLogError] = useState<string | null>(null);
  const [logSaving, setLogSaving] = useState(false);

  const [sceneCheck, { data, error, isLoading }] = useSceneCheckMutation();

  React.useEffect(() => {
    if (data) {
      setFlavorData({
        expectation,
        focus: data.event_focus?.result || '',
        description: data.event_focus?.description || ''
      });
      setFlavorText('');
    }
  }, [data]);

  const handleScene = async () => {
    setFlavorText('');
    if (!expectation.trim()) return;
    await sceneCheck({ chaos, flavor: false });
  };

  const handleFlavor = async () => {
    if (!flavorData) return;
    setFlavorText('Generating...');
    try {
      const response = await fetch('/oracle/scene/flavor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      const data = await response.json();
      if (data.success && data.data) {
        setFlavorText(data.data.narration);
      } else {
        setFlavorText('Error: Failed to generate flavor text');
      }
    } catch {
      setFlavorText('Error: Failed to generate flavor text');
    }
  };

  const handleLog = () => {
    setShowLogModal(true);
    setLogError(null);
  };

  const handleSaveLog = async (text: string) => {
    setLogSaving(true);
    setLogError(null);
    try {
      const response = await fetch('/session/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text, type: 'oracle' })
      });
      const data = await response.json();
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

  const logText = data ?
    `Scene Expectation: ${expectation}\n\nExpected: ${expectation}\nRoll: ${data.roll}\nResult: ${data.result}${data.event_focus ? `\n\nEvent Focus: ${data.event_focus.result}\n${data.event_focus.description}` : ''}${flavorText ? `\n\n${flavorText}` : ''}` :
    '';

  return (
    <section style={{ marginBottom: '2em' }}>
      <h2>Scene Check</h2>
      <label>
        What do you expect the scene to be?
        <input
          value={expectation}
          onChange={(e) => setExpectation(e.target.value)}
          placeholder="Describe what you expect to happen..."
        />
      </label>
      <button onClick={handleScene} disabled={isLoading || !expectation.trim()}>
        {isLoading ? 'Running Scene Test...' : 'Run Scene Test'}
      </button>
      {flavorData && data && (
        <button onClick={handleFlavor} disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Scene Flavor'}
        </button>
      )}
      {isLoading && <div className="loader">Generating narration...</div>}
      <pre style={{
        background: '#222',
        padding: '1em',
        marginTop: '1em',
        borderLeft: '4px solid #6b46c1',
        whiteSpace: 'pre-wrap'
      }}>
        {data ? `Expected: ${expectation}\nRoll: ${data.roll}\nResult: ${data.result}${data.event_focus ? `\n\nEvent Focus: ${data.event_focus.result}\n${data.event_focus.description}` : ''}` : error ? (typeof error === 'object' && error !== null && 'data' in error && (error as any).data?.message ? `Error: ${(error as any).data.message}` : 'Error: Failed to get scene check result') : ''}
        {flavorText && `\n\n${flavorText}`}
      </pre>
      {data && (
        <button
          onClick={handleLog}
          className="mt-2 px-3 py-1 bg-purple-700 text-white rounded"
        >
          Log to Session
        </button>
      )}
      <LogModal
        open={showLogModal}
        onClose={() => setShowLogModal(false)}
        logText={logText}
        onSave={handleSaveLog}
        saving={logSaving}
        error={logError}
      />
    </section>
  );
} 