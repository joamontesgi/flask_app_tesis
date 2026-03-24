import { useState } from "react";
import { convertPcap } from "../api.js";

export default function Convert() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!file) {
      setError("Selecciona un PCAP.");
      return;
    }
    setLoading(true);
    try {
      const data = await convertPcap(file);
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
        <h1>PCAP → CSV</h1>
        <p className="lede">Sube un PCAP; el servicio de captura ejecuta cicflowmeter de forma aislada.</p>
      </header>

      <form className="form" onSubmit={onSubmit}>
        <label className="field">
          <span>Archivo PCAP</span>
          <input type="file" accept=".pcap,.cap" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </label>
        <button className="btn primary" type="submit" disabled={loading}>
          {loading ? "Convirtiendo…" : "Convertir"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {result ? (
        <pre className="code">{JSON.stringify(result, null, 2)}</pre>
      ) : null}
    </div>
  );
}
