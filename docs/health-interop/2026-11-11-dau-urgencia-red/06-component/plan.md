# Plan — Componente (paso 6)

Caso: aviso mínimo de atención de urgencia a la red (DAU). Fuente de verdad:
`05-implementation-guide/` (operations.md, sushi-config.yaml, FSH y ejemplos
compilados en `fsh-generated/resources/`), `04-fhir-proposal.md` y
`04-mapping-table.md`. Todo validado; el paso 6 construye SOLO lo que la guía
dice.

## Decisiones del plan

- **Stack: Python 3.12, solo stdlib** (`json`, `urllib`, `uuid`, `hashlib`,
  `unittest`, `http.server` para el mock del cliente). `pytest` NO está
  instalado en este entorno y Node no aporta nada para manipular JSON FHIR;
  stdlib evita instalar dependencias y que el componente dependa de la red.
  Tests con `unittest` (stdlib): `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  o `sh run_tests.sh`.
- **Datos sintéticos siempre** (SYN-URG-001/002, RUN ficticios). Nada de datos
  reales en código, ejemplos, tests ni README.
- **Goldens**: copias textuales de los JSON compilados por SUSHI en
  `05-implementation-guide/fsh-generated/resources/` (14 ejemplos + 3 Bundles),
  en `06-component/tests/goldens/`. La comparación pasa por `tests/golden.py`,
  que normaliza SOLO lo documentado en las Rulings de `state.md` (quitar `id`
  y `meta` del lado del golden; normalizar el RUN; normalizar los `fullUrl`
  `urn:uuid:`; añadir el identificador local y el `contentType` que la regla
  exige). Nunca se edita el golden para que pase el test.
- **Referencias**: los builders emiten referencias lógicas
  (`Patient/ejemplo-paciente`, como los ejemplos compilados). El ensamblador
  de Bundle (`bundles.py`) las reescribe a los `fullUrl` `urn:uuid:` de las
  entradas (regla de la guía; Ruling en `state.md`). Los recursos dentro de un
  Bundle se emiten SIN `Resource.id` (la guía: "sin `Resource.id` en el PUT").
- **RUN**: validación estricta del DV chileno (PI-0: DV inválido → se rechaza).
  Los ejemplos del componente usan RUN con DV válido (`12345678-5` paciente,
  `98765432-5` profesional). Los RUN de la guía (`12345678-9`, `98765432-1`)
  tienen DV inválido y se normalizan en la comparación de goldens (Ruling).
- **Identificadores locales**: los PUT condicionales de Condition,
  MedicationRequest y DocumentReference exigen un `identifier` que los ejemplos
  de la guía no llevan. Los builders aceptan `local_id` y lo incluyen, con los
  sistemas de la guía (`https://his.ejemplo.cl/fhir/sid/diagnostico`,
  `.../medicamento`, `.../documento`) y valor `<DAU>-1` (Ruling).
- **DocumentReference**: el perfil fija `contentType = application/pdf`
  (patternCode en la StructureDefinition); el ejemplo compilado por SUSHI lo
  omite. El builder lo pone siempre (Ruling).
