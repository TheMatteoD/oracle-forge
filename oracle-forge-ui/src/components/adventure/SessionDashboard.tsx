import { useState } from "react";
import PlayerPanel from "./PlayerPanel";
import WorldSummary from "./WorldSummary";
import SessionJournal from "./SessionJournal";
import MapViewer from "./MapViewer";
import { useEndSessionMutation } from "@/api/sessionApi";
import { useGetActiveAdventureQuery, useGetAdventureQuery } from "@/api/adventureApi";

export default function SessionDashboard() {
  const [ending, setEnding] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [mdLink, setMdLink] = useState<string | null>(null);
  const [endSession] = useEndSessionMutation();

  // Get the active adventure name
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const activeAdventureName = activeData?.active;

  // Fetch the full adventure data
  const { data: adventure, isLoading: loadingAdventure, error: errorAdventure } = useGetAdventureQuery(activeAdventureName!, { skip: !activeAdventureName });

  if (loadingActive || loadingAdventure) {
    return <div>Loading session dashboard...</div>;
  }
  if (errorActive || errorAdventure) {
    return <div className="text-red-400">Error loading adventure data.</div>;
  }
  if (!adventure) {
    return <div>No active adventure found.</div>;
  }

  const leaveAdventure = async () => {
    try {
      await endSession().unwrap();
      localStorage.removeItem("activeAdventure");
      window.location.reload(); // Forces full state reset (simplest path)
    } catch (error) {
      console.error("Failed to leave adventure:", error);
    }
  };

  const handleEndSession = async () => {
    setEnding(true);
    setError(null);
    setSummary(null);
    setMdLink(null);
    try {
      const data = await endSession().unwrap();
      if (data && data.summary) {
        setSummary(data.summary);
        setMdLink(`/vault/adventures/${adventure.name}/sessions/session_01.md`); // This assumes session_01 is active
      } else {
        setError(data?.error || "Failed to end session.");
      }
    } catch (e: any) {
      setError(e.data?.error || e.message || "Failed to end session.");
    } finally {
      setEnding(false);
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">📘 Session Dashboard: {adventure.name}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MapViewer />
        {/* <PlayerPanel adventure={adventure.name} />
        <WorldSummary adventure={adventure.name} /> */}
        {/* <SessionJournal /> */}
      </div>

      <div className="flex gap-4 mt-6 mb-5">
        <button
          onClick={leaveAdventure}
          className="px-4 py-2 bg-red-700 text-white rounded"
        >
          Leave Adventure
        </button>
        <button
          onClick={handleEndSession}
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