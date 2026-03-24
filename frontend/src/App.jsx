import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Home from "./pages/Home.jsx";
import Predict from "./pages/Predict.jsx";
import Capture from "./pages/Capture.jsx";
import Convert from "./pages/Convert.jsx";
import Monitor from "./pages/Monitor.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="predict" element={<Predict />} />
        <Route path="capture" element={<Capture />} />
        <Route path="convert" element={<Convert />} />
        <Route path="monitor" element={<Monitor />} />
      </Route>
    </Routes>
  );
}
