import sys
import subprocess

print("Running evaluate-tests skill...")
print("=" * 50)

# Run the skill directly
result = subprocess.run([sys.executable, 'skills/evaluate-tests/__init__.py'], 
                       capture_output=True, text=True, cwd='.')

print(f"Exit code: {result.returncode}")
print(f"Stdout:\n{result.stdout}")
if result.stderr:
    print(f"Stderr:\n{result.stderr}")

# Also try to import and run it directly
try:
    print("\n" + "=" * 50)
    print("Trying direct import...")
    
    # Import the skill as a module
    import importlib.util
    spec = importlib.util.spec_from_file_location("evaluate_tests", "skills/evaluate-tests/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    print("Successfully loaded module")
    if hasattr(module, 'main'):
        print("Running main()...")
        result2 = module.main()
        print(f"Main returned: {result2}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
