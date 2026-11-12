# Modelo BPMN — Aviso mínimo de atención de urgencia a la red (DAU)

- **Estado:** v5, presentado para validación (2026-11-12). La v4 fue validada por el usuario el 2026-11-11; esta v5 solo reordena el dibujo y corrige de qué tarea sale PI-3 (ver Historial). El proceso y las tareas son los mismos.
- **Fecha:** 2026-11-11 (v5: 2026-11-12)
- **Archivo BPMN:** `02-bpmn-model.bpmn` (BPMN 2.0, con diagrama)
- **Spec de origen:** `01-use-case-spec.md` revisión 3 (tres eventos + fallecimiento como extensión; validada por el usuario el 2026-11-11)
- **Referencia de proceso:** Guía de Implementación FHIR — Urgencia (Admisión, Alta y Abandono) v0.2.0 del MINSAL, publicada en https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/ (modelo de eventos y arquitectura verificados en vivo el 2026-11-11). **Corrige la referencia anterior**: la guía v0.1.1 del build continuo (build.fhir.org) que usó la revisión experta de la v1 está desactualizada en tres puntos: el estado de admisión es `arrived`, no `in-progress` (en FHIR R4, `in-progress` indica que el paciente ya está con el profesional); no existe un evento de Categorización (los estados intermedios categorizado y en atención no se informan); y el egreso no incluye el fallecimiento (los episodios cierran solo con alta o abandono).
- **Historial:** la v1 fue revisada por un experto en procesos de salud (2026-11-11). La v2 aplicó sus correcciones C1–C13 y C15–C16. La v3 aplicó las respuestas del usuario a Q1, Q2, Q4 y Q6, más lo que la guía v0.2.0 resuelve de Q5 y Q7. La v4 aplica la decisión Q3 (fallecimiento como extensión del caso). La v5 (2026-11-12) reordena el dibujo para que se lea sin solapamientos: la rama "Enviar DAU en PDF" pasa a una segunda fila del carril HIS/RCE (antes compartía fila con el evento de fin "Episodio cerrado / aviso publicado" y sus etiquetas se solapaban), y corrige PI-3: la solicitud del DAU sale de la tarea "Solicitar y recibir DAU en PDF" (antes salía de "Consultar episodios en el repositorio", que no es quien la envía). Las tareas, los flujos y la semántica del proceso no cambian.

## El diagrama (descrito)

Tres participantes (pools), de arriba a abajo:

1. **Establecimiento informante — Unidad de Urgencia**, con cuatro carriles:
   - *Admisión / Registro*: la persona llega → puerta **¿Emergencia vital?** (nuevo: si es C1, va directo a la atención y la admisión administrativa se completa en paralelo o después) → recepcionar (llegada y procedencia) → identificar (doble verificador) → datos sociodemográficos y previsión → motivo de consulta → aperturar DAU e instalar brazalete → informar la llegada al Selector de Demanda. También constata el abandono NEA.
   - *Categorización / Selector de Demanda*: categorizar paciente (C1–C5) → asignar box → puerta ¿Categoría? (C1 directo a atención; C2–C5 a esperar atención). El NEA puede ocurrir esperando la categorización (nuevo evento de borde sobre "Categorizar paciente") o esperando la atención (evento de borde sobre "Esperar atención").
   - *Equipo clínico de Urgencia*: atender clínicamente → **informar al paciente o familiares** (nuevo) → puerta de desenlace (la decide el Terminador, médico u odontólogo) → si es alta, indicar medicamentos al alta. También constata el abandono por fuga.
   - *HIS / RCE*: crear el episodio DAU en el HIS (ID DAU) → **publicar el evento de admisión a la red** (nuevo, PI-0) → cerrar el DAU y generar el PDF (después del desenlace, en ambas ramas) → publicar el aviso de alta o abandono (PI-1) → fin "Episodio cerrado / aviso publicado". También envía el DAU en PDF cuando llega una solicitud (evento de inicio de mensaje): esa rama va en una segunda fila del carril, para que su evento de inicio no se solape con el evento de fin del aviso.
