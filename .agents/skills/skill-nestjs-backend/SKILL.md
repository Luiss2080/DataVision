---
name: skill-nestjs-backend
description: Skill para desarrollo backend escalable usando NestJS, TypeScript y Arquitectura Hexagonal.
---

# Instrucciones y Reglas: Backend (NestJS)

1. **Stack Tecnológico:**
   - Framework: NestJS.
   - Lenguaje: TypeScript estricto.
   - Validación: class-validator, class-transformer.
   - Documentación: @nestjs/swagger (OpenAPI).

2. **Arquitectura:**
   - Modular y orientada a dominios (Domain-Driven Design básico). Cada módulo agrupa su Controller, Service, Module, DTOs y Entities.
   - Usar Inyección de Dependencias.
   - Mantener controladores ligeros; toda la lógica de negocio debe ir en los servicios.
   - Manejo centralizado de excepciones mediante Exception Filters.

3. **Seguridad:**
   - Implementar Guards (JWT, Roles) para protección de rutas.
   - Uso obligatorio de DTOs para validación de Input.
   - Encriptación de contraseñas usando `bcrypt` antes de guardar en base de datos.

4. **Reglas de Código:**
   - Cero uso de `any` o `@ts-ignore`.
   - Nomenclatura coherente: PascalCase para clases/interfaces, camelCase para métodos/variables.
