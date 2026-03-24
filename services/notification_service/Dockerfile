FROM python:3.10-slim

WORKDIR /app

COPY services/notification_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/notification_service /app/notify_pkg

ENV PYTHONPATH=/app/notify_pkg

EXPOSE 8003

CMD ["python", "-m", "notification_service.app"]
