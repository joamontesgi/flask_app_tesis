# Prototipo de detección DDoS (microservicios + React)

Arquitectura: **API Gateway (Flask)** + **ML** (CNN/DNN) + **Captura** (tcpdump/CICFlowMeter) + **Notificaciones** (Twilio), y **frontend** en React (Vite).

| Servicio              | Puerto | Descripción                          |
|-----------------------|--------|--------------------------------------|
| **Frontend (Nginx)**  | **8080** | SPA React (Docker); proxy `/api` → gateway |
| Gateway               | 8000   | CORS, `/api/v1/*`, orquestación      |
| ML                    | 8001   | `POST /predict` (CSV)                |
| Captura               | 8002   | interfaces, PCAP, conversión CSV     |
| Notificaciones        | 8003   | `POST /send` (Twilio)               |
| Frontend dev (Vite)   | 5173   | Solo ejecución local sin Docker      |

Los modelos `.h5` deben estar en la carpeta `models/` del repositorio (`cnn.h5`, `redneuronal4.h5`).

---

## Requisitos

- **Python** 3.10+ (recomendado; el ML usa TensorFlow/Keras).
- **Node.js** 18+ y **npm** (solo para el frontend).
- **Sin Docker (captura en vivo):** Linux o WSL2 con `tcpdump`, `cicflowmeter` y permisos adecuados. En Windows nativo la captura suele no estar disponible.
- **Con Docker:** Docker Engine y Docker Compose v2.

---

## Ejecución sin Docker

Abre **cuatro terminales** para los microservicios (más una quinta para el frontend). Todas las rutas son relativas a la **raíz del repositorio** (`flask_app_tesis/`).

### 1. Entornos virtuales (recomendado)

Crea un venv por servicio o uno solo con todas las dependencias instaladas (más simple para desarrollo):

```bash
# Desde la raíz del repo
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r services\gateway\requirements.txt
pip install -r services\ml_service\requirements.txt
pip install -r services\capture_service\requirements.txt
pip install -r services\notification_service\requirements.txt
```

**Linux / macOS / WSL:**

```bash
source .venv/bin/activate
pip install -r services/gateway/requirements.txt
pip install -r services/ml_service/requirements.txt
pip install -r services/capture_service/requirements.txt
pip install -r services/notification_service/requirements.txt
```

(Opcional) Copia variables de entorno:

```bash
cp .env.example .env
```

### 2. Variables de entorno (local)

En cada terminal puedes exportar las URLs de los servicios (valores por defecto ya coinciden con los puertos indicados):

**PowerShell:**

```powershell
$env:ML_SERVICE_URL = "http://127.0.0.1:8001"
$env:CAPTURE_SERVICE_URL = "http://127.0.0.1:8002"
$env:NOTIFICATION_SERVICE_URL = "http://127.0.0.1:8003"
$env:MODEL_BASE_DIR = "$(Resolve-Path .\models)"
```

**Bash:**

```bash
export ML_SERVICE_URL=http://127.0.0.1:8001
export CAPTURE_SERVICE_URL=http://127.0.0.1:8002
export NOTIFICATION_SERVICE_URL=http://127.0.0.1:8003
export MODEL_BASE_DIR="$(pwd)/models"
```

### 3. Arrancar microservicios (orden sugerido)

Trabaja siempre desde la **raíz del repositorio** para no confundir rutas. `PYTHONPATH` debe incluir:

- `services` → import `shared`
- `services/ml_service`, `services/capture_service`, etc. → import `ml_service`, `capture_service`, …

**Terminal A — ML (puerto 8001)**

Bash:

```bash
export PYTHONPATH="$(pwd)/services/ml_service:$(pwd)/services"
export PORT=8001
python -m ml_service.app
```

PowerShell:

```powershell
$root = Get-Location
$env:PYTHONPATH = "$root\services\ml_service;$root\services"
$env:PORT = "8001"
python -m ml_service.app
```

**Terminal B — Captura (puerto 8002)**

Bash:

