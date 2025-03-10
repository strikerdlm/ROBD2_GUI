# ROBD2 Diagnostic Interface

A modern, intuitive graphical user interface for the ROBD2 device, designed for aerospace physiology training and research.

## ⚠️ Important Notice

This software is **EXPERIMENTAL** and should only be used in controlled environments under the supervision of trained medical professionals or experts in ROBD devices for aerospace physiology training. This software is not intended for clinical use or any other settings without proper medical supervision.

## About

The ROBD2 Diagnostic Interface is a comprehensive tool for monitoring, calibrating, and analyzing data from ROBD2 devices. It provides real-time visualization of critical parameters, data logging capabilities, and diagnostic tools for aerospace physiology training.

## Features

- Real-time data visualization with customizable time scales
- Comprehensive data logging and export capabilities
- Device calibration tools
- Performance monitoring
- Diagnostic command interface
- Modern, intuitive user interface
- Automatic data validation and range checking
- CSV data export with timestamps
- Training tab with script viewers and checklists
- Mouse wheel scrolling support for all scrollable windows
- Pre-flight, during training, and post-training checklists
- Support for both English and Spanish training scripts

## Requirements

- Python 3.8 or higher
- Windows 10 or higher
- Required Python packages:
  ```
  pyserial
  rich
  matplotlib
  numpy
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/strikerdlm/ROBD2_GUI.git
   cd ROBD2_GUI
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python robd2_gui.py
   ```

## Usage

1. Connect to the ROBD2 device using the Connection tab
2. Select the appropriate device ID
3. Use the Dashboard tab for real-time monitoring
4. Export data using the Export button when monitoring is complete

## Data Validation

The software implements the following validation ranges:
- SpO2: 50-100%
- O2 Concentration: 0-100%
- Pulse Rate: 20-220 bpm

## License

Copyright © 2025 Diego Malpica MD. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.

## Disclaimer

This software is provided "as is" without any warranties, express or implied. The authors and developers are not responsible for any damages or injuries that may occur from the use of this software.

## Author

- **Diego Malpica MD** - *Initial work* - [strikerdlm](https://github.com/strikerdlm)

## Acknowledgments

- Special thanks to the aerospace physiology research community
- ROBD2 device development team
- All contributors and testers 