# Validation — dau-urgencia-red

## 2026-11-12 — El BPMN seguía solapado: reorden del modelo (v5) y del render

- Artefact: `02-bpmn-model.bpmn` (v5), `02-bpmn-model.md` (v5), `render_bpmn.py` y las skills `bpmn-modeling` e `implementation-guide-sushi` del pack
- Tool / profile: revisión visual del PNG a tamaño de visualización (4320 px, visto 1:1 por zonas: izquierda — admisión/categorización — y derecha — atención/publicación/red)
- Result: el pantallazo del usuario mostraba "Episodio cerrado / aviso publicado" solapado con "Solicitud de DAU recibida" y con su círculo, y el nudo PI-2/PI-3. Tras la v5, verificado mirando las dos zonas: "Episodio cerrado / aviso publicado" está a la derecha de su círculo y "Solicitud de DAU recibida" debajo del suyo, en filas distintas, sin tocarse; "Transacción recibida", "Episodio disponible en el repositorio" y "Consulta FHIR recibida" ya no se solapan con sus círculos; PI-2 y PI-3 tienen sus etiquetas separadas y legibles. SUSHI compila con 0 errores y 0 warnings. La v5 queda presentada para validación (la v4 fue la validada por el usuario). El PNG nuevo (8640×1620, 528411 bytes) se subió por la web de GitHub (commit 73b8936); el .bpmn/.svg/.md y `render_bpmn.py` se subieron por snapshot (commit 87be126). El pack se subió como v0.13.0 (commit 01dade6). Verificado en vivo (run 43160619603, success): `process.html` muestra el PNG nuevo (200, 528411 bytes), a 4320 px con los botones de zoom y el script `zoomDiagram`, y el grafo de recursos sigue en 200.
- Evidence: PNG a 4320 px mirado 1:1 por zonas (izquierda y derecha); SUSHI v3.21.0 0 errores; run 43160619603 success; curl en vivo a process.html y a los dos PNG.

## 2026-11-12 — El BPMN seguía ilegible: ancho de visualización

- Artefact: `05-implementation-guide/input/pagecontent/process.md` (ancho de la imagen 2400 → 4320 px, nota de desplazamiento) y las skills `bpmn-modeling` e `implementation-guide-sushi` del pack
- Tool / profile: SUSHI v3.21.0 y revisión visual del BPMN AL TAMAÑO DE VISUALIZACIÓN (el PNG a 4320 px, visto 1:1 por zonas: izquierda y centro)
- Result: la página mostraba el BPMN a 2400 px y el texto quedaba a ~7 px (ilegible). Con el ancho nativo (4320 px) el texto se ve a 12 px y es legible: se verificó mirando las dos zonas a tamaño real (etiquetas de la columna izquierda, tareas de admisión, "Atender clínicamente", "Paciente se retira (fuga)", los PI-0/PI-1/PI-3 y los eventos). SUSHI compila con 0 errores y 0 warnings. Pendiente: subir la página y los registros, verificar el run y la guía en vivo (que `process.html` lleve `width:4320px`), y subir el pack con la skill reparada (v0.12.0).
- Evidence: PNG a 4320 px mirado 1:1 por zonas; SUSHI v3.21.0 0 errores.

## 2026-11-12 — El BPMN se veía muy mal: reparación del render y de la skill

- Artefact: `render_bpmn.py`, `02-bpmn-model.svg`, `02-bpmn-model.png` (2×) y las skills `bpmn-modeling` e `implementation-guide-sushi` del pack
- Tool / profile: render con `render_bpmn.py` reescrito, conversión con cairosvg a 2×, y revisión visual del PNG (vista completa y zonas ampliadas: inferior derecha PI-2, centro-derecha PI-1/Episodio cerrado, y la zona de "Atender clínicamente / Paciente se retira (fuga)")
- Result: el render quedó reparado y se verificó mirándolo: la columna de etiquetas izquierda es legible (pool y lane en horizontal, sin solapamientos), los PI-0/PI-1/PI-2/PI-3 son legibles con fondo blanco, "Episodio cerrado / aviso publicado" ya no se solapa con "Solicitud de DAU recibida", y la etiqueta del evento de borde "Paciente se retira (fuga)" es una sola línea y ya no cae sobre la caja de "Constatar abandono (fuga)". SUSHI compila con 0 errores y 0 warnings. El PNG nuevo (8640×1620, 537 KB) se subió por la web de GitHub (commit fffcd69, "Replace the BPMN PNG with the repaired 2x render"); el SVG y `render_bpmn.py` se subieron por snapshot (commit eef1a6d). El pack se subió como v0.11.0 (commit cee9291) con la skill reparada. Verificado en vivo (run 43159039439, success): `process.html` muestra el PNG nuevo (200, 537264 bytes — antes 230627), con los botones de zoom y el script `zoomDiagram`, y el grafo de recursos sigue en 200.
- Evidence: PNG 8640×1620 mirado completo y por zonas; SUSHI v3.21.0 0 errores; run 43159039439 success; curl en vivo a process.html y a los dos PNG.

