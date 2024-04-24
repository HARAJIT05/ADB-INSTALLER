# ADB Toolkit

This toolkit provides a simple GUI interface to manage Android Debug Bridge (ADB) functionalities such as installing APKs and flashing recovery images. It uses Tkinter for the GUI and subprocess module to interact with ADB and Fastboot.

## Features

- **Install APKs**: Select a directory containing APK files and install them on the connected Android device.
- **Flash Recovery**: Choose a recovery image file and flash it onto the connected Android device.
- **Device Information**: Displays the name of the connected device.
- **Abort Installation**: Close the application.

## Prerequisites

- Python 3.x installed on your system.
- ADB and Fastboot installed and added to your system's PATH.

## Installation

1. Clone the repository or download the script.
2. Ensure that ADB and Fastboot are installed and accessible from the command line.
3. Run the script using Python.

```bash
python adbinstaller.py
```

## Usage

1. Connect your Android device to your computer via USB.
2. Launch the application.
3. Click on "Install APKs" to select a directory containing APK files and install them.
4. Click on "Flash Recovery" to select a recovery image file and flash it onto the device.
5. Click on "Abort" to close the application.

## Supported Operating Systems

- Windows
- Linux
- macOS

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Harajit](https://github.com/HARAJIT05)

## Acknowledgments

Special thanks to the developers of Tkinter and ADB for providing the tools necessary to create this application.
