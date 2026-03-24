# Build estático (Vite + React)
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Rutas API relativas (/api/...) → Nginx hace proxy al gateway
ENV VITE_API_URL=

RUN npm run build

# Servir con Nginx y proxy /api → gateway
FROM nginx:1.25-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
