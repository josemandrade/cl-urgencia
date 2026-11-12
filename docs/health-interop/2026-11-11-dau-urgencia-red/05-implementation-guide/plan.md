# Plan — Guía de Implementación (paso 5)

Caso: aviso mínimo de atención de urgencia a la red (DAU). Fuente de verdad: `04-fhir-proposal.md` y `04-mapping-table.md` (validados 2026-11-11). La guía se construye en FSH y se compila con SUSHI (v3.21.0 en este entorno).

## Decisiones del plan

- La guía es una **guía de prueba** para este caso, no la guía del MINSAL. Su `id` es `hl7.fhir.uv.test.dau-urgencia-red`, versión `0.1.0`, y su canonical es `https://josemandrade.github.io/cl-urgencia/` (el sitio de GitHub Pages del repo cl-urgencia, donde el workflow despliega la guía). El id usa el reino `uv` (y no `cl`) porque la plantilla `hl7.base.template` solo acepta los reinos `us`, `uv` y `eu` en el id, y la plantilla genérica `fhir.base.template` necesita Jekyll, que no está en el runner de GitHub.
- Los perfiles se definen **en local** y se basan en los perfiles de la guía cl-urgencia v0.2.0, con nombres propios (`DAUEncuentroUrgencia`, no `EncuentroUrgencia`) para no reclamar ser los perfiles del MINSAL. No se depende del paquete de la guía del MINSAL ni de CL-Core, porque no están publicados como paquetes FHIR que SUSHI pueda resolver; la única dependencia es `hl7.fhir.r4.core 4.0.1`. Las restricciones de la guía v0.2.0 se transcriben en los perfiles locales y se citan como fuente.
- Java no está disponible en este entorno, así que el IG Publisher no corre en local. La validación local es SUSHI (compila el FSH y valida los ejemplos contra sus perfiles). La validación completa con el IG Publisher corre en el workflow de Git (Task 18).
- Los ejemplos son sintéticos (SYN-URG-001, RUN ficticios). Nunca datos reales.

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `05-implementation-guide/sushi-config.yaml` | Identidad, versión, dependencias, páginas |
| `05-implementation-guide/ig.ini` | Entrada del IG Publisher / Auto-IG Builder |
| `05-implementation-guide/input/fsh/valuesets.fsh` | ValueSet y CodeSystem de destino al alta |
| `05-implementation-guide/input/fsh/extensions.fsh` | Extensiones (tipo de abandono, previsión, etc.) |
| `05-implementation-guide/input/fsh/encounter.fsh` | Perfiles EncuentroUrgencia, Alta y Abandono |
| `05-implementation-guide/input/fsh/patient.fsh` | Perfil Paciente |
| `05-implementation-guide/input/fsh/organization.fsh` | Perfil Organización |
| `05-implementation-guide/input/fsh/practitioner.fsh` | Perfil Profesional |
| `05-implementation-guide/input/fsh/condition.fsh` | Perfil Diagnóstico |
| `05-implementation-guide/input/fsh/medicationrequest.fsh` | Perfil Indicación de medicamento |
| `05-implementation-guide/input/fsh/documentreference.fsh` | Perfil Documento + ValueSet de tipo de documento |
| `05-implementation-guide/input/fsh/bundle.fsh` | Perfil Bundle de aviso |
| `05-implementation-guide/input/fsh/examples.fsh` | Ejemplos sintéticos (instancias) |
| `05-implementation-guide/input/pagecontent/index.md` | Caso de uso, usuarios, roles, puntos de interoperabilidad |
| `05-implementation-guide/input/pagecontent/operations.md` | Operaciones en cada punto de interoperabilidad |
| `05-implementation-guide/input/pagecontent/mapping.md` | Mapeo de datos a recursos, campo a campo |
| `05-implementation-guide/input/pagecontent/profiles.md` | Perfiles involucrados |
| `.github/workflows/ig-build.yml` | Workflow de Git (raíz del repo cl-urgencia) |

### Task 1: Andamiaje de la guía

**Files:**
- Create: `05-implementation-guide/sushi-config.yaml`, `05-implementation-guide/ig.ini`, `05-implementation-guide/input/pagecontent/index.md`
- Test: `sushi .` compila sin errores

