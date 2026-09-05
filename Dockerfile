# Use an official Python runtime as base
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Copy dependency definition files first for optimal layer caching
COPY pyproject.toml uv.lock requirements.txt ./

# Install project dependencies
RUN uv pip install --no-cache -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Healthcheck for container health monitoring
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start the Streamlit application
CMD ["uv", "run", "streamlit", "run", "src/app.py"]