## 2026-11-12 — Diagramas como PNG directo, con zoom in / zoom out

- Artefact: `05-implementation-guide/` (PNG nuevos en `input/images/`, `process.md`, `resources.md`, `profiles.md`) y la skill `implementation-guide-sushi` del pack
- Tool / profile: conversión con cairosvg y SUSHI v3.21.0 de los cambios
- Result: los dos SVG se convirtieron a PNG (grafo 2440×1800, 227 KB; BPMN 4080×810, 230 KB) y las tres páginas muestran el PNG directo, con botones Zoom in (+), Zoom out (−) y 100% y el script `zoomDiagram`/`resetDiagram` en cada página. SUSHI compila con 0 errores y 0 warnings; los enlaces internos y las imágenes de las tres páginas se verifican (ninguno roto). Los PNG no se pudieron subir por el snapshot push (solo texto UTF-8, el archivo binario se rechazó): se subieron por la web de GitHub (commit 0356af5, "Add the BPMN and resource diagram PNGs"). Verificado en vivo (run 14, commit 37ee318, success): los dos PNG devuelven 200 en la raíz del sitio, las tres páginas muestran el PNG y el `<script>` con `zoomDiagram` sobrevivió al publisher (está en resources.html, process.html y profiles.html), el menú incluye "Diagrama de recursos" y el header sigue `<ul class="nav navbar-nav">`.
- Evidence: conversión con cairosvg, SUSHI v3.21.0 0 errores, comprobación de enlaces y de script/botones en local; run 14 success; curl en vivo a resources.html, process.html, profiles.html y a los dos PNG.

## 2026-11-12 — El diagrama de recursos tiene su propia página (corrección de la skill)

- Artefact: `05-implementation-guide/` (página nueva `resources.md`, `menu.xml`, `sushi-config.yaml`, `index.md`) y las skills `implementation-guide-sushi` y `fhir-modeling` del pack
- Tool / profile: revisión en vivo de la guía publicada y render del SVG
- Result: verificado que el diagrama SÍ estaba publicado en `profiles.html` (sección "Diagrama de recursos", `<img src="04-fhir-proposal-graph.svg">`, SVG con 200) y que el SVG renderiza bien (render a PNG: grafo legible, Encounter como centro, Bundle como marco, 12 referencias etiquetadas). El problema era de visibilidad: estaba enterrado en la mitad de Perfiles. Corregido: página propia `resources.md` ("Diagrama de recursos") con el diagrama, cómo leerlo y la tabla de recursos y referencias, con entrada propia en el menú (después de "Proceso (BPMN)") y enlazada desde el índice y desde Perfiles. La skill queda corregida: el diagrama tiene su propia página y su propia entrada en el menú, no solo va en Perfiles. SUSHI compila con 0 errores y 0 warnings; los enlaces internos y las imágenes de `resources.md`, `index.md` y `profiles.md` se verifican (ninguno roto). Pendiente: subir a cl-urgencia y verificar el run y la guía en vivo.
- Evidence: lectura en vivo de profiles.html (el `<img>` y la sección presentes), render del SVG a PNG con cairosvg, SUSHI v3.21.0 0 errores, comprobación de enlaces en local.

## 2026-11-12 — Run 12: imágenes del BPMN y del diagrama de recursos cargando, header horizontal

- Artefact: guía publicada en https://josemandrade.github.io/cl-urgencia/
- Tool / profile: GitHub Actions, workflow "IG build", run 12 (commit `fa240d0`)
- Result: success (build y deploy en verde). Verificado en vivo: `process.html` referencia `02-bpmn-model.svg` (por nombre de archivo) y el SVG devuelve 200; `profiles.html` referencia `04-fhir-proposal-graph.svg` y devuelve 200; el header sigue siendo `<ul class="nav navbar-nav">`. Las imágenes ya se ven en la guía.
- Evidence: run de Actions 43157084530 (success), curl 200 de ambos SVG y lectura en vivo de process.html, profiles.html e index.html.

## 2026-11-12 — Run 11: BPMN y diagrama de recursos en la guía y header horizontal (pero las imágenes daban 404)

