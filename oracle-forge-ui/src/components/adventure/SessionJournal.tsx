import { useState } from "react";
import { useGetSessionLogQuery, useAppendSessionLogMutation, LogEntry } from "@/api/sessionApi";

export default function SessionJournal() {
  const [note, setNote] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  
  // RTK Query hooks
  const { data: log = [], isLoading, error } = useGetSessionLogQuery();
  const [appendLog, { isLoading: isSaving }] = useAppendSessionLogMutation();

  const submitNote = async () => {
    if (!note.trim()) return;
    
    try {
      await appendLog({ content: note, type: "note" }).unwrap();
      setNote("");
      setStatus("Saved!");
      
      // Clear status after 2 seconds
      setTimeout(() => setStatus(null), 2000);
    } catch (error) {
      console.error("Error saving note:", error);
      setStatus("Error saving note.");
      
      // Clear error status after 3 seconds
      setTimeout(() => setStatus(null), 3000);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return timestamp?.slice(0, 19).replace('T', ' ');
  };

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">📝 Session Journal</h3>
      
      {isLoading ? (
        <div>Loading log...</div>
      ) : error ? (
        <div className="text-red-400">Error loading log entries.</div>
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
        className="mt-2 px-3 py-1 bg-green-700 text-white rounded disabled:opacity-50" 
        onClick={submitNote}
        disabled={!note.trim() || isSaving}
      >
        {isSaving ? "Saving..." : "Save Note"}
      </button>
      
      {status && <div className="mt-2 text-sm italic">{status}</div>}
    </div>
  );
} 