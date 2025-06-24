import React, { useState } from "react";
import config from "../../config";

const API_BASE = config.SERVER_URL;

export default function SessionJournal() {
  const [note, setNote] = useState("");
  const [status, setStatus] = useState(null);

  const submitNote = async () => {
    if (!note.trim()) return;
    const res = await fetch(`${API_BASE}/session/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ entry: note, type: "note" }),
    });
    const data = await res.json();
    if (data.success) {
      setNote("");
      setStatus("Saved!");
    } else {
      setStatus("Error saving note.");
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">📝 Session Journal</h3>
      <textarea
        className="w-full p-2 rounded border bg-gray-900 text-white"
        rows={4}
        placeholder="Write any thoughts, summaries, or notes..."
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />
      <button className="mt-2 px-3 py-1 bg-green-700 text-white rounded" onClick={submitNote}>
        Save Note
      </button>
      {status && <div className="mt-2 text-sm italic">{status}</div>}
    </div>
  );
}
