import { useState, useEffect } from 'react';
import { OracleAPI } from '@/api/apiClient';
import type { APIResponse } from '@/types/api';

// Types for the component
interface MeaningResult {
  keywords: string[];
  rolls: number[];
}

interface FlavorResult {
  narration: string;
}

interface LogModalProps {
  open: boolean;
  onClose: () => void;
  logText: string;
  onSave: (text: string) => Promise<void>;
  saving: boolean;
  error: string | null;
}

interface MeaningOracleProps {
  chaos: number;
}

// Log Modal Component (reusing from other oracle components)
function LogModal({ open, onClose, logText, onSave, saving, error }: LogModalProps) {
  const [text, setText] = useState(logText);
  
  useEffect(() => { 
    setText(logText); 
  }, [logText]);
  
  if (!open) return null;
  
  return (
    <div style={{ 
      position: 'fixed', 
      top: 0, 
      left: 0, 
      width: '100vw', 
      height: '100vh', 
      background: 'rgba(0,0,0,0.7)', 
      zIndex: 1000 
    }}>
      <div style={{ 
        background: '#222', 
        color: '#fff', 
        maxWidth: 500, 
        margin: '10vh auto', 
        padding: 24, 
        borderRadius: 8, 
        boxShadow: '0 0 16px #000' 
      }}>
        <h3>Edit Log Entry</h3>
        <textarea 
          value={text} 
          onChange={e => setText(e.target.value)} 
          rows={7} 
          style={{ 
            width: '100%', 
            background: '#111', 
            color: '#fff', 
            marginTop: 8 
          }} 
        />
        {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
        <div style={{ marginTop: 12, textAlign: 'right' }}>
          <button onClick={onClose} style={{ marginRight: 8 }}>Cancel</button>
          <button 
            onClick={() => onSave(text)} 
            disabled={saving} 
            style={{ 
              background: '#38a169', 
              color: '#fff', 
              padding: '6px 16px', 
              borderRadius: 4 
            }}
          >
            {saving ? 'Saving...' : 'Save to Session'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function MeaningOracle({ chaos: _chaos }: MeaningOracleProps) {
  const [question, setQuestion] = useState('');
  const [tables, setTables] = useState<string[]>([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [output, setOutput] = useState('');
  const [flavorData, setFlavorData] = useState<{
    question: string;
    keywords: string[];
  } | null>(null);
  const [flavorText, setFlavorText] = useState('');
  const [loading, setLoading] = useState(false);
  const [showLogModal, setShowLogModal] = useState(false);
  const [logError, setLogError] = useState<string | null>(null);
  const [logSaving, setLogSaving] = useState(false);

  useEffect(() => {
    // Note: This endpoint might need to be added to the OracleAPI class
    // For now, using the old API pattern until we add it
    fetch('/oracle/meaning/tables')
      .then(response => response.json())
      .then((data: APIResponse<string[]>) => {
        if (data.success && data.data) {
          setTables(data.data);
        } else {
          console.error("Failed to fetch tables:", data.error);
          setTables([]);
        }
      })
      .catch(error => {
        console.error("Error fetching tables:", error);
        setTables([]);
      });
  }, []);

  const handleMeaning = async () => {
    if (!question.trim()) {
      setOutput('Error: Please enter a question');
      return;
    }

    if (!selectedTable) {
      setOutput('Error: Please select a table');
      return;
    }

    setLoading(true);
    setFlavorData(null);
    setOutput('');
    setFlavorText('');
    
    try {
      const response = await OracleAPI.meaningOracle('dnd5e', question);
      
      if (response.success && response.data) {
        const data = response.data as MeaningResult;
        setOutput(`Key words: ${data.keywords.join(', ')}\nRolls: ${data.rolls.join(', ')}`);
        setFlavorData({ question, keywords: data.keywords });
      } else {
        console.error("Failed to get meaning:", response.error);
        setOutput(`Error: ${response.error || 'Failed to get meaning'}`);
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
      // Note: This endpoint might need to be added to the OracleAPI class
      // For now, using the old API pattern until we add it
      const response = await fetch('/oracle/meaning/flavor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(flavorData)
      });
      
      const data = await response.json() as APIResponse<FlavorResult>;
      
      if (data.success && data.data) {
        setOutput((prev) => `${prev}\n\n${data.data!.narration}`);
        setFlavorText(data.data!.narration);
        setFlavorData(null);
      } else {
        console.error("Failed to get flavor:", data.error);
        setOutput((prev) => `${prev}\n\nError: Failed to generate flavor text`);
      }
    } catch (error) {
      console.error("Failed to fetch flavor for meaning:", error);
      setOutput((prev) => `${prev}\n\nError: Failed to generate flavor text`);
    } finally {
      setLoading(false);
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
      // Note: This endpoint might need to be added to a SessionAPI class
      // For now, using the old API pattern until we add it
      const response = await fetch('/session/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text, type: 'oracle' })
      });
      
      const data = await response.json() as APIResponse<any>;
      
      if (data.success) {
        setShowLogModal(false);
      } else {
        console.error("Failed to save log:", data.error);
        setLogError('Failed to save log.');
      }
    } catch (error) {
      console.error("Error saving log:", error);
      setLogError('Failed to save log.');
    } finally {
      setLogSaving(false);
    }
  };

  const logText = output ? 
    `Oracle Question: ${question}\n\n${output}${flavorText ? `\n\n${flavorText}` : ''}` : 
    '';

  return (
    <section style={{ marginBottom: '2em' }}>
      <h2>Meaning Oracle</h2>

      <label>
        Question:
        <input 
          value={question} 
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Enter your question..."
        />
      </label>

      <label>
        Table:
        <select value={selectedTable} onChange={(e) => setSelectedTable(e.target.value)}>
          <option value="">Select a table...</option>
          {tables.map((table) => (
            <option key={table} value={table}>{table}</option>
          ))}
        </select>
      </label>

      <button onClick={handleMeaning} disabled={loading || !question.trim() || !selectedTable}>
        {loading ? 'Getting Meaning...' : 'Get Meaning'}
      </button>
      
      {flavorData && (
        <button onClick={handleFlavor} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Flavor'}
        </button>
      )}
      
      {loading && <div className="loader">Generating...</div>}

      <pre style={{
        background: '#222',
        padding: '1em',
        marginTop: '1em',
        borderLeft: '4px solid #6b46c1',
        whiteSpace: 'pre-wrap'
      }}>
        {output}
      </pre>

      {output && (
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