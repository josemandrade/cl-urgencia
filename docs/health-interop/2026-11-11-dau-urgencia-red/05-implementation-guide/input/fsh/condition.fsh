// Hipótesis y diagnóstico de egreso.
// Fuente: perfil Diagnóstico de urgencia (sobre CL-Core CoreDiagnosticoCl) de
// la Guía de interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

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
