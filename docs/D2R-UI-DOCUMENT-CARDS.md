# Imágenes de las cards de documentación

## Criterio visual

Las miniaturas se capturan del render 3D existente, usando sus vistas de cámara. Se muestran los mecanismos y elementos que aparecen en la célula; no se añadieron equipos, cableado ni dispositivos de Safety que el modelo no represente. Los enlaces y documentos de cada card mantienen su funcionamiento.

Cada imagen se distribuye a 640 × 360 px en JPEG optimizado. La interfaz usa la misma proporción y recorta solo lo necesario para ajustarse a la miniatura.

| Card | Imagen | Vista del simulador |
|---|---|---|
| 00 · Brief del cliente | `assets/cards/cell-overview.jpg` | General |
| 01 · Especificación funcional | `assets/cards/process-flow.jpg` | General, acercamiento al flujo |
| 02 · Diseño mecánico, eléctrico y neumático | `assets/cards/gravity-feeder.jpg` | Alimentador |
| 03 · Componentes, hardware y E/S | `assets/cards/control-cabinet.jpg` | Armario de control |
| 04 · Safety Engineering | `assets/cards/safety-guard.jpg` | Resguardo y estación de inspección |
| 05 · Arquitectura PLC | `assets/cards/plc-architecture.jpg` | Armario de control, vista cercana |
| 06 · Programación, HMI y visión | `assets/cards/vision-inspection.jpg` | Cámara de inspección |
| 07 · Proyecto y commissioning | `assets/cards/sorting-pusher.jpg` | Expulsor y rampa |

Las imágenes describen el modelo didáctico. El armario no representa una selección de hardware aprobada, la cámara es parte de la simulación y la vista del resguardo no constituye una solución Safety validada.

## Comprobación visual

En Chromium, las ocho imágenes cargaron a 640 px de ancho en `960 × 600` y `393 × 844`. Los textos e imágenes caben en sus cards, la página no presenta scroll horizontal y no aparecieron errores JavaScript. Se comprobó que el canvas 3D sigue visible detrás del panel de documentación.

Capturas:

- [Cards en 960 × 600](evidence/docs-cards-960x600.png)
- [Cards en 393 × 844](evidence/docs-cards-393x844.png)
