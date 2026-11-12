# Tabla de mapeo CMBD → FHIR — Aviso mínimo de atención de urgencia a la red (DAU)

- **Estado:** propuesta para validación (paso 4, `mapping-to-fhir`)
- **Fecha:** 2026-11-11
- **Fuente:** Conjunto Mínimo Básico de Datos (CMBD) de Urgencia del DEIS, según el mapeo de la Guía de Implementación FHIR — Urgencia (Admisión, Alta y Abandono) v0.2.0 (https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/mapeo-cmbd.html), verificado en vivo el 2026-11-11.
- **Destino:** FHIR R4, perfiles de la guía cl-urgencia v0.2.0 (ver `04-fhir-proposal.md`).
- **Evento** indica la primera transacción en que se informa el dato; las transacciones siguientes lo repiten si sigue vigente (el `Encounter` se envía siempre completo).

## Convenciones de formato

- Fecha y hora del CMBD (`DDMMAAAA` + `HH:MM`) se envían como un solo `dateTime` ISO 8601 con zona horaria: `2026-09-09T10:00:00-03:00`. Una fecha sin hora se rechaza (invariante `urg-enc-5`).
- Los códigos del CMBD se envían tal cual, con el `system` del CodeSystem correspondiente.
- Los códigos del NID no llevan cero a la izquierda: `01 FONASA` del CMBD se envía como `1`. El valor original del CMBD queda en el log de mapeo.
- Paciente, profesional y establecimiento usan directamente los perfiles del NID 0.4.6; los códigos de previsión, tramo FONASA, leyes previsionales y título profesional también son los del NID.

## Mapeo campo a campo

