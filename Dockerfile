FROM python:3.10-slim

# Install Playwright system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libatspi2.0-0 libx11-xcb1 libxfixes3 \
    libxkbcommon0 libxshmfence1 xvfb && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy source
COPY . .

# Expose Render port
ENV PORT=10000
EXPOSE 10000

# Start server
CMD ["python", "app.py"]

