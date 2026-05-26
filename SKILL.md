---
name: openfoam-cfd
description: "OpenFOAM CFD simulation end-to-end workflow. Use when user needs help with: case setup and directory structure, mesh generation (blockMesh, snappyHexMesh), solver selection and configuration, source term modification (fvOptions, coded sources), boundary conditions, turbulence modeling, and publication-level post-processing with ParaView, Tecplot, or MATLAB. Covers the full CFD pipeline from geometry to publication figures."
---

# OpenFOAM CFD

End-to-end OpenFOAM CFD simulation skill covering case setup, meshing, solver configuration, source terms, and publication-quality post-processing.

## Workflow Overview

`
Geometry -> Meshing -> Case Setup -> Solver -> Post-Processing
`

## 1. Case Directory Structure

Every OpenFOAM case follows this layout:

`
caseName/
  0/                  # Initial/boundary conditions (time directory)
    U, p, k, epsilon ...
  constant/
    polyMesh/          # Mesh files
    transportProperties
    turbulenceProperties
  system/
    controlDict        # Time control, I/O
    fvSchemes          # Discretization schemes
    fvSolution         # Linear solver settings
    blockMeshDict      # (if using blockMesh)
`

When creating a new case, copy from ssets/case-skeleton/.

## 2. Meshing

### blockMesh -- structured hex mesh
- Define in system/blockMeshDict
- Key sections: ertices, locks, edges, oundary, mergePatchPairs
- Use ssets/templates/blockMeshDict as starting template
- Run: lockMesh
- Check: checkMesh

### snappyHexMesh -- complex geometry
- Requires STL/OBJ surface in constant/triSurface/
- Configure system/snappyHexMeshDict
- Process: castellated -> snap -> addLayers
- Run: snappyHexMesh -overwrite

### Mesh quality checklist
- checkMesh must pass all checks
- max non-orthogonality < 70 (ideally < 65)
- max skewness < 4
- min cell volume > 0
- Avoid sudden cell size transitions (>1.2 growth ratio)

## 3. Solver & Physical Setup

### Solver selection
| Physics | Solver |
|---------|--------|
| Steady incompressible | simpleFoam |
| Transient incompressible | pisoFoam / pimpleFoam |
| Steady compressible | rhoSimpleFoam |
| Transient compressible | rhoPimpleFoam |
| Multiphase (VOF) | interFoam |
| Heat transfer | buoyantSimpleFoam / buoyantPimpleFoam |
| Reacting flow | reactingFoam |

### Key dictionary files
- system/controlDict: start/end time, deltaT, writeInterval
- system/fvSchemes: div schemes, grad schemes, laplacian schemes
- system/fvSolution: solvers, tolerances, relaxation factors
- constant/transportProperties: fluid properties
- constant/turbulenceProperties: RAS/LES model selection

Use templates from ssets/templates/ as starting points.

### Boundary conditions
Common BC types:
- ixedValue -- prescribed value (inlet velocity, wall temperature)
- zeroGradient -- zero normal gradient (outlet, symmetry)
- inletOutlet -- zeroGradient outflow, fixedValue backflow
- 
oSlip -- zero velocity at wall
- symmetryPlane / symmetry -- symmetry condition
- cyclic / cyclicAMI -- periodic boundary
- empty -- 2D simulations
- wedge -- axisymmetric (wedge type geometry)

## 4. Source Terms (fvOptions)

Source terms are added via system/fvOptions. Common types:

### scalarCodedSource -- custom scalar source
`
energySource
{
    type            scalarCodedSource;
    selectionMode   all;
    fields          (h);
    name            sourceTime;
    codeInclude     #{
        #include "fvCFD.H"
    #};
    codeCorrect     #{
        // Source expression: e.g. Q = 1e6 * (1 - T/300)
        const scalarField& T = mesh().lookupObject<volScalarField>("T");
        scalarField& heSource = eqn.source();
        heSource += 1e6 * (1.0 - T/300.0);
    #};
}
`

### vectorCodedSource -- momentum source
Use for: pump, fan, porous media body force, Actuator Disk Model (ADM)

### semiImplicitSource / explicitSource
Simpler alternatives for constant or tabulated sources.

