# Entidades y datos — Aviso mínimo de atención de urgencia a la red (DAU)

- **Estado:** propuesto para validación (paso 3, `entities-data`)
- **Fecha:** 2026-11-11
- **Spec de origen:** `01-use-case-spec.md` revisión 3 (validada por el usuario el 2026-11-11)
- **Modelo de origen:** `02-bpmn-model.md` revisión 4 (validado por el usuario el 2026-11-11)
- **Repaso IHE temprano:** ver `02-bpmn-model.md`, sección "IHE landscape scan"

Los nombres de entidades, roles y puntos son los mismos de la spec y del BPMN. Esta lista nombra las cosas del caso y los datos que cada una lleva; la correspondencia con recursos FHIR y la revisión IHE por punto se hacen en el paso 4.

## Entidades principales

| Entidad | Definición | Sistema que la posee | Identificadores |
|---|---|---|---|
| Persona atendida | La persona que recibe atención en la unidad de urgencia | HIS/RCE del establecimiento (la admite); el MPI MINSAL resuelve su identidad | RUN (principal); si no tiene RUN: pasaporte, RUN de la madre, o identificador local con su ficha clínica local; NN si no está identificada |
| Episodio de urgencia | La atención de una persona en la unidad de urgencia, desde la admisión hasta el cierre (alta, abandono o fallecimiento) | HIS/RCE del establecimiento | ID DAU (único en el establecimiento, nunca se reutiliza; el mismo en las tres transacciones) |
| Establecimiento | El establecimiento de salud: el informante y, en la derivación, el de destino | HIS/RCE (origen); el Bus y el Repositorio lo conocen por código | Código DEIS |
| Profesional | El profesional que atiende (Terminador: médico u odontólogo; también el Selector de Demanda) | HIS/RCE del establecimiento | Opcional (la guía lo marca opcional) |
| Hipótesis diagnóstica | La hipótesis al ingreso o durante la atención | HIS/RCE del establecimiento | Sin identificador propio (pertenece al episodio) |
| Diagnóstico de egreso | El diagnóstico al cierre del episodio | HIS/RCE del establecimiento | Sin identificador propio (pertenece al episodio); código CIE-10 |
| Medicamento al alta | Cada medicamento indicado al alta | HIS/RCE del establecimiento | Sin identificador propio (pertenece al episodio) |
| DAU en PDF | El documento con el detalle clínico completo del episodio (resumen de alta o nota de urgencia) | HIS/RCE del establecimiento (lo genera al cerrar); el Repositorio lo referencia | Referencia al documento (`DocumentReference.content.attachment.url`) |
| Bus de Interoperabilidad MINSAL | La plataforma central que recibe, valida y aplica las transacciones | MINSAL (infraestructura) | — |
| Repositorio FHIR | Donde quedan guardados los episodios y se consultan | MINSAL (infraestructura) | — |
| MPI MINSAL | El índice maestro de pacientes que resuelve la identidad (RUN ↔ identificadores) | MINSAL (infraestructura) | — |
| Portal Ciudadano (HCC) | Muestra a la persona sus propias atenciones (no las restringidas) | MINSAL (consumidor) | — |

## Datos por entidad

### Persona atendida

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Identificador (RUN, o pasaporte, RUN de la madre, identificador local, o NN) | Obligatorio | Admisión (doble verificador: RUN y nombre, u otro identificador) | Codificado (sistema de identificación) |
| Datos sociodemográficos | Obligatorio | Admisión | Estructurado o texto, según el campo |
| Previsión | Obligatorio | Admisión | Codificado |

### Episodio de urgencia

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| ID DAU | Obligatorio; único en el establecimiento, nunca se reutiliza | Admisión (apertura del DAU) | Codificado (sistema `https://interoperabilidad.minsal.cl/fhir/sid/dau/[código DEIS]`) |
| Estado del episodio | Obligatorio (`arrived` en admisión, `finished` al cierre) | Admisión / cierre | Codificado |
| Fecha y hora de admisión | Obligatorio | Admisión | Estructurado (fecha y hora) |
| Fecha y hora de cierre | Obligatorio al cierre (`period.end`: hora en que el paciente sale físicamente, hora en que se constata el abandono, u hora del fallecimiento) | Cierre | Estructurado (fecha y hora) |
| Motivo de consulta | Obligatorio | Admisión | Texto libre |
| Procedencia | Obligatorio | Admisión (recepción) | Codificado |
| Medio de llegada | Obligatorio | Admisión (recepción) | Codificado |
| Destino de alta | Obligatorio en alta (domicilio, hospitalización 01, traslado 02, derivación 04; con 01/02/04 se informa el establecimiento de destino) | Cierre (alta) | Codificado + referencia al establecimiento de destino |
| Tipo de abandono | Obligatorio en abandono (fuga o NEA) | Cierre (abandono) | Codificado |
| Desenlace por fallecimiento | Obligatorio en fallecimiento; **el valor exacto se define en el paso 4** (extensión del caso, no de la guía) | Cierre (fallecimiento) | Codificado (por definir) |
| Seguridad (episodio restringido) | Condicional: `meta.security = R` en episodios de abuso sexual, violencia o constatación de lesiones | Cierre | Codificado |

