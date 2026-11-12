// Establecimiento de salud.
// Perfil propio de esta guía. Diseñado a partir de la especificación del caso
// de uso (entidades y datos de los pasos 1–3) sobre el recurso base
// Organization de FHIR R4.

Profile: DAUPrestadorOrganizacional
Parent: Organization
Id: dau-prestador-organizacional
Title: "Prestador organizacional (DAU)"
Description: "Establecimiento de salud (emisor del aviso o destino del alta). Perfil propio de esta guía, sobre el recurso base Organization de FHIR R4."
* identifier 1..1
* identifier.system = "https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino"
* identifier.value 1..1
* identifier.value ^short = "Código DEIS del establecimiento"
* name 1..1
