import { useEffect, useRef } from "react";
import Plotly from "plotly.js-dist-min";

const LABELS = [
  "Benigno",
  "DDoS",
  "GoldenEye",
  "Hulk",
  "Slowhttptest",
  "Slowloris",
];

const ORDER = [
  "benign",
  "ddos",
  "dos_goldeneye",
  "dos_hulk",
  "dos_slowhttptest",
  "dos_slowloris",
];

function series(counts) {
  return ORDER.map((k) => Number(counts?.[k] ?? 0));
}

export default function PredictionCharts({ prediction }) {
  const barCnn = useRef(null);
  const pieCnn = useRef(null);
  const barDnn = useRef(null);
  const pieDnn = useRef(null);

  useEffect(() => {
    if (!prediction) return;
    const cnn = series(prediction.cnn?.counts);
    const dnn = series(prediction.dnn?.counts);

    const barLayout = { title: "Barras", paper_bgcolor: "transparent", plot_bgcolor: "transparent" };
    const pieLayout = { title: "Distribución", paper_bgcolor: "transparent" };

    Plotly.newPlot(
      barCnn.current,
      [{ x: LABELS, y: cnn, type: "bar", marker: { color: "#5eead4" } }],
      { ...barLayout, title: "CNN — barras" },
      { responsive: true, displaylogo: false }
    );
    Plotly.newPlot(
      pieCnn.current,
      [{ labels: LABELS, values: cnn, type: "pie" }],
      { ...pieLayout, title: "CNN — pie" },
      { responsive: true, displaylogo: false }
    );
    Plotly.newPlot(
      barDnn.current,
      [{ x: LABELS, y: dnn, type: "bar", marker: { color: "#a78bfa" } }],
      { ...barLayout, title: "DNN — barras" },
      { responsive: true, displaylogo: false }
    );
    Plotly.newPlot(
      pieDnn.current,
      [{ labels: LABELS, values: dnn, type: "pie" }],
      { ...pieLayout, title: "DNN — pie" },
      { responsive: true, displaylogo: false }
    );
  }, [prediction]);

  if (!prediction) return null;

  return (
    <div className="charts-grid">
      <div ref={barCnn} className="chart" />
      <div ref={pieCnn} className="chart" />
      <div ref={barDnn} className="chart" />
      <div ref={pieDnn} className="chart" />
    </div>
  );
}
