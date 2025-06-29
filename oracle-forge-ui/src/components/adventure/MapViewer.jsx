import React, { useState, useEffect } from "react";
import { apiGet } from '../../api/apiClient';

export default function MapViewer({ adventure }) {
  const [visible, setVisible] = useState(false);
  const [mode, setMode] = useState("custom"); // 'azgaar' or 'custom'

  // Azgaar map state
  const [azgaarAvailable, setAzgaarAvailable] = useState(false);
  const [azgaarChecking, setAzgaarChecking] = useState(true);
  const [azgaarUploadFile, setAzgaarUploadFile] = useState(null);
  const [azgaarStatus, setAzgaarStatus] = useState(null);

  // Custom map state
  const [customMaps, setCustomMaps] = useState([]);
  const [customIndex, setCustomIndex] = useState(0);
  const [customUploadFile, setCustomUploadFile] = useState(null);
  const [customStatus, setCustomStatus] = useState(null);
  const [customLoading, setCustomLoading] = useState(false);

  // Check Azgaar map availability only when in Azgaar mode and visible
  useEffect(() => {
    if (!adventure || !visible || mode !== "azgaar") return;
    setAzgaarChecking(true);
    fetch(`${config.SERVER_URL}/adventures/${adventure}/map_file`, { method: "HEAD" })
      .then(res => setAzgaarAvailable(res.ok))
      .catch(() => setAzgaarAvailable(false))
      .finally(() => setAzgaarChecking(false));
  }, [adventure, azgaarStatus, visible, mode]);

  // Fetch custom maps
  const fetchCustomMaps = () => {
    if (!adventure) return;
    setCustomLoading(true);
    apiGet(`adventures/${adventure}/custom_maps`)
      .then(response => {
        if (response.success) {
          setCustomMaps(response.data || []);
          setCustomIndex(0);
        } else {
          console.error("Failed to fetch custom maps:", response.error);
          setCustomMaps([]);
        }
      })
      .catch(error => {
        console.error("Error fetching custom maps:", error);
        setCustomMaps([]);
      })
      .finally(() => setCustomLoading(false));
  };

  useEffect(() => {
    fetchCustomMaps();
  }, [adventure, customStatus]);

  // Azgaar map upload
  const uploadAzgaar = async () => {
    if (!azgaarUploadFile) return;
    const formData = new FormData();
    formData.append("file", azgaarUploadFile);
    setAzgaarStatus(null);
    try {
      const res = await fetch(`${config.SERVER_URL}/adventures/${adventure}/upload_map`, {
        method: "POST",
        body: formData,
      });
      const response = await res.json();
      if (response.success) {
        setAzgaarStatus("✅ Map uploaded!");
      } else {
        console.error("Failed to upload Azgaar map:", response.error);
        setAzgaarStatus("❌ Upload failed.");
      }
    } catch (error) {
      console.error("Error uploading Azgaar map:", error);
      setAzgaarStatus("❌ Upload failed.");
    }
  };

  // Custom map upload
  const uploadCustom = async () => {
    if (!customUploadFile) return;
    const formData = new FormData();
    formData.append("file", customUploadFile);
    setCustomStatus(null);
    try {
      const res = await fetch(`${config.SERVER_URL}/adventures/${adventure}/upload_custom_map`, {
        method: "POST",
        body: formData,
      });
      const response = await res.json();
      if (response.success) {
        setCustomStatus("✅ Image uploaded!");
        fetchCustomMaps();
      } else {
        console.error("Failed to upload custom map:", response.error);
        setCustomStatus("❌ Upload failed.");
      }
    } catch (error) {
      console.error("Error uploading custom map:", error);
      setCustomStatus("❌ Upload failed.");
    }
  };

  // Slideshow navigation
  const nextCustom = () => setCustomIndex(i => (i + 1) % customMaps.length);
  const prevCustom = () => setCustomIndex(i => (i - 1 + customMaps.length) % customMaps.length);

  return (
    <div className="bg-black rounded overflow-hidden p-4">
      <button
        className="bg-blue-700 text-white px-3 py-1 rounded mb-3"
        onClick={() => setVisible(v => !v)}
      >
        {visible ? "Hide Map" : "Show Map"}
      </button>
      {visible && (
        <div>
          <div className="mb-3">
            <button
              className={`px-3 py-1 rounded mr-2 ${mode === "azgaar" ? "bg-blue-700 text-white" : "bg-gray-700 text-gray-200"}`}
              onClick={() => setMode("azgaar")}
            >
              Azgaar Map
            </button>
            <button
              className={`px-3 py-1 rounded ${mode === "custom" ? "bg-blue-700 text-white" : "bg-gray-700 text-gray-200"}`}
              onClick={() => setMode("custom")}
            >
              Custom Maps
            </button>
          </div>
          {mode === "azgaar" && (
            <div>
              <iframe
                src={`${config.SERVER_URL}/azgaar/index.html`}
                title="Azgaar Map"
                width="100%"
                height="500"
                style={{ border: "none" }}
              />
              <div className="mt-4 bg-gray-900 p-3 rounded">
                <h4 className="text-white font-semibold mb-2">Azgaar Map Loader</h4>
                {azgaarChecking ? (
                  <span className="text-gray-400">Checking for map file...</span>
                ) : azgaarAvailable ? (
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
                <div className="mt-3">
                  <input
                    type="file"
                    accept=".map"
                    onChange={e => setAzgaarUploadFile(e.target.files[0])}
                    className="mb-2"
                  />
                  <button onClick={uploadAzgaar} className="bg-blue-700 text-white px-3 py-1 rounded ml-2">
                    Upload Azgaar Map
                  </button>
                  {azgaarStatus && <div className="mt-2 text-sm italic">{azgaarStatus}</div>}
                </div>
              </div>
            </div>
          )}
          {mode === "custom" && (
            <div className="bg-gray-900 p-3 rounded">
              <h4 className="text-white font-semibold mb-2">Custom Map Gallery</h4>
              <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={e => setCustomUploadFile(e.target.files[0])}
                className="mb-2"
              />
              <button onClick={uploadCustom} className="bg-blue-700 text-white px-3 py-1 rounded ml-2">
                Upload Image
              </button>
              {customStatus && <div className="mt-2 text-sm italic">{customStatus}</div>}
              <div className="mt-4">
                {customLoading ? (
                  <span className="text-gray-400">Loading images...</span>
                ) : customMaps.length === 0 ? (
                  <span className="text-gray-400">No custom maps uploaded yet.</span>
                ) : (
                  <div className="flex flex-col items-center">
                    <img
                      src={`${config.SERVER_URL}/adventures/${adventure}/custom_maps/${customMaps[customIndex]}`}
                      alt="Custom Map"
                      style={{ maxWidth: "100%", maxHeight: 400, borderRadius: 8, border: "2px solid #333" }}
                    />
                    <div className="mt-2 flex items-center">
                      <button
                        className="bg-gray-700 text-white px-2 py-1 rounded mr-2"
                        onClick={prevCustom}
                        disabled={customMaps.length <= 1}
                      >
                        ◀
                      </button>
                      <span className="text-gray-300">
                        {customIndex + 1} / {customMaps.length}
                      </span>
                      <button
                        className="bg-gray-700 text-white px-2 py-1 rounded ml-2"
                        onClick={nextCustom}
                        disabled={customMaps.length <= 1}
                      >
                        ▶
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 