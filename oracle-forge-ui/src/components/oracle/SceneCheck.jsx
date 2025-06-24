import React, { useState } from 'react';
import config from "../../config";

const API = config.SERVER_URL;

export default function SceneCheck({ chaos }) {
  const [expectation, setExpectation] = useState('');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScene = async () => {
    const res = await fetch(`${API}/oracle/scene`, {
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
  };

  const handleFlavor = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/oracle/scene/flavor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      const data = await res.json();
      setOutput((prev) => `${prev}\n\n${data.narration}`);
      setFlavorData(null);
    } catch (error) {
      console.error("Failed to fetch scene flavor:", error);
    } finally {
      setLoading(false);
    }
  };

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
    </section>
  );
}
