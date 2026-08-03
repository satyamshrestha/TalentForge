FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -m appuser \
    && chown -R appuser:appuser /app


USER appuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]