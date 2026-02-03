/**
 * ROBD2 Safety Management Dashboard - Type Definitions
 * 
 * These types define the data structures used throughout the application
 * for aerospace physiology monitoring and safety management.
 * 
 * @author Diego Malpica MD - Aerospace Medicine
 * @version 2.0.0
 */

/** Live sample data from the ROBD2 device */
export interface LiveSample {
  timestamp: Date;
  altitude: number;       // feet - range: 0-35,000 ft
  o2Conc: number;         // percentage - range: 0-100%
  blp: number;            // mmHg (Barometric Lung Pressure)
  spo2: number;           // percentage - range: 50-100%
  pulse: number;          // bpm - range: 20-220 bpm
  o2Voltage?: number;     // V - ADC reading
  errorPercent?: number;  // percentage - calibration error
}

/** Time series data point for charting */
export interface DataPoint {
  time: number;           // seconds from session start
  value: number;
}

/** Connection status for the device */
export interface ConnectionStatus {
  connected: boolean;
  port: string | null;
  threadAlive: boolean;
  pollInterval: number;
  sampleAgeSec: number | null;
  attemptAgeSec: number | null;
  consecutiveErrors: number;
}

/** Calibration data structure */
export interface CalibrationData {
  roomAirO2: number | null;
  roomAirAdc: number | null;
  pureO2O2: number | null;
  pureO2Adc: number | null;
  timestamp?: Date;
}

/** Physiological parameters at altitude */
export interface PhysiologicalParams {
  altitudeFt: number;
  altitudeM: number;
  pressureMmHg: number;
  pao2: number;           // Alveolar O2 partial pressure
  sao2: number;           // Arterial O2 saturation
  ventilationRateLMin: number;
  heartRateBpm: number;
}

/** Gas consumption calculation results */
export interface GasConsumption {
  weeklyAirM3: number;
  weeklyNitrogenM3: number;
  weeklyOxygenM3: number;
  totalAirM3: number;
  totalNitrogenM3: number;
  totalOxygenM3: number;
  totalCostAir: number;
  totalCostNitrogen: number;
  totalCostOxygen: number;
  totalCost: number;
  totalCostWithContingency: number;
}

/** Cylinder capacity calculation results */
export interface CylinderCapacity {
  airPerSessionM3: number;
  nitrogenPerSessionM3: number;
  oxygenPerSessionM3: number;
  maxStudentsAir: number;
  maxStudentsNitrogen: number;
  maxStudentsOxygen: number;
  maxStudents: number;
}

/** Single session cost calculation */
export interface SingleSessionCost {
  airConsumedM3: number;
  nitrogenConsumedM3: number;
  oxygenConsumedM3: number;
  costAir: number;
  costNitrogen: number;
  costOxygen: number;
  totalCost: number;
}

/** Training program step */
export interface ProgramStep {
  stepNumber: number;
  mode: 'HLD' | 'CHG' | 'END';  // Hold, Change, End
  altitude: number;             // feet
  value: number;                // minutes (HLD) or ft/min (CHG)
}

/** Training program */
export interface TrainingProgram {
  programNumber: number;
  name: string;
  steps: ProgramStep[];
}

/** Performance statistics */
export interface PerformanceStats {
  samples: number;
  meanO2: number;
  stdO2: number;
  cvPercent: number;  // Coefficient of variation
  minO2?: number;
  maxO2?: number;
  minSpO2?: number;
  maxSpO2?: number;
}

/** Debug log entry */
export interface DebugLogEntry {
  timestamp: Date;
  type: 'marker' | 'event' | 'error' | 'command';
  message: string;
}

/** Application language */
export type Language = 'en' | 'es';

/** Navigation page keys */
export type PageKey = 
  | 'dashboard'
  | 'connection'
  | 'diagnostics'
  | 'calibration'
  | 'gasCalculators'
  | 'programs'
  | 'logging'
  | 'performance';

/** Alert severity levels */
export type AlertSeverity = 'info' | 'success' | 'warning' | 'error';

/** Chart theme configuration */
export interface ChartTheme {
  backgroundColor: string;
  textColor: string;
  axisLineColor: string;
  splitLineColor: string;
  tooltipBackgroundColor: string;
  colors: string[];
}

/** Safe operational ranges based on aerospace physiology standards */
export const SAFE_RANGES = {
  spo2: { min: 90, warning: 88, critical: 85 },
  o2Conc: { min: 0, max: 100 },
  pulse: { min: 40, max: 180, warning: 120 },
  altitude: { max: 35000, warning: 25000, critical: 30000 },
} as const;

/**
 * Data validation ranges per FAA/JAA aerospace physiology standards
 * Reference: FAA-H-8083-25B Pilot's Handbook of Aeronautical Knowledge
 */
export const VALIDATION_RANGES = {
  spo2: { min: 50, max: 100 },
  o2Conc: { min: 0, max: 100 },
  pulse: { min: 20, max: 220 },
  altitude: { min: 0, max: 35000 },
  temperature: { min: 15, max: 35 },
} as const;
