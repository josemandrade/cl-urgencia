// Documento del episodio de urgencia (resumen de alta o nota de urgencia).
// Fuente: perfil Documento de urgencia de la Guía de interoperabilidad de
// eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

ValueSet: DAUTipoDocumento
Id: dau-tipo-documento
Title: "Tipo de documento de urgencia (DAU)"
Description: "Tipos de documento del episodio de urgencia: resumen de alta (LOINC 59258-4) y nota de urgencia (LOINC 34111-5)."
* http://loinc.org#59258-4 "Resumen de alta de urgencia"
* http://loinc.org#34111-5 "Nota de urgencia"

Profile: DAUDocumentoUrgencia
Parent: DocumentReference
Id: dau-documento-urgencia
Title: "Documento de urgencia (DAU)"
Description: "Documento del episodio de urgencia: resumen de alta (LOINC 59258-4, en el alta) o nota de urgencia (LOINC 34111-5, en el abandono). El PDF del DAU se publica por content.attachment.url, con autenticación."
* status 1..1
* status = #current
* type 1..1
* type from DAUTipoDocumento (required)
* subject 1..1
* subject only Reference(DAUPaciente)
* context.encounter 1..1
* context.encounter only Reference(DAUEncuentroUrgencia)
* content 1..1
* content.attachment.contentType = #application/pdf
* content.attachment.url 1..1
* content.attachment.url ^short = "URL del PDF del DAU, con autenticación. Lo publica el HIS o se replica por acuerdo institucional."
* date 1..1
