# State — dau-urgencia-red

- Last updated: 2026-11-12 18:53 America/Santiago
- Current step: 4/5 (diagramas de secuencia, skill nueva del pack v0.17.0) — aplicación de `sequence-diagrams` al caso DAU, pendiente la validación del usuario
- Current task: validación del usuario de los diagramas de secuencia
- Last completed: diagramas de secuencia subidos a cl-urgencia (texto 55d2bb2, 15 archivos; PNG 64bab50, 5 archivos por la web) y verificados en vivo (run 43313844154 success; sequences.html y los 5 PNG 200; zoom presente)
- Next action: validación del usuario de los diagramas; después, opcional: explorador a v0.17.0
- Files changed in this task: `06-component/plan.md`, `06-component/tests/goldens/` (14 JSON), `06-component/src/dau/*.py` (16 módulos), `06-component/tests/*.py` (12 módulos), `06-component/examples/` (12 JSON), `06-component/README.md`, `state.md`, `validation.md`, `README.md` del caso.
- Open questions: ninguna pendiente en el paso 6
- Blockers: prueba de aceptación en Codex bloqueada (sin credenciales); el workflow de la guía no se puede subir por API sin el permiso Workflows de la App.
- Files changed in this task: `06-component/plan.md`, `06-component/tests/goldens/` (14 JSON), `state.md`
- Do not redo: pasos 1–5 validados; la spec v3, el BPMN v4, el repaso IHE, las entidades, la propuesta FHIR, la guía con SUSHI y las tres subidas a GitHub son las versiones vigentes.

Rulings (desviaciones de la guía, cambio mínimo que la satisface):
- Task 2: Ruling: los RUN de ejemplo de la guía (12345678-9 paciente, 98765432-1 profesional) NO pasan el DV chileno (DV calculado 5 en ambos; verificado por programa) — la guía dice en PI-0 que un RUN con DV inválido se rechaza, así que el componente valida el DV estrictamente y sus ejemplos sintéticos usan 12345678-5 y 98765432-5; las comparaciones con goldens normalizan el RUN.
- Task 7/8/9: Ruling: los PUT condicionales de Condition/MedicationRequest/DocumentReference en los Bundles de alta/abandono exigen un `identifier` local que los recursos de ejemplo de la guía no llevan (verificado: 0 ocurrencias de `identifier` en los 5 JSON compilados) — sin él, el PUT condicional no puede emparejar nada. Los builders aceptan `local_id` y lo incluyen, con los sistemas de la guía (`https://his.ejemplo.cl/fhir/sid/diagnostico|medicamento|documento`) y valor `<DAU>-1`.
- Task 9: Ruling: el perfil `DAUDocumentoUrgencia` fija `contentType = application/pdf` (patternCode en la StructureDefinition), pero el ejemplo compilado por SUSHI lo omite (verificado: 0 ocurrencias de `contentType`) — el builder lo pone siempre, siguiendo el perfil (normativo) y no el ejemplo.
- Task 10/11/12: Ruling: la guía dice que las referencias entre recursos van por `fullUrl urn:uuid:`, pero los ejemplos compilados por SUSHI referencian `Patient/ejemplo-paciente` (verificado en el Bundle de admisión) — el ensamblador de Bundle reescribe las referencias internas a los `fullUrl` de las entradas; además, los recursos en un Bundle se emiten SIN `Resource.id` (la guía: "sin `Resource.id` en el PUT") y los goldens se comparan con `id` quitado.
- Task 3: Ruling: los perfiles FSH fijan `identifier.system` (DEIS para Organization, RUN para Practitioner), pero los ejemplos compilados por SUSHI llevan el identificador SOLO con `value` (sin `system`) — los builders reproducen el ejemplo compilado tal cual (es lo que exige la comparación con goldens) y los validadores comprueban el sistema solo cuando está presente; si el sistema está presente y es distinto del fijado, es error.

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
- Task 11: complete — paso 4: propuesta FHIR + tabla de mapeo + revisión experta IHE por punto, validadas por el usuario; paso 5: guía con SUSHI validada y publicada
- Task 12: complete — BPMN v7 modelado y verificado (0 diagonales en los 51 flujos; ningún segmento cruza una figura; mirado a 4320 px por zonas; SUSHI 0 errores) y validado por el usuario (2026-11-12 09:56); paso 2 cerrado para v7
- Task 13: complete — v7 subida (17d9b59), PNG subido por la web (7e9befd), run 24 success y guía verificada en vivo (PNG 200/448885, process.html a 4320 px con zoom); pack v0.15.0 publicado (3ca29e5); explorador actualizado a v0.15.0
- Task 14: complete — registros de la v7 subidos (fdca400); skill de git `git-workflow-health` creada en el pack (v0.16.0 local, verificada: 0× 0.15.0, 14× 0.16.0, JSON/JS/hook ok), investigando superpowers (using-git-worktrees, finishing-a-development-branch)
- Task 15: complete — pack v0.16.0 publicado (6ee9db9, 16 archivos; verificado en remoto: skill.yaml 0.16.0 y git-workflow-health en main)
- Task 16: complete — paso 6: componente que implementa la guía (06-component/) construido (21 Component Tasks, 140 tests en verde) y subido a cl-urgencia (be2ef3f, 64 archivos, verificado en remoto); vía remota con las puertas de git-workflow-health (la carpeta no es un checkout git)
- Task 17: complete — informe final de la prueba del pack escrito (final-test-report.md, 20 hallazgos F1–F20, historial de versiones v0.2.0–v0.16.0, pendientes y bloqueos) y subido a cl-urgencia (734e8d7, 4 archivos, verificado en remoto) al tercer intento (los dos primeros: reinicio del servicio y tarjeta caducada)
- Task 18: complete — generador durable `render_sequence.py` (SVG fuente, PNG 2×, check mecánico `--check`) + diagrama de secuencia de admisión (4 participantes, 3 envíos + 3 retornos)
- Task 19: complete — diagrama de secuencia de alta (alt alta/fallecimiento destino 03, opt corrección entered-in-error)
- Task 20: complete — diagrama de secuencia de abandono (alt NEA tipo 1 / fuga tipo 2)
- Task 21: complete — diagrama de secuencia de consulta de la red (alt consulta puntual/suscripción; 5 operaciones PI-2 + notificación asíncrona)
- Task 22: complete — diagrama de secuencia de recuperación del PDF (PI-3) + `04-sequence-diagrams.md` (5 secciones con tabla mensaje → operación → IHE → resultado) + página `sequences.md` en la guía (registro en sushi-config.yaml y menu.xml, enlaces desde index.md y operations.md); SUSHI 0 errores 0 warnings
- Nota visual (2026-11-12): el primer render tenía 4 defectos del generador (tofu U+2192 en los subtítulos; solape pestaña-etiqueta 50×9 px y 44×9 px en el diagrama de alta; guarda del segundo operando fuera del borde izquierdo del fragmento; píldoras de las dos líneas de una etiqueta solapadas 2 px); corregidos en `render_sequence.py` (se escribe `>`; pestaña 70 px sobre la primera flecha; guarda anclada a la izquierda dentro del fragmento; interlineado 19 px) y verificados por programa: 0 solapamientos y 0 tofu en los 5 SVG; el diagrama de alta vuelto a mirar completo

