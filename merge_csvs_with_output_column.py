#!/usr/bin/env python3
"""
Lee todos los .csv bajo una carpeta (recursivo), los une en un solo CSV
y añade una columna según el nombre del archivo:

  - Columna "salida"
  - Elimina cualquier columna existente llamada "salida" en los CSV
  - Ignora filas donde "salida" sería NaN
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def label_from_filename(stem: str) -> str:
    """
    Extrae el nombre del sitio desde el nombre del archivo.
    Ej:
      www.cloudflare.com_algo.csv -> cloudflare
      stackoverflow.com_algo.csv -> stackoverflow
    """
    host_part = stem.split("_", 1)[0]
    labels = [p for p in host_part.split(".") if p]

    while labels and labels[0].lower() == "www":
        labels = labels[1:]

    if not labels:
        return host_part

    return labels[0]


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Une CSVs y añade la columna "salida" (sin NaN).'
    )
    parser.add_argument(
        "root",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Carpeta raíz donde buscar *.csv (por defecto: .)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("merged_flows.csv"),
        help="Archivo CSV de salida (por defecto: merged_flows.csv)",
    )
    parser.add_argument(
        "--site-column",
        default="salida",
        help='Nombre de la columna (por defecto: "salida")',
    )
    parser.add_argument(
        "--exclude-merged",
        action="store_true",
        help="No incluir el propio archivo de salida si está bajo la misma raíz",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    out_path = args.output if args.output.is_absolute() else Path.cwd() / args.output
    out_path = out_path.resolve()

    if not root.is_dir():
        print(f"No es un directorio: {root}", file=sys.stderr)
        sys.exit(1)

    csv_files = sorted(root.rglob("*.csv"))
    if args.exclude_merged:
        csv_files = [p for p in csv_files if p.resolve() != out_path]

    if not csv_files:
        print(f"No se encontraron .csv bajo {root}", file=sys.stderr)
        sys.exit(1)

    base_columns: list[str] | None = None
    rows_written = 0
    files_used = 0

    with out_path.open("w", encoding="utf-8", newline="") as out_f:
        writer: csv.DictWriter | None = None

        for path in csv_files:
            try:
                with path.open("r", encoding="utf-8-sig", newline="") as inf:
                    reader = csv.DictReader(inf)
                    if not reader.fieldnames:
                        continue

                    # ❌ eliminar columna "salida" si existe
                    cols = [c for c in reader.fieldnames if c != "salida"]

                    if base_columns is None:
                        base_columns = cols
                        fieldnames_out = base_columns + [args.site_column]
                        writer = csv.DictWriter(out_f, fieldnames=fieldnames_out)
                        writer.writeheader()
                    elif cols != base_columns:
                        print(
                            f"Aviso: columnas distintas en {path}, "
                            f"se rellenan faltantes con vacío.",
                            file=sys.stderr,
                        )

                    site_val = label_from_filename(path.stem)

                    for row in reader:
                        out_row = {
                            c: (row.get(c) if row.get(c) is not None else "")
                            for c in base_columns
                        }

                        # ❌ eliminar fila si la columna salida sería NaN
                        if site_val.strip() == "":
                            continue

                        # ✅ nueva columna
                        out_row[args.site_column] = site_val
                        writer.writerow(out_row)
                        rows_written += 1

                    files_used += 1

            except OSError as e:
                print(f"No se pudo leer {path}: {e}", file=sys.stderr)

    if writer is None:
        print("No se escribió ninguna fila (CSV vacíos o ilegibles).", file=sys.stderr)
        sys.exit(1)

    print(f"Unidos {files_used} archivos, {rows_written} filas -> {out_path}")


if __name__ == "__main__":
    main()
