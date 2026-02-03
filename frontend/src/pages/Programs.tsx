/**
 * Programs Page
 * 
 * Training program management for ROBD2
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
  FileCode,
  Plus,
  Send,
  Plane,
  Droplets,
  Mountain,
  Save,
} from 'lucide-react';

type StepMode = 'HLD' | 'CHG' | 'END';

interface Step {
  number: number;
  mode: StepMode;
  altitude: number;
  value: number;
}

export function Programs() {
  const { t } = useTranslation();
  const [programNumber, setProgramNumber] = useState(1);
  const [programName, setProgramName] = useState('');
  const [stepNumber, setStepNumber] = useState(1);
  const [stepMode, setStepMode] = useState<StepMode>('HLD');
  const [stepAltitude, setStepAltitude] = useState(0);
  const [stepValue, setStepValue] = useState(1);
  const [fsAltitude, setFsAltitude] = useState(10000);
  const [steps, setSteps] = useState<Step[]>([]);
  const [messages, setMessages] = useState<{ text: string; type: 'success' | 'info' }[]>([]);

  const addMessage = (text: string, type: 'success' | 'info' = 'info') => {
    setMessages(prev => [{ text, type }, ...prev.slice(0, 4)]);
  };

  const saveProgramName = () => {
    const cmd = `PROG ${programNumber} NAME ${programName || 'PROGRAM'}`;
    addMessage(`Command: ${cmd}`, 'success');
  };

  const sendStep = () => {
    let cmd: string;
    if (stepMode === 'END') {
      cmd = `PROG ${programNumber} ${stepNumber} END`;
    } else {
      cmd = `PROG ${programNumber} ${stepNumber} ${stepMode} ${stepAltitude} ${stepValue}`;
    }
    
    setSteps(prev => [...prev, { number: stepNumber, mode: stepMode, altitude: stepAltitude, value: stepValue }]);
    addMessage(`Step added: ${cmd}`, 'success');
    setStepNumber(prev => prev + 1);
  };

  const enterFlightSimMode = () => {
    addMessage('Command: RUN FLSIM', 'success');
  };

  const setO2Dump = (on: boolean) => {
    addMessage(`Command: SET O2DUMP ${on ? 1 : 0}`, 'success');
  };

  const sendFsAltitude = () => {
    addMessage(`Command: SET FSALT ${fsAltitude}`, 'success');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <FileCode className="text-primary-500" />
          {t('programs.title')}
        </h1>
      </div>

      {/* Program Setup */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Program Configuration</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.programNumber')}
            </label>
            <input
              type="number"
              value={programNumber}
              onChange={(e) => setProgramNumber(Number(e.target.value))}
              min={1}
              max={20}
              className="input-field"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.programName')}
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={programName}
                onChange={(e) => setProgramName(e.target.value)}
                placeholder="Enter program name"
                className="input-field flex-1"
              />
              <button onClick={saveProgramName} className="btn-primary">
                <Save size={18} />
                {t('programs.saveName')}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Add Step */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Plus size={20} />
          {t('programs.addStep')}
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.stepNumber')}
            </label>
            <input
              type="number"
              value={stepNumber}
              onChange={(e) => setStepNumber(Number(e.target.value))}
              min={1}
              max={98}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.mode')}
            </label>
            <select
              value={stepMode}
              onChange={(e) => setStepMode(e.target.value as StepMode)}
              className="input-field"
            >
              <option value="HLD">HLD (Hold)</option>
              <option value="CHG">CHG (Change)</option>
              <option value="END">END</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('gasCalc.altitudeFt')}
            </label>
            <input
              type="number"
              value={stepAltitude}
              onChange={(e) => setStepAltitude(Number(e.target.value))}
              min={0}
              max={34000}
              step={500}
              className="input-field"
              disabled={stepMode === 'END'}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.holdOrRate')}
            </label>
            <input
              type="number"
              value={stepValue}
              onChange={(e) => setStepValue(Number(e.target.value))}
              min={0}
              className="input-field"
              disabled={stepMode === 'END'}
            />
          </div>
        </div>
        <button onClick={sendStep} className="btn-primary">
          <Send size={18} />
          {t('programs.sendStep')}
        </button>
      </div>

      {/* Current Program Steps */}
      {steps.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Program Steps</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-2 px-4 text-gray-400 font-medium">Step</th>
                  <th className="text-left py-2 px-4 text-gray-400 font-medium">Mode</th>
                  <th className="text-left py-2 px-4 text-gray-400 font-medium">Altitude (ft)</th>
                  <th className="text-left py-2 px-4 text-gray-400 font-medium">Value</th>
                </tr>
              </thead>
              <tbody>
                {steps.map((step, i) => (
                  <motion.tr
                    key={i}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="border-b border-white/5"
                  >
                    <td className="py-3 px-4 text-white">{step.number}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-sm ${
                        step.mode === 'HLD' ? 'bg-blue-500/20 text-blue-400' :
                        step.mode === 'CHG' ? 'bg-green-500/20 text-green-400' :
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {step.mode}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-white font-mono">{step.altitude.toLocaleString()}</td>
                    <td className="py-3 px-4 text-white font-mono">{step.value}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Training Helpers */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">{t('programs.trainingHelpers')}</h3>
        <div className="flex flex-wrap gap-3 mb-6">
          <button onClick={enterFlightSimMode} className="btn-secondary">
            <Plane size={18} />
            {t('programs.enterFsMode')}
          </button>
          <button onClick={() => setO2Dump(true)} className="btn-secondary">
            <Droplets size={18} />
            {t('programs.o2DumpOn')}
          </button>
          <button onClick={() => setO2Dump(false)} className="btn-secondary">
            <Droplets size={18} />
            {t('programs.o2DumpOff')}
          </button>
        </div>
        
        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-400 mb-2">
              {t('programs.setFsAlt')}
            </label>
            <input
              type="number"
              value={fsAltitude}
              onChange={(e) => setFsAltitude(Number(e.target.value))}
              min={0}
              max={34000}
              step={500}
              className="input-field"
            />
          </div>
          <button onClick={sendFsAltitude} className="btn-primary h-[50px]">
            <Mountain size={18} />
            {t('programs.sendAltitude')}
          </button>
        </div>
      </div>

      {/* Messages */}
      {messages.length > 0 && (
        <div className="space-y-2">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className={`p-3 rounded-xl text-sm ${
                msg.type === 'success' ? 'bg-green-500/10 text-green-400' : 'bg-blue-500/10 text-blue-400'
              }`}
            >
              {msg.text}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Programs;
