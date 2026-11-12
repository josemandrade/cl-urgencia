# Operaciones en los puntos de interoperabilidad

Las operaciones son las transacciones y consultas que el HIS/RCE, el Bus de Interoperabilidad MINSAL y la red hacen en cada punto. Todas usan datos sintéticos en los ejemplos.

## PI-1 — Publicación del aviso (push al Bus)

El HIS/RCE hace **push** de una transacción `Bundle` (type = transaction) al Bus de Interoperabilidad MINSAL en el momento del evento, en tiempo real, no por lotes. Una transacción por evento, sobre un solo `Encounter` por episodio, actualizado por PUT condicional por ID DAU. Un solo paciente por Bundle. Las referencias entre recursos van por `fullUrl` `urn:uuid:`.

### Admisión — `POST /Bundle` (transacción)

El aviso de admisión se envía cuando la persona es admitida (`Encounter.status = arrived`).

| Entrada | Operación | Recurso |
|---|---|---|
| Paciente | `POST Patient` + `ifNoneExist` | `DAUPaciente` |
| Establecimiento | `POST Organization` + `ifNoneExist` | `DAUPrestadorOrganizacional` |
| Profesional | `POST Practitioner` + `ifNoneExist` | `DAUPrestadorProfesional` |
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | `DAUEncuentroUrgencia` |

Ejemplo: `ejemplo-bundle-admision`. Los maestros solo se crean; nunca se modifican. El `Encounter` se envía siempre completo y sin `Resource.id` en el PUT.

### Alta — `POST /Bundle` (transacción)

El aviso de alta se envía cuando el episodio se cierra con alta (`Encounter.status = finished`, `hospitalization.dischargeDisposition` con el destino).

| Entrada | Operación | Recurso |
|---|---|---|
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | `DAUEncuentroUrgenciaAlta` |
| Diagnóstico de egreso | `PUT Condition?identifier=<id local>` | `DAUDiagnosticoUrgencia` (CIE-10, use = DD) |
| Medicamentos | `PUT MedicationRequest?identifier=<id local>` | `DAUIndicacionMedicamento` (solo si existen) |
| Documento | `PUT DocumentReference?identifier=<id local>` | `DAUDocumentoUrgencia` (LOINC 59258-4) |

Ejemplo: `ejemplo-bundle-alta` (alta con fallecimiento, destino 03). Si el PDF no está listo, se reenvía el Bundle de alta completo cuando exista. El fallecimiento es un alta con destino `03 Fallecido`, sin `hospitalization.destination`.

### Abandono — `POST /Bundle` (transacción)

El aviso de abandono se envía cuando la persona se va antes de cerrar el episodio (`Encounter.status = finished`, tipo de abandono en la extensión `tipoAbandono`: 1 NEA, 2 fuga).

| Entrada | Operación | Recurso |
|---|---|---|
| Episodio | `PUT Encounter?identifier=<sistema DAU>\|<ID DAU>` | `DAUEncuentroUrgenciaAbandono` |
| Hipótesis | `PUT Condition?identifier=<id local>` | `DAUDiagnosticoUrgencia` (provisional, sin use) |
| Documento | `PUT DocumentReference?identifier=<id local>` | `DAUDocumentoUrgencia` (LOINC 34111-5) |

Ejemplo: `ejemplo-bundle-abandono` (fuga).

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

## PI-2 — Consulta y suscripción (pull del Repositorio)

La red hace **pull** del Repositorio FHIR:

- `Encounter?patient.identifier=<sistema RUN>|<RUN>&class=EMER`
- `Encounter?service-provider.identifier=<sistema DEIS>|<código>&class=EMER&status=arrived`
- `Condition?encounter=Encounter/[id]`
- `DocumentReference?encounter=Encounter/[id]`

O **suscripción**: `Subscription` sobre `Encounter` con `class=EMER` (una suscripción FHIR, no DSUB).

## PI-3 — Acceso al PDF del DAU

El PDF se obtiene por `DocumentReference.content.attachment.url`, con autenticación. Lo publica el HIS o se replica por acuerdo institucional.
