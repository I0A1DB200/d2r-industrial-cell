# Expulsión OK por contacto y transferencia a rampa

2026-10-30. Base del paquete: a6b121b6acd8b6665358c6483d6ab4c5f745670b. Rama visual/industrial-v1.2.

## Contrato conservado

Grupo sort=(1.25,0,0), carrera lógica1.48, Watch0…200mm con la conversión anterior. SORT_STOP .5s, DISCHARGE2.2s y PUSH_RETRACT1.1s; FEED.8 y el resto de fases intactos. Intervalo.9, lote4 OK/3 NOK, I/O, diagnósticos, contadores y Safety no cambian. La declaración de señales, fases, Watch y snapshots, el control temporal de update y el bloque de conteo/transiciones se comparan byte a byte con V0 mediante tests/protected_contract.py. El tramo gráfico NOK original también se conserva.

## Geometría y movimiento

Placa local(0,1.385,.80), .59×.16×.075. Cara de empuje en reposo.7625, fuera del borde de cinta.55; borde inferior1.305 por encima de cara superior1.2925. Placa y vástago son hijos de arm, cuyo reposo es0; cuerpo y tapas son hijos fijos de sort. Cuerpo centro(0,1.385,2.20), longitud1.80/radio.13, boca1.30 y trasera3.10. El vástago conserva extremo posterior1.35 dentro del cuerpo; su centro y longitud se calculan hasta el reverso de la placa, arm.z+.8375. Apoyos bajo el cuerpo, sin desplazarlo junto al carro.

Durante SORT_STOP la pieza se mantiene(1.25,1.36,0). En empuje OK se conserva q=ease(elapsed/2.2), arm.z=-1.48q y pieza.z=min(0,.7625+arm.z-.19). La pieza espera hasta el contacto; después su cara posterior y la cara de empuje coinciden, sin montar la pieza sobre la placa. Al completar el empuje, centroZ=-.9075 y cara posterior=-.7175: la pieza completa está fuera de cinta. Retorno1.1s: arm.z=-1.48(1-q), sin arrastrarla. Los tres NOK mantienen arm=0 y su recorrido anterior.

Puente horizontal Z=-.55…-.7175, cara superior1.2925. Rampa de ancho.88 hastaZ=-2.25, desnivel.54 y pendiente atan2(.54,1.5325). Su sólido se centra compensando media altura en la normal del plano, de modo que la **cara superior**, no su eje, une ambos extremos. Guías laterales sobre el plano.

Primera cuarta parte de retorno: basculación alrededor de la esquina inferior trasera. Resto: deslizamiento paralelo a la rampa. Se usan las fórmulas aprobadas con tilt=ease(u/.25), slide=ease((u-.25)/.75), pitch=-slope*tilt; ease conserva el clamp[0,1]. La altura del centro incluye .0675/cos(slope), evitando introducir las esquinas inferiores en la rampa. Al final hay voladizo sobre la caja; no se afirma una simulación de apoyo/fricción o caída física.

Se fija poseOKExit(1) antes de ocultar y contar. No se añade un frame, pausa ni retraso al conteo: en el instante de fin original se guarda la pose terminal exacta, aunque el último frame visible depende de la cadencia de render. Cada siguiente clearPiece elimina la inclinación.

## Pasos visuales

Se interrumpen las guías de cinta y se dividen los dos paneles transparentes. El hueco orientativo.84…1.66 resultó más estrecho que el exterior de las guías de rampa (.80…1.70). Se amplía a **.78…1.72**, dejando.02 de margen por lado. Esto se comprueba sobre vértices de los meshes de barrera, no solo sobre sus centros. No se cambia Safety ni se presenta el cerramiento abierto como solución certificada.

Vista sort: cámara[6.1,3.6,-.8], objetivo[1.25,1.35,.6]. Se conservan los cinco botones de vistas y el estilo ACES/PMREM del paquete anterior.

