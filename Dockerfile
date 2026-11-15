# ==============================================================================
# Lucen Production Multi-Stage Dockerfile for Render Free Web Service
# Combines Next.js 15 Web Studio and FastAPI HydraDB Engine in a single container
# ==============================================================================

# Stage 1: Build Next.js Web Studio
FROM node:20-slim AS frontend-builder
WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

# Stage 2: Final Production Container with Python 3.11 and Node 20 runtime
FROM python:3.11-slim
WORKDIR /app

# Install Node.js runtime and curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and CLI source code
COPY backend/ ./backend/
COPY eval/ ./eval/
COPY tools/ ./tools/
COPY assets/ ./assets/
COPY lucen.py .
COPY run_production.py .

# Copy built Next.js frontend from frontend-builder stage
COPY --from=frontend-builder /app/web ./web

# Set production environment defaults
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production
ENV PORT=3000

# Expose Render external HTTP port
EXPOSE 3000

# Run unified supervisor
CMD ["python", "run_production.py"]