| Campo CMBD | Formato fuente | Ruta FHIR | Regla de transformación | Si falta / ambiguo / inválido |
|---|---|---|---|---|
| COD SS | Código de Servicio de Salud | `Organization.partOf` (referencia al Servicio de Salud) | Referencia al `Organization` del Servicio de Salud | Si falta: se omite (no es obligatorio) |
| COD ESTAB | Código DEIS del establecimiento | `Organization.identifier.value` (`system = https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino`) | Se envía tal cual, con su `system` | Si falta: **se rechaza la transacción** (el establecimiento es obligatorio) |
| ID DAU | Identificador del DAU en el HIS/RCE | `Encounter.identifier.value`, con `system = https://interoperabilidad.minsal.cl/fhir/sid/dau/[COD ESTAB]` | Se envía tal cual; el `system` se construye con el COD ESTAB | Si falta: **se rechaza** (es la llave del `PUT` condicional y debe ser único y no reutilizarse nunca) |
| ID ATENCION | Identificador de la atención en el HIS/RCE | `Encounter.identifier` (segundo identificador) | Se envía solo si difiere del ID DAU | Si falta o es igual al ID DAU: se omite |
| ID_BD_PERSONAS | Identificador MPI | `Patient.identifier` (system MPI) | **No lo envía el HIS.** Lo agrega el Bus al resolver la identidad contra el MPI | Si el MPI no resuelve la identidad: la transacción se rechaza (`422`) y el HIS/RCE corrige y reenvía |
| ID PACIENTE | Número de ficha clínica local | `Patient.identifier` con tipo `12` (Número de ficha clínica sistema local) | Se envía con tipo `12` y `use = temp` (NN) | Si falta y no hay RUN: se usa otro identificador disponible (pasaporte, RUN madre) o NN |
| RUN + DV | RUN con dígito verificador | `Patient.identifier.value = RUN-DV`, tipo `01` RUN | Se envía como `RUN-DV`, `system = urn:oid:2.16.840.1.113883.2.22.1.152.787300` | Si falta: se usan los alternativos (ver TIPO_IDENTIFICACION). Si el dígito verificador es inválido: **se rechaza la transacción** |
| TIPO_IDENTIFICACION | Código 1–4, 9 | `Patient.identifier.type` (CL-Core `CSTipoIdentificador`) | Equivalencia: `1 RUN → 01 RUN`, `2 Pasaporte → 05 PPN`, `3 RUN materno → 03 RUN Madre`, `4 Sin RUN (incluye NN) → 12 Número de ficha clínica sistema local`, `9 Otro → 14 Otro` | Si el código no está en la tabla: **se rechaza** (no se adivina el tipo) |
| FECHA NACIMIENTO | Fecha | `Patient.birthDate` | Se convierte a ISO 8601 (`YYYY-MM-DD`) | Si falta (NN): ausente, con la extensión `data-absent-reason = unknown` |
| SEXO | Código 01, 02, 03, 99 | `Patient.extension[SexoBiologico]` (CL-Core `CSSexoListadoDeis`) y `Patient.gender` | Equivalencia a `gender`: `01 → male`, `02 → female`, `03 → other`, `99 → unknown` | Si el código no está en la tabla: **se rechaza** |
| TELÉFONO CONTACTO | Teléfono | `Patient.telecom` (`system = phone`) | Se envía tal cual | Si falta: se omite (el NID lo exige, pero el CMBD no siempre lo trae; se registra en el log) |
| PREVISIÓN | Código NID | `Encounter.extension[prevision].extension[prevision]` (NID `CSPrevision`) | Se envía el código NID **sin cero a la izquierda** (`01 FONASA → 1`); el valor original queda en el log | Si falta: se omite (la previsión es un dato CMBD sin elemento FHIR propio; va en la extensión) |
| CLASIFICACIÓN BENEFICIARIO FONASA | Código NID | `Encounter.extension[prevision].extension[tramoFonasa]` (NID `CSTramosFONASA`) | Se envía el código NID sin cero a la izquierda | Si falta: se omite |
| LEYES PREVISIONALES | Códigos NID (varios) | `Encounter.extension[leyPrevisional]` (0..*, NID `CSLeyPrevisionales`) | Una extensión por ley | Si no hay: se omite |
| FECHA_ADM + HORA_ADM | `DDMMAAAA` + `HH:MM` | `Encounter.period.start` | Se combinan en un solo `dateTime` ISO 8601 con zona horaria | Si falta o no tiene hora: **se rechaza** (`urg-enc-5`) |
| PROCEDENCIA DEL PACIENTE | Código | `Encounter.hospitalization.admitSource` (ValueSet "Procedencia del paciente", requerido) | Se envía tal cual, con su `system` | Si falta: se omite ("si existe"). Si el código no está en el ValueSet: **se rechaza** |
| UNIDAD DE ATENCIÓN | Código | `Encounter.serviceType` (ValueSet "Unidad de atención de urgencia", requerido) | Se envía tal cual, con su `system` | Si falta: se omite. Si el código no está en el ValueSet: **se rechaza** |
| MOT_CONSULTA | Texto libre | `Encounter.reasonCode.text` | Se envía tal cual, hasta 200 caracteres | Si falta: se omite ("si existe"). Si supera 200 caracteres: **se rechaza** |
| CLASIFICACIÓN DE LA CONSULTA | Código 01, 02, 03 | `Encounter.extension[clasificacionConsulta]` | Se envía tal cual. Con 01, 02 o 03 el episodio se marca como restringido (`meta.security = R`) | Si falta: se omite. Si el código no está en el ValueSet: **se rechaza** |
| LLEGADA | Código | `Encounter.hospitalization.extension[medioLlegada]` (ValueSet "Medio de llegada", requerido) | Se envía tal cual, con su `system` | Si falta: se omite ("si existe"). Si el código no está en el ValueSet: **se rechaza** |
| FECHA_ATENCION + HORA_ATENCION | `DDMMAAAA` + `HH:MM` | `Encounter.participant` con `type = ATND` (médico tratante), `period.start` | Se combinan en un solo `dateTime` ISO 8601 con zona horaria | Si falta: se omite (el paciente puede no haber sido atendido, como en NEA) |
| HIPOTESIS_DIAG | Texto y/o código | `Condition` con `verificationStatus = provisional`, referenciada en `Encounter.diagnosis` **sin** `use` | Solo en el abandono; en el alta se informa el diagnóstico de egreso | Si no existe (NEA): se omite y el aviso lo registra como condicional |
| COD_DIAG + TIPO_COD_DIAG (hipótesis) | Código + tipo 01–04 | `Condition.code.coding` (el `system` indica el tipo de codificación) | Equivalencia: `01 CIE-10 → http://hl7.org/fhir/sid/icd-10`, `02 TAPSA → no se acepta`, `03 SNOMED → http://snomed.info/sct`, `04 Otros → solo Condition.code.text` | Opcional en la hipótesis. TAPSA: **se rechaza** (no se acepta mientras el DEIS no publique su sistema de códigos). `04 Otros`: solo texto, no válido en el alta |
| INDICACIÓN DE FÁRMACOS | Texto | Un `MedicationRequest` por fármaco: `medicationCodeableConcept.text` + `dosageInstruction.text` | Un recurso por fármaco | Si no hay: se omite (en abandono no hay). Si el texto está vacío: **se rechaza** ese recurso |
| ID RECETA | Identificador de la receta | `MedicationRequest.groupIdentifier` | Se envía tal cual | Si falta: se omite |
| SOLIC_MEDIOS_DIAG / DESCRIP_MEDIOS_DIAG | Texto | No se envía estructurado; queda en el PDF | No se mapea | No aplica (los exámenes tienen sus propias guías) |
| FECHA_ALTA + HORA_ALTA | `DDMMAAAA` + `HH:MM` | `Encounter.period.end` | Salida física de urgencia (si se hospitaliza, cuando deja urgencia hacia la cama). En el fallecimiento: hora del fallecimiento | Si falta en un episodio `finished`: **se rechaza** (`urg-enc-1`). Si es anterior a `period.start`: **se rechaza** (`urg-enc-3`) |
| DIAG_FINAL | Texto | `Condition.code.text`, referenciada en `Encounter.diagnosis` con `use = DD` | Se envía el texto del diagnóstico final | Si falta en el alta: **se rechaza** (el alta exige al menos un diagnóstico) |
| TIPO_DIAG | Código 01, 02, 03 | `Condition.verificationStatus` | Equivalencia: `01 → provisional`, `02 → confirmed`. `03` (descartado) **no se informa** | Si es `03` (descartado): se omite y se registra en el log. Si el código no está en la tabla: **se rechaza** |
| COD_DIAG + TIPO_COD_DIAG (egreso) | Código + tipo | `Condition.code.coding` con **CIE-10 obligatorio** (`http://hl7.org/fhir/sid/icd-10`) | Se exige CIE-10 en el alta (`urg-alta-cie10`) | Si no es CIE-10: **se rechaza**. TAPSA: **se rechaza** |
| CONDICIÓN AL CIERRE | Deducido | Se deduce del destino | `03 Fallecido → fallecido`; otro → vivo. Es el campo que reconoce el fallecimiento: un alta con `dischargeDisposition = 03 Fallecido` es un fallecimiento (ver `04-fhir-proposal.md`, sección 5) | No es un campo que se envíe; se deduce. Si el destino es `03`, el receptor debe interpretarlo como fallecido |
| PRONÓSTICO MÉDICO LEGAL | Código | `Encounter.extension[pronosticoMedicoLegal]` (ValueSet "Pronóstico médico-legal", requerido) | Se envía tal cual, con su `system` | Si falta: se omite. Si el código no está en el ValueSet: **se rechaza** |
| DESTINO_ALTA | Código | `Encounter.hospitalization.dischargeDisposition` (ValueSet "Destino al alta de urgencia", requerido) | Códigos: `01` Hospitalización, `02` Traslado, **`03` Fallecido**, `04` Derivación, `05` Domicilio, `06` Otro (`system = https://interoperabilidad.minsal.cl/fhir/ig/urgencia-eventos/CodeSystem/destino-alta`). Con 01, 02 o 04 se informa el establecimiento de destino | Si falta en el alta: **se rechaza** (`urg-enc-2`). Si el código no está en el ValueSet: **se rechaza** |
| GES | Código | `Condition.extension[ges]` | Se envía tal cual | Si falta: se omite |
| PERTINENCIA | Boolean | `Encounter.extension[pertinencia]` | Se envía tal cual | Si falta: se omite |
| ID PROFESIONAL ALTA | Identificador del profesional | `Encounter.participant.individual` → `Practitioner` (`participant.type = DIS`) | Se referencia el `Practitioner` del mismo Bundle | Si falta: se omite (opcional) |
| RUN + DV (profesional) | RUN con dígito verificador | `Practitioner.identifier[run]` | Se envía como `RUN-DV` | Si el dígito verificador es inválido: **se rechaza** |
| TÍTULO PROFESIONAL | Código NID | `Practitioner.qualification[TituloProfesional].code` (NID `CSTituloProfesional`) | Se envía el código NID | Si falta: se omite |
| ESPECIALIDAD MÉDICA | Código NID | `Practitioner.qualification[EspecialidadMedica].code` (NID `CSEspecialidadMed`) | Se envía el código NID | Si falta: se omite |
| ABANDONO | Código 1, 2 | Bundle de abandono + `Encounter.hospitalization.dischargeDisposition` (ValueSet "Tipo de abandono", requerido) | Equivalencia: `1 → NEA` (abandono antes de la atención médica), `2 → fuga` (abandono durante la atención médica). `period.end` = fecha y hora en que se constata el abandono | Si el código no está en el ValueSet: **se rechaza** |

