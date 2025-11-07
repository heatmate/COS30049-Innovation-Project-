import React, { useState } from "react"
import PieData from "./components/PieData"
import HeatmapData from "./components/HeatmapData";
import "./App.css"


const baseUrl = import.meta.env.VITE_API_BASE_URL;
console.log(baseUrl);

function App() {
  const [codeSnippet, setCodeSnippet] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handlePredict = async () => {
    if (!codeSnippet.trim()) {
      setError("Please enter a snippet of your code first.");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const response = await fetch(
        `${baseUrl}/predict_v2?code_snippet=${encodeURIComponent(
          codeSnippet
        )}`
      );

      if (!response.ok) {
        throw new Error(`Server has returned ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("failed to fetch the prediction. Make sure backend is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="header">
      <h1 className="text-2xl font-bold">
        Software Vulnerability Detector
      </h1>

      <textarea
        value={codeSnippet}
        onChange={(e) => setCodeSnippet(e.target.value)}
        placeholder="Paste Code Snippet Here...."
        rows="8"
        className="w-full p-2 border rounded mb-4 font-mono"
      />

      <button
        onClick={handlePredict}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Analysing..." : "Predict Vulnerability"}
      </button>

      {error && <p className="text-red-500 mt-3">{error}</p>}

      {result && (
        <div className="mt-6 border p-4">
          <h2 className="text-lg font-semibold mb-2">Prediction result</h2>
          <p><strong>Category:</strong> {result.vulnerability_category}</p>
          <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>

          <h3 className="mt-3 font-semibold">Probabilities:</h3>
          <ul className="list-disc pl-6">
            {Object.entries(result.probabilities).map(([key, value]) => (
              <li key={key}>
                {key}: {(value * 100).toFixed(2)}%
              </li>
            ))}
          </ul>

          <div className="mt-8">
            <PieData data={result.probabilities} />
            <HeatmapData data={result.probabilities} />
          </div> 
        </div>
      )}
    </div>
  );
}

export default App;

