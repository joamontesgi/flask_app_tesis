"""Genera PDF del informe de análisis (narrativa del LLM; sin acciones ejecutadas)."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "static" / "reports"


def build_block_report_pdf(
    llm_narrative: str,
    prediction_summary: str,
    malicious_ips: list[str],
    actions: list[dict],
    model_name: str,
) -> str:
    """
    Escribe el PDF bajo static/reports/ y devuelve la ruta relativa para url_for('static', ...).
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"informe_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = REPORTS_DIR / filename

    styles = getSampleStyleSheet()
    story: list = []
    story.append(
        Paragraph(
            escape("Informe de análisis y medidas posibles (LangChain + OpenAI ChatGPT)"),
            styles["Title"],
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        Paragraph(
            escape(
                "Este documento es informativo. El sistema no ejecuta bloqueos en firewall "
                "ni modifica la red."
            ),
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            escape(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
            styles["Normal"],
        )
    )
    story.append(Paragraph(escape(f"Modelo LLM: {model_name}"), styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph(escape("Resumen predicción (CNN y DNN)"), styles["Heading2"]))
    story.append(Paragraph(escape(prediction_summary), styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(
        Paragraph(
            escape("IPs de origen con flujos no benignos (CNN y/o DNN)"),
            styles["Heading2"],
        )
    )
    story.append(
        Paragraph(
            escape(", ".join(malicious_ips) if malicious_ips else "—"),
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.3 * cm))

    story.append(
        Paragraph(
            escape("Posibles medidas (no ejecutadas por la aplicación)"),
            styles["Heading2"],
        )
    )
    if actions:
        for a in actions:
            story.append(
                Paragraph(
                    escape(
                        f"• {a.get('ip', '?')}: {a.get('result', '')} ({a.get('mode', '')})"
                    ),
                    styles["Normal"],
                )
            )
    else:
        story.append(Paragraph(escape("(ninguna entrada)"), styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph(escape("Análisis (respuesta del LLM)"), styles["Heading2"]))
    narrative = (llm_narrative or "").strip() or "(Sin texto del modelo.)"
    for block in narrative.split("\n\n"):
        b = block.strip()
        if b:
            story.append(
                Paragraph(escape(b).replace("\n", "<br/>"), styles["Normal"]),
            )
            story.append(Spacer(1, 0.2 * cm))

    doc = SimpleDocTemplate(str(path), pagesize=A4)
    doc.build(story)
    return f"reports/{filename}"
