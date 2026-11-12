# Decisions — dau-urgencia-red

## 2026-11-12 — El BPMN seguía ilegible: el problema era el ancho de visualización

- Context: tras reparar el render, el usuario dijo que el BPMN "sigue siendo ilegible". La causa no era el render (que ya estaba legible a resolución completa) sino el tamaño al que se mostraba en la guía: la página ponía la imagen a 2400 px de ancho, pero el PNG tiene 8640 px, así que el texto de 12 px se veía a ~7 px — ilegible. La verificación anterior miró el PNG a resolución completa, no al tamaño de visualización, y por eso no detectó el problema.
- Decision: la página muestra el BPMN a su ancho nativo (4320 px, el ancho del SVG), en un contenedor con scroll horizontal, con los botones de zoom y una nota que dice que hay que desplazarse a la derecha. A 4320 px el texto se ve a 12 px (su tamaño de diseño) y es legible. Se verificó mirando el diagrama AL TAMAÑO DE VISUALIZACIÓN (el PNG reducido a 4320 px, visto 1:1 por zonas): las etiquetas de la izquierda, las tareas, los PI y los eventos se leen. La skill lleva ahora la regla: mostrar cada diagrama a su ancho nativo (nunca achicarlo para que quepa en la columna) y verificar la legibilidad AL TAMAÑO DE VISUALIZACIÓN, no solo a resolución completa. El PNG no cambia (es el mismo archivo 2×), solo cambia la página.
- Consequences: el BPMN es legible en la guía (hay que desplazarse en horizontal para recorrerlo, que es lo normal en un BPMN ancho). El zoom parte de 4320 px ("100%" = ancho nativo).

## 2026-11-12 — El BPMN se veía muy mal: se repara el render y la skill

- Context: el usuario vio que la imagen del BPMN en la guía "se ve muy pero muy mal". La causa no era el modelo BPMN (validado) sino el render (`render_bpmn.py`): dibujaba el nombre de cada pool Y de cada lane como texto vertical rotado en la misma franja (x=56), y los nombres (35–60 caracteres) eran mucho más largos que sus lanes (75–155 px), así que se apilaban en un muro ilegible; además las etiquetas de los flujos de mensaje (PI) se ponían en el centroide de todos los waypoints, donde 5–6 etiquetas caían en la misma zona y se solapaban, y la etiqueta del evento de borde "Paciente se retira (fuga)" (2 líneas) caía sobre la caja de la tarea siguiente (solo 15 px de hueco).
- Decision: se reescribió el render: nombres de pool y lane en horizontal en una columna de etiquetas a la izquierda (240 px; pool pequeño y atenuado arriba, lane en negrita centrado), etiquetas de flujo cortas (los PI sin el paréntesis) sobre el segmento más largo, ninguna etiqueta puede solapar a otra (todas las etiquetas fuera de su forma —nombres de gateway/evento/objeto de datos y etiquetas de flujo— se descolisionan juntas, y las de flujo llevan fondo blanco), las etiquetas de evento de borde en una sola línea y pequeñas, y el PNG a 2× (8640×1620) para que el texto sea nítido al acercar. Se miró el PNG antes de darlo por bueno (varias zonas ampliadas) y se corrigió hasta que quedó legible. La skill `bpmn-modeling` lleva ahora la puerta dura: renderizar y MIRAR el PNG antes de presentar el modelo, con las reglas de legibilidad; `implementation-guide-sushi` exige lo mismo al volver a renderizar para la guía.
- Consequences: el BPMN ahora se lee (columna de etiquetas limpia, PI legibles, sin solapamientos). El PNG es más grande (537 KB, 8640×1620) y al ser binario hay que subirlo por la web de GitHub.

## 2026-11-12 — Los diagramas van como PNG directo, con zoom in / zoom out

