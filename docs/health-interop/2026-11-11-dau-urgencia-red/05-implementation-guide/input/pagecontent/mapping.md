# Mapeo de datos a recursos

Mapeo campo a campo del CMBD y de los datos del episodio a FHIR. La fuente completa es la [tabla de mapeo](../04-mapping-table.md) validada en el paso 4. Las fechas CMBD (`DDMMAAAA` + `HH:MM`) se convierten a un solo dateTime ISO 8601 con zona horaria. Los códigos NID van sin cero a la izquierda (`01 FONASA` → `1`).

| Campo origen | Recurso y ruta FHIR | Regla | Si falta o es ambiguo |
|---|---|---|---|
| ID_DAU | `Encounter.identifier` (system `.../sid/dau/[código DEIS]`, value = ID DAU) | Único por establecimiento, nunca reutilizado; clave del PUT condicional | Sin ID DAU no se puede publicar el aviso; el HIS debe asignarlo |
| FECHA_INGRESO + HORA_INGRESO | `Encounter.period.start` | ISO 8601 con hora y zona horaria | Sin fecha de admisión no se puede publicar la admisión |
| FECHA_EGRESO + HORA_EGRESO | `Encounter.period.end` | Debe ser ≥ period.start (invariante `dau-enc-period`) | En admisión no existe; en alta/abandono es obligatorio |
| RUN paciente | `Patient.identifier` (system `urn:oid:2.16.840.1.113883.2.22.1.152.787300`) | Sin puntos ni guión, con DV | RUN con DV inválido: el Bus rechaza; el HIS corrige y reenvía |
| TIPO_IDENTIFICACION | `Patient.identifier.type` | 1→01 RUN, 2→05 PPN, 3→03 RUN Madre, 4→12 ficha local, 9→14 Otro | Sin tipo, se usa el RUN si existe; en NN, ficha local (tipo 12, use temp) |
| NOMBRE / APELLIDOS | `Patient.name` | family + given | En NN, ausente con data-absent-reason = unknown |
| SEXO | `Patient.gender` | 01 male, 02 female, 03 other, 99 unknown | 99 unknown si no se conoce |
| FECHA_NACIMIENTO | `Patient.birthDate` | Fecha ISO | En NN, ausente con data-absent-reason = unknown |
| CÓDIGO DEIS establecimiento | `Organization.identifier` (system CSEstablecimientoDestino) | Código DEIS del establecimiento emisor o destino | Sin DEIS no se puede identificar el establecimiento |
| RUN profesional | `Practitioner.identifier` (mismo sistema RUN) | Médico tratante (ATND) o quien da el alta (DIS) | Si no hay profesional identificado, el participant es opcional en la admisión |
| MOTIVO_CONSULTA | `Encounter.reasonCode.text` | Texto libre, máximo 200 caracteres (invariante `dau-enc-reason`) | Si excede 200 caracteres, se trunca en el origen o se rechaza |
| DESTINO_ALTA | `Encounter.hospitalization.dischargeDisposition` | 01 Hospitalización, 02 Traslado, 03 Fallecido, 04 Derivación, 05 Domicilio, 06 Otro | Sin destino no se puede cerrar el alta |
| DESTINO (establecimiento) | `Encounter.hospitalization.destination` | Obligatorio si el destino es 01/02/04 (invariante `dau-alta-destino`); ausente en 03/05/06 | Si el destino es 01/02/04 y falta el establecimiento, el alta se rechaza |
| CONDICIÓN AL CIERRE | `Encounter.hospitalization.dischargeDisposition` | 03 → fallecido (el fallecimiento es un alta, no un Bundle nuevo) | — |
| TIPO_ABANDONO | `Encounter.extension[tipoAbandono]` | 1 NEA (antes de la atención médica), 2 fuga (durante la atención) | Sin tipo de abandono no se puede publicar el abandono |
| TIPO_COD_DIAG | `Condition.code` | 01 CIE-10, 02 TAPSA (no aceptado), 03 SNOMED, 04 solo texto | TAPSA se rechaza; 04 solo texto no es válido en el alta |
| TIPO_DIAG | `Condition.verificationStatus` | 01 provisional (hipótesis), 02 confirmed (diagnóstico de egreso), 03 descartado (no se informa) | Sin verificación, se usa provisional en la hipótesis |
| DIAGNÓSTICO | `Condition.code` + `Encounter.diagnosis.use = DD` (en el alta) | En el alta, el diagnóstico de egreso debe ser CIE-10 | Sin diagnóstico de egreso no se puede cerrar el alta |
| MEDICAMENTOS | `MedicationRequest` | Solo si existe al menos un medicamento al alta | Sin medicamentos, no se envía MedicationRequest |
| DAU (PDF) | `DocumentReference.content.attachment.url` | LOINC 59258-4 (resumen de alta) o 34111-5 (nota de urgencia); contentType application/pdf | Si el PDF no está listo, se reenvía el Bundle de alta completo cuando exista |
| ID_BD_PERSONAS | `Patient.identifier` (identificador MPI) | Lo agrega el Bus, no el HIS | — |
| Categorización (C1–C5) | — | Fuera de alcance: la categoría no viaja en el aviso | — |
