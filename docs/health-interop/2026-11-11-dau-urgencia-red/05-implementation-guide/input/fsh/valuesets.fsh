// Destino al alta de urgencia.
// Fuente: ValueSet "Destino al alta de urgencia" (vs-destino-alta) de la
// Guía de interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0).

CodeSystem: DAUDestinoAltaCS
Id: dau-destino-alta
Title: "Destino al alta de urgencia (DAU)"
Description: "Códigos de destino al alta de urgencia, de la guía cl-urgencia v0.2.0."
* #01 "Hospitalización" "Hospitalización en el mismo u otro establecimiento"
* #02 "Traslado" "Traslado a otro establecimiento"
* #03 "Fallecido" "Fallecimiento durante la atención de urgencia"
* #04 "Derivación" "Derivación a otro nivel de atención"
* #05 "Domicilio" "Alta a domicilio"
* #06 "Otro" "Otro destino"

ValueSet: DAUDestinoAlta
Id: dau-destino-alta
Title: "Destino al alta de urgencia (DAU)"
Description: "Destinos posibles al alta de urgencia."
* include codes from system DAUDestinoAltaCS
