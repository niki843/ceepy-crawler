# Use the latest Python image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the FastAPI application code
COPY /app/ ./app/

# Copy dependencies file
COPY requirements.txt ./

# Copy alembic.ini file
COPY alembic.ini ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install && playwright install-deps

# Expose the FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]