## Reglas generales de datos desordenados

- **Falta un valor obligatorio:** la transacción se rechaza con `OperationOutcome`; no se inventa ni se completa el dato. Un valor "si existe" ausente simplemente se omite.
- **Múltiples valores:** varios diagnósticos → un `Condition` por diagnóstico, `rank = 1` para el principal. Varios fármacos → un `MedicationRequest` por fármaco. Varios identificadores → el RUN es el principal; los demás se envían como identificadores adicionales.
- **Valores en conflicto:** un diagnóstico marcado a la vez provisional y confirmado → **se rechaza** (no se adivina). `period.end` anterior a `period.start` → **se rechaza** (`urg-enc-3`). Una admisión de un episodio ya cerrado → **se rechaza** (el `PUT` lo reabriría).
- **Valores fuera de rango:** una fecha sin hora o sin zona horaria → **se rechaza** (`urg-enc-5`). Un código fuera del ValueSet requerido → **se rechaza**. Un código TAPSA → **se rechaza** (no aceptado mientras el DEIS no publique su sistema).
- **Pérdida de información:** cuando la transformación pierde información (por ejemplo, los códigos NID sin el cero a la izquierda, o el texto original del motivo), el valor original del CMBD queda en el log de mapeo. Nunca se corrige en silencio un valor que cambiaría el significado clínico: se rechaza.