- **Git**: la carpeta del caso NO es un checkout git (`git rev-parse` falla).
  Vía remota con las mismas puertas (`git-workflow-health`): no se sube nada
  desde aquí; el push es del usuario con tarjeta. Registrado en `state.md`.

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `06-component/plan.md` | Este plan (descomposición en tareas) |
| `06-component/README.md` | Cómo correr el componente, tests y ejemplos; tabla de trazabilidad operación→código |
| `06-component/run_tests.sh` | `PYTHONPATH=src python3 -m unittest discover -s tests -v` |
| `06-component/src/dau/__init__.py` | Paquete; `__version__ = "0.1.0"` |
| `06-component/src/dau/constants.py` | Sistemas, códigos y ValueSets de la guía |
| `06-component/src/dau/identifiers.py` | Validación del DV del RUN; sistemas de identificadores |
| `06-component/src/dau/patients.py` | Constructor y validador `DAUPaciente` |
| `06-component/src/dau/providers.py` | Constructores `DAUPrestadorOrganizacional` y `DAUPrestadorProfesional` |
| `06-component/src/dau/encounters.py` | Constructores Encounter admisión / alta / abandono + invariantes |
| `06-component/src/dau/conditions.py` | Constructor `DAUDiagnosticoUrgencia` |
| `06-component/src/dau/medications.py` | Constructor `DAUIndicacionMedicamento` |
| `06-component/src/dau/documents.py` | Constructor `DAUDocumentoUrgencia` |
| `06-component/src/dau/bundles.py` | Ensamblador de los 3 Bundles + reescritura de referencias a `urn:uuid:` |
| `06-component/src/dau/identity.py` | PI-0: resultado de la resolución de identidad |
| `06-component/src/dau/search.py` | PI-2: constructores de consultas + `Subscription` |
| `06-component/src/dau/access.py` | PI-3: petición de descarga del PDF |
| `06-component/src/dau/responses.py` | Respuestas del Bus (200/400/412/422) y correcciones |
| `06-component/src/dau/client.py` | Cliente FHIR por `urllib` (POST Bundle, GET, GET PDF) |
| `06-component/src/dau/cli.py` | CLI para correr los ejemplos |
| `06-component/src/dau/validate.py` | Validación de recursos contra los perfiles DAU |
| `06-component/tests/test_*.py` | Tests `unittest`, uno por módulo |
| `06-component/tests/golden.py` | Comparación contra goldens con normalización documentada |
| `06-component/tests/goldens/` | JSON compilados por SUSHI (copias textuales) |
| `06-component/examples/` | Entradas sintéticas JSON por operación |

## Interfaces (contrato entre tareas)

- Entradas: dicts planos con claves `snake_case` (ej. paciente:
  `{run, family, given, gender, birth_date, ficha_local?}`).
- Builders: `build_<recurso>(data: dict) -> dict` (JSON serializable). Incluyen
  `meta.profile` con la canónica del perfil y NO incluyen `id`.
- Validadores: `validate_<recurso>(resource: dict) -> list[str]`; lista vacía
  = válido. Comprueban campos requeridos, cardinalidades, sistemas y códigos
  de los bindings, y los invariantes del perfil.
- `bundles.build_admission_bundle(data)` / `build_discharge_bundle(data)` /
  `build_abandonment_bundle(data)` devuelven el Bundle transacción completo
  (`type=transaction`, `timestamp`, entradas con `fullUrl urn:uuid:`,
  `request.method/url[/ifNoneExist]`, referencias reescritas a `urn:uuid:`).
  Aceptan `uuids: dict | None` para fijar los fullUrl en los tests.
- `search.build_patient_search(run)` etc. devuelven `{"method": "GET",
  "url": "<path>?<query>"}` con los parámetros exactos de operations.md.
- `responses.handle_bus_response(status, body)` devuelve
  `{"outcome": "applied" | "correct_and_resend" | "ambiguous" | "identity_unresolved",
  "detail": ...}` para 200 / 400-422 / 412 / 422.

## Tareas del componente (una operación por tarea)

### Task 1: Andamiaje + identificadores

**Files:**
- Create: `06-component/src/dau/__init__.py`, `constants.py`, `identifiers.py`, `run_tests.sh`, `tests/__init__.py`
- Test: `tests/test_identifiers.py` (unittest)

