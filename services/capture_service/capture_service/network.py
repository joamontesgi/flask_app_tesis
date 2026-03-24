"""Listado de interfaces de red multiplataforma."""

from __future__ import annotations

import os
import platform
from typing import List


class NetworkInterfaceLister:
    def list_interfaces(self) -> List[str]:
        if platform.system() == "Linux" and os.path.isdir("/sys/class/net"):
            return sorted(os.listdir("/sys/class/net"))
        try:
            import netifaces as ni

            return list(ni.interfaces())
        except Exception:
            return []
