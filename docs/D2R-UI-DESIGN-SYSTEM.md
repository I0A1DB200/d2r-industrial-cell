# Sistema visual D2R para interfaces de simulación

## Propósito

Fijar una pauta reutilizable para la marca, encabezado, botoneras, paneles y estados de las experiencias 3D de Digital2Real. Este sistema regula la presentación; no define comportamiento PLC, Safety ni lógica de proceso.

## Fuente de verdad

Los tokens se declaran en `:root` dentro de `D2R-3D-001_Prototipo_Funcional_v11.html`. La vista técnica clara redefine los tokens de superficie y estado en `body.technical-view`. Los estilos de los controles visibles deben consumir estos tokens en vez de introducir nuevos valores hexadecimales.

| Token | Valor industrial | Uso |
|---|---|---|
| `--d2r-brand` | `#EF832E` | Marca y selección persistente |
| `--d2r-brand-contrast` | `#10151C` | Texto sobre fondo de marca |
| `--d2r-canvas` | `#0B111A` | Fondo oscuro de la escena |
| `--d2r-panel` | `#101A27EE` | Paneles flotantes |
| `--d2r-panel-raised` | `#111D2BF7` | Panel lateral elevado |
| `--d2r-control` / `--d2r-control-border` | `#223347` / `#53677E` | Botón sin seleccionar |
| `--d2r-control-hover` / `--d2r-control-hover-border` | `#30475D` / `#71879D` | Hover; se distingue de la selección |
| `--d2r-text` / `--d2r-text-muted` | `#E9EEF7` / `#91A4B7` | Texto principal y secundario |
| `--d2r-ready` | `#34D399` | READY y resultado OK |
| `--d2r-run` | `#18E8FF` | Máquina en marcha |
| `--d2r-warning` | `#FA8A47` | Atención o pausa |
| `--d2r-stop` | `#F47C69` | FIN DE PIEZA, NOK y estado visual FAULT; no es una indicación Safety |
| `--d2r-radius-control` / `--d2r-radius-panel` | `8px` / `12px` | Esquinas de controles y paneles |

La vista técnica utiliza superficies claras y variantes más oscuras de los colores de estado para mantener legibilidad. La acentuación cian del botón TÉC solo identifica el estilo técnico activo. El lector de documentos conserva su barra oscura con un ámbito de tokens propio, aunque se abra desde la vista técnica.

## Estados de botones

1. **Normal:** fondo pizarra, borde visible y texto claro.
2. **Hover:** aclarado discreto; no utiliza el naranja de selección.
3. **Seleccionado/activo:** naranja D2R con texto oscuro. Se reserva para vista, pestaña o modo que continúa activo.
4. **Deshabilitado:** opacidad reducida, cursor de no disponible y sin cambio por hover. Un control puede estar deshabilitado y activo durante una marcha; en ese caso conserva su indicador activo.
5. **Foco de teclado:** contorno visible de 2 px.

START y FIN DE PIEZA conservan botones neutros; sus iconos usan acentos verde y coral. AUTO/PIEZA, navegación y pestañas usan el naranja cuando representan una selección persistente. El naranja no representa un estado de Safety.

## Encabezado D2R

Mantener esta jerarquía:

- `D2R`: marca en naranja.
- Nombre de la célula: texto principal, por ejemplo `Inspection Cell`.
- Producto/versión: metadato secundario, por ejemplo `Engineering Lab · v1.0`.
- Estado actual: `READY`, `RUN`, `PAUSED` o `FAULT`, con color semántico y texto; el estado no depende solo del color.

En el encabezado y los LED del HMI se usa la misma asignación: READY verde, RUN cian, PAUSED ámbar y FAULT coral.

## Organización de CSS

- Declarar los valores visuales compartidos en `:root`.
- Consumir tokens desde las reglas de encabezado, controles, paneles y lector documental.
- Sobrescribir los mismos tokens para temas alternativos; evitar duplicar toda la hoja de estilos.
- Mantener los tamaños compactos actuales como tokens (`--d2r-control-size`, `--d2r-control-size-compact`, `--d2r-control-size-short`) porque dependen del viewport.
- No vincular colores CSS a transiciones de máquina. La UI puede leer el estado para reflejarlo, pero estos estilos no lo modifican.

## Comportamiento responsive

- Hasta 530 px de ancho, el HMI ocupa el ancho disponible debajo de la barra de vistas; PLC Watch usa un panel inferior desplazable y la barra SIM queda compacta.
- En horizontal con menos de 500 px de alto y más de 530 px de ancho, cabecera y vistas comparten la fila superior. El HMI conserva su columna izquierda y PLC Watch empieza debajo de esa fila en la columna derecha; no tapa los cinco selectores.
- Entre 531 y 820 px de ancho, reducir márgenes y controles sin ocultar acciones ni provocar desplazamiento horizontal de página.
- El contenido de PLC Watch puede desplazarse dentro del panel. La botonera SIM permanece accesible en el borde inferior.
- Tras cambiar posiciones, comprobar `390×844`, `960×600` y `640×360` con PLC Watch abierto. Revisar límites y solapamientos de cabecera, vistas, HMI, Watch y barra SIM.

## Criterios al replicarlo en otra experiencia

- Copiar los tokens, no los selectores ligados a IDs específicos de esta célula.
- Aplicar la misma jerarquía D2R y las mismas reglas de interacción.
- Usar texto, icono y color para identificar estados; no comunicar estados críticos solo con color.
- No presentar un indicador Safety como función certificada ni como dispositivo real.
- Añadir un token nuevo solo cuando tenga un uso semántico estable y no encaje en uno existente.

## Verificación visual ejecutada

Con PLC Watch abierto en Chromium, las vistas `390×844`, `960×600` y `640×360` se renderizaron sin errores JavaScript ni scroll horizontal de página. En las tres se ven los cinco selectores de vista, no hay solapamientos entre cabecera, vistas, HMI, Watch y barra SIM, y Watch permanece desplazable. En `640×360`, los cinco botones de vista comparten la fila superior con la cabecera y la primera fila de tags queda visible.

Capturas:

- [390×844 · móvil vertical](evidence/ui-mobile-390x844.png)
- [960×600 · ventana media](evidence/ui-responsive-960x600.png)
- [640×360 · horizontal bajo](evidence/ui-landscape-low-640x360.png)

La revisión utilizó Chromium con renderizado WebGL por software y el módulo Three.js r164 ya utilizado por el simulador. Es evidencia de layout en navegador, no una prueba en teléfonos físicos ni una medición de GPU de usuario.

## Alcance y verificación

Este sistema cubre estilos de interfaz y el indicador de estado del encabezado. No cambia geometría, iluminación, secuencia, señales, contadores, clasificación ni Safety. El criterio es visual; los colores no representan requisitos normativos de HMI ni certificación industrial.
