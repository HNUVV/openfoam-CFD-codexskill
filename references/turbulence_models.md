# Turbulence Model Selection Guide

## RAS (RANS) Models

### One-Equation
| Model | Best For | Wall Treatment |
|-------|----------|----------------|
| SpalartAllmaras | External aero, airfoils | y+ < 1 or wall functions |

### Two-Equation
| Model | Best For | Notes |
|-------|----------|-------|
| kEpsilon | Free-shear flows, industrial | Robust, over-predicts near-wall TKE |
| kOmega | Near-wall flows | Sensitive to inlet omega |
| kOmegaSST | General purpose, separation | Blends k-epsilon + k-omega. **Recommended default** |
| kOmegaSSTLM | Transitional flows | Langtry-Menter transition model |

### Reynolds Stress
| Model | Best For |
|-------|----------|
| LRR / SSG | Swirling, highly anisotropic flows, cyclone separators |

## LES Models

| Model | Best For |
|-------|----------|
| Smagorinsky | Simple, isotropic turbulence |
| WALE | Wall-bounded flows, better near-wall behavior |
| dynamicKEqn | Locally dynamic, no tuning |
| kEqn | One-equation eddy viscosity |

## DES (Hybrid RANS-LES)
| Model | Best For |
|-------|----------|
| SpalartAllmarasDES | External aero with separation |
| kOmegaSSTDES | General purpose, good for industrial |

## Selection Quick Guide

- **Default choice**: kOmegaSST (good for most applications)
- **External aero (clean)**: SpalartAllmaras
- **Swirling/rotating**: RSM or kOmegaSST
- **Transition important**: kOmegaSSTLM
- **Unsteady/LES required**: WALE or dynamicKEqn

## Wall y+ Guidelines

| y+ Range | Wall Treatment | Notes |
|----------|---------------|-------|
| y+ < 1 | Fully resolved | Requires very fine near-wall mesh |
| y+ ~ 1 | Transition zone | Avoid if possible |
| 30 < y+ < 300 | Wall functions | Standard log-law wall functions |
| SpalartAllmaras | y+ < 1 or y+ > 30 | All-y+ wall treatment available |

## kOmegaSST inlet values

Estimate from:
- k = 1.5 * (I * U_inf)^2, where I = turbulence intensity (0.01-0.05)
- omega = k^0.5 / (L * Cmu^0.25), L = turbulence length scale (~0.07*Dh)
- nut ~ turb viscosity ratio * nu
