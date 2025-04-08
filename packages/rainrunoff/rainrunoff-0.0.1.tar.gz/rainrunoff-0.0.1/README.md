# rainrunoff

`rainrunoff` is a modular, daily time-step rainfall-runoff model written in Python. It is designed to simulate hydrological response in lumped subbasins using the SCS Curve Number method and various hydrologic routing techniques.

The model is structured to support extensibility, including evapotranspiration estimation, water balance modeling, and multi-objective calibration using evolutionary algorithms. It is suitable for educational use, research, and integration into GIS-based workflows.



## Features

- Daily rainfall-runoff simulation using:
  - SCS Curve Number method
- Supports multiple routing methods:
  - Muskingum method
  - Kirpich lag time
  - Kinematic wave
- Curve Number estimation from land use and soil data
- Command-line interface (CLI) support
- Modular structure for future extensions (e.g., calibration, QGIS plugin)
- In-memory storage of all results with options for daily, monthly, and annual summaries
- Missing data handling using long-term monthly averages
- Logging and unit testing support

## Installation

After cloning the repository or downloading the source:

```bash
pip install .
