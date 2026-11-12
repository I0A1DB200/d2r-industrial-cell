# 02 · Diseño mecánico, eléctrico y neumático

**Estado:** borrador didáctico v0.2 · revisión pendiente
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

## Desglose del conjunto mecánico representado

| Subconjunto | Función de proceso | Confirmado en el HTML | Ingeniería real pendiente |
| --- | --- | --- | --- |
| Cargador por gravedad | Mantener varias piezas y presentar la inferior. | Cuatro guías abiertas; una pieza activa y hasta seis superiores; descenso visual después de extraerla. | Tolerancias de pieza, capacidad, recarga, retención, atasco y detección de cargador vacío. |
| Empujador de alimentación | Extraer la pieza inferior y transferirla a cinta. | Corredera, empujador, lengüeta de apoyo y cilindro visual orientado +X. | Carga, pandeo, guiado, fuerza, carrera, amortiguación y protección de punto de atrapamiento. |
| Cinta | Transportar e inmovilizar la pieza durante inspección. | Plataforma y cinta con superficie superior compartida; rodillos y guías laterales. | Dimensiones de producto, velocidad requerida, motor/reductor, tensión de banda y detección de movimiento. |
| Pórtico de visión | Posicionar cámara e iluminación sobre pieza detenida. | Cámara gráfica cenital, soporte, luz y cono de iluminación visual. | Campo de visión, profundidad de campo, óptica, luz real, soporte y validación de capacidad de inspección. |
| Expulsor lateral | Retirar piezas OK por contacto hacia salida A. | Placa fija a corredera móvil, vástago vinculado, puente horizontal y rampa inclinada. | Fuerza, guiado, empuje permitido, diseño del borde, desgaste, salida de pieza y resguardo. |
| Salida B | Recibir piezas NOK al final del transporte. | Tramo final y caja de recogida ilustrados. | Altura de caída, acumulación, retirada, presencia y capacidad del contenedor. |

### Referencias de la geometría visual

Estas coordenadas y dimensiones sirven para leer el modelo, no para fabricar. El HTML usa unidades gráficas sin tolerancia ni escala CAD validada.

| Referencia del modelo | Valor representado | Nota |
| --- | --- | --- |
| Origen de grupo alimentador | `x = -2.98`; eje local `x = -1.02` (mundial `x ≈ -4`) | Ubicación visual relativa a la cinta. |
| Pieza 3D | `0.52 × 0.135 × 0.38` | Caja visual con cinco taladros simulados. |
| Paso de pila | `0.135` | Una pieza inferior activa más hasta seis piezas superiores. |
| Superficie superior de cinta | `y = 1.2925` | Coincide visualmente con la cara inferior de pieza. |
| Cuerpo cilíndrico de expulsor | Longitud `1.80`, radio `0.13`, centro local `(0, 1.385, 2.20)` | Cuerpo y tapas fijos en el grupo sort. |
| Placa de expulsor | `(0, 1.385, 0.80)`, `0.59 × 0.16 × 0.075` | En reposo su cara queda fuera del borde de cinta. |
| Carrera gráfica de expulsor | `1.48` | El vástago acompaña a la corredera; no representa una carrera seleccionada. |
| Holgura visual placa/cinta | Cara de empuje reposo `z=0.7625`; borde cinta `z=0.55`; cara inferior placa `y=1.305`. | La placa queda fuera del paso y sobre la superficie superior; no incluye tolerancias. |

| Componentes de la cinta | Referencia visual | Observación |
| --- | --- | --- |
| Plataforma principal | Centro `y=1.13`, altura `0.215`. | Cara superior coincide con cara inferior de cinta. |
| Cinta | Centro `y=1.265`, espesor `0.055`; cara superior `y=1.2925`. | Material y textura solo gráficos. |
| Rodillos extremos | Centro `y=1.13`, radio `0.16`. | No se modela eje, accionamiento ni transmisión real. |
| Guías de pieza | Aproximadamente `y=1.31`. | No representan cálculo de contención de producto. |
| Puente salida A | Superficie superior `y=1.2925`; desde borde de cinta a `z≈-0.7175` local sort. | Alineación de transferencia visual. |
| Rampa A | Ancho gráfico `0.88`, fin aproximado `z=-2.25`, desnivel `0.54`. | Pendiente visual; falta cálculo de caída, fricción y acumulación. |

