# Proceso — Modelo BPMN del aviso mínimo DAU

El proceso que publica el aviso mínimo, modelado en BPMN 2.0 (versión 4, validada en el paso 2). Tres participantes (pools), de arriba a abajo: el establecimiento informante — Unidad de Urgencia (con los carriles Admisión / Registro, Categorización / Selector de Demanda, Equipo clínico de Urgencia y HIS / RCE), el Bus de Interoperabilidad MINSAL y Repositorio FHIR, y el punto de la red receptor (APS, especialidad, otro hospital, SAMU).

<div style="margin:8px 0;">
<button type="button" onclick="zoomDiagram('bpmn-img', 1.25)" style="padding:4px 10px; cursor:pointer;">Zoom in (+)</button>
<button type="button" onclick="zoomDiagram('bpmn-img', 0.8)" style="padding:4px 10px; cursor:pointer;">Zoom out (−)</button>
<button type="button" onclick="resetDiagram('bpmn-img')" style="padding:4px 10px; cursor:pointer;">100%</button>
</div>
<div style="overflow:auto; border:1px solid #ddd; padding:8px;">
<a href="02-bpmn-model.png"><img id="bpmn-img" src="02-bpmn-model.png" alt="Modelo BPMN del proceso de aviso mínimo de atención de urgencia a la red" style="width:4320px; max-width:none; height:auto;"/></a>
</div>

El diagrama es ancho (4320 px, su ancho real) y se muestra a ese tamaño para que el texto sea legible: desplázate a la derecha con la barra inferior para recorrerlo, y usa Zoom in (+) para acercar y Zoom out (−) para alejar. También puedes [abrirlo a tamaño completo](02-bpmn-model.png).

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

El diagrama es una imagen (PNG) a tamaño real. El modelo BPMN completo (XML, BPMN 2.0) está en [02-bpmn-model.bpmn](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/02-bpmn-model.bpmn), y su descripción paso a paso en [02-bpmn-model.md](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/02-bpmn-model.md).

## Flujo, paso a paso

1. La persona llega a la urgencia (evento de inicio).
2. Puerta **¿Emergencia vital?**: si es C1, va directo a "Atender clínicamente" (la admisión administrativa se completa en paralelo o después); si no, sigue la admisión.
3. Admisión: recepcionar (llegada y procedencia) → identificar con doble verificador → datos sociodemográficos y previsión → motivo de consulta → aperturar el DAU e instalar el brazalete → crear el episodio DAU en el HIS (ID DAU) → **publicar el evento de admisión a la red (PI-0)** → informar la llegada al Selector de Demanda.
4. Categorización: categorizar (C1–C5) → asignar box.
5. Puerta **¿Categoría?**: C1 → atención inmediata; C2–C5 → esperar atención.
6. **NEA:** si la persona se retira después de la admisión — esperando la categorización o esperando la atención — se constata el abandono (NEA) y el flujo va a la puerta de desenlace por la rama de abandono. El paciente NEA nunca fue atendido: no tiene hipótesis ni medicamentos.
7. Atención clínica → informar al paciente o familiares (si el paciente no puede recibir la información, se hace a familiares). **Fuga:** si la persona se retira durante la atención, se constata el abandono (fuga) y el flujo va a la puerta de desenlace por la rama de abandono.
8. Puerta **¿Cómo termina la atención?** (decisión del Terminador):
   - **Alta** → indicar medicamentos al alta → cerrar el DAU y generar el PDF → publicar el aviso de alta (PI-1) → fin.
   - **Abandono** (NEA o fuga) → cerrar el DAU y generar el PDF → publicar el aviso de abandono (PI-1) → fin. En abandono no hay medicamentos al alta; en NEA, además, pueden no existir hipótesis ni PDF.
   - **Fallecimiento** (extensión del caso, no de la guía) → cerrar el DAU como fallecido y generar el PDF → publicar el aviso de fallecimiento (PI-1) → fin.
9. El Bus recibe cada transacción, la valida y la aplica en el Repositorio FHIR.
10. El punto receptor **consulta los episodios en el repositorio** (PI-2, pull) o está **suscrito** a los cambios de episodio.
11. Puerta **¿Necesita el detalle clínico?**: Sí → solicita el DAU, lo recibe en PDF y hace el seguimiento; No → hace el seguimiento con el aviso. Fin.

El DAU nace en la Admisión (apertura, con su ID DAU) y se cierra en el Egreso (cierre y PDF). Nunca se "genera" antes del desenlace.

## Puntos de interoperabilidad

| Punto | Qué pasa | Datos | Quién | Cuándo | Perfiles IHE |
|---|---|---|---|---|---|
| PI-0 | Publicación del evento de admisión | Bundle de admisión: paciente, establecimiento, fecha/hora de admisión, motivo, procedencia, medio de llegada; episodio abierto (`arrived`), ID DAU | HIS/RCE del establecimiento → Bus de Interoperabilidad MINSAL | Al crear el episodio (admisión) | PIXm, MHD, NAV, ATNA, CT |
| PI-1 | Publicación del evento de alta, abandono o fallecimiento | Bundle de alta, abandono o fallecimiento: el mismo episodio actualizado + fecha/hora de cierre, destino o tipo de abandono o fallecimiento, diagnóstico, medicamentos, referencia al DAU | HIS/RCE del establecimiento → Bus de Interoperabilidad MINSAL | Cierre del episodio de urgencia | PIXm, MHD, XDR, ATNA, CT |
| PI-2 | Consulta de episodios | Búsqueda FHIR (`Encounter?patient.identifier=…&class=EMER` o por establecimiento y estado) o suscripción a los cambios de episodio | Punto de la red receptor → Repositorio FHIR (consulta); Repositorio → receptor (episodios) | El receptor consulta o está suscrito | QEDm, DSUB, MHD, ATNA, CT |
| PI-3 | Recuperación del DAU en PDF | Solicitud del DAU y DAU en PDF (descargado desde `DocumentReference.content.attachment.url`, con autenticación) | Receptor → HIS/RCE (solicitud); HIS/RCE → Receptor (PDF) | El receptor decide que necesita el detalle clínico | MHD, ATNA, CT |

PI-0 y PI-1 son **push** (el establecimiento envía la transacción en el momento del evento); PI-2 es **pull** (la red consulta el repositorio) con la opción de **suscripción** para enterarse del evento apenas ocurre. PI-1 y PI-2 mueven el aviso mínimo; PI-3 mueve el documento completo. El aviso referencia el DAU, no lo copia.

Las operaciones de cada punto, con sus transacciones y sus perfiles IHE, están en [Operaciones](operations.html); la revisión IHE por punto, con el encaje y las brechas, en [Relación con IHE](ihe.html).
