# Aviso mínimo de atención de urgencia a la red (DAU)

Guía de implementación de prueba para el caso de uso: el mínimo que un establecimiento debe informar a la red cuando atiende a una persona en su unidad de urgencia, para la continuidad de la atención.

> Esta es una guía de prueba, construida en la prueba del componente `health-interop-superpowers`. No es la guía del MINSAL. Sus perfiles (`DAUEncuentroUrgencia`, `DAUPaciente`, etc.) son perfiles propios de esta guía, diseñados a partir de la especificación del caso de uso sobre los recursos base de FHIR R4. Los datos que codifican son los que el caso de uso exige informar a la red; la [Guía de interoperabilidad de eventos de urgencia del MINSAL (cl-urgencia v0.2.0)](https://interoperabilidad.minsal.cl/fhir/ig/cl-urgencia/0.2.0/) es la referencia de esos requisitos de datos. Todos los ejemplos usan datos sintéticos.

## El caso de uso

Cuando una persona es atendida en la unidad de urgencia de un establecimiento, la red necesita saberlo para darle continuidad a la atención: quién fue atendido, dónde y cuándo, cómo terminó (alta con destino, o abandono voluntario: fuga o NEA), la hipótesis y el diagnóstico de egreso, los medicamentos al alta, y dónde está el detalle completo: el DAU en PDF del HIS/RCE.

Los puntos de la red que consumen el aviso: APS, especialidad, otro hospital y SAMU.

## Los tres eventos

El aviso se publica en tres momentos, una transacción `Bundle` por evento, siempre sobre un solo `Encounter` por episodio, actualizado por PUT condicional por ID DAU:

1. **Admisión** — la persona llega y se admite (`status = arrived`).
2. **Alta** — el episodio se cierra con alta y destino (`status = finished`, `dischargeDisposition` con el destino). El fallecimiento es un alta con destino `03 Fallecido`.
3. **Abandono** — la persona se va antes de cerrar el episodio (`status = finished`, tipo de abandono: NEA o fuga).

## Usuarios, roles y departamentos

- **HIS/RCE del establecimiento**: publica cada transacción en el momento del evento (push al Bus de Interoperabilidad MINSAL).
- **Bus de Interoperabilidad MINSAL**: valida perfil y terminología, resuelve la identidad contra el MPI MINSAL y aplica en el Repositorio FHIR.
- **Repositorio FHIR**: lo consulta la red (pull) y avisa por suscripción.
- **APS, especialidad, otro hospital, SAMU**: consumen el aviso para continuidad de la atención.
- **Portal Ciudadano (HCC)**: muestra al paciente solo sus propias atenciones, no las restringidas.

## Puntos de interoperabilidad

| Punto | Qué pasa | Recursos |
|---|---|---|
| PI-0 | Identidad del paciente (RUN, MPI) | `Patient` |
| PI-1 | Publicación del aviso (push al Bus) | `Bundle` (transaction) |
| PI-2 | Consulta y suscripción (pull del Repositorio) | `Encounter`, `Condition`, `DocumentReference` |
| PI-3 | Acceso al PDF del DAU | `DocumentReference.content.attachment.url` |

La [relación con los perfiles IHE](ihe.html) (qué perfil encaja en cada punto, en parte o no encaja) está documentada punto por punto.

## Perfiles de esta guía

El detalle de cada perfil (tabla de elementos, diferencial, snapshot, bindings y formatos) está en su página; la lista completa de artefactos está en el [resumen de artefactos](artifacts.html).

- [`DAUEncuentroUrgencia`](StructureDefinition-dau-encuentro-urgencia.html), [`DAUEncuentroUrgenciaAlta`](StructureDefinition-dau-encuentro-urgencia-alta.html), [`DAUEncuentroUrgenciaAbandono`](StructureDefinition-dau-encuentro-urgencia-abandono.html) (Encounter)
- [`DAUPaciente`](StructureDefinition-dau-paciente.html) (Patient), [`DAUPrestadorOrganizacional`](StructureDefinition-dau-prestador-organizacional.html) (Organization), [`DAUPrestadorProfesional`](StructureDefinition-dau-prestador-profesional.html) (Practitioner)
- [`DAUDiagnosticoUrgencia`](StructureDefinition-dau-diagnostico-urgencia.html) (Condition), [`DAUIndicacionMedicamento`](StructureDefinition-dau-indicacion-medicamento.html) (MedicationRequest), [`DAUDocumentoUrgencia`](StructureDefinition-dau-documento-urgencia.html) (DocumentReference)
- [`DAUBundleAviso`](StructureDefinition-dau-bundle-aviso.html) (Bundle)

El proceso que publica el aviso está modelado en BPMN en la página [Proceso (BPMN)](process.html), y el diagrama de recursos (estilo ClinFHIR GraphBuilder) está en [Diagrama de recursos](resources.html) y en [Perfiles](profiles.html#diagrama-de-recursos). Las operaciones en el tiempo, flujo por flujo (cada mensaje con su operación), están en [Diagramas de secuencia](sequences.html). El mapeo campo a campo está en [Mapeo de datos](mapping.html) y en la [tabla de mapeo](https://github.com/josemandrade/cl-urgencia/blob/main/docs/health-interop/2026-11-11-dau-urgencia-red/04-mapping-table.md) validada en el paso 4.
