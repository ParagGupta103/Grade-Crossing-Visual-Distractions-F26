import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"🚀 Starting step: {script_name}")
    print(f"{'='*50}\n")
    
    try:
        # sys.executable ensures we use the same Python interpreter running main.py
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: '{script_name}' failed with exit code {e.returncode}.")
        print("Pipeline aborted.")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred while running '{script_name}': {e}")
        print("Pipeline aborted.")
        sys.exit(1)
        
    print(f"\n✅ Successfully completed step: {script_name}")

def main():
    print("Starting full pipeline execution...")
    
    # Check if coordinates.csv exists before starting
    if not os.path.exists("coordinates.csv"):
        print("⚠️  Warning: 'coordinates.csv' not found. 'dataset_generation.py' will likely fail and exit.")
        print("Please ensure you have placed your 'coordinates.csv' in the root directory.\n")
        
    # The order of execution
    scripts = [
        "dataset_generation.py",
        "detector.py",
        "risk_analyzer.py"
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"❌ Error: Script '{script}' not found in the current directory.")
            sys.exit(1)
        run_script(script)

    print(f"\n{'='*50}")
    print("🎉 Full pipeline execution finished successfully!")
    print("Check 'risk_summary.csv' for the final analysis.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
