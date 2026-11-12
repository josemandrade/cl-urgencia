// Extensiones.
// Fuente: la Guía de interoperabilidad de eventos de urgencia del MINSAL
// (cl-urgencia v0.2.0). Los códigos de previsión, ley previsional,
// clasificación de consulta, pronóstico médico legal, pertinencia y medio de
// llegada son los del NID / CL-Core; se documentan en la descripción y no se
// atan a un ValueSet local para que la guía se compile sin dependencias externas.

// Tipo de abandono: 1 NEA (antes de la atención médica), 2 fuga (durante la atención).
CodeSystem: DAUTipoAbandonoCS
Id: dau-tipo-abandono
Title: "Tipo de abandono"
Description: "Códigos de tipo de abandono voluntario de la atención de urgencia."
* #1 "NEA" "No efectuó atención: el paciente se fue antes de la atención médica"
* #2 "Fuga" "Fuga: el paciente se fue durante la atención"

ValueSet: DAUTipoAbandonoVS
Id: dau-tipo-abandono
Title: "Tipo de abandono"
Description: "Tipos de abandono voluntario de la atención de urgencia."
* include codes from system DAUTipoAbandonoCS

Extension: DAUTipoAbandono
Id: dau-tipo-abandono
Title: "Tipo de abandono"
Description: "Tipo de abandono voluntario: 1 NEA (antes de la atención médica), 2 fuga (durante la atención)."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept
* valueCodeableConcept from DAUTipoAbandonoVS (required)

Extension: DAUPrevision
Id: dau-prevision
Title: "Previsión"
Description: "Previsión del paciente (FONASA, ISAPRE, etc.). Los códigos son los del NID."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept

Extension: DAULeyPrevisional
Id: dau-ley-previsional
Title: "Ley previsional"
Description: "Ley previsional aplicable al episodio (por ejemplo, ley de urgencia). Los códigos son los del NID."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept

Extension: DAUClasificacionConsulta
Id: dau-clasificacion-consulta
Title: "Clasificación de consulta"
Description: "Clasificación de la consulta de urgencia. Los episodios restringidos (01 abuso sexual, 02 violencia, 03 constatación de lesiones) llevan meta.security = R."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept

Extension: DAUPronosticoMedicoLegal
Id: dau-pronostico-medico-legal
Title: "Pronóstico médico legal"
Description: "Pronóstico médico legal del episodio."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept

Extension: DAUPertinencia
Id: dau-pertinencia
Title: "Pertinencia"
Description: "Pertinencia de la consulta de urgencia."
* ^context[+].type = #element
* ^context[=].expression = "Encounter"
* value[x] only CodeableConcept

Extension: DAUMedioLlegada
Id: dau-medio-llegada
Title: "Medio de llegada"
Description: "Medio por el que el paciente llegó a la urgencia (por ejemplo, SAMU, medios propios)."
* ^context[+].type = #element
* ^context[=].expression = "Encounter.hospitalization"
* value[x] only CodeableConcept
