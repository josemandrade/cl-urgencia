# Componente DAU — aviso mínimo de urgencia a la red (paso 6)

Implementación en Python de la [guía validada](../05-implementation-guide/)
(aviso mínimo de atención de urgencia a la red, SUSHI 0 errores, publicada en
https://josemandrade.github.io/cl-urgencia/). Construye SOLO lo que la guía
dice: los tres Bundles transaccionales (PI-1), la resolución de identidad
(PI-0), las consultas y la suscripción (PI-2), el acceso al PDF (PI-3) y la
clasificación de las respuestas del Bus.

Fuente de verdad: `05-implementation-guide/` (`operations.md`, `plan.md`,
`sushi-config.yaml`, FSH y ejemplos compilados) más `04-fhir-proposal.md` y
`04-mapping-table.md`. Los 14 ejemplos compilados por SUSHI viven como
goldens en `tests/goldens/` (copias textuales, nunca editados); los tests
comparan contra ellos.

## Stack

**Python 3.12, solo stdlib** (`json`, `urllib`, `uuid`, `unittest`,
`http.server` para el mock del cliente). Sin dependencias nuevas.

- `pytest` **no está instalado** en este entorno; los tests usan `unittest`
  (stdlib): `PYTHONPATH=src python3 -m unittest discover -s tests -v` o
  `sh run_tests.sh`.
- Node no aporta nada para manipular JSON FHIR; stdlib evita instalar
  dependencias y que el componente dependa de la red para correr o testearse.

## Prerrequisitos

- Python 3.12 o superior (`python3 --version`). Nada más: sin pip, sin
  paquetes, sin Java, sin SUSHI para correr el componente (SUSHI solo hizo
  falta para compilar la guía, paso 5).

## Datos sintéticos siempre

Todos los datos son ficticios, estilo `SYN-URG-001`/`SYN-URG-002` de la guía
(paciente Pérez Juan, RUN `12345678-5`; profesional González María, RUN
`98765432-5`; establecimiento DEIS `12345` "Hospital de Prueba"). **Nada de
datos reales de pacientes** en el código, los ejemplos, los tests ni este
README.

Desviaciones conocidas respecto de la guía: están registradas como `Ruling:`
en `../state.md` (RUN de ejemplo de la guía con DV inválido; identificador
local para los PUT condicionales; `contentType` del DocumentReference;
referencias `urn:uuid:` y recursos sin `id` en los Bundles; identificador
solo con `value` en los prestadores).

## Cómo correr los tests

```sh
cd 06-component
sh run_tests.sh
# o bien:
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

140 tests, todos en verde (2026-11-12): builders y validadores contra los
goldens (Tasks 2–9), Bundles contra sus goldens (Tasks 10–12), PI-0/PI-2/PI-3
(Tasks 13–19), respuestas del Bus (Task 20), cliente contra mock local y CLI
con los 12 ejemplos (Task 21). Cada test se escribió antes que el código
(RED-GREEN); el plan en `plan.md` detalla la descomposición en 21 tareas.

## Cómo usar la librería

```python
from dau.bundles import build_admission_bundle
from dau.search import build_patient_search
from dau.responses import handle_bus_response
from dau.client import DauClient

bundle = build_admission_bundle(datos)          # dict, sin id
consulta = build_patient_search("12345678-5")   # {"method": "GET", "url": ...}
cliente = DauClient("https://bus.ejemplo.cl/fhir", token="...")
status, respuesta = cliente.post_bundle(bundle)
resultado = handle_bus_response(status, respuesta)
```

- Entradas: dicts planos con claves `snake_case`.
- Builders: `build_<recurso>(data) -> dict` (JSON serializable), con
  `meta.profile` canónico y SIN `id`.
- Validadores: `validate_<recurso>(resource) -> list[str]`; lista vacía =
  válido (campos requeridos, cardinalidades, bindings e invariantes).
- Los builders no hacen llamadas de red. Solo `DauClient` habla por HTTP, y
  solo contra la `base_url` que se le pasa explícitamente.

## Configuración

No hay archivos de configuración ni variables de entorno. El cliente se
configura en el constructor:

```python
DauClient(base_url, token=None)
```

- `base_url`: base FHIR del Bus o del Repositorio (p. ej.
  `https://bus.ejemplo.cl/fhir`). Sin barra final.
- `token`: Bearer opcional; sin él no se envía cabecera `Authorization`.

## CLI

```sh
PYTHONPATH=src python3 -m dau.cli <operación> <entrada.json>
```

Escribe el JSON resultante por stdout. La CLI construye, no envía: para
enviar un Bundle hay que usar `DauClient`. Hay una entrada de ejemplo por
operación en `examples/` (12 archivos, todos sintéticos).

### Ejemplos por operación

Comandos desde `06-component/`:

```sh
PYTHONPATH=src python3 -m dau.cli admission-bundle examples/admission-bundle.json
PYTHONPATH=src python3 -m dau.cli discharge-bundle examples/discharge-bundle.json
PYTHONPATH=src python3 -m dau.cli abandonment-bundle examples/abandonment-bundle.json
PYTHONPATH=src python3 -m dau.cli patient-search examples/patient-search.json
PYTHONPATH=src python3 -m dau.cli encounter-search-by-patient examples/encounter-search-by-patient.json
PYTHONPATH=src python3 -m dau.cli encounter-search-by-provider examples/encounter-search-by-provider.json
PYTHONPATH=src python3 -m dau.cli condition-search examples/condition-search.json
PYTHONPATH=src python3 -m dau.cli document-search examples/document-search.json
PYTHONPATH=src python3 -m dau.cli subscription examples/subscription.json
PYTHONPATH=src python3 -m dau.cli pdf-download examples/pdf-download.json
PYTHONPATH=src python3 -m dau.cli resolve-identity examples/resolve-identity.json
PYTHONPATH=src python3 -m dau.cli bus-response examples/bus-response.json
```

**1. `admission-bundle` — Bundle de admisión (PI-1).** Entrada
(`examples/admission-bundle.json`): paciente, organización, profesional,
encuentro (DAU `SYN-URG-001`, DEIS `12345`, inicio `2026-11-11T10:05:00-03:00`,
ATND `10:15`, motivo "Dolor torácico") y `timestamp`. Salida esperada: Bundle
`type=transaction` con 4 entradas: POST Patient, Organization y Practitioner
con `ifNoneExist`, y PUT
`Encounter?identifier=https://interoperabilidad.minsal.cl/fhir/sid/dau/12345|SYN-URG-001`.
Las referencias internas van por `fullUrl urn:uuid:` y ningún recurso lleva
`id`.

**2. `discharge-bundle` — Bundle de alta (PI-1).** Entrada: como la admisión,
más `period_end` `14:20`, destino `03` (Fallecido), diagnóstico de egreso
ICD-10 `I46.9` confirmado, medicamento "Paracetamol 500 mg" y documento
LOINC `59258-4` (`.../SYN-URG-001.pdf`). Salida esperada: 4 PUT condicionales
(Encounter, Condition, MedicationRequest, DocumentReference); sin
`medication` en la entrada, 3 entradas.

**3. `abandonment-bundle` — Bundle de abandono (PI-1).** Entrada: DAU
`SYN-URG-002`, `period_end` `11:30`, tipo `2` (fuga), hipótesis `R07.4`
provisional, documento LOINC `34111-5` (`.../SYN-URG-002.pdf`). Salida
esperada: 3 PUT condicionales, Encounter sin `hospitalization` (sin destino
al alta).

**4. `patient-search` — Buscar paciente, PDQm (PI-2).** Entrada:
`{"run": "12345678-5"}`. Salida esperada:

```json
{"method": "GET", "url": "Patient?identifier=urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-5"}
```

Un RUN con DV inválido da error antes de construir la consulta.

**5. `encounter-search-by-patient` — Buscar episodios por paciente, QEDm
(PI-2).** Entrada: `{"run": "12345678-5"}`. Salida esperada:
`GET Encounter?patient.identifier=urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-5&class=EMER`.

**6. `encounter-search-by-provider` — Buscar episodios por prestador, QEDm
(PI-2).** Entrada: `{"deis_code": "12345"}`. Salida esperada:
`GET Encounter?service-provider.identifier=https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino|12345&class=EMER&status=arrived`.

**7. `condition-search` — Buscar diagnósticos, QEDm (PI-2).** Entrada:
`{"encounter_id": "SYN-URG-001"}`. Salida esperada:
`GET Condition?encounter=Encounter/SYN-URG-001`.

**8. `document-search` — Buscar documento, MHD ITI-67 (PI-2).** Entrada:
`{"encounter_id": "SYN-URG-001"}`. Salida esperada:
`GET DocumentReference?encounter=Encounter/SYN-URG-001`.

**9. `subscription` — Suscripción, Subscription FHIR (PI-2, no DSUB).**
Entrada: `{"channel_type": "rest-hook", "endpoint":
"https://his.ejemplo.cl/fhir/notificaciones"}`. Salida esperada:

```json
{"resourceType": "Subscription", "status": "requested", "criteria": "Encounter?class=EMER",
 "channel": {"type": "rest-hook", "endpoint": "https://his.ejemplo.cl/fhir/notificaciones"}}
```

**10. `pdf-download` — Acceso al PDF del DAU, MHD ITI-68 como patrón (PI-3).**
Entrada: un DocumentReference (con `content[0].attachment.url`) y `token`.
Salida esperada:
`{"method": "GET", "url": "https://his.ejemplo.cl/dau/SYN-URG-001.pdf",
"headers": {"Authorization": "Bearer token-sintetico"}}`. Sin URL o sin token
da error.

**11. `resolve-identity` — Identidad del paciente, PI-0 (PIXm parcial, la
resolución ocurre dentro del Bus).** Entrada:
`{"run": "12345678-5", "mpi_result": "found"}`. Salida esperada: `"resolved"`.
Los demás casos: RUN con DV inválido → `"rejected_invalid_run"`;
`not_found` → `"created"`; `duplicate` → `"rejected_to_reconciliation"`;
`down` → `"transient_error"`.

**12. `bus-response` — Clasificar una respuesta del Bus (PI-1).** Entrada:
`{"status": 200, "body": {...}}`. Salida esperada:
`{"outcome": "applied", ...}`. 400/422 (OperationOutcome) →
`"correct_and_resend"`; 412 → `"ambiguous"`; 422 con mención al MPI →
`"identity_unresolved"`.

## Trazabilidad operación → código

| Operación de la guía | Archivo | Función |
|---|---|---|
| PI-1 Bundle de admisión | `src/dau/bundles.py` | `build_admission_bundle(data, uuids=None)` |
| PI-1 Bundle de alta | `src/dau/bundles.py` | `build_discharge_bundle(data, uuids=None)` |
| PI-1 Bundle de abandono | `src/dau/bundles.py` | `build_abandonment_bundle(data, uuids=None)` |
| PI-1 Respuestas del Bus (200/400/412/422) | `src/dau/responses.py` | `handle_bus_response(status, body)` |
| PI-1 Corrección (`entered-in-error`) | `src/dau/responses.py` | `build_correction_encounter(encounter)` |
| PI-1 Admisión de episodio cerrado | `src/dau/responses.py` | `check_admission_allowed(existing_status)` |
| PI-0 Identidad del paciente | `src/dau/identity.py` | `resolve_identity(run, mpi_result)` |
| PI-2 Buscar paciente (PDQm) | `src/dau/search.py` | `build_patient_search(run)` |
| PI-2 Buscar episodios por paciente (QEDm) | `src/dau/search.py` | `build_encounter_search_by_patient(run)` |
| PI-2 Buscar episodios por prestador (QEDm) | `src/dau/search.py` | `build_encounter_search_by_provider(deis_code)` |
| PI-2 Buscar diagnósticos (QEDm) | `src/dau/search.py` | `build_condition_search(encounter_id)` |
| PI-2 Buscar documento (MHD) | `src/dau/search.py` | `build_document_search(encounter_id)` |
| PI-2 Suscripción (Subscription FHIR) | `src/dau/search.py` | `build_encounter_subscription(channel_type, endpoint)` |
| PI-3 Acceso al PDF del DAU | `src/dau/access.py` | `build_pdf_download(document_reference, token)` |
| Envío HTTP (POST Bundle, GET, GET PDF) | `src/dau/client.py` | `DauClient.post_bundle / .search / .get_pdf / .post_subscription` |
| CLI | `src/dau/cli.py` | `main(argv)` |
| Paciente (DAUPaciente) | `src/dau/patients.py` | `build_patient`, `validate_patient` |
| Prestadores | `src/dau/providers.py` | `build_organization`, `build_practitioner`, `validate_*` |
| Encuentros (admisión/alta/abandono) | `src/dau/encounters.py` | `build_*_encounter`, `validate_encounter` |
| Diagnóstico | `src/dau/conditions.py` | `build_condition`, `validate_condition` |
| Medicamento al alta | `src/dau/medications.py` | `build_medication_request`, `validate_medication_request` |
| Documento | `src/dau/documents.py` | `build_document_reference`, `validate_document_reference` |
| Identificadores (RUN/DV, sistema DAU) | `src/dau/identifiers.py` | `validate_run`, `dau_system` |
| Constantes de la guía | `src/dau/constants.py` | — |
| Validación compartida | `src/dau/validate.py` | `check_profile`, `check_coding`, `check_reference`, … |

## Estructura

```
06-component/
  plan.md            descomposición en 21 tareas (una operación por tarea)
  README.md          este archivo
  run_tests.sh       corre la suite completa
  src/dau/           paquete (versión 0.1.0)
  tests/             tests unittest + goldens/ (JSON compilados por SUSHI)
  examples/          una entrada sintética por operación (12 archivos)
```

## Lo que NO hace este componente

- No llama a ningún perfil IHE como transacción: las operaciones usan
  búsquedas FHIR simples y una Subscription FHIR; los perfiles IHE (PDQm,
  QEDm, MHD, PIXm) son el apoyo documentado en la guía, no el mecanismo.
- No toca datos reales ni se conecta a ningún servidor por defecto: el
  cliente solo existe si se instancia con una `base_url` explícita.
- No publica la guía ni sube nada a GitHub: el push necesita la aprobación
  del usuario (ver `../state.md`; la carpeta del caso no es un checkout git).
