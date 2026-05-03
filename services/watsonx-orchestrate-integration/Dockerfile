FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port 8004
EXPOSE 8004

# Set environment variables
ENV PORT=8004
ENV ORCHESTRATE_MOCK_MODE=true
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m", "app.handler"]

# Made with Bob
