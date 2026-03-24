import { useEffect, useState } from "react";
import { capture, getInterfaces } from "../api.js";

export default function Capture() {
  const [ifaces, setIfaces] = useState([]);
  const [iface, setIface] = useState("");
  const [seconds, setSeconds] = useState(30);
  const [useSudo, setUseSudo] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getInterfaces()
      .then((d) => {
        const list = d.interfaces || [];
        setIfaces(list);
        if (list.length && !iface) setIface(list[0]);
      })
      .catch((e) => setError(e.message));
  }, []);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await capture({ interface: iface, seconds, useSudo });
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
        <h1>Captura en vivo</h1>
        <p className="lede">
          Llama al microservicio de captura (tcpdump + CICFlowMeter). En Windows nativo suele
          fallar: usa Linux o WSL2.
        </p>
      </header>

      <form className="form" onSubmit={onSubmit}>
        <label className="field">
          <span>Interfaz</span>
          <select value={iface} onChange={(e) => setIface(e.target.value)}>
            {ifaces.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span>Duración (segundos)</span>
          <input
            type="number"
            min={1}
            max={3600}
            value={seconds}
            onChange={(e) => setSeconds(Number(e.target.value))}
          />
        </label>
        <label className="field checkbox">
          <input type="checkbox" checked={useSudo} onChange={(e) => setUseSudo(e.target.checked)} />
          <span>Usar sudo (Linux)</span>
        </label>
        <button className="btn primary" type="submit" disabled={loading || !iface}>
          {loading ? "Capturando…" : "Iniciar captura"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {result ? (
        <pre className="code">{JSON.stringify(result, null, 2)}</pre>
      ) : null}
    </div>
  );
}
