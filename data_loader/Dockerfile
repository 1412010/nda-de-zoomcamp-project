# Use Python base image
FROM python:3.12

# Install dependencies
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

# Set working directory
WORKDIR /app

# Copy script and CSV file
COPY load_data.py .
COPY data ./data

# Run the script when the container starts
ENTRYPOINT ["python", "load_data.py"]