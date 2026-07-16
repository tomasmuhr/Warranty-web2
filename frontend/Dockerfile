# ==========================================
# STAGE 1: development (Used in development)
# ==========================================
FROM node:25-alpine AS development

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# Vite's default dev server port
EXPOSE 5173

# In development, we run the interactive dev server
CMD ["npm", "run", "dev"]

# ==========================================
# STAGE 2: builder (Intermediary compiler)
# ==========================================
FROM development AS builder
# This stage inherits everything from development and runs the static production compilation
RUN npm run build

# ==========================================
# STAGE 3: production (Used in production)
# ==========================================
FROM nginx:1.27-alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy the compiled HTML/JS from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]