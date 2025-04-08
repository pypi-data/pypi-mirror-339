#!/usr/bin/env python
import sys
import os
import site
import importlib.util

def main():
    print("Python's module search paths:")
    for path in sys.path:
        print(f"  {path}")
    
    print("\nSite packages directories:")
    print(f"  User site packages: {site.getusersitepackages()}")
    for path in site.getsitepackages():
        print(f"  {path}")
    
    # Check if vtai can be found in any path
    print("\nSearching for vtai module:")
    found = False
    for path in sys.path:
        module_path = os.path.join(path, "vtai")
        if os.path.exists(module_path):
            print(f"  Found at {module_path}")
            found = True
    
    if not found:
        print("  vtai module not found in search paths")

if __name__ == "__main__":
    main()
