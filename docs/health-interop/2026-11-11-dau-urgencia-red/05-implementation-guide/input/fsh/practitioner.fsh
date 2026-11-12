// Profesional de salud.
// Perfil propio de esta guía. Diseñado a partir de la especificación del caso
// de uso (entidades y datos de los pasos 1–3) sobre el recurso base
// Practitioner de FHIR R4.

Profile: DAUPrestadorProfesional
Parent: Practitioner
Id: dau-prestador-profesional
Title: "Prestador profesional (DAU)"
Description: "Profesional de salud (médico tratante ATND o quien da el alta DIS). Perfil propio de esta guía, sobre el recurso base Practitioner de FHIR R4."
* identifier 1..1
* identifier.system = "urn:oid:2.16.840.1.113883.2.22.1.152.787300"
* identifier.value 1..1
* identifier.value ^short = "RUN del profesional, sin puntos ni guión, con DV"
* name 1..1
