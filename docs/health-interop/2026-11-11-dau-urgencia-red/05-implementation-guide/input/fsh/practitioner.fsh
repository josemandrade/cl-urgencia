// Profesional de salud.
// Fuente: perfil MINSAL Prestador Profesional (NID) de la Guía de
// interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

Profile: DAUPrestadorProfesional
Parent: Practitioner
Id: dau-prestador-profesional
Title: "Prestador profesional (DAU)"
Description: "Profesional de salud (médico tratante ATND o quien da el alta DIS). Basado en el perfil MINSAL Prestador Profesional (NID) de la guía cl-urgencia v0.2.0."
* identifier 1..1
* identifier.system = "urn:oid:2.16.840.1.113883.2.22.1.152.787300"
* identifier.value 1..1
* identifier.value ^short = "RUN del profesional, sin puntos ni guión, con DV"
* name 1..1
