# DAU — Aviso mínimo de atención de urgencia a la red

Caso de uso clínico (prueba del componente `health-interop-superpowers` v0.5.0, hecha en esta sesión).
Repositorio del proyecto: https://github.com/josemandrade/cl-urgencia.git (rama `main`, repo público).
Carpeta de trabajo: `docs/health-interop/2026-11-11-dau-urgencia-red/`.

## Estado

| Step | Artefact | Status | Validated by | Date |
|------|----------|--------|--------------|------|
| 1 | `01-use-case-spec.md` | validated | user | 2026-11-11 |
| 2 | `02-bpmn-model.md` | validated | user | 2026-11-11 |
| 3 | `03-entities-data.md` | validated | user | 2026-11-11 |
| 4 | `04-fhir-proposal.md` | validated (propuesta FHIR + tabla de mapeo + revisión IHE por punto + diagrama de recursos) | user | 2026-11-11 |
| 4 | `04-sequence-diagrams.md` | validated (5 diagramas de secuencia, un flujo cada uno, cada mensaje con su operación) | user | 2026-11-12 |
| 5 | `05-implementation-guide/` | validated (plan + guía con SUSHI, 0 errores 0 warnings; workflow de Git en la raíz) + página `sequences.md` (SUSHI 0/0 con la página nueva) | user | 2026-11-11 |
| 6 | `06-component/` | presented for user review (21 tareas, 140 tests OK; ver `validation.md` 2026-11-12) | — | 2026-11-12 |

## Qué sigue

Paso 6 construido y subido a cl-urgencia (commit be2ef3f, 64 archivos, verificado en remoto: 06-component/README.md en main con la tabla de trazabilidad): el componente en `06-component/` implementa la guía (3 Bundles, PI-0, PI-2, PI-3, respuestas del Bus, cliente + CLI + ejemplos + README con la tabla de trazabilidad). Informe final de la prueba del pack: `final-test-report.md` (20 hallazgos F1–F20, pack v0.2.0–v0.16.0, pendientes y bloqueos). El espacio explorador sigue en v0.5.0; actualizarlo a v0.6.0 cuando el usuario lo apruebe.

## Bloqueos

- Prueba de aceptación en Codex: sin credenciales.
- Prueba de aceptación en Codex (sesión limpia con la frase disparadora): bloqueada, Codex no tiene credenciales en este entorno (`codex doctor`: no Codex credentials found). La prueba aquí es el recorrido paso a paso en esta sesión.
