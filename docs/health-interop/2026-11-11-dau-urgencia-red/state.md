# State — dau-urgencia-red

- Last updated: 2026-11-11 23:50 America/Santiago
- Current step: 6 (component-building)
- Current task: componente que implementa la guía (06-component/) — por empezar; la URL de la guía desplegada está pendiente del workflow
- Last completed: el BPMN v6 está renderizado y verificado (0 diagonales por programa; mirado a 4320 px por zonas, sin solapamientos; todas las líneas perpendiculares). La v6 queda presentada para validación. Falta subir el PNG nuevo (por la web), el .bpmn/.svg/.md y los registros, verificar el run y la guía en vivo, y subir el pack v0.14.0 con la skill reparada (enrutado ortogonal según buenas prácticas BPMN). Después, paso 6 (componente).
- Next action: paso 6 (componente que implementa la guía, en 06-component/).
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
