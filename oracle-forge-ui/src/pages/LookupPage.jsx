// src/pages/LookupPage.jsx
import React, { useState } from 'react';
import Navbar from '../components/core/Navbar';
import config from "../config";

export default function LookupPage() {
  const API = config.SERVER_URL;
  const [monsterQuery, setMonsterQuery] = useState({ query: '', system: '', tag: '', random: '', environment: '', theme: '', context: '', narrate: false, log_session: true });
  const [spellQuery, setSpellQuery] = useState({ query: '', system: '', class: '', level: '', tag: '', random: '', theme: '', context: '', narrate: false, log_session: true });
  const [itemQuery, setItemQuery] = useState({ query: '', system: '', category: '', subcategory: '', tag: '', random: '', environment: '', quality: '', theme: '', context: '', narrate: false, log_session: true });
  const [ruleQuery, setRuleQuery] = useState({ query: '', system: '', tag: '' });

  const [monsterOutput, setMonsterOutput] = useState('');
  const [spellOutput, setSpellOutput] = useState('');
  const [itemOutput, setItemOutput] = useState('');
  const [ruleOutput, setRuleOutput] = useState('');

  // Rewrite state
  const [rewriteNarration, setRewriteNarration] = useState('');
  const [rewriteInstruction, setRewriteInstruction] = useState('');
  const [rewriteOutput, setRewriteOutput] = useState('');

  const fetchData = async (path, body, setter) => {
    // Convert empty strings to undefined for the API
    const cleanBody = Object.fromEntries(
      Object.entries(body).map(([key, value]) => [key, value === '' ? undefined : value])
    );
    
    const res = await fetch(`${API}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cleanBody)
    });
    const data = await res.json();
    setter(JSON.stringify(data, null, 2));
  };

  const handleRewrite = async () => {
    if (!rewriteNarration || !rewriteInstruction) {
      alert('Please provide both narration and instruction');
      return;
    }

    const res = await fetch(`${API}/lookup/rewrite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        narration: rewriteNarration,
        instruction: rewriteInstruction,
        log_session: true
      })
    });
    const data = await res.json();
    setRewriteOutput(JSON.stringify(data, null, 2));
  };

  const renderLookupSection = (title, query, setQuery, fetchFunction, output, setOutput) => {
    const hasNarration = query.narrate;
    const isItemLookup = title === 'Item Lookup';
    
    return (
      <div style={sectionStyle}>
        <h2>{title}</h2>
        <div style={inputGridStyle}>
          <input placeholder="Name Query" onChange={e => setQuery({ ...query, query: e.target.value })} />
          <input placeholder="System" onChange={e => setQuery({ ...query, system: e.target.value })} />
          <input placeholder="Tag" onChange={e => setQuery({ ...query, tag: e.target.value })} />
          {isItemLookup && (
            <>
              <input placeholder="Category" onChange={e => setQuery({ ...query, category: e.target.value })} />
              <input placeholder="Subcategory" onChange={e => setQuery({ ...query, subcategory: e.target.value })} />
              <input placeholder="Quality" onChange={e => setQuery({ ...query, quality: e.target.value })} />
            </>
          )}
          <input placeholder="Random Count" type="number" min="1" onChange={e => setQuery({ ...query, random: parseInt(e.target.value) || '' })} />
          <input placeholder="Environment" onChange={e => setQuery({ ...query, environment: e.target.value })} />
          <input placeholder="Theme" onChange={e => setQuery({ ...query, theme: e.target.value })} />
          <input placeholder="Context" onChange={e => setQuery({ ...query, context: e.target.value })} />
          <label style={checkboxStyle}>
            <input 
              type="checkbox" 
              checked={query.narrate} 
              onChange={e => setQuery({ ...query, narrate: e.target.checked })} 
            />
            Narrate
          </label>
          <label style={checkboxStyle}>
            <input 
              type="checkbox" 
              checked={query.log_session} 
              onChange={e => setQuery({ ...query, log_session: e.target.checked })} 
            />
            Log to Session
          </label>
        </div>
        <button onClick={() => fetchFunction(query, setOutput)}>Lookup {title.split(' ')[0]}</button>
        
        {output && (
          <div>
            {hasNarration && (
              <div style={narrationStyle}>
                <h3>LLM Narration</h3>
                <pre style={outputStyle}>
                  {(() => {
                    try {
                      const data = JSON.parse(output);
                      return data.narration || 'No narration available';
                    } catch {
                      return 'No narration available';
                    }
                  })()}
                </pre>
              </div>
            )}
            <div style={dataStyle}>
              <h3>Raw Data</h3>
              <pre style={outputStyle}>
                {(() => {
                  try {
                    const data = JSON.parse(output);
                    return JSON.stringify(data.items || data, null, 2);
                  } catch {
                    return output;
                  }
                })()}
              </pre>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      <h1 style={{ fontSize: '1.5em' }}>📚 Oracle Forge - Lookup Tools</h1>

      {renderLookupSection('Monster Lookup', monsterQuery, setMonsterQuery, 
        (query, setter) => fetchData('/lookup/monster', query, setter), monsterOutput, setMonsterOutput)}
      
      {renderLookupSection('Spell Lookup', spellQuery, setSpellQuery, 
        (query, setter) => fetchData('/lookup/spell', query, setter), spellOutput, setSpellOutput)}
      
      {renderLookupSection('Item Lookup', itemQuery, setItemQuery, 
        (query, setter) => fetchData('/lookup/item', query, setter), itemOutput, setItemOutput)}

      <div style={sectionStyle}>
        <h2>Rule Lookup</h2>
        <input placeholder="Text Query" onChange={e => setRuleQuery({ ...ruleQuery, query: e.target.value })} />
        <input placeholder="System" onChange={e => setRuleQuery({ ...ruleQuery, system: e.target.value })} />
        <input placeholder="Tag" onChange={e => setRuleQuery({ ...ruleQuery, tag: e.target.value })} />
        <button onClick={() => fetchData('/lookup/rule', ruleQuery, setRuleOutput)}>Lookup Rule</button>
        <pre style={outputStyle}>{ruleOutput}</pre>
      </div>

      <div style={sectionStyle}>
        <h2>Rewrite Narration</h2>
        <div style={inputGridStyle}>
          <textarea 
            placeholder="Original Narration" 
            value={rewriteNarration}
            onChange={e => setRewriteNarration(e.target.value)}
            style={textareaStyle}
          />
          <textarea 
            placeholder="Rewrite Instruction" 
            value={rewriteInstruction}
            onChange={e => setRewriteInstruction(e.target.value)}
            style={textareaStyle}
          />
        </div>
        <button onClick={handleRewrite}>Rewrite Narration</button>
        {rewriteOutput && (
          <div style={dataStyle}>
            <h3>Rewritten Narration</h3>
            <pre style={outputStyle}>
              {(() => {
                try {
                  const data = JSON.parse(rewriteOutput);
                  return data.rewritten_narration || 'No rewritten narration available';
                } catch {
                  return rewriteOutput;
                }
              })()}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

const linkStyle = {
  color: '#6b46c1',
  display: 'inline-block',
  marginRight: '1em',
};

const sectionStyle = {
  marginBottom: '2em',
  padding: '1em',
  border: '1px solid #333',
  borderRadius: '8px',
};

const inputGridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  gap: '0.5em',
  marginBottom: '1em',
};

const checkboxStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '0.5em',
  fontSize: '0.9em',
};

const textareaStyle = {
  width: '100%',
  minHeight: '100px',
  padding: '0.5em',
  background: '#222',
  color: '#eee',
  border: '1px solid #444',
  borderRadius: '4px',
  fontFamily: 'monospace',
  resize: 'vertical',
};

const outputStyle = {
  background: '#222',
  padding: '1em',
  marginTop: '1em',
  borderLeft: '4px solid #6b46c1',
  whiteSpace: 'pre-wrap',
  borderRadius: '4px',
};

const narrationStyle = {
  marginBottom: '1em',
};

const dataStyle = {
  marginTop: '1em',
};
