/**
 * Diagnostics Page
 * 
 * Device command interface for ROBD2 troubleshooting
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
  Stethoscope,
  Send,
  Terminal,
  Gauge,
  Zap,
} from 'lucide-react';

const QUICK_COMMANDS = [
  'GET RUN ALL',
  'GET RUN O2CONC',
  'GET RUN BLPRESS',
  'GET RUN SPO2',
  'GET RUN PULSE',
  'GET RUN ALT',
  'GET RUN FINALALT',
  'GET RUN ELTIME',
  'GET RUN REMTIME',
  'GET INFO',
  'GET STATUS',
];

export function Diagnostics() {
  const { t } = useTranslation();
  const [selectedCommand, setSelectedCommand] = useState(QUICK_COMMANDS[0]);
  const [customCommand, setCustomCommand] = useState('');
  const [mfcNum, setMfcNum] = useState(1);
  const [adcNum, setAdcNum] = useState(12);
  const [commandHistory, setCommandHistory] = useState<{ cmd: string; response: string; time: Date }[]>([]);

  const sendCommand = (cmd: string) => {
    // Simulate command response in demo mode
    const responses: Record<string, string> = {
      'GET RUN ALL': '1,RUN,25000,ASCEND,15.5,5.2,120,300,92.5,78',
      'GET RUN O2CONC': '15.5',
      'GET RUN BLPRESS': '5.2',
      'GET RUN SPO2': '92.5',
      'GET RUN PULSE': '78',
      'GET RUN ALT': '25000',
      'GET INFO': 'ROBD2-9515 v2.1.3',
      'GET STATUS': 'OK',
    };
    
    const response = responses[cmd] || `Response for: ${cmd} (Demo Mode)`;
    
    setCommandHistory(prev => [
      { cmd, response, time: new Date() },
      ...prev.slice(0, 49),
    ]);
  };

  const handleSend = () => {
    const cmd = customCommand.trim() || selectedCommand;
    sendCommand(cmd);
    if (customCommand.trim()) setCustomCommand('');
  };

  const handleMfcFlow = () => {
    sendCommand(`GET MFC ${mfcNum}`);
  };

  const handleAdcVoltage = () => {
    sendCommand(`GET ADC ${adcNum}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <Stethoscope className="text-primary-500" />
          {t('diagnostics.title')}
        </h1>
      </div>

      {/* Quick Commands */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">{t('diagnostics.quickCommands')}</h3>
        <select
          value={selectedCommand}
          onChange={(e) => setSelectedCommand(e.target.value)}
          className="input-field mb-4"
        >
          {QUICK_COMMANDS.map(cmd => (
            <option key={cmd} value={cmd}>{cmd}</option>
          ))}
        </select>

        {/* Custom Command */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-400 mb-2">
            {t('diagnostics.customCommand')}
          </label>
          <input
            type="text"
            value={customCommand}
            onChange={(e) => setCustomCommand(e.target.value)}
            placeholder={t('diagnostics.placeholder')}
            className="input-field"
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
        </div>

        {/* MFC and ADC */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('diagnostics.mfcNum')}
            </label>
            <input
              type="number"
              value={mfcNum}
              onChange={(e) => setMfcNum(Number(e.target.value))}
              min={0}
              max={9}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('diagnostics.adcNum')}
            </label>
            <input
              type="number"
              value={adcNum}
              onChange={(e) => setAdcNum(Number(e.target.value))}
              min={1}
              max={16}
              className="input-field"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3">
          <button onClick={handleSend} className="btn-primary">
            <Send size={18} />
            {t('diagnostics.send')}
          </button>
          <button onClick={handleMfcFlow} className="btn-secondary">
            <Gauge size={18} />
            {t('diagnostics.getMfcFlow')}
          </button>
          <button onClick={handleAdcVoltage} className="btn-secondary">
            <Zap size={18} />
            {t('diagnostics.getAdcVoltage')}
          </button>
        </div>
      </div>

      {/* Command History */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Terminal size={20} />
          Command History
        </h3>
        <div className="max-h-[400px] overflow-y-auto scrollbar-thin space-y-3">
          {commandHistory.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No commands sent yet</p>
          ) : (
            commandHistory.map((entry, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="p-4 bg-white/5 rounded-xl"
              >
                <div className="flex items-center justify-between mb-2">
                  <code className="text-primary-400 font-mono text-sm">{entry.cmd}</code>
                  <span className="text-xs text-gray-500">
                    {entry.time.toLocaleTimeString()}
                  </span>
                </div>
                <pre className="text-green-400 font-mono text-sm bg-black/30 p-3 rounded-lg overflow-x-auto">
                  {entry.response}
                </pre>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Diagnostics;
