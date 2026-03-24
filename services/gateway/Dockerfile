FROM python:3.10-slim

WORKDIR /app

COPY services/gateway/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/gateway /app/gateway_pkg

ENV PYTHONPATH=/app/gateway_pkg

EXPOSE 8000

CMD ["python", "-m", "gateway.app"]
