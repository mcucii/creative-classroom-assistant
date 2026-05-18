FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV AWS_REGION=eu-central-1
EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "app.py"]