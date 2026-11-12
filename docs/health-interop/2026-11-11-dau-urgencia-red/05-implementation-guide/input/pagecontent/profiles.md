# Perfiles

Los perfiles de esta guía son perfiles propios, diseñados a partir de la especificación del caso de uso (entidades y datos de los pasos 1–3) sobre los recursos base de FHIR R4. No son transcripciones de los perfiles de otra guía: la única dependencia es el núcleo FHIR R4. Los datos que codifican (identificadores, códigos) son los que el caso de uso exige informar a la red; la guía nacional de eventos de urgencia del MINSAL (cl-urgencia v0.2.0) es la referencia de esos requisitos de datos, no la fuente de estos perfiles.

Cada perfil tiene su página con la definición formal (tabla de elementos, diferencial, snapshot, bindings de terminología, restricciones y los formatos XML/JSON/TTL). La lista completa de artefactos, con sus páginas, está en el [resumen de artefactos](artifacts.html).

## Diagrama de recursos

El diagrama (estilo ClinFHIR GraphBuilder) muestra los recursos de la guía y cómo se referencian entre sí, con el `Encounter` como centro y el `Bundle` como marco de la transacción. [Abrir el diagrama a tamaño completo](04-fhir-proposal-graph.svg).

<div style="overflow-x:auto; border:1px solid #ddd; padding:8px;">
<a href="04-fhir-proposal-graph.svg"><img src="04-fhir-proposal-graph.svg" alt="Diagrama de recursos estilo ClinFHIR GraphBuilder: Encounter como centro, referenciado por Condition, MedicationRequest y DocumentReference, con Patient, Organization y Practitioner" style="width:100%; max-width:1220px; height:auto;"/></a>
</div>

El `Encounter` es el centro: el paciente (`Patient`), el establecimiento (`Organization`) y el profesional (`Practitioner`) lo referencian; el diagnóstico (`Condition`) y los medicamentos (`MedicationRequest`) cuelgan del episodio; el documento (`DocumentReference`) referencia el episodio y apunta al PDF del DAU; el `Bundle` (transaction) enmarca los recursos de cada aviso. El PDF no es un recurso FHIR (borde punteado en el diagrama). El detalle de cada recurso y su mapeo campo a campo están en la [tabla de mapeo](mapping.html) y en la [propuesta FHIR](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/04-fhir-proposal.md).

