import { useState } from "react";
import axios from "axios";

import Header from "./components/Header";
import UploadCard from "./components/UploadCard";
import ConfidenceBar from "./components/ConfidenceBar";
import ProbabilityCard from "./components/ProbabilityCard";
import Loader from "./components/Loader";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [probabilities, setProbabilities] = useState<Record<string, number> | null>(null);
  const [loading, setLoading] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;

  const handleFileSelect = (selected: File) => {
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setPrediction(null);
    setConfidence(null);
    setProbabilities(null);
  };

  const handleAnalyze = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      setLoading(true);

      const response = await axios.post(
        `${API_URL}/predict`,
        formData
      );

      setPrediction(response.data.prediction);
      setConfidence(response.data.confidence);
      setProbabilities(response.data.probabilities);

    } catch (err) {
      alert("Backend connection error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />

      <UploadCard
        preview={preview}
        onFileChange={handleFileSelect}
        onAnalyze={handleAnalyze}
        loading={loading}
      />

      {loading && <Loader />}

      {prediction && confidence !== null && (
        <div className="bg-white/70 backdrop-blur-lg shadow-xl rounded-3xl p-10 w-full max-w-xl mx-auto mt-12 transition-all duration-300">
          <h2 className="text-2xl font-semibold text-gray-900">
            {prediction}
          </h2>

          <ConfidenceBar confidence={confidence} />

          {probabilities && (
            <ProbabilityCard probabilities={probabilities} />
          )}
        </div>
      )}

      {/* <div className="text-center text-gray-400 text-sm mt-20 mb-10">
        Hami Yasir 24MCA1020
      </div> */}
    </div>
  );
}

export default App;