```bash
export PYTHONPATH="$(pwd)/services/capture_service:$(pwd)/services"
export PORT=8002
python -m capture_service.app
```

PowerShell:

```powershell
$root = Get-Location
$env:PYTHONPATH = "$root\services\capture_service;$root\services"
$env:PORT = "8002"
python -m capture_service.app
```

**Terminal C — Notificaciones (puerto 8003)**

Bash:

```bash
export PYTHONPATH="$(pwd)/services/notification_service:$(pwd)/services"
export PORT=8003
python -m notification_service.app
```

PowerShell:

```powershell
$root = Get-Location
$env:PYTHONPATH = "$root\services\notification_service;$root\services"
$env:PORT = "8003"
python -m notification_service.app
```

**Terminal D — Gateway (puerto 8000)**

Bash:

```bash
export PYTHONPATH="$(pwd)/services/gateway:$(pwd)/services"
export PORT=8000
python -m gateway.app
```

PowerShell:

```powershell
$root = Get-Location
$env:PYTHONPATH = "$root\services\gateway;$root\services"
$env:PORT = "8000"
python -m gateway.app
```

### 4. Frontend React

```bash
cd frontend
npm install
npm run dev
```

Abre `http://127.0.0.1:5173`. El `vite.config.js` hace **proxy** de `/api` al gateway en `http://127.0.0.1:8000`, así que no hace falta `VITE_API_URL` en desarrollo.

Si sirves el frontend en otro host/puerto sin proxy, crea `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

### 5. Comprobar salud de los servicios

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
```

### Monolito legado (opcional)

El archivo `app.py` en la raíz es la aplicación Flask antigua con plantillas Jinja:

```bash
pip install -r requirements.txt
python app.py
```

Por defecto escucha en el puerto **5000**.

---

## Ejecución con Docker (frontend + todos los microservicios)

Desde la **raíz del repositorio** (donde está `docker-compose.yml`) se levanta **Nginx + React** y los cuatro backends. La aplicación web queda en:

**http://localhost:8080**

Las peticiones del navegador van a la misma origin (`/api/...`); Nginx hace **proxy** al gateway interno (`gateway:8000`). No hace falta configurar `VITE_API_URL` en la imagen.

### Construir y levantar todo

```bash
docker compose up --build
```

En segundo plano:

```bash
docker compose up --build -d
```

### Servicios y puertos publicados en el host

| Contenedor            | Puerto host | Uso |
|-----------------------|-------------|-----|
| **frontend**          | **8080**    | Interfaz web (entrada principal) |
| gateway               | 8000        | API directa (opcional, depuración) |
| ml-service            | 8001        | ML (opcional) |
| capture-service       | 8002        | Captura (opcional) |
| notification-service  | 8003        | Twilio (opcional) |

Para usar solo el puerto **8080**, puedes comentar o quitar los `ports` de los servicios internos en `docker-compose.yml` y dejar únicamente `frontend`.

### Ver logs

```bash
docker compose logs -f
docker compose logs -f frontend
docker compose logs -f gateway
```

### Detener y limpiar

```bash
docker compose down
```

Volúmenes nombrados (p. ej. `workspace_data`) se conservan salvo que uses:

```bash
docker compose down -v
```

**Notas**

- El servicio de **captura** en Docker usa `cap_add` para TCP dump; en **Windows** suele hacer falta **Docker Desktop** con motor Linux.
- Si el puerto **8080** está ocupado, cambia en `docker-compose.yml` la línea del frontend, por ejemplo `"8081:80"`.
- Desarrollo local del frontend **sin** Docker: `cd frontend && npm run dev` (puerto 5173) con proxy a `http://127.0.0.1:8000`, como en la sección anterior.

---

## Resumen rápido

| Modo        | Comando principal |
|------------|-------------------|
| Sin Docker | 4 terminales Python (ML, captura, notificación, gateway) + `npm run dev` en `frontend/` |
| Docker     | `docker compose up --build` en la raíz → abrir **http://localhost:8080** |
