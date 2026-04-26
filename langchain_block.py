from __future__ import annotations

import os
from typing import Any


def _openai_chat_model_name() -> str:
    return (
        os.environ.get("OPENAI_CHAT_MODEL")
        or os.environ.get("LANGCHAIN_BLOCK_MODEL")
        or "gpt-4o"
    )


def _generate_advisory_report(
    model: str,
    summary: str,
    malicious_ips: list[str],
) -> str:
    """Genera informe usando OpenAI directamente (más fiable que LangChain)."""

    try:
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return "❌ OPENAI_API_KEY no configurada"

        client = OpenAI(api_key=api_key)

        print("🔑 API KEY detectada:", api_key[:10], "...")
        print("🤖 Modelo usado:", model)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un analista de ciberseguridad. Respondes en español, claro y profesional. "
                        "Esta aplicación no bloquea tráfico ni ejecuta comandos en firewall."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Resultados de los modelos ML (CNN y DNN): {summary}\n\n"
                        f"IPs sospechosas: {malicious_ips}\n\n"
                        "Redacta un informe de 3 a 5 párrafos que incluya:\n"
                        "1. Interpretación del tráfico\n"
                        "2. Evaluación del riesgo\n"
                        "3. Posible recomendación de bloqueo (sin ejecutarlo)\n"
                        "4. Otras medidas de seguridad\n\n"
                        "IMPORTANTE: No afirmes que se ejecutó ningún bloqueo."
                    ),
                },
            ],
        )

        print("🔎 RESPUESTA RAW:", response)

        content = response.choices[0].message.content

        if not content:
            return "⚠️ El modelo respondió vacío."

        return content.strip()

    except Exception as e:
        print("❌ ERROR REAL DEL LLM:", e)
        return f"❌ Error real del LLM ({model}): {str(e)}"


def run_langchain_blocking(
    malicious_ips: list[str],
    prediction_summary: str | None = None,
) -> dict[str, Any]:
    """
    Genera recomendaciones con el LLM.
    ❗ No bloquea IPs ni ejecuta acciones reales.
    """

    print("🚀 Ejecutando análisis LLM...")

    if not malicious_ips:
        return {
            "mode": "skipped",
            "actions": [],
            "message": "No hay IPs asociadas a tráfico sospechoso.",
            "llm_narrative": "No se generó informe porque no hay IPs sospechosas.",
        }

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or not api_key.strip():
        return {
            "mode": "missing_api_key",
            "actions": [],
            "message": "Configura OPENAI_API_KEY.",
            "llm_narrative": "❌ Falta OPENAI_API_KEY",
        }

    summary = prediction_summary or ""
    model = _openai_chat_model_name()

    print("📊 Summary:", summary)
    print("🌐 IPs:", malicious_ips)

    actions = [
        {
            "ip": ip,
            "result": "Posible contramedida (no aplicada): evaluar bloqueo en firewall/ACL.",
            "mode": "recomendación",
        }
        for ip in malicious_ips
    ]

    result: dict[str, Any] = {
        "mode": "recomendacion",
        "model": model,
        "actions": actions,
        "message": "No hay bloqueo automático. Solo recomendaciones.",
        "llm_narrative": "",
        "pdf_static_path": None,
    }

    # 🔥 Generación REAL (sin silencios)
    result["llm_narrative"] = _generate_advisory_report(
        model, summary, malicious_ips
    )

    print("\n🧠 NARRATIVA GENERADA:\n")
    print(result["llm_narrative"])
    print("\n" + "=" * 60)

    # 📄 PDF opcional
    try:
        if result["llm_narrative"] and not result["llm_narrative"].startswith("❌"):
            from block_report_pdf import build_block_report_pdf

            result["pdf_static_path"] = build_block_report_pdf(
                result["llm_narrative"],
                summary,
                malicious_ips,
                actions,
                model,
            )

            print("📄 PDF generado:", result["pdf_static_path"])

    except Exception as e:
        print("⚠️ ERROR generando PDF:", e)

    return result