import React, { useState } from "react";
import config from "../../config";

const API_BASE = config.SERVER_URL;

export default function MapUploader({ adventure }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);

  const upload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE}/adventures/${adventure}/upload_map`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (data.success) {
      setStatus("✅ Map uploaded!");
    } else {
      setStatus("❌ Upload failed.");
    }
  };

  return (
    <div className="bg-gray-900 p-4 rounded shadow mt-4">
      <h4 className="text-md font-semibold mb-2">🗺️ Upload Map File</h4>
      <input
        type="file"
        accept=".map"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-2"
      />
      <button onClick={upload} className="bg-blue-700 text-white px-3 py-1 rounded">
        Upload
      </button>
      <p>
      Using the map generator above, create the adventure's map and then save and upload here for safe storage and easy re-loading later! 
      </p>
      {status && <div className="mt-2 text-sm italic">{status}</div>}
    </div>
  );
}
