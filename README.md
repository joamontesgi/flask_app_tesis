# Aplicativo de tesis — Detección DDoS (Flask + CNN/DNN)

Aplicación web para analizar tráfico (PCAP → CSV con CICFlowMeter), ejecutar modelos **CNN** y **DNN**, mostrar un dashboard con gráficas y, si hay flujos no benignos, un **informe asistido con LangChain + OpenAI (ChatGPT)** que interpreta el contexto y señala **posibles medidas** (entre ellas, valorar el **bloqueo de IPs** en el perímetro), **sin ejecutar bloqueos** desde la aplicación.

---

## 1. Requisitos previos

- **Python 3.8** (el proyecto incluye `.python-version` para pyenv).
- Herramientas del sistema (según lo que uses):
  - **tcpdump**, **sudo** — captura en tiempo real.
  - **cicflowmeter** — conversión PCAP → CSV.

### Opcional: pyenv

```bash
pyenv install 3.8.5
pyenv local 3.8.5
```

### Dependencia del sistema (ejemplo)

```bash
sudo apt-get install -y libffi-dev
```

---

## 2. Instalación

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> Si no tienes `pip` en el sistema: `sudo apt install python3-pip` o usa solo el `venv` anterior con `python3 -m venv`.

---

## 3. Variables de entorno importantes

### OpenAI / LangChain (informe tras la predicción)

Tras analizar un CSV, si el **CNN** o el **DNN** marcan flujos **no benignos** (y el CSV tiene **`src_ip`**), la app unifica las IPs de origen afectadas e invoca **ChatGPT** vía LangChain con el **resumen de conteos de ambos modelos**. No se aplican reglas de firewall desde esta app.

| Variable | Descripción |
|----------|-------------|
| `OPENAI_API_KEY` | **Obligatoria** para usar el LLM. Sin ella verás un aviso en el dashboard (`missing_api_key`). |
| `OPENAI_CHAT_MODEL` o `LANGCHAIN_BLOCK_MODEL` | Modelo de chat (por defecto `gpt-4o-mini`). Ejemplos: `gpt-4o`, `gpt-4o-mini`. |

Puedes definir la clave en un archivo **`.env`** en la raíz del proyecto (no lo subas a git). La aplicación carga las variables automáticamente al arrancar:

```env
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-4o-mini
```

O bien exportarla en la shell:

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_CHAT_MODEL="gpt-4o-mini"
```

### Informe del LLM y PDF

El LLM redacta un informe en español comparando o integrando **CNN y DNN**, las IPs implicadas y **posibles** medidas (p. ej. bloqueo perimetral), sin afirmar que se ejecutó nada. El texto se muestra en el dashboard y puede guardarse en **PDF** bajo `static/reports/`. Requiere `reportlab` (`pip install -r requirements.txt`).

---

## 4. Ejecutar la aplicación

```bash
source .venv/bin/activate
export OPENAI_API_KEY="sk-..."    # si quieres LangChain + ChatGPT activos
python app.py
```

Abre en el navegador: **http://127.0.0.1:5000** (el servidor escucha en `0.0.0.0:5000`).

---

## 5. Flujo de uso típico

1. **Inicio** — elegir interfaz si aplica.
2. **Capturar tramas** o cargar un **PCAP**.
3. **Convertir a CSV** (CICFlowMeter) si solo tienes PCAP.
4. **Analizar y obtener resultados** — subir el CSV; se muestran conteos CNN/DNN y gráficas.
5. Si hay tráfico no benigno y **`src_ip`** en el CSV, el panel **“Análisis y posibles medidas (LangChain)”** muestra IPs de interés, **recomendaciones no ejecutadas** y el **informe del LLM** (y enlace al **PDF** si se generó).

---

## 6. Otros servicios (opcional)

- **Twilio** — en modo captura en tiempo real con “demonio”, para alertas por SMS (credenciales en el formulario).
- Los modelos entrenados deben estar en la carpeta **`models/`** (`cnn.h5`, `redneuronal4.h5`, etc.).

---

## 7. Notas

- Los PDF bajo `static/reports/` se ignoran en git salvo la carpeta vacía.
- Para **uso sin internet en el navegador**, sirve copiar Bootstrap, Plotly y jsPDF a `static/` y referenciarlos en las plantillas en lugar de CDN (las plantillas actuales pueden seguir usando enlaces remotos para esas librerías).

---

## 8. Resumen rápido

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Opción A: crear .env con OPENAI_API_KEY=...
# Opción B: export OPENAI_API_KEY="sk-..."
python app.py
```