**Interfaces:**
- Consumes: operations.md (sistemas RUN/DAU/DEIS), `04-mapping-table.md`
- Produces: constantes (sistemas, códigos de destino 01–06, tipos de abandono
  1/2, LOINC 59258-4/34111-5); `validate_run(run)` (DV chileno, formato
  `12345678-5`); `dau_system(deis_code)`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError` (no existe `dau.identifiers`)
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: `unittest` en verde; RUN `12345678-5` válido, `12345678-9` inválido
  (DV calculado 5), `98765432-5` válido, `98765432-1` inválido
- [ ] **Step 5: Update `state.md` with `Component Task 1: complete`**

### Task 2: Paciente (DAUPaciente)

**Files:**
- Create: `06-component/src/dau/patients.py`, `tests/test_patients.py`
- Test: golden `Patient-ejemplo-paciente.json` (RUN normalizado, ver Ruling)

**Interfaces:**
- Consumes: Task 1, perfil `DAUPaciente` (identifier RUN 1..1 sistema RUN,
  name, gender 1..1, birthDate; NN: fichaLocal tipo 12 use temp, gender unknown)
- Produces: `build_patient(data)`, `validate_patient(resource)`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; el paciente SYN-URG-001 coincide con el golden salvo el
  RUN (normalizado) y `id`/`meta` (quitado del lado del golden); sin RUN o con
  DV inválido, `validate_patient` devuelve errores
- [ ] **Step 5: Update `state.md` with `Component Task 2: complete`**

### Task 3: Prestadores (Organización + Profesional)

**Files:**
- Create: `06-component/src/dau/providers.py`, `tests/test_providers.py`
- Test: goldens `Organization-ejemplo-establecimiento.json`,
  `Practitioner-ejemplo-profesional.json` (RUN normalizado)

**Interfaces:**
- Consumes: Task 1, perfiles `DAUPrestadorOrganizacional` (identifier DEIS
  1..1, name 1..1) y `DAUPrestadorProfesional` (identifier RUN 1..1, name 1..1)
- Produces: `build_organization(data)`, `build_practitioner(data)`,
  `validate_organization(resource)`, `validate_practitioner(resource)`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; ambos coinciden con sus goldens salvo `id`/`meta` y el
  RUN del profesional (normalizado)
- [ ] **Step 5: Update `state.md` with `Component Task 3: complete`**

### Task 4: Encuentro de admisión (DAUEncuentroUrgencia)

**Files:**
- Create: `06-component/src/dau/encounters.py`, `tests/test_encounters.py`
- Test: golden `Encounter-ejemplo-encuentro-admision.json`

**Interfaces:**
- Consumes: Tasks 1–3, perfil `DAUEncuentroUrgencia` (identifier DAU 1..*,
  status 1..1, class EMER, subject/serviceProvider 1..1, participant ATND
  con period.start, period.start 1..1, reasonCode.text ≤ 200)
- Produces: `build_admission_encounter(data)`, `validate_encounter(resource)`
  (invariantes `dau-enc-period`, `dau-enc-reason`)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo `id`/`meta`; `period.end`
  anterior a `period.start` y `reasonCode.text` de 201 caracteres dan error
- [ ] **Step 5: Update `state.md` with `Component Task 4: complete`**

### Task 5: Encuentro de alta (DAUEncuentroUrgenciaAlta)

**Files:**
- Create: `06-component/src/dau/encounters.py` (variante alta),
  `tests/test_encounters.py` (casos de alta)
- Test: golden `Encounter-ejemplo-encuentro-alta.json`

**Interfaces:**
- Consumes: Task 4, perfil alta (status finished, dischargeDisposition 1..1
  binding `DAUDestinoAlta` 01–06, diagnosis 1..* con use DD, period.end 1..1,
  invariante `dau-alta-destino`)
- Produces: `build_discharge_encounter(data)`, validación de la variante

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError` (no existe `build_discharge_encounter`)
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo `id`/`meta`; destino 07 da
  error; destino 01 sin `destination` da error; sin diagnosis con use DD da error
- [ ] **Step 5: Update `state.md` with `Component Task 5: complete`**

### Task 6: Encuentro de abandono (DAUEncuentroUrgenciaAbandono)

**Files:**
- Create: `06-component/src/dau/encounters.py` (variante abandono),
  `tests/test_encounters.py` (casos de abandono)
- Test: golden `Encounter-ejemplo-encuentro-abandono.json`

**Interfaces:**
- Consumes: Task 4, perfil abandono (status finished, extensión tipoAbandono
  1..1 (1 NEA / 2 fuga), diagnosis 0..* sin use, period.end 1..1,
  dischargeDisposition 0..0, destination 0..0)
- Produces: `build_abandonment_encounter(data)`, validación de la variante

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo `id`/`meta`; tipo 3 da
  error; con dischargeDisposition da error