| Perfil | Recurso base | Qué restringe |
|---|---|---|
| [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) | [Encounter](https://hl7.org/fhir/R4/encounter.html) | identifier ID DAU 1..1, status 1..1, class = EMER, subject/serviceProvider 1..1, participant ATND/DIS, period.start 1..1, reasonCode.text ≤ 200, period.end ≥ period.start, extensiones (previsión, ley previsional, clasificación, pronóstico, pertinencia, medio de llegada) |
| [`DAUEncuentroUrgenciaAlta`](StructureDefinition-dau-encuentro-urgencia-alta.html) | Encounter (padre [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html)) | status = finished, hospitalization.dischargeDisposition 1..1 (binding requerido a [`DAUDestinoAlta`](ValueSet-dau-destino-alta.html)), diagnosis 1..* con use = DD, period.end 1..1, si el destino es 01/02/04 debe haber `hospitalization.destination` |
| [`DAUEncuentroUrgenciaAbandono`](StructureDefinition-dau-encuentro-urgencia-abandono.html) | Encounter (padre [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html)) | status = finished, extensión [`tipoAbandono`](StructureDefinition-dau-tipo-abandono.html) 1..1 (1 NEA, 2 fuga), diagnosis 0..* sin use, period.end 1..1, sin dischargeDisposition ni destino |
| [`DAUPaciente`](StructureDefinition-dau-paciente.html) | [Patient](https://hl7.org/fhir/R4/patient.html) | identifier RUN 1..1 (sistema `urn:oid:2.16.840.1.113883.2.22.1.152.787300`), identifier ficha local para NN (tipo 12, use temp), gender 1..1, birthDate, deceased[x] |
| [`DAUPrestadorOrganizacional`](StructureDefinition-dau-prestador-organizacional.html) | [Organization](https://hl7.org/fhir/R4/organization.html) | identifier 1..1 (sistema CSEstablecimientoDestino, valor = código DEIS), name 1..1 |
| [`DAUPrestadorProfesional`](StructureDefinition-dau-prestador-profesional.html) | [Practitioner](https://hl7.org/fhir/R4/practitioner.html) | identifier RUN 1..1, name 1..1 |
| [`DAUDiagnosticoUrgencia`](StructureDefinition-dau-diagnostico-urgencia.html) | [Condition](https://hl7.org/fhir/R4/condition.html) | clinicalStatus 1..1, verificationStatus 1..1, code 1..1 (CIE-10 preferente, SNOMED o texto), subject 1..1, encounter 1..1 |
| [`DAUIndicacionMedicamento`](StructureDefinition-dau-indicacion-medicamento.html) | [MedicationRequest](https://hl7.org/fhir/R4/medicationrequest.html) | status = active, intent = order, medication[x] 1..1, subject 1..1, encounter 1..1, dosageInstruction |
| [`DAUDocumentoUrgencia`](StructureDefinition-dau-documento-urgencia.html) | [DocumentReference](https://hl7.org/fhir/R4/documentreference.html) | status = current, type 1..1 (LOINC 59258-4 o 34111-5), subject 1..1, context.encounter 1..1, content.attachment.url 1..1 (PDF), date 1..1 |
| [`DAUBundleAviso`](StructureDefinition-dau-bundle-aviso.html) | [Bundle](https://hl7.org/fhir/R4/bundle.html) | type = transaction, timestamp 1..1, entry 1..* (fullUrl `urn:uuid:`, request.method, request.url) |

## Terminología

La terminología de esta guía (sistemas de códigos y conjuntos de valores, locales y externos) está descrita en la página de [Terminología](terminology.html). Los artefactos locales son:

| Artefacto | Contenido |
|---|---|
| [`DAUDestinoAlta`](ValueSet-dau-destino-alta.html) ([CodeSystem](CodeSystem-dau-destino-alta.html)) | 01 Hospitalización, 02 Traslado, 03 Fallecido, 04 Derivación, 05 Domicilio, 06 Otro |
| [`DAUTipoAbandonoVS`](ValueSet-dau-tipo-abandono.html) ([CodeSystem](CodeSystem-dau-tipo-abandono.html)) | 1 NEA, 2 Fuga |
| [`DAUTipoDocumento`](ValueSet-dau-tipo-documento.html) | LOINC 59258-4 (resumen de alta), LOINC 34111-5 (nota de urgencia) |

## Extensiones

| Extensión | Dónde | Valor |
|---|---|---|
| [`DAUTipoAbandono`](StructureDefinition-dau-tipo-abandono.html) | Encounter | CodeableConcept (1 NEA, 2 fuga) |
| [`DAUPrevision`](StructureDefinition-dau-prevision.html) | Encounter | CodeableConcept (códigos NID) |
| [`DAULeyPrevisional`](StructureDefinition-dau-ley-previsional.html) | Encounter | CodeableConcept (códigos NID) |
| [`DAUClasificacionConsulta`](StructureDefinition-dau-clasificacion-consulta.html) | Encounter | CodeableConcept (01 abuso sexual, 02 violencia, 03 constatación de lesiones → episodio restringido, meta.security = R) |
| [`DAUPronosticoMedicoLegal`](StructureDefinition-dau-pronostico-medico-legal.html) | Encounter | CodeableConcept |
| [`DAUPertinencia`](StructureDefinition-dau-pertinencia.html) | Encounter | CodeableConcept |
| [`DAUMedioLlegada`](StructureDefinition-dau-medio-llegada.html) | Encounter.hospitalization | CodeableConcept |
