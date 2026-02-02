import subprocess
import sys
from pathlib import Path

def run_command(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False
        )
        print(f"✓ {description} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error code {e.returncode}\n")
        return False

def main():
    """Run the complete ETL pipeline"""
    print("="*60)
    print("MoMo SMS ETL Pipeline")
    print("="*60)
    print("This will run the complete Extract-Transform-Load process:")
    print("  1. Extract: Parse XML to raw JSON")
    print("  2. Transform: Clean & normalize data")
    print("  3. Transform: Categorize transactions")
    print("  4. Load: Save to SQLite database")
    print("="*60)
    
    # Check if database exists
    db_path = Path(__file__).parent.parent / 'database' / 'db.sqlite3'
    if not db_path.exists():
        print("\nWARNING: Database not initialized!")
        print("  Run 'python database/init_db.py' first")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(0)
    
    # Get the etl directory
    etl_dir = Path(__file__).parent
    
    # Define pipeline steps
    steps = [
        (etl_dir / 'parse_xml.py', 'Step 1: Extract (Parse XML)'),
        (etl_dir / 'clean_normalize.py', 'Step 2: Transform (Clean & Normalize)'),
        (etl_dir / 'categorize.py', 'Step 3: Transform (Categorize)'),
        (etl_dir / 'load_db.py', 'Step 4: Load (Save to Database)'),
    ]
    
    # Run each step
    for i, (script, description) in enumerate(steps, 1):
        if not script.exists():
            print(f"✗ Error: Script not found: {script}")
            sys.exit(1)
        
        success = run_command(str(script), description)
        
        if not success:
            print(f"\n✗ Pipeline failed at step {i}")
            print("Fix the errors and run again.")
            sys.exit(1)
    
    # Success!
    print("="*60)
    print("✓ ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Start API server: python api/app.py")
    print("  2. Run DSA comparison: python dsa/search_comparison.py")
    print("  3. Test API with curl or Postman")
    print("="*60)

if __name__ == "__main__":
    main()