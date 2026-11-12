// Establecimiento de salud.
// Fuente: perfil MINSAL Prestador Organizacional (NID) de la Guía de
// interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

Profile: DAUPrestadorOrganizacional
Parent: Organization
Id: dau-prestador-organizacional
Title: "Prestador organizacional (DAU)"
Description: "Establecimiento de salud (emisor del aviso o destino del alta). Basado en el perfil MINSAL Prestador Organizacional (NID) de la guía cl-urgencia v0.2.0."
* identifier 1..1
* identifier.system = "https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino"
* identifier.value 1..1
* identifier.value ^short = "Código DEIS del establecimiento"
* name 1..1
