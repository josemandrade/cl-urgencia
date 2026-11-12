// Medicamento indicado al alta.
// Fuente: perfil Indicación de medicamento de la Guía de interoperabilidad de
// eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

Profile: DAUIndicacionMedicamento
Parent: MedicationRequest
Id: dau-indicacion-medicamento
Title: "Indicación de medicamento (DAU)"
Description: "Medicamento indicado al alta de la urgencia. Solo se informa si existe al menos un medicamento al alta."
* status 1..1
* status = #active
* intent 1..1
* intent = #order
* medication[x] 1..1
* medication[x] only CodeableConcept
* subject 1..1
* subject only Reference(DAUPaciente)
* encounter 1..1
* encounter only Reference(DAUEncuentroUrgencia)
* dosageInstruction 0..*