**Interfaces:**
- Consumes: la propuesta validada (`04-fhir-proposal.md`), el caso de uso (`01-use-case-spec.md`)
- Produces: la carpeta de la guía con su identidad (id `hl7.fhir.uv.test.dau-urgencia-red`, versión `0.1.0`, FHIR R4 4.0.1, dependencia solo `hl7.fhir.r4.core`)

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with `sushi: command not found` o la carpeta no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 1: complete`**

### Task 2: ValueSet y CodeSystem de destino al alta

**Files:**
- Create: `05-implementation-guide/input/fsh/valuesets.fsh`
- Test: `sushi .` compila; el ValueSet contiene los 6 códigos (01–06)

**Interfaces:**
- Consumes: la tabla de mapeo (`04-mapping-table.md`), el ValueSet "Destino al alta de urgencia" de la guía v0.2.0
- Produces: `DAUDestinoAlta` (CodeSystem) y `DAUDestinoAlta` (ValueSet), con 01 Hospitalización, 02 Traslado, 03 Fallecido, 04 Derivación, 05 Domicilio, 06 Otro

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el ValueSet no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 2: complete`**

### Task 3: Extensiones

**Files:**
- Create: `05-implementation-guide/input/fsh/extensions.fsh`
- Test: `sushi .` compila; las 7 extensiones existen con su `url` y su `value[x]`

**Interfaces:**
- Consumes: la propuesta (sección 3, extensiones del Encounter)
- Produces: `DAUTipoAbandono` (con su CodeSystem 1 NEA / 2 fuga), `DAUPrevision`, `DAULeyPrevisional`, `DAUClasificacionConsulta`, `DAUPronosticoMedicoLegal`, `DAUPertinencia`, `DAUMedioLlegada`

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with las extensiones no existen
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 3: complete`**

### Task 4: Perfil EncuentroUrgencia

**Files:**
- Create: `05-implementation-guide/input/fsh/encounter.fsh` (perfil base)
- Test: `sushi .` compila; el ejemplo de admisión valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 2 y 3), las extensiones de la Task 3
- Produces: `DAUEncuentroUrgencia` (Encounter): identifier ID DAU 1..1, status 1..1, class = EMER, subject/serviceProvider 1..1, participant ATND/DIS, period.start 1..1, reasonCode, diagnosis, hospitalization.destination, invariantes `period.end ≥ period.start` y `reasonCode.text ≤ 200`

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 4: complete`**

### Task 5: Perfil EncuentroUrgenciaAlta

**Files:**
- Create: `05-implementation-guide/input/fsh/encounter.fsh` (variante alta)
- Test: `sushi .` compila; el ejemplo de alta valida contra el perfil

**Interfaces:**
- Consumes: `DAUEncuentroUrgencia` (Task 4), `DAUDestinoAlta` (Task 2)
- Produces: `DAUEncuentroUrgenciaAlta` (Encounter, padre `DAUEncuentroUrgencia`): status = finished, dischargeDisposition 1..1 (binding requerido a `DAUDestinoAlta`), diagnosis 1..* con use = DD, period.end 1..1, invariante: si el destino es 01/02/04, `hospitalization.destination` debe estar presente

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 5: complete`**

### Task 6: Perfil EncuentroUrgenciaAbandono

**Files:**
- Create: `05-implementation-guide/input/fsh/encounter.fsh` (variante abandono)
- Test: `sushi .` compila; el ejemplo de abandono valida contra el perfil

**Interfaces:**
- Consumes: `DAUEncuentroUrgencia` (Task 4), `DAUTipoAbandono` (Task 3)
- Produces: `DAUEncuentroUrgenciaAbandono` (Encounter, padre `DAUEncuentroUrgencia`): status = finished, extensión `tipoAbandono` 1..1, diagnosis 0..* (hipótesis provisional, sin use), period.end 1..1, dischargeDisposition 0..0, hospitalization.destination 0..0

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 6: complete`**

### Task 7: Perfil Paciente

