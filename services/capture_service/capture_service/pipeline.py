"""Captura y exportación de flujos (tcpdump + cicflowmeter)."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from capture_service.security import assert_safe_iface


@dataclass
class CaptureArtifacts:
    basename: str
    pcap_path: str
    csv_path: str


class TrafficCapturePipeline:
    def __init__(self, workdir: Path, captures_dir: Optional[Path] = None) -> None:
        self._workdir = workdir
        self._captures = captures_dir or (workdir / "captures")
        self._workdir.mkdir(parents=True, exist_ok=True)
        self._captures.mkdir(parents=True, exist_ok=True)

    @property
    def workdir(self) -> Path:
        return self._workdir

    def csv_path(self, basename: str) -> Path:
        if not basename or "/" in basename or "\\" in basename or ".." in basename:
            raise ValueError("basename inválido")
        return self._workdir / f"{basename}.csv"

    def capture_and_export_flows(
        self,
        interface: str,
        seconds: int,
        use_sudo: bool = True,
    ) -> CaptureArtifacts:
        assert_safe_iface(interface)
        if seconds < 1 or seconds > 3600:
            raise ValueError("Duración debe estar entre 1 y 3600 segundos.")
        basename = datetime.now().strftime("%Y%m%d-%H%M%S")
        pcap_file = self._workdir / f"{basename}.pcap"
        timeout_bin = shutil.which("timeout")
        tcpdump_bin = shutil.which("tcpdump")
        if not tcpdump_bin:
            raise RuntimeError("tcpdump no está instalado o no está en PATH (típico en Linux/WSL).")
        if platform.system() == "Linux" and use_sudo and timeout_bin:
            cmd = [
                "sudo",
                timeout_bin,
                str(seconds),
                tcpdump_bin,
                "-i",
                interface,
                "-w",
                str(pcap_file),
            ]
        elif timeout_bin:
            cmd = [timeout_bin, str(seconds), tcpdump_bin, "-i", interface, "-w", str(pcap_file)]
        else:
            raise RuntimeError("Se requiere el comando 'timeout' para limitar la captura (p. ej. en Linux/WSL).")

        subprocess.run(cmd, check=True, cwd=str(self._workdir))
        return self.export_csv(basename)

    def export_csv(self, basename: str) -> CaptureArtifacts:
        if not basename or "/" in basename or "\\" in basename or ".." in basename:
            raise ValueError("basename inválido")
        pcap_path = self._workdir / f"{basename}.pcap"
        if not pcap_path.is_file():
            raise FileNotFoundError(f"No existe {pcap_path}")
        csv_path = self._workdir / f"{basename}.csv"
        cic = shutil.which("cicflowmeter")
        if not cic:
            raise RuntimeError("cicflowmeter no está en PATH.")
        subprocess.run(
            [cic, "-f", str(pcap_path.name), "-c", str(csv_path.name)],
            check=True,
            cwd=str(self._workdir),
        )
        return CaptureArtifacts(
            basename=basename,
            pcap_path=str(pcap_path.resolve()),
            csv_path=str(csv_path.resolve()),
        )

    def convert_uploaded_pcap(self, src_stream, filename: str) -> CaptureArtifacts:
        stem = Path(filename or "upload.pcap").stem or "upload"
        basename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{stem}"
        dest = self._workdir / f"{basename}.pcap"
        dest.write_bytes(src_stream.read())
        return self.export_csv(basename)

    def archive_artifacts(self, artifacts: CaptureArtifacts) -> None:
        for p in (artifacts.pcap_path, artifacts.csv_path):
            if os.path.isfile(p):
                shutil.move(p, self._captures / Path(p).name)

    def archive_basename(self, basename: str) -> None:
        if not basename or "/" in basename or "\\" in basename or ".." in basename:
            raise ValueError("basename inválido")
        for ext in (".pcap", ".csv"):
            p = self._workdir / f"{basename}{ext}"
            if p.is_file():
                shutil.move(str(p), self._captures / p.name)


def resolve_workspace() -> tuple[Path, Path]:
    if os.environ.get("WORKSPACE_ROOT"):
        root = Path(os.environ["WORKSPACE_ROOT"])
        captures = Path(os.environ.get("CAPTURES_DIR", root / "captures"))
        return root, captures
    repo = Path(__file__).resolve().parents[3]
    root = repo / "workspace"
    captures = repo / "captures"
    return root, captures