- Context: el usuario pidió que los diagramas se agreguen directo como JPG o PNG (o un mejor formato), y para el BPMN lo mismo; y, si hace falta, configurar zoom in / zoom out. El SVG en un `<img>` no se veía de forma fiable para el usuario, aunque el archivo cargaba y renderizaba.
- Decision: los diagramas se incrustan como PNG directo en las páginas: el grafo de recursos a 2× (2440×1800) y el BPMN a su ancho nativo (4080×810), ambos generados desde los SVG (que quedan como fuente en la carpeta del caso) y copiados a `input/images/`. Las páginas (`process.md`, `resources.md`, `profiles.md`) muestran el PNG con botones Zoom in (+), Zoom out (−) y 100%, y un pequeño script inline que escala el ancho de la imagen (×1.25 / ×0.8 por clic, entre 400 y 8000 px; 100% restaura el ancho original). El script va en la misma página que la imagen (cada página lo define), porque las páginas son independientes. El contenedor tiene scroll horizontal para el BPMN. La skill `implementation-guide-sushi` lleva la regla (PNG directo, no SVG en `<img>`; zoom con botones y script; verificar en la página publicada que el script sobrevive al publisher).
- Consequences: los diagramas se ven directo en la página, sin depender del render del SVG, y el lector puede acercar y alejar.

## 2026-11-12 — El diagrama de recursos tiene su propia página (no solo va en Perfiles)

- Context: el usuario miró la guía y no vio el diagrama de recursos, lo que le hizo dudar de la skill. El diagrama SÍ estaba publicado (en `profiles.html`, sección "Diagrama de recursos", con el SVG en 200 y renderizando bien — verificado en vivo y renderizado a PNG), pero estaba enterrado en la mitad de la página de Perfiles: hay que abrir "Perfiles" y bajar para encontrarlo, y el índice solo lo enlazaba. La regla de la skill ("mostrar el diagrama en la página de Perfiles") era demasiado débil: un diagrama que solo vive dentro de otra página es fácil de no encontrar, y el lector concluye que no se subió.
- Decision: el diagrama de recursos tiene su propia página (`resources.md`, "Diagrama de recursos") con su propia entrada en el menú, igual que el BPMN tiene su propia página ("Proceso (BPMN)"). El diagrama sigue también en `profiles.md` (donde se listan los recursos) y enlazado desde el índice. La skill `implementation-guide-sushi` queda corregida: ambos diagramas (BPMN y recursos) tienen su propia página y su propia entrada en el menú, para que sean visibles como pestañas de primer nivel; `fhir-modeling` igual. El BPMN ya era encontrable por tener su propia pestaña, y eso confirma el patrón.
- Consequences: el diagrama es visible desde el menú sin abrir otra página; la skill ya no permite enterrarlo dentro de Perfiles.

## 2026-11-12 — La guía incluye el BPMN y el diagrama de recursos, y el header es una barra horizontal

- Context: la guía publicada no mostraba el BPMN ni el diagrama de recursos (estaban en la carpeta del caso, fuera de la guía), y el header se veía como una lista vertical de pestañas. El `menu.xml` era un `<ul>` sin clase, y el `index.md` enlazaba el diagrama de recursos a la propuesta en GitHub (fuera de la guía).
- Decision: la guía incluye el BPMN (página nueva `process.md`, con el diagrama SVG, el flujo paso a paso y la tabla de PI) y el diagrama de recursos (sección "Diagrama de recursos" en `profiles.md`, con el `Encounter` como centro). Ambos SVG se copiaron a `05-implementation-guide/input/images/` (el publisher los publica como `images/<archivo>`) y se referencian como `images/<archivo>`; el BPMN (4080×810) va en un contenedor con scroll horizontal y enlaza al SVG a tamaño completo. El header se repara: `menu.xml` pasa a ser `<ul class="nav navbar-nav">` (las clases Bootstrap que ponen las pestañas en horizontal; sin ellas el `<ul>` se ve como lista vertical). Las skills `implementation-guide-sushi` (la guía debe incluir el BPMN y el diagrama, con las imágenes dentro de la carpeta de la guía; el menú debe ser `<ul class="nav navbar-nav">` y el header se verifica en vivo) y `fhir-modeling` (el BPMN y el grafo de la propuesta se llevan a la guía) llevan ambas reglas.
- Consequences: el lector ve el proceso y los recursos dentro de la guía, sin salir a GitHub; el header es una barra de navegación horizontal.

## 2026-11-12 — Cada operación de la guía enlaza a su perfil IHE (buscar paciente → PDQm)