2. **Bus de Interoperabilidad MINSAL y Repositorio FHIR**: evento de inicio de mensaje "Transacción recibida (admisión, alta o abandono)" → recibir la transacción y aplicarla en el repositorio → evento de fin "Episodio disponible en el repositorio". Además, un segundo flujo responde las consultas: evento de inicio "Consulta FHIR recibida" → responder la consulta de episodios → evento de fin "Episodios entregados".
3. **Punto de la red receptor (APS / Especialidad / Otro hospital / SAMU)**: consultar episodios en el repositorio (o suscribirse) → puerta ¿Necesita el detalle clínico? → si sí, solicitar y recibir el DAU en PDF → seguimiento; si no, seguimiento directo → fin.

El DAU nace en la Admisión (apertura, con su ID DAU) y se cierra en el Egreso (cierre y PDF). Nunca se "genera" antes del desenlace.

## Flujo, paso a paso

1. La persona llega a la urgencia (evento de inicio).
2. Puerta **¿Emergencia vital?**: si es C1, va directo a "Atender clínicamente" (la admisión administrativa se completa en paralelo o después — ver "Pendiente" abajo); si no, sigue la admisión.
3. Admisión: recepcionar (llegada y procedencia) → identificar con doble verificador → datos sociodemográficos y previsión → motivo de consulta → aperturar el DAU e instalar el brazalete → crear el episodio DAU en el HIS (ID DAU) → **publicar el evento de admisión a la red (PI-0)** → informar la llegada al Selector de Demanda.
4. Categorización: categorizar (C1–C5) → asignar box.
5. Puerta **¿Categoría?**: C1 → atención inmediata; C2–C5 → esperar atención.
6. **NEA:** si la persona se retira después de la admisión — esperando la categorización o esperando la atención (eventos de borde sobre "Categorizar paciente" y sobre "Esperar atención") — se constata el abandono (NEA) y el flujo va a la puerta de desenlace por la rama de abandono. El paciente NEA nunca fue atendido: no tiene hipótesis ni medicamentos.
7. Atención clínica → informar al paciente o familiares (si el paciente no puede recibir la información, se hace a familiares). **Fuga:** si la persona se retira durante la atención (evento de borde sobre "Atender clínicamente"), se constata el abandono (fuga) y el flujo va a la puerta de desenlace por la rama de abandono.
8. Puerta **¿Cómo termina la atención?** (decisión del Terminador):
   - **Alta** → indicar medicamentos al alta → cerrar el DAU y generar el PDF → publicar el aviso de alta (PI-1) → fin.
   - **Abandono** (NEA o fuga) → cerrar el DAU y generar el PDF → publicar el aviso de abandono (PI-1) → fin. En abandono no hay medicamentos al alta; en NEA, además, pueden no existir hipótesis ni PDF.
   - **Fallecimiento** (extensión del caso, no de la guía) → cerrar el DAU como fallecido y generar el PDF → publicar el aviso de fallecimiento (PI-1) → fin.
9. El Bus recibe cada transacción, la valida y la aplica en el Repositorio FHIR.
10. El punto receptor **consulta los episodios en el repositorio** (PI-2, pull) o está **suscrito** a los cambios de episodio.
11. Puerta **¿Necesita el detalle clínico?**: Sí → solicita el DAU, lo recibe en PDF y hace el seguimiento; No → hace el seguimiento con el aviso. Fin.

## IHE landscape scan

Repaso temprano de perfiles IHE (`ihe-landscape-scan`). Verificado en vivo el 2026-11-11 en https://profiles.ihe.net/ (dominio ITI, Technical Framework Rev 20.2, todos los perfiles normativos en Final Text, última revisión 20.2 del 11 de noviembre de 2025; guías de implementación FHIR en sus páginas oficiales; lista de perfiles en la wiki de IHE).

**Nota de orden:** en esta prueba el repaso se hizo al inicio del paso 3, porque la skill se creó cuando el BPMN v4 ya estaba modelado y validado. En los próximos casos corre tras validar la spec y antes del BPMN, como dice la skill. El repaso queda registrado aquí para que el paso 4 lo confirme o refute punto por punto.

El ajuste por punto (encaja / encaja parcial / no encaja) **se decide en el paso 4** (`ihe-profile-review`), no aquí. Un candidato es una posibilidad a tener en mente, no una decisión.

