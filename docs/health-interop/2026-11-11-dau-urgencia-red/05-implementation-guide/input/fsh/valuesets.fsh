// Destino al alta de urgencia.
// Sistema de códigos propio de esta guía. Los destinos son los que el caso de
// uso exige informar a la red (hospitalización, traslado, fallecido,
// derivación, domicilio, otro).

CodeSystem: DAUDestinoAltaCS
Id: dau-destino-alta
Title: "Destino al alta de urgencia (DAU)"
Description: "Códigos de destino al alta de urgencia, definidos en esta guía."
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
