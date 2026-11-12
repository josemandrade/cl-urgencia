// Paciente atendido en la urgencia.
// Perfil propio de esta guía. Diseñado a partir de la especificación del caso
// de uso (entidades y datos de los pasos 1–3) sobre el recurso base Patient
// de FHIR R4.

Profile: DAUPaciente
Parent: Patient
Id: dau-paciente
Title: "Paciente de urgencia (DAU)"
Description: "Persona atendida en la urgencia. Perfil propio de esta guía, sobre el recurso base Patient de FHIR R4. En NN (persona sin identificar) se usa la ficha clínica local como identificador, con gender = unknown y birthDate ausente."
* identifier 1..*
* identifier ^slicing.discriminator.type = #value
* identifier ^slicing.discriminator.path = "system"
* identifier ^slicing.rules = #open
* identifier contains run 1..1 and fichaLocal 0..1
* identifier[run].system = "urn:oid:2.16.840.1.113883.2.22.1.152.787300"
* identifier[run].value 1..1
* identifier[run].value ^short = "RUN, sin puntos ni guión, con DV"
* identifier[fichaLocal].type 0..1
* identifier[fichaLocal].type ^short = "Tipo de identificador 12 (ficha clínica local)"
* identifier[fichaLocal].use = #temp
* identifier[fichaLocal].value 1..1
* name ^short = "Nombre y apellidos. Ausente en NN (con data-absent-reason = unknown)"
* gender 1..1
* gender ^short = "01 male, 02 female, 03 other, 99 unknown (mapeo CMBD)"
* birthDate 0..1
* deceased[x] 0..1
* deceased[x] ^short = "false en NN. La muerte no se registra aquí: el fallecimiento es un alta con destino 03 en el Encounter."
