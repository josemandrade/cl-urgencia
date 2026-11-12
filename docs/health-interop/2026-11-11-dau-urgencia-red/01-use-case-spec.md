# Spec de caso de uso — Aviso mínimo de atención de urgencia a la red (DAU)

- **Estado:** validada por el usuario, revisión 3 (2026-11-11)
- **Fecha:** 2026-11-11
- **Carpeta de trabajo:** `docs/health-interop/2026-11-11-dau-urgencia-red/`
- **Origen:** descripción del usuario, 2026-11-11
- **Referencia normativa:** Guía de Implementación FHIR — Urgencia (Admisión, Alta y Abandono) v0.2.0 del MINSAL, publicada en https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/index.html (verificada en vivo el 2026-11-11: modelo de eventos y arquitectura). El objetivo del caso es el mismo que el de la guía; las respuestas P1–P8 y P10 vienen de esa guía. La revisión 2 adopta el modelo de tres eventos de la guía (respuesta Q1 = sí).
- **Datos:** sintéticos en todos los ejemplos. Nada de esto usa datos reales de pacientes.

## 1. Problema

Cuando una persona es atendida en la unidad de urgencia de un establecimiento, los demás puntos de la red no se enteran, o se enteran tarde, por teléfono o por el relato del propio paciente. La continuidad de la atención se rompe:

- El equipo de APS no sabe que su paciente pasó por urgencia, ni cómo terminó, ni qué se le indicó.
- La especialidad recibe al paciente sin conocer el diagnóstico de egreso de la urgencia.
- Otro hospital o el SAMU no tienen el desenlace de la atención que ya ocurrió.

El detalle clínico completo sí existe: el Documento de Atención de Urgencia (DAU) en PDF, generado por el HIS/RCE del establecimiento. Lo que falta es un **aviso mínimo, estructurado, que viaje por la red** al cierre de la atención, para que cualquier punto de la red sepa qué pasó y dónde está el detalle.

## 2. Objetivo

Definir el conjunto mínimo de datos que un establecimiento debe informar a la red cuando atiende a una persona en su unidad de urgencia, para que cualquier otro punto de la red (APS, especialidad, otro hospital, SAMU) sepa: quién fue atendido, dónde y cuándo ocurrió la atención, cómo terminó, qué tenía el paciente y qué se le indicó, y dónde está el detalle clínico completo.

## 3. Alcance

### Entra

- Tres eventos por cada episodio de atención en unidad de urgencia, uno por cada hito, publicados en el momento del evento (tiempo real o casi real, no en lotes al final del día):
  - **Admisión** — al admitir al paciente en urgencia. El episodio queda abierto (`arrived`): paciente, establecimiento, fecha y hora de admisión, motivo de consulta, procedencia, medio de llegada.
  - **Alta** — al dar el alta médica. El episodio se cierra (`finished`): fecha y hora de alta, destino, diagnóstico de egreso, medicamentos indicados, PDF.
  - **Abandono** — al constatar que el paciente se retiró sin alta (fuga o NEA). El episodio se cierra (`finished`): fecha y hora de abandono, tipo de abandono, hipótesis diagnóstica y PDF si existen.
- Todo episodio abre con una admisión y cierra con un alta o un abandono. Un solo episodio, un solo identificador: el **ID DAU** (único en el establecimiento, nunca se reutiliza, el mismo en las tres transacciones).
- **Extensión del caso (no de la guía v0.2.0):** el episodio también puede cerrar con **fallecimiento**, por decisión del usuario (Q3). La guía no contempla este desenlace. El episodio se cierra con fecha y hora de fallecimiento, el DAU se cierra como fallecido y se publica el aviso con ese desenlace. El valor exacto del desenlace y el contenido del evento (por ejemplo, el diagnóstico de causa de muerte) se definen en el paso 4, porque la guía no los define.
- El aviso contiene solo el mínimo: identificación de la persona, establecimiento y fecha/hora, desenlace, hipótesis y diagnóstico de egreso, medicamentos indicados al alta y la referencia al DAU en PDF.
- El aviso debe poder consultarse después (no es solo una notificación que se pierde).
- El transporte es el de la guía: el establecimiento **envía cada transacción al Bus de Interoperabilidad MINSAL**, que la valida y la aplica en el **Repositorio FHIR**; la red **consulta el repositorio** (búsquedas FHIR estándar) y puede **suscribirse** a los cambios de episodio para enterarse de un evento apenas ocurre.

### No entra