- Artefact: guía publicada en https://josemandrade.github.io/cl-urgencia/
- Tool / profile: GitHub Actions, workflow "IG build", run 11 (commit `d507886`)
- Result: success (build y deploy en verde). Verificado en vivo: el header ya es `<ul class="nav navbar-nav">` (barra horizontal) y la pestaña "Proceso (BPMN)" está en el menú; `process.html` existe (200) y `profiles.html` muestra la sección "Diagrama de recursos". **Pero las imágenes daban 404**: `images/02-bpmn-model.svg` y `images/04-fhir-proposal-graph.svg` no existen en el sitio. Hallazgo: el IG Publisher copia el contenido de `input/images/` a la **raíz del sitio publicado**, no a una carpeta `images/` — los SVG están en la raíz (`/02-bpmn-model.svg` y `/04-fhir-proposal-graph.svg` devuelven 200). Corregido: las páginas referencian los SVG solo por su nombre de archivo (sin `images/`), y la regla de la skill quedó corregida (antes decía `images/<archivo>`, que era lo que causaba el 404). El link checker del publisher no falló por las imágenes rotas (no las verifica como enlaces), así que el run pasó en verde con las imágenes rotas.
- Evidence: run de Actions 43156632027 (success), curl 404 en `images/*.svg` y 200 en la raíz, ficheros presentes en main.

## 2026-11-12 — La guía incluye el BPMN y el diagrama de recursos; el header es una barra horizontal

- Artefact: `05-implementation-guide/` (página nueva `process.md`, `profiles.md` con el diagrama de recursos, `index.md`, `menu.xml`, `sushi-config.yaml`, `input/images/` con los dos SVG) y las skills `implementation-guide-sushi` y `fhir-modeling` del pack
- Tool / profile: revisión en vivo del header y del CSS, y SUSHI v3.21.0 de los cambios
- Result: diagnóstico del header: el `menu.xml` era un `<ul>` sin clase dentro de un `<div class="nav-collapse collapse navbar-inverse-collapse">`; el CSS `bootstrap-fhir.css` sí define `.navbar-nav` (45 ocurrencias), pero sin la clase el `<ul>` se ve como lista vertical. Corregido a `<ul class="nav navbar-nav">` y añadida la pestaña "Proceso (BPMN)". Los dos SVG (BPMN 4080×810 y grafo de recursos 1220×900) se copiaron a `input/images/` y se muestran en la guía (BPMN en `process.html` con scroll horizontal y enlace a tamaño completo; grafo en `profiles.html`). SUSHI compila con 0 errores y 0 warnings; los enlaces internos y las imágenes de `process.md`, `profiles.md` e `index.md` se verifican contra los artefactos generados y `input/images/` (ninguno roto). Pendiente: subir a cl-urgencia y verificar el run y la guía en vivo.
- Evidence: `bootstrap-fhir.css` con 45 ocurrencias de `navbar-nav`, lectura en vivo del `<nav>` en index.html, SUSHI v3.21.0 0 errores, comprobación de enlaces en local.

## 2026-11-12 — Run 10: operaciones enlazadas a sus perfiles IHE, publicadas y verificadas en vivo

- Artefact: guía publicada en https://josemandrade.github.io/cl-urgencia/ (operations.html)
- Tool / profile: GitHub Actions, workflow "IG build", run 10 (commit `87831b1`)
- Result: success (build y deploy en verde). Verificado en vivo: operations.html muestra "Buscar paciente" con su enlace a PDQm, y cada operación con su perfil IHE (PIXm en PI-0 y en las transacciones push, MHD en alta/abandono/PI-3, QEDm en buscar episodios y diagnósticos, Subscription FHIR en la suscripción con DSUB refutado). La página tiene 18 enlaces a profiles.ihe.net.
- Evidence: run de Actions 43155426381 (success), lectura en vivo de operations.html con curl.

## 2026-11-12 — Operaciones enlazadas a sus perfiles IHE (buscar paciente → PDQm)

- Artefact: `05-implementation-guide/input/pagecontent/operations.md` y `04-fhir-proposal.md` (revisión 3), con las skills `implementation-guide-sushi` y `fhir-modeling` del pack
- Tool / profile: revisión en vivo de las URLs de los perfiles IHE y SUSHI v3.21.0 de los cambios
- Result: reescrita `operations.md`: cada operación enlaza a su perfil IHE (PIXm en PI-0 y en las tres transacciones push; MHD en alta, abandono y PI-3; PDQm en buscar paciente; QEDm en buscar episodios y diagnósticos; MHD ITI-67 en buscar documento; Subscription FHIR en la suscripción, con DSUB refutado), y PI-2 se reestructura en operaciones nombradas (buscar paciente, buscar episodios, buscar diagnósticos, buscar documento, suscripción). Añadida la operación `GET /Patient?identifier=<sistema RUN>|<RUN>`. La propuesta pasa a revisión 3 (sección 6 con el perfil IHE por operación). SUSHI compila con 0 errores y 0 warnings; los 27 enlaces internos de `operations.md` se verifican contra los artefactos generados (ninguno roto) y las 7 URLs externas (PIXm, PDQm, MHD, QEDm, ATNA, CT, Subscription FHIR) devuelven 200. Subido a cl-urgencia, commit `87831b1`.
- Evidence: curl 200 de las 7 URLs, SUSHI v3.21.0 0 errores, comprobación de enlaces en local.

