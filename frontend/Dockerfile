# Build stage
FROM node:18-alpine as build

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
FROM node:18-alpine

WORKDIR /app

# Copy built application
COPY --from=build /app/build ./build
COPY --from=build /app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "preview"] 