## Códigos sin mapear

| Código / campo fuente | Valor fuente | Razón por la que no se mapea |
|---|---|---|
| TIPO_COD_DIAG `02` TAPSA | Código TAPSA | No se acepta mientras el DEIS no publique su sistema de códigos |
| TIPO_COD_DIAG `04` Otros (en el alta) | Código de otro sistema | Solo `Condition.code.text`; no válido en el alta (el alta exige CIE-10) |
| TIPO_DIAG `03` (descartado) | Diagnóstico descartado | Los diagnósticos descartados no se informan |
| CATEGORIZACIÓN ESI, PRIMERA_CATE, ULTIMA_CATE, fechas, horas, profesionales y número de categorizaciones | Campos de categorización | Fuera del alcance de esta versión, por decisión de la versión 0.1.2 de la guía; la categoría C1–C5 no viaja en el aviso |
| SOLIC_MEDIOS_DIAG / DESCRIP_MEDIOS_DIAG | Solicitudes y resultados de exámenes | No se envían estructurados; quedan en el PDF (tienen sus propias guías) |
| Signos vitales, anamnesis, examen físico, evolución, procedimientos y medicamentos administrados | Datos clínicos del episodio | No se envían como recursos estructurados; siguen en el PDF |

## Validación

Pendiente: la tabla de mapeo se presenta al usuario para validación junto con la propuesta (`04-fhir-proposal.md`). Sin validación no se avanza a la Guía de Implementación con SUSHI (paso 5).
