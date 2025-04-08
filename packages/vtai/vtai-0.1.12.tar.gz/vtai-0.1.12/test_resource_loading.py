#!/usr/bin/env python
import os
import importlib.resources
import sys
from pathlib import Path

def main():
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")

    # Check if vtai is installed
    try:
        import vtai
        print(f"vtai location: {vtai.__file__}")
    except ImportError:
        print("vtai not installed")
        sys.exit(1)
    
    # Try to access router data
    print("\nTrying to access layers.json:")
    try:
        # Method 1: Using importlib.resources
        print("Method 1: Using importlib.resources")
        try:
            with importlib.resources.files("vtai.router").joinpath("layers.json").open("r") as f:
                content = f.read(50) + "..." if len(f.read()) > 50 else f.read()
                print(f"Content preview: {content}")
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        # Method 2: Alternative method
        print("\nMethod 2: Using package relative path")
        try:
            vtai_path = Path(vtai.__file__).parent
            layers_path = vtai_path / "router" / "layers.json"
            if layers_path.exists():
                with open(layers_path, "r") as f:
                    content = f.read(50) + "..." if len(f.read()) > 50 else f.read()
                    print(f"Content exists at {layers_path}")
                    print(f"Content preview: {content}")
            else:
                print(f"File not found at {layers_path}")
        except Exception as e:
            print(f"Method 2 failed: {e}")

        # Method 3: Using importlib.resources.path
        print("\nMethod 3: Using importlib.resources.path")
        try:
            with importlib.resources.path("vtai.router", "layers.json") as path:
                if path.exists():
                    with open(path, "r") as f:
                        content = f.read(50) + "..." if len(f.read()) > 50 else f.read()
                        print(f"Content exists at {path}")
                        print(f"Content preview: {content}")
                else:
                    print(f"File not found at {path}")
        except Exception as e:
            print(f"Method 3 failed: {e}")
            
    except Exception as e:
        print(f"Error accessing resources: {e}")
    
    # Check for image resources
    print("\nChecking for image resources:")
    try:
        print("Trying to find vt.jpg:")
        try:
            with importlib.resources.path("vtai.resources", "vt.jpg") as path:
                print(f"vt.jpg exists: {path.exists()} at {path}")
        except Exception as e:
            print(f"Error finding vt.jpg: {e}")
    except Exception as e:
        print(f"Error checking image resources: {e}")

if __name__ == "__main__":
    main()
