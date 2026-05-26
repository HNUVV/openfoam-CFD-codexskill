# Tecplot Workflow for OpenFOAM CFD

## Data Conversion
Use foamToTecplot360 to convert OpenFOAM results:
    foamToTecplot360 -fields "(U p k omega nut)" -time 0:100:10

## Load Data
1. File, Load Data Files, select .plt file
2. For time series: File, Load Data, Tecplot Data Loader

## Essential Operations
- Slice: Data, Extract, Slice for 2D planes
- Iso-Surfaces: Data, Extract, Iso-Surfaces for 3D features
- Streamtraces: Data, Extract, Streamtraces for flow paths
- XY Plot: Plot, XY for line/profile plots

## Publication Figure Export
- EPS: 600 DPI, Color, Vector (best for LaTeX)
- PDF: preserves vector graphics
- PNG: Anti-aliasing ON, Supersample 3x
- TIFF: 600 DPI for journal submission

## Macro for Batch Processing
1. Scripting, Record Macro
2. Perform operations on one case
3. Scripting, Stop Recording, save .mcr file
4. Scripting, Play Macro for other cases