## 2026-11-12 — Run 9: perfiles propios y página de IHE publicados y verificados en vivo

- Artefact: guía publicada en https://josemandrade.github.io/cl-urgencia/
- Tool / profile: GitHub Actions, workflow "IG build", run 9 (commit `05d2122`)
- Result: success (build y deploy en verde). Verificado en vivo: la página `ihe.html` existe y muestra la revisión por punto (PI-0 a PI-3, encaje, actores, brechas); `profiles.html` dice "perfiles propios" y ya no dice "transcripciones locales"; el menú incluye "Relación con IHE".
- Evidence: run de Actions 43153872690 (success), lectura en vivo de ihe.html y comprobación con curl de profiles.html.

## 2026-11-12 — Run 8: corrección de navegación publicada y verificada en vivo

- Artefact: guía publicada en https://josemandrade.github.io/cl-urgencia/
- Tool / profile: GitHub Actions, workflow "IG build", run 8 (commit `a564056`)
- Result: success (build y deploy en verde). Verificado en vivo en el sitio: la página de Terminología existe y lista los CodeSystems y ValueSets locales (con enlaces a sus páginas) y las terminologías externas; `profiles.html` enlaza a las páginas de los 17 StructureDefinitions; `operations.html` enlaza a los tres Bundles de ejemplo; el menú incluye Terminología y Artefactos.
- Evidence: run de Actions 43152679723 (success), lectura en vivo de terminology.html y comprobación con curl de profiles.html y operations.html.

## 2026-11-12 — La guía publicada: los artefactos FHIR estaban generados, pero las páginas no enlazaban a ellos

- Artefact: `05-implementation-guide/` (profiles.md, terminology.md, operations.md, index.md, menu.xml, sushi-config.yaml) y la skill `implementation-guide-sushi` del pack
- Tool / profile: guía publicada en https://josemandrade.github.io/cl-urgencia/ y revisión en vivo de sus páginas
- Result: el publisher SÍ generó las páginas de los artefactos (StructureDefinition con diferencial/snapshot/bindings/XML/JSON, CodeSystem/ValueSet con expansión, 14 ejemplos); el problema era de navegación. `profiles.md` era una tabla estática con los nombres en código y sin enlaces; `operations.md` nombraba los ejemplos solo por su id; no había página de Terminología; el menú no incluía Artefactos. Corregido: cada perfil/extensión/ValueSet/CodeSystem enlaza a su página generada; cada operación enlaza a su Bundle de ejemplo y a los recursos que lleva; página nueva `terminology.md` (CodeSystems y ValueSets locales con sus códigos, y terminologías externas: CIE-10, SNOMED CT, LOINC, NID, sistemas de identificación RUN/DAU/DEIS); menú con Terminología y Artefactos. Detalle clave: la página generada se llama `<ResourceType>-<id>.html` con el id en minúsculas (`StructureDefinition-dau-encuentro-urgencia.html`), no con el nombre computable (`StructureDefinition-DAUEncuentroUrgencia.html` da 404). SUSHI compila con 0 errores y 0 warnings; los 86 enlaces internos de las páginas se verificaron contra los 37 artefactos generados (ninguno roto ni fuera del sitio). También se corrigió la skill `implementation-guide-sushi` (sección "Make the guide navigable") para que las guías futuras salgan navegables por defecto. Subido a main, commit `a564056`; el workflow corre para publicar el cambio.
- Evidence: páginas verificadas en vivo (perfiles, artefactos, operaciones, una StructureDefinition, un ValueSet, un Bundle de ejemplo), SUSHI v3.21.0 0 errores, comprobación de enlaces en local.

## 2026-11-12 — Run 7: el build está en verde; el deploy falla porque GitHub Pages no está activado

- Artefact: `.github/workflows/ig-build.yml`, `05-implementation-guide/` (enlaces del paso 4 a URLs de GitHub)
- Tool / profile: GitHub Actions, workflow "IG build", run 7 (commit `c2a10af`, `1074d62` con el paso Install Jekyll)
- Result: build job success (11 pasos: SUSHI, publisher con Jekyll, revisión de enlaces y subida del artefacto para Pages). El job deploy falló en `actions/deploy-pages@v4`. La API de Pages del repo devuelve 404 ("Not Found"): GitHub Pages no está activado para cl-urgencia. Pendiente: activar Pages (Settings → Pages → Source: GitHub Actions) y re-ejecutar el job de deploy ("Re-run failed jobs") o un nuevo push.
- Evidence: run de Actions 43151447780 (build: success; deploy: failure en el paso 2), API `GET /repos/josemandrade/cl-urgencia/pages` → 404.

## 2026-11-12 — Run 4: la plantilla HL7 exige un contacto de grupo de trabajo de HL7

