/**
 * Logging Page
 * 
 * Data export and debug logging for ROBD2 sessions
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
  FileText,
  Download,
  Flag,
  Save,
  CheckCircle,
  XCircle,
} from 'lucide-react';

interface LoggingProps {
  onExportCsv: () => string;
}

export function Logging({ onExportCsv }: LoggingProps) {
  const { t } = useTranslation();
  const [filename, setFilename] = useState(() => {
    const now = new Date();
    return `flight_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}${String(now.getSeconds()).padStart(2, '0')}.csv`;
  });
  const [debugLog, setDebugLog] = useState<{ time: Date; message: string }[]>([]);
  const [saveStatus, setSaveStatus] = useState<{ success: boolean; message: string } | null>(null);

  const addDebugMarker = () => {
    const entry = {
      time: new Date(),
      message: `Marker ${debugLog.length + 1}`,
    };
    setDebugLog(prev => [...prev, entry]);
  };

  const handleSaveCsv = () => {
    try {
      const csvData = onExportCsv();
      
      if (!csvData) {
        setSaveStatus({ success: false, message: 'No data to export' });
        return;
      }
      
      const blob = new Blob([csvData], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
      
      setSaveStatus({ success: true, message: `Downloaded: ${filename}` });
    } catch (error) {
      setSaveStatus({ success: false, message: `Error: ${error}` });
    }
    
    setTimeout(() => setSaveStatus(null), 5000);
  };

  const handleDownloadDebugLog = () => {
    const content = debugLog.length > 0
      ? debugLog.map(e => `${e.time.toISOString()} - ${e.message}`).join('\n')
      : '(empty)';
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `debug_${new Date().toISOString().replace(/[:.]/g, '-')}.log`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <FileText className="text-primary-500" />
          {t('logging.title')}
        </h1>
      </div>

      {/* Export Section */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">{t('logging.exportBuffered')}</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('logging.filename')}
            </label>
            <input
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="input-field"
            />
          </div>
          <button onClick={handleSaveCsv} className="btn-primary">
            <Save size={18} />
            {t('logging.saveBuffer')}
          </button>
          
          {saveStatus && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 rounded-xl flex items-center gap-3 ${
                saveStatus.success
                  ? 'bg-green-500/10 border border-green-500/30'
                  : 'bg-red-500/10 border border-red-500/30'
              }`}
            >
              {saveStatus.success ? (
                <CheckCircle size={20} className="text-green-400" />
              ) : (
                <XCircle size={20} className="text-red-400" />
              )}
              <span className={saveStatus.success ? 'text-green-300' : 'text-red-300'}>
                {saveStatus.message}
              </span>
            </motion.div>
          )}
        </div>
      </div>

      {/* Debug Log Section */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">{t('logging.debugLog')}</h3>
        <div className="flex gap-3 mb-4">
          <button onClick={addDebugMarker} className="btn-secondary">
            <Flag size={18} />
            {t('logging.addMarker')}
          </button>
          <button onClick={handleDownloadDebugLog} className="btn-secondary">
            <Download size={18} />
            {t('logging.downloadDebug')}
          </button>
        </div>
        
        {/* Log Entries */}
        <div className="max-h-[300px] overflow-y-auto scrollbar-thin bg-black/20 rounded-xl p-4">
          {debugLog.length === 0 ? (
            <p className="text-gray-500 text-center py-8">{t('logging.empty')}</p>
          ) : (
            <div className="space-y-2 font-mono text-sm">
              {debugLog.map((entry, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-4 text-gray-300"
                >
                  <span className="text-gray-500 whitespace-nowrap">
                    {entry.time.toLocaleTimeString()}
                  </span>
                  <span className="text-primary-400">{entry.message}</span>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Data Export Information */}
      <div className="glass-card p-6 bg-blue-500/5">
        <h3 className="text-lg font-semibold text-white mb-3">Export Format Information</h3>
        <div className="text-sm text-gray-400 space-y-2">
          <p>Exported CSV files contain the following columns:</p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li>Time (s) - Seconds from session start</li>
            <li>Time (min) - Minutes from session start</li>
            <li>Altitude (ft) - Current altitude in feet</li>
            <li>O₂ Concentration (%) - Breathing gas O₂ percentage</li>
            <li>BLP (mmHg) - Barometric lung pressure</li>
            <li>SpO₂ (%) - Pulse oximeter oxygen saturation</li>
            <li>Pulse (bpm) - Heart rate in beats per minute</li>
            <li>O₂ Voltage (V) - Raw ADC sensor voltage</li>
            <li>Error (%) - Calibration error percentage</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Logging;
