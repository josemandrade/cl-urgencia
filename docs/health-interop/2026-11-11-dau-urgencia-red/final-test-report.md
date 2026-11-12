# Informe final de la prueba — health-interop-superpowers

**Caso de prueba:** aviso mínimo de atención de urgencia a la red (DAU), carpeta `docs/health-interop/2026-11-11-dau-urgencia-red/`
**Fechas:** 2026-11-11 y 2026-11-12
**Pack probado:** `health-interop-superpowers`, de la v0.2.0 a la v0.16.0 (15 skills)
**Repositorios:** pack https://github.com/josemandrade/health-interop-superpowers (privado), caso https://github.com/josemandrade/cl-urgencia (público)
**Guía publicada:** https://josemandrade.github.io/cl-urgencia/
**Método:** la prueba se hizo en esta sesión, paso a paso, siguiendo las skills y sus puertas de validación; cada paso se presentó al usuario para validación antes de avanzar. No se pudo probar en un harness real: la prueba de aceptación en Codex quedó bloqueada (sin credenciales) — ver "Pendiente".

## Veredicto

El pack funciona de principio a fin con un caso real: **los 6 pasos se completaron, se validaron con el usuario y se publicaron**. La guía compila con SUSHI en 0 errores y 0 warnings, el componente pasa sus 140 tests, y todo está verificado en remoto y en vivo.

La prueba encontró **19 hallazgos** (F1–F19). Todos salvo los anotados como pendientes se corrigieron en el pack durante la prueba, con su versión. Ningún hallazgo quedó sin registrar.

## Recorrido por pasos

| Paso | Artefacto | Estado | Validado por | Fecha |
|------|-----------|--------|--------------|-------|
| 1 | `01-use-case-spec.md` (spec v3) | validado | usuario | 2026-11-11 |
| 2 | `02-bpmn-model.bpmn` (BPMN v7) | validado | usuario | 2026-11-12 09:56 |
| 3 | `03-entities-data.md` (12 entidades) + repaso IHE temprano | validado | usuario | 2026-11-11 |
| 4 | `04-fhir-proposal.md` (rev 3) + `04-mapping-table.md` + diagrama de recursos | validado | usuario | 2026-11-12 |
| 5 | `05-implementation-guide/` (SUSHI, 0 errores) | validado y publicado | usuario | 2026-11-12 |
| 6 | `06-component/` (21 tareas, 140 tests) | construido y subido | usuario (revisión + push) | 2026-11-12 |

Evidencia de la publicación: guía en vivo (run 24, success); componente en main, commit `be2ef3f` (64 archivos, verificado en remoto: `06-component/README.md` en main con la tabla de trazabilidad); registros del push, commit `ac6a3fd`.

## Hallazgos

### F1 — El brainstorming no se ejerció (paso 1)
La spec se redactó directamente desde la descripción del caso entregada por el usuario en un solo mensaje, sin el diálogo del brainstorming: no se hicieron las preguntas (qué problema resuelve, quién lo usa, qué datos entran y salen, cómo se ve el éxito) ni se devolvió la comprensión en trozos cortos esperando corrección. La comprensión del proceso llegó débil al paso 2: la admisión ni siquiera estaba en la comprensión inicial.
**Corrección:** regla nueva en `brainstorming-health` (v0.6.0): aunque el usuario entregue una descripción completa en un solo mensaje, el diálogo del brainstorming se hace igual antes de redactar la spec.

### F2 — La revisión experta detectó que faltaba la admisión (paso 2)
El BPMN v1 no reflejaba el proceso real: admisión ausente (crítico), NEA modelado como si el paciente hubiera sido atendido (crítico), el DAU se generaba antes del desenlace (alto), la fuga era salida de puerta en vez de interrupción (medio).
**Corrección:** nueva skill experta `process-expert-review` (v0.6.0) y puerta dura en los pasos 1 y 2: nada pasa a BPMN sin spec revisada por experto y validada; nada pasa a FHIR sin BPMN revisado y validado. La revisión se hace contra la práctica real y la guía publicada, nunca de memoria, prefiriendo la versión publicada al build continuo.

