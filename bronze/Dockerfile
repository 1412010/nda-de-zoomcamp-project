FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY gcp_service_acc_key.json .
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp_service_acc_key.json"

COPY extract_to_gcs.py .
ENTRYPOINT ["python", "extract_to_gcs.py"]