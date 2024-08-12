# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.5.1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Create a directory for the 
WORKDIR /api

# Copy the poetry configuration files
COPY pyproject.toml poetry.lock* /api/

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY src /api/src

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Quart application
#CMD ["poetry", "run", "quart", "run", "--host", "0.0.0.0"]
CMD ["poetry", "run", "start"]
# CMD ["sh", "-c", "cd /api/src && poetry run start"]