FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    binutils \
    xxd \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

# Compile the buggy binary, then remove the source so the agent only has the binary
COPY billing.c /tmp/billing.c
RUN gcc -O0 -o /app/billing_processor /tmp/billing.c && rm /tmp/billing.c

# Generate the binary transaction test data
COPY data/generate_transactions.py /tmp/generate_transactions.py
RUN python3 /tmp/generate_transactions.py /app/transactions.bin && rm /tmp/generate_transactions.py

WORKDIR /app
