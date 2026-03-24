import { NavLink, Outlet } from "react-router-dom";

const linkClass = ({ isActive }) =>
  "nav-link" + (isActive ? " nav-link--active" : "");

export default function Layout() {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand__mark" />
          <div>
            <div className="brand__title">DDoS Lab</div>
            <div className="brand__sub">CNN · DNN · PCAP</div>
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/" end className={linkClass}>
            Inicio
          </NavLink>
          <NavLink to="/predict" className={linkClass}>
            Predicción CSV
          </NavLink>
          <NavLink to="/capture" className={linkClass}>
            Captura
          </NavLink>
          <NavLink to="/convert" className={linkClass}>
            PCAP → CSV
          </NavLink>
          <NavLink to="/monitor" className={linkClass}>
            Monitoreo + alerta
          </NavLink>
        </nav>
        <p className="hint">
          Frontend React · Gateway Flask orquesta microservicios ML, captura y Twilio.
        </p>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
