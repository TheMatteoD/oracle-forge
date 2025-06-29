import React, { useEffect, useState } from "react";
import { apiGet, apiPost } from '../../api/apiClient';


export default function GenericGenerators() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState("");
  const [result, setResult] = useState(null);
  const [flavorText, setFlavorText] = useState("");
  const [flavorNarration, setFlavorNarration] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    apiGet('/generators/categories')
      .then((res) => res.json())
      .then(setCategories);
  }, []);

  useEffect(() => {
    if (!selectedCategory) return;
    apiGet(`/generators/${selectedCategory}/files`)
      .then((res) => res.json())
      .then(setFiles);
  }, [selectedCategory]);

  useEffect(() => {
    if (!selectedCategory || !selectedFile) return;
    apiGet(`/generators/${selectedCategory}/${selectedFile}/tables`)
      .then((res) => res.json())
      .then(setTables);
  }, [selectedFile]);

  const rollTable = () => {
    apiPost('/generators/roll', {
      category: selectedCategory,
      file: selectedFile,
      table_id: selectedTable,
    })
      .then((res) => res.json())
      .then((data) => {
        setResult({ [selectedTable]: data.result || data.error });
        setFlavorNarration("");
      });
  };

  const generateFlavor = async () => {
    setLoading(true);
    try {
      const res = await apiPost('/generators/flavor', {
        context: flavorText,
        data: result,
        category: selectedCategory,
        source: `${selectedFile.replace(".yaml", "")}.${selectedTable}`,
      });
      const data = await res.json();
      setFlavorNarration(data.narration);
    } catch (err) {
      console.error("Flavor generation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-lg font-bold mb-4">Generic Table Generator</h2>

      <label>Category:</label>
      <select onChange={(e) => setSelectedCategory(e.target.value)} value={selectedCategory}>
        <option value="">-- Select --</option>
        {categories.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      {files.length > 0 && (
        <>
          <label className="block mt-4">YAML File:</label>
          <select onChange={(e) => setSelectedFile(e.target.value)} value={selectedFile}>
            <option value="">-- Select --</option>
            {files.map((file) => (
              <option key={file} value={file}>{file}</option>
            ))}
          </select>
        </>
      )}

      {tables.length > 0 && (
        <>
          <label className="block mt-4">Table:</label>
          <select onChange={(e) => setSelectedTable(e.target.value)} value={selectedTable}>
            <option value="">-- Select --</option>
            {tables.map((table) => (
              <option key={table} value={table}>{table}</option>
            ))}
          </select>

          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded" onClick={rollTable}>
            Roll Table
          </button>
        </>
      )}

      {result && (
        <div className="mt-6 p-4 bg-gray-100 rounded border">
          <h3 className="text-md font-semibold">Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>

          <textarea
            className="mt-4 w-full border p-2"
            rows={3}
            placeholder="Add flavor context (optional)..."
            value={flavorText}
            onChange={(e) => setFlavorText(e.target.value)}
          />
          <button
            className="mt-2 px-3 py-1 bg-purple-700 text-white rounded"
            onClick={generateFlavor}
          >
            Generate Flavor
          </button>
          {loading && <div className="loader mt-1 text-sm italic text-gray-600">Generating narration...</div>}
        </div>
      )}

      {flavorNarration && (
        <div className="mt-4 p-4 bg-white rounded shadow border">
          <strong>Narration:</strong>
          <p className="mt-2 whitespace-pre-wrap">{flavorNarration}</p>
        </div>
      )}
    </div>
  );
}
