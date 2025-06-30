import { useState, useEffect } from "react";

interface LogEntry {
  timestamp: string;
  type: string;
  content: string;
}

export default function SessionJournal() {
  const [note, setNote] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [log, setLog] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchLog = async () => {
    setLoading(true);
    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      const response = await fetch('/session/log');
      const data = await response.json();
      
      if (data.success) {
        setLog(Array.isArray(data.data) ? data.data : []);
      } else {
        console.error("Failed to fetch log:", data.error);
        setLog([]);
      }
    } catch (error) {
      console.error("Error fetching log:", error);
      setLog([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLog();
  }, []);

  const submitNote = async () => {
    if (!note.trim()) return;
    
    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      const response = await fetch('/session/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: note, type: "note" })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setNote("");
        setStatus("Saved!");
        fetchLog();
      } else {
        console.error("Failed to save note:", data.error);
        setStatus("Error saving note.");
      }
    } catch (error) {
      console.error("Error saving note:", error);
      setStatus("Error saving note.");
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return timestamp?.slice(0, 19).replace('T', ' ');
  };

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">📝 Session Journal</h3>
      
      {loading ? (
        <div>Loading log...</div>
      ) : (
        <div className="mb-3 max-h-48 overflow-y-auto bg-gray-900 p-2 rounded">
          {log.length === 0 && (
            <div className="text-gray-400">No log entries yet.</div>
          )}
          {log.map((entry, i) => (
            <div key={i} className="mb-2 border-b border-gray-700 pb-1">
              <span className="text-xs text-gray-400">
                [{formatTimestamp(entry.timestamp)}] 
              </span>
              <span className="text-xs text-purple-300">[{entry.type}]</span>
              <div className="ml-2">{entry.content}</div>
            </div>
          ))}
        </div>
      )}
      
      <textarea
        className="w-full p-2 rounded border bg-gray-900 text-white"
        rows={3}
        placeholder="Write any thoughts, summaries, or notes..."
        value={note}
        onChange={(e) => setNote(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && e.ctrlKey && submitNote()}
      />
      
      <button 
        className="mt-2 px-3 py-1 bg-green-700 text-white rounded" 
        onClick={submitNote}
        disabled={!note.trim()}
      >
        Save Note
      </button>
      
      {status && <div className="mt-2 text-sm italic">{status}</div>}
    </div>
  );
} 