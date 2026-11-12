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
| 5 | `05-implementation-guide/` | validated (plan + guía con SUSHI, 0 errores 0 warnings; workflow de Git en la raíz) | user | 2026-11-11 |
| 6 | `06-component/` | in progress | — | 2026-11-11 |

## Qué sigue

Paso 6: componente que implementa la guía y sus operaciones, en `06-component/`. El usuario pidió la URL de la guía desplegada: subir la carpeta de trabajo y el workflow a cl-urgencia y verificar el despliegue en GitHub Pages (`https://josemandrade.github.io/cl-urgencia/`). El espacio explorador sigue en v0.5.0; actualizarlo a v0.6.0 cuando el usuario lo apruebe.

## Bloqueos

- Prueba de aceptación en Codex: sin credenciales.
- Prueba de aceptación en Codex (sesión limpia con la frase disparadora): bloqueada, Codex no tiene credenciales en este entorno (`codex doctor`: no Codex credentials found). La prueba aquí es el recorrido paso a paso en esta sesión.
