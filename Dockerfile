FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgomp1 \
    libstdc++6 \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY app /app

RUN mkdir -p /app/input /app/output /app/work

CMD ["python", "-u", "pipeline.py"]
