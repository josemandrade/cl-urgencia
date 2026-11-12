# Diagrama de recursos

El diagrama de recursos de la guía (estilo ClinFHIR GraphBuilder, de la [propuesta FHIR](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/04-fhir-proposal.md)) muestra los recursos y cómo se referencian entre sí, con el `Encounter` como centro y el `Bundle` como marco de la transacción. [Abrir el diagrama a tamaño completo](04-fhir-proposal-graph.svg).

<div style="overflow-x:auto; border:1px solid #ddd; padding:8px;">
<a href="04-fhir-proposal-graph.svg"><img src="04-fhir-proposal-graph.svg" alt="Diagrama de recursos estilo ClinFHIR GraphBuilder: Encounter como centro, referenciado por Condition, MedicationRequest y DocumentReference, con Patient, Organization y Practitioner" style="width:100%; max-width:1220px; height:auto;"/></a>
</div>

## Cómo leerlo

- Las flechas son **referencias FHIR**; la etiqueta de cada flecha es el elemento que lleva la referencia (por ejemplo, `subject`, `encounter`, `diagnosis.condition`).
- El `Encounter` es el centro: el paciente (`Patient`), el establecimiento (`Organization`) y el profesional (`Practitioner`) lo referencian; el diagnóstico (`Condition`) y los medicamentos (`MedicationRequest`) cuelgan del episodio; el documento (`DocumentReference`) referencia el episodio y apunta al PDF del DAU.
- El `Bundle` (transaction, borde punteado) es el sobre que lleva los recursos de cada aviso: una transacción por evento (admisión, alta, abandono).
- El **PDF del DAU no es un recurso FHIR** (borde punteado): es el documento clínico completo, referenciado desde el `DocumentReference` por `content.attachment.url`.

## Los recursos y sus referencias

| Recurso | Perfil | Referencia a | Por qué |
|---|---|---|---|
| [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) | Encounter | [`DAUPaciente`](StructureDefinition-dau-paciente.html) (`subject`), [`DAUPrestadorOrganizacional`](StructureDefinition-dau-prestador-organizacional.html) (`serviceProvider`), [`DAUPrestadorProfesional`](StructureDefinition-dau-prestador-profesional.html) (`participant.individual`) | El episodio es el centro; quién fue atendido, dónde y por quién |
| [`DAUDiagnosticoUrgencia`](StructureDefinition-dau-diagnostico-urgencia.html) | Condition | [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) (`encounter`), [`DAUPaciente`](StructureDefinition-dau-paciente.html) (`subject`) | La hipótesis y el diagnóstico de egreso de un episodio |
| [`DAUIndicacionMedicamento`](StructureDefinition-dau-indicacion-medicamento.html) | MedicationRequest | [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) (`encounter`), [`DAUPaciente`](StructureDefinition-dau-paciente.html) (`subject`) | Los medicamentos al alta de un episodio |
| [`DAUDocumentoUrgencia`](StructureDefinition-dau-documento-urgencia.html) | DocumentReference | [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) (`context.encounter`), [`DAUPaciente`](StructureDefinition-dau-paciente.html) (`subject`) | El resumen de alta o la nota de urgencia, y el PDF del DAU |
| [`DAUBundleAviso`](StructureDefinition-dau-bundle-aviso.html) | Bundle | Todos los recursos del aviso (por `fullUrl` `urn:uuid:`) | Una transacción por evento, sobre un solo `Encounter` |

El detalle de cada perfil está en [Perfiles](profiles.html) y el mapeo campo a campo en [Mapeo de datos](mapping.html).