- El detalle clínico exhaustivo: anamnesis, examen físico, signos vitales, exámenes, procedimientos. Todo eso sigue en el DAU en PDF generado por el HIS/RCE.
- La atención hospitalizada: el caso cubre la urgencia; la hospitalización solo aparece como posible destino del alta.
- Decisiones clínicas automatizadas: el aviso informa, no decide.
- Acceso a datos reales de pacientes ni acceso a producción: la prueba y los ejemplos usan datos sintéticos.

## 4. Usuarios, roles y departamentos

| Actor | Rol | Qué hace | Qué ve | Qué decide |
|---|---|---|---|---|
| Persona atendida | Paciente | Es atendida en la urgencia | Su propia atención (según las reglas de acceso de la red) | Nada sobre el aviso |
| Equipo clínico de la Unidad de Urgencia | Médico de urgencia, enfermería, triaje | Atiende, registra, define el egreso y los medicamentos al alta | La atención completa en el HIS/RCE | El desenlace y el contenido clínico del aviso |
| HIS / RCE del establecimiento informante | Sistema de registro clínico | Genera el DAU en PDF y origina los datos del aviso | El registro clínico completo | Nada clínico; es la fuente de los datos |
| Admisión / registro de urgencia | Personal administrativo | Registra la atención (persona, lugar, fecha/hora) | Datos de identificación y de la atención | Nada clínico |
| Red de salud — APS | Equipo de salud / médico tratante | Recibe el aviso de sus pacientes y actúa (control, seguimiento) | El aviso mínimo; el DAU si lo necesita | El seguimiento en APS |
| Red de salud — Especialidad | Especialista | Recibe el aviso cuando el paciente llega derivado | El aviso mínimo; el DAU si lo necesita | La atención de especialidad |
| Red de salud — Otro hospital | Equipo receptor | Recibe el aviso en traslados o atenciones posteriores | El aviso mínimo; el DAU si lo necesita | La atención en ese hospital |
| Red de salud — SAMU | Equipo prehospitalario | Recibe el aviso cuando corresponde (traslado, atención en terreno) | El aviso mínimo; el DAU si lo necesita | La atención prehospitalaria |
| Bus de Interoperabilidad MINSAL y Repositorio FHIR | Sistema intermediario | El Bus recibe las transacciones del establecimiento, las valida (perfil y terminología), resuelve la identidad contra el MPI MINSAL y las aplica en el Repositorio FHIR; el Repositorio conserva el estado vigente de cada episodio y la referencia a su documento | Las transacciones (según reglas de acceso) | Nada clínico; su rol es validar, custodiar y entregar |
| HCC (Portal Ciudadano) | Portal del paciente | Muestra al paciente sus propias atenciones de urgencia y el documento DAU (no muestra los episodios marcados como restringidos) | Solo sus propias atenciones | Nada clínico |

## 5. El episodio y el aviso (flujo narrado, antes del BPMN)

1. La persona llega a la unidad de urgencia y se la admite: se registra la atención, se apertura el DAU (ID DAU) y se crea el episodio en el HIS.
2. Al admitirla, el establecimiento publica el **evento de admisión** al Bus (PI-0): el episodio queda abierto en el Repositorio FHIR y la red ya sabe que la persona está en urgencia.
3. Se la categoriza (C1–C5) y se la atiende clínicamente; el detalle queda en el HIS/RCE y el DAU en PDF se genera al cerrar.
4. La atención termina: alta (con destino), abandono voluntario (fuga o NEA), o fallecimiento (extensión del caso). El DAU se cierra y se genera el PDF.
5. Al cierre, el establecimiento publica el **evento de alta, de abandono o de fallecimiento** (PI-1): el mismo episodio, actualizado, queda cerrado en el Repositorio.
6. Los puntos de la red **consultan el repositorio** (PI-2) o están **suscritos** a los cambios de episodio: ven quién fue atendido, dónde y cuándo, cómo terminó, la hipótesis y el diagnóstico de egreso, y los medicamentos indicados.
7. Si necesitan el detalle clínico completo, recuperan el DAU en PDF referenciado en el aviso (PI-3).

**Nota:** los estados intermedios (categorizado, en atención médica) **no se informan** a la red. La red ve dos momentos: la admisión y el cierre. Por eso la categoría C1–C5 es un dato del proceso, no del aviso (respuesta Q7, según la guía).

## 6. Datos mínimos del aviso (por evento, según la guía v0.2.0)

Cada evento es una transacción que trae siempre paciente, establecimiento y encuentro. El encuentro se envía siempre completo: el alta y el abandono repiten todos los datos informados en la admisión.

