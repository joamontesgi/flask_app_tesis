"""
Integración LangChain + OpenAI ChatGPT (API de chat).
- No se ejecuta bloqueo en firewall ni se modifica el sistema: solo análisis asistido.
- El LLM describe el contexto del modelo ML y señala que bloquear las IPs listadas es una
  posible contramedida, entre otras, a valorar por un operador humano.
- Tras la respuesta se puede generar un PDF informativo (static/reports/).
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


def _generate_advisory_report(
    model: str,
    summary: str,
    malicious_ips: list[str],
) -> str:
    """Una sola llamada al LLM: informe sin ejecutar acciones en red."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model=model, temperature=0.2)
    msgs = [
        SystemMessage(
            content=(
                "Eres un analista de ciberseguridad. Respondes en español, claro y profesional. "
                "Esta aplicación no bloquea tráfico ni ejecuta comandos en firewall: solo orientas "
                "al operador sobre interpretación y opciones de mitigación."
            )
        ),
        HumanMessage(
            content=(
                f"Resultados de los modelos ML (CNN y DNN) sobre el mismo tráfico analizado: {summary}\n\n"
                "La línea anterior resume los conteos por clase para CNN y para DNN.\n\n"
                f"Direcciones de origen (src_ip) con al menos un flujo clasificado como no benigno "
                f"por CNN o por DNN (unión de ambos): {malicious_ips}\n\n"
                "Redacta un informe de 3 a 5 párrafos que incluya:\n"
                "(1) Qué indican conjuntamente los conteos de CNN y DNN sobre el tipo de actividad; "
                "si difieren en algún aspecto, menciona discrepancias y cómo interpretarlas con cautela.\n"
                "(2) Qué implica la presencia de las IPs listadas a la luz de ambos modelos.\n"
                "(3) Que una POSIBLE medida entre varias sería bloquear esas IPs en el perímetro "
                "(firewall, ACL u otro filtro), si un operador lo considera adecuado tras revisar "
                "falsos positivos y políticas; deja claro que aquí no se ha bloqueado nada automáticamente.\n"
                "(4) Otras recomendaciones (correlación con otros logs, monitorización, incident response).\n"
                "No afirmes que se ejecutó ningún bloqueo."
            )
        ),
    ]
    out = llm.invoke(msgs)
    return (getattr(out, "content", None) or "").strip()


def run_langchain_blocking(
    malicious_ips: list[str],
    prediction_summary: str | None = None,
) -> dict[str, Any]:
    """
    Genera recomendaciones con el LLM. No bloquea IPs ni llama a iptables.
    """
    if not malicious_ips:
        return {
            "mode": "skipped",
            "actions": [],
            "message": "No hay IPs asociadas a tráfico no benigno que requieran comentario.",
        }

    if not (os.environ.get("OPENAI_API_KEY") or "").strip():
        return {
            "mode": "missing_api_key",
            "actions": [],
            "message": (
                "Configura OPENAI_API_KEY para el informe asistido con ChatGPT. "
                "Opcional: OPENAI_CHAT_MODEL (p. ej. gpt-4o-mini)."
            ),
        }

    summary = prediction_summary or ""
    model = _openai_chat_model_name()

    actions = [
        {
            "ip": ip,
            "result": (
                "Posible contramedida (no aplicada por el sistema): valorar bloqueo en "
                "firewall/ACL o contención según política del operador."
            ),
            "mode": "recomendación",
        }
        for ip in malicious_ips
    ]

    result: dict[str, Any] = {
        "mode": "recomendacion",
        "model": model,
        "actions": actions,
        "message": (
            "No hay bloqueo automático. OpenAI ChatGPT ofrece contexto y medidas posibles "
            "(incluido, si procede, bloquear IPs tras revisión humana)."
        ),
        "llm_narrative": "",
        "pdf_static_path": None,
    }

    try:
        result["llm_narrative"] = _generate_advisory_report(model, summary, malicious_ips)
    except Exception:
        pass

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
    except Exception:
        pass

    return result
