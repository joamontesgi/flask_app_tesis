const base = () => import.meta.env.VITE_API_URL || "";

export async function getInterfaces() {
  const r = await fetch(`${base}/api/v1/interfaces`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function predictCsv(file) {
  const fd = new FormData();
  fd.append("file", file);
  const r = await fetch(`${base}/api/v1/predict`, { method: "POST", body: fd });
  if (!r.ok) {
    const t = await r.text();
    throw new Error(t);
  }
  return r.json();
}

export async function capture({ interface: iface, seconds, useSudo }) {
  const r = await fetch(`${base}/api/v1/capture`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      interface: iface,
      seconds,
      use_sudo: useSudo,
    }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function convertPcap(file) {
  const fd = new FormData();
  fd.append("file", file);
  const r = await fetch(`${base}/api/v1/convert`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function runMonitor(payload) {
  const r = await fetch(`${base}/api/v1/monitor/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
