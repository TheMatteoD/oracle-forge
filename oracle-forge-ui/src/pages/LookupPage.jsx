// src/pages/LookupPage.jsx
import React, { useState } from 'react';
import Navbar from '../components/core/Navbar';
import config from "../config";

export default function LookupPage() {
  const API = config.SERVER_URL;
  const [monsterQuery, setMonsterQuery] = useState({ query: '', system: '', tag: '' });
  const [spellQuery, setSpellQuery] = useState({ query: '', system: '', class: '', level: '', tag: '' });
  const [ruleQuery, setRuleQuery] = useState({ query: '', system: '', tag: '' });

  const [monsterOutput, setMonsterOutput] = useState('');
  const [spellOutput, setSpellOutput] = useState('');
  const [ruleOutput, setRuleOutput] = useState('');

  const fetchData = async (path, body, setter) => {
    const res = await fetch(`${API}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    setter(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      <h1 style={{ fontSize: '1.5em' }}>📚 Oracle Forge - Lookup Tools</h1>

      <div style={sectionStyle}>
        <h2>Monster Lookup</h2>
        <input placeholder="Name Query" onChange={e => setMonsterQuery({ ...monsterQuery, query: e.target.value })} />
        <input placeholder="System" onChange={e => setMonsterQuery({ ...monsterQuery, system: e.target.value })} />
        <input placeholder="Tag" onChange={e => setMonsterQuery({ ...monsterQuery, tag: e.target.value })} />
        <button onClick={() => fetchData('/lookup/monster', monsterQuery, setMonsterOutput)}>Lookup Monster</button>
        <pre style={outputStyle}>{monsterOutput}</pre>
      </div>

      <div style={sectionStyle}>
        <h2>Spell Lookup</h2>
        <input placeholder="Name Query" onChange={e => setSpellQuery({ ...spellQuery, query: e.target.value })} />
        <input placeholder="System" onChange={e => setSpellQuery({ ...spellQuery, system: e.target.value })} />
        <input placeholder="Class" onChange={e => setSpellQuery({ ...spellQuery, class: e.target.value })} />
        <input placeholder="Level" type="number" min="0" onChange={e => setSpellQuery({ ...spellQuery, level: e.target.value })} />
        <input placeholder="Tag" onChange={e => setSpellQuery({ ...spellQuery, tag: e.target.value })} />
        <button onClick={() => fetchData('/lookup/spell', spellQuery, setSpellOutput)}>Lookup Spell</button>
        <pre style={outputStyle}>{spellOutput}</pre>
      </div>

      <div style={sectionStyle}>
        <h2>Rule Lookup</h2>
        <input placeholder="Text Query" onChange={e => setRuleQuery({ ...ruleQuery, query: e.target.value })} />
        <input placeholder="System" onChange={e => setRuleQuery({ ...ruleQuery, system: e.target.value })} />
        <input placeholder="Tag" onChange={e => setRuleQuery({ ...ruleQuery, tag: e.target.value })} />
        <button onClick={() => fetchData('/lookup/rule', ruleQuery, setRuleOutput)}>Lookup Rule</button>
        <pre style={outputStyle}>{ruleOutput}</pre>
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
};

const outputStyle = {
  background: '#222',
  padding: '1em',
  marginTop: '1em',
  borderLeft: '4px solid #6b46c1',
  whiteSpace: 'pre-wrap',
};
