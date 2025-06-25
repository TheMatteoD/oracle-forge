import config from "../../config"
import React, { useState } from "react";
import PlayerPanel from "./PlayerPanel";
import WorldSummary from "./WorldSummary";
import SessionJournal from "./SessionJournal";
import MapViewer from "./MapViewer";

export default function SessionDashboard({ adventure }) {
  const [ending, setEnding] = useState(false);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [mdLink, setMdLink] = useState(null);

  const leaveAdventure = async () => {
    await fetch(`${config.SERVER_URL}/adventures/clear`, { method: "POST" });
    localStorage.removeItem("activeAdventure");
    window.location.reload(); // Forces full state reset (simplest path)
  };

  const endSession = async () => {
    setEnding(true);
    setError(null);
    setSummary(null);
    setMdLink(null);
    try {
      const res = await fetch(`${config.SERVER_URL}/session/end`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setSummary(data.summary);
        // Try to guess the markdown file path
        setMdLink(`/vault/adventures/${adventure}/sessions/session_01.md`); // This assumes session_01 is active
      } else {
        setError(data.error || "Failed to end session.");
      }
    } catch (e) {
      setError("Failed to end session.");
    } finally {
      setEnding(false);
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">📘 Session Dashboard: {adventure}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MapViewer adventure={adventure} />
        <PlayerPanel />
        <WorldSummary adventure={adventure} />
        <SessionJournal />
      </div>

      <div className="flex gap-4 mt-6 mb-5">
        <button
          onClick={leaveAdventure}
          className="px-4 py-2 bg-red-700 text-white rounded"
        >
          Leave Adventure
        </button>
        <button
          onClick={endSession}
          className="px-4 py-2 bg-purple-700 text-white rounded"
          disabled={ending}
        >
          {ending ? "Ending Session..." : "End Session"}
        </button>
      </div>
      {error && <div className="text-red-400 mb-2">{error}</div>}
      {summary && (
        <div className="bg-gray-900 p-4 rounded mt-4">
          <h3 className="text-lg font-semibold mb-2">Session Summary</h3>
          <pre className="whitespace-pre-wrap text-sm">{summary}</pre>
          {mdLink && (
            <a href={mdLink} download className="text-blue-400 underline mt-2 inline-block">Download Markdown</a>
          )}
        </div>
      )}
    </div>
  );
}
