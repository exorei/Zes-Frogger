import importlib
import subprocess
import sys

# List of required packages
packages = ['tkinter', 'tkinterdnd2']

missing_packages = []

# Log file
log_file_path = 'dependencies_check_log.txt'

try:
    log_file = open(log_file_path, 'w')
except PermissionError:
    print(f"PermissionError: Unable to write to {log_file_path}. Please close the file if it is open elsewhere.")
    sys.exit(1)

# Header for log file
log_file.write('Checking for required packages\n')

# Check each package
for package in packages:
    try:
        importlib.import_module(package)
        print(f'* {package} (Installed)')
        log_file.write(f'* {package} (Installed)\n')
    except ImportError:
        print(f'* {package} (Not Installed)')
        log_file.write(f'* {package} (Not Installed)\n')
        missing_packages.append(package)

# Check for PyInstaller as a command-line tool
try:
    result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print('* pyinstaller (Installed)')
        log_file.write('* pyinstaller (Installed)\n')
    else:
        raise Exception('PyInstaller not found')
except Exception:
    print('* pyinstaller (Not Installed)')
    log_file.write('* pyinstaller (Not Installed)\n')
    missing_packages.append('pyinstaller')

# Summary
if missing_packages:
    log_file.write('\nSome packages are not installed.\n')
    log_file.write('Missing packages: ' + ' '.join(missing_packages) + '\n')
    print('\nSome packages are not installed.')
    print('Missing packages: ' + ' '.join(missing_packages))
    log_file.close()

    user_input = input("Do you want to install the missing packages? [Y/N] ").strip().lower()
    if user_input != 'y':
        print("Exiting without installing missing packages.")
        sys.exit(1)

    for package in missing_packages:
        print(f"Installing {package}...")
        log_file = open(log_file_path, 'a')  # Append to the log file
        result = subprocess.run(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log_file.write(result.stdout)
        log_file.write(result.stderr)
        log_file.close()

        if result.returncode != 0:
            print(f"Failed to install {package}. Exiting...")
            sys.exit(1)

    print("All missing packages have been installed.")
    log_file = open(log_file_path, 'a')
    log_file.write("All missing packages have been installed.\n")
    log_file.close()
else:
    log_file.write('\nAll required packages are installed.\n')
    print('All required packages are installed.')
    log_file.close()

input("Press Enter to exit...")