Component Tasks:
- Component Task 1: complete — andamiaje + identificadores (constants, identifiers, run_tests.sh, 8 tests en verde: RUN 12345678-5 válido, 12345678-9 inválido, 98765432-5 válido, 98765432-1 inválido)
- Component Task 2: complete — paciente DAUPaciente (build/validate, golden salvo RUN normalizado e id/meta; 8 tests)
- Component Task 3: complete — prestadores Organization + Practitioner (goldens salvo id/meta y RUN normalizado; 12 tests). Ruling: identifier solo con value en los ejemplos compilados, sistema solo validado si está presente
- Component Task 4: complete — Encounter de admisión (invariantes dau-enc-period, dau-enc-reason; 24 tests en test_encounters con las variantes)
- Component Task 5: complete — Encounter de alta (destino 01–06, dau-alta-destino, diagnosis DD)
- Component Task 6: complete — Encounter de abandono (tipo 1/2, sin dischargeDisposition ni destination)
- Component Task 7: complete — diagnóstico (2 goldens, local_id para el PUT condicional)
- Component Task 8: complete — medicamento al alta (golden, local_id)
- Component Task 9: complete — documento (2 goldens, local_id, contentType application/pdf siempre)
- Component Task 13: complete — PI-0 identidad (5 casos de la guía; 6 tests)
- Component Task 14: complete — PI-2 buscar paciente PDQm (URL exacta)
- Component Task 15: complete — PI-2 buscar episodios QEDm (por paciente y por prestador)
- Component Task 16: complete — PI-2 buscar diagnósticos QEDm
- Component Task 17: complete — PI-2 buscar documento MHD
- Component Task 18: complete — PI-2 suscripción FHIR (criteria Encounter?class=EMER, rest-hook)
- Component Task 19: complete — PI-3 acceso al PDF (GET autenticado, alta y abandono)
- Component Task 20: complete — respuestas del Bus (200 applied, 400/422 correct_and_resend, 412 ambiguous, 422 con MPI identity_unresolved; corrección entered-in-error conserva el ID DAU; admisión de episodio cerrado rechazada; 9 tests)
- Component Task 10: complete — Bundle de admisión (golden, 4 entradas: 3 POST con ifNoneExist + PUT por ID DAU; referencias internas reescritas a urn:uuid:; sin id)
- Component Task 11: complete — Bundle de alta (golden, 4 PUT; sin medicamento, 3 entradas)
- Component Task 12: complete — Bundle de abandono (golden, 3 PUT, sin hospitalization; 3 tests)
- Component Tasks 2–9 + 13–19 verificadas por el coordinador con la suite completa: 109 tests OK (8 + 78 + 23), corrida propia 2026-11-12
- Component Task 21: complete — cliente HTTP (urllib, mock local) + CLI (12 operaciones) + 12 ejemplos sintéticos + README del componente (prerrequisitos, comandos, configuración, ejemplos por operación, tabla de trazabilidad); 9 tests. RED observado: `ModuleNotFoundError: No module named 'dau.client'`
- Component Tasks 10–12: complete — Bundles transaccionales (13 tests en verde, los 3 coinciden con sus goldens salvo lo normalizado por las Rulings; sin medicamento el Bundle de alta tiene 3 entradas). Nota RED-GREEN: los tres builders viven en un solo módulo (`bundles.py`), así que el RED se observó una sola vez a nivel de import (`ModuleNotFoundError: No module named 'dau.bundles'`); cada variante se verificó por separado contra su golden.
- Suite completa del componente (corrida propia del coordinador, 2026-11-12): **140 tests OK** (`Ran 140 tests in 1.050s`)
