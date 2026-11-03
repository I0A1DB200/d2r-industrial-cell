# Vista técnica y sensores compactos

La vista `TÉC` ofrece una presentación clara inspirada en la ilustración aportada: fondo y suelo claros, materiales más mates, protecciones con borde cian fino y sin cuadrícula. El aspecto industrial actual sigue disponible y es el modo inicial. El cambio de estilo también se puede abrir directamente con `?style=technical`.

Los seis sensores visibles usan ahora una carcasa rectangular de `0.16 × 0.09 × 0.12` unidades, sin poste ni esfera grande. Cada carcasa tiene dos LED pequeños en la cara superior:

- Verde fijo: indicador visual de alimentación simulada; no representa una medición de tensión real.
- Cian: estado activo de la entrada DI existente cuando la señal detecta una pieza. En reposo queda apagado.

PLC Watch conserva sus etiquetas y posiciones ilustrativas. Seleccionar una fila sigue centrando la cámara en el marcador asociado.

No se modificaron fases, duraciones, I/O, contadores, clasificación, trayectorias, lógica PLC ni Safety. No se añadieron dependencias.

## Validación ejecutada

- `tests/check_visual.py`: 28 comprobaciones PASS, incluida la huella de V0, la configuración visual existente, el límite DPR y la ausencia de errores JavaScript.
- `tests/check_controls.py --ui-only`: controles y paneles PASS a 390×844, 960×600 y 640×360; sin errores JavaScript.
- En Chromium, el botón `TÉC` activó el perfil técnico y el control HMI START llevó `DI_InspectionPresent` a `1` al llegar la pieza a inspección.

Las pruebas usan el simulador cinemático y Chromium con renderizado por software. No validan sensores, tensión ni rendimiento de GPU físicos.
