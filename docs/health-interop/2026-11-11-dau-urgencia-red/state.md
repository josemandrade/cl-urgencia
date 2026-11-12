# State — dau-urgencia-red

- Last updated: 2026-11-11 23:05 America/Santiago
- Current step: 3 (entities-data)
- Current task: entidades y datos (`03-entities-data.md`) presentados para validación
- Last completed: paso 2 validado por el usuario (BPMN v4 + spec v3). Repaso IHE temprano verificado en vivo en profiles.ihe.net (PIXm v3.1.0, PDQm v3.2.0, MHD v4.2.5, mCSD v4.0.0, QEDm v3.0.0, y los clásicos PIX/PDQ/XDS.b/XDR/DSUB/NAV/ATNA/CT/BPPC en ITI TF Rev 20.2 Final Text) y escrito en `02-bpmn-model.md` con una columna de candidatos por punto de interoperabilidad. Entidades y datos escritos en `03-entities-data.md` (12 entidades, campos por entidad, calidad y propiedad).
- Next action: esperar validación de las entidades; si valida, paso 4 (propuesta FHIR + tabla de mapeo + revisión experta IHE por punto). Reintentar la subida a cl-urgencia cuando el usuario agregue el repo a la instalación de la GitHub App. Subir el pack v0.6.0 a GitHub y actualizar el espacio explorador cuando el usuario lo apruebe.
- Open questions: ninguna pendiente en el paso 3 (el valor del desenlace de fallecimiento se define en el paso 4)
- Blockers: subida a cl-urgencia bloqueada — la GitHub App no tiene acceso al repo (403); el repo sigue vacío, nada se subió. Prueba de aceptación en Codex bloqueada (sin credenciales).
- Files changed in this task: `02-bpmn-model.md` (repaso IHE + columna de candidatos + estado validado), `01-use-case-spec.md` (estado validado), `03-entities-data.md`, `README.md`, `state.md`, `validation.md`
- Do not redo: pasos 1–2 validados; la spec v3, el BPMN v4 y el repaso IHE son las versiones vigentes.

Tasks:
- Task 1: complete — crear carpeta de trabajo y `state.md`
- Task 2: complete — escribir `01-use-case-spec.md` (brainstorming)
- Task 3: complete — spec validada por el usuario
- Task 4: blocked — subir carpeta de trabajo a cl-urgencia (GitHub App sin acceso al repo; el usuario debe incluirlo en la instalación)
- Task 5: complete — modelo BPMN v4 + spec v3 validados por el usuario (paso 2 cerrado)
- Task 6: complete — aplicar C17/C20/C18(según guía)/C6 según respuestas a Q1, Q2, Q4, Q6 y guía v0.2.0; C14 fallecimiento aplicado según Q3 (extensión del caso)
- Task 7: complete — reparación del componente: revisión experta en el paso 1 (brainstorming) y revisión de la ubicación del estudio IHE
- Task 8: complete — IHE en dos momentos: nueva skill `ihe-landscape-scan` + bootstrap actualizado; regla nueva en `brainstorming-health` (diálogo aunque el usuario describa el caso completo)
- Task 9: pending — subir el pack v0.6.0 a GitHub y actualizar el espacio explorador (pendiente de aprobación del usuario)
- Task 10: in progress — repaso IHE temprano verificado en vivo y escrito en `02-bpmn-model.md`; entidades y datos escritos en `03-entities-data.md`, presentados para validación
