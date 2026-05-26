# OpenFOAM Solver Selection Guide

## Incompressible Flow

| Solver | Description | Use When |
|--------|-------------|----------|
| simpleFoam | Steady, incompressible, turbulent | RANS, steady-state problems |
| pisoFoam | Transient, incompressible, turbulent | LES/DNS, small time steps |
| pimpleFoam | Transient with PIMPLE (hybrid PISO-SIMPLE) | Large time steps, CFL > 1 OK |
| icoFoam | Transient, incompressible, laminar | Learning, validation cases |

## Compressible Flow

| Solver | Description | Key Features |
|--------|-------------|--------------|
| rhoSimpleFoam | Steady compressible | RANS, subsonic to supersonic |
| rhoPimpleFoam | Transient compressible | All speeds, PIMPLE algorithm |
| rhoCentralFoam | Shock-capturing | Supersonic, shock-dominated flows |
| sonicFoam | Transient, sonic | Transonic/supersonic |

## Heat Transfer

| Solver | Description |
|--------|-------------|
| buoyantSimpleFoam | Steady, buoyancy-driven |
| buoyantPimpleFoam | Transient, buoyancy-driven |
| chtMultiRegionFoam | Conjugate heat transfer (multi-region) |

## Multiphase

| Solver | Description | Interface Method |
|--------|-------------|------------------|
| interFoam | Two-phase incompressible | VOF |
| multiphaseInterFoam | N-phase incompressible | VOF |
| interMixingFoam | Three-phase with mixing | VOF |
| twoPhaseEulerFoam | Two-phase Euler-Euler | Eulerian |

## Other

| Solver | Purpose |
|--------|---------|
| reactingFoam | Combustion/reactive flow |
| particleFoam | Lagrangian particle tracking |
| solidDisplacementFoam | Solid mechanics FV |
| potentialFoam | Potential flow initialization |

## Decision Flow

1. Compressible (Ma > 0.3)? -> rho*Foam
2. Steady or transient? -> simpleFoam / pimpleFoam
3. Multiphase? -> interFoam / reacting*
4. Heat important? -> buoyant* / cht*
