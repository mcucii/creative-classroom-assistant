FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/start.sh

ENV AWS_REGION=eu-central-1
EXPOSE 8501 8080
CMD ["/app/start.sh"]    