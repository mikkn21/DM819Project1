import subprocess
import sys
import platform

def install_requirements():
    """Install the packages from requirements.txt using the appropriate pip and python commands."""
    try:
        pip_cmd = "pip"
        python_cmd = sys.executable

        if platform.system() == "Darwin":  # macOS
            pip_cmd = "pip3"
            python_cmd = "python3"

        
        subprocess.check_call([python_cmd, "-m", pip_cmd, "install", "-r", "requirements.txt"])

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing the packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    print("All packages are installed. You can now run 'python prog.py' or 'python3 prog.py' depending on your system.")

