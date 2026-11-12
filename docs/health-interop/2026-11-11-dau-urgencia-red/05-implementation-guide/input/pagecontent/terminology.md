# Terminología

Esta página lista los sistemas de códigos y los conjuntos de valores que usa la guía. Los artefactos definidos en esta guía tienen su propia página (con la definición lógica y la expansión completa de los códigos); las terminologías externas se citan por su sistema canónico. La lista completa de artefactos está en el [resumen de artefactos](artifacts.html).

## Sistemas de códigos definidos en esta guía

| Sistema de códigos | Sistema (URL canónica) | Códigos |
|---|---|---|
| [`Destino al alta de urgencia (DAU)`](CodeSystem-dau-destino-alta.html) (`DAUDestinoAlta`) | `https://josemandrade.github.io/cl-urgencia/CodeSystem/dau-destino-alta` | 01 Hospitalización, 02 Traslado, 03 Fallecido, 04 Derivación, 05 Domicilio, 06 Otro |
| [`Tipo de abandono`](CodeSystem-dau-tipo-abandono.html) (`DAUTipoAbandono`) | `https://josemandrade.github.io/cl-urgencia/CodeSystem/dau-tipo-abandono` | 1 NEA, 2 Fuga |

Los códigos de destino al alta (01–06) y de tipo de abandono (1–2) son los que el caso de uso exige informar a la red; los sistemas de códigos son propios de esta guía (definidos en la terminología local). La guía nacional de eventos de urgencia del MINSAL (cl-urgencia v0.2.0) es la referencia de esos requisitos de datos.

## Conjuntos de valores definidos en esta guía

| Conjunto de valores | Contenido | Usado en |
|---|---|---|
| [`Destino al alta de urgencia (DAU)`](ValueSet-dau-destino-alta.html) (`DAUDestinoAlta`) | Todos los códigos de [`DAUDestinoAlta`](CodeSystem-dau-destino-alta.html) (01–06) | `DAUEncuentroUrgenciaAlta.hospitalization.dischargeDisposition` (binding requerido) |
| [`Tipo de abandono`](ValueSet-dau-tipo-abandono.html) (`DAUTipoAbandonoVS`) | Todos los códigos de [`DAUTipoAbandono`](CodeSystem-dau-tipo-abandono.html) (1–2) | Extensión [`DAUTipoAbandono`](StructureDefinition-dau-tipo-abandono.html) |
| [`Tipo de documento de urgencia (DAU)`](ValueSet-dau-tipo-documento.html) (`DAUTipoDocumento`) | LOINC 59258-4 (resumen de alta), LOINC 34111-5 (nota de urgencia) | `DAUDocumentoUrgencia.type` (binding requerido) |

Cada página de ValueSet muestra la expansión completa (código, display y definición de cada concepto).

## Terminologías externas

La guía usa terminologías externas que no define: solo las referencia por su sistema canónico.

| Terminología | Sistema | Para qué se usa |
|---|---|---|
| CIE-10 | `http://hl7.org/fhir/sid/icd-10` | Diagnóstico de egreso en el alta (código preferente, `use = DD`); causa de muerte en el fallecimiento; hipótesis y diagnósticos en general |
| SNOMED CT | `http://snomed.info/sct` | Diagnósticos (alternativa a CIE-10) |
| LOINC | `http://loinc.org` | Tipo de documento: 59258-4 resumen de alta, 34111-5 nota de urgencia |
| NID (MINSAL) | Códigos del Nomenclador de Identificación y Datos (sin cero a la izquierda: `01 FONASA` → `1`) | Previsión, ley previsional; tipo de identificación (TIPO_IDENTIFICACION) |
| Códigos de identificación de personas (CL-Core) | `CSTipoIdentificador` | Tipo de identificador del paciente (01 RUN, 05 PPN, 03 RUN Madre, 12 ficha local, 14 Otro) |
| v3-ActCode (HL7) | `http://terminology.hl7.org/CodeSystem/v3-ActCode` | `Encounter.class` = EMER (emergencia) |
| v3-ParticipationType (HL7) | `http://terminology.hl7.org/CodeSystem/v3-ParticipationType` | `Encounter.participant.type` = ATND (médico tratante), DIS (quien da el alta) |

## Sistemas de identificación

| Sistema | URL | Para qué |
|---|---|---|
| ID DAU | `https://interoperabilidad.minsal.cl/fhir/sid/dau/[código DEIS]` | Identificador del episodio de urgencia (clave del PUT condicional); único por establecimiento, nunca reutilizado |
| RUN | `urn:oid:2.16.840.1.113883.2.22.1.152.787300` | Identificador de la persona atendida (y del profesional) |
| Establecimiento (código DEIS) | `https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino` | Identificador del establecimiento emisor o destino |

TAPSA no se acepta como sistema de codificación de diagnósticos mientras DEIS no publique su sistema (decisión de la guía del MINSAL v0.2.0).
