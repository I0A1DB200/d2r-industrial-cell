# Mandos y cilindros · paquete 1

2026-10-30. Base: a2c05f705addccfd0b62ebe6f843664bd233f08d; rama visual/industrial-v1.2.

HMI PAUSA/REANUDAR delega mediante click al botón SIM. START y FIN DE PIEZA de HMI también delegan en SIM. Una sola función de presentación sincroniza texto, disabled, title, aria-label, aria-disabled, aria-pressed y selección de ambos planos. Las acciones actualizan la presentación inmediatamente, sin esperar el siguiente frame. RESET de HMI continúa bloqueado durante marcha, incluida pausa; RESET de SIM conserva su disponibilidad durante marcha. STOP conserva la petición de fin de pieza: no detiene el movimiento inmediatamente.

La presentación detecta betweenCycles>0 antes de consultar la fase y muestra ENTRE PIEZAS. No cambia .9 s, fases, secuencia ni condiciones de transición. Se conservan I/O, contadores, clasificación y Safety. Durante el intervalo, STOP mantiene el comportamiento anterior: termina la siguiente pieza que el ciclo original inicia; no se ha añadido una transición de parada nueva.

Los cuerpos y tapas de ambos cilindros están fijos. Los vástagos cambian de longitud y centro para mantener un extremo interno fijo y el otro unido al móvil. C02 utiliza cuerpo Z=2.20, longitud1.80, anclaje1.35 y unión al reverso de la placa; el cuerpo no está dentro de arm. El alimentador todavía conserva la trayectoria anterior en este paquete; su cargador/corredera se reconstruye en el paquete siguiente.

Responsive: panel inferior en 390×844, SIM compacta con scroll; reserva lateral para HMI en 640×360; Watch/Alarmas comparten el mismo contenedor, sin superponer mandos. HMI tiene scroll propio cuando la altura es limitada.

## Pruebas ejecutadas

`CHROMIUM_PATH=/usr/bin/chromium python tests/check_controls.py`

Playwright, HTTP local automático, Chromium y adaptador CDP separado de solo lectura. Sin sustituir funciones ni reloj. Clics reales, sin force. Resultado: todas las comprobaciones PASS, salida0; cero pageerror.

- 390×844, 960×600, 640×360 con Watch abierto: cajas de Watch sin intersección con HMI o SIM; START HMI, PAUSA HMI, reanudación SIM, RESET SIM durante marcha y RESET HMI parado comprobados.
- Pausa congela elapsed y posición; pares de metadatos sincronizados; disabled de RESET HMI inmediato.
- Rod C02 unido a placa durante empuje y extremo fijo1.35 dentro del cuerpo; alimentador unido al empujador con anclaje dentro del cuerpo.
- AUTO: intervalo con phase7 observado y texto ENTRE PIEZAS, sin excepción. STOP HMI solicitado durante intervalo completa la siguiente pieza, sin parada inmediata. STOP SIM durante transporte termina una pieza.

[Resultados y capturas](../tests/evidence/controls/). Se revisaron visualmente las tres capturas. La comprobación geométrica mide rod y cuerpo; no acredita neumática real. No es una certificación Safety.

El lote de siete se comprobó posteriormente con las nuevas trayectorias finales; véanse los informes de alimentador y transferencia. V0 permanece inmutable. Las comparaciones históricas de igualdad total de UI/funciones/posiciones de v1.2 dejan de ser aplicables a estos cambios explícitamente autorizados; no deben usarse para negar el nuevo alcance.

## Revalidación con la geometría final

`python tests/check_controls.py --ui-only`: 25 PASS en el HTML final, Watch y Alarmas abiertos en390×844,960×600,640×360, sin pageerror. Capturas y fuente identificada por SHA256 en [controls-final](../tests/evidence/controls-final/). Las pruebas temporales de STOP/intervalo siguen documentadas en el primer paquete, y el lote final completo de transferencia vuelve a cubrir todos los intervalos sin excepción.
