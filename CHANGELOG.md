# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-03

### Added
- **TypeScript Frontend** - Modern React + TypeScript web application
  - Publication-quality ECharts visualizations designed for Q1 science journal submissions
  - Glass-morphism UI design with Tailwind CSS
  - Framer Motion animations for smooth interactions
  - Bilingual support (English/Spanish) with i18next

### Dashboard Features
- Real-time altitude profile with warning/critical zone markers
- SpO₂ gauge chart with clinical thresholds
- Multi-parameter time series charts (O₂, BLP, SpO₂, Pulse)
- Interactive data zoom and pan capabilities
- CSV data export functionality

### Gas Calculators
- Physiological parameters calculator (PAO₂, SaO₂, ventilation, heart rate)
- Training gas consumption estimator
- Cylinder capacity calculator
- Single session cost calculator
- Altitude-physiology curve visualization

### Performance Analytics
- Statistical distribution histograms
- Box plot analysis
- Coefficient of variation metrics
- Quality assessment indicators

### Scientific References
All calculations verified against peer-reviewed literature:
- West JB. Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.
- FAA-H-8083-25B Pilot's Handbook of Aeronautical Knowledge, Chapter 17.
- Severinghaus JW. J Appl Physiol. 1979;46(3):599-602.
- Richalet JP. Presse Med. 2012;41(6):638-43.
- Weil JV. Compr Physiol. 2012;2(2):1495-1550.

### Technical Stack
- React 19 with TypeScript
- ECharts 6 for data visualization
- Vite 7 for fast builds
- Tailwind CSS 3 for styling

## [1.0.0] - 2024-03-19

### Added
- Initial release of ROBD2 Diagnostic Interface
- Modern, intuitive user interface with multiple tabs
- Real-time data visualization with customizable time scales
- Comprehensive data logging and export capabilities
- Device calibration tools
- Performance monitoring
- Diagnostic command interface
- Training scripts and checklists
- Dashboard with real-time plots
- Automatic data validation and range checking
- CSV data export with timestamps

### Features
- Connection management with COM port selection
- Pre-flight checklist system
- Training scripts for both fixed-wing and rotary-wing aircraft
- During and after training checklists
- Real-time monitoring of:
  - Altitude
  - O2 Concentration
  - Breathing Loop Pressure (BLP)
  - SpO2
  - Pulse rate
- Data export functionality
- Diagnostic command interface
- Program creation and management
- Comprehensive logging system

### Technical Details
- Built with Python 3.8+
- Uses tkinter for GUI
- Implements matplotlib for real-time plotting
- Serial communication for device interface
- Thread-safe data processing
- Modular architecture for easy maintenance

### Dependencies
- pyserial
- rich
- matplotlib
- numpy

### Security
- Input validation for all user inputs
- Safe file handling
- Proper error handling and logging
- Secure serial communication

### Documentation
- Comprehensive inline documentation
- User-friendly interface
- Clear error messages
- Tooltips for better user guidance

## [1.0.1] - 2024-03-10

### Added
- Comprehensive training scripts for both fixed-wing and rotary-wing aircraft
- Language support for Spanish and English in training scripts
- Night vision training procedures for fixed-wing aircraft
- Detailed setup instructions and flight commands in training scripts
- Emergency procedures and safety reminders
- Improved script organization with separate frames for each aircraft type
- Clear instructions for script usage and navigation

### Enhanced
- Training tab interface with better organization
- Script viewer window with improved readability
- User interface for script selection and display

## [2.0.0] - 2024-03-20

### Added
- Advanced gas calculations with altitude compensation
- Professional results display with color-coded messages
- Dark mode support for reduced eye strain
- Automatic backup of session data
- Session summary reports
- Historical data analysis tools
- Real-time script viewer with progress tracking
- Integrated training session management

### Enhanced
- Improved calibration interface with right-side results panel
- Enhanced data validation with additional parameters:
  - Altitude (0-35,000 ft)
  - Temperature (15-35°C)
- Modernized About window with updated information
- Better organization of features and documentation
- More comprehensive error handling and logging
- Improved scrolling functionality across all tabs
- Updated package version requirements

### Technical Improvements
- Refactored code for better maintainability
- Enhanced thread safety in data processing
- Improved memory management
- Better error handling during cleanup operations
- More efficient data processing algorithms

### Documentation
- Updated README with comprehensive feature list
- Added Quick Start Guide
- Enhanced installation instructions
- Added support contact information
- Improved inline documentation

### Dependencies
- Updated minimum versions:
  - pyserial>=3.5
  - rich>=13.0.0
  - matplotlib>=3.7.0
  - numpy>=1.24.0

[1.0.0]: https://github.com/strikerdlm/ROBD2_GUI/releases/tag/v1.0.0
[1.0.1]: https://github.com/strikerdlm/ROBD2_GUI/compare/v1.0.0...v1.0.1
[2.0.0]: https://github.com/strikerdlm/ROBD2_GUI/compare/v1.0.1...v2.0.0 