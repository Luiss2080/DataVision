---
name: skill-devops
description: Skill para configuración de infraestructura, contenedores (Docker) y despliegue (CI/CD).
---

# Instrucciones y Reglas: DevOps y Despliegue

1. **Stack Tecnológico:**
   - Contenedores: Docker, Docker Compose.
   - Versionado de Infraestructura: `docker-compose.yml` local y en staging.
   - Hosting: Vercel (Frontend), AWS/Railway (Backend, PostgreSQL, Redis).

2. **Arquitectura de Infraestructura:**
   - Separación de entornos: Todo debe funcionar localmente dentro de contenedores usando `docker-compose` sin depender de instalaciones en el host (excepto Node/NPM inicial).
   - Manejo estricto de variables de entorno (usar `.env.example` en repositorios, `.env` nunca debe commitearse).
   - El Backend debe ser "Stateless" (sin estado), apoyando sus estados volátiles (sesiones) en Redis.

3. **Reglas de Docker:**
   - Usar imágenes base ligeras (ej. `node:18-alpine`).
   - Implementar builds multi-stage para reducir el tamaño final de las imágenes de producción.
   - El código en desarrollo debe usar volúmenes compartidos para `Hot-Reloading`.
