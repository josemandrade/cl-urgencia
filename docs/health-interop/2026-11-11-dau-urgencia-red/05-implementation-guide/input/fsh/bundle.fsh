// Transacción con el aviso mínimo de un evento del episodio.
// Perfil propio de esta guía. Diseñado a partir de la especificación del caso
// de uso (entidades y datos de los pasos 1–3) sobre el recurso base Bundle
// de FHIR R4.

Profile: DAUBundleAviso
Parent: Bundle
Id: dau-bundle-aviso
Title: "Bundle de aviso (DAU)"
Description: "Transacción con el aviso mínimo de un evento del episodio de urgencia (admisión, alta o abandono). Un Bundle por evento, sobre un solo Encounter. Un solo paciente por Bundle. Las referencias entre recursos van por fullUrl urn:uuid:. Maestros (Patient, Organization, Practitioner): solo POST con ifNoneExist. Episodio (Encounter, Condition, MedicationRequest, DocumentReference): PUT condicional por identificador local del HIS."
* type 1..1
* type = #transaction
* timestamp 1..1
* entry 1..*
* entry.fullUrl 1..1
* entry.fullUrl ^short = "urn:uuid: de la instancia dentro de la transacción"
* entry.resource 1..1
* entry.request 1..1
* entry.request.method 1..1
* entry.request.url 1..1
* entry.request.url ^short = "La operación condicional: POST con ifNoneExist para los maestros, PUT condicional por identificador local para el episodio"
