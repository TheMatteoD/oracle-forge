import config from "../../config"
import React from "react";
import AzgaarMap from "./AzgaarMap";
import PlayerPanel from "./PlayerPanel";
import WorldSummary from "./WorldSummary";
import SessionJournal from "./SessionJournal";
import MapUploader from "./MapUploader";

export default function SessionDashboard({ adventure }) {
  const leaveAdventure = async () => {
    await fetch(`${config.SERVER_URL}/adventures/clear`, { method: "POST" });
    localStorage.removeItem("activeAdventure");
    window.location.reload(); // Forces full state reset (simplest path)
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">📘 Session Dashboard: {adventure}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AzgaarMap adventure={adventure} />
        <MapUploader adventure={adventure} />
        <PlayerPanel />
        <WorldSummary />
        <SessionJournal />
      </div>

      <button
        onClick={leaveAdventure}
        className="mb-5 px-4 py-2 bg-red-700 text-white rounded"
      >
        Leave Adventure
      </button>     
    </div>
  );
}
