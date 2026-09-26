---
name: skill-nextjs-frontend
description: Skill para el desarrollo frontend escalable usando Next.js, React, TailwindCSS y Framer Motion.
---

# Instrucciones y Reglas: Frontend (Next.js)

1. **Stack Tecnológico:**
   - Framework: Next.js (App Router preferiblemente).
   - Estilos: Tailwind CSS.
   - Animaciones: Framer Motion.
   - Estado: Zustand (para estado global simple) o Context API.
   - Tipado: TypeScript estricto.

2. **Arquitectura del Frontend:**
   - Mantener componentes pequeños y reutilizables en carpetas como `/components/ui`, `/components/layout`, `/components/forms`.
   - Utilizar Server Components (`layout.tsx`, `page.tsx`) por defecto para maximizar el SEO y rendimiento.
   - Utilizar `'use client'` solo en las hojas (componentes interactivos) del árbol de renderizado.

3. **Estética y UI:**
   - El diseño debe ser PREMIUM. Usar gradientes sutiles, micro-interacciones, efectos glassmorphism si corresponde.
   - Implementar Dark Mode / Light Mode.
   - Usar Skeleton Loaders en lugar de spinners globales para mejor UX.

4. **Reglas de Código:**
   - No usar `any`.
   - Organizar las importaciones.
   - Utilizar interfaces y types compartidos desde el backend si existe un monorepo, o replicarlos con precisión.
