# Perfiles

Los perfiles de esta guía son transcripciones locales de los perfiles de la Guía de interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0), con nombres propios (`DAU...`) para no reclamar ser los perfiles del MINSAL. La única dependencia es el núcleo FHIR R4; no se depende del paquete de la guía del MINSAL ni de CL-Core.

| Perfil | Recurso base | Qué restringe |
|---|---|---|
| `DAUEncuentroUrgencia` | Encounter | identifier ID DAU 1..1, status 1..1, class = EMER, subject/serviceProvider 1..1, participant ATND/DIS, period.start 1..1, reasonCode.text ≤ 200, period.end ≥ period.start, extensiones (previsión, ley previsional, clasificación, pronóstico, pertinencia, medio de llegada) |
| `DAUEncuentroUrgenciaAlta` | Encounter (padre `DAUEncuentroUrgencia`) | status = finished, hospitalization.dischargeDisposition 1..1 (binding requerido a `DAUDestinoAlta`), diagnosis 1..* con use = DD, period.end 1..1, si el destino es 01/02/04 debe haber `hospitalization.destination` |
| `DAUEncuentroUrgenciaAbandono` | Encounter (padre `DAUEncuentroUrgencia`) | status = finished, extensión `tipoAbandono` 1..1 (1 NEA, 2 fuga), diagnosis 0..* sin use, period.end 1..1, sin dischargeDisposition ni destino |
| `DAUPaciente` | Patient | identifier RUN 1..1 (sistema `urn:oid:2.16.840.1.113883.2.22.1.152.787300`), identifier ficha local para NN (tipo 12, use temp), gender 1..1, birthDate, deceased[x] |
| `DAUPrestadorOrganizacional` | Organization | identifier 1..1 (sistema CSEstablecimientoDestino, valor = código DEIS), name 1..1 |
| `DAUPrestadorProfesional` | Practitioner | identifier RUN 1..1, name 1..1 |
| `DAUDiagnosticoUrgencia` | Condition | clinicalStatus 1..1, verificationStatus 1..1, code 1..1 (CIE-10 preferente, SNOMED o texto), subject 1..1, encounter 1..1 |
| `DAUIndicacionMedicamento` | MedicationRequest | status = active, intent = order, medication[x] 1..1, subject 1..1, encounter 1..1, dosageInstruction |
| `DAUDocumentoUrgencia` | DocumentReference | status = current, type 1..1 (LOINC 59258-4 o 34111-5), subject 1..1, context.encounter 1..1, content.attachment.url 1..1 (PDF), date 1..1 |
| `DAUBundleAviso` | Bundle | type = transaction, timestamp 1..1, entry 1..* (fullUrl `urn:uuid:`, request.method, request.url) |

## Terminología

| Artefacto | Contenido |
|---|---|
| `DAUDestinoAlta` (CodeSystem + ValueSet) | 01 Hospitalización, 02 Traslado, 03 Fallecido, 04 Derivación, 05 Domicilio, 06 Otro |
| `DAUTipoAbandonoVS` (ValueSet) | 1 NEA, 2 Fuga |
| `DAUTipoDocumento` (ValueSet) | LOINC 59258-4 (resumen de alta), LOINC 34111-5 (nota de urgencia) |

## Extensiones

| Extensión | Dónde | Valor |
|---|---|---|
| `DAUTipoAbandono` | Encounter | CodeableConcept (1 NEA, 2 fuga) |
| `DAUPrevision` | Encounter | CodeableConcept (códigos NID) |
| `DAULeyPrevisional` | Encounter | CodeableConcept (códigos NID) |
| `DAUClasificacionConsulta` | Encounter | CodeableConcept (01 abuso sexual, 02 violencia, 03 constatación de lesiones → episodio restringido, meta.security = R) |
| `DAUPronosticoMedicoLegal` | Encounter | CodeableConcept |
| `DAUPertinencia` | Encounter | CodeableConcept |
| `DAUMedioLlegada` | Encounter.hospitalization | CodeableConcept |
