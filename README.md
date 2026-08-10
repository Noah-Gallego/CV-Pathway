# CV Pathway

Research and analysis of air pollution and preterm birth rates across California counties from 2007–2023.

[![Python](https://img.shields.io/badge/python-analysis-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,numpy,pandas&theme=light" alt="Python, NumPy, and pandas" />
</p>

## Research question

The project examines the relationship between county-level PM2.5 exposure and preterm birth outcomes, including a comparison of higher-pollution Central Valley counties with coastal counties.

## Reported findings

The existing project documentation reports a PM2.5/preterm-birth correlation of `r = 0.286` with `p < 0.001`, average PM2.5 values of 12.9 μg/m³ for the high-pollution group and 7.8 μg/m³ for the coastal group, and corresponding preterm-birth rates of 9.14% and 7.98%.

These figures are preserved from the project materials and are not presented as an independently validated causal result.

## Preview

![PM2.5 and preterm-birth correlation chart](https://noah-readme-assets-v3.vercel.app/CV-Pathway/asset__outputs__correlation_scatter.png)

## Contents

- `final.py` — analysis script
- `data/main_dataset.csv` and `data/Data-Preterm-Birth.csv` — committed data files
- `outputs/correlation_scatter.png` — correlation visualization
- `outputs/preterm_air_quality_by_county.png` — county comparison visualization
- `CV Pathway - Noah Gallego.pdf` — project presentation

## Usage

Run the analysis script with Python from the repository root:

```bash
python3 final.py
```

The script's dependencies and exact output behavior should be checked in `final.py`; no dependency manifest is included in this checkout.

## Limitations

This is an observational county-level analysis. Correlation does not establish causation, and the results depend on the supplied data preparation and grouping choices.

## Status

The repository contains the analysis script, data, generated charts, and presentation. No live application or public demo is provided.
