// Ejemplos sintéticos. Todos los datos son ficticios (SYN-URG-001, RUN ficticios).
// Nunca datos reales de pacientes.

// ---------- Maestros ----------

Instance: ejemplo-paciente
InstanceOf: DAUPaciente
Title: "Paciente de ejemplo (SYN-URG-001)"
Description: "Persona atendida en la urgencia (datos sintéticos)."
Usage: #example
* identifier[run].value = "12345678-9"
* name.family = "Pérez"
* name.given[0] = "Juan"
* gender = #male
* birthDate = "1980-05-15"

Instance: ejemplo-establecimiento
InstanceOf: DAUPrestadorOrganizacional
Title: "Establecimiento de ejemplo"
Description: "Establecimiento emisor del aviso (datos sintéticos)."
Usage: #example
* identifier.value = "12345"
* name = "Hospital de Prueba"

Instance: ejemplo-profesional
InstanceOf: DAUPrestadorProfesional
Title: "Profesional de ejemplo"
Description: "Médico tratante (datos sintéticos)."
Usage: #example
* identifier.value = "98765432-1"
* name.family = "González"
* name.given[0] = "María"

// ---------- Episodio: admisión ----------

Instance: ejemplo-encuentro-admision
InstanceOf: DAUEncuentroUrgencia
Title: "Encuentro de ejemplo — admisión"
Description: "Episodio de urgencia en admisión (status = arrived). Datos sintéticos."
Usage: #example
* identifier[0].system = "https://interoperabilidad.minsal.cl/fhir/sid/dau/12345"
* identifier[0].value = "SYN-URG-001"
* status = #arrived
* subject = Reference(ejemplo-paciente)
* serviceProvider = Reference(ejemplo-establecimiento)
* participant[atnd].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#ATND "atendiente"
* participant[atnd].individual = Reference(ejemplo-profesional)
* participant[atnd].period.start = "2026-11-11T10:15:00-03:00"
* period.start = "2026-11-11T10:05:00-03:00"
* reasonCode.text = "Dolor torácico"

// ---------- Episodio: alta (fallecimiento) ----------

Instance: ejemplo-encuentro-alta
InstanceOf: DAUEncuentroUrgenciaAlta
Title: "Encuentro de ejemplo — alta con fallecimiento"
Description: "Episodio de urgencia cerrado por fallecimiento (destino 03). Datos sintéticos."
Usage: #example
* identifier[0].system = "https://interoperabilidad.minsal.cl/fhir/sid/dau/12345"
* identifier[0].value = "SYN-URG-001"
* status = #finished
* subject = Reference(ejemplo-paciente)
* serviceProvider = Reference(ejemplo-establecimiento)
* participant[atnd].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#ATND "atendiente"
* participant[atnd].individual = Reference(ejemplo-profesional)
* participant[atnd].period.start = "2026-11-11T10:15:00-03:00"
* participant[dis].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#DIS "quien da el alta"
* participant[dis].individual = Reference(ejemplo-profesional)
* period.start = "2026-11-11T10:05:00-03:00"
* period.end = "2026-11-11T14:20:00-03:00"
* reasonCode.text = "Dolor torácico"
* hospitalization.dischargeDisposition = DAUDestinoAltaCS#03 "Fallecido"
* diagnosis[0].use = http://terminology.hl7.org/CodeSystem/diagnosis-role#DD "Diagnóstico de egreso"
* diagnosis[0].condition = Reference(ejemplo-diagnostico-egreso)

Instance: ejemplo-diagnostico-egreso
InstanceOf: DAUDiagnosticoUrgencia
Title: "Diagnóstico de egreso de ejemplo (causa de muerte)"
Description: "Causa de muerte CIE-10 I46.9, con use = DD. Datos sintéticos."
Usage: #example
* clinicalStatus = http://terminology.hl7.org/CodeSystem/condition-clinical#active "Activo"
* verificationStatus = http://terminology.hl7.org/CodeSystem/condition-ver-status#confirmed "Confirmado"
* code = http://hl7.org/fhir/sid/icd-10#I46.9 "Paro cardíaco, no especificado"
* subject = Reference(ejemplo-paciente)
* encounter = Reference(ejemplo-encuentro-alta)
* recordedDate = "2026-11-11T14:20:00-03:00"

