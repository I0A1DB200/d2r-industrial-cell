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
