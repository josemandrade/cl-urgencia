# State — dau-urgencia-red

- Last updated: 2026-11-11 23:50 America/Santiago
- Current step: 6 (component-building)
- Current task: componente que implementa la guía (06-component/) — por empezar; la URL de la guía desplegada está pendiente del workflow
- Last completed: paso 5 validado por el usuario. Subida a cl-urgencia (34 archivos, pasos 4–5, commit 92909ae, verificado). El usuario agregó el workflow `.github/workflows/ig-build.yml` por la web (commit 92da894) y le corrigió la URL del publisher (commit bf9dc1a). Run 2: SUSHI pasó, pero el publisher falló: la plantilla `hl7.base.template` rechaza el id con reino `cl` ("Unrecognized realm in id"). Run 3 (con `fhir.base.template#1.0.0`, commit c72dea4): el build llegó hasta generar las salidas y falló porque Jekyll no está en el runner. Decisión del usuario: cambiar el id a `hl7.fhir.uv.test.dau-urgencia-red` y volver a `hl7.base.template#current`. El cambio está aplicado en local (sushi-config.yaml, ig.ini, plan.md) y SUSHI regenera con el id nuevo (0 errores).
- Next action: subir el cambio de id a cl-urgencia y verificar el run 4 de Actions (que SUSHI, el publisher y el deploy pasen) y la URL viva (`https://josemandrade.github.io/cl-urgencia/`). Después, paso 6 (componente).
- Open questions: ninguna pendiente en el paso 6
- Blockers: prueba de aceptación en Codex bloqueada (sin credenciales); el workflow de la guía no se puede subir por API sin el permiso Workflows de la App.
- Files changed in this task: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`, `.gitignore`, `README.md`, `state.md`, `validation.md`, `decisions.md`
- Do not redo: pasos 1–5 validados; la spec v3, el BPMN v4, el repaso IHE, las entidades, la propuesta FHIR, la guía con SUSHI y las tres subidas a GitHub son las versiones vigentes.

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