**Files:**
- Create: `05-implementation-guide/input/fsh/patient.fsh`
- Test: `sushi .` compila; el ejemplo de paciente valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, Patient), la tabla de mapeo (RUN, NN)
- Produces: `DAUPaciente` (Patient): identifier RUN 1..1 (sistema `urn:oid:2.16.840.1.113883.2.22.1.152.787300`), identifier ficha local para NN (tipo 12, use temp), name, gender 1..1, birthDate, deceased[x]

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 7: complete`**

### Task 8: Perfil Prestador Organizacional

**Files:**
- Create: `05-implementation-guide/input/fsh/organization.fsh`
- Test: `sushi .` compila; el ejemplo de establecimiento valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, Organization)
- Produces: `DAUPrestadorOrganizacional` (Organization): identifier 1..1 (sistema CSEstablecimientoDestino, valor = código DEIS), name 1..1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 8: complete`**

### Task 9: Perfil Prestador Profesional

**Files:**
- Create: `05-implementation-guide/input/fsh/practitioner.fsh`
- Test: `sushi .` compila; el ejemplo de profesional valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, Practitioner)
- Produces: `DAUPrestadorProfesional` (Practitioner): identifier RUN 1..1, name 1..1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 9: complete`**

### Task 10: Perfil Diagnóstico de urgencia

**Files:**
- Create: `05-implementation-guide/input/fsh/condition.fsh`
- Test: `sushi .` compila; el ejemplo de diagnóstico valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, Condition)
- Produces: `DAUDiagnosticoUrgencia` (Condition): clinicalStatus 1..1, verificationStatus 1..1 (provisional/confirmed), code 1..1 (CIE-10 preferente, SNOMED o texto), subject 1..1, encounter 1..1, recordedDate

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 10: complete`**

### Task 11: Perfil Indicación de medicamento

**Files:**
- Create: `05-implementation-guide/input/fsh/medicationrequest.fsh`
- Test: `sushi .` compila; el ejemplo de medicamento valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, MedicationRequest)
- Produces: `DAUIndicacionMedicamento` (MedicationRequest): status 1..1, intent 1..1, medication[x] 1..1, subject 1..1, encounter 1..1, dosageInstruction

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 11: complete`**

### Task 12: Perfil Documento de urgencia

**Files:**
- Create: `05-implementation-guide/input/fsh/documentreference.fsh`
- Test: `sushi .` compila; el ejemplo de documento valida contra el perfil

**Interfaces:**
- Consumes: la propuesta (sección 3, DocumentReference)
- Produces: `DAUDocumentoUrgencia` (DocumentReference): status 1..1, type 1..1 (LOINC 59258-4 resumen de alta o 34111-5 nota de urgencia, ValueSet `DAUTipoDocumento`), subject 1..1, context.encounter 1..1, content.attachment.url 1..1 (PDF), content.attachment.contentType = application/pdf, date 1..1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 12: complete`**

### Task 13: Perfil Bundle de aviso

**Files:**
- Create: `05-implementation-guide/input/fsh/bundle.fsh`
- Test: `sushi .` compila; los ejemplos de Bundle validan contra el perfil

**Interfaces:**
- Consumes: todos los perfiles (Tasks 4–12), la propuesta (sección 2, Bundle)
- Produces: `DAUBundleAviso` (Bundle): type = transaction, entry 1..* (fullUrl `urn:uuid:`, request.method, request.url con la operación condicional), timestamp

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el perfil no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 13: complete`**

### Task 14: Operación de admisión (Bundle + ejemplo)

**Files:**
- Create: `05-implementation-guide/input/fsh/examples.fsh` (instancias de admisión), `05-implementation-guide/input/pagecontent/operations.md` (sección admisión)
- Test: `sushi .` compila; el Bundle de admisión valida contra `DAUBundleAviso`

**Interfaces:**
- Consumes: `DAUBundleAviso` (Task 13), los perfiles de maestros y del Encounter (Tasks 4, 7, 8, 9)
- Produces: el ejemplo `ejemplo-bundle-admision` (transacción: POST de los maestros con `ifNoneExist`, PUT condicional del Encounter por ID DAU, status arrived) y la descripción de la operación en PI-1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el ejemplo no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 14: complete`**

### Task 15: Operación de alta (Bundle + ejemplo)

**Files:**
- Create: `05-implementation-guide/input/fsh/examples.fsh` (instancias de alta), `05-implementation-guide/input/pagecontent/operations.md` (sección alta)
- Test: `sushi .` compila; el Bundle de alta valida contra `DAUBundleAviso`

