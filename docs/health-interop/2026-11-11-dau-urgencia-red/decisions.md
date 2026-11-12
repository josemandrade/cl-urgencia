# Decisions — dau-urgencia-red

## 2026-11-11 — El repaso IHE temprano se hizo al inicio del paso 3, no antes del BPMN

- Context: la skill `ihe-landscape-scan` se creó en el pack cuando el BPMN v4 ya estaba modelado y validado. El flujo del componente dice que el repaso corre tras validar la spec y antes del BPMN.
- Decision: en esta prueba el repaso se hizo al inicio del paso 3 y quedó registrado en `02-bpmn-model.md`, con los candidatos por punto de interoperabilidad, para que el paso 4 los confirme o refute.
- Alternatives considered: rehacer el BPMN con el repaso en mente. Rechazado: el BPMN ya estaba validado; el repaso no cambia el modelo, solo anota los candidatos.
- Consequences: en los próximos casos el repaso corre antes del BPMN; en esta prueba el BPMN se dibujó sin él.

## 2026-11-11 — El estudio IHE va en dos momentos

- Context: el usuario cuestionó la ubicación del estudio IHE (en el paso 4): como el proceso se obtiene y se aclara con una guía, quizás el estudio IHE debería venir después del brainstorming. La propuesta fue dividirlo en dos momentos.
- Decision: (1) un repaso temprano de perfiles IHE (`ihe-landscape-scan`) tras validar la spec y antes del BPMN, para que el modelo se dibuje con los perfiles en mente; (2) la revisión experta detallada por punto (`ihe-profile-review`) sigue en el paso 4, confirmando o refutando cada candidato.
- Alternatives considered: mover el estudio entero después del brainstorming. Rechazado: la revisión detallada por punto necesita el BPMN y las entidades; sin ellos no se puede juzgar el ajuste.
- Consequences: el componente queda en v0.6.0 local (14 skills); el repaso temprano se escribe en `02-bpmn-model.md`.

## 2026-11-11 — La spec no se redacta desde una descripción de un solo mensaje

- Context: la prueba mostró que el diálogo de brainstorming no se ejerció: la spec se redactó desde la descripción del usuario en un solo mensaje.
- Decision: nueva regla en `brainstorming-health` (v0.6.0): aunque el usuario entregue una descripción completa, el diálogo del brainstorming se hace igual (preguntas, devolución en trozos cortos, esperar corrección) antes de redactar la spec.
- Alternatives considered: ninguna; es el contenido de la skill que no se siguió.
- Consequences: los próximos casos harán el diálogo aunque el usuario describa el caso completo de entrada.

## 2026-11-11 — Se usa el caso DAU urgencia como caso de la prueba

- Context: el usuario pidió probar el componente y luego entregó este caso clínico: el mínimo que un establecimiento debe informar a la red cuando atiende a una persona en su unidad de urgencia.
- Decision: el recorrido de prueba usa este caso real (no uno inventado). La carpeta es `2026-11-11-dau-urgencia-red`.
- Alternatives considered: inventar un caso sintético (presión arterial de APS a cardiología). Rechazado: el usuario dio un caso concreto y dijo "ese es el caso".
- Consequences: la prueba produce la spec, el BPMN, la propuesta FHIR y el componente para este caso.

## 2026-11-11 — Datos sintéticos en toda la prueba

- Context: el caso es clínico y la skill `privacy-safety-health` exige datos sintéticos por defecto.
- Decision: todos los ejemplos, tests y goldens usan datos sintéticos (identificadores SYN-*, establecimientos ficticios). Nada de datos reales de pacientes.
- Alternatives considered: ninguna; es una regla del componente.
- Consequences: los ejemplos no son clínicamente reales; sirven para probar la estructura, no para uso asistencial.

## 2026-11-11 — La prueba se hace en esta sesión, paso a paso

- Context: el agente de prueba se detuvo al denegarse el permiso de terminal, y Codex no tiene credenciales, así que la prueba de aceptación en harness real quedó bloqueada.
- Decision: el usuario eligió que la prueba se haga aquí mismo, paso a paso, siguiendo las skills y sus puertas de validación.
- Alternatives considered: re-autorizar la terminal al agente de prueba; dejar la prueba en pausa. Rechazadas por el usuario al elegir esta opción.
- Consequences: cada paso se presenta al usuario para validación antes de avanzar (puerta dura del paso 1: nada pasa a BPMN sin spec validada).
