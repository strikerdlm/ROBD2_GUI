/**
 * MetricCard Component
 * 
 * Displays a key metric with optional trend and status indicators
 * Designed for real-time aerospace physiology monitoring
 */

import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react';
import { SAFE_RANGES } from '../types';

interface MetricCardProps {
  title: string;
  value: number | string;
  unit: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'stable';
  color?: string;
  warning?: boolean;
  critical?: boolean;
  min?: number;
  max?: number;
  format?: (value: number) => string;
}

export function MetricCard({
  title,
  value,
  unit,
  icon,
  trend,
  color = 'from-primary-400 to-cyan-400',
  warning = false,
  critical = false,
  min,
  max,
  format,
}: MetricCardProps) {
  const numValue = typeof value === 'number' ? value : parseFloat(value as string);
  const displayValue = format && typeof value === 'number' ? format(value) : value;
  
  // Calculate percentage for progress bar if min/max provided
  const percentage = min !== undefined && max !== undefined
    ? Math.min(100, Math.max(0, ((numValue - min) / (max - min)) * 100))
    : null;

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp size={16} className="text-green-400" />;
      case 'down':
        return <TrendingDown size={16} className="text-red-400" />;
      default:
        return <Minus size={16} className="text-gray-400" />;
    }
  };

  const borderColor = critical
    ? 'border-red-500/50'
    : warning
    ? 'border-yellow-500/50'
    : 'border-white/10';

  return (
    <motion.div
      whileHover={{ y: -2, scale: 1.01 }}
      transition={{ duration: 0.2 }}
      className={`metric-card ${borderColor} ${
        critical ? 'bg-red-500/10' : warning ? 'bg-yellow-500/10' : ''
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {icon && <span className="text-gray-400">{icon}</span>}
          <span className="metric-label">{title}</span>
        </div>
        {(warning || critical) && (
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
          >
            <AlertTriangle
              size={18}
              className={critical ? 'text-red-500' : 'text-yellow-500'}
            />
          </motion.div>
        )}
      </div>
      
      <div className="flex items-end gap-2">
        <span className={`metric-value bg-gradient-to-r ${color} bg-clip-text text-transparent`}>
          {displayValue}
        </span>
        <span className="text-lg text-gray-400 mb-1">{unit}</span>
        {trend && <span className="mb-1 ml-auto">{getTrendIcon()}</span>}
      </div>

      {percentage !== null && (
        <div className="mt-4">
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${percentage}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              className={`h-full rounded-full ${
                critical
                  ? 'bg-gradient-to-r from-red-500 to-red-400'
                  : warning
                  ? 'bg-gradient-to-r from-yellow-500 to-yellow-400'
                  : 'bg-gradient-to-r from-primary-500 to-cyan-500'
              }`}
            />
          </div>
          <div className="flex justify-between mt-1 text-xs text-gray-500">
            <span>{min}</span>
            <span>{max}</span>
          </div>
        </div>
      )}
    </motion.div>
  );
}

/**
 * SpO2 Metric Card with safety thresholds
 */
export function SpO2Card({ value }: { value: number }) {
  const { warning, critical } = SAFE_RANGES.spo2;
  const isWarning = value < warning && value >= critical;
  const isCritical = value < critical;

  return (
    <MetricCard
      title="SpO₂"
      value={value}
      unit="%"
      color="from-purple-400 to-violet-400"
      warning={isWarning}
      critical={isCritical}
      min={50}
      max={100}
      format={(v) => v.toFixed(1)}
    />
  );
}

/**
 * Pulse Metric Card with safety thresholds
 */
export function PulseCard({ value }: { value: number }) {
  const { min, max, warning } = SAFE_RANGES.pulse;
  const isWarning = value > warning;

  return (
    <MetricCard
      title="Pulse"
      value={value}
      unit="bpm"
      color="from-yellow-400 to-orange-400"
      warning={isWarning}
      min={min}
      max={max}
      format={(v) => v.toFixed(0)}
    />
  );
}

/**
 * Altitude Metric Card with danger zones
 */
export function AltitudeCard({ value }: { value: number }) {
  const { max, warning, critical } = SAFE_RANGES.altitude;
  const isWarning = value > warning && value < critical;
  const isCritical = value >= critical;

  return (
    <MetricCard
      title="Altitude"
      value={value}
      unit="ft"
      color="from-blue-400 to-cyan-400"
      warning={isWarning}
      critical={isCritical}
      min={0}
      max={max}
      format={(v) => v.toLocaleString()}
    />
  );
}

export default MetricCard;
