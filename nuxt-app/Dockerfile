# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install dependencies for building
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package*.json ./
COPY requirements.txt .

# Install dependencies
RUN npm ci --only=production
RUN pip install --no-cache-dir -r requirements.txt

#non-root user
RUN useradd -m -u 1001 fastapi

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=nodejs:nodejs /app/.output /app/.output
COPY --from=builder --chown=nodejs:nodejs /app/package.json /app/package.json

# Switch to non-root user
USER nodejs

# Expose port (configurable via environment variable)
EXPOSE 3000

# Set environment to production
ENV NODE_ENV=production

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", ".output/server/index.mjs"]