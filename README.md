# ROBD2 Diagnostic Interface v2.0.0

A modern, intuitive graphical user interface for the ROBD2 device, designed for aerospace physiology training and research.

## ⚠️ Important Notice

This software is **EXPERIMENTAL** and should only be used in controlled environments under the supervision of trained medical professionals or experts in ROBD devices for aerospace physiology training. This software is not intended for clinical use or any other settings without proper medical supervision.

## About

The ROBD2 Diagnostic Interface is a comprehensive tool for monitoring, calibrating, and analyzing data from ROBD2 devices. It provides real-time visualization of critical parameters, advanced gas calculations, data logging capabilities, and diagnostic tools for aerospace physiology training.

### Author
**Diego Malpica MD**
- Aerospace Medicine
- Aerospace Physiology Instructor
- Aerospace Scientific Department
- Aerospace Medicine Directorate
- Colombian Aerospace Force

Initial work - [strikerdlm](https://github.com/strikerdlm)

## Features

### Core Functionality
- Real-time data visualization with customizable time scales and auto-scaling
- Advanced gas calculations with altitude compensation
- Comprehensive data logging and export capabilities
- Multi-step device calibration with validation
- Performance monitoring and analysis tools
- Interactive diagnostic command interface

### User Interface
- Modern, intuitive tabbed interface
- Professional results display with color-coded messages
- Customizable layout with resizable panels
- Dark mode support for reduced eye strain
- Mouse wheel scrolling support for all scrollable windows

### Training Support
- Pre-flight, during training, and post-training checklists
- Support for both English and Spanish training scripts
- Real-time script viewer with progress tracking
- Integrated training session management
- Automatic data validation and range checking

### Data Management
- CSV data export with timestamps and metadata
- Automatic backup of session data
- Data filtering and validation
- Session summary reports
- Historical data analysis tools

## Requirements

### Software Requirements
- Python 3.8 or higher
- Windows 10 or higher

### Required Python Packages
```
pyserial>=3.5
rich>=13.0.0
matplotlib>=3.7.0
numpy>=1.24.0
```

## Web Frontend (New!)

A modern TypeScript frontend is available in the `frontend/` directory, featuring:
- Publication-quality ECharts visualizations
- Real-time monitoring dashboard
- Gas calculators with scientific accuracy
- Performance analytics
- Bilingual support (EN/ES)

### Running the Web Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## Python GUI Installation

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

## Quick Start Guide

1. Connect your ROBD2 device to a USB port
2. Launch the application
3. In the Connection tab:
   - Select the appropriate COM port
   - Choose your device ID
   - Click "Connect"
4. Use the Dashboard tab for real-time monitoring
5. Use the Calibration tab for device setup
6. Export data using the Export button when monitoring is complete

## Data Validation

The software implements comprehensive data validation:
- SpO2: 50-100%
- O2 Concentration: 0-100%
- Pulse Rate: 20-220 bpm
- Altitude: 0-35,000 ft
- Temperature: 15-35°C

## License

Copyright © 2024 Diego Malpica MD. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.

## Disclaimer

This software is provided "as is" without any warranties, express or implied. The authors and developers are not responsible for any damages or injuries that may occur from the use of this software.

## Support

For technical support, bug reports, or feature requests, please contact:
- Email: dlmalpicah@unal.edu.co
- GitHub Issues: [ROBD2_GUI Issues](https://github.com/strikerdlm/ROBD2_GUI/issues)

## Acknowledgments

- Aerospace physiology research community
- ROBD2 device development team
- Beta testers and contributors
- Colombian Aerospace Force 