### Establecimiento

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Código DEIS | Obligatorio (origen y destino) | Admisión (origen); cierre (destino, cuando aplica) | Codificado |

### Profesional

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Identificador del profesional | Opcional | Atención | Codificado |

### Hipótesis diagnóstica

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Descripción de la hipótesis | Condicional (si existe; en NEA puede no existir) | Atención | Texto libre |
| Estado provisional | Obligatorio cuando existe (`provisional`) | Atención | Codificado |

### Diagnóstico de egreso

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Código del diagnóstico | Obligatorio en alta | Cierre (alta) | Codificado (CIE-10) |
| Uso del diagnóstico | Obligatorio en alta (`use = DD`, diagnóstico de egreso) | Cierre (alta) | Codificado |

Los diagnósticos descartados no se informan.

### Medicamento al alta

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Medicamento indicado al alta | Condicional (si existen; en abandono no hay) | Cierre (alta) | Codificado (medicamento) |

Los detalles de la prescripción (dosis, frecuencia, duración) se precisan en el paso 4 según la guía.

### DAU en PDF

| Campo | Obligatorio / opcional / derivado | Origen | Forma |
|---|---|---|---|
| Tipo de documento | Obligatorio al cierre (resumen de alta LOINC 59258-4, o nota de urgencia LOINC 34111-5 en abandono; en NEA puede no existir) | Cierre | Codificado (LOINC) |
| URL del adjunto | Obligatoria cuando el documento existe | Cierre | Estructurado (URL, con autenticación) |
| Seguridad (documento restringido) | Condicional: `meta.security = R` en episodios restringidos | Cierre | Codificado |

## Calidad y propiedad de los datos

| Entidad | Quién la posee | Quién puede cambiarla | Con qué frecuencia cambia | Qué pasa si falta | Qué pasa si se duplica o está desactualizada |
|---|---|---|---|---|---|
| Persona atendida | HIS/RCE (admisión); la identidad la resuelve el MPI | Admisión (doble verificador) | Una vez por episodio (la identidad no cambia durante la atención) | Sin RUN se usan los alternativos (pasaporte, RUN de la madre, identificador local, NN) | Las identidades duplicadas las resuelve el MPI con referencias cruzadas |
| Episodio de urgencia | HIS/RCE | HIS/RCE, en los tres eventos | En cada evento (se envía completo y actualizado cada vez, por PUT condicional por ID DAU) | Sin ID DAU no se puede publicar el evento: es el identificador del episodio | El ID DAU nunca se reutiliza, así que no hay duplicados por identificador; una actualización tardía se resuelve porque cada transacción envía el episodio completo |
| Establecimiento | El establecimiento (código DEIS nacional) | MINSAL (el código DEIS no cambia) | Casi nunca | Sin código DEIS no se puede identificar el origen ni el destino | El código DEIS es único por establecimiento |
| Profesional | HIS/RCE | El profesional que atiende | Por episodio | Es opcional: el evento se publica igual | No aplica |
| Hipótesis diagnóstica | HIS/RCE | El equipo clínico | Durante la atención | En NEA puede no existir: el aviso lo registra como condicional | No aplica (la hipótesis provisional se reemplaza por el diagnóstico de egreso al cerrar) |
| Diagnóstico de egreso | HIS/RCE | El Terminador | Al cierre | Es obligatorio en alta: el evento de alta no está completo sin él | Los diagnósticos descartados no se informan |
| Medicamento al alta | HIS/RCE | El Terminador | Al cierre | Si no existen, el aviso no lleva el dato; en abandono no hay | No aplica |
| DAU en PDF | HIS/RCE (lo genera al cerrar) | HIS/RCE | Al cierre | En NEA puede no existir: el aviso lo registra como condicional | El PDF se descarga por su URL con autenticación; una versión nueva del documento reemplaza la anterior |
| Bus, Repositorio, MPI | MINSAL (infraestructura nacional) | MINSAL | Continua (el Bus valida perfil y terminología en cada transacción) | El Bus rechaza la transacción si no cumple el perfil o la terminología | El Bus resuelve la identidad contra el MPI en cada transacción |

## Validación

Pendiente: las entidades y sus datos se presentan al usuario para validación. Sin validación no se avanza a la propuesta FHIR (paso 4).