### F3 — El estudio IHE va en dos momentos (pasos 2 y 4)
El usuario cuestionó que el estudio IHE viviera solo en el paso 4: como el proceso se obtiene de una guía, el estudio debería venir después del brainstorming.
**Corrección:** dos momentos (v0.6.0): `ihe-landscape-scan` tras validar la spec y antes del BPMN (candidatos verificados en vivo), y la revisión detallada por punto (`ihe-profile-review`) sigue en el paso 4, confirmando o refutando cada candidato. En esta prueba el repaso se hizo al inicio del paso 3 (la skill nació cuando el BPMN ya estaba validado) y quedó registrado en `02-bpmn-model.md`; en los próximos casos corre antes del BPMN.

### F4 — En FHIR R4 el destino al alta es `hospitalization.dischargeDisposition` (paso 5)
La primera compilación dio 3 errores: `dischargeDisposition` no existe como elemento directo de `Encounter`.
**Corrección:** se corrigieron el FSH y el invariante `dau-alta-destino`; la compilación siguiente quedó en 0 errores. La prosa puede decir `dischargeDisposition`, pero el FSH y el JSON usan la ruta completa.

### F5 — El fallecimiento SÍ está contemplado: es un alta con destino `03` (paso 4)
La spec v3 y el BPMN v4 decían que la guía no contemplaba el fallecimiento. Al revisar la guía v0.2.0 en vivo apareció el código `03 Fallecido` en el ValueSet del alta, con binding requerido en el perfil de alta.
**Corrección:** el fallecimiento es un evento de alta (`dischargeDisposition = 03`, `period.end` = hora del fallecimiento, diagnóstico de egreso = causa de muerte CIE-10 con `use = DD`, resumen de alta LOINC 59258-4). No hace falta Bundle ni código nuevos. La nota imprecisa quedó corregida en `validation.md`.

### F6 — La GitHub App no puede subir workflows (paso 5)
El push del workflow por API da 403: la App no tiene el permiso Workflows, que GitHub exige para crear o modificar archivos de workflow.
**Corrección (proceso, no skill):** el usuario agrega y edita `ig-build.yml` por la web de GitHub. La skill `implementation-guide-sushi` documenta la limitación. El workflow quedó en main por la web (commits `92da894`, `bf9dc1a`, `1074d62`).

### F7 — La URL vieja del IG Publisher da 404 (paso 5)
`https://fhir.github.io/latest-ig-publisher/org.hl7.fhir.publisher.jar` ya no sirve el jar (run 1: SUSHI pasó, la descarga falló).
**Corrección:** el publisher actual es la release 3.0.3 y el artefacto se llama `publisher.jar`: `https://github.com/HL7/fhir-ig-publisher/releases/latest/download/publisher.jar` (verificado: descarga, 243 MB). La plantilla del workflow en `implementation-guide-sushi` lleva la URL nueva.

### F8 — La plantilla HL7 rechaza reinos fuera de us/uv/eu y exige contacto de grupo de trabajo; la genérica necesita Jekyll (paso 5)
`hl7.base.template` rechazó el id con reino `cl` (run 3) y luego exigió un contacto con URL a un grupo de trabajo real de HL7 (run 4). La plantilla genérica `fhir.base.template` acepta `cl` pero necesita Jekyll, que no está en el runner (run 3).
**Corrección:** el id de la guía pasó a `hl7.fhir.uv.test.dau-urgencia-red` y el workflow instala Jekyll (paso "Install Jekyll", añadido por la web). La skill documenta ambas limitaciones y que el id debe volver a `hl7.fhir.cl.*` si la guía se publica como guía chilena oficial (con la plantilla genérica + Jekyll).

### F9 — Las páginas de la guía deben enlazar a los artefactos generados (paso 5)
La guía publicada tenía las páginas de los artefactos FHIR generadas, pero `profiles.md` era una tabla estática sin enlaces, `operations.md` nombraba los ejemplos solo por su id, no había página de Terminología y el menú no incluía Artefactos.
**Corrección:** cada artefacto enlaza a su página generada (`<ResourceType>-<id>.html`, con el id en minúsculas: `StructureDefinition-dau-encuentro-urgencia.html`, no `DAUEncuentroUrgencia`); página de Terminología obligatoria; Artefactos en el menú. Regla "Make the guide navigable" en `implementation-guide-sushi` (86 enlaces internos verificados contra los 37 artefactos generados).

