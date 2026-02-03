/**
 * ROBD2 Mock Data Service
 * 
 * Provides simulated ROBD2 device data for demonstration purposes.
 * Generates physiologically plausible data based on altitude physiology models.
 * 
 * References:
 * - West JB. Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.
 * - FAA-H-8083-25B Pilot's Handbook of Aeronautical Knowledge, Chapter 17.
 * 
 * @author Diego Malpica MD - Aerospace Medicine
 */

import type { 
  LiveSample, 
  ConnectionStatus, 
  PhysiologicalParams,
  GasConsumption,
  CylinderCapacity,
  SingleSessionCost,
  PerformanceStats
} from '../types';

const MAX_BUFFER_SIZE = 2000;

class MockDataService {
  private samples: LiveSample[] = [];
  private startTime: Date | null = null;
  private isConnected = false;
  private pollIntervalId: number | null = null;
  private consecutiveErrors = 0;
  private lastSampleTime: Date | null = null;
  private currentAltitude = 0;
  private altitudeDirection = 1;
  private listeners: Set<(sample: LiveSample) => void> = new Set();

  /**
   * Simulate connection to ROBD2 device
   */
  connect(_port: string): { success: boolean; message: string } {
    this.isConnected = true;
    this.startTime = new Date();
    this.consecutiveErrors = 0;
    return { success: true, message: 'Connected to ROBD2 device (Demo Mode)' };
  }

  /**
   * Disconnect from device
   */
  disconnect(): { success: boolean; message: string } {
    this.isConnected = false;
    this.stopPolling();
    return { success: true, message: 'Disconnected from device' };
  }

  /**
   * Start continuous data polling
   */
  startPolling(intervalMs: number = 2000): void {
    if (this.pollIntervalId !== null) return;
    
    this.pollIntervalId = window.setInterval(() => {
      const sample = this.generateSample();
      this.addSample(sample);
      this.notifyListeners(sample);
    }, intervalMs);
  }

  /**
   * Stop polling
   */
  stopPolling(): void {
    if (this.pollIntervalId !== null) {
      clearInterval(this.pollIntervalId);
      this.pollIntervalId = null;
    }
  }

  /**
   * Subscribe to new samples
   */
  subscribe(callback: (sample: LiveSample) => void): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  private notifyListeners(sample: LiveSample): void {
    for (const listener of this.listeners) {
      listener(sample);
    }
  }

  /**
   * Generate physiologically plausible sample data
   * Based on altitude physiology models from aerospace medicine literature
   */
  private generateSample(): LiveSample {
    // Simulate altitude profile (slow ascent/descent)
    const altitudeChange = (Math.random() * 500 - 100) * this.altitudeDirection;
    this.currentAltitude = Math.max(0, Math.min(35000, this.currentAltitude + altitudeChange));
    
    // Change direction occasionally
    if (Math.random() < 0.02) {
      this.altitudeDirection *= -1;
    }
    
    // If at boundaries, reverse
    if (this.currentAltitude <= 0) this.altitudeDirection = 1;
    if (this.currentAltitude >= 30000) this.altitudeDirection = -1;

    const altitude = this.currentAltitude;
    
    // Calculate physiological parameters based on altitude
    // Using barometric formula: P = P0 * (1 - L*h/T0)^(g*M/(R*L))
    const altitudeM = altitude * 0.3048;
    const pressure = 760 * Math.pow(1 - 2.25577e-5 * altitudeM, 5.25588);
    
    // O2 concentration in breathing gas (simulating ROBD2 output)
    // FiO2 decreases as altitude equivalent increases
    const baseO2 = 20.9;
    const o2Reduction = (altitude / 1000) * 0.5;
    const o2Conc = Math.max(4, baseO2 - o2Reduction + this.gaussianRandom(0, 0.3));
    
    // BLP (Barometric Lung Pressure) - simulated breathing pressure
    const blp = 5 + Math.abs(this.gaussianRandom(0, 0.5));
    
    // SpO2 calculation using Hill equation approximation
    // Reference: Severinghaus JW. Simple, accurate equations for human blood O2 dissociation computations.
    // J Appl Physiol. 1979;46(3):599-602.
    const pio2 = (pressure - 47) * 0.2095;
    const pao2 = Math.max(20, pio2 - 5);
    const theoreticalSao2 = 100 * Math.pow(pao2, 3) / (Math.pow(pao2, 3) + Math.pow(26.6, 3));
    const spo2 = Math.min(100, Math.max(50, theoreticalSao2 + this.gaussianRandom(0, 1)));
    
    // Pulse rate increases with altitude (hypoxic response)
    // Reference: Richalet JP. Altitude and the cardiovascular system. Presse Med. 2012;41(6 Pt 2):638-43.
    const basePulse = 72;
    const pulseIncrease = (altitude / 5000) * 5;
    const pulse = Math.min(180, Math.max(40, basePulse + pulseIncrease + this.gaussianRandom(0, 3)));
    
    const now = new Date();
    this.lastSampleTime = now;
    
    return {
      timestamp: now,
      altitude,
      o2Conc,
      blp,
      spo2,
      pulse,
      o2Voltage: o2Conc / 10,
      errorPercent: Math.abs(this.gaussianRandom(0, 0.5)),
    };
  }

  /**
   * Box-Muller transform for Gaussian random numbers
   */
  private gaussianRandom(mean: number, stdDev: number): number {
    const u1 = Math.random();
    const u2 = Math.random();
    const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return mean + z * stdDev;
  }

  /**
   * Add sample to buffer with validation
   */
  private addSample(sample: LiveSample): void {
    if (!this.startTime) {
      this.startTime = sample.timestamp;
    }
    
    // Validate and clamp values
    const validatedSample: LiveSample = {
      ...sample,
      spo2: Math.max(50, Math.min(100, sample.spo2)),
      o2Conc: Math.max(0, Math.min(100, sample.o2Conc)),
      pulse: Math.max(20, Math.min(220, sample.pulse)),
      altitude: Math.max(0, Math.min(35000, sample.altitude)),
    };
    
    this.samples.push(validatedSample);
    
    // Maintain buffer size
    if (this.samples.length > MAX_BUFFER_SIZE) {
      this.samples.shift();
    }
  }

  /**
   * Get all samples
   */
  getSamples(): LiveSample[] {
    return [...this.samples];
  }

  /**
   * Get latest sample
   */
  getLatestSample(): LiveSample | null {
    return this.samples.length > 0 ? this.samples[this.samples.length - 1] : null;
  }

  /**
   * Get time series data for a specific metric
   */
  getTimeSeries(metric: keyof LiveSample): { time: number; value: number }[] {
    if (!this.startTime || this.samples.length === 0) return [];
    
    const startMs = this.startTime.getTime();
    return this.samples.map(s => ({
      time: (s.timestamp.getTime() - startMs) / 1000,
      value: s[metric] as number,
    }));
  }

  /**
   * Get connection status
   */
  getConnectionStatus(): ConnectionStatus {
    const now = Date.now();
    return {
      connected: this.isConnected,
      port: this.isConnected ? 'COM3 (Demo)' : null,
      threadAlive: this.pollIntervalId !== null,
      pollInterval: 2.0,
      sampleAgeSec: this.lastSampleTime ? (now - this.lastSampleTime.getTime()) / 1000 : null,
      attemptAgeSec: this.lastSampleTime ? (now - this.lastSampleTime.getTime()) / 1000 : null,
      consecutiveErrors: this.consecutiveErrors,
    };
  }

  /**
   * Calculate performance statistics
   */
  getPerformanceStats(): PerformanceStats | null {
    if (this.samples.length < 2) return null;
    
    const o2Values = this.samples.map(s => s.o2Conc);
    const spo2Values = this.samples.map(s => s.spo2);
    
    const mean = o2Values.reduce((a, b) => a + b, 0) / o2Values.length;
    const variance = o2Values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / o2Values.length;
    const std = Math.sqrt(variance);
    
    return {
      samples: this.samples.length,
      meanO2: mean,
      stdO2: std,
      cvPercent: mean > 0 ? (std / mean) * 100 : 0,
      minO2: Math.min(...o2Values),
      maxO2: Math.max(...o2Values),
      minSpO2: Math.min(...spo2Values),
      maxSpO2: Math.max(...spo2Values),
    };
  }

  /**
   * Clear all data
   */
  clearData(): void {
    this.samples = [];
    this.startTime = null;
    this.currentAltitude = 0;
  }

  /**
   * Export data to CSV format
   */
  exportToCsv(): string {
    if (this.samples.length === 0 || !this.startTime) return '';
    
    const headers = [
      'Time (s)',
      'Time (min)',
      'Altitude (ft)',
      'O2 Concentration (%)',
      'BLP (mmHg)',
      'SpO2 (%)',
      'Pulse (bpm)',
      'O2 Voltage (V)',
      'Error (%)',
    ];
    
    const startMs = this.startTime.getTime();
    const rows = this.samples.map(s => {
      const timeS = (s.timestamp.getTime() - startMs) / 1000;
      return [
        timeS.toFixed(2),
        (timeS / 60).toFixed(2),
        s.altitude.toFixed(1),
        s.o2Conc.toFixed(2),
        s.blp.toFixed(2),
        s.spo2.toFixed(2),
        s.pulse.toFixed(0),
        (s.o2Voltage ?? 0).toFixed(3),
        (s.errorPercent ?? 0).toFixed(2),
      ].join(',');
    });
    
    return [headers.join(','), ...rows].join('\n');
  }

  /**
   * Get available ports (simulated)
   */
  getAvailablePorts(): string[] {
    return ['COM1', 'COM3', 'COM4', '/dev/ttyUSB0', '/dev/ttyACM0'];
  }
}

// Gas calculator functions based on aerospace physiology

/**
 * Calculate ventilation rate at altitude
 * Based on hypoxic ventilatory response (HVR) studies
 * Reference: Weil JV. Ventilatory responses to hypoxia and hyperoxia. 
 * Compr Physiol. 2012;2(2):1495-1550.
 */
function calculateVentilationRate(altitudeFt: number): number {
  const altitudeM = altitudeFt * 0.3048;
  const altitudeAbove1500m = Math.max(0, altitudeM - 1500);
  const ventilationIncreaseFactor = altitudeAbove1500m / 1000;
  const ventilationRate = 6.0 * (1 + ventilationIncreaseFactor);
  return Math.min(ventilationRate, 60.0);
}

/**
 * Calculate physiological parameters at altitude
 * Reference: West JB. Respiratory Physiology: The Essentials. 10th ed.
 */
export function calculatePhysiologicalParams(altitudeFt: number): PhysiologicalParams {
  const altitudeM = altitudeFt * 0.3048;
  
  // Barometric formula for pressure at altitude
  const pressure = 760 * Math.pow(1 - 2.25577e-5 * altitudeM, 5.25588);
  
  const fio2 = 0.2095;
  const pio2 = (pressure - 47) * fio2;  // Water vapor pressure = 47 mmHg
  const pao2 = pio2 - 5;  // A-a gradient approximation
  
  // Hill equation for O2-hemoglobin dissociation
  const sao2 = 100 * Math.pow(pao2, 3) / (Math.pow(pao2, 3) + Math.pow(150, 3));
  
  const ventilationRate = calculateVentilationRate(altitudeFt);
  
  // Heart rate increase with altitude
  const altitudeAbove1000m = Math.max(0, altitudeM - 1000);
  const heartRateIncrease = altitudeAbove1000m / 100;
  const heartRate = 70 + heartRateIncrease;
  
  return {
    altitudeFt,
    altitudeM,
    pressureMmHg: pressure,
    pao2,
    sao2,
    ventilationRateLMin: ventilationRate,
    heartRateBpm: heartRate,
  };
}

/**
 * Calculate gas consumption for training sessions
 */
export function calculateGasConsumption(
  studentsPerWeek: number,
  weeks: number,
  sessionDurationMin: number,
  recoveryDurationMin: number,
  altitudeFt: number,
  priceAir: number,
  priceNitrogen: number,
  priceOxygen: number,
  contingency: number
): GasConsumption {
  const ventilationRate = calculateVentilationRate(altitudeFt);
  
  const airConsumedSession = (ventilationRate * sessionDurationMin) / 1000;
  const nitrogenConsumedSession = airConsumedSession * 0.05;
  const oxygenConsumedSession = (ventilationRate * recoveryDurationMin) / 1000;
  
  const weeklyAir = airConsumedSession * studentsPerWeek;
  const weeklyNitrogen = nitrogenConsumedSession * studentsPerWeek;
  const weeklyOxygen = oxygenConsumedSession * studentsPerWeek;
  
  const totalAir = weeklyAir * weeks;
  const totalNitrogen = weeklyNitrogen * weeks;
  const totalOxygen = weeklyOxygen * weeks;
  
  const totalCostAir = totalAir * priceAir;
  const totalCostNitrogen = totalNitrogen * priceNitrogen;
  const totalCostOxygen = totalOxygen * priceOxygen;
  const totalCost = totalCostAir + totalCostNitrogen + totalCostOxygen;
  
  return {
    weeklyAirM3: weeklyAir,
    weeklyNitrogenM3: weeklyNitrogen,
    weeklyOxygenM3: weeklyOxygen,
    totalAirM3: totalAir,
    totalNitrogenM3: totalNitrogen,
    totalOxygenM3: totalOxygen,
    totalCostAir,
    totalCostNitrogen,
    totalCostOxygen,
    totalCost,
    totalCostWithContingency: totalCost * (1 + contingency),
  };
}

/**
 * Calculate cylinder capacity for training
 */
export function calculateCylinderCapacity(
  airCylM3: number,
  nitrogenCylM3: number,
  oxygenCylM3: number,
  sessionDurationMin: number,
  recoveryDurationMin: number,
  altitudeFt: number
): CylinderCapacity {
  const ventilationRate = calculateVentilationRate(altitudeFt);
  
  const airPerSession = (ventilationRate * sessionDurationMin) / 1000;
  const nitrogenPerSession = airPerSession * 0.05;
  const oxygenPerSession = (ventilationRate * recoveryDurationMin) / 1000;
  
  const maxStudentsAir = airPerSession > 0 ? Math.floor(airCylM3 / airPerSession) : 0;
  const maxStudentsNitrogen = nitrogenPerSession > 0 ? Math.floor(nitrogenCylM3 / nitrogenPerSession) : 0;
  const maxStudentsOxygen = oxygenPerSession > 0 ? Math.floor(oxygenCylM3 / oxygenPerSession) : 0;
  
  return {
    airPerSessionM3: airPerSession,
    nitrogenPerSessionM3: nitrogenPerSession,
    oxygenPerSessionM3: oxygenPerSession,
    maxStudentsAir,
    maxStudentsNitrogen,
    maxStudentsOxygen,
    maxStudents: Math.min(maxStudentsAir, maxStudentsNitrogen, maxStudentsOxygen),
  };
}

/**
 * Calculate single session costs
 */
export function calculateSingleSession(
  sessionDurationMin: number,
  recoveryDurationMin: number,
  altitudeFt: number,
  priceAir: number,
  priceNitrogen: number,
  priceOxygen: number
): SingleSessionCost {
  const ventilationRate = calculateVentilationRate(altitudeFt);
  
  const airConsumed = (ventilationRate * sessionDurationMin) / 1000;
  const nitrogenConsumed = airConsumed * 0.05;
  const oxygenConsumed = (ventilationRate * recoveryDurationMin) / 1000;
  
  const costAir = airConsumed * priceAir;
  const costNitrogen = nitrogenConsumed * priceNitrogen;
  const costOxygen = oxygenConsumed * priceOxygen;
  
  return {
    airConsumedM3: airConsumed,
    nitrogenConsumedM3: nitrogenConsumed,
    oxygenConsumedM3: oxygenConsumed,
    costAir,
    costNitrogen,
    costOxygen,
    totalCost: costAir + costNitrogen + costOxygen,
  };
}

// Export singleton instance
export const mockDataService = new MockDataService();
export default mockDataService;
