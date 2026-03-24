export default function Home() {
  return (
    <div className="page">
      <header className="page-header">
        <h1>Prototipo de detección DDoS</h1>
        <p className="lede">
          Arquitectura orientada a microservicios: inferencia (CNN/DNN), captura de tráfico,
          conversión CICFlowMeter y alertas Twilio, expuestos detrás de un API gateway para
          esta interfaz React.
        </p>
      </header>
      <section className="cards">
        <article className="card">
          <h3>Predicción</h3>
          <p>Sube un CSV de flujos y obtén conteos agregados con ambos modelos.</p>
        </article>
        <article className="card">
          <h3>Captura</h3>
          <p>Dispara capturas por interfaz (requiere Linux/WSL con tcpdump y permisos).</p>
        </article>
        <article className="card">
          <h3>Monitoreo</h3>
          <p>Bucle automático hasta detectar tráfico maligno y enviar SMS.</p>
        </article>
      </section>
    </div>
  );
}
