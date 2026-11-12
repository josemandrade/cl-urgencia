// Hipótesis y diagnóstico de egreso.
// Perfil propio de esta guía. Diseñado a partir de la especificación del caso
// de uso (entidades y datos de los pasos 1–3) sobre el recurso base Condition
// de FHIR R4.

Profile: DAUDiagnosticoUrgencia
Parent: Condition
Id: dau-diagnostico-urgencia
Title: "Diagnóstico de urgencia (DAU)"
Description: "Hipótesis (verificationStatus = provisional) o diagnóstico de egreso (verificationStatus = confirmed, use = DD) del episodio de urgencia. En el alta, el diagnóstico de egreso debe ser CIE-10. Los diagnósticos descartados no se informan."
* clinicalStatus 1..1
* verificationStatus 1..1
* verificationStatus ^short = "provisional (hipótesis) o confirmed (diagnóstico de egreso)"
* code 1..1
* code ^short = "CIE-10 (preferente, http://hl7.org/fhir/sid/icd-10), SNOMED CT (http://snomed.info/sct) o solo texto. TAPSA no se acepta."
* subject 1..1
* subject only Reference(DAUPaciente)
* encounter 1..1
* encounter only Reference(DAUEncuentroUrgencia)
* recordedDate 0..1