- Context: la guía tenía la revisión IHE por punto en su propia página (`ihe.md`), pero las operaciones en `operations.md` no enlazaban a ningún perfil IHE, y la búsqueda del paciente (PDQm) ni siquiera estaba como operación: PI-2 listaba solo las búsquedas de `Encounter`, `Condition` y `DocumentReference`.
- Decision: cada operación de la guía enlaza al perfil IHE que la apoya (página en profiles.ihe.net, con el encaje y las transacciones cuando aplican): las tres transacciones push enlazan a PIXm (identidad) y MHD (documento); PI-0 enlaza a PIXm; PI-2 se reestructura en operaciones nombradas — buscar paciente → PDQm (ITI-78, ITI-119), buscar episodios → QEDm (PCC-44), buscar diagnósticos → QEDm, buscar documento → MHD (ITI-67), suscripción → Subscription FHIR (DSUB refutado); PI-3 enlaza a MHD (ITI-68). Se añade la operación `GET /Patient?identifier=<sistema RUN>|<RUN>` (buscar paciente por RUN). Cada operación dice cuando ningún perfil IHE lleva la transacción (la transacción es nacional; el perfil cubre una función de apoyo). La propuesta pasó a revisión 3 (sección 6 con el perfil IHE por operación). Las skills `implementation-guide-sushi` (enlazar cada operación a su perfil IHE, incluidas las búsquedas) y `fhir-modeling` (la propuesta lista el perfil IHE por operación) llevan la regla.
- Consequences: la página de operaciones es ahora el mapa entre cada operación y su estándar IHE; el lector llega al perfil desde la operación, no solo desde la página de IHE.

## 2026-11-12 — `DAUPaciente` se mantiene sobre el `Patient` base de FHIR R4 (no sobre `PatientCL`)

- Context: en la revisión 2 de la propuesta se ofreció elegir otro recurso base; el ejemplo era que `Patient` se basara en `PatientCL` / `CorePacienteCl` de la guía core de Chile. Se verificó que es técnicamente posible (paquete FHIR `hl7.fhir.cl.clcore` 1.9.4 resoluble por SUSHI, `baseDefinition: https://hl7chile.cl/fhir/ig/clcore/StructureDefinition/CorePacienteCl`, 0 errores).
- Decision: el usuario eligió mantener el base de FHIR R4 (`http://hl7.org/fhir/StructureDefinition/Patient`) para `DAUPaciente`. No se añade la dependencia `hl7.fhir.cl.clcore` y el `Parent:` sigue siendo `Patient`. La oferta queda registrada en la propuesta (sección 2) por si en otro caso se quiere elegir otro base.
- Consequences: la guía sigue con la única dependencia `hl7.fhir.r4.core`; `DAUPaciente` no hereda las restricciones de CL-Core.

## 2026-11-12 — Ofrecer asociaciones y el recurso base en la propuesta (revisión 2 de la propuesta)

- Context: el usuario pidió que las skills ofrezcan las asociaciones a otras guías FHIR o perfiles IHE cuando corresponda, y que la propuesta de recursos deje la URL del recurso base que se propone e informe que se puede elegir otro base en ese lugar (por ejemplo, `Patient` con base `PatientCL` / `CorePacienteCl` de la guía core de Chile).
- Decision: se configuraron las skills `fhir-modeling` (la propuesta lista cada recurso con su base y su URL canónica, e invita a elegir otro base), `implementation-guide-sushi` (ofrecer la asociación cuando corresponda; el `Parent:` es el base elegido en la propuesta validada; si es de otra guía, se añade su paquete FHIR como dependencia si es resoluble) e `ihe-profile-review` (ofrecer la asociación cuando un perfil encaje, en vez de asumirla). La propuesta `04-fhir-proposal.md` pasó a revisión 2: perfiles propios con su base (FHIR R4) y su URL canónica, y la invitación a elegir otro base. Verificado: CL-Core SÍ está como paquete FHIR resoluble (`hl7.fhir.cl.clcore`, última 1.9.4, también 1.9.2); SUSHI resuelve `CorePacienteCl` como `Parent:` (0 errores, `baseDefinition: https://hl7chile.cl/fhir/ig/clcore/StructureDefinition/CorePacienteCl`), corrigiendo la suposición del paso 5 de que no lo estaba. Pendiente la decisión del usuario: si `DAUPaciente` pasa a basarse en `PatientCL` (se usaría CL-Core 1.9.4).
- Alternatives considered: mantener la suposición del paso 5 (rechazado por la verificación en vivo del registro de paquetes); usar CL-Core 1.9.2 (la que citaba la guía del MINSAL) en vez de 1.9.4 (pendiente de la elección del usuario si toma PatientCL).
- Consequences: las skills ahora ofrecen las asociaciones como elección explícita; la propuesta registra el base de cada recurso con su URL.