- Artefact: `.github/workflows/ig-build.yml`, `05-implementation-guide/` (con `ig.ini` en `hl7.base.template#current`, id `hl7.fhir.uv.test.dau-urgencia-red`)
- Tool / profile: GitHub Actions, workflow "IG build", run 4 (commit `4f50e2a`)
- Result: failed — el chequeo de reino pasó (`uv`), pero la plantilla falló en `onGenerate.jira.xslt` línea 28: el primer contacto de la guía debe tener una URL a una página de grupo de trabajo de HL7 (`http://www.hl7.org/Special/committees/...`). Leído el código de la plantilla (`hl7.base.template` 1.0.0): el XSLT además busca el grupo en la lista de grupos de HL7 (líneas 50–55), así que debe ser un grupo real. Decisión del usuario: volver a `fhir.base.template` e instalar Jekyll en el workflow. El id se queda en `uv`.
- Evidence: run de Actions 43148434540 (job build: paso 8 failure), log `logs_116845353006.zip` (paso 8), plantilla `hl7.base.template` 1.0.0 leída en local (`scripts/onGenerate.jira.xslt`, líneas 19–31 y 50–55).

## 2026-11-12 — Run 3 del workflow: la plantilla genérica necesita Jekyll (no instalado)

- Artefact: `.github/workflows/ig-build.yml`, `05-implementation-guide/` (con `ig.ini` en `fhir.base.template#1.0.0`)
- Tool / profile: GitHub Actions, workflow "IG build", run 3 (commit `c72dea4`, id `hl7.fhir.cl.test.dau-urgencia-red`)
- Result: failed — el build llegó mucho más lejos (SUSHI 0 errores, validación y salidas generadas) y falló en el último paso: el publisher corre `jekyll build` para armar el sitio y Jekyll no está en el runner (`Cannot run program "jekyll" ... error=2, No such file or directory`). La advertencia "This content depends on fhir.base.template which is no longer considered secure to use" es solo eso, una advertencia. Decisión del usuario: cambiar el id a `hl7.fhir.uv.test.dau-urgencia-red` y volver a `hl7.base.template#current`.
- Failures: la descarga del log por API pide derechos de admin ("Must have admin rights to Repository"); el usuario subió el zip del log.
- Evidence: run de Actions 43147215268 (job build: paso 8 failure), log `logs_116842173595.zip` (paso 8), plantilla `fhir.base.template` 1.0.0 leída en local (su README la describe como "Base IG template managed by HL7 but usable by anyone (no logos)").

## 2026-11-11 — Workflow de la guía: SUSHI pasó, la descarga del IG Publisher falló (404)

- Artefact: `.github/workflows/ig-build.yml`, `05-implementation-guide/` (fuente de la guía)
- Tool / profile: GitHub Actions, workflow "IG build", run 1 (commit `92da894`, "Create ig-build.yml")
- Result: failed — el build falló en el paso "Download the IG Publisher" (0 segundos). SUSHI corrió bien en CI (paso 5, success), así que el FSH compila. La URL `https://fhir.github.io/latest-ig-publisher/org.hl7.fhir.publisher.jar` devuelve **404** (verificado en vivo con curl: el sitio latest-ig-publisher ya no sirve el jar). El publisher actual es la release 3.0.3 de HL7/fhir-ig-publisher (2026-11-06) y el artefacto se llama `publisher.jar` (no `org.hl7.fhir.publisher.jar`): `https://github.com/HL7/fhir-ig-publisher/releases/latest/download/publisher.jar` (verificado: redirige a la 3.0.3 y descarga, 243 MB, sha256 eeb61f43ff54d532b8da07c5f5e60bc09c63285f8c5bbb2936467bac049a20af).
- Failures: el push de la corrección (un solo archivo, el workflow) por API falló con el mismo 403 de antes — la App sigue sin el permiso Workflows. La corrección está aplicada en local (`~/workspace/health-interop-test-run/.github/workflows/ig-build.yml`); pendiente que el usuario la aplique en la web de GitHub (editar el archivo en main, cambiar la línea del wget, commitear). Al commitear, el workflow corre de nuevo.
- Evidence: run de Actions 43144197867 (status completed, conclusion failure; job build: paso 7 failure, paso 8 skipped, deploy skipped), curl -I (404 en la URL vieja, 302→200 en la nueva), release 3.0.3 verificada en la API de GitHub.

## 2026-11-11 — Subida a cl-urgencia (pasos 4–5) y el workflow que no se pudo subir

