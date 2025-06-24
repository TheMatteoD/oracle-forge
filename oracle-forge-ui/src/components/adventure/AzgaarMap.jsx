import React, { useEffect, useState } from "react";
import config from "../../config";

export default function AzgaarMap({ adventure }) {
  const [mapAvailable, setMapAvailable] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (!adventure) return;
    setChecking(true);
    fetch(`${config.SERVER_URL}/adventures/${adventure}/map_file`, { method: "HEAD" })
      .then(res => setMapAvailable(res.ok))
      .catch(() => setMapAvailable(false))
      .finally(() => setChecking(false));
  }, [adventure]);

  return (
    <div className="bg-black rounded overflow-hidden p-4">
      <iframe
        src={`${config.SERVER_URL}/azgaar/index.html`}
        title="Azgaar Map"
        width="100%"
        height="800"
        style={{ border: "none" }}
      />
      <div className="mt-4 bg-gray-900 p-3 rounded">
        <h4 className="text-white font-semibold mb-2">Azgaar Map Loader</h4>
        {checking ? (
          <span className="text-gray-400">Checking for map file...</span>
        ) : mapAvailable ? (
          <>
            <a
              href={`${config.SERVER_URL}/adventures/${adventure}/map_file`}
              download
              className="bg-blue-700 text-white px-3 py-1 rounded mr-2"
            >
              Link to the saved map
            </a>
            <span className="text-gray-300 ml-2">
              Download and load this file manually in Azgaar: <b>Menu → Load map → From .map file</b>.
              OR right click and copy link and in Azgaar: <b>Menu → Load map → From URL</b>
            </span>
          </>
        ) : (
          <span className="text-gray-400">No map file found for this adventure. Upload one to enable manual loading.</span>
        )}
      </div>
    </div>
  );
}