- [ ] **Step 5: Update `state.md` with `Component Task 6: complete`**

### Task 7: Diagnóstico (DAUDiagnosticoUrgencia)

**Files:**
- Create: `06-component/src/dau/conditions.py`, `tests/test_conditions.py`
- Test: goldens `Condition-ejemplo-diagnostico-egreso.json`,
  `Condition-ejemplo-hipotesis.json`

**Interfaces:**
- Consumes: Tasks 1 y 4, perfil `DAUDiagnosticoUrgencia` (clinicalStatus y
  verificationStatus 1..1, code 1..1 CIE-10/SNOMED/texto, subject y encounter
  1..1, recordedDate)
- Produces: `build_condition(data)`, `validate_condition(resource)`; acepta
  `local_id` y lo incluye (Ruling: PUT condicional)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; ambos coinciden con sus goldens salvo `id`/`meta` y el
  identificador local añadido; código sin sistema da error
- [ ] **Step 5: Update `state.md` with `Component Task 7: complete`**

### Task 8: Medicamento (DAUIndicacionMedicamento)

**Files:**
- Create: `06-component/src/dau/medications.py`, `tests/test_medications.py`
- Test: golden `MedicationRequest-ejemplo-medicamento-alta.json`

**Interfaces:**
- Consumes: Tasks 1 y 4, perfil `DAUIndicacionMedicamento` (status active,
  intent order, medication[x] CodeableConcept 1..1, subject y encounter 1..1)
- Produces: `build_medication_request(data)`, `validate_medication_request(resource)`;
  acepta `local_id` (Ruling: PUT condicional)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo `id`/`meta` y el
  identificador local añadido; sin `medicationCodeableConcept` da error
- [ ] **Step 5: Update `state.md` with `Component Task 8: complete`**

### Task 9: Documento (DAUDocumentoUrgencia)

**Files:**
- Create: `06-component/src/dau/documents.py`, `tests/test_documents.py`
- Test: goldens `DocumentReference-ejemplo-documento-alta.json`,
  `DocumentReference-ejemplo-documento-abandono.json`

**Interfaces:**
- Consumes: Tasks 1 y 4, perfil `DAUDocumentoUrgencia` (status current,
  type 1..1 LOINC 59258-4 o 34111-5, subject y context.encounter 1..1,
  content.attachment.url 1..1, contentType application/pdf, date 1..1)
- Produces: `build_document_reference(data)`, `validate_document_reference(resource)`;
  acepta `local_id` (Ruling: PUT condicional); `contentType` siempre
  `application/pdf` (Ruling: el perfil lo fija, el ejemplo compilado lo omite)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; ambos coinciden con sus goldens salvo `id`/`meta`, el
  identificador local y el `contentType` añadidos; LOINC distinto de 59258-4 /
  34111-5 da error
- [ ] **Step 5: Update `state.md` with `Component Task 9: complete`**

### Task 10: Bundle de admisión (PI-1)

**Files:**
- Create: `06-component/src/dau/bundles.py`, `tests/test_bundles.py`
- Test: golden `Bundle-ejemplo-bundle-admision.json`

**Interfaces:**
- Consumes: Tasks 2–4, perfil `DAUBundleAviso` (type transaction, timestamp,
  entry `fullUrl urn:uuid:`, request.method/url[/ifNoneExist])
- Produces: `build_admission_bundle(data, uuids=None)`; POST de los maestros
  con `ifNoneExist`, PUT condicional del Encounter por ID DAU; reescribe las
  referencias internas a los `fullUrl urn:uuid:` (Ruling); entradas SIN `id`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo `id`/`meta`, RUN
  normalizados y referencias reescritas a `urn:uuid:`; ningún `subject` queda
  como `Patient/ejemplo-paciente`
- [ ] **Step 5: Update `state.md` with `Component Task 10: complete`**

### Task 11: Bundle de alta (PI-1)

**Files:**
- Create: `06-component/src/dau/bundles.py` (variante alta),
  `tests/test_bundles.py` (casos de alta)
