# ROBD2 Safety Management Dashboard

A modern, publication-quality TypeScript frontend for the ROBD2 Reduced Oxygen Breathing Device, designed for aerospace physiology training and research.

## Overview

This dashboard provides real-time monitoring, gas calculations, and performance analysis for hypoxia awareness training using the ROBD2 device. The interface is designed for both scientific accuracy and investor-ready presentations.

## Features

### Real-Time Monitoring Dashboard
- **Altitude Profile Visualization** - Real-time altitude tracking with warning and critical zone markers
- **SpO₂ Gauge Chart** - Publication-quality gauge showing oxygen saturation with clinical thresholds
- **Multi-parameter Time Series** - Synchronized charts for O₂ concentration, BLP, SpO₂, and pulse
- **Interactive Data Zoom** - Pan and zoom through session data with smooth animations

### Gas Calculators
- **Physiological Parameters** - Calculate PAO₂, SaO₂, ventilation rate, and heart rate at altitude
- **Consumption Calculator** - Estimate gas usage for training programs
- **Cylinder Capacity** - Determine maximum students per cylinder set
- **Single Session Cost** - Calculate per-session operational costs

### Calibration System
- Two-point O₂ sensor calibration (21% room air and 100% O₂)
- Visual calibration curve display
- ADC voltage correlation
- CSV export for calibration records

### Performance Analytics
- Statistical distribution histograms
- Box plot analysis for data quality assessment
- Coefficient of variation (CV) metrics
- Session quality indicators

## Scientific References

All calculations and thresholds in this application are based on peer-reviewed aerospace medicine literature:

1. **West JB.** Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.
   - Barometric pressure and alveolar gas equations

2. **FAA-H-8083-25B** Pilot's Handbook of Aeronautical Knowledge, Chapter 17.
   - Hypoxia classifications and altitude physiology

3. **Richalet JP.** Altitude and the cardiovascular system. Presse Med. 2012;41(6 Pt 2):638-43.
   - Heart rate response to hypoxic conditions

4. **Severinghaus JW.** Simple, accurate equations for human blood O2 dissociation computations. J Appl Physiol. 1979;46(3):599-602.
   - O₂-hemoglobin dissociation modeling

5. **Weil JV.** Ventilatory responses to hypoxia and hyperoxia. Compr Physiol. 2012;2(2):1495-1550.
   - Hypoxic ventilatory response calculations

## Technology Stack

- **React 19** - Modern component-based UI
- **TypeScript** - Type-safe development
- **ECharts 6** - Professional-grade data visualization
- **Tailwind CSS 3** - Utility-first styling
- **Framer Motion** - Smooth animations
- **i18next** - Internationalization (English/Spanish)
- **Vite** - Fast build tooling

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view in development mode.

## Production Build

```bash
npm run build
```

Outputs optimized files to `dist/` directory.

## Type Checking

```bash
npm run typecheck
```

## Project Structure

```
frontend/
├── src/
│   ├── charts/          # ECharts theme and configurations
│   ├── components/      # Reusable UI components
│   ├── hooks/           # Custom React hooks
│   ├── i18n/            # Internationalization files
│   ├── pages/           # Page components
│   ├── services/        # Data services and API mock
│   ├── types/           # TypeScript type definitions
│   └── App.tsx          # Main application component
├── public/              # Static assets
└── dist/                # Production build output
```

## Safety Thresholds

The application implements the following clinical thresholds based on aerospace medicine standards:

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| SpO₂      | ≥90%   | 88-90%  | <85%     |
| Pulse     | 40-120 | >120    | >180     |
| Altitude  | <25,000 ft | 25,000-30,000 ft | >30,000 ft |

## Demo Mode

The application includes a demo mode that generates physiologically plausible data when no ROBD2 device is connected. This allows for:
- UI testing and development
- Investor demonstrations
- Training without hardware

## Author

**Diego Malpica MD**
- Aerospace Medicine
- Aerospace Physiology Instructor
- Colombian Aerospace Force

## License

Copyright © 2024-2026 Diego Malpica MD. All rights reserved.

---

*This software is designed for use in controlled aerospace physiology training environments under the supervision of trained professionals.*