**Interfaces:**
- Consumes: `DAUBundleAviso` (Task 13), `DAUEncuentroUrgenciaAlta` (Task 5), `DAUDiagnosticoUrgencia` (Task 10), `DAUIndicacionMedicamento` (Task 11), `DAUDocumentoUrgencia` (Task 12)
- Produces: el ejemplo `ejemplo-bundle-alta` (transacción: Encounter finished con destino 03 Fallecido, Condition causa de muerte I46.9 con use DD, DocumentReference resumen de alta LOINC 59258-4) y la descripción de la operación en PI-1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el ejemplo no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 15: complete`**

### Task 16: Operación de abandono (Bundle + ejemplo)

**Files:**
- Create: `05-implementation-guide/input/fsh/examples.fsh` (instancias de abandono), `05-implementation-guide/input/pagecontent/operations.md` (sección abandono)
- Test: `sushi .` compila; el Bundle de abandono valida contra `DAUBundleAviso`

**Interfaces:**
- Consumes: `DAUBundleAviso` (Task 13), `DAUEncuentroUrgenciaAbandono` (Task 6), `DAUDocumentoUrgencia` (Task 12)
- Produces: el ejemplo `ejemplo-bundle-abandono` (transacción: Encounter finished con tipo de abandono 2 fuga, Condition hipótesis provisional, DocumentReference nota de urgencia LOINC 34111-5) y la descripción de la operación en PI-1

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with el ejemplo no existe
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 16: complete`**

### Task 17: Páginas de la guía (perfiles, mapeo, índice final)

**Files:**
- Create: `05-implementation-guide/input/pagecontent/profiles.md`, `05-implementation-guide/input/pagecontent/mapping.md`, `05-implementation-guide/input/pagecontent/index.md` (contenido final)
- Test: `sushi .` compila; las páginas aparecen en el `ImplementationGuide` generado

**Interfaces:**
- Consumes: todos los perfiles y ejemplos (Tasks 2–16), la tabla de mapeo (`04-mapping-table.md`), el diagrama (`04-fhir-proposal-graph.svg`)
- Produces: las páginas narrativas de la guía (caso de uso, perfiles, operaciones, mapeo campo a campo con qué pasa si el dato falta o es ambiguo)

- [x] **Step 1: Write the failing test**
- [x] **Step 2: Run the test to verify it fails**
  Expected: FAIL with las páginas no existen
- [x] **Step 3: Write the minimal FSH and code**
- [x] **Step 4: Run SUSHI and the tests to verify they pass**
  Expected: SUSHI compiles with no errors, tests PASS
- [x] **Step 5: Update `state.md` with `Task 17: complete`**

### Task 18: CI/CD de la guía (workflow de Git + Auto-IG Builder)

**Files:**
- Create: `.github/workflows/ig-build.yml` (raíz del repo cl-urgencia, no dentro de `05-implementation-guide/`)
- Test: el workflow en sí — un push que construye en verde, y un push con un FSH roto que construye en rojo

**Interfaces:**
- Consumes: la carpeta `05-implementation-guide/` (con `sushi-config.yaml` e `ig.ini`), los perfiles y ejemplos validados
- Produces: un workflow que valida la guía con SUSHI + IG Publisher en cada push/PR y la despliega a GitHub Pages desde `main`. La IG está en subcarpeta, así que el servicio Auto-IG Builder no se puede usar (exige la IG en la raíz de un repo público); el workflow es la vía de despliegue. Activar GitHub Pages en el repo (Settings → Pages → Source: GitHub Actions).

- [x] **Step 1: Write the workflow file**
- [x] **Step 2: Push it to a branch and open a pull request — the workflow must run and pass**
  Expected: the build job is green; `qa.tgz` is uploaded as an artifact
- [x] **Step 3: Break one FSH file on purpose and push — the workflow must fail and not deploy**
  Expected: the build job is red; the deploy job never runs
- [x] **Step 4: Revert the break, merge to `main`, and confirm the deploy**
  Expected: the site is live at `https://josemandrade.github.io/cl-urgencia/` 
- [x] **Step 5: Update `state.md` with `Task 18: complete`**