Instance: ejemplo-medicamento-alta
InstanceOf: DAUIndicacionMedicamento
Title: "Medicamento al alta de ejemplo"
Description: "Medicamento indicado al alta. Datos sintéticos."
Usage: #example
* status = #active
* intent = #order
* medicationCodeableConcept.text = "Paracetamol 500 mg"
* subject = Reference(ejemplo-paciente)
* encounter = Reference(ejemplo-encuentro-alta)
* dosageInstruction[0].text = "1 comprimido cada 8 horas por 5 días"

Instance: ejemplo-documento-alta
InstanceOf: DAUDocumentoUrgencia
Title: "Documento de ejemplo — resumen de alta"
Description: "Resumen de alta (LOINC 59258-4) con el PDF del DAU. Datos sintéticos."
Usage: #example
* status = #current
* type = http://loinc.org#59258-4 "Resumen de alta de urgencia"
* subject = Reference(ejemplo-paciente)
* context.encounter = Reference(ejemplo-encuentro-alta)
* content.attachment.url = "https://his.ejemplo.cl/dau/SYN-URG-001.pdf"
* date = "2026-11-11T14:25:00-03:00"

// ---------- Episodio: abandono (fuga) ----------

Instance: ejemplo-encuentro-abandono
InstanceOf: DAUEncuentroUrgenciaAbandono
Title: "Encuentro de ejemplo — abandono (fuga)"
Description: "Episodio cerrado por abandono voluntario (fuga). Datos sintéticos."
Usage: #example
* identifier[0].system = "https://interoperabilidad.minsal.cl/fhir/sid/dau/12345"
* identifier[0].value = "SYN-URG-002"
* status = #finished
* subject = Reference(ejemplo-paciente)
* serviceProvider = Reference(ejemplo-establecimiento)
* participant[atnd].type = http://terminology.hl7.org/CodeSystem/v3-ParticipationType#ATND "atendiente"
* participant[atnd].individual = Reference(ejemplo-profesional)
* participant[atnd].period.start = "2026-11-11T10:15:00-03:00"
* period.start = "2026-11-11T10:05:00-03:00"
* period.end = "2026-11-11T11:30:00-03:00"
* reasonCode.text = "Dolor torácico"
* extension[tipoAbandono].valueCodeableConcept = DAUTipoAbandonoCS#2 "Fuga"
* diagnosis[0].condition = Reference(ejemplo-hipotesis)

Instance: ejemplo-hipotesis
InstanceOf: DAUDiagnosticoUrgencia
Title: "Hipótesis de ejemplo"
Description: "Hipótesis diagnóstica provisional, sin use. Datos sintéticos."
Usage: #example
* clinicalStatus = http://terminology.hl7.org/CodeSystem/condition-clinical#active "Activo"
* verificationStatus = http://terminology.hl7.org/CodeSystem/condition-ver-status#provisional "Provisional"
* code = http://hl7.org/fhir/sid/icd-10#R07.4 "Dolor en el pecho, no especificado"
* subject = Reference(ejemplo-paciente)
* encounter = Reference(ejemplo-encuentro-abandono)
* recordedDate = "2026-11-11T11:00:00-03:00"

Instance: ejemplo-documento-abandono
InstanceOf: DAUDocumentoUrgencia
Title: "Documento de ejemplo — nota de urgencia"
Description: "Nota de urgencia (LOINC 34111-5) con el PDF del DAU. Datos sintéticos."
Usage: #example
* status = #current
* type = http://loinc.org#34111-5 "Nota de urgencia"
* subject = Reference(ejemplo-paciente)
* context.encounter = Reference(ejemplo-encuentro-abandono)
* content.attachment.url = "https://his.ejemplo.cl/dau/SYN-URG-002.pdf"
* date = "2026-11-11T11:35:00-03:00"

// ---------- Bundles (transacciones) ----------