| # | Dato | Admisión | Alta | Abandono |
|---|---|---|---|---|
| 1 | Persona atendida | Obligatorio (RUN, o pasaporte / RUN de la madre / identificador local; NN con número de ficha clínica local; la identidad se resuelve contra el MPI MINSAL) | Obligatorio | Obligatorio |
| 2 | Establecimiento y unidad | Obligatorio (código DEIS) | Obligatorio | Obligatorio |
| 3 | Fecha y hora de admisión | Obligatorio (`period.start`) | Obligatorio (se repite) | Obligatorio (se repite) |
| 4 | Fecha y hora de cierre | No se envía | Obligatorio (`period.end` = hora en que el paciente sale físicamente) | Obligatorio (`period.end` = hora en que se constata el abandono) |
| 4b | Fecha y hora de fallecimiento | — | — | Obligatorio en el cierre por fallecimiento (`period.end` = hora del fallecimiento; extensión del caso, valor del desenlace por definir en el paso 4) |
| 5 | Motivo de consulta | Si existe | Si existe | Si existe |
| 6 | Procedencia | Si existe | Si existe | Si existe |
| 7 | Medio de llegada | Si existe | Si existe | Si existe |
| 8 | Desenlace | Episodio abierto (`arrived`) | Alta (`finished` + destino) | Abandono (`finished` + tipo de abandono: fuga o NEA) |
| 8b | Desenlace por fallecimiento | — | — | Fallecimiento (`finished`; extensión del caso, no de la guía: el valor exacto del desenlace y el contenido del evento se definen en el paso 4) |
| 9 | Destino del alta | No se envía | Obligatorio: domicilio, hospitalización (01), traslado (02) o derivación (04); con destino hospitalización, traslado o derivación se informa el establecimiento de destino | No se envía |
| 10 | Hipótesis diagnóstica | — | Puede ser hipótesis o confirmado | Si existe, como hipótesis (`provisional`); puede ir solo en texto si no fue codificada |
| 11 | Diagnóstico de egreso | — | Obligatorio, al menos uno, codificado en **CIE-10** | — |
| 12 | Medicamentos indicados al alta | — | Si existe | — |
| 13 | Referencia al DAU | — | Si existe (resumen de alta, LOINC 59258-4; si el PDF aún no está listo, se reenvía el Bundle de alta completo cuando exista) | Si existe (nota de urgencia, LOINC 34111-5) |
| 14 | Identificador del episodio | **ID DAU**, con sistema `https://interoperabilidad.minsal.cl/fhir/sid/dau/[código DEIS]`; único en el establecimiento, nunca se reutiliza, el mismo en las tres transacciones | Igual | Igual |

Reglas que la guía impone y el caso respeta: un episodio cerrado debe tener fecha de cierre y destino o tipo de abandono; la fecha de cierre no puede ser anterior a la de admisión; todas las fechas llevan hora y zona horaria; los diagnósticos descartados no se informan; las consultas por abuso sexual, violencia o constatación de lesiones se marcan como restringidas; el HIS no debe enviar una admisión de un episodio ya cerrado.

## 7. Ejemplo concreto (todos los valores son sintéticos)

Paciente SYN-URG-001, 54 años, sexo femenino. El 2026-11-11, entre las 09:40 y las 12:15, es atendida en la Unidad de Urgencia del Hospital Las Acacias (establecimiento ficticio). Desenlace: **alta con destino APS**, control en 7 días. Hipótesis: dolor abdominal en estudio. Diagnóstico de egreso: gastroenteritis aguda. Medicamentos al alta: paracetamol 500 mg cada 8 horas por 3 días; sales de rehidratación oral. El DAU completo queda como PDF en el HIS del hospital, referencia DAU-2026-000123.

En términos de la guía, el episodio tiene **dos transacciones**:

- **Admisión, 09:40:** el episodio se abre (`arrived`) con la persona, el establecimiento, la fecha y hora de admisión, el motivo de consulta, la procedencia y el medio de llegada, identificado por el ID DAU DAU-2026-000123.
- **Alta, 12:15:** el mismo episodio se cierra (`finished`) repitiendo los datos de la admisión y agregando la fecha y hora de alta, el destino (APS), el diagnóstico de egreso en CIE-10, los medicamentos indicados y la referencia al PDF (resumen de alta).

Al día siguiente, el médico de APS del centro de la paciente abre el aviso, ve que estuvo en urgencia, cómo terminó y qué se le indicó, y abre el DAU en PDF para el detalle clínico.

