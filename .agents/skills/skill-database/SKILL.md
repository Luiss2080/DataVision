---
name: skill-database
description: Skill para modelado y gestión de bases de datos usando PostgreSQL, Prisma ORM y Redis.
---

# Instrucciones y Reglas: Base de Datos y Caché

1. **Stack Tecnológico:**
   - Relacional: PostgreSQL (Single Source of Truth).
   - ORM: Prisma (Tipado seguro E2E).
   - Caché: Redis (Manejo de sesiones distribuidas, rate-limiting, y query caching).

2. **Arquitectura de Base de Datos:**
   - Normalización hasta 3FN cuando sea posible.
   - Definir relaciones explícitas en el `schema.prisma`.
   - Utilizar índices lógicos para consultas frecuentes (ej. correos de usuario).
   - Implementar Soft Deletes (marcar como inactivo en lugar de borrar físicamente de la DB) cuando el negocio lo requiera.

3. **Reglas de Código y Prisma:**
   - No cometer queries N+1. Utilizar `include` inteligentemente.
   - Tratar la base de datos de producción como inmutable: Todos los cambios estructurales deben realizarse mediante migraciones versionadas (`prisma migrate dev`).
   - Sincronizar siempre los clientes Prisma si el esquema cambia.
