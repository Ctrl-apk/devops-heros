FROM python:3.12-alpine

WORKDIR /app

RUN adduser -D appuser && chown -R appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

USER appuser

EXPOSE 8080

CMD ["python", "main.py"]