- Artefact: `docs/health-interop/2026-11-11-dau-urgencia-red/` (pasos 4 y 5), `.gitignore`, `.github/workflows/ig-build.yml`
- Tool / profile: subida con el conector GitHub (snapshot push)
- Result: passed (parcial) — 34 archivos subidos a main, commit `92909ae`, sobre `2cefbfb`. Verificado: `sushi-config.yaml` en el repo muestra id `hl7.fhir.cl.test.dau-urgencia-red`, versión 0.1.0. El workflow `.github/workflows/ig-build.yml` **no** se pudo subir: el primer intento (con el workflow) falló con 403 "Resource not accessible by integration" al crear el árbol; el segundo intento (sin el workflow) pasó. Causa: la GitHub App de Muse no tiene el permiso Workflows, que GitHub exige para crear o modificar archivos de workflow por API. Sin el workflow no hay build ni deploy, así que la URL de GitHub Pages todavía no está viva.
- Failures: 403 en el push con el workflow (permiso Workflows de la App). Pendiente: que el usuario agregue el workflow por la web de GitHub o le dé a la App el permiso Workflows, y activar GitHub Pages (Settings → Pages → Source: GitHub Actions) si el deploy lo pide.
- Evidence: commit `92909ae` en main, `sushi-config.yaml` verificado en el repo.

## 2026-11-11 — Paso 5 validado por el usuario (Guía de Implementación)

- Artefact: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`
- Tool / profile: validación del usuario en chat ("Valido la Guía de Implementación")
- Result: passed — paso 5 cerrado; la guía y el workflow quedan como fuente de verdad del paso 6. El usuario pidió la URL de la guía desplegada en GitHub Pages.
- Failures: ninguna.
- Evidence: respuesta del usuario (widget de validación).

## 2026-11-11 — Paso 5: guía con SUSHI (Tasks 1–18) terminada y presentada

- Artefact: `05-implementation-guide/` (plan.md, sushi-config.yaml, ig.ini, 11 FSH, 4 páginas, menu.xml), `.github/workflows/ig-build.yml`, `.gitignore`
- Tool / profile: SUSHI v3.21.0 (`sushi .` en la carpeta de la guía)
- Result: passed — SUSHI compila con **0 errores y 0 warnings** ("Just like a perfect pearl"). 17 StructureDefinitions (10 perfiles + 7 extensiones), 3 ValueSets, 2 CodeSystems, 14 instancias; los 14 ejemplos validan contra sus perfiles. Verificado en el JSON generado (`fsh-generated/resources/`): el Encounter de alta tiene status finished y `hospitalization.dischargeDisposition` 03, el Bundle de alta es transaction con 4 PUT, el Bundle de admisión trae los POST con ifNoneExist. El workflow YAML parsea (2 jobs, 9 pasos en build).
- Failures: la primera compilación de los perfiles dio 3 errores — `dischargeDisposition` no existe como elemento directo de Encounter en FHIR R4; es `Encounter.hospitalization.dischargeDisposition`. Se corrigieron el FSH y el invariante `dau-alta-destino`, y la siguiente compilación quedó en 0 errores.
- Evidence: salida de SUSHI (0 Errors, 0 Warnings), `fsh-generated/resources/` (36 recursos JSON), YAML del workflow validado.

## 2026-11-11 — Paso 4 validado por el usuario (propuesta FHIR + mapeo + diagrama)

- Artefact: `04-fhir-proposal.md`, `04-mapping-table.md`, `04-fhir-proposal-graph.svg`
- Tool / profile: validación del usuario en chat ("Valido la propuesta FHIR y el mapeo")
- Result: passed — paso 4 cerrado; la propuesta, el mapeo, la revisión IHE y el diagrama quedan como fuente de verdad del paso 5.
- Failures: ninguna.
- Evidence: respuesta del usuario (widget de validación).

## 2026-11-11 — Corrección del paso 4: diagrama de recursos estilo ClinFHIR GraphBuilder

- Artefact: `04-fhir-proposal.md` (sección 2, "Diagrama de recursos"), `04-fhir-proposal-graph.svg`, `render_fhir_graph.py`
- Tool / profile: corrección del usuario en chat ("a la propuesta de recursos le hace falta un diagrama como los que se construyen con el graphbuilder de clinfhir")
- Result: passed — el diagrama muestra los 8 recursos y el PDF, con las 12 referencias etiquetadas por el elemento que las lleva, el `Encounter` como centro y el `Bundle` como marco punteado. Generado con un script durable (`render_fhir_graph.py`) y verificado visualmente (render a PNG con cairosvg y revisión de la imagen: etiquetas sin solaparse —se movió `participant.individual` para no chocar con `hospitalization.destination`—, sin cruces entre flechas).
- Failures: la primera versión tenía las etiquetas `hospitalization.destination` y `participant.individual` solapadas; se corrigió moviendo la segunda sobre su diagonal, junto al nodo Practitioner.
- Evidence: `04-fhir-proposal-graph.svg` (SVG bien formado, 11 KB) y el render verificado.

## 2026-11-11 — Paso 3 validado por el usuario (entidades y datos)

- Artefact: `03-entities-data.md`
- Tool / profile: validación del usuario en chat ("Valido las entidades y sus datos")
- Result: passed
- Failures: none
- Evidence: 12 entidades con campos, identificadores, origen, obligatoriedad y tabla de calidad y propiedad.

## 2026-11-11 — El fallecimiento es un alta con destino 03 (corrige la nota anterior)

- Artefact: `04-fhir-proposal.md` (sección 5), `04-mapping-table.md` (CONDICIÓN AL CIERRE)
- Tool / profile: revisión en vivo de la guía cl-urgencia v0.2.0 (ValueSet "Destino al alta de urgencia" y perfil EncuentroUrgenciaAlta)
- Result: passed — la guía **sí** contempla el fallecimiento como destino de alta: el ValueSet `vs-destino-alta` incluye el código `03 Fallecido` (`system = https://interoperabilidad.minsal.cl/fhir/ig/urgencia-eventos/CodeSystem/destino-alta`) y el perfil de alta liga `dischargeDisposition` 1..1 a ese ValueSet (requerido). El mapeo CMBD deduce "CONDICIÓN AL CIERRE: `03 Fallecido` → fallecido".
- Failures: la spec v3 y el BPMN v4 decían que "la guía no lo contempla": impreciso. La guía no nombra un evento separado de fallecimiento, pero el código existe en el ValueSet del alta. Consecuencia: no hace falta un Bundle nuevo ni un código nuevo; el fallecimiento es un evento de alta con `dischargeDisposition = 03`, `period.end` = hora del fallecimiento, diagnóstico de egreso = causa de muerte (CIE-10, `use = DD`) y documento de resumen de alta (LOINC 59258-4).
- Evidence: https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/ValueSet-vs-destino-alta.html (6 conceptos, incluye `03` Fallecido) y https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/StructureDefinition-encuentro-urgencia-alta.html (`dischargeDisposition` 1..1, binding requerido a "Destino al alta de urgencia").

