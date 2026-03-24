import { useState } from "react";
import { predictCsv } from "../api.js";
import PredictionCharts from "../components/PredictionCharts.jsx";

export default function Predict() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!file) {
      setError("Selecciona un archivo CSV.");
      return;
    }
    setLoading(true);
    try {
      const data = await predictCsv(file);
      setResult(data);
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Predicción sobre CSV</h1>
        <p className="lede">El gateway reenvía el archivo al microservicio ML (CNN + DNN).</p>
      </header>

      <form className="form" onSubmit={onSubmit}>
        <label className="field">
          <span>Archivo CSV (CICFlowMeter)</span>
          <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </label>
        <button className="btn primary" type="submit" disabled={loading}>
          {loading ? "Analizando…" : "Ejecutar modelos"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {result ? (
        <>
          <div className="metrics">
            <Metric title="CNN — benignos" value={result.cnn?.counts?.benign} />
            <Metric title="CNN — DDoS" value={result.cnn?.counts?.ddos} />
            <Metric title="DNN — benignos" value={result.dnn?.counts?.benign} />
            <Metric title="DNN — DDoS" value={result.dnn?.counts?.ddos} />
          </div>
          <PredictionCharts prediction={result} />
        </>
      ) : null}
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="metric">
      <div className="metric__label">{title}</div>
      <div className="metric__value">{value ?? "—"}</div>
    </div>
  );
}