| Área | Perfil candidato | Versión / estado (verificado 2026-11-11) | Qué podría cubrir en este caso | Qué necesitaría |
|---|---|---|---|---|
| Identidad | **PIXm** (FHIR) | v3.1.0, Publication, activa 2025-11-04, FHIR R4. https://profiles.ihe.net/ITI/PIXm/ | Resolver la identidad de la persona atendida contra el MPI MINSAL: el Bus consulta las referencias cruzadas de identificadores (RUN ↔ identificador del MPI). Transacciones ITI-83 (consulta de referencias cruzadas) e ITI-104 (alimentación de identidad FHIR). | Un MPI que actúe como Patient Identifier Cross-reference Manager y el RUN (o un identificador alternativo) como identificador de origen. |
| Identidad | **PIX** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Lo mismo que PIXm, con la pila clásica (HL7v2). Se lista por completitud; en una arquitectura FHIR, PIXm es la preferida. | Lo mismo que PIXm, con mensajería HL7v2. |
| Demografía | **PDQm** (FHIR) | v3.2.0, Publication, activa 2025-11-04, FHIR R4. https://profiles.ihe.net/ITI/PDQm/ | Buscar a la persona por demografía (nombre, fecha de nacimiento) cuando no se conoce su identificador. Transacciones ITI-78 (consulta por demografía) e ITI-119 (coincidencia de demografía). En este caso el RUN es el dato de partida, así que su uso es marginal; se lista porque la guía prevé identificadores alternativos (pasaporte, RUN de la madre, identificador local) y pacientes sin RUN conocido. | Un proveedor de demografía (el MPI o el HIS) que responda consultas por demografía. |
| Demografía | **PDQ** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Lo mismo que PDQm, con la pila clásica. Se lista por completitud. | Lo mismo que PDQm, con mensajería HL7v2/v3. |
| Documentos | **MHD** (FHIR) | v4.2.5, Publication, activa 2026-10-18, FHIR R4. https://profiles.ihe.net/ITI/MHD/ | Compartir el DAU en PDF como documento: publicar el documento con sus metadatos (ITI-65 Provide Document Bundle), buscar referencias (ITI-67 Find Document References) y recuperar el documento (ITI-68 Retrieve Document). Es la vía FHIR del intercambio de documentos XDS; puede usarse como API al Repositorio FHIR y también en push. | El Repositorio como Document Recipient / Document Responder y el DAU como DocumentReference con metadatos XDS. |
| Documentos | **XDS.b** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | La vía clásica (SOAP/ebXML) del intercambio de documentos entre empresas. Cubre lo mismo que MHD con la pila clásica; en una arquitectura FHIR como la de la guía, MHD es la preferida. | Un registro y un repositorio de documentos XDS. |
| Documentos | **XDR** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Intercambio fiable punto a punto de documentos (push por web service). Cubre el push del DAU al Bus como documento; en la guía el push es una transacción Bundle FHIR, así que XDR es una alternativa clásica al push. | Un receptor de documentos que acepte el push. |
| Consulta de datos | **QEDm** (FHIR, dominio PCC) | v3.0.0, Publication, FHIR R4. https://profiles.ihe.net/PCC/QEDm/ | Consultar los datos existentes de la persona en el Repositorio: problemas, alergias, condiciones, medicamentos, procedimientos, encuentros y procedencia. Es la vía estándar para el pull de PI-2 (la red consulta el Repositorio). Transacción PCC-44 (Mobile Query Existing Data). | El Repositorio como Clinical Data Source y los códigos y el vocabulario de las consultas definidos en el despliegue. |
| Suscripción | **DSUB** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Suscripción a metadatos de documentos: el Repositorio avisa cuando aparece un documento que cumple un criterio. Cubre la opción de suscripción de PI-2 (la guía prevé Subscription sobre Encounter `class=EMER`; DSUB es su equivalente en el mundo XDS). | Un registro de documentos que soporte suscripciones. |
| Notificación | **NAV** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Notificación de disponibilidad de documentos: avisar fuera de banda que un documento de interés existe. Cubre el aviso a la red de PI-0/PI-1 como notificación (no como entrega del documento). | Un servicio de notificación y los suscriptores. |
| Descubrimiento | **mCSD** (FHIR) | v4.0.0, Publication, activa 2025-05-21, FHIR R4. https://profiles.ihe.net/ITI/mCSD/ | Descubrir los servicios de la red: organizaciones, ubicaciones, profesionales y servicios de salud. Cubre la derivación (hospitalización 01, traslado 02, derivación 04): encontrar el establecimiento de destino y sus servicios. Transacciones ITI-90 (buscar servicios coincidentes), ITI-91 (actualizaciones) e ITI-130 (alimentación de servicios). | Un directorio de servicios (Care Services Directory) con los establecimientos por código DEIS. |
| Consentimiento | **BPPC** (clásica) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Registrar el consentimiento de privacidad del paciente como documento. Los episodios restringidos (abuso sexual, violencia, constatación de lesiones) se marcan con seguridad R en la guía; BPPC es la vía IHE para documentar el consentimiento que habilita o restringe el acceso. | Un repositorio de consentimientos y la política de acceso que lo aplica. La versión avanzada (APPC) está en Trial Implementation. |
| Seguridad | **ATNA** (transversal) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Seguridad transversal: autenticación de nodos, controles de acceso y registro de auditoría en el HIS/RCE, el Bus y el Repositorio. La guía exige TLS 1.2+ y autenticación; ATNA estandariza cómo se audita y se autentican los nodos. | Un repositorio de auditoría y certificados en cada nodo. |
| Tiempo | **CT** (transversal) | ITI TF Rev 20.2, Final Text. https://profiles.ihe.net/ITI/TF/Volume1/ | Tiempo consistente: sincronizar los relojes de los sistemas de la red (error mediano menor de 1 segundo). Las horas de admisión, egreso y fallecimiento se comparan entre establecimientos; CT es la base. | Un servidor de tiempo (NTP) en la red. |

