# 02 · Diseño mecánico, eléctrico y neumático

**Estado:** borrador didáctico v0.1 · revisión pendiente  
**Objetivo:** traducir la secuencia funcional a estaciones, accionamientos, sensores y documentos de diseño coordinados.

> La geometría del HTML es una representación visual. No es CAD liberado, plano de fabricación ni cálculo estructural.

## Disposición funcional propuesta

| Estación | Función | Elementos que deben definirse en ingeniería |
| --- | --- | --- |
| Alimentador | Presentar una pieza cada vez desde el cargador. | Cargador, guías, retención, empujador, cilindro, reposición y detección de nivel/pieza. |
| Transporte | Llevar la pieza a inspección y clasificación. | Cinta, accionamiento, rodillos, guías, estructura y confirmación de movimiento. |
| Inspección | Iluminar, capturar y evaluar la pieza detenida. | Soporte de cámara, óptica, iluminación, protección frente a luz ambiente y referencia de pieza. |
| Salida A | Desviar piezas OK con expulsor lateral y rampa. | Carrera útil, guiado, topes, contenedor y confirmación de salida. |
| Salida B | Entregar piezas NOK al final de la cinta. | Transferencia, contenedor, retención y confirmación de salida. |

El armario que aparece junto al alimentador solo establece una referencia visual; su posición final depende de accesibilidad, cableado, ambiente y requisitos de mantenimiento.

## Interfaces eléctricas y de control

Como concepto inicial, las entradas discretas representan presencia, posición retraída/extendida y confirmación de salida. Las salidas representan mando de cinta, válvulas y disparo de visión. La alimentación, tipo de señal, protección, conectores, puesta a tierra, segregación de potencia/control y esquema de red siguen pendientes.

La conexión de la cámara Cognex se modelará como equipo externo: disparo desde control y retorno de disponibilidad, captura y resultado. No hay cámara, enlace de datos ni DB externa conectada actualmente.

## Concepto neumático

El modelo visual representa un mecanismo de alimentación y un expulsor con cilindro. La selección real requiere carga, carrera, velocidad, ciclo, presión disponible, guiado, amortiguación, detección de extremos y evaluación de consumo. El esquema debe mostrar unidad de preparación, válvulas, puertos, actuadores, sensores y estado ante pérdida de energía o aire, decidido mediante el análisis de riesgos.

## Paquete de diseño que se debe producir

- Layout 2D/3D con cotas, interfaces, mantenimiento y reposición de piezas.
- Planos de conjunto y detalle, lista de materiales y tolerancias de fabricación.
- Esquema eléctrico, distribución de 24 VDC, protecciones, bornes, cableado y lista de cables.
- Esquema neumático, lista de válvulas/actuadores y tabla de estados.
- Tabla de interfaces entre mecánica, electricidad, PLC, cámara y Safety.

## Verificación de diseño

Revisar colisiones, alcance del operador, extracción de contenedores, visibilidad de cámara, acceso a sensores y actuadores, mantenimiento y protección de cables/mangueras. Confirmar que cada sensor puede ajustarse y sustituirse sin desmontajes no previstos. Las capturas del simulador sirven para explicar disposición y secuencia; no demuestran distancias de seguridad, resistencia, ergonomía ni prestaciones reales.

**Trazabilidad:** `REQ-001`…`REQ-003`, `REQ-008` y `REQ-009`.  
**Pendiente:** planos, dimensiones de producto, cargas, energía disponible, entorno y revisión de riesgos.
