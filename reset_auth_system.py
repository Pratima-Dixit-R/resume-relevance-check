import os
import signal
import subprocess
import time
from pathlib import Path

def stop_processes_on_ports(ports):
    """Stop processes running on specified ports"""
    for port in ports:
        try:
            # Find processes on the port
            result = subprocess.run(
                f"netstat -ano | findstr :{port}", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'LISTENING' in line:
                        parts = line.split()
                        pid = parts[-1]
                        print(f"Stopping process on port {port} (PID: {pid})")
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            time.sleep(2)  # Wait for graceful shutdown
                        except ProcessLookupError:
                            print(f"Process {pid} already terminated")
                        except PermissionError:
                            print(f"Permission denied to kill process {pid}")
        except Exception as e:
            print(f"Error stopping processes on port {port}: {e}")

def clear_database():
    """Clear the existing database"""
    db_path = Path("evaluations.db")
    backup_path = Path("evaluations_fresh_backup.db")
    
    if db_path.exists():
        try:
            # Create a backup
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"Created backup of existing database: {backup_path}")
            
            # Remove the existing database
            db_path.unlink()
            print(f"Removed existing database: {db_path}")
            
            print("Database cleared successfully.")
        except PermissionError:
            print("Cannot remove database - it's being used by another process")
            print("Please close any running applications and try again")
            return False
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    else:
        print("No existing database found.")
    
    return True

def restart_services():
    """Restart the services"""
    print("Starting services...")
    # This would typically start your FastAPI and Streamlit services
    # For now, we'll just print instructions
    print("Please start your services using:")
    print("  - For FastAPI backend: uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
    print("  - For Streamlit frontend: streamlit run src/dashboard/streamlit_app.py --server.port 8501")

def main():
    print("Resetting authentication system...")
    
    # Stop running processes
    stop_processes_on_ports([8000, 8501])
    
    # Wait a moment for processes to stop
    time.sleep(3)
    
    # Clear database
    if clear_database():
        print("\nAuthentication system reset complete!")
        print("You can now register new users with LinkedIn-level encryption security.")
        restart_services()
    else:
        print("\nFailed to reset authentication system.")
        print("Please manually stop any running services and try again.")

if __name__ == "__main__":
    main()