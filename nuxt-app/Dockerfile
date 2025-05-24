# Build stage
FROM node:18-alpine AS builder

# Install dependencies for building
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

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