### Common use cases
- Heat source / sink in energy equation
- Momentum source (pump, fan, actuator disk)
- Mass source / sink
- Porous media (Darcy-Forchheimer)
- Scalar transport source

## 5. Running & Monitoring

### Standard run sequence
`
blockMesh                    # or snappyHexMesh
checkMesh                    # verify mesh quality
decomposePar                 # (parallel only)
mpirun -np N solverName -parallel  # run
reconstructPar               # (parallel only)
`

### Convergence monitoring
- Check residuals: 	ail -f log.solverName or oamLog log.solverName
- Monitor forces: add orceCoeffs function object
- Monitor probes: add probes function object
- Check mass balance / continuity

### Common convergence issues
- High CFL number -> reduce deltaT
- Diverging pressure -> check BCs, improve mesh near walls
- Oscillating residuals -> reduce relaxation factors
- Negative k/epsilon -> use bounded schemes, check inlet values

## 6. Post-Processing (Publication Level)

### 6a. ParaView -- 3D visualization
- Open case: paraFoam or load .foam file
- Extract slices, iso-surfaces, streamlines
- Calculate derived fields: Q-criterion, vorticity, wall shear stress
- Use Calculator filter for custom expressions
- Export high-res images: File -> Save Screenshot (set 4K+ resolution)
- Tips for publication figures:
  - Consistent color maps (use Cool to Warm or Viridis)
  - Add scale bars and annotations
  - Use Plot Over Line for profile plots
  - Export data as CSV for external plotting

### 6b. Tecplot -- publication plots
- Convert OpenFOAM data: oamToTecplot360 -fields "(U p k)"
- Load .plt files into Tecplot
- Key operations:
  - Data -> Extract -> Slice for 2D slices
  - Data -> Extract -> Iso-Surfaces for 3D features
  - Plot -> XY for line/profile plots
  - Use Macro recording for batch processing
- Export: File -> Export -> choose EPS/PDF/TIFF at 600+ DPI
- Style: use Contour -> Coloring -> Multi-Coloring for multi-variable plots

### 6c. MATLAB -- data analysis & plotting
- Post-process OpenFOAM sampled data
- Run scripts/of_postprocess_matlab.m template
- Key workflow:
  1. Sample data in OpenFOAM using postProcess -func sample
  2. Load sampled data into MATLAB
  3. Process, analyze, plot with publication formatting
- Publication figure settings: see 
eferences/matlab_figure_style.md

### Common post-processing tasks
- Pressure coefficient Cp distribution
- Velocity profiles at cross-sections
- Wall shear stress / skin friction
- Nusselt number for heat transfer
- Turbulence intensity, turbulent kinetic energy
- Spectral analysis (FFT) for unsteady flows
- Q-criterion / lambda2 for vortex identification

## 7. Advanced Topics

### Custom solver compilation
- Copy existing solver: oamNewApp or copy from pplications/solvers/
- Modify equations in .C file
- Compile: wmake
- Reference: 
eferences/custom_solver_guide.md

### Custom boundary conditions
- Use codedFixedValue, codedMixed for simple custom BCs
- For complex BCs: create new BC class, compile with wmake

### Function objects
Common function objects for data extraction:
- orceCoeffs -- lift/drag coefficients
- probes -- point monitoring
- surfaces / sampledSurface -- cut planes
- ieldAverage -- Reynolds-averaged quantities
- wallShearStress -- wall shear

### Parallel running
- decomposePar with scotch or simple method
- Optimal decomposition: ~50k-100k cells per core

## Resources

### scripts/
- setup_case.py -- Interactive case creation from templates
- 
un_batch.py -- Batch parameter sweep
- of_postprocess_matlab.m -- MATLAB post-processing template

### references/
- dictionary_quickref.md -- Common dictionary parameters
- solver_selection.md -- Detailed solver selection guide
- 	urbulence_models.md -- RAS/LES model selection
- matlab_figure_style.md -- Publication-quality MATLAB figure settings
- 	ecotplot_workflow.md -- Tecplot workflow for CFD

### assets/
- case-skeleton/ -- Empty case directory structure
- 	emplates/ -- Template dictionaries (controlDict, fvSchemes, fvSolution, etc.)
- matlab-templates/ -- MATLAB figure templates
