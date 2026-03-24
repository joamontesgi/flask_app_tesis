import { useState } from "react";
import { runMonitor } from "../api.js";
import PredictionCharts from "../components/PredictionCharts.jsx";

export default function Monitor() {
  const [form, setForm] = useState({
    interface: "",
    seconds_per_capture: 30,
    max_cycles: 50,
    use_sudo: true,
    twilio_account_sid: "",
    twilio_auth_token: "",
    twilio_from: "",
    twilio_to: "",
    alert_message: "Posible ataque DDoS detectado en el monitoreo.",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function setField(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await runMonitor({
        interface: form.interface,
        seconds_per_capture: Number(form.seconds_per_capture),
        max_cycles: Number(form.max_cycles),
        use_sudo: form.use_sudo,
        twilio_account_sid: form.twilio_account_sid,
        twilio_auth_token: form.twilio_auth_token,
        twilio_from: form.twilio_from,
        twilio_to: form.twilio_to,
        alert_message: form.alert_message,
      });
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
        <h1>Monitoreo con alerta</h1>
        <p className="lede">
          El gateway orquesta captura → inferencia CNN → Twilio cuando hay tráfico de ataque
          (misma política que el demonio original). La petición HTTP puede tardar varios ciclos.
        </p>
      </header>

      <form className="form two-col" onSubmit={onSubmit}>
        <label className="field">
          <span>Interfaz</span>
          <input value={form.interface} onChange={(e) => setField("interface", e.target.value)} required />
        </label>
        <label className="field">
          <span>Segundos por captura</span>
          <input
            type="number"
            min={1}
            value={form.seconds_per_capture}
            onChange={(e) => setField("seconds_per_capture", e.target.value)}
          />
        </label>
        <label className="field">
          <span>Máx. ciclos</span>
          <input
            type="number"
            min={1}
            value={form.max_cycles}
            onChange={(e) => setField("max_cycles", e.target.value)}
          />
        </label>
        <label className="field checkbox">
          <input
            type="checkbox"
            checked={form.use_sudo}
            onChange={(e) => setField("use_sudo", e.target.checked)}
          />
          <span>Usar sudo</span>
        </label>
        <label className="field">
          <span>Twilio Account SID</span>
          <input value={form.twilio_account_sid} onChange={(e) => setField("twilio_account_sid", e.target.value)} required />
        </label>
        <label className="field">
          <span>Twilio Auth Token</span>
          <input
            type="password"
            value={form.twilio_auth_token}
            onChange={(e) => setField("twilio_auth_token", e.target.value)}
            required
          />
        </label>
        <label className="field">
          <span>From (número Twilio)</span>
          <input value={form.twilio_from} onChange={(e) => setField("twilio_from", e.target.value)} required />
        </label>
        <label className="field">
          <span>To (destino)</span>
          <input value={form.twilio_to} onChange={(e) => setField("twilio_to", e.target.value)} required />
        </label>
        <label className="field wide">
          <span>Mensaje SMS</span>
          <input value={form.alert_message} onChange={(e) => setField("alert_message", e.target.value)} />
        </label>
        <div className="wide">
          <button className="btn primary" type="submit" disabled={loading}>
            {loading ? "Ejecutando bucle…" : "Iniciar monitoreo"}
          </button>
        </div>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {result?.prediction ? (
        <>
          <p className="success">
            Alerta enviada. Basename: <code>{result.basename}</code> · Fecha: {result.fecha}
          </p>
          <PredictionCharts prediction={result.prediction} />
        </>
      ) : null}
    </div>
  );
}
