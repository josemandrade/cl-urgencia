# Operaciones en los puntos de interoperabilidad

Las operaciones son las transacciones y consultas que el HIS/RCE, el Bus de Interoperabilidad MINSAL y la red hacen en cada punto. Todas usan datos sintéticos en los ejemplos. Cada operación tiene su transacción de ejemplo (un `Bundle` completo, con los recursos que lleva), enlazada abajo.

**Cada operación enlaza al perfil IHE que la apoya** (con su página en profiles.ihe.net), cuando hay uno. Ningún perfil IHE lleva la transacción en sí: las tres transacciones `Bundle` son nacionales, de la guía; los perfiles cubren funciones de apoyo (identidad, documentos, consulta, seguridad, tiempo). La revisión completa por punto, con el encaje y las brechas, está en [Relación con IHE](ihe.html). Las operaciones en el tiempo, flujo por flujo (cada mensaje con su operación y su resultado esperado), están en [Diagramas de secuencia](sequences.html).

## PI-1 — Publicación del aviso (push al Bus)

El HIS/RCE hace **push** de una transacción `Bundle` (type = transaction) al Bus de Interoperabilidad MINSAL en el momento del evento, en tiempo real, no por lotes. Una transacción por evento, sobre un solo `Encounter` por episodio, actualizado por PUT condicional por ID DAU. Un solo paciente por Bundle. Las referencias entre recursos van por `fullUrl` `urn:uuid:`.

### Admisión — `POST /Bundle` (transacción)

El aviso de admisión se envía cuando la persona es admitida (`Encounter.status = arrived`).

| Entrada | Operación | Recurso |
|---|---|---|
| Paciente | `POST Patient` + `ifNoneExist` | [`DAUPaciente`](StructureDefinition-dau-paciente.html) |
| Establecimiento | `POST Organization` + `ifNoneExist` | [`DAUPrestadorOrganizacional`](StructureDefinition-dau-prestador-organizacional.html) |
| Profesional | `POST Practitioner` + `ifNoneExist` | [`DAUPrestadorProfesional`](StructureDefinition-dau-prestador-profesional.html) |
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html) |

Ejemplo: [Bundle de admisión](Bundle-ejemplo-bundle-admision.html) — transacción con los maestros (POST con `ifNoneExist`) y el episodio ([Encounter de admisión](Encounter-ejemplo-encuentro-admision.html), [paciente](Patient-ejemplo-paciente.html), [establecimiento](Organization-ejemplo-establecimiento.html), [profesional](Practitioner-ejemplo-profesional.html)). Los maestros solo se crean; nunca se modifican. El `Encounter` se envía siempre completo y sin `Resource.id` en el PUT.