## Puntos de interoperabilidad

| Punto | Nombre | Datos que se mueven | Emisor → Receptor | Disparador | Perfiles IHE candidatos (repaso temprano; el paso 4 confirma o refuta) |
|---|---|---|---|---|---|
| PI-0 | Publicación del evento de admisión | Bundle de admisión: paciente, establecimiento, fecha/hora de admisión, motivo, procedencia, medio de llegada; episodio abierto (`arrived`), ID DAU | HIS/RCE del establecimiento → Bus de Interoperabilidad MINSAL | Al crear el episodio (admisión) | PIXm (identidad en el MPI), MHD (publicación del documento), NAV (notificación), ATNA, CT |
| PI-1 | Publicación del evento de alta, abandono o fallecimiento | Bundle de alta, abandono o fallecimiento (extensión): el mismo episodio actualizado (se repiten los datos de la admisión) + fecha/hora de cierre, destino o tipo de abandono o fallecimiento, diagnóstico, medicamentos, referencia al DAU | HIS/RCE del establecimiento → Bus de Interoperabilidad MINSAL | Cierre del episodio de urgencia | PIXm, MHD, XDR (push), ATNA, CT |
| PI-2 | Consulta de episodios | Búsqueda FHIR (`Encounter?patient.identifier=…&class=EMER` o por establecimiento y estado) o suscripción a los cambios de episodio; el repositorio entrega los episodios | Punto de la red receptor → Repositorio FHIR (consulta); Repositorio → receptor (episodios) | El receptor consulta o está suscrito | QEDm (consulta de datos), DSUB (suscripción), MHD (buscar documentos), ATNA, CT |
| PI-3 | Recuperación del DAU en PDF | Solicitud del DAU y DAU en PDF (descargado desde `DocumentReference.content.attachment.url`, con autenticación) | Receptor → HIS/RCE (solicitud); HIS/RCE → Receptor (PDF) | El receptor decide que necesita el detalle clínico | MHD (recuperar el documento), ATNA, CT |

Notas:

- PI-0 y PI-1 son **push** (el establecimiento envía la transacción en el momento del evento); PI-2 es **pull** (la red consulta el repositorio) con la opción de **suscripción** para enterarse del evento apenas ocurre. Eso resuelve Q5.
- PI-1 y PI-2 mueven el aviso mínimo; PI-3 mueve el documento completo. El aviso referencia el DAU, no lo copia.
- El DAU en PDF se genera siempre, en ambas ramas del desenlace (también en abandono), pero solo al cerrar el episodio.
- En la rama de abandono no hay medicamentos al alta: el aviso no lleva el dato en ese caso. En NEA, además, pueden no existir hipótesis ni PDF: el aviso lo registra como condicional.
- **La categoría C1–C5 no viaja en el aviso** (resuelve Q7, según la guía: los estados intermedios no se informan). La categorización es un dato del proceso, no de la transacción.

## Qué cambió respecto de la v3 (C14, decisión Q3)

