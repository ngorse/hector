# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 5555

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5555
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True
ENV LLM_PROTOCOL=http
ENV LLM_HOST=host.docker.internal
ENV LLM_PORT=11434
ENV LLM_MODEL=llama3.2

# Run the Flask application
CMD ["flask", "run"]