Instance: ejemplo-bundle-admision
InstanceOf: DAUBundleAviso
Title: "Bundle de ejemplo — admisión"
Description: "Transacción de admisión: POST de los maestros con ifNoneExist, PUT condicional del Encounter por ID DAU. Datos sintéticos."
Usage: #example
* type = #transaction
* timestamp = "2026-11-11T10:05:00-03:00"
* entry[0].fullUrl = "urn:uuid:11111111-1111-1111-1111-111111111111"
* entry[0].resource = ejemplo-paciente
* entry[0].request.method = #POST
* entry[0].request.url = "Patient"
* entry[0].request.ifNoneExist = "identifier=urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-9"
* entry[1].fullUrl = "urn:uuid:22222222-2222-2222-2222-222222222222"
* entry[1].resource = ejemplo-establecimiento
* entry[1].request.method = #POST
* entry[1].request.url = "Organization"
* entry[1].request.ifNoneExist = "identifier=https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino|12345"
* entry[2].fullUrl = "urn:uuid:33333333-3333-3333-3333-333333333333"
* entry[2].resource = ejemplo-profesional
* entry[2].request.method = #POST
* entry[2].request.url = "Practitioner"
* entry[2].request.ifNoneExist = "identifier=urn:oid:2.16.840.1.113883.2.22.1.152.787300|98765432-1"
* entry[3].fullUrl = "urn:uuid:44444444-4444-4444-4444-444444444444"
* entry[3].resource = ejemplo-encuentro-admision
* entry[3].request.method = #PUT
* entry[3].request.url = "Encounter?identifier=https://interoperabilidad.minsal.cl/fhir/sid/dau/12345|SYN-URG-001"

Instance: ejemplo-bundle-alta
InstanceOf: DAUBundleAviso
Title: "Bundle de ejemplo — alta con fallecimiento"
Description: "Transacción de alta: PUT condicional del Encounter (finished, destino 03), de la Condition (causa de muerte), del MedicationRequest y del DocumentReference. Datos sintéticos."
Usage: #example
* type = #transaction
* timestamp = "2026-11-11T14:25:00-03:00"
* entry[0].fullUrl = "urn:uuid:44444444-4444-4444-4444-444444444444"
* entry[0].resource = ejemplo-encuentro-alta
* entry[0].request.method = #PUT
* entry[0].request.url = "Encounter?identifier=https://interoperabilidad.minsal.cl/fhir/sid/dau/12345|SYN-URG-001"
* entry[1].fullUrl = "urn:uuid:55555555-5555-5555-5555-555555555555"
* entry[1].resource = ejemplo-diagnostico-egreso
* entry[1].request.method = #PUT
* entry[1].request.url = "Condition?identifier=https://his.ejemplo.cl/fhir/sid/diagnostico|SYN-URG-001-1"
* entry[2].fullUrl = "urn:uuid:66666666-6666-6666-6666-666666666666"
* entry[2].resource = ejemplo-medicamento-alta
* entry[2].request.method = #PUT
* entry[2].request.url = "MedicationRequest?identifier=https://his.ejemplo.cl/fhir/sid/medicamento|SYN-URG-001-1"
* entry[3].fullUrl = "urn:uuid:77777777-7777-7777-7777-777777777777"
* entry[3].resource = ejemplo-documento-alta
* entry[3].request.method = #PUT
* entry[3].request.url = "DocumentReference?identifier=https://his.ejemplo.cl/fhir/sid/documento|SYN-URG-001-1"

Instance: ejemplo-bundle-abandono
InstanceOf: DAUBundleAviso
Title: "Bundle de ejemplo — abandono (fuga)"
Description: "Transacción de abandono: PUT condicional del Encounter (finished, tipo 2 fuga), de la Condition (hipótesis provisional) y del DocumentReference (nota de urgencia). Datos sintéticos."
Usage: #example
* type = #transaction
* timestamp = "2026-11-11T11:35:00-03:00"
* entry[0].fullUrl = "urn:uuid:88888888-8888-8888-8888-888888888888"
* entry[0].resource = ejemplo-encuentro-abandono
* entry[0].request.method = #PUT
* entry[0].request.url = "Encounter?identifier=https://interoperabilidad.minsal.cl/fhir/sid/dau/12345|SYN-URG-002"
* entry[1].fullUrl = "urn:uuid:99999999-9999-9999-9999-999999999999"
* entry[1].resource = ejemplo-hipotesis
* entry[1].request.method = #PUT
* entry[1].request.url = "Condition?identifier=https://his.ejemplo.cl/fhir/sid/diagnostico|SYN-URG-002-1"
* entry[2].fullUrl = "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
* entry[2].resource = ejemplo-documento-abandono
* entry[2].request.method = #PUT
* entry[2].request.url = "DocumentReference?identifier=https://his.ejemplo.cl/fhir/sid/documento|SYN-URG-002-1"
