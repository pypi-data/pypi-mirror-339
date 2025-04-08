#!/usr/bin/env python
import os
import sys
import importlib
import subprocess

def main():
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")

    # Check if vtai is installed
    try:
        import vtai
        print(f"vtai location: {vtai.__file__}")
        print(f"vtai version: {getattr(vtai, '__version__', 'unknown')}")
        
        # Check if the entry point function exists
        try:
            from vtai.app import main as app_main
            print("Entry point function 'main' exists in vtai.app")
        except ImportError:
            print("Failed to import 'main' from vtai.app")
        
        # Try running the command
        print("\nTrying to run 'vtai --help':")
        try:
            result = subprocess.run(["vtai", "--help"], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=5)
            print(f"Return code: {result.returncode}")
            print(f"Output preview: {result.stdout[:100]}...")
        except subprocess.TimeoutExpired:
            print("Command timed out after 5 seconds")
        except Exception as e:
            print(f"Error running command: {e}")
    except ImportError:
        print("vtai not installed")

if __name__ == "__main__":
    main()
