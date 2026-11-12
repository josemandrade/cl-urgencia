// Encounter del episodio de urgencia.
// Fuente: perfil EncuentroUrgencia (y sus variantes de alta y abandono) de la
// Guía de interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

Invariant: dau-enc-period
Description: "La fecha de término del episodio no puede ser anterior a la fecha de admisión (urg-enc-3)."
Expression: "period.end.empty() or period.end >= period.start"
Severity: #error

Invariant: dau-enc-reason
Description: "El motivo de consulta (reasonCode.text) tiene como máximo 200 caracteres."
Expression: "reasonCode.text.all($this.length() <= 200)"
Severity: #error

Invariant: dau-alta-destino
Description: "Si el destino al alta es hospitalización, traslado o derivación (01/02/04), debe indicarse el establecimiento de destino."
Expression: "hospitalization.dischargeDisposition.coding.where(code = '01' or code = '02' or code = '04').exists() implies hospitalization.destination.exists()"
Severity: #error

Profile: DAUEncuentroUrgencia
Parent: Encounter
Id: dau-encuentro-urgencia
Title: "Encuentro de urgencia (DAU)"
Description: "Episodio de atención de urgencia. Basado en el perfil EncuentroUrgencia de la guía cl-urgencia v0.2.0 (sobre EncounterCL de CL-Core). Un solo Encounter por episodio, actualizado por PUT condicional por ID DAU."
* obeys dau-enc-period
* obeys dau-enc-reason
* identifier 1..*
* identifier.system 1..1
* identifier.system ^short = "Sistema del ID DAU: https://interoperabilidad.minsal.cl/fhir/sid/dau/[código DEIS]"
* identifier.value 1..1
* identifier.value ^short = "ID DAU, único por establecimiento, nunca reutilizado"
* status 1..1
* status ^short = "arrived (admisión), finished (alta o abandono) o entered-in-error (corrección)"
* class 1..1
* class = http://terminology.hl7.org/CodeSystem/v3-ActCode#EMER "Emergencia"
* subject 1..1
* subject only Reference(DAUPaciente)
* serviceProvider 1..1
* serviceProvider only Reference(DAUPrestadorOrganizacional)
* participant ^slicing.discriminator.type = #value
* participant ^slicing.discriminator.path = "type"
* participant ^slicing.rules = #open
* participant contains atnd 0..1 and dis 0..1
* participant[atnd].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#ATND "atendiente"
* participant[atnd].individual only Reference(DAUPrestadorProfesional)
* participant[atnd].period.start 1..1
* participant[atnd].period.start ^short = "Inicio de la atención médica"
* participant[dis].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#DIS "quien da el alta"
* participant[dis].individual only Reference(DAUPrestadorProfesional)
* period 1..1
* period.start 1..1
* period.start ^short = "Admisión (llegada a la urgencia)"
* period.end 0..1
* period.end ^short = "Salida física (alta) u hora en que se constata el abandono"
* reasonCode 0..1
* reasonCode.text 1..1
* diagnosis 0..*
* diagnosis.condition only Reference(DAUDiagnosticoUrgencia)
* hospitalization.destination 0..1
* hospitalization.destination only Reference(DAUPrestadorOrganizacional)
* hospitalization.extension contains DAUMedioLlegada named medioLlegada 0..1
* extension contains DAUPrevision named prevision 0..1
* extension contains DAULeyPrevisional named leyPrevisional 0..1
* extension contains DAUClasificacionConsulta named clasificacionConsulta 0..1
* extension contains DAUPronosticoMedicoLegal named pronosticoMedicoLegal 0..1
* extension contains DAUPertinencia named pertinencia 0..1

Profile: DAUEncuentroUrgenciaAlta
Parent: DAUEncuentroUrgencia
Id: dau-encuentro-urgencia-alta
Title: "Encuentro de urgencia — alta (DAU)"
Description: "Variante de alta del episodio de urgencia. Basada en el perfil EncuentroUrgenciaAlta de la guía cl-urgencia v0.2.0. El fallecimiento es un alta con destino 03 Fallecido: hospitalization.dischargeDisposition = 03, period.end = hora del fallecimiento, diagnóstico de egreso = causa de muerte (CIE-10, use = DD)."
* obeys dau-alta-destino
* status = #finished
* hospitalization.dischargeDisposition 1..1
* hospitalization.dischargeDisposition from DAUDestinoAlta (required)
* diagnosis 1..*
* diagnosis.use = http://terminology.hl7.org/CodeSystem/diagnosis-role#DD "Diagnóstico de egreso"
* period.end 1..1

Profile: DAUEncuentroUrgenciaAbandono
Parent: DAUEncuentroUrgencia
Id: dau-encuentro-urgencia-abandono
Title: "Encuentro de urgencia — abandono (DAU)"
Description: "Variante de abandono voluntario del episodio de urgencia. Basada en el perfil EncuentroUrgencia (abandono) de la guía cl-urgencia v0.2.0. No lleva dischargeDisposition ni destino: el tipo de abandono va en la extensión tipoAbandono (1 NEA, 2 fuga)."
* status = #finished
* extension contains DAUTipoAbandono named tipoAbandono 1..1
* diagnosis 0..*
* diagnosis.use 0..0
* period.end 1..1
* hospitalization.dischargeDisposition 0..0
* hospitalization.destination 0..0