Perfiles IHE: [PIXm](https://profiles.ihe.net/ITI/PIXm/) (parcial — la identidad se resuelve contra el MPI dentro del Bus; ITI-83, ITI-104). La transacción en sí es nacional. [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) y [CT](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html) son transversales (TLS 1.2+, autenticación, tiempo consistente).

### Alta — `POST /Bundle` (transacción)

El aviso de alta se envía cuando el episodio se cierra con alta (`Encounter.status = finished`, `hospitalization.dischargeDisposition` con el destino).

| Entrada | Operación | Recurso |
|---|---|---|
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | [`DAUEncuentroUrgenciaAlta`](StructureDefinition-dau-encuentro-urgencia-alta.html) |
| Diagnóstico de egreso | `PUT Condition?identifier=<id local>` | [`DAUDiagnosticoUrgencia`](StructureDefinition-dau-diagnostico-urgencia.html) (CIE-10, use = DD) |
| Medicamentos | `PUT MedicationRequest?identifier=<id local>` | [`DAUIndicacionMedicamento`](StructureDefinition-dau-indicacion-medicamento.html) (solo si existen) |
| Documento | `PUT DocumentReference?identifier=<id local>` | [`DAUDocumentoUrgencia`](StructureDefinition-dau-documento-urgencia.html) (LOINC 59258-4) |

Ejemplo: [Bundle de alta con fallecimiento](Bundle-ejemplo-bundle-alta.html) (destino 03) — con el [Encounter de alta](Encounter-ejemplo-encuentro-alta.html), el [diagnóstico de egreso](Condition-ejemplo-diagnostico-egreso.html) (causa de muerte, CIE-10), el [medicamento al alta](MedicationRequest-ejemplo-medicamento-alta.html) y el [documento resumen de alta](DocumentReference-ejemplo-documento-alta.html). Si el PDF no está listo, se reenvía el Bundle de alta completo cuando exista. El fallecimiento es un alta con destino `03 Fallecido`, sin `hospitalization.destination`.

Perfiles IHE: [PIXm](https://profiles.ihe.net/ITI/PIXm/) (parcial — identidad, como en la admisión) y [MHD](https://profiles.ihe.net/ITI/MHD/) (parcial — el cierre incluye un `DocumentReference` al DAU; ITI-65 publicar el documento, ITI-67/ITI-68 buscarlo y recuperarlo). La transacción en sí es nacional; el documento se lleva como referencia dentro del Bundle de cierre, no con una transacción MHD. [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) y [CT](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html) son transversales.

### Abandono — `POST /Bundle` (transacción)

El aviso de abandono se envía cuando la persona se va antes de cerrar el episodio (`Encounter.status = finished`, tipo de abandono en la extensión [`tipoAbandono`](StructureDefinition-dau-tipo-abandono.html): 1 NEA, 2 fuga).

| Entrada | Operación | Recurso |
|---|---|---|
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | [`DAUEncuentroUrgenciaAbandono`](StructureDefinition-dau-encuentro-urgencia-abandono.html) |
| Hipótesis | `PUT Condition?identifier=<id local>` | [`DAUDiagnosticoUrgencia`](StructureDefinition-dau-diagnostico-urgencia.html) (provisional, sin use) |
| Documento | `PUT DocumentReference?identifier=<id local>` | [`DAUDocumentoUrgencia`](StructureDefinition-dau-documento-urgencia.html) (LOINC 34111-5) |

Ejemplo: [Bundle de abandono (fuga)](Bundle-ejemplo-bundle-abandono.html) — con el [Encounter de abandono](Encounter-ejemplo-encuentro-abandono.html), la [hipótesis](Condition-ejemplo-hipotesis.html) y el [documento nota de urgencia](DocumentReference-ejemplo-documento-abandono.html).

Perfiles IHE: [PIXm](https://profiles.ihe.net/ITI/PIXm/) (parcial — identidad, como en la admisión) y [MHD](https://profiles.ihe.net/ITI/MHD/) (parcial — el abandono incluye un `DocumentReference` nota de urgencia; ITI-65, ITI-67, ITI-68). La transacción en sí es nacional. [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) y [CT](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html) son transversales.

### Respuestas del Bus

- `200` (transaction-response): el aviso se aplicó.
- `400` / `422` (OperationOutcome): no se aplica nada; el HIS corrige y reenvía.
- `412`: el identificador condicional es ambiguo.
- `422`: la identidad no se resolvió en el MPI; el HIS corrige y reenvía.
- Sin respuesta: se puede reenviar (las operaciones condicionales evitan duplicados).

### Corrección

Para corregir un aviso, se reenvía el `Encounter` con `status = entered-in-error`. No se envía la admisión de un episodio ya cerrado (el PUT lo reabriría).

## PI-0 — Identidad del paciente

La identidad se resuelve contra el MPI MINSAL dentro del Bus. RUN con DV inválido: se rechaza. Identidad no encontrada: se crea en el MPI. Duplicada o contradictoria: se rechaza a conciliación. MPI caído: error transitorio.

Perfil IHE: [PIXm](https://profiles.ihe.net/ITI/PIXm/) (Patient Identifier Cross-reference for Mobile, parcial — el Bus resuelve la identidad contra el MPI, que es la función del Patient Identifier Cross-reference Manager; ITI-83 consulta, ITI-104 alimentación). El HIS no llama a PIXm: la resolución ocurre dentro del Bus, como parte de la transacción.

## PI-2 — Consulta y suscripción (pull del Repositorio)

La red hace **pull** del Repositorio FHIR. Cada operación de consulta enlaza al perfil IHE que estandariza esa búsqueda.

### Buscar paciente — `GET /Patient?identifier=<sistema RUN>|<RUN>`

Buscar a la persona atendida por su RUN, antes de consultar sus episodios.

Perfil IHE: [PDQm](https://profiles.ihe.net/ITI/PDQm/) (Patient Demographics Query for Mobile, parcial — la búsqueda de pacientes por identificador o datos demográficos es la transacción del perfil; ITI-78, ITI-119). La búsqueda de la guía es una búsqueda FHIR simple; la guía no declara conformidad PDQm ni sus opciones.

### Buscar episodios — `GET /Encounter?patient.identifier=<sistema RUN>|<RUN>&class=EMER`

Atenciones de urgencia de un paciente. También por establecimiento: `GET /Encounter?service-provider.identifier=<sistema DEIS>|<código>&class=EMER&status=arrived` (pacientes actualmente en urgencia en un establecimiento).

Perfil IHE: [QEDm](https://profiles.ihe.net/PCC/QEDm/) (Mobile Query Existing Data, parcial — el patrón de consultar datos existentes por búsqueda FHIR coincide con esta búsqueda; PCC-44). La guía no declara conformidad QEDm ni sus opciones; es una búsqueda FHIR simple, no una transacción QEDm.

### Buscar diagnósticos del episodio — `GET /Condition?encounter=Encounter/[id]`

Diagnósticos (hipótesis y diagnóstico de egreso) de una atención.

Perfil IHE: [QEDm](https://profiles.ihe.net/PCC/QEDm/) (parcial, como en buscar episodios; PCC-44).

### Buscar documento del episodio — `GET /DocumentReference?encounter=Encounter/[id]`

Documento del DAU (resumen de alta o nota de urgencia) de una atención.

Perfil IHE: [MHD](https://profiles.ihe.net/ITI/MHD/) (parcial — buscar referencias de documentos es ITI-67; la guía lo hace con una búsqueda FHIR simple, no con una transacción MHD).

### Suscribirse a episodios — `Subscription` sobre `Encounter class=EMER`

Para enterarse de un evento apenas ocurre, el consumidor crea una `Subscription` sobre `Encounter` con `class=EMER`.

Perfil IHE: ninguno — la suscripción de la guía es una [Subscription FHIR](https://www.hl7.org/fhir/subscription.html), no DSUB. DSUB (Document Metadata Subscription) es una suscripción a metadatos de documentos de un registro XDS, y el Repositorio aquí es un repositorio FHIR, no un registro XDS; por eso no encaja. El canal de notificación (por ejemplo, REST-hook) es un detalle de implementación.

## PI-3 — Acceso al PDF del DAU

El PDF se obtiene por `DocumentReference.content.attachment.url`, con autenticación. Lo publica el HIS o se replica por acuerdo institucional.

Perfil IHE: [MHD](https://profiles.ihe.net/ITI/MHD/) (parcial — recuperar un documento es ITI-68, Retrieve Document, la forma estándar de recuperar un documento). El patrón coincide; el mecanismo no: la guía descarga el PDF con un GET autenticado directo a la URL del `DocumentReference`, no con una transacción ITI-68 contra un Document Responder.
