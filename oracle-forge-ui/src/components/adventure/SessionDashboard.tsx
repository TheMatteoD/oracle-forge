import { useState } from "react";
import PlayerPanel from "./PlayerPanel";
import WorldSummary from "./WorldSummary";
import SessionJournal from "./SessionJournal";
import MapViewer from "./MapViewer";
import type { Adventure } from '@/types/api';

interface SessionDashboardProps {
  adventure: Adventure;
}

export default function SessionDashboard({ adventure }: SessionDashboardProps) {
  const [ending, setEnding] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [mdLink, setMdLink] = useState<string | null>(null);

  const leaveAdventure = async () => {
    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      await fetch('/adventures/clear', { method: "POST" });
      localStorage.removeItem("activeAdventure");
      window.location.reload(); // Forces full state reset (simplest path)
    } catch (error) {
      console.error("Failed to leave adventure:", error);
    }
  };

  const endSession = async () => {
    setEnding(true);
    setError(null);
    setSummary(null);
    setMdLink(null);
    
    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      const res = await fetch('/session/end', { method: "POST" });
      const data = await res.json();
      
      if (data.success) {
        setSummary(data.summary);
        // Try to guess the markdown file path
        setMdLink(`/vault/adventures/${adventure.name}/sessions/session_01.md`); // This assumes session_01 is active
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
      <h2 className="text-xl font-bold mb-4">📘 Session Dashboard: {adventure.name}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MapViewer adventure={adventure.name} />
        <PlayerPanel adventure={adventure.name} />
        <WorldSummary adventure={adventure.name} />
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
            <a 
              href={mdLink} 
              download 
              className="text-blue-400 underline mt-2 inline-block"
            >
              Download Markdown
            </a>
          )}
        </div>
      )}
    </div>
  );
} 