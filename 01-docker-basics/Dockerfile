########## STAGE 1 — BUILDER ##########
FROM python:3.12-slim AS builder

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install uv inside builder
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Set build workspace
WORKDIR /app

# Copy only dependency files first (cache-friendly)
COPY pyproject.toml uv.lock ./

# Install dependencies in a virtual environment inside /app/.venv
RUN uv sync --frozen --no-dev

# Copy source code & assets AFTER dependencies
COPY src ./src
COPY start.sh .
COPY pdfs ./pdfs



########## STAGE 2 — RUNTIME ##########
FROM python:3.12-slim AS runtime

# Working directory inside runtime image
WORKDIR /app

# Copy only the .venv built previously (optimized, safe)
COPY --from=builder /app/.venv ./.venv

# Copy your application code
COPY --from=builder /app/src ./src
COPY --from=builder /app/start.sh .
COPY --from=builder /app/pdfs ./pdfs

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["bash", "start.sh"]
