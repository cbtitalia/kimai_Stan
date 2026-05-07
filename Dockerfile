
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY toggle_pointage.py .
CMD ["uvicorn", "toggle_pointage:app", "--host", "0.0.0.0", "--port", "8059"]