### F10 — Los perfiles son propios; la guía documenta su relación con IHE (paso 5)
La guía se presentaba como transcripción de los perfiles del MINSAL y de CL-Core, y no mostraba las relaciones IHE.
**Corrección:** los perfiles `DAU...` son propios de esta guía (base FHIR R4 + spec del caso; las restricciones no cambian) y la guía tiene la página "Relación con IHE" (PI-0 a PI-3, encaje, actores, brechas). Ambas reglas están en `implementation-guide-sushi`.

### F11 — Las asociaciones se ofrecen, no se asumen; el recurso base se declara con su URL (paso 4)
El usuario pidió que las skills ofrezcan las asociaciones a otras guías FHIR o perfiles IHE cuando corresponda, y que la propuesta deje la URL del recurso base e informe que se puede elegir otro (ejemplo: `Patient` con base `PatientCL` de CL-Core).
**Corrección:** configuradas `fhir-modeling`, `implementation-guide-sushi` e `ihe-profile-review`. Verificado en vivo: CL-Core SÍ es un paquete FHIR resoluble (`hl7.fhir.cl.clcore`, última 1.9.4; SUSHI resuelve `CorePacienteCl` como `Parent:`, 0 errores), corrigiendo la suposición del paso 5. El usuario decidió mantener `DAUPaciente` sobre el `Patient` base de FHIR R4 (no `PatientCL`); no se añade la dependencia.

### F12 — Cada operación enlaza a su perfil IHE (paso 5)
Las operaciones no enlazaban a ningún perfil IHE y la búsqueda del paciente (PDQm) ni siquiera estaba como operación.
**Corrección:** `operations.md` reescrita: cada operación con su perfil IHE y su enlace a profiles.ihe.net (buscar paciente → PDQm, buscar episodios/diagnósticos → QEDm, documento → MHD, identidad → PIXm; la suscripción es Subscription FHIR, DSUB refutado). Regla en `implementation-guide-sushi` y en `fhir-modeling`. Verificado en vivo (run 10, 18 enlaces a profiles.ihe.net).

### F13 — La guía debe incluir el BPMN y el diagrama de recursos como páginas propias; el menú debe ser horizontal; el publisher pone `input/images/` en la raíz (paso 5)
La guía no tenía el BPMN ni el diagrama de recursos, y el header se veía como lista vertical (`menu.xml` era un `<ul>` sin clase). Además, la primera versión referenciaba las imágenes como `images/<archivo>` y daba 404: el IG Publisher copia `input/images/` a la **raíz del sitio publicado**, no a `images/`.
**Corrección:** páginas propias `process.md` y `resources.md` con entrada en el menú; menú `<ul class="nav navbar-nav">`; imágenes referenciadas solo por su nombre de archivo. Reglas en `implementation-guide-sushi` y `fhir-modeling`. Verificado en vivo (run 12: ambos SVG con 200, header horizontal).

### F14 — Los diagramas van como PNG directo, con zoom in / zoom out (paso 5)
El usuario pidió los diagramas directo como JPG o PNG (o mejor formato) y, si hace falta, zoom in / zoom out. El SVG en `<img>` no se veía de forma fiable para él, aunque el archivo cargaba y renderizaba.
**Corrección:** los diagramas se incrustan como PNG directo (grafo 2440×1800, BPMN a su ancho nativo 4320 px) con botones Zoom in (+), Zoom out (−) y 100% y script inline `zoomDiagram`/`resetDiagram` por página. El script sobrevive al publisher (verificado en vivo, run 14). Regla en `implementation-guide-sushi`.

### F15 — Un diagrama no se verifica con un 200: hay que mirarlo al tamaño de visualización, por zonas (pasos 2 y 5)
Dos veces el diagrama "estaba bien" según las comprobaciones y seguía ilegible para el usuario. Primera causa: el render dibujaba pool y lane como texto vertical rotado en la misma franja y las etiquetas PI se ponían en el centroide, donde se apilaban. Segunda causa: la página mostraba el PNG de 8640 px a 2400 px, así que el texto de 12 px se veía a ~7 px; la verificación anterior había mirado el PNG a resolución completa, no al tamaño de visualización, y no detectó el problema.
**Corrección:** render reescrito (nombres en horizontal en columna de etiquetas de 240 px, etiquetas de flujo cortas sobre el segmento más largo, descolisión conjunta con fondo blanco, PNG a 2×); la página muestra el BPMN a su ancho nativo (4320 px) con scroll horizontal y zoom. Puerta dura en `bpmn-modeling` y en `implementation-guide-sushi`: renderizar y MIRAR el PNG antes de presentar el modelo, al tamaño de visualización y por zonas.

