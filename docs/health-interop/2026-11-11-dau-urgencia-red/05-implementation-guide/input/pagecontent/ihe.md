# Relación con IHE

Esta guía define sus propias transacciones (las tres transacciones `Bundle` del [aviso mínimo](operations.html)) y sus propios [perfiles](profiles.html), diseñados para este caso de uso. No declara conformidad con ningún perfil IHE: **ningún perfil IHE lleva la transacción en sí**. Los perfiles IHE cubren funciones de apoyo (identidad, documentos, consulta, seguridad, tiempo), y esta página dice, punto por punto, cuál encaja, cuál encaja en parte y cuál no, para que quien implemente o evalúe la guía sepa qué parte ya está cubierta por un estándar IHE y qué parte es propia de esta guía.

Repaso verificado en vivo en [profiles.ihe.net](https://profiles.ihe.net/) (2026-11-11): PIXm v3.1.0, PDQm v3.2.0, MHD v4.2.5, mCSD v4.0.0, QEDm v3.0.0 (Publication, FHIR R4) y los clásicos PIX, PDQ, XDS.b, XDR, DSUB, NAV, ATNA, CT, BPPC en ITI TF Rev 20.2 (Final Text). El repaso temprano y la revisión por punto están en la [propuesta FHIR](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/04-fhir-proposal.md) validada en el paso 4.

## Por punto de interoperabilidad

### PI-0 — Publicación de la admisión (push HIS → Bus)

| Perfil IHE | Encaje | Por qué |
|---|---|---|
| **PIXm** (Patient Identifier Cross-reference for Mobile, ITI-83, ITI-104) | Parcial | El Bus resuelve la identidad contra el MPI, que es la función del Patient Identifier Cross-reference Manager. Pero el HIS no llama a PIXm: la resolución ocurre dentro del Bus, como parte de la transacción. |
| **MHD** (Mobile access to Health Documents) | No encaja | En la admisión no se publica ningún documento. |
| **NAV** (Notification of Document Availability) | No encaja | NAV avisa de documentos disponibles; en la admisión no hay documento. |
| **ATNA** (Audit Trail and Node Authentication) | Parcial (transversal) | Cubre autenticación de nodos y auditoría; la guía exige TLS 1.2+ y autenticación del emisor, pero no nombra ATNA ni el formato de auditoría. |
| **CT** (Consistent Time) | Parcial (transversal) | Cubre el tiempo consistente; la guía exige ISO 8601 con zona horaria, pero no nombra CT ni un servidor de tiempo. |

Lo que queda a medida: la transacción de admisión en sí (el `Bundle`, `PUT Encounter?identifier=…`).

### PI-1 — Publicación del alta, el abandono o el fallecimiento (push HIS → Bus)

| Perfil IHE | Encaje | Por qué |
|---|---|---|
| **PIXm** | Parcial | Igual que en PI-0. |
| **MHD** (ITI-65, ITI-67, ITI-68) | Parcial | El cierre incluye un `DocumentReference` al DAU; MHD ITI-65 (Provide Document Bundle) cubre publicar el documento con sus metadatos, e ITI-67/ITI-68 buscarlo y recuperarlo. Pero la guía lleva el documento como referencia dentro del Bundle de cierre, y el PDF se descarga por su URL; no se usa una transacción MHD. |
| **XDR** (Cross-Enterprise Document Reliable Interchange) | No encaja | El push de la guía es una transacción Bundle FHIR al Bus, no un envío punto a punto de documentos XDR, que no llevaría las actualizaciones del `Encounter`. |
| **ATNA** | Parcial (transversal) | Como en PI-0. |
| **CT** | Parcial (transversal) | Como en PI-0. |

Lo que queda a medida: la transacción de cierre en sí (el `Bundle`, `PUT` condicional del episodio completo).

### PI-2 — Consulta de episodios (pull receptor → Repositorio, o suscripción)

| Perfil IHE | Encaje | Por qué |
|---|---|---|
| **QEDm** (Mobile Query Existing Data, PCC-44) | Parcial | El patrón de consultar datos existentes por búsqueda FHIR coincide con las búsquedas de la guía (`Encounter?patient.identifier=…&class=EMER`, `Condition?encounter=`, `DocumentReference?encounter=`). Pero la guía no declara conformidad QEDm ni sus opciones; la consulta central (episodios por paciente) es una búsqueda FHIR simple, no una transacción QEDm. |
| **DSUB** (Document Metadata Subscription) | No encaja | La suscripción de la guía es una `Subscription` FHIR sobre `Encounter class=EMER`; DSUB es una suscripción a metadatos de documentos de un registro XDS, y el Repositorio aquí es un repositorio FHIR, no un registro XDS. |
| **MHD** (ITI-66, ITI-67) | Parcial | Buscar listas (ITI-66) y referencias (ITI-67) de documentos coincide con localizar el DAU, pero la guía lo hace con una búsqueda FHIR simple (`DocumentReference?encounter=`), no con transacciones MHD. |
| **ATNA** | Parcial (transversal) | Como en PI-0. |
| **CT** | Parcial (transversal) | Como en PI-0. |

Lo que queda a medida: las búsquedas FHIR de la guía y la `Subscription` sobre `Encounter`.

### PI-3 — Recuperación del DAU en PDF (receptor → HIS)

| Perfil IHE | Encaje | Por qué |
|---|---|---|
| **MHD** (ITI-68, Retrieve Document) | Parcial | ITI-68 es la forma estándar de recuperar un documento. Pero la guía descarga el PDF con un GET autenticado directo a `DocumentReference.content.attachment.url`, no con una transacción ITI-68 contra un Document Responder. El patrón coincide; el mecanismo no. |
| **ATNA** | Parcial (transversal) | Como en PI-0. |
| **CT** | Parcial (transversal) | Como en PI-0. |

Lo que queda a medida: la descarga autenticada por URL del PDF.

## Brechas y riesgos

| Brecha / riesgo | Severidad | Detalle |
|---|---|---|
| La conciliación de identidades duplicadas o contradictorias no está definida | Media | El Bus rechaza y envía a conciliación, pero el proceso de conciliación no está descrito en la guía. |
| La vinculación del MPI para pacientes NN una vez conocida la identidad está pendiente de definir con el NID | Media | La guía lo dice explícito: queda pendiente de definir con el NID. |
| El documento DAU vive en el HIS; si el HIS no está disponible, el PDF no se puede descargar | Media | El Repositorio guarda la referencia, no necesariamente el documento; la replicación es por acuerdo institucional, no está garantizada. |
| El consentimiento se aplica por políticas de acceso y etiquetas de seguridad, no por un perfil IHE (BPPC refutado) | Baja–media | La guía marca los episodios restringidos con `meta.security = R` y el Portal Ciudadano no los muestra; no hay documentos de consentimiento BPPC en el flujo. |
| La auditoría no está estandarizada a ATNA | Baja | El Bus registra trazabilidad (emisor, fecha de recepción, resultado de validación, respuesta), pero el formato de auditoría no es ATNA. |
| El canal de notificación de la `Subscription` no está especificado | Baja | La guía dice que el consumidor crea una `Subscription` sobre `Encounter class=EMER`; el canal (por ejemplo, REST-hook) es un detalle de implementación. |
| La admisión de la vía rápida C1 puede completarse durante la atención; la guía prohíbe enviar una admisión de un episodio ya cerrado | Baja | El Bundle de cierre crea el episodio si no existe (un alta sin admisión previa crea el episodio igual), así que el caso está cubierto. |
