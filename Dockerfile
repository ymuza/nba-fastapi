# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code to the working directory
COPY . /app/
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application
CMD ["sh", "/app/wait-for-it.sh", "db:5432", "--", "sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
