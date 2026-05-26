#!/usr/bin/env python3
"""
OpenFOAM Case Setup Script

Creates a new OpenFOAM case from templates with interactive prompts.

Usage:
    python setup_case.py <caseName> [--solver simpleFoam] [--mesh blockMesh] [--template path/to/templates]
"""

import os
import sys
import shutil
import argparse

def create_case(case_name, solver="simpleFoam", mesh_type="blockMesh", template_dir=None):
    # Determine template source
    if template_dir is None:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "templates")
    
    templates = os.path.abspath(template_dir)
    case_path = os.path.abspath(case_name)
    
    if os.path.exists(case_path):
        print(f"Error: {case_path} already exists")
        return False
    
    # Create directory structure
    dirs = ["0", "constant", "system"]
    for d in dirs:
        os.makedirs(os.path.join(case_path, d), exist_ok=True)
    
    # Copy template files
    system_files = ["controlDict", "fvSchemes", "fvSolution", "fvOptions"]
    constant_files = ["transportProperties", "turbulenceProperties"]
    zero_files = ["U", "p"]
    
    for f in system_files:
        src = os.path.join(templates, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(case_path, "system", f))
    
    for f in constant_files:
        src = os.path.join(templates, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(case_path, "constant", f))
    
    for f in zero_files:
        src = os.path.join(templates, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(case_path, "0", f))
    
    # Update controlDict with solver name
    ctrl_path = os.path.join(case_path, "system", "controlDict")
    if os.path.exists(ctrl_path):
        with open(ctrl_path, "r") as f:
            content = f.read()
        content = content.replace("REPLACE_SOLVER", solver)
        with open(ctrl_path, "w") as f:
            f.write(content)
    
    print(f"Case created: {case_path}")
    print(f"  Solver: {solver}")
    print(f"  Mesh type: {mesh_type}")
    print(f"\nNext steps:")
    print(f"  1. Create blockMeshDict in {case_path}/system/")
    print(f"  2. Edit boundary conditions in {case_path}/0/")
    print(f"  3. Edit fluid properties in {case_path}/constant/")
    print(f"  4. Run: blockMesh && checkMesh && {solver}")
    return True

def main():
    parser = argparse.ArgumentParser(description="OpenFOAM case setup")
    parser.add_argument("case_name", help="Name of the case directory")
    parser.add_argument("--solver", default="simpleFoam", help="Solver to use")
    parser.add_argument("--mesh", default="blockMesh", help="Mesh type")
    parser.add_argument("--template", help="Path to template directory")
    args = parser.parse_args()
    
    success = create_case(args.case_name, args.solver, args.mesh, args.template)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