- **Q3 = incluir como extensión del caso (C14):** la puerta de desenlace tiene una tercera salida, "Fallecimiento", que va a la tarea nueva "Cerrar DAU (fallecido)" en el carril HIS/RCE, y de ahí a "Publicar aviso mínimo". El fallecimiento es una extensión del caso: la guía v0.2.0 no lo contempla, y el valor exacto del desenlace y el contenido del evento se definen en el paso 4.

## Qué cambió respecto de la v2 (respuestas del usuario + guía v0.2.0)

- **Q1 = sí (C17 / PI-0):** el modelo adopta los tres eventos del MINSAL. Nueva tarea "Publicar evento de admisión a la red" en el carril HIS/RCE, tras crear el episodio, con message flow PI-0 al Bus. La spec cambia en consecuencia (revisión 2).
- **Q2 = sí (C20 / vía rápida C1):** nueva puerta "¿Emergencia vital?" tras el inicio. Si es C1, el paciente va directo a "Atender clínicamente", sin pasar por la admisión administrativa.
- **Q4 = después de la admisión:** segundo evento de borde NEA sobre "Categorizar paciente" (el paciente puede irse de la sala de espera antes de ser categorizado). El NEA sigue sin pasar por la atención.
- **Q6 = sí:** nueva tarea "Informar al paciente o familiares" en el carril clínico, tras la atención y antes de la puerta de desenlace.
- **Q5 (resuelto por la guía):** la plataforma genérica se reemplaza por el **Bus de Interoperabilidad MINSAL y Repositorio FHIR** (nombres exactos de la guía). PI-2 cambia de sentido: ya no es la plataforma avisando al receptor, sino el receptor consultando el repositorio (nueva rama de respuesta a consultas en el pool B) o suscribiéndose.
- **Q7 (resuelto por la guía):** la categoría no viaja en el aviso; queda solo como paso del proceso y dato del DAU.

## Preguntas resueltas

- **Q1 — tres eventos:** sí, adoptado. (Responde P1 de la spec.)
- **Q2 — vía rápida C1:** sí, modelada con la puerta "¿Emergencia vital?".
- **Q3 — fallecimiento:** sí, incluido como **extensión del caso** (no de la guía). La guía v0.2.0 no lo contempla; el valor exacto del desenlace y el contenido del evento se definen en el paso 4.
- **Q4 — dónde ocurre el NEA:** después de la admisión (antes de ser categorizado o esperando la atención). La fuga sigue siendo solo durante la atención.
- **Q5 — PI-2 push o pull:** resuelto por la guía: push al Bus (PI-0/PI-1) y pull del Repositorio (PI-2), con suscripción opcional.
- **Q6 — entrega de información:** sí, tarea explícita; si el paciente no puede recibirla, se hace a familiares.
- **Q7 — categoría en el aviso:** no, según la guía v0.2.0. (Tampoco existe un evento de Categorización en la guía publicada; el de la v0.1.1 del build continuo no llegó a la publicación.)

## Pendiente que no cambia el modelo (anotado)

- **Admisión administrativa del C1 en la vía rápida:** en el bypass, la atención empieza antes de que exista el episodio DAU. La guía exige que la admisión (con el ID DAU) exista antes del cierre, y prohíbe enviar una admisión de un episodio ya cerrado. Falta modelar la rama paralela en la que la admisión se completa durante la atención (o detallar que la admisión mínima se registra en el reanimador). Se propone modelarla en la próxima revisión si el usuario lo pide.
- C21 (dividir "Atender clínicamente" en evaluar/tratar/reevaluar) sigue anotado como pendiente: por ahora la tarea incluye evaluación, hipótesis, exámenes, procedimientos, tratamiento inicial, interconsultas y reevaluación.
- SAMU aparece como receptor, pero también es origen: el paciente puede llegar trasladado por SAMU. El dato "llegada" (recepción) lo captura.
- El destino de alta puede ser hospitalización o traslado a otro hospital; el traspaso físico no se modela, queda registrado como dato "destino".
- Los nombres de roles, tareas y puntos son los mismos de la spec (`01-use-case-spec.md`).

## Validación

Validado por el usuario el 2026-11-11 (BPMN v4 + spec revisión 3). El paso 2 queda cerrado. El paso 3 sigue con el repaso IHE temprano (esta sección, añadida al inicio del paso 3) y las entidades (`03-entities-data.md`).