- Test: golden `Bundle-ejemplo-bundle-alta.json`

**Interfaces:**
- Consumes: Tasks 5, 7, 8, 9, 10, perfil `DAUBundleAviso`
- Produces: `build_discharge_bundle(data, uuids=None)`; 4 PUT condicionales
  (Encounter, Condition, MedicationRequest, DocumentReference)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo lo normalizado (Rulings);
  sin medicamento, el Bundle tiene 3 entradas
- [ ] **Step 5: Update `state.md` with `Component Task 11: complete`**

### Task 12: Bundle de abandono (PI-1)

**Files:**
- Create: `06-component/src/dau/bundles.py` (variante abandono),
  `tests/test_bundles.py` (casos de abandono)
- Test: golden `Bundle-ejemplo-bundle-abandono.json`

**Interfaces:**
- Consumes: Tasks 6, 7, 9, 10, perfil `DAUBundleAviso`
- Produces: `build_abandonment_bundle(data, uuids=None)`; 3 PUT condicionales
  (Encounter, Condition hipótesis, DocumentReference)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; coincide con el golden salvo lo normalizado (Rulings)
- [ ] **Step 5: Update `state.md` with `Component Task 12: complete`**

### Task 13: PI-0 — Identidad del paciente

**Files:**
- Create: `06-component/src/dau/identity.py`, `tests/test_identity.py`
- Test: casos de operations.md (DV inválido, no encontrada, duplicada, MPI caído)

**Interfaces:**
- Consumes: Task 1 (`validate_run`), operations.md PI-0 (PIXm parcial, la
  resolución ocurre dentro del Bus; el HIS no llama a PIXm)
- Produces: `resolve_identity(run, mpi_result)` →
  `resolved` | `rejected_invalid_run` | `created` | `rejected_to_reconciliation` |
  `transient_error`; sin llamadas de red (la resolución es del Bus)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; los 5 casos de PI-0 dan el resultado que la guía dice
- [ ] **Step 5: Update `state.md` with `Component Task 13: complete`**

### Task 14: PI-2 — Buscar paciente (PDQm)

**Files:**
- Create: `06-component/src/dau/search.py`, `tests/test_search.py`
- Test: `GET /Patient?identifier=<sistema RUN>|<RUN>`

**Interfaces:**
- Consumes: Task 1, operations.md PI-2 (PDQm parcial, ITI-78/ITI-119)
- Produces: `build_patient_search(run)` → `{"method": "GET", "url": ...}`;
  RUN con DV inválido → error antes de construir la consulta

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; la URL es exactamente
  `Patient?identifier=urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-5`
- [ ] **Step 5: Update `state.md` with `Component Task 14: complete`**

### Task 15: PI-2 — Buscar episodios (QEDm)

**Files:**
- Create: `06-component/src/dau/search.py` (buscar episodios),
  `tests/test_search.py` (casos de episodios)
- Test: `GET /Encounter?patient.identifier=...&class=EMER` y
  `GET /Encounter?service-provider.identifier=...&class=EMER&status=arrived`

**Interfaces:**
- Consumes: Task 1, operations.md PI-2 (QEDm parcial, PCC-44)
- Produces: `build_encounter_search_by_patient(run)`,
  `build_encounter_search_by_provider(deis_code)`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; ambas URLs exactas según operations.md
- [ ] **Step 5: Update `state.md` with `Component Task 15: complete`**

### Task 16: PI-2 — Buscar diagnósticos (QEDm)

**Files:**
- Create: `06-component/src/dau/search.py` (buscar diagnósticos),
  `tests/test_search.py`
- Test: `GET /Condition?encounter=Encounter/[id]`

**Interfaces:**
- Consumes: operations.md PI-2 (QEDm parcial, PCC-44)
- Produces: `build_condition_search(encounter_id)`; `encounter_id` vacío → error

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; URL exacta
- [ ] **Step 5: Update `state.md` with `Component Task 16: complete`**

### Task 17: PI-2 — Buscar documento (MHD ITI-67)

**Files:**
- Create: `06-component/src/dau/search.py` (buscar documento),
  `tests/test_search.py`
