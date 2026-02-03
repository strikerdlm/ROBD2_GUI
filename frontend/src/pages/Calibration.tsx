/**
 * Calibration Page
 * 
 * O2 sensor calibration interface for ROBD2
 */

// Calibration Page Component
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import ReactECharts from 'echarts-for-react';
import {
  Target,
  Wind,
  Download,
  Trash2,
  Info,
  CheckCircle,
} from 'lucide-react';
import type { EChartsOption } from 'echarts';
import { CHART_COLORS } from '../charts/theme';
import type { CalibrationData, LiveSample } from '../types';

interface CalibrationProps {
  isConnected: boolean;
  latestSample: LiveSample | null;
  calibrationData: CalibrationData;
  onRecordRoomAir: () => void;
  onRecordPureO2: () => void;
  onClearCalibration: () => void;
}

export function Calibration({
  isConnected,
  latestSample,
  calibrationData,
  onRecordRoomAir,
  onRecordPureO2,
  onClearCalibration,
}: CalibrationProps) {
  const { t } = useTranslation();

  const hasRoomAir = calibrationData.roomAirO2 !== null;
  const hasPureO2 = calibrationData.pureO2O2 !== null;
  const hasAnyCalibration = hasRoomAir || hasPureO2;

  // Calibration curve chart
  const calibrationCurveOptions: EChartsOption = {
    title: {
      text: 'O₂ Sensor Calibration Curve',
      subtext: 'Linear interpolation between calibration points',
      left: 'center',
      textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
    },
    xAxis: {
      type: 'value',
      name: 'ADC Voltage (V)',
      nameLocation: 'middle',
      nameGap: 30,
      min: 0,
      max: 12,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    yAxis: {
      type: 'value',
      name: 'O₂ Concentration (%)',
      nameLocation: 'middle',
      nameGap: 40,
      min: 0,
      max: 100,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    series: [
      // Calibration line
      {
        type: 'line' as const,
        data: hasRoomAir && hasPureO2
          ? [
              [calibrationData.roomAirAdc as number, calibrationData.roomAirO2 as number],
              [calibrationData.pureO2Adc as number, calibrationData.pureO2O2 as number],
            ]
          : hasRoomAir
          ? [[calibrationData.roomAirAdc as number, calibrationData.roomAirO2 as number]]
          : hasPureO2
          ? [[calibrationData.pureO2Adc as number, calibrationData.pureO2O2 as number]]
          : [],
        lineStyle: { color: CHART_COLORS.o2, width: 3 },
        itemStyle: { color: CHART_COLORS.o2 },
        symbol: 'circle',
        symbolSize: 12,
      },
      // Room air point
      ...(hasRoomAir ? [{
        type: 'scatter' as const,
        data: [[calibrationData.roomAirAdc as number, calibrationData.roomAirO2 as number]],
        symbolSize: 20,
        itemStyle: { color: CHART_COLORS.altitude },
        label: {
          show: true,
          formatter: 'Room Air\n21%',
          position: 'right' as const,
          color: CHART_COLORS.text,
        },
      }] : []),
      // Pure O2 point
      ...(hasPureO2 ? [{
        type: 'scatter' as const,
        data: [[calibrationData.pureO2Adc as number, calibrationData.pureO2O2 as number]],
        symbolSize: 20,
        itemStyle: { color: CHART_COLORS.o2 },
        label: {
          show: true,
          formatter: '100% O₂',
          position: 'right' as const,
          color: CHART_COLORS.text,
        },
      }] : []),
      // Current reading
      ...(latestSample ? [{
        type: 'scatter' as const,
        data: [[latestSample.o2Conc / 10, latestSample.o2Conc]],
        symbolSize: 16,
        itemStyle: { 
          color: CHART_COLORS.pulse,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: 'Current',
          position: 'top' as const,
          color: CHART_COLORS.text,
        },
      }] : []),
    ],
  };

  const downloadCalibrationCsv = () => {
    const lines = ['type,o2_pct,adc'];
    if (hasRoomAir) {
      lines.push(`room_air,${calibrationData.roomAirO2},${calibrationData.roomAirAdc}`);
    }
    if (hasPureO2) {
      lines.push(`pure_o2,${calibrationData.pureO2O2},${calibrationData.pureO2Adc}`);
    }
    const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'calibration.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <Target className="text-primary-500" />
          {t('calibration.title')}
        </h1>
      </div>

      {/* Info Banner */}
      {!isConnected && (
        <div className="glass-card p-4 bg-blue-500/10 border-blue-500/30 flex gap-3">
          <Info size={20} className="text-blue-400 flex-shrink-0" />
          <p className="text-blue-300 text-sm">{t('calibration.info')}</p>
        </div>
      )}

      {/* Current Reading */}
      {latestSample && (
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Current O₂ Reading</h3>
          <div className="flex items-center gap-8">
            <div>
              <span className="text-4xl font-bold text-primary-400">
                {latestSample.o2Conc.toFixed(2)}
              </span>
              <span className="text-xl text-gray-400 ml-2">%</span>
            </div>
            <div className="text-gray-500">
              <p>ADC Equivalent: {(latestSample.o2Conc / 10).toFixed(3)} V</p>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="glass-card p-6">
        <div className="flex flex-wrap gap-4">
          <button onClick={onRecordRoomAir} className="btn-primary flex-1 min-w-[200px]">
            <Wind size={18} />
            {t('calibration.recordRoomAir')}
          </button>
          <button onClick={onRecordPureO2} className="btn-primary flex-1 min-w-[200px]">
            <Wind size={18} />
            {t('calibration.recordPureO2')}
          </button>
          <button
            onClick={onClearCalibration}
            disabled={!hasAnyCalibration}
            className="btn-secondary"
          >
            <Trash2 size={18} />
            {t('calibration.clear')}
          </button>
        </div>
      </div>

      {/* Calibration Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Room Air Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className={`glass-card p-6 ${hasRoomAir ? 'border-green-500/30' : ''}`}
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">{t('calibration.roomAirCard')}</h3>
            {hasRoomAir && <CheckCircle size={24} className="text-green-400" />}
          </div>
          <div className="space-y-4">
            <div>
              <span className="text-gray-500 text-sm">O₂ Concentration</span>
              <p className="text-3xl font-bold text-primary-400">
                {hasRoomAir ? `${calibrationData.roomAirO2?.toFixed(2)} %` : '—'}
              </p>
            </div>
            <div className="pt-4 border-t border-white/10">
              <span className="text-gray-500 text-sm">{t('calibration.adcValue')}</span>
              <p className="text-xl font-mono text-gray-300">
                {hasRoomAir ? calibrationData.roomAirAdc?.toFixed(3) : '—'}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Pure O2 Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className={`glass-card p-6 ${hasPureO2 ? 'border-green-500/30' : ''}`}
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">{t('calibration.pureO2Card')}</h3>
            {hasPureO2 && <CheckCircle size={24} className="text-green-400" />}
          </div>
          <div className="space-y-4">
            <div>
              <span className="text-gray-500 text-sm">O₂ Concentration</span>
              <p className="text-3xl font-bold text-green-400">
                {hasPureO2 ? `${calibrationData.pureO2O2?.toFixed(2)} %` : '—'}
              </p>
            </div>
            <div className="pt-4 border-t border-white/10">
              <span className="text-gray-500 text-sm">{t('calibration.adcValue')}</span>
              <p className="text-xl font-mono text-gray-300">
                {hasPureO2 ? calibrationData.pureO2Adc?.toFixed(3) : '—'}
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Calibration Chart */}
      <div className="chart-container h-[400px]">
        <ReactECharts
          option={calibrationCurveOptions}
          style={{ height: '100%' }}
          opts={{ renderer: 'svg' }}
        />
      </div>

      {/* Download Button */}
      {hasAnyCalibration && (
        <button onClick={downloadCalibrationCsv} className="btn-primary">
          <Download size={18} />
          {t('calibration.downloadCsv')}
        </button>
      )}
    </div>
  );
}

export default Calibration;
