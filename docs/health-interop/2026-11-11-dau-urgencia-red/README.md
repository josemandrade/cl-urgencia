# DAU — Aviso mínimo de atención de urgencia a la red

Caso de uso clínico (prueba del componente `health-interop-superpowers` v0.5.0, hecha en esta sesión).
Repositorio del proyecto: https://github.com/josemandrade/cl-urgencia.git (rama `main`, repo público).
Carpeta de trabajo: `docs/health-interop/2026-11-11-dau-urgencia-red/`.

## Estado

| Step | Artefact | Status | Validated by | Date |
|------|----------|--------|--------------|------|
| 1 | `01-use-case-spec.md` | validated | user | 2026-11-11 |
| 2 | `02-bpmn-model.md` | validated | user | 2026-11-11 |
| 3 | `03-entities-data.md` | in progress (entidades y datos, a la espera de validación) | — | 2026-11-11 |
| 4 | `04-fhir-proposal.md` | pending | — | — |
| 5 | `05-implementation-guide/` | pending | — | — |
| 6 | `06-component/` | pending | — | — |

## Qué sigue

Validar las entidades y sus datos (paso 3). Si valida, paso 4: propuesta FHIR + tabla de mapeo + revisión experta IHE por punto (confirmando o refutando los candidatos del repaso temprano). Cuando el repo esté incluido en la instalación de la GitHub App, subir la carpeta a cl-urgencia.

## Bloqueos

- Subida a cl-urgencia: la GitHub App no tiene acceso al repo (403 "Resource not accessible by integration"). El repo sigue vacío, nada se subió. Falta incluir `cl-urgencia` en la instalación de la app.
- Paso 3 pendiente de validación.
- Prueba de aceptación en Codex (sesión limpia con la frase disparadora): bloqueada, Codex no tiene credenciales en este entorno (`codex doctor`: no Codex credentials found). La prueba aquí es el recorrido paso a paso en esta sesión.