## 8. Criterio de éxito

Un médico de APS, al día siguiente de la atención, puede saber **sin llamar por teléfono** que su paciente estuvo en urgencia, cómo terminó la atención, qué diagnóstico se dio y qué medicamentos se indicaron, y puede abrir el DAU en PDF cuando necesita el detalle.

## 9. Sugerencias del brainstorming incorporadas

- El aviso mínimo es un **aviso**, no el registro clínico: separa "qué pasó" del detalle.
- El DAU en PDF se **referencia**, no se copia: el detalle sigue viviendo en el HIS/RCE del establecimiento.
- **Tres eventos, no uno:** cada hito (admisión, alta, abandono) es una transacción que actualiza el mismo episodio, identificado por el ID DAU.
- El **destino del alta como dato estructurado**: sirve para enrutar (si el destino es APS, ese APS es el receptor principal del aviso).
- El aviso debe poder **consultarse después**, no solo notificarse en el momento: la red consulta el Repositorio FHIR o se suscribe a los cambios de episodio.
- El envío es **en el momento del evento** (tiempo real o casi real), no en lotes al final del día: la continuidad depende de que la red se entere mientras el paciente está en urgencia o recién egresado.

## 10. Preguntas abiertas (resueltas por la guía v0.2.0, salvo P9)

- **P1 — ¿Cuándo se publica el aviso?** Resuelto: tres eventos, uno por hito, publicados en el momento del evento (admisión al admitir, alta al dar el alta, abandono al constatarlo).
- **P2 — ¿Cómo viaja por la red?** Resuelto: hay un hub central: el establecimiento envía cada transacción (push) al **Bus de Interoperabilidad MINSAL**, que la valida y la aplica en el **Repositorio FHIR**; la red consulta el repositorio (pull) o se suscribe a los cambios de episodio.
- **P3 — ¿Cómo se identifica a la persona entre establecimientos?** Resuelto: RUN (o pasaporte, RUN de la madre, identificador local; NN con número de ficha clínica local). La identidad se resuelve contra el **MPI MINSAL**: si no se encuentra, se crea; si es duplicada o contradictoria, se rechaza y va a conciliación.
- **P4 — Destino del alta: ¿qué valores admite?** Resuelto: domicilio, hospitalización (01), traslado (02) o derivación (04). Con destino hospitalización, traslado o derivación se informa el establecimiento de destino concreto.
- **P5 — Fuga vs NEA: ¿cuál es la diferencia operativa?** Resuelto: ambos son tipos de abandono. NEA = se va antes de ser atendido (no espera atención); fuga = se retira tras haber sido atendido. El tipo de abandono va en el evento de abandono.
- **P6 — Medicamentos al alta: ¿qué campos lleva cada uno?** Parcialmente resuelto: van solo en el alta (si existen), como indicaciones (`MedicationRequest`). Los campos de cada indicación se definen en los pasos 3 y 4.
- **P7 — ¿Quién puede ver el aviso?** Resuelto: los equipos de la red que continúan la atención (APS, especialidad, otros hospitales, SAMU) consultan el repositorio; el paciente ve sus propias atenciones en HCC; los episodios restringidos solo los ven los equipos autorizados.
- **P8 — ¿Qué habilita compartir el aviso?** Parcialmente resuelto: el acceso se rige por las políticas de acceso de la red y el consentimiento del paciente cuando corresponda; el transporte va cifrado y la URL del PDF exige autenticación. El detalle normativo queda para los pasos 3–5.
- **P9 — ¿Qué pasa si la persona fallece en urgencia?** **Resuelto: se incluye como extensión del caso.** El usuario decidió incluir el fallecimiento como tercer desenlace (Q3), aunque la guía v0.2.0 no lo contempla. El episodio se cierra como fallecido y se publica el aviso con ese desenlace. El valor exacto del desenlace y el contenido del evento (por ejemplo, el diagnóstico de causa de muerte) se definen en el paso 4.
- **P10 — ¿Qué identifica al aviso mismo?** Resuelto: el **ID DAU** (`https://interoperabilidad.minsal.cl/fhir/sid/dau/[código DEIS]`), único en el establecimiento, nunca se reutiliza, el mismo en las tres transacciones.

## 11. Fuera de alcance (confirmado)

- El detalle clínico completo, que sigue en el DAU en PDF.
- La atención hospitalizada como caso propio.
- La decisión clínica: el aviso informa, no recomienda conducta.
- Datos reales de pacientes y acceso a sistemas de producción.
