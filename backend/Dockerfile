# Etapa 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Instalar dependencias necesarias para Prisma y pnpm
RUN apk add --no-cache openssl
RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .

# Generar cliente de Prisma y construir la app
RUN npx prisma generate
RUN pnpm build

# Etapa 2: Producción
FROM node:18-alpine

WORKDIR /app

RUN apk add --no-cache openssl

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000

# Script de inicio que corre las migraciones y arranca el server
CMD ["sh", "-c", "npx prisma migrate deploy && node dist/main"]
