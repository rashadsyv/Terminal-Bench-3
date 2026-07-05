FROM python:3.11-slim-bookworm

RUN pip install --no-cache-dir pytest

# Bake tests into the image — Harbor does NOT upload tests/ at verify time
COPY . /tests/

# Fix line endings in case files were created on Windows
RUN sed -i 's/\r$//' /tests/test.sh

# Pre-create the artifact directory so Harbor's upload does not fail
RUN mkdir -p /app
