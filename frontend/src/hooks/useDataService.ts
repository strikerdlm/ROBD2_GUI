/**
 * Custom hook for ROBD2 data service management
 * 
 * Provides real-time data updates and connection management
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import type { LiveSample, ConnectionStatus, PerformanceStats, CalibrationData } from '../types';
import mockDataService from '../services/mockDataService';

interface UseDataServiceReturn {
  // Connection
  isConnected: boolean;
  connectionStatus: ConnectionStatus;
  availablePorts: string[];
  connect: (port: string) => { success: boolean; message: string };
  disconnect: () => { success: boolean; message: string };
  
  // Data
  latestSample: LiveSample | null;
  samples: LiveSample[];
  timeSeries: {
    altitude: { time: number; value: number }[];
    o2Conc: { time: number; value: number }[];
    blp: { time: number; value: number }[];
    spo2: { time: number; value: number }[];
    pulse: { time: number; value: number }[];
  };
  
  // Polling
  isPolling: boolean;
  startPolling: () => void;
  stopPolling: () => void;
  
  // Stats & Export
  performanceStats: PerformanceStats | null;
  exportCsv: () => string;
  clearData: () => void;
  
  // Calibration
  calibrationData: CalibrationData;
  setCalibrationData: React.Dispatch<React.SetStateAction<CalibrationData>>;
  recordRoomAir: () => void;
  recordPureO2: () => void;
  clearCalibration: () => void;
}

export function useDataService(): UseDataServiceReturn {
  const [isConnected, setIsConnected] = useState(false);
  const [isPolling, setIsPolling] = useState(false);
  const [latestSample, setLatestSample] = useState<LiveSample | null>(null);
  const [samples, setSamples] = useState<LiveSample[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    connected: false,
    port: null,
    threadAlive: false,
    pollInterval: 2.0,
    sampleAgeSec: null,
    attemptAgeSec: null,
    consecutiveErrors: 0,
  });
  const [calibrationData, setCalibrationData] = useState<CalibrationData>({
    roomAirO2: null,
    roomAirAdc: null,
    pureO2O2: null,
    pureO2Adc: null,
  });
  
  const updateIntervalRef = useRef<number | null>(null);

  // Subscribe to data updates
  useEffect(() => {
    const unsubscribe = mockDataService.subscribe((sample) => {
      setLatestSample(sample);
      setSamples(mockDataService.getSamples());
    });

    return () => {
      unsubscribe();
    };
  }, []);

  // Update connection status periodically
  useEffect(() => {
    const updateStatus = () => {
      setConnectionStatus(mockDataService.getConnectionStatus());
    };

    updateIntervalRef.current = window.setInterval(updateStatus, 1000);
    
    return () => {
      if (updateIntervalRef.current) {
        clearInterval(updateIntervalRef.current);
      }
    };
  }, []);

  const connect = useCallback((port: string) => {
    const result = mockDataService.connect(port);
    setIsConnected(result.success);
    if (result.success) {
      mockDataService.startPolling(2000);
      setIsPolling(true);
    }
    return result;
  }, []);

  const disconnect = useCallback(() => {
    const result = mockDataService.disconnect();
    setIsConnected(false);
    setIsPolling(false);
    return result;
  }, []);

  const startPolling = useCallback(() => {
    if (isConnected) {
      mockDataService.startPolling(2000);
      setIsPolling(true);
    }
  }, [isConnected]);

  const stopPolling = useCallback(() => {
    mockDataService.stopPolling();
    setIsPolling(false);
  }, []);

  const clearData = useCallback(() => {
    mockDataService.clearData();
    setSamples([]);
    setLatestSample(null);
  }, []);

  const exportCsv = useCallback(() => {
    return mockDataService.exportToCsv();
  }, []);

  const recordRoomAir = useCallback(() => {
    const sample = mockDataService.getLatestSample();
    if (sample) {
      setCalibrationData(prev => ({
        ...prev,
        roomAirO2: sample.o2Conc,
        roomAirAdc: sample.o2Conc / 10,
        timestamp: new Date(),
      }));
    }
  }, []);

  const recordPureO2 = useCallback(() => {
    const sample = mockDataService.getLatestSample();
    if (sample) {
      setCalibrationData(prev => ({
        ...prev,
        pureO2O2: Math.max(sample.o2Conc, 95),
        pureO2Adc: (sample.o2Conc / 10) + 1,
        timestamp: new Date(),
      }));
    }
  }, []);

  const clearCalibration = useCallback(() => {
    setCalibrationData({
      roomAirO2: null,
      roomAirAdc: null,
      pureO2O2: null,
      pureO2Adc: null,
    });
  }, []);

  // Compute time series data
  const timeSeries = {
    altitude: mockDataService.getTimeSeries('altitude'),
    o2Conc: mockDataService.getTimeSeries('o2Conc'),
    blp: mockDataService.getTimeSeries('blp'),
    spo2: mockDataService.getTimeSeries('spo2'),
    pulse: mockDataService.getTimeSeries('pulse'),
  };

  return {
    isConnected,
    connectionStatus,
    availablePorts: mockDataService.getAvailablePorts(),
    connect,
    disconnect,
    latestSample,
    samples,
    timeSeries,
    isPolling,
    startPolling,
    stopPolling,
    performanceStats: mockDataService.getPerformanceStats(),
    exportCsv,
    clearData,
    calibrationData,
    setCalibrationData,
    recordRoomAir,
    recordPureO2,
    clearCalibration,
  };
}

export default useDataService;
