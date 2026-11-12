# Diagramas de secuencia — Operaciones en el tiempo, flujo por flujo

Las operaciones son una lista; un diagrama de secuencia las muestra en el tiempo: quién llama a quién, en qué orden, qué vuelve y qué puede fallar. Cada diagrama cubre **un flujo** del proceso (BPMN v7), y **cada mensaje nombra la operación que lo lleva** (id PI-n, interacción FHIR, perfil IHE cuando uno aplica). Flecha sólida = síncrono (el emisor espera la respuesta); flecha abierta = asíncrono (push sin espera); flecha punteada = retorno, con el resultado que la operación promete. La lista completa de operaciones, con sus transacciones y sus perfiles IHE, está en [Operaciones](operations.html); el detalle por flujo (camino BPMN, participantes, tabla de operaciones) está en [04-sequence-diagrams.md](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/04-sequence-diagrams.md).

Cada diagrama se muestra a su ancho real para que el texto sea legible: desplázate a la derecha con la barra inferior para recorrerlo, y usa Zoom in (+) para acercar y Zoom out (−) para alejar.

## Admisión — publicar el evento de admisión (PI-0 / PI-1)

BPMN v7: Persona llega > ¿Emergencia vital? > Admisión > Crear episodio DAU en el HIS > Publicar evento de admisión (PI-0) > Bus recibe y aplica.

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('seq-admission-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('seq-admission-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('seq-admission-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="04-sequence-admission.png"><img id="seq-admission-img" src="04-sequence-admission.png" alt="Diagrama de secuencia de la admisión" style="width:1280px; max-width:none; height:auto;"/></a>
</div>

También puedes [abrirlo a tamaño completo](04-sequence-admission.png).

| Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|
| 1. HIS/RCE → Bus: `POST /Bundle` (admisión) | [PI-1 Admisión](operations.html) | Ninguno (transacción nacional) | 200 transaction-response |
| 2. Bus → MPI: resolver identidad | [PI-0 Resolver identidad](operations.html) | PIXm ITI-83 | Identidad resuelta (asociada al MPI) |
| 3. MPI → Bus (retorno) | PI-0 Resolver identidad | PIXm ITI-83 | identidad resuelta / no resuelta |
| 4. Bus → Repositorio: aplicar transacción | [PI-1 Admisión](operations.html) — aplicación en el Repositorio | Ninguno (transacción nacional) | aplicado |
| 5. Repositorio → Bus (retorno) | PI-1 Admisión | — | aplicado |
| 6. Bus → HIS/RCE (retorno) | PI-1 Admisión | — | 200 aplicado / 400–422 corregir y reenviar / 412 ambiguo / 422 identidad no resuelta |

C1 (vía rápida): la admisión administrativa corre en paralelo con la atención clínica (puerta AND del BPMN); el aviso se publica cuando el episodio existe en el HIS. Nunca se envía la admisión de un episodio ya cerrado: el PUT lo reabriría.

## Alta — publicar el evento de alta (PI-1)

BPMN v7: Puerta de desenlace > Alta > Indicar medicamentos > Cerrar DAU y generar PDF > Publicar aviso de alta (PI-1) > Bus recibe y aplica.

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('seq-discharge-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('seq-discharge-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('seq-discharge-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="04-sequence-discharge.png"><img id="seq-discharge-img" src="04-sequence-discharge.png" alt="Diagrama de secuencia del alta" style="width:1280px; max-width:none; height:auto;"/></a>
</div>

También puedes [abrirlo a tamaño completo](04-sequence-discharge.png).

| Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|
| 1a. HIS/RCE → Bus: `POST /Bundle` (alta) — alt [alta, destino 01, 02, 04, 05 o 06] | [PI-1 Alta](operations.html) | Ninguno (transacción nacional) | 200 transaction-response |
| 1b. HIS/RCE → Bus: `POST /Bundle` (alta, destino 03) — alt [fallecimiento, destino 03] | [PI-1 Alta](operations.html) | Ninguno (transacción nacional) | 200 transaction-response |
| 2. Bus → MPI: resolver identidad | [PI-0 Resolver identidad](operations.html) | PIXm ITI-83 | Identidad resuelta |
| 3. MPI → Bus (retorno) | PI-0 Resolver identidad | PIXm ITI-83 | identidad resuelta / no resuelta |
| 4. Bus → Repositorio: aplicar transacción | [PI-1 Alta](operations.html) — aplicación en el Repositorio | Ninguno (transacción nacional) | aplicado |
| 5. Repositorio → Bus (retorno) | PI-1 Alta | — | aplicado |
| 6. Bus → HIS/RCE (retorno) | PI-1 Alta | — | 200 aplicado / 400–422 / 412 / 422 |
| 7. HIS/RCE → Bus: `POST /Bundle` (entered-in-error) — opt [si el aviso se envió por error] | [PI-1 Corrección](operations.html) | Ninguno (transacción nacional) | 200 aplicado |
| 8. Bus → HIS/RCE (retorno) | PI-1 Corrección | — | 200 aplicado |

El fallecimiento es un alta con destino `03 Fallecido` (causa de muerte en CIE-10 con `use = DD`, resumen de alta LOINC 59258-4 si existe; sin medicamentos ni establecimiento de destino). La corrección reenvía el `Encounter` con `status = entered-in-error`; nunca se envía la admisión de un episodio ya cerrado.

## Abandono — publicar el evento de abandono (PI-1)

BPMN v7: NEA (después de la admisión, esperando categorización o atención) o fuga (durante la atención) > Constatar abandono > Puerta de desenlace (rama abandono) > Cerrar DAU y generar PDF > Publicar aviso de abandono (PI-1) > Bus recibe y aplica.

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('seq-abandonment-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('seq-abandonment-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('seq-abandonment-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="04-sequence-abandonment.png"><img id="seq-abandonment-img" src="04-sequence-abandonment.png" alt="Diagrama de secuencia del abandono" style="width:1280px; max-width:none; height:auto;"/></a>
</div>

También puedes [abrirlo a tamaño completo](04-sequence-abandonment.png).

| Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|
| 1a. HIS/RCE → Bus: `POST /Bundle` (abandono, NEA) — alt [NEA, tipo 1] | [PI-1 Abandono](operations.html) | Ninguno (transacción nacional) | 200 transaction-response |
| 1b. HIS/RCE → Bus: `POST /Bundle` (abandono, fuga) — alt [fuga, tipo 2] | [PI-1 Abandono](operations.html) | Ninguno (transacción nacional) | 200 transaction-response |
| 2. Bus → MPI: resolver identidad | [PI-0 Resolver identidad](operations.html) | PIXm ITI-83 | Identidad resuelta |
| 3. MPI → Bus (retorno) | PI-0 Resolver identidad | PIXm ITI-83 | identidad resuelta / no resuelta |
| 4. Bus → Repositorio: aplicar transacción | [PI-1 Abandono](operations.html) — aplicación en el Repositorio | Ninguno (transacción nacional) | aplicado |
| 5. Repositorio → Bus (retorno) | PI-1 Abandono | — | aplicado |
| 6. Bus → HIS/RCE (retorno) | PI-1 Abandono | — | 200 aplicado / 400–422 / 412 / 422 |

NEA: el paciente nunca fue atendido (sin hipótesis ni medicamentos; el PDF puede no existir). Fuga: hipótesis provisional (sin `use`) y nota de urgencia (LOINC 34111-5). El aviso de abandono repite todos los datos de la admisión: el PUT reemplaza el `Encounter` completo; un dato omitido se borra del repositorio.

## Consulta de la red — pull del Repositorio y suscripción (PI-2)

BPMN v7: Punto de la red > Consultar episodios en el repositorio (o suscribirse) > ¿Necesita el detalle clínico?

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('seq-network-pull-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('seq-network-pull-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('seq-network-pull-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="04-sequence-network-pull.png"><img id="seq-network-pull-img" src="04-sequence-network-pull.png" alt="Diagrama de secuencia de la consulta de la red" style="width:1040px; max-width:none; height:auto;"/></a>
</div>

También puedes [abrirlo a tamaño completo](04-sequence-network-pull.png).

| Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|
| 1. Punto de la red → Repositorio: `GET /Patient?identifier=<RUN>` — alt [consulta puntual] | [PI-2 Buscar paciente](operations.html) | PDQm ITI-78 | Patient |
| 2. Repositorio → Punto de la red (retorno) | PI-2 Buscar paciente | PDQm ITI-78 | Patient |
| 3. Punto de la red → Repositorio: `GET /Encounter?patient.identifier=<RUN>&class=EMER` | [PI-2 Buscar episodios](operations.html) | QEDm PCC-44 | Bundle de Encounter |
| 4. Repositorio → Punto de la red (retorno) | PI-2 Buscar episodios | QEDm PCC-44 | Bundle de Encounter |
| 5. Punto de la red → Repositorio: `GET /Condition?encounter=Encounter/[id]` | [PI-2 Buscar diagnósticos](operations.html) | QEDm PCC-44 | Condition(s) |
| 6. Repositorio → Punto de la red (retorno) | PI-2 Buscar diagnósticos | QEDm PCC-44 | Condition(s) |
| 7. Punto de la red → Repositorio: `GET /DocumentReference?encounter=Encounter/[id]` | [PI-2 Buscar documento](operations.html) | MHD ITI-67 | DocumentReference |
| 8. Repositorio → Punto de la red (retorno) | PI-2 Buscar documento | MHD ITI-67 | DocumentReference |
| 9. Punto de la red → Repositorio: `POST Subscription` (Encounter `class=EMER`) — alt [suscripción] | [PI-2 Suscribirse](operations.html) | Ninguno — Subscription FHIR (DSUB refutado) | 201 Created |
| 10. Repositorio → Punto de la red (retorno) | PI-2 Suscribirse | — | 201 Created |
| 11. Repositorio → Punto de la red: notificación (asíncrono) | [PI-2 Suscribirse](operations.html) | Ninguno — Subscription FHIR | Encounter creado / actualizado |

Buscar episodios también por establecimiento (`GET /Encounter?service-provider.identifier=<sistema DEIS>|<código>&class=EMER&status=arrived`). DSUB no encaja: la suscripción es una `Subscription` FHIR sobre `Encounter class=EMER`, no una suscripción DSUB a metadatos de un registro XDS; el canal de notificación (por ejemplo, REST-hook) es un detalle de implementación.

## Recuperación del DAU en PDF (PI-3)

BPMN v7: Punto de la red > ¿Necesita el detalle clínico? (sí) > Solicitar y recibir DAU en PDF (PI-3) > Seguimiento.

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('seq-document-retrieval-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('seq-document-retrieval-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('seq-document-retrieval-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="04-sequence-document-retrieval.png"><img id="seq-document-retrieval-img" src="04-sequence-document-retrieval.png" alt="Diagrama de secuencia de la recuperación del DAU en PDF" style="width:980px; max-width:none; height:auto;"/></a>
</div>

También puedes [abrirlo a tamaño completo](04-sequence-document-retrieval.png).

| Mensaje | Operación | Perfil IHE | Resultado esperado |
|---|---|---|---|
| 1. Punto de la red → Repositorio: `GET /DocumentReference?encounter=Encounter/[id]` | [PI-2 Buscar documento](operations.html) | MHD ITI-67 | DocumentReference (con `attachment.url`) |
| 2. Repositorio → Punto de la red (retorno) | PI-2 Buscar documento | MHD ITI-67 | DocumentReference (con `attachment.url`) |
| 3. Punto de la red → HIS/RCE: `GET <attachment.url>` (autenticado) | [PI-3 Acceso al PDF](operations.html) | MHD ITI-68 | PDF del DAU |
| 4. HIS/RCE → Punto de la red (retorno) | PI-3 Acceso al PDF | MHD ITI-68 | PDF del DAU |

El PDF se descarga con un GET autenticado directo a `DocumentReference.content.attachment.url`; no es una transacción ITI-68. Si el HIS no está disponible, el PDF no se puede descargar: el Repositorio guarda la referencia, no el documento.

<script>
function zoomDiagram(id, f) {
  var el = document.getElementById(id);
  if (!el) return;
  if (el.dataset.orig === undefined) { el.dataset.orig = el.style.width || ''; el.dataset.origMax = el.style.maxWidth || ''; }
  var w = Math.round(el.clientWidth * f);
  w = Math.max(400, Math.min(8000, w));
  el.style.width = w + 'px';
  el.style.maxWidth = 'none';
}
function resetDiagram(id) {
  var el = document.getElementById(id);
  if (!el) return;
  el.style.width = (el.dataset.orig !== undefined) ? el.dataset.orig : '';
  el.style.maxWidth = (el.dataset.origMax !== undefined) ? el.dataset.origMax : '';
}
</script>