### Trayectoria visual del alimentador

Dentro de `FEED` (0,8 s del modelo): `0–0,45` avanza el empujador (carrera visual de `1,0`) y la pieza inferior pasa de `x=-4` a `x=-3`; `0,45–0,75` vuelve el carro mientras la pieza permanece en `x=-3`; `0,75–0,78` espera; `0,78–1,00` desciende la pila animada cuadráticamente un paso de `0,135`. La lengüeta trasera sostiene visualmente la pila durante el avance y se retira antes del descenso. Esto es cinemática gráfica, no cálculo por gravedad ni un accionamiento real validado.

### Trayectoria visual del expulsor OK

El grupo sort está en `x=1,25`. En `SORT_STOP` la pieza queda detenida; durante `DISCHARGE` la placa se aproxima y empuja por contacto, con desplazamiento de la pieza limitado a cero hasta que su cara llega a la placa. En `PUSH_RETRACT`, la pieza OK bascula al inicio de la trayectoria y luego sigue la rampa mientras el cilindro retorna. Las piezas NOK siguen transporte de cinta a B y no activan el expulsor. Son reglas del modelo que sirven para explicar interfaces y movimiento; no representan fuerza, fricción o gravedad simuladas.

La geometría de rampa y de la pieza OK está ajustada para continuidad visual. Sus ángulos, alturas y trayectorias no son resultados de cálculo de caída, fricción ni dimensionamiento.

## Arquitectura eléctrica candidata

El siguiente esquema muestra límites funcionales posibles; no es una conexión aprobada ni define el tipo de señal:

```text
Sensores de presencia/posición ──> entradas del PLC
HMI de operador ────────────────> comandos / estados en PLC
PLC ──> accionamiento de cinta
PLC ──> válvula de alimentación y válvula de expulsor
PLC ──> input Trigger de cámara (E/S o red, por decidir)
Cámara ──> Ready / Done / Valid / Resultado hacia DB de intercambio PLC
Dispositivos Safety ──> sistema Safety independiente, por diseñar y validar
```

Las líneas no significan que el equipo esté instalado. Confirmar arquitectura de red, alimentación, aislamiento, referencias comunes, protección y diagnóstico antes de realizar un esquema eléctrico.

## Tabla de interfaces entre disciplinas

| Interfaz | Define | Entrega al siguiente equipo | Revisión conjunta |
| --- | --- | --- | --- |
| Pieza ↔ alimentador | Envolvente, masa, orientación y tolerancias. | Plano de pieza y condiciones de variación. | Mecánica + proceso. |
| Cinta ↔ visión | Velocidad, parada, posición repetible y vibración admisible. | Ventana de captura y señal de pieza presente. | Mecánica + control + visión. |
| PLC ↔ Cognex | Trigger, job/receta, resultado, validez, diagnóstico y timeout. | Tabla de datos versionada y herramienta de configuración. | Control + visión + cliente. |
| Expulsor ↔ pieza/rampa | Cara de contacto, fuerza, carrera, orientación y salida completa. | Envolvente de movimiento y confirmación de A. | Mecánica + control + mantenimiento. |
| Electricidad ↔ neumática | Válvula, tensión, presión, sensores de extremo y retorno. | Lista de bornes/tags y esquema neumático. | Electricidad + mecánica + control. |

## Revisión previa a congelar el diseño

Completar primero dimensiones y peso de pieza, estabilidad del producto sobre cinta, producción requerida, variaciones del cargador, tiempo de exposición de cámara, energía disponible, espacio de contenedores y accesos de mantenimiento. Después ejecutar revisiones de interferencias, ergonomía y cableado. Ninguno de estos valores se deduce de la vista 3D.