## 2026-11-12 — Los perfiles son propios de esta guía; la guía documenta su relación con IHE

- Context: el usuario corrigió que la guía se presentaba como transcripción de los perfiles de la guía del MINSAL (cl-urgencia v0.2.0) y de CL-Core, y que no mostraba las relaciones con los perfiles IHE. La revisión IHE por punto del paso 4 existía (en `04-fhir-proposal.md`) pero no estaba en la guía publicada.
- Decision: los perfiles (`DAU...`) son propios de esta guía, diseñados a partir de la especificación del caso de uso (entidades y datos de los pasos 1–3) sobre los recursos base de FHIR R4. No se transcriben los perfiles de otra guía ni se depende de otro paquete (MINSAL, CL-Core). Los datos que codifican (ID DAU, RUN, código DEIS, destinos 01–06, tipo de abandono 1–2, códigos NID, LOINC) son los que el caso de uso exige informar a la red; la guía nacional del MINSAL es la referencia de esos requisitos de datos, no la fuente de los perfiles. Las restricciones (cardinalidades, invariantes, bindings) no cambian: son las que la spec exige, así que los ejemplos siguen validando. Se reescribieron las descripciones y los comentarios del FSH y de las páginas (index, profiles, terminology). Además, la guía ahora tiene una página "Relación con IHE" (`ihe.md`) con la revisión por punto (PI-0 a PI-3, encaje total/parcial/no encaja, actores, transacciones y brechas), enlazada desde el índice y el menú. La skill `implementation-guide-sushi` del pack lleva ambas reglas (perfiles propios; página de relaciones IHE).
- Alternatives considered: redefinir los códigos de datos desde cero (rechazado: los códigos son los datos que la red espera; cambiarlos rompería la interoperabilidad con la red nacional); mantener la presentación como transcripción (rechazado por el usuario).
- Consequences: la guía ya no reclama ni sugiere ser los perfiles del MINSAL; es una guía de prueba con perfiles propios sobre FHIR R4. Si algún día la guía se alineara a los perfiles del MINSAL, habría que declarar la conformidad explícita y cambiar los `Parent:` (hoy son los recursos base).

## 2026-11-12 — El id de la guía pasa a `hl7.fhir.uv.test.dau-urgencia-red` (reino `uv`, no `cl`)

- Context: la guía nació con id `hl7.fhir.cl.test.dau-urgencia-red` para reflejar el nombre de la guía del MINSAL (`hl7.fhir.cl.minsal.urgencia.eventos`). Al publicar en CI, la plantilla `hl7.base.template` rechazó el id ("Unrecognized realm in id... where realm is uv, us or eu") — su XSLT `onGenerate.genProperties.xslt` solo acepta los reinos `us`, `uv` y `eu`. La alternativa, la plantilla genérica `fhir.base.template`, sí acepta `cl`, pero necesita Jekyll para armar el sitio y Jekyll no está en el runner de GitHub (el run 3 falló en "Cannot run program jekyll"). El usuario eligió cambiar el id a `uv`.
- Decision: el id (y `packageId`) de la guía es `hl7.fhir.uv.test.dau-urgencia-red`, versión `0.1.0`, canonical `https://josemandrade.github.io/cl-urgencia/` (sin cambios). La plantilla vuelve a `hl7.base.template#current` (la actual, sin Jekyll).
- Alternatives considered: mantener `cl` e instalar Jekyll en el workflow (rechazado por el usuario: la plantilla genérica está marcada "no longer considered secure" por el publisher y añade un paso frágil al workflow); usar una copia local de la plantilla HL7 con el chequeo de reino quitado (rechazado: un fork de la plantilla es frágil).
- Consequences: el id ya no refleja el reino chileno; sigue siendo una guía de prueba (el segmento `.test.` lo marca). Si algún día se publica como guía chilena oficial, el id deberá volver a `hl7.fhir.cl.*` y la plantilla deberá ser la genérica con Jekyll (como la guía del MINSAL).

