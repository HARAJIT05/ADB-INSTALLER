import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.request
import zipfile

ADB_DOWNLOAD_URL = {
    'Windows': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
    'Linux': 'https://dl.google.com/android/repository/platform-tools-latest-linux.zip',
    'Darwin': 'https://dl.google.com/android/repository/platform-tools-latest-darwin.zip'
}

def download_and_install_adb():
    # Determine the user's operating system
    os_name = platform.system()
    if os_name not in ADB_DOWNLOAD_URL:
        messagebox.showerror("Error", f"Unsupported operating system: {os_name}")
        return False

    # Download the ADB SDK zip file
    download_url = ADB_DOWNLOAD_URL[os_name]
    try:
        urllib.request.urlretrieve(download_url, 'platform-tools.zip')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download ADB SDK: {e}")
        return False

    # Extract the downloaded zip file
    try:
        with zipfile.ZipFile('platform-tools.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract ADB SDK: {e}")
        return False

    # Delete the downloaded zip file
    os.remove('platform-tools.zip')

    # Set the PATH environment variable to include the extracted directory
    os.environ['PATH'] += os.pathsep + os.path.abspath('platform-tools')

    return True

def check_adb_installed():
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def ensure_adb_installed():
    if not check_adb_installed():
        if not download_and_install_adb():
            messagebox.showerror("Error", "Failed to download and install ADB SDK.")
            return False
    return True

def get_device_name():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices_info = result.stdout.split('\n')[1:-2]
        devices = [device.split('\t')[0] for device in devices_info]
        if devices:
            return devices[0]  # Assuming the first device is the target device
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get device name: {e}")
    return "No device found"

def choose_directory():
    directory_path = filedialog.askdirectory()
    directory_var.set(directory_path)

def install_apk():
    device_name = get_device_name()
    if device_name == "No device found":
        messagebox.showerror("Error", "No device found. Make sure your device is connectedand ADB is on.")
        return
    
    directory_path = directory_var.get()
    if directory_path:
        success = True
        failed_apks = []
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.apk'):
                apk_path = os.path.join(directory_path, file_name)
                result = subprocess.run(['adb', '-s', device_name, 'install', apk_path], capture_output=True)
                if result.returncode != 0:
                    success = False
                    failed_apks.append(file_name)
        if success:
            messagebox.showinfo("Success", "All APKs installed successfully.")
        else:
            messagebox.showerror("Error", f"Failed to install the following APKs:\n{', '.join(failed_apks)}")

def flash_recovery():
    device_name = get_device_name()
    if device_name == "No device found":
        messagebox.showerror("Error", "No device found. Make sure your device is connectedand ADB is on.")
        return
    
    recovery_img_path = filedialog.askopenfilename(title="Select Recovery Image", filetypes=[("Recovery Image Files", "*.img")])
    if recovery_img_path:
        # Reboot into bootloader
        subprocess.run(['adb', '-s', device_name, 'reboot', 'bootloader'])
        # Wait for device to reboot into bootloader
        import time
        time.sleep(10)
        # Flash recovery or boot recovery temporarily
        result = subprocess.run(['fastboot', '-s', device_name, 'flash', 'recovery', recovery_img_path], capture_output=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", "Recovery flashed successfully.")
        else:
            messagebox.showerror("Error", "Failed to flash recovery.")

def abort_installation():
    root.destroy()

root = tk.Tk()
root.title("")

directory_var = tk.StringVar()

label_device = tk.Label(root, text="Device:")
label_device.grid(row=0, column=0, padx=5, pady=5)

device_name = get_device_name()
label_device_value = tk.Label(root, text=device_name)
label_device_value.grid(row=0, column=1, padx=5, pady=5)

label_directory = tk.Label(root, text="Select Directory:")
label_directory.grid(row=1, column=0, padx=5, pady=5)

directory_entry = tk.Entry(root, textvariable=directory_var, width=50)
directory_entry.grid(row=1, column=1, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=choose_directory)
browse_button.grid(row=1, column=2, padx=5, pady=5)

install_button = tk.Button(root, text="Install APKs", command=install_apk)
install_button.grid(row=2, column=0, padx=5, pady=5)

flash_button = tk.Button(root, text="Flash Recovery", command=flash_recovery)
flash_button.grid(row=2, column=1, padx=5, pady=5)

abort_button = tk.Button(root, text="Abort", command=abort_installation)
abort_button.grid(row=2, column=2, padx=5, pady=5)

# Ensure ADB is installed
if not ensure_adb_installed():
    root.destroy()
else:
    root.mainloop()
