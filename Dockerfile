FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install build deps (if needed) and pip deps
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libpq-dev \
	&& pip install --no-cache-dir -r requirements.txt gunicorn \
	&& apt-get remove -y build-essential \
	&& apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 80

# Use Gunicorn with Uvicorn workers; allow PORT override via $PORT
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-80} --workers 4 --log-level info"]
