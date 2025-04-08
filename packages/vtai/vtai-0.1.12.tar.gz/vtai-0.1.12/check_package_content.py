#!/usr/bin/env python
import os
import sys
import importlib
import pkg_resources

def main():
    print(f"Python version: {sys.version}")
    
    # Check if vtai is installed
    try:
        import vtai
        print(f"vtai location: {vtai.__file__}")
        
        # List all files in the package
        print("\nListing all resource files in the package:")
        try:
            package_name = "vtai"
            package = importlib.import_module(package_name)
            package_path = os.path.dirname(package.__file__)
            
            print(f"Package path: {package_path}")
            for root, dirs, files in os.walk(package_path):
                rel_path = os.path.relpath(root, package_path)
                if rel_path == ".":
                    rel_path = ""
                for file in files:
                    if not file.endswith(".pyc") and "__pycache__" not in root:
                        full_path = os.path.join(root, file)
                        print(f"  {os.path.join(rel_path, file)}: {os.path.exists(full_path)}")
        except Exception as e:
            print(f"Error listing resources: {e}")
            
        # Check specific important files
        important_files = [
            "router/layers.json",
            "resources/vt.jpg",
            "resources/chatgpt-icon.png"
        ]
        
        print("\nChecking important files:")
        for file in important_files:
            file_path = os.path.join(package_path, file)
            exists = os.path.exists(file_path)
            print(f"  {file}: {'EXISTS' if exists else 'MISSING'} ({file_path})")
            
    except ImportError:
        print("vtai not installed")

if __name__ == "__main__":
    main()