## 2026-11-11 — Subidas a GitHub verificadas

- Artefact: `health-interop-superpowers` (pack v0.6.0) y `cl-urgencia` (carpeta de trabajo)
- Tool / profile: conector GitHub (snapshot push) + verificación remota (list_commits, get_file_contents)
- Result: passed — pack: main `bc1bcca` (39 archivos, skill.yaml 0.6.0 con 14 skills) sobre `a1daa78`. Caso: main `2cefbfb` (9 archivos) sobre el commit inicial `dd5b450` del proveedor, que dejó un README.md vacío en la raíz.
- Failures: none — el 403 anterior se resolvió cuando el usuario incluyó `cl-urgencia` en la instalación de la GitHub App.
- Evidence: registros de sync guardados (5 entradas en el pack, 1 en el caso).

## 2026-11-11 — Paso 2 validado por el usuario (BPMN v4 + spec v3)

- Artefact: `02-bpmn-model.bpmn`, `02-bpmn-model.md` (revisión 4), `01-use-case-spec.md` (revisión 3)
- Tool / profile: validación del usuario en chat ("Valido el BPMN v4 y la spec v3")
- Result: passed
- Failures: none
- Evidence: XML revalidado (0 referencias sin resolver, 25 tareas, 4 puertas, 3 eventos de borde, 41 flujos de secuencia); SVG re-renderizado.

## 2026-11-11 — Repaso IHE temprano verificado en vivo

- Artefact: `02-bpmn-model.md`, sección "IHE landscape scan"
- Tool / profile: `ihe-landscape-scan` contra https://profiles.ihe.net/ (dominio ITI y PCC) y la wiki de IHE
- Result: passed — 12 perfiles candidatos verificados: PIXm v3.1.0, PDQm v3.2.0, MHD v4.2.5, mCSD v4.0.0 (todas Publication, FHIR R4), QEDm v3.0.0 (Publication, FHIR R4, dominio PCC), y los clásicos PIX, PDQ, XDS.b, XDR, DSUB, NAV, ATNA, CT, BPPC en ITI TF Rev 20.2 (Final Text, última revisión 20.2 del 11 de noviembre de 2025)
- Failures: none — la URL https://profiles.ihe.net/ITI/QEDm/ devolvió 404: QEDm es del dominio PCC, no ITI; la página correcta es https://profiles.ihe.net/PCC/QEDm/
- Evidence: sección "IHE landscape scan" en `02-bpmn-model.md`, con versión, estado, URL y fecha de verificación por perfil, y candidatos por punto de interoperabilidad en la tabla de PI.

## 2026-11-11 — Decisión Q3: fallecimiento como extensión del caso

- Artefact: `02-bpmn-model.bpmn` (v4), `01-use-case-spec.md` (revisión 3)
- Tool / profile: decisión del usuario en chat ("Incluirlo como extensión del caso")
- Result: passed (decisión registrada y aplicada)
- Failures: none — la guía v0.2.0 no contempla el fallecimiento; el caso lo incluye como extensión, y el valor exacto del desenlace y el contenido del evento se definen en el paso 4.
- Evidence: corrección C14 aplicada (tercera salida "Fallecimiento" de la puerta de desenlace → "Cerrar DAU (fallecido)" → publicar aviso); XML revalidado sin referencias sin resolver.

