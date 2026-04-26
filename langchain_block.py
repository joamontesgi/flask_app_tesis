"""
Integración LangChain + OpenAI ChatGPT (API moderna).
- No se ejecuta bloqueo en firewall ni se modifica el sistema: solo análisis asistido.
- El LLM describe el contexto del modelo ML y sugiere posibles acciones.
"""

from __future__ import annotations

import os
from typing import Any


def _openai_chat_model_name() -> str:
    return (
        os.environ.get("OPENAI_CHAT_MODEL")
        or os.environ.get("LANGCHAIN_BLOCK_MODEL")
        or "gpt-4o-mini"
    )


def _extract_text_from_response(out) -> str:
    """Soporta múltiples formatos de salida."""
    if not out:
        return ""

    content = getattr(out, "content", "")

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        return "\n".join(texts).strip()

    return ""


def _generate_advisory_report(
    model: str,
    summary: str,
    malicious_ips: list[str],
) -> str:
    """Genera informe con LLM (robusto y compatible)."""

    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    from openai import OpenAI

    # ✅ Cliente moderno (evita bug de proxies)
    client = OpenAI()

    llm = ChatOpenAI(
        model=model,
        temperature=0.2,
        max_tokens=800,
        client=client,  # 🔥 FIX CLAVE
    )

    msgs = [
        SystemMessage(
            content=(
                "Eres un analista de ciberseguridad. Respondes en español, claro y profesional. "
                "No ejecutas acciones reales, solo das recomendaciones."
            )
        ),
        HumanMessage(
            content=(
                f"Resultados ML: {summary}\n\n"
                f"IPs sospechosas: {malicious_ips}\n\n"
                "Genera un informe de 3 a 5 párrafos que incluya:\n"
                "1. Evaluación del tráfico\n"
                "2. Riesgos\n"
                "3. Recomendación sobre bloqueo (sin ejecutarlo)\n"
                "4. Otras medidas\n\n"
                "Responde SIEMPRE con texto."
            )
        ),
    ]

    try:
        out = llm.invoke(msgs)

        print("LLM RAW:", out)  # debug

        text = _extract_text_from_response(out)

        if not text:
            return "No se pudo generar narrativa (respuesta vacía)."

        return text

    except Exception as e:
        print("ERROR LLM:", str(e))
        return f"Error generando narrativa: {str(e)}"


def run_langchain_blocking(
    malicious_ips: list[str],
    prediction_summary: str | None = None,
) -> dict[str, Any]:
    """Pipeline principal (sin acciones reales en red)."""

    if not malicious_ips:
        return {
            "mode": "skipped",
            "actions": [],
            "message": "No hay IPs sospechosas.",
        }

    if not (os.environ.get("OPENAI_API_KEY") or "").strip():
        return {
            "mode": "missing_api_key",
            "actions": [],
            "message": "Falta OPENAI_API_KEY.",
        }

    summary = prediction_summary or ""
    model = _openai_chat_model_name()

    actions = [
        {
            "ip": ip,
            "result": (
                "Posible contramedida: evaluar bloqueo en firewall o contención manual."
            ),
            "mode": "recomendación",
        }
        for ip in malicious_ips
    ]

    result: dict[str, Any] = {
        "mode": "recomendacion",
        "model": model,
        "actions": actions,
        "message": "Sistema sin bloqueo automático (solo recomendación).",
        "llm_narrative": "",
        "pdf_static_path": None,
    }

    try:
        narrative = _generate_advisory_report(model, summary, malicious_ips)
        result["llm_narrative"] = narrative
    except Exception as e:
        result["llm_narrative"] = f"Error: {str(e)}"

    try:
        if result.get("llm_narrative"):
            from block_report_pdf import build_block_report_pdf

            result["pdf_static_path"] = build_block_report_pdf(
                result["llm_narrative"],
                summary,
                malicious_ips,
                actions,
                model,
            )
    except Exception as e:
        print("ERROR PDF:", str(e))

    return result