- Test: `GET /DocumentReference?encounter=Encounter/[id]`

**Interfaces:**
- Consumes: operations.md PI-2 (MHD parcial, ITI-67)
- Produces: `build_document_search(encounter_id)`; `encounter_id` vacío → error

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; URL exacta
- [ ] **Step 5: Update `state.md` with `Component Task 17: complete`**

### Task 18: PI-2 — Suscripción (Subscription FHIR)

**Files:**
- Create: `06-component/src/dau/search.py` (suscripción),
  `tests/test_search.py`
- Test: `Subscription` sobre `Encounter class=EMER`

**Interfaces:**
- Consumes: operations.md PI-2 (sin perfil IHE: es Subscription FHIR, no DSUB)
- Produces: `build_encounter_subscription(channel_type, endpoint)`; `criteria`
  = `Encounter?class=EMER`; `status` = `requested`; el canal es un detalle de
  implementación y se pasa como parámetro

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `AttributeError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; criteria, status y canal correctos; canal no soportado
  (`email`) → error explícito
- [ ] **Step 5: Update `state.md` with `Component Task 18: complete`**

### Task 19: PI-3 — Acceso al PDF del DAU (MHD ITI-68)

**Files:**
- Create: `06-component/src/dau/access.py`, `tests/test_access.py`
- Test: descarga por `DocumentReference.content.attachment.url`, autenticada

**Interfaces:**
- Consumes: Task 9, operations.md PI-3 (MHD parcial: el patrón es ITI-68 pero
  el mecanismo es un GET autenticado directo a la URL, no una transacción ITI-68)
- Produces: `build_pdf_download(document_reference, token)` →
  `{"method": "GET", "url": <attachment.url>, "headers": {"Authorization":
  "Bearer <token>"}}`; sin `attachment.url` → error; sin token → error

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; URL y cabecera exactas para el documento de alta y el
  de abandono
- [ ] **Step 5: Update `state.md` with `Component Task 19: complete`**

### Task 20: Respuestas del Bus y correcciones (PI-1)

**Files:**
- Create: `06-component/src/dau/responses.py`, `tests/test_responses.py`
- Test: 200, 400, 412, 422 y corrección con `entered-in-error`

**Interfaces:**
- Consumes: operations.md PI-1 (respuestas y corrección)
- Produces: `handle_bus_response(status, body)` →
  `applied` (200) | `correct_and_resend` (400/422 OperationOutcome) |
  `ambiguous` (412) | `identity_unresolved` (422 MPI);
  `build_correction_encounter(encounter)` → Encounter con
  `status = entered-in-error`; `admission_for_closed_episode` → error (nunca
  se envía la admisión de un episodio ya cerrado)

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; cada código da el resultado que la guía dice; la
  corrección conserva el ID DAU y cambia solo el status
- [ ] **Step 5: Update `state.md` with `Component Task 20: complete`**

### Task 21: Cliente HTTP + CLI + ejemplos + README

**Files:**
- Create: `06-component/src/dau/client.py`, `06-component/src/dau/cli.py`,
  `06-component/examples/*.json`, `06-component/README.md`
- Test: cliente contra un mock local (`http.server`); CLI con los 3 ejemplos

**Interfaces:**
- Consumes: Tasks 10–20
- Produces: `DauClient(base_url, token)` (POST Bundle, GET búsqueda, GET PDF,
  con `urllib`); CLI `python3 -m dau.cli <operación> <entrada.json>` que
  escribe el JSON resultante; `examples/` con una entrada sintética por
  operación; README con prerrequisitos, comandos, configuración, cómo correr
  los tests y la tabla de trazabilidad operación→código

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails**
  Expected: FAIL con `ModuleNotFoundError`
- [ ] **Step 3: Write the minimal code**
- [ ] **Step 4: Run the tests to verify they pass**
  Expected: en verde; el cliente POSTea el Bundle al mock y devuelve la
  respuesta; la CLI genera los 3 Bundles y las 5 consultas desde `examples/`
- [ ] **Step 5: Update `state.md` with `Component Task 21: complete`**