## 2026-11-11 — La guía es una guía de prueba, no la guía del MINSAL

- Context: la guía del paso 5 se construye sobre los perfiles de la guía cl-urgencia v0.2.0 del MINSAL, pero no es esa guía y no puede depender de su paquete (no está publicado como paquete FHIR que SUSHI pueda resolver), igual que CL-Core.
- Decision: la guía tiene id `hl7.fhir.cl.test.dau-urgencia-red`, versión `0.1.0`, canonical `https://josemandrade.github.io/cl-urgencia/` (el sitio de GitHub Pages del repo cl-urgencia), y solo depende de `hl7.fhir.r4.core 4.0.1`. Los perfiles se definen en local con nombres propios (`DAUEncuentroUrgencia`, no `EncuentroUrgencia`) para no reclamar ser los perfiles del MINSAL, y se citan como fuente la guía v0.2.0.
- Alternatives considered: depender del paquete de la guía del MINSAL o de CL-Core (rechazado: no están en packages.fhir.org y SUSHI no los resolvería; la guía no compilaría).
- Consequences: las restricciones de la guía v0.2.0 se transcriben en los perfiles locales; si la guía del MINSAL cambia, la transcripción se actualiza a mano.

## 2026-11-11 — En FHIR R4, el destino al alta es `hospitalization.dischargeDisposition`

- Context: el FSH inicial usó `dischargeDisposition` como elemento directo de Encounter; SUSHI devolvió 3 errores ("No element found at path dischargeDisposition").
- Decision: la ruta correcta en FHIR R4 es `Encounter.hospitalization.dischargeDisposition`. Se corrigieron el perfil de alta, el de abandono y el invariante `dau-alta-destino`.
- Alternatives considered: ninguna (es la estructura de FHIR R4).
- Consequences: la propuesta y la guía usan `dischargeDisposition` como nombre corto en la prosa, pero el FSH y el JSON usan la ruta completa.

## 2026-11-11 — El diagrama de recursos sigue el estilo de ClinFHIR GraphBuilder

