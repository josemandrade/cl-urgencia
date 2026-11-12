# Validation — dau-urgencia-red

## 2026-11-11 — Paso 5 validado por el usuario (Guía de Implementación)

- Artefact: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`
- Tool / profile: validación del usuario en chat ("Valido la Guía de Implementación")
- Result: passed — paso 5 cerrado; la guía y el workflow quedan como fuente de verdad del paso 6. El usuario pidió la URL de la guía desplegada en GitHub Pages.
- Failures: ninguna.
- Evidence: respuesta del usuario (widget de validación).

## 2026-11-11 — Paso 5: guía con SUSHI (Tasks 1–18) terminada y presentada

- Artefact: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`, `.gitignore`
- Tool / profile: SUSHI v3.21.0 (`sushi .` en la carpeta de la guía)
- Result: passed — SUSHI compila con **0 errores y 0 warnings** ("Just like a perfect pearl"). 17 StructureDefinitions (10 perfiles + 7 extensiones), 3 ValueSets, 2 CodeSystems, 14 instancias; los 14 ejemplos validan contra sus perfiles. Verificado en el JSON generado (`fsh-generated/resources/`): el Encounter de alta tiene status finished y `hospitalization.dischargeDisposition` 03, el Bundle de alta es transaction con 4 PUT, el Bundle de admisión trae los POST con ifNoneExist. El workflow YAML parsea (2 jobs, 9 pasos en build).
- Failures: la primera compilación de los perfiles dio 3 errores — `dischargeDisposition` no existe como elemento directo de Encounter en FHIR R4; es `Encounter.hospitalization.dischargeDisposition`. Se corrigieron el FSH y el invariante `dau-alta-destino`, y la siguiente compilación quedó en 0 errores.
- Evidence: salida de SUSHI (0 Errors, 0 Warnings), `fsh-generated/resources/` (36 recursos JSON), YAML del workflow validado.

## 2026-11-11 — Paso 4 validado por el usuario (propuesta FHIR + mapeo + diagrama)

- Artefact: `04-fhir-proposal.md`, `04-mapping-table.md`, `04-fhir-proposal-graph.svg`
- Tool / profile: validación del usuario en chat ("Valido la propuesta FHIR y el mapeo")
- Result: passed — paso 4 cerrado; la propuesta, el mapeo, la revisión IHE y el diagrama quedan como fuente de verdad del paso 5.
- Failures: ninguna.
- Evidence: respuesta del usuario (widget de validación).

## 2026-11-11 — Corrección del paso 4: diagrama de recursos estilo ClinFHIR GraphBuilder

- Artefact: `04-fhir-proposal.md` (sección 2, "Diagrama de recursos"), `04-fhir-proposal-graph.svg`, `render_fhir_graph.py`
- Tool / profile: corrección del usuario en chat ("a la propuesta de recursos le hace falta un diagrama como los que se construyen con el graphbuilder de clinfhir")
- Result: passed — el diagrama muestra los 8 recursos y el PDF, con las 12 referencias etiquetadas por el elemento que las lleva, el `Encounter` como centro y el `Bundle` como marco punteado. Generado con un script durable (`render_fhir_graph.py`) y verificado visualmente (render a PNG con cairosvg y revisión de la imagen: etiquetas sin solaparse —se movió `participant.individual` para no chocar con `hospitalization.destination`—, sin cruces entre flechas).
- Failures: la primera versión tenía las etiquetas `hospitalization.destination` y `participant.individual` solapadas; se corrigió moviendo la segunda sobre su diagonal, junto al nodo Practitioner.
- Evidence: `04-fhir-proposal-graph.svg` (SVG bien formado, 11 KB) y el render verificado.

## 2026-11-11 — Paso 3 validado por el usuario (entidades y datos)

- Artefact: `03-entities-data.md`
- Tool / profile: validación del usuario en chat ("Valido las entidades y sus datos")
- Result: passed
- Failures: none
- Evidence: 12 entidades con campos, identificadores, origen, obligatoriedad y tabla de calidad y propiedad.

## 2026-11-11 — El fallecimiento es un alta con destino 03 (corrige la nota anterior)

- Artefact: `04-fhir-proposal.md` (sección 5), `04-mapping-table.md` (CONDICIÓN AL CIERRE)
- Tool / profile: revisión en vivo de la guía cl-urgencia v0.2.0 (ValueSet "Destino al alta de urgencia" y perfil EncuentroUrgenciaAlta)
- Result: passed — la guía **sí** contempla el fallecimiento como destino de alta: el ValueSet `vs-destino-alta` incluye el código `03 Fallecido` (`system = https://interoperabilidad.minsal.cl/fhir/ig/urgencia-eventos/CodeSystem/destino-alta`) y el perfil de alta liga `dischargeDisposition` 1..1 a ese ValueSet (requerido). El mapeo CMBD deduce "CONDICIÓN AL CIERRE: `03 Fallecido` → fallecido".
- Failures: la spec v3 y el BPMN v4 decían que "la guía no lo contempla": impreciso. La guía no nombra un evento separado de fallecimiento, pero el código existe en el ValueSet del alta. Consecuencia: no hace falta un Bundle nuevo ni un código nuevo; el fallecimiento es un evento de alta con `dischargeDisposition = 03`, `period.end` = hora del fallecimiento, diagnóstico de egreso = causa de muerte (CIE-10, `use = DD`) y documento de resumen de alta (LOINC 59258-4).
- Evidence: https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/ValueSet-vs-destino-alta.html (6 conceptos, incluye `03` Fallecido) y https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/StructureDefinition-encuentro-urgencia-alta.html (`dischargeDisposition` 1..1, binding requerido a "Destino al alta de urgencia").

## 2026-11-11 — Subidas a GitHub verificadas

- Artefact: `health-interop-superpowers` (pack v0.6.0) y `cl-urgencia` (carpeta de trabajo)
- Tool / profile: conector GitHub (snapshot push) + verificación remota (list_commits, get_file_contents)
- Result: passed — pack: main `bc1bcca` (39 archivos, skill.yaml 0.6.0 con 14 skills) sobre `a1daa78`. Caso: main `2cefbfb` (9 archivos) sobre el commit inicial `dd5b450` del proveedor, que dejó un README.md vacío en la raíz.
- Failures: none — el 403 anterior se resolvió cuando el usuario incluyó `cl-urgencia` en la instalación de la GitHub App.
- Evidence: registros de sync guardados (5 entradas en el pack, 1 en el caso).

## 2026-11-11 — Paso 2 validado por el usuario (BPMN v4 + spec v3)

- Artefact: `02-bpmn-model.bpmn`, `02-bpmn-model.md` (revisión 4), `01-use-case-spec.md` (revisión 3)
- Tool / profile: validación del usuario en chat ("Valido el BPMN v4 y la spec v3")
- Result: passed
- Failures: none
- Evidence: XML revalidado (0 referencias sin resolver, 25 tareas, 4 puertas, 3 eventos de borde, 41 flujos de secuencia); SVG re-renderizado.

## 2026-11-11 — Repaso IHE temprano verificado en vivo

- Artefact: `02-bpmn-model.md`, sección "IHE landscape scan"
- Tool / profile: `ihe-landscape-scan` contra https://profiles.ihe.net/ (dominio ITI y PCC) y la wiki de IHE
- Result: passed — 12 perfiles candidatos verificados: PIXm v3.1.0, PDQm v3.2.0, MHD v4.2.5, mCSD v4.0.0 (todas Publication, FHIR R4), QEDm v3.0.0 (Publication, FHIR R4, dominio PCC), y los clásicos PIX, PDQ, XDS.b, XDR, DSUB, NAV, ATNA, CT, BPPC en ITI TF Rev 20.2 (Final Text, última revisión 20.2 del 11 de noviembre de 2025)
- Failures: none — la URL https://profiles.ihe.net/ITI/QEDm/ devolvió 404: QEDm es del dominio PCC, no ITI; la página correcta es https://profiles.ihe.net/PCC/QEDm/
- Evidence: sección "IHE landscape scan" en `02-bpmn-model.md`, con versión, estado, URL y fecha de verificación por perfil, y candidatos por punto de interoperabilidad en la tabla de PI.

## 2026-11-11 — Decisión Q3: fallecimiento como extensión del caso

- Artefact: `02-bpmn-model.bpmn` (v4), `01-use-case-spec.md` (revisión 3)
- Tool / profile: decisión del usuario en chat ("Incluirlo como extensión del caso")
- Result: passed (decisión registrada y aplicada)
- Failures: none — la guía v0.2.0 no contempla el fallecimiento; el caso lo incluye como extensión, y el valor exacto del desenlace y el contenido del evento se definen en el paso 4.
- Evidence: corrección C14 aplicada (tercera salida "Fallecimiento" de la puerta de desenlace → "Cerrar DAU (fallecido)" → publicar aviso); XML revalidado sin referencias sin resolver.

## 2026-11-11 — La prueba no ejerció el diálogo de brainstorming (hallazgo de la prueba)