### F16 — Un BPMN claro necesita reglas estructurales (paso 2, v5)
Del pantallazo del usuario: el evento de fin "Episodio cerrado / aviso publicado" y el evento de inicio "Solicitud de DAU recibida" estaban a 60 px en la misma fila, con etiquetas solapadas; tres flujos de mensaje compartían el mismo punto de origen y formaban un nudo; PI-3 salía de la tarea equivocada ("Consultar episodios", que no es quien envía la solicitud).
**Corrección (v5):** cada rama en su propia fila; un flujo de mensaje sale de la tarea que realmente lo envía; los flujos de mensaje se encaminan por el hueco entre pools; el render trata cada forma como obstáculo de descolisión; dividir el diagrama antes de que se vuelva un muro. Reglas en `bpmn-modeling`. Verificado en vivo (run 43160619603, success; PNG 200/528411).

### F17 — Las líneas que unen deben ser perpendiculares, verificadas por programa (paso 2, v6)
El usuario pidió líneas perpendiculares, no diagonales, y buenas prácticas de BPMN leídas en vivo (Camunda, Visual Paradigm, Schematex/OMG BPMN 2.0 y Bruce Silver, JointJS: enrutado Manhattan/ortogonal).
**Corrección (v6):** todos los flujos reencaminados en ortogonal — **0 aristas diagonales en los 41 flujos**, verificado por programa — con las puertas alineadas, cambios de fila en L/Z y canales del hueco entre pools escalonados (PI-2 y=590, PI-2 retorno y=605, PI-3 y=620) para que ningún flujo comparta tramo. La verificación mecánica (0 diagonales) es puerta en `bpmn-modeling` y en `implementation-guide-sushi`. Verificado en vivo (run 43162491258, success; PNG 200/437579). La v6 fue validada por el usuario (2026-11-12 08:15).

### F18 — El trabajo en paralelo se modela con puertas AND y subprocesos; añadir un elemento reabre el check de cruces (paso 2, v7)
La vía rápida C1 exige que la admisión se complete durante la atención, y la guía exige que la admisión (con el ID DAU) exista antes del cierre y prohíbe enviar una admisión de un episodio ya cerrado.
**Corrección (v7):** puerta paralela AND que bifurca en "Atender clínicamente" y el subproceso "Completar admisión administrativa", unidas en una puerta paralela AND **antes** de la puerta de desenlace. 0 diagonales en los 51 flujos y ningún segmento cruza una figura (salvo 3 objetos de datos preexistentes), verificado por programa y mirado a 4320 px por zonas. La skill lleva la sección de ramas paralelas y el check de cruces. Validada por el usuario (2026-11-12 09:56) y verificada en vivo (run 24, PNG 200/448885).

### F19 — Las acciones de git en el proyecto local las tiene el componente (paso 6)
El usuario pidió que las acciones de git en el proyecto local las tenga el componente, y sugirió revisar cómo lo hace obra/superpowers.
**Corrección:** nueva skill `git-workflow-health` (v0.16.0): detectar el repo local al inicio; una rama por caso (`health-interop/<slug>`); preguntar worktree o rama; un commit por paso validado o `Task N` (nunca `git add -A` a ciegas); merge siempre con el menú exacto de superpowers (merge local / push + PR / dejar la rama; nunca asumir la base; nunca force-push); revisión antes de merge a `main`; push nunca sin aprobación explícita; verificar en remoto antes de declarar subido (`git ls-remote`, run verde + página en vivo); registro en `state.md`/`validation.md`/`decisions.md`. Investigado en superpowers en vivo (15 skills). El paso 6 se subió por la vía remota con las mismas puertas (la carpeta del caso no es un checkout git). **Una tarjeta de aprobación caducada significa que nada se subió**: varias subidas fallaron así durante la prueba; las que se aprobaron a tiempo se aplicaron (la v7 al cuarto intento, en 18 s).

