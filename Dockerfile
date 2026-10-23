# ========================================================
# TP04: Big Data Environment Deployment Using Docker
# Application: Safecast Big Data Radiation Analyzer
# ========================================================

# 1. FROM: Specify the base image for Python runtime
FROM python:3.11-slim

# Set environment variables for unbuffered output
ENV PYTHONUNBUFFERED=1

# 2. WORKDIR: Set the working directory inside the container
WORKDIR /app

# 3. COPY: Copy project requirements, source code, and sample data
COPY requirements.txt .
COPY app.py .
COPY sample_safecast.csv .

# 4. RUN: Install dependencies inside the image during build
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for web dashboard and port mapping
EXPOSE 5000

# 5. CMD: Define default command executed when container starts
CMD ["python", "app.py"]
