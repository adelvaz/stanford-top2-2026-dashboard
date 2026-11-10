# Los científicos más citados del mundo · Ranking Stanford-Elsevier 2026

Explorador interactivo de la versión 9 (octubre de 2026) de la base de datos *Updated science-wide author databases of standardized citation indicators* (Ioannidis, Baas y Elsevier), conocida como «ranking de Stanford» o «Top 2 %».

**Ver el panel:** https://adelvaz.github.io/stanford-top2-2026-dashboard/

## Qué permite hacer

- **Resumen mundial:** un mapa por países y gráficos por continente, disciplina y tipo de institución, con filtros combinables.
- **Países:** un ranking con la variación respecto a la edición 2025 y un índice de especialización disciplinar.
- **Instituciones:** las principales instituciones según los filtros y un buscador.
- **Disciplinas:** los 20 campos y 174 subcampos Science-Metrix, y el peso de cada continente en cada disciplina.
- **España en detalle:**
  - Universidades por recuento, por cada 100 PDI ETC (equivalente a tiempo completo) y por la razón observados/esperados según su composición por ramas de conocimiento.
  - Un buscador de investigadores.

Todos los análisis se pueden ver para la tabla de trayectoria (citas 1996-2025) o para la del año 2025.

## Datos y método

- Ioannidis, J. P. A. (2026). *August 2026 data-update for "Updated science-wide author databases of standardized citation indicators"* (versión 9). Elsevier Data Repository. https://doi.org/10.17632/btchxktzyw.9 (CC BY-NC 3.0). La comparación usa la versión 8 (https://doi.org/10.17632/btchxktzyw.8).
- Personal docente e investigador: Ministerio de Ciencia, Innovación y Universidades, SIIU, *Estadística de Personal de las Universidades*, curso 2024-2025.
- Mapa: Natural Earth vía [world-atlas](https://github.com/topojson/world-atlas).

El tipo de institución se asigna automáticamente por palabras clave en el nombre de la institución; es una aproximación. La pestaña «Método y fuentes» del panel detalla definiciones y cautelas. Este ranking mide impacto en citas de Scopus, no calidad investigadora: conviene leerlo según los principios de DORA, el Manifiesto de Leiden y CoARA.

## Estructura

- `index.html`: el panel completo, autocontenido. Los datos agregados van incrustados; D3 y TopoJSON se cargan desde cdnjs.
- `scripts/build_dash_data.py`: agrega las tablas originales (Excel convertidas a Parquet) y genera el JSON del panel.
- `scripts/univ.py`: normalización de los nombres de las universidades españolas.
- `scripts/template.html`: plantilla del panel antes de incrustar los datos.

## Autoría

Ángel M. Delgado Vázquez · Biblioteca/CRAI, Universidad Pablo de Olavide (ORCID [0000-0003-2461-8553](https://orcid.org/0000-0003-2461-8553)).

Es un ejemplo de análisis y visualización de datos asistido por IA (Claude) para la microcredencial «La IA en la investigación científica».

Los datos derivados respetan la licencia CC BY-NC 3.0 de la fuente original.
