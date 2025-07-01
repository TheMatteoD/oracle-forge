import { useState } from "react";
import config from "@/config.js";
import {
  useGetActiveAdventureQuery,
  useListCustomMapsQuery,
  useUploadCustomMapMutation,
  useUploadAzgaarMapMutation,
  useCheckAzgaarMapExistsQuery,
} from "@/api/adventureApi";

// Modes for the map viewer
const MODES = {
  AZGAAR: "azgaar",
  CUSTOM: "custom",
} as const;
type MapMode = typeof MODES[keyof typeof MODES];

export default function MapViewer() {
  // UI state
  const [visible, setVisible] = useState(false);
  const [mode, setMode] = useState<MapMode>(MODES.CUSTOM);
  const [azgaarUploadFile, setAzgaarUploadFile] = useState<File | null>(null);
  const [azgaarStatus, setAzgaarStatus] = useState<string | null>(null);
  const [customUploadFile, setCustomUploadFile] = useState<File | null>(null);
  const [customStatus, setCustomStatus] = useState<string | null>(null);
  const [customIndex, setCustomIndex] = useState(0);

  // Get the active adventure name
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;

  // RTK Query hooks for Azgaar map
  const {
    data: azgaarAvailable,
    isLoading: azgaarChecking,
    error: azgaarCheckError,
    refetch: refetchAzgaarAvailable,
  } = useCheckAzgaarMapExistsQuery(adventure!, { skip: !adventure || !visible || mode !== MODES.AZGAAR });
  const [uploadAzgaarMap, { isLoading: uploadingAzgaar }] = useUploadAzgaarMapMutation();

  // RTK Query hooks for custom maps
  const {
    data: customMaps = [],
    isLoading: customLoading,
    error: customError,
    refetch: refetchCustomMaps,
  } = useListCustomMapsQuery(adventure!, { skip: !adventure || !visible || mode !== MODES.CUSTOM });
  const [uploadCustomMap, { isLoading: uploadingCustom }] = useUploadCustomMapMutation();

  // Azgaar map upload handler
  const handleAzgaarUpload = async () => {
    if (!azgaarUploadFile || !adventure) return;
    setAzgaarStatus(null);
    try {
      const response = await uploadAzgaarMap({ adventure, file: azgaarUploadFile }).unwrap();
      if (response.success) {
        setAzgaarStatus("✅ Map uploaded!");
        refetchAzgaarAvailable();
      } else {
        setAzgaarStatus("❌ Upload failed.");
      }
    } catch {
      setAzgaarStatus("❌ Upload failed.");
    }
  };

  // Custom map upload handler
  const handleCustomUpload = async () => {
    if (!customUploadFile || !adventure) return;
    setCustomStatus(null);
    try {
      const response = await uploadCustomMap({ adventure, file: customUploadFile }).unwrap();
      if (response.success) {
        setCustomStatus("✅ Image uploaded!");
        refetchCustomMaps();
      } else {
        setCustomStatus("❌ Upload failed.");
      }
    } catch {
      setCustomStatus("❌ Upload failed.");
    }
  };

  // Gallery navigation
  const nextCustom = () => setCustomIndex(i => (i + 1) % customMaps.length);
  const prevCustom = () => setCustomIndex(i => (i - 1 + customMaps.length) % customMaps.length);

  // Reset gallery index if customMaps changes
  if (customIndex >= customMaps.length && customMaps.length > 0) {
    setCustomIndex(0);
  }

  // Loading and error states for the whole component
  if (loadingActive) return <div>Loading map viewer...</div>;
  if (errorActive) return <div className="text-red-400">Error loading active adventure.</div>;
  if (!adventure) return <div>No active adventure found.</div>;

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
              className={`px-3 py-1 rounded mr-2 ${mode === MODES.AZGAAR ? "bg-blue-700 text-white" : "bg-gray-700 text-gray-200"}`}
              onClick={() => setMode(MODES.AZGAAR)}
            >
              Azgaar Map
            </button>
            <button
              className={`px-3 py-1 rounded ${mode === MODES.CUSTOM ? "bg-blue-700 text-white" : "bg-gray-700 text-gray-200"}`}
              onClick={() => setMode(MODES.CUSTOM)}
            >
              Custom Maps
            </button>
          </div>

          {/* Azgaar Map Mode */}
          {mode === MODES.AZGAAR && (
            <div>
              {/* Azgaar map iframe (served from backend) */}
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
                      Saved map 
                    </a>
                    <span className="text-gray-300 ml-2">
                      Load this file manually in Azgaar: right click and copy link and in Azgaar: <b>Menu → Load map → From URL</b>
                    </span>
                  </>
                ) : azgaarCheckError ? (
                  <span className="text-red-400">Error checking map file.</span>
                ) : (
                  <span className="text-gray-400">No map file found for this adventure. Upload one to enable manual loading.</span>
                )}
                <div className="mt-3">
                  <input
                    type="file"
                    accept=".map"
                    onChange={e => setAzgaarUploadFile(e.target.files?.[0] || null)}
                    className="mb-2"
                  />
                  <button
                    onClick={handleAzgaarUpload}
                    disabled={!azgaarUploadFile || uploadingAzgaar}
                    className="bg-blue-700 text-white px-3 py-1 rounded ml-2"
                  >
                    {uploadingAzgaar ? "Uploading..." : "Upload Azgaar Map"}
                  </button>
                  {azgaarStatus && <div className="mt-2 text-sm italic">{azgaarStatus}</div>}
                </div>
              </div>
            </div>
          )}

          {/* Custom Maps Mode */}
          {mode === MODES.CUSTOM && (
            <div className="bg-gray-900 p-3 rounded">
              <h4 className="text-white font-semibold mb-2">Custom Map Gallery</h4>
              <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={e => setCustomUploadFile(e.target.files?.[0] || null)}
                className="mb-2"
              />
              <button
                onClick={handleCustomUpload}
                disabled={!customUploadFile || uploadingCustom}
                className="bg-blue-700 text-white px-3 py-1 rounded ml-2"
              >
                {uploadingCustom ? "Uploading..." : "Upload Image"}
              </button>
              {customStatus && <div className="mt-2 text-sm italic">{customStatus}</div>}
              <div className="mt-4">
                {customLoading ? (
                  <span className="text-gray-400">Loading images...</span>
                ) : customError ? (
                  <span className="text-red-400">Error loading custom maps.</span>
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