- Context: el usuario corrigió la propuesta porque le faltaba un diagrama como los de GraphBuilder (https://clinfhir.com/): cada recurso es un rectángulo con título y tipo, y las referencias son flechas direccionales etiquetadas con el elemento que las lleva.
- Decision: el diagrama (`04-fhir-proposal-graph.svg`) se genera con un script durable (`render_fhir_graph.py`, en la raíz de la carpeta de trabajo) y se enlaza en la propuesta. El `Bundle` es el marco punteado que envuelve el grafo. `Organization` aparece dos veces (emisor y destino) porque son dos instancias distintas —evita dibujar dos flechas al mismo nodo—. El PDF DAU se dibuja con borde punteado porque no es un recurso FHIR.
- Alternatives considered: usar GraphBuilder en el navegador (rechazado: herramienta interactiva, lenta y poco reproducible; el SVG generado localmente tiene el mismo estilo y se puede regenerar).
- Consequences: el script es la fuente del diagrama; si cambian los recursos o las referencias, se edita el script y se regenera el SVG.

## 2026-11-11 — El fallecimiento se informa como alta con destino 03 Fallecido

- Context: la spec v3 y el BPMN v4 decían que la guía no contemplaba el fallecimiento y que el valor del desenlace se definiría en el paso 4. Al revisar la guía en vivo para la propuesta, apareció el código `03 Fallecido` en el ValueSet del alta.
- Decision: el fallecimiento es un **evento de alta** (Bundle de alta, perfil EncuentroUrgenciaAlta) con `dischargeDisposition = 03 Fallecido`, `period.end` = hora del fallecimiento, diagnóstico de egreso = causa de muerte (CIE-10, `use = DD`) y documento de resumen de alta (LOINC 59258-4). No se crea un Bundle nuevo ni un perfil nuevo.
- Alternatives considered: un Bundle nuevo de fallecimiento con un código nuevo (rechazado: el código ya existe y el perfil de alta lo acepta); una extensión en el `Encounter` (rechazado: rompería el reconocimiento de eventos de la guía); registrar la muerte en `Patient.deceased` (rechazado: los maestros son solo creación, nunca se modifican).
- Consequences: la rama "Fallecimiento" del BPMN v4 se mantiene como rama clínica, pero mapea a la transacción de alta. La nota "la guía no lo contempla" queda corregida en `validation.md`.

## 2026-11-11 — El repaso IHE temprano se hizo al inicio del paso 3, no antes del BPMN

- Context: la skill `ihe-landscape-scan` se creó en el pack cuando el BPMN v4 ya estaba modelado y validado. El flujo del componente dice que el repaso corre tras validar la spec y antes del BPMN.
- Decision: en esta prueba el repaso se hizo al inicio del paso 3 y quedó registrado en `02-bpmn-model.md`, con los candidatos por punto de interoperabilidad, para que el paso 4 los confirme o refute.
- Alternatives considered: rehacer el BPMN con el repaso en mente. Rechazado: el BPMN ya estaba validado; el repaso no cambia el modelo, solo anota los candidatos.
- Consequences: en los próximos casos el repaso corre antes del BPMN; en esta prueba el BPMN se dibujó sin él.

## 2026-11-11 — El estudio IHE va en dos momentos

- Context: el usuario cuestionó la ubicación del estudio IHE (en el paso 4): como el proceso se obtiene y se aclara con una guía, quizás el estudio IHE debería venir después del brainstorming. La propuesta fue dividirlo en dos momentos.
- Decision: (1) un repaso temprano de perfiles IHE (`ihe-landscape-scan`) tras validar la spec y antes del BPMN, para que el modelo se dibuje con los perfiles en mente; (2) la revisión experta detallada por punto (`ihe-profile-review`) sigue en el paso 4, confirmando o refutando cada candidato.
- Alternatives considered: mover el estudio entero después del brainstorming. Rechazado: la revisión detallada por punto necesita el BPMN y las entidades; sin ellos no se puede juzgar el ajuste.
- Consequences: el componente queda en v0.6.0 local (14 skills); el repaso temprano se escribe en `02-bpmn-model.md`.

## 2026-11-11 — La spec no se redacta desde una descripción de un solo mensaje

- Context: la prueba mostró que el diálogo de brainstorming no se ejerció: la spec se redactó desde la descripción del usuario en un solo mensaje.
- Decision: nueva regla en `brainstorming-health` (v0.6.0): aunque el usuario entregue una descripción completa, el diálogo del brainstorming se hace igual (preguntas, devolución en trozos cortos, esperar corrección) antes de redactar la spec.
- Alternatives considered: ninguna; es el contenido de la skill que no se siguió.
- Consequences: los próximos casos harán el diálogo aunque el usuario describa el caso completo de entrada.

## 2026-11-11 — Se usa el caso DAU urgencia como caso de la prueba

- Context: el usuario pidió probar el componente y luego entregó este caso clínico: el mínimo que un establecimiento debe informar a la red cuando atiende a una persona en su unidad de urgencia.
- Decision: el recorrido de prueba usa este caso real (no uno inventado). La carpeta es `2026-11-11-dau-urgencia-red`.
- Alternatives considered: inventar un caso sintético (presión arterial de APS a cardiología). Rechazado: el usuario dio un caso concreto y dijo "ese es el caso".
- Consequences: la prueba produce la spec, el BPMN, la propuesta FHIR y el componente para este caso.

## 2026-11-11 — Datos sintéticos en toda la prueba

- Context: el caso es clínico y la skill `privacy-safety-health` exige datos sintéticos por defecto.
- Decision: todos los ejemplos, tests y goldens usan datos sintéticos (identificadores SYN-*, establecimientos ficticios). Nada de datos reales de pacientes.
- Alternatives considered: ninguna; es una regla del componente.
- Consequences: los ejemplos no son clínicamente reales; sirven para probar la estructura, no para uso asistencial.

## 2026-11-11 — La prueba se hace en esta sesión, paso a paso

- Context: el agente de prueba se detuvo al denegarse el permiso de terminal, y Codex no tiene credenciales, así que la prueba de aceptación en harness real quedó bloqueada.
- Decision: el usuario eligió que la prueba se haga aquí mismo, paso a paso, siguiendo las skills y sus puertas de validación.
- Alternatives considered: re-autorizar la terminal al agente de prueba; dejar la prueba en pausa. Rechazadas por el usuario al elegir esta opción.
- Consequences: cada paso se presenta al usuario para validación antes de avanzar (puerta dura del paso 1: nada pasa a BPMN sin spec validada).
