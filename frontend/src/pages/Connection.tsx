/**
 * Connection Page
 * 
 * Device connection management for ROBD2
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
  Plug,
  RefreshCw,
  Power,
  PowerOff,
  Radio,
  AlertCircle,
  CheckCircle2,
  Info,
} from 'lucide-react';
import type { ConnectionStatus } from '../types';

interface ConnectionProps {
  isConnected: boolean;
  connectionStatus: ConnectionStatus;
  availablePorts: string[];
  onConnect: (port: string) => { success: boolean; message: string };
  onDisconnect: () => { success: boolean; message: string };
  isPolling: boolean;
  onStartPolling: () => void;
  onStopPolling: () => void;
}

export function Connection({
  isConnected,
  connectionStatus,
  availablePorts,
  onConnect,
  onDisconnect,
  isPolling,
  onStartPolling,
  onStopPolling,
}: ConnectionProps) {
  const { t } = useTranslation();
  const [selectedPort, setSelectedPort] = useState(availablePorts[0] || '');
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleConnect = () => {
    if (selectedPort) {
      const result = onConnect(selectedPort);
      setMessage({
        type: result.success ? 'success' : 'error',
        text: result.message,
      });
    }
  };

  const handleDisconnect = () => {
    const result = onDisconnect();
    setMessage({
      type: result.success ? 'success' : 'error',
      text: result.message,
    });
  };

  const formatAge = (seconds: number | null): string => {
    if (seconds === null) return '—';
    if (seconds >= 120) return `${(seconds / 60).toFixed(1)} min`;
    return `${seconds.toFixed(1)} s`;
  };

  return (
    <div className="space-y-6 max-w-2xl">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <Plug className="text-primary-500" />
          {t('connection.title')}
        </h1>
      </div>

      {/* Connection Card */}
      <div className="glass-card p-6 space-y-6">
        {/* Port Selection */}
        <div className="space-y-4">
          <div className="flex gap-3">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-400 mb-2">
                {t('connection.port')}
              </label>
              <select
                value={selectedPort}
                onChange={(e) => setSelectedPort(e.target.value)}
                className="input-field"
                disabled={isConnected}
              >
                {availablePorts.map((port) => (
                  <option key={port} value={port}>
                    {port}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={() => setSelectedPort(availablePorts[0] || '')}
                className="btn-secondary h-[50px]"
              >
                <RefreshCw size={18} />
                {t('connection.refresh')}
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleConnect}
              disabled={isConnected || !selectedPort}
              className="btn-primary flex-1"
            >
              <Power size={18} />
              {t('connection.connect')}
            </button>
            <button
              onClick={handleDisconnect}
              disabled={!isConnected}
              className="btn-secondary flex-1"
            >
              <PowerOff size={18} />
              {t('connection.disconnect')}
            </button>
          </div>

          {/* Polling Toggle */}
          <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
            <div className="flex items-center gap-3">
              <Radio size={20} className={isPolling ? 'text-green-400 animate-pulse' : 'text-gray-500'} />
              <span className="font-medium text-white">{t('connection.polling')}</span>
            </div>
            <button
              onClick={isPolling ? onStopPolling : onStartPolling}
              disabled={!isConnected}
              className={`relative w-14 h-8 rounded-full transition-colors duration-200 ${
                isPolling ? 'bg-green-500' : 'bg-gray-600'
              } ${!isConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <motion.div
                animate={{ x: isPolling ? 24 : 4 }}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                className="absolute top-1 w-6 h-6 bg-white rounded-full shadow-lg"
              />
            </button>
          </div>
        </div>

        {/* Status */}
        <div className="pt-4 border-t border-white/10">
          <div className="flex items-center gap-3 mb-4">
            <div
              className={`w-4 h-4 rounded-full ${
                isConnected
                  ? 'bg-green-500 shadow-lg shadow-green-500/50 animate-pulse'
                  : 'bg-red-500 shadow-lg shadow-red-500/50'
              }`}
            />
            <span className={`font-semibold ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
              {isConnected ? t('connection.connected') : t('connection.disconnected')}
            </span>
            {isConnected && connectionStatus.port && (
              <span className="text-gray-500 text-sm">({connectionStatus.port})</span>
            )}
          </div>

          {/* Connection Details */}
          {isConnected && (
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="p-3 bg-white/5 rounded-lg">
                <span className="text-gray-500">Last Sample</span>
                <p className="text-white font-mono">{formatAge(connectionStatus.sampleAgeSec)}</p>
              </div>
              <div className="p-3 bg-white/5 rounded-lg">
                <span className="text-gray-500">Poll Interval</span>
                <p className="text-white font-mono">{connectionStatus.pollInterval}s</p>
              </div>
              <div className="p-3 bg-white/5 rounded-lg">
                <span className="text-gray-500">Errors</span>
                <p className={`font-mono ${connectionStatus.consecutiveErrors > 0 ? 'text-yellow-400' : 'text-white'}`}>
                  {connectionStatus.consecutiveErrors}
                </p>
              </div>
              <div className="p-3 bg-white/5 rounded-lg">
                <span className="text-gray-500">Thread</span>
                <p className={`font-mono ${connectionStatus.threadAlive ? 'text-green-400' : 'text-gray-400'}`}>
                  {connectionStatus.threadAlive ? 'Active' : 'Inactive'}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Message */}
        {message && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-xl flex items-center gap-3 ${
              message.type === 'success'
                ? 'bg-green-500/10 border border-green-500/30'
                : 'bg-red-500/10 border border-red-500/30'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle2 size={20} className="text-green-400" />
            ) : (
              <AlertCircle size={20} className="text-red-400" />
            )}
            <span className={message.type === 'success' ? 'text-green-300' : 'text-red-300'}>
              {message.text}
            </span>
          </motion.div>
        )}

        {/* Demo Mode Info */}
        <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl flex gap-3">
          <Info size={20} className="text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-blue-300 text-sm">{t('connection.demoMode')}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Connection;
