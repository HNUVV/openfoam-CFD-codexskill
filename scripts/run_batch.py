#!/usr/bin/env python3
"""
Batch Parameter Sweep Script for OpenFOAM

Runs multiple OpenFOAM cases with varying parameters defined in a CSV file.

CSV format:
    case_name,param1,param2,...
    case_Re100,100,0.001
    case_Re200,200,0.001

Usage:
    python run_batch.py --base case_templates/baseCase --params sweep.csv --solver simpleFoam
"""

import os
import sys
import csv
import shutil
import subprocess
import argparse
from pathlib import Path

def read_params(csv_path):
    params = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            params.append(row)
    return params

def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r") as f:
        content = f.read()
    for old, new in replacements.items():
        content = content.replace(old, str(new))
    with open(filepath, "w") as f:
        f.write(content)

def run_case(case_dir, solver, n_procs=1):
    cwd = os.getcwd()
    os.chdir(case_dir)
    cmd = [solver] if n_procs == 1 else ["mpirun", "-np", str(n_procs), solver, "-parallel"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        os.chdir(cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        os.chdir(cwd)
        return False, "", "Timeout"
    except Exception as e:
        os.chdir(cwd)
        return False, "", str(e)

def main():
    parser = argparse.ArgumentParser(description="Batch OpenFOAM parameter sweep")
    parser.add_argument("--base", required=True, help="Base case directory")
    parser.add_argument("--params", required=True, help="CSV file with parameters")
    parser.add_argument("--solver", default="simpleFoam", help="Solver executable")
    parser.add_argument("--nprocs", type=int, default=1, help="Number of MPI processes")
    parser.add_argument("--dry-run", action="store_true", help="Print cases without running")
    args = parser.parse_args()
    
    base_dir = os.path.abspath(args.base)
    if not os.path.isdir(base_dir):
        print(f"Error: base case not found: {base_dir}")
        sys.exit(1)
    
    params_list = read_params(args.params)
    print(f"Found {len(params_list)} parameter sets")
    
    results = []
    for i, params in enumerate(params_list):
        case_name = params.get("case_name", f"case_{i:03d}")
        case_dir = os.path.join(os.path.dirname(base_dir), case_name)
        
        print(f"[{i+1}/{len(params_list)}] {case_name} ... ", end="", flush=True)
        
        # Copy base case
        if os.path.exists(case_dir):
            shutil.rmtree(case_dir)
        shutil.copytree(base_dir, case_dir, symlinks=True)
        
        # Apply parameter replacements
        for key, value in params.items():
            if key == "case_name":
                continue
            replace_key = f"REPLACE_{key.upper()}"
            for root, dirs, files in os.walk(case_dir):
                for f in files:
                    replace_in_file(os.path.join(root, f), {replace_key: value})
        
        if args.dry_run:
            print("dry run")
            results.append((case_name, True))
            continue
        
        success, stdout, stderr = run_case(case_dir, args.solver, args.nprocs)
        status = "OK" if success else "FAIL"
        print(status)
        if not success:
            log_path = os.path.join(case_dir, "error.log")
            with open(log_path, "w") as f:
                f.write(stderr if stderr else "Unknown error")
            print(f"  Error log: {log_path}")
        
        results.append((case_name, success))
    
    # Summary
    ok = sum(1 for _, s in results if s)
    fail = len(results) - ok
    print(f"\nSummary: {ok} OK, {fail} FAILED")
    if fail:
        sys.exit(1)

if __name__ == "__main__":
    main()