## Pruebas e instrucciones

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/check_transfer.py
python tests/check_transfer_geometry.py
CHROMIUM_PATH=/usr/bin/chromium python tests/check_controls.py --ui-only
CHROMIUM_PATH=/usr/bin/chromium python tests/check_visual.py
```

Todos usan HTTP automático, Chromium, clics reales y observación CDP externa; no sustituyen funciones ni reloj. Las capturas arrival, approach, contact y return se toman usando la pausa real de SIM. Capturas800×600 y muestreo de lote256×192 para software. Para acciones HMI se vuelve a390×844; la resolución pequeña de muestreo no es un diseño de pantalla HMI soportado.

Resultado final sobre el HTML de este paquete:

- Transferencia completa: **38 PASS, salida0**. Cuatro poses terminales OK exactas y tres NOK originales; siete poses de fin observadas. Contacto, espera, retorno sin arrastre, pieza fuera de cinta, esquinas inferiores sin penetrar puente/rampa, vástago unido, cuerpo fijo, todos los NOK con arm0. F01/F02 enclavan diagnóstico y RESET HMI libera el fallo y recarga siete piezas. Cero pageerror, incluidos los intervalos entre piezas.
- Revalidación de mandos final: **25 PASS, salida0** con Watch y Alarmas en los tres tamaños pedidos; clics reales, pausa compartida, RESET y metadatos inmediatos. Capturas finales en [controls-final](../tests/evidence/controls-final/).
- Render/configuración y contratos protegidos: **28 PASS, salida0**. Conserva ACES, PMREM, una sombra2048, frustum, dimensiones de cajas, texturas, cilindros32, cristal sin sombras y DPR recalculado. Los bloques funcionales protegidos coinciden con V0; la UI y las trayectorias autorizadas se verifican por sus contratos actuales en lugar de exigir igualdad con V0.
- Validación geométrica posterior: **2 PASS**, sobre poses retenidas de la ejecución real. Tres muestras de la primera cuarta parte mantienen fija la esquina inferior trasera; ocho de deslizamiento conservan pitch y ambos bordes inferiores alineados al plano. Es postanálisis de esas muestras, no una simulación nueva ni cobertura de todos los frames.
- V0 conserva SHA256 y se pasó git diff --check. No se añadieron dependencias o assets de producción.

[Resultados, capturas y hashes](../tests/evidence/transfer/). Las cinco capturas finales **rest, arrival, approach, contact y return** corresponden al mismo SHA256 que los informes finales. Se revisaron visualmente. El lote completo se repitió después de ampliar el hueco a.78…1.72; la evidencia final no corresponde al hueco anterior. Los informes iniciales fallidos se conservan separados y no se presentan como PASS.

Un primer ensayo pasó el lote y las comprobaciones de transferencia, pero falló después al intentar pulsar HMI RESET a256×192: SIM interceptaba el clic. Se conserva el informe original como fallo de infraestructura/uso del viewport de muestreo para una acción HMI (clasificación F). El runner se corrigió para volver a390×844 y se repitió la ejecución completa. No se usó force ni se alteró el simulador para superar ese fallo.

El primer ensayo de resize también leyó DPR1.25 junto con el tamaño anterior810×610 antes de procesarse el evento. Se conservó ese FAIL y se sustituyó la espera fija del ensayo por sondeo de la condición real (DPR y tamaño esperados, límite30s). La repetición completa del comprobador visual pasó sin modificar el código del producto. Se clasifica como sincronización de observación/infraestructura, no como cambio del reloj o reparación de render.

## Límites

Es geometría y animación cinemática, no una simulación neumática ni dinámica. El ensayo comprueba caras de contacto, extremos de vástagos y esquinas inferiores contra el plano de puente/rampa; no acredita tolerancias, esfuerzos, fricción, colisiones CAD universales ni Safety real. Las muestras persistidas están reducidas; las aserciones se calculan antes de reducirlas. La baja cadencia de SwiftShader no representa una GPU de usuario y no se compensa cambiando el reloj.
