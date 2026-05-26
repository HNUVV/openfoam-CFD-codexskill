# OpenFOAM Dictionary Quick Reference

## system/controlDict

| Keyword | Description | Typical Value |
|---------|-------------|---------------|
| startFrom | Start control | latestTime / startTime / firstTime |
| startTime | Start time value | 0 |
| stopAt | Stop control | endTime / writeNow |
| endTime | End time value | 1000 |
| deltaT | Time step | 1e-5 (transient) |
| writeControl | Write trigger | timeStep / runTime / adjustableRunTime |
| writeInterval | Write frequency | 100 |
| purgeWrite | Keep only N dirs | 2 |
| writeFormat | Format | ascii / binary |
| writePrecision | Digits | 8 |
| runTimeModifiable | Re-read on change | yes |

## system/fvSchemes

| Sub-dict | Scheme Options | Notes |
|----------|---------------|-------|
| ddtSchemes | Euler, backward, CrankNicolson, steadyState | Transient: backward (2nd order) |
| gradSchemes | Gauss linear, leastSquares, cellMDLimited | leastSquares for skewed meshes |
| divSchemes | Gauss linear, Gauss limitedLinear, Gauss upwind | Momentum: limitedLinear 1 |
| laplacianSchemes | Gauss linear corrected, Gauss linear limited | corrected: non-ortho correction |
| interpolationSchemes | linear, linearUpwind | linearUpwind for higher order |
| snGradSchemes | corrected, limited | corrected with non-ortho loops |

## system/fvSolution

### Solver keys
| Solver | For fields | Tolerance | RelTol |
|--------|-----------|-----------|--------|
| PCG/PBiCG + DIC/DILU | p, p_rgh | 1e-8 | 0.01 |
| smoothSolver + symGaussSeidel | U, k, epsilon, omega | 1e-8 | 0.1 |

### Relaxation factors
| Field | Steady (simpleFoam) | Transient |
|-------|---------------------|-----------|
| p / p_rgh | 0.3 | 0.3-0.5 |
| U | 0.7 | 0.7-0.9 |
| k, epsilon, omega | 0.7 | 0.7-0.9 |
