# State — dau-urgencia-red

- Last updated: 2026-11-11 23:50 America/Santiago
- Current step: 5 (implementation-guide-sushi)
- Current task: guía con SUSHI terminada y presentada para validación (Tasks 1–18 completas)
- Last completed: paso 5 ejecutado — `05-implementation-guide/` con `sushi-config.yaml` (id `hl7.fhir.cl.test.dau-urgencia-red`, v0.1.0, FHIR R4 4.0.1, solo dependencia `hl7.fhir.r4.core`), `ig.ini`, 11 archivos FSH (10 perfiles, 7 extensiones, 3 ValueSets, 2 CodeSystems, 14 ejemplos sintéticos), 4 páginas (index, profiles, operations, mapping), `menu.xml`, y el workflow `.github/workflows/ig-build.yml` en la raíz del repo. SUSHI v3.21.0 compila con **0 errores y 0 warnings** ("Just like a perfect pearl"); los 14 ejemplos validan contra sus perfiles. Verificado en el JSON generado: el Encounter de alta tiene status finished y dischargeDisposition 03, el Bundle de alta es transaction con 4 PUT, el Bundle de admisión trae los POST con ifNoneExist. Corrección en el camino: `dischargeDisposition` es `Encounter.hospitalization.dischargeDisposition` en FHIR R4 (SUSHI lo señaló con 3 errores; se corrigió el FSH y el invariante).
- Next action: esperar validación de la guía; si valida, paso 6 (componente). Después, subir la carpeta de trabajo y el workflow a cl-urgencia (con aprobación del usuario) y verificar el workflow en GitHub (pasos 2–4 de la Task 18: PR en verde, FSH roto en rojo, deploy en main). Activar GitHub Pages en el repo (Settings → Pages → Source: GitHub Actions).
- Open questions: ninguna pendiente en el paso 5
- Blockers: prueba de aceptación en Codex bloqueada (sin credenciales); el IG Publisher no corre en local (sin Java) — la validación completa la hace el workflow.
- Files changed in this task: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`, `.gitignore`, `README.md`, `state.md`, `validation.md`, `decisions.md`
- Do not redo: pasos 1–4 validados; la spec v3, el BPMN v4, el repaso IHE, las entidades, la propuesta FHIR y las dos subidas a GitHub son las versiones vigentes.

Tasks:
- Task 1: complete — crear carpeta de trabajo y `state.md`
- Task 2: complete — escribir `01-use-case-spec.md` (brainstorming)
- Task 3: complete — spec validada por el usuario
- Task 4: complete — carpeta de trabajo subida a cl-urgencia (main 2cefbfb, 9 archivos; el repo ya no está vacío)
- Task 5: complete — modelo BPMN v4 + spec v3 validados por el usuario (paso 2 cerrado)
- Task 6: complete — aplicar C17/C20/C18(según guía)/C6 según respuestas a Q1, Q2, Q4, Q6 y guía v0.2.0; C14 fallecimiento aplicado según Q3 (extensión del caso)
- Task 7: complete — reparación del componente: revisión experta en el paso 1 (brainstorming) y revisión de la ubicación del estudio IHE
- Task 8: complete — IHE en dos momentos: nueva skill `ihe-landscape-scan` + bootstrap actualizado; regla nueva en `brainstorming-health` (diálogo aunque el usuario describa el caso completo)
- Task 9: pending — actualizar el espacio explorador a v0.6.0 (pendiente de aprobación del usuario); la subida del pack a GitHub ya está hecha (main bc1bcca)
- Task 10: complete — repaso IHE temprano verificado en vivo y escrito en `02-bpmn-model.md`; entidades y datos escritos en `03-entities-data.md` y validados por el usuario (paso 3 cerrado)
- Task 11: in progress — paso 4: propuesta FHIR + tabla de mapeo + revisión experta IHE por punto, presentadas para validación
