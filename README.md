# d2r-industrial-cell
D2R Industrial Inspection Cell - Three.js, PLC Simulation &amp; Engineering Experiences

## QA baseline V0

Infraestructura Playwright + Chromium con servidor HTTP automático, observación
CDP y referencia original verificada por SHA256. Instrucciones y limitaciones:
[docs/D2R-3D-BASELINE.md](docs/D2R-3D-BASELINE.md).

```sh
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/run_baseline.py
```

Un FAIL por errores JavaScript se conserva como fallo; consultar el informe
`test-results/baseline/results.json`, incluso si el lote llegó a 7 piezas.

Mejora visual industrial y cinco vistas capturadas:
[docs/D2R-3D-VISUAL-v1.2.md](docs/D2R-3D-VISUAL-v1.2.md).

## Mandos y mecanismos actuales

La referencia V0 conserva el fallo histórico de `refreshUX`. El HTML actual
se valida con los contratos y ensayos de los nuevos mecanismos:

- [Mandos SIM/HMI y cilindros](docs/D2R-3D-CONTROLS-ACTUATORS.md).
- [Alimentador de siete piezas](docs/D2R-3D-GRAVITY-FEEDER.md).
- [Transferencia OK por contacto](docs/D2R-3D-PUSHER-TRANSFER.md).

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/check_controls.py --ui-only
CHROMIUM_PATH=/usr/bin/chromium python tests/check_feeder.py
CHROMIUM_PATH=/usr/bin/chromium python tests/check_transfer.py
python tests/check_transfer_geometry.py
CHROMIUM_PATH=/usr/bin/chromium python tests/check_visual.py
```