### F20 — Los ejemplos compilados de la guía discrepan de sus propios perfiles en 5 puntos (paso 6)
Al implementar la guía, el componente encontró 5 discrepancias entre los perfiles FSH (normativos) y los ejemplos JSON que compiló SUSHI: los RUN de ejemplo de la guía no pasan el dígito verificador chileno (12345678-9 y 98765432-1; el DV calculado es 5 en ambos); los perfiles fijan `identifier.system` pero los ejemplos llevan el identificador solo con `value`; los PUT condicionales de Condition/MedicationRequest/DocumentReference exigen un `identifier` local que los ejemplos no llevan; el perfil de documento fija `contentType = application/pdf` pero el ejemplo lo omite; la guía dice que las referencias van por `fullUrl urn:uuid:` pero los ejemplos referencian `Patient/ejemplo-paciente`, y los recursos se emiten sin `Resource.id` en el PUT.
**Corrección:** las 5 quedaron como `Ruling:` en `state.md` (el cambio mínimo que satisface la guía: los builders siguen el perfil cuando el ejemplo omite algo normativo, reproducen el ejemplo cuando la comparación con goldens lo exige, y normalizan lo que el ejemplo no puede cumplir). El componente valida estrictamente el DV del RUN, como dice PI-0. Los 140 tests pasan contra los goldens, salvo lo normalizado por las Rulings.

## Historial de versiones del pack durante la prueba

| Versión | Qué cambió (por la prueba) |
|---------|----------------------------|
| v0.2.0 | Estado inicial de la prueba (13 skills, flujo de 6 pasos) |
| v0.3.0 | IHE por punto en el paso 4; skill `ihe-profile-review` |
| v0.4.0 | Soporte de plugins (Claude Code, Cursor, Codex, Gemini CLI, Muse, OpenCode, Antigravity) |
| v0.5.0 | Skills reestructuradas estilo superpowers; `state.md` como checkpoint de reanudación; tareas pequeñas |
| v0.6.0 | F1, F2, F3: `process-expert-review`, `ihe-landscape-scan`, regla de brainstorming |
| v0.7.0 | CI/CD de la guía (workflow) en `implementation-guide-sushi` |
| v0.10.0 | BPMN y diagrama de recursos en la guía; header horizontal |
| v0.11.0 | F15 (primera parte): reparación del render BPMN |
| v0.12.0 | F15 (segunda parte): ancho de visualización nativo |
| v0.13.0 | F16: reglas estructurales del BPMN (v5) |
| v0.14.0 | F17: líneas ortogonales, 0 diagonales (v6) |
| v0.15.0 | F18: ramas paralelas AND + subprocesos, check de cruces (v7) |
| v0.16.0 | F19: skill `git-workflow-health` (15 skills) |

El pack quedó publicado como v0.16.0 (commit `6ee9db9`, 16 archivos, verificado en remoto).

## Pendiente y bloqueado

- **Prueba de aceptación en Codex (bloqueado):** una sesión limpia que diga "I have a clinical use case that needs health data interoperability" debería auto-disparar `brainstorming-health`. No se pudo correr: Codex CLI 0.164.0-alpha.9 está instalado, pero `codex doctor` dice "no Codex credentials found". El pack no ha sido probado de principio a fin en un harness real.
- **Explorador en v0.15.0:** el espacio explorador tiene el contenido de la v0.15.0; la skill de git (v0.16.0) todavía no está reflejada en él. Nadie ha pedido actualizarlo.
- **Hueco preexistente en `.muse-plugin/plugin.json`:** lista solo 13 skills; omite `ihe-landscape-scan` y `process-expert-review`. No lo introdujo la prueba ni se corrigió en ella.
- **Hueco de contabilidad en los registros de sync:** varias subidas intermedias (pack v0.8.0–v0.14.0, subidas de la v6) nunca se anotaron en los JSON de sync; las entradas más nuevas por ruta van por detrás de los heads reales. Los heads siempre se verificaron en vivo antes de cada push y no hay otro escritor; el registro queda incompleto, no incorrecto.

## Cierre

La prueba cubrió el flujo completo del pack con un caso clínico real, de la spec al componente, con validación del usuario en cada puerta. El pack salió de la prueba en v0.16.0 con 15 skills, la guía publicada y verificada en vivo, y el componente subido y verificado en remoto. Lo que no se pudo probar (harness real) y lo que quedó pendiente (explorador v0.16.0, `plugin.json`, contabilidad de sync) está anotado arriba, no escondido.