- Artefact: `01-use-case-spec.md` (paso 1)
- Tool / profile: revisión del recorrido de la prueba contra la skill `brainstorming-health`
- Result: failed — el diálogo de brainstorming no se hizo
- Failures: (alto) la spec se redactó directamente desde la descripción del caso entregada por el usuario en un solo mensaje ("ese es el caso"), sin el diálogo del brainstorming: no se hicieron las preguntas del brainstorming (qué problema resuelve, quién lo usa, qué datos entran y salen, cómo se ve el éxito), ni se devolvió la comprensión en trozos cortos esperando corrección. La spec sí recoge problema, usuarios, roles, flujo, ejemplo y criterio de éxito, pero eso vino de la descripción del usuario y de la guía, no de un brainstorming. Consecuencia: las preguntas P1–P10 quedaron sin responder al inicio (por ejemplo, P1 cuándo se publica, P2 hub o punto a punto) y la comprensión del proceso llegó débil al paso 2 — la admisión ni siquiera estaba en la comprensión inicial, y solo la revisión experta la detectó en el BPMN v1. La validación del usuario ("la valido") cubrió el contenido de la spec, no el proceso del brainstorming.
- Evidence: origen de la spec ("descripción del usuario, 2026-11-11"); el usuario lo señaló en el chat el 2026-11-11 ("al usar el componente no usamos brainstorming").
- Fix aplicado: nueva regla en `brainstorming-health` (v0.6.0): aunque el usuario entregue una descripción completa en un solo mensaje, el diálogo del brainstorming se hace igual antes de redactar la spec.

## 2026-11-11 — Guía publicada v0.2.0 verificada en vivo (corrige la referencia de la revisión experta)

- Artefact: guía de Implementación FHIR — Urgencia (Admisión, Alta y Abandono) v0.2.0 (https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/index.html, modelo.html, arquitectura.html)
- Tool / profile: lectura directa de la guía publicada
- Result: passed (con correcciones a la referencia anterior)
- Failures: la guía v0.1.1 del build continuo usada por la revisión experta de la v1 estaba desactualizada en tres puntos: (1) el estado de admisión es `arrived`, no `in-progress`; (2) no existe un evento de Categorización — los estados intermedios (categorizado, en atención) no se informan; (3) el egreso no incluye el fallecimiento — los episodios cierran solo con alta o abandono. Además resuelve: tres transacciones Bundle (admisión/alta/abandono) sobre un solo Encounter por ID DAU; push al Bus + pull del Repositorio (con suscripción opcional); identidad por RUN con resolución en el MPI MINSAL; destinos de alta (domicilio, hospitalización 01, traslado 02, derivación 04); la categoría C1–C5 no viaja en el aviso.
- Evidence: páginas index/modelo/arquitectura de la guía v0.2.0 leídas el 2026-11-11; cambios reflejados en la spec revisión 2 y en el BPMN v3. Q3 (fallecimiento) queda en conflicto: el usuario respondió sí, la guía no lo contempla; decisión pendiente.

## 2026-11-11 — Revisión experta del modelo BPMN (v1)

- Artefact: `02-bpmn-model.bpmn` (v1)
- Tool / profile: revisión por experto en procesos de salud y gestión de urgencias, con referencia a la Guía de Interoperabilidad de Urgencia del MINSAL v0.1.1 (verificada en vivo: build.fhir.org/ig/Minsal-CL/IG_Urgencia/spec-events.html)
- Result: failed — el modelo no refleja el proceso real de urgencia
- Failures: (crítico) admisión ausente, colapsada en "Registrar atención en urgencia"; (crítico) NEA modelado como si el paciente hubiera sido atendido; (alto) el DAU se generaba antes del desenlace en vez de aperturarse en la admisión y cerrarse en el egreso; (medio) la fuga era salida de puerta en vez de interrupción; (medio) la tarea "Enviar DAU en PDF" no tenía flujos de secuencia; (bajo) faltaban los eventos de fin en los pools A y B
- Evidence: informe de revisión en el chat 2026-11-11; correcciones C1–C13 y C15–C16 aplicadas en el modelo v2; preguntas Q1–Q7 pendientes de decisión del usuario

## 2026-11-11 — Spec del caso validada por el usuario

- Artefact: `01-use-case-spec.md`
- Tool / profile: validación del usuario en chat ("la valido")
- Result: passed
- Failures: none
- Evidence: mensaje del usuario 2026-11-11 validando la spec; las preguntas P1–P10 quedan abiertas para los pasos siguientes, no bloquean el paso 2.