## 2026-11-11 — La prueba no ejerció el diálogo de brainstorming (hallazgo de la prueba)

- Artefact: `01-use-case-spec.md` (paso 1)
- Tool / profile: revisión del recorrido de la prueba contra la skill `brainstorming-health`
- Result: failed — el diálogo de brainstorming no se hizo
- Failures: (alto) la spec se redactó directamente desde la descripción del caso entregada por el usuario en un solo mensaje ("ese es el caso"), sin el diálogo del brainstorming: no se hicieron las preguntas del brainstorming (qué problema resuelve, quién lo usa, qué datos entran y salen, cómo se ve el éxito), ni se devolvió la comprensión en trozos cortos esperando corrección. La spec sí recoge problema, usuarios, roles, flujo, ejemplo y criterio de éxito, pero eso vino de la descripción del usuario y de la guía, no de un brainstorming. Consecuencia: las preguntas P1–P10 quedaron sin responder al inicio (por ejemplo, P1 cuándo se publica, P2 hub o punto a punto) y la comprensión del proceso llegó débil al paso 2 — la admisión ni siquiera estaba en la comprensión inicial, y solo la revisión experta la detectó en el BPMN v1. La validación del usuario ("la valido") cubrió el contenido de la spec, no el proceso del brainstorming.
- Evidence: origen de la spec ("descripción del usuario, 2026-11-11"); el usuario lo señaló en el chat el 2026-11-11 ("al usar el componente no usamos brainstorming").
- Fix aplicado: nueva regla en `brainstorming-health` (v0.6.0): aunque el usuario entregue una descripción completa en un solo mensaje, el diálogo del brainstorming se hace igual antes de redactar la spec.

## 2026-11-11 — Guía publicada v0.2.0 verificada en vivo (corrige la referencia de la revisión experta)

- Artefact: guía de Implementación FHIR — Urgencia (Admisión, Alta y Abandono) v0.2.0 (https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/index.html, modelo.html, arquitectura.html)
- Tool / profile: lectura directa de la guía publicada
- Result: passed (con correcciones a la referencia anterior)
- Failures: la guía v0.1.1 del build continuo usada por la revisión experta de la v1 estaba desactualizada en tres puntos: (1) el estado de admisión es `arrived`, no `in-progress`; (2) no existe un evento de Categorización — los estados intermedios (categorizado, en atención) no se informan; (3) el egreso no incluye el fallecimiento — los episodios cierran solo con alta o abandono. Además resuelve: tres transacciones Bundle (admisión/alta/abandono) sobre un solo Encounter por ID DAU; push al Bus + pull del Repositorio (con suscripción opcional); identidad por RUN con resolución en el MPI MINSAL; destinos de alta (domicilio, hospitalización 01, traslado 02, derivación 04); la categoría C1–C5 no viaja en el aviso.
- Evidence: páginas index/modelo/arquitectura de la guía v0.2.0 leídas el 2026-11-11; cambios reflejados en la spec revisión 2 y en el BPMN v3. Q3 (fallecimiento) queda en conflicto: el usuario respondió sí, la guía no lo contempla; decisión pendiente.

## 2026-11-11 — Revisión experta del modelo BPMN (v1)

- Artefact: `02-bpmn-model.bpmn` (v1)
- Tool / profile: revisión por experto en procesos de salud y gestión de urgencias, con referencia a la Guía de Interoperabilidad de Urgencia del MINSAL v0.1.1 (verificada en vivo: build.fhir.org/ig/Minsal-CL/IG_Urgencia/spec-events.html)
- Result: failed — el modelo no refleja el proceso real de urgencia
- Failures: (crítico) admisión ausente, colapsada en "Registrar atención en urgencia"; (crítico) NEA modelado como si el paciente hubiera sido atendido; (alto) el DAU se generaba antes del desenlace en vez de aperturarse en la admisión y cerrarse en el egreso; (medio) la fuga era salida de puerta en vez de interrupción; (medio) la tarea "Enviar DAU en PDF" no tenía flujos de secuencia; (bajo) faltaban los eventos de fin en los pools A y B
- Evidence: informe de revisión en el chat 2026-11-11; correcciones C1–C13 y C15–C16 aplicadas en el modelo v2; preguntas Q1–Q7 pendientes de decisión del usuario

## 2026-11-11 — Spec del caso validada por el usuario

- Artefact: `01-use-case-spec.md`
- Tool / profile: validación del usuario en chat ("la valido")
- Result: passed
- Failures: none
- Evidence: mensaje del usuario 2026-11-11 validando la spec; las preguntas P1–P10 quedan abiertas para los pasos siguientes, no bloquean el paso 2.
