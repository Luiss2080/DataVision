# SDD Skills — Spec-Driven Development para agentes de IA

Suite de 4 skills en formato **Agent Skills** (estándar abierto, agentskills.io).
Cada skill es una carpeta con `SKILL.md`, `references/` y `scripts/`, sin nada
específico de un proveedor.

| Skill | Qué hace |
|---|---|
| `spec-generator` | Constitución, spec (historias + Gherkin, RF/RNF/RD), clarificación, fortalecimiento, plan |
| `sdd-test-design` | Diseño de tests, recomendaciones para la spec, tests en rojo y sellado |
| `sdd-implement` | Tareas e implementación por excepción sin tocar el contrato |
| `sdd-validate` | Validación con evidencias y revisión dirigida de zonas críticas |

Flujo: `spec-generator → sdd-test-design → sdd-implement → sdd-validate`.

## Requisitos
- Un agente con acceso a archivos y terminal.
- Python 3.9+ para los scripts (solo biblioteca estándar).
- Git en el proyecto (la validación compara contra un commit base).

## Instalación

### Opción rápida (Linux, macOS, WSL, Git Bash)
```bash
# En un proyecto
./install.sh /ruta/a/mi-proyecto

# Para todos tus proyectos (carpeta de usuario)
./install.sh --global
```
Copia las skills a `.agents/skills/` y crea enlaces en `.claude/skills/`, para que las
detecten los agentes que leen cualquiera de las dos ubicaciones. Con `--copy` copia en
vez de enlazar (útil en Windows sin permisos de symlink).

### Manual
Copia las carpetas de `skills/` al directorio de skills de tu agente. Ubicaciones
habituales (revisa la documentación de tu agente, cambian entre versiones):

| Agente | Proyecto | Global |
|---|---|---|
| Genérico (estándar) | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` o `.agents/skills/` (también lee `.claude/skills/`) | `~/.cursor/skills/` |
| claude.ai / app de Claude | Subir los `.skill` o el zip de cada carpeta en Ajustes → Skills | — |

## Activación en todos los agentes

Las skills se cargan cuando la petición encaja con su descripción o se invocan por
nombre (en muchos agentes, `/spec-generator`). Para que **cualquier** agente siga el
flujo siempre, añade este bloque a `AGENTS.md` (lo leen la mayoría de agentes) y, si usas
Claude Code, a `CLAUDE.md` (o deja `CLAUDE.md` con una línea `@AGENTS.md`):

```markdown
## Spec-Driven Development
Este proyecto sigue SDD. Antes de cualquier cambio en código, configuración,
dependencias, datos o infraestructura, usa la skill `spec-generator`.
Flujo: spec-generator → sdd-test-design → sdd-implement → sdd-validate.
Constitución: docs/constitution.md. Specs: docs/specs/.
Nunca modifiques archivos listados en un tests.lock.
```

`./install.sh <proyecto> --agents-md` lo añade si no existe.

## Si tu agente no soporta skills
Apunta en `AGENTS.md` a las instrucciones directamente:
`Sigue skills/spec-generator/SKILL.md y sus referencias antes de cualquier cambio.`
Pierdes la carga progresiva (el agente leerá más contexto), pero el flujo funciona.

## Hacerlo cumplir fuera del agente (recomendado)
Las instrucciones se pueden ignorar; la CI no. Añade a tu pipeline:
```bash
python scripts/test_lock.py verify docs/specs/<spec>
python scripts/scan_evasions.py origin/main
```
y las puertas de calidad de `docs/constitution.md`.

## Versionado
Mantén este repositorio como fuente única. Cambia las skills aquí, etiqueta versiones
(`v1.0.0`) y reinstala en los proyectos. `references/conventions.md` es idéntico en las
cuatro skills: si lo cambias, cámbialo en todas (`./install.sh` avisa si difieren).
