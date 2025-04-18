FROM apache/airflow:2.10.5

USER root
RUN apt-get update && apt-get install -y gcc g++ curl && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

# ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/scripts"

# Install Google Cloud SDK
RUN pip install --no-cache-dir \
    apache-airflow-providers-google \
    apache-airflow-providers-celery \
    redis \
    google-cloud-storage \
    google-cloud-dataproc


# Ensure the provider is installed and available
RUN airflow info




# RUN apt-get update && apt-get install -y \
#     gcc \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
# USER airflow

# Install Google and Celery provider packages, plus Redis client
# RUN pip install --no-cache-dir \
#     apache-airflow-providers-google==10.14.0 \
#     apache-airflow-providers-celery==3.3.0 \
#     redis==5.0.1