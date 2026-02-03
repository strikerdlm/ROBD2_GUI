/**
 * ROBD2 Safety Management Dashboard
 * 
 * A modern, publication-quality web interface for aerospace physiology
 * training and monitoring with the ROBD2 device.
 * 
 * @author Diego Malpica MD - Aerospace Medicine
 * @version 2.0.0
 * 
 * Scientific References:
 * - West JB. Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.
 * - FAA-H-8083-25B Pilot's Handbook of Aeronautical Knowledge, Chapter 17.
 * - Richalet JP. Altitude and the cardiovascular system. Presse Med. 2012;41(6):638-43.
 * - Severinghaus JW. Simple, accurate equations for human blood O2 dissociation computations.
 *   J Appl Physiol. 1979;46(3):599-602.
 */

import { useState, useEffect } from 'react';
import './i18n';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Connection } from './pages/Connection';
import { Diagnostics } from './pages/Diagnostics';
import { Calibration } from './pages/Calibration';
import { GasCalculators } from './pages/GasCalculators';
import { Programs } from './pages/Programs';
import { Logging } from './pages/Logging';
import { Performance } from './pages/Performance';
import { useDataService } from './hooks/useDataService';
import type { PageKey } from './types';

function App() {
  const [currentPage, setCurrentPage] = useState<PageKey>('dashboard');
  
  const {
    isConnected,
    connectionStatus,
    availablePorts,
    connect,
    disconnect,
    latestSample,
    samples,
    timeSeries,
    isPolling,
    startPolling,
    stopPolling,
    performanceStats,
    exportCsv,
    calibrationData,
    recordRoomAir,
    recordPureO2,
    clearCalibration,
  } = useDataService();

  // Auto-connect in demo mode on first load
  useEffect(() => {
    if (!isConnected && availablePorts.length > 0) {
      connect(availablePorts[0]);
    }
  }, []);

  const handleExportCsv = () => {
    const csv = exportCsv();
    if (csv) {
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `robd2_data_${new Date().toISOString().replace(/[:.]/g, '-')}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return (
          <Dashboard
            latestSample={latestSample}
            timeSeries={timeSeries}
            onExportCsv={handleExportCsv}
          />
        );
      case 'connection':
        return (
          <Connection
            isConnected={isConnected}
            connectionStatus={connectionStatus}
            availablePorts={availablePorts}
            onConnect={connect}
            onDisconnect={disconnect}
            isPolling={isPolling}
            onStartPolling={startPolling}
            onStopPolling={stopPolling}
          />
        );
      case 'diagnostics':
        return <Diagnostics />;
      case 'calibration':
        return (
          <Calibration
            isConnected={isConnected}
            latestSample={latestSample}
            calibrationData={calibrationData}
            onRecordRoomAir={recordRoomAir}
            onRecordPureO2={recordPureO2}
            onClearCalibration={clearCalibration}
          />
        );
      case 'gasCalculators':
        return <GasCalculators />;
      case 'programs':
        return <Programs />;
      case 'logging':
        return <Logging onExportCsv={exportCsv} />;
      case 'performance':
        return <Performance performanceStats={performanceStats} samples={samples} />;
      default:
        return <Dashboard latestSample={latestSample} timeSeries={timeSeries} onExportCsv={handleExportCsv} />;
    }
  };

  return (
    <Layout
      currentPage={currentPage}
      onNavigate={setCurrentPage}
      isConnected={isConnected}
    >
      {renderPage()}
    </Layout>
  );
}

export default App;
