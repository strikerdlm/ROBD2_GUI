/**
 * Dashboard Page
 * 
 * Real-time monitoring dashboard with publication-quality ECharts visualizations
 * Displays critical aerospace physiology parameters for safety management
 * 
 * Scientific basis:
 * - Altitude-induced hypoxia monitoring based on FAA guidelines
 * - SpO2/O2 saturation thresholds per aerospace medicine standards
 * - Heart rate response to hypoxic conditions
 * 
 * References:
 * - FAA-H-8083-25B Pilot's Handbook of Aeronautical Knowledge
 * - West JB. Respiratory Physiology: The Essentials. 10th ed.
 */

import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import ReactECharts from 'echarts-for-react';
import { motion } from 'framer-motion';
import {
  Wind,
  Activity,
  Download,
  Settings,
  AlertTriangle,
  TrendingUp,
} from 'lucide-react';
import type { EChartsOption } from 'echarts';
import { CHART_COLORS, getBaseChartOptions, createLineSeries } from '../charts/theme';
import { MetricCard, SpO2Card, PulseCard, AltitudeCard } from '../components/MetricCard';
import type { LiveSample } from '../types';

interface DashboardProps {
  latestSample: LiveSample | null;
  timeSeries: {
    altitude: { time: number; value: number }[];
    o2Conc: { time: number; value: number }[];
    blp: { time: number; value: number }[];
    spo2: { time: number; value: number }[];
    pulse: { time: number; value: number }[];
  };
  onExportCsv: () => void;
}

export function Dashboard({ latestSample, timeSeries, onExportCsv }: DashboardProps) {
  const { t } = useTranslation();
  const [smoothingWindow, setSmoothingWindow] = useState(3);
  const [maxPoints, setMaxPoints] = useState(800);
  const [showSettings, setShowSettings] = useState(false);

  // Smooth data using moving average
  const smooth = (data: { time: number; value: number }[], window: number) => {
    if (window <= 1 || data.length === 0) return data;
    
    return data.map((point, i) => {
      const start = Math.max(0, i - window + 1);
      const windowData = data.slice(start, i + 1);
      const avg = windowData.reduce((sum, p) => sum + p.value, 0) / windowData.length;
      return { time: point.time, value: avg };
    });
  };

  // Limit data points
  const limitData = (data: { time: number; value: number }[], max: number) => {
    return data.length > max ? data.slice(-max) : data;
  };

  // Prepare chart data
  const processedData = useMemo(() => ({
    altitude: limitData(smooth(timeSeries.altitude, smoothingWindow), maxPoints),
    o2Conc: limitData(smooth(timeSeries.o2Conc, smoothingWindow), maxPoints),
    blp: limitData(smooth(timeSeries.blp, smoothingWindow), maxPoints),
    spo2: limitData(smooth(timeSeries.spo2, smoothingWindow), maxPoints),
    pulse: limitData(smooth(timeSeries.pulse, smoothingWindow), maxPoints),
  }), [timeSeries, smoothingWindow, maxPoints]);

  // Altitude chart options
  const altitudeChartOptions: EChartsOption = useMemo(() => ({
    ...getBaseChartOptions(),
    title: {
      text: t('dashboard.altitude'),
      subtext: 'Altitude Profile (ft)',
      left: 'center',
      textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
    },
    xAxis: {
      type: 'value',
      name: 'Time (s)',
      nameLocation: 'middle',
      nameGap: 30,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    yAxis: {
      type: 'value',
      name: 'Altitude (ft)',
      nameLocation: 'middle',
      nameGap: 50,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted, formatter: '{value}' },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    series: [
      {
        ...createLineSeries(
          'Altitude',
          processedData.altitude.map(p => [p.time, p.value]),
          CHART_COLORS.altitude,
          { areaStyle: true }
        ),
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { color: CHART_COLORS.warning, type: 'dashed' },
          data: [
            { yAxis: 25000, label: { formatter: 'Warning Zone', color: CHART_COLORS.warning } },
            { yAxis: 30000, label: { formatter: 'Critical Zone', color: CHART_COLORS.danger } },
          ],
        },
      },
    ],
  }), [processedData.altitude, t]);

  // O2 & BLP combined chart
  const o2BlpChartOptions: EChartsOption = useMemo(() => ({
    ...getBaseChartOptions(),
    title: {
      text: `${t('dashboard.o2')} & BLP`,
      subtext: 'Oxygen Concentration (%) and Barometric Lung Pressure (mmHg)',
      left: 'center',
      textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
    },
    legend: {
      data: ['O₂ %', 'BLP'],
      top: 50,
      textStyle: { color: CHART_COLORS.text },
    },
    xAxis: {
      type: 'value',
      name: 'Time (s)',
      nameLocation: 'middle',
      nameGap: 30,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    yAxis: [
      {
        type: 'value',
        name: 'O₂ %',
        position: 'left',
        axisLine: { lineStyle: { color: CHART_COLORS.o2 } },
        axisLabel: { color: CHART_COLORS.o2 },
        splitLine: { lineStyle: { color: CHART_COLORS.grid } },
      },
      {
        type: 'value',
        name: 'BLP (mmHg)',
        position: 'right',
        axisLine: { lineStyle: { color: CHART_COLORS.blp } },
        axisLabel: { color: CHART_COLORS.blp },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        ...createLineSeries(
          'O₂ %',
          processedData.o2Conc.map(p => [p.time, p.value]),
          CHART_COLORS.o2,
          { smooth: true }
        ),
        yAxisIndex: 0,
      },
      {
        ...createLineSeries(
          'BLP',
          processedData.blp.map(p => [p.time, p.value]),
          CHART_COLORS.blp,
          { smooth: true }
        ),
        yAxisIndex: 1,
      },
    ],
  }), [processedData.o2Conc, processedData.blp, t]);

  // SpO2 & Pulse combined chart
  const spo2PulseChartOptions: EChartsOption = useMemo(() => ({
    ...getBaseChartOptions(),
    title: {
      text: `${t('dashboard.spo2')} & ${t('dashboard.pulse')}`,
      subtext: 'Oxygen Saturation (%) and Heart Rate (bpm)',
      left: 'center',
      textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
    },
    legend: {
      data: ['SpO₂ %', 'Pulse'],
      top: 50,
      textStyle: { color: CHART_COLORS.text },
    },
    xAxis: {
      type: 'value',
      name: 'Time (s)',
      nameLocation: 'middle',
      nameGap: 30,
      axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      axisLabel: { color: CHART_COLORS.textMuted },
      splitLine: { lineStyle: { color: CHART_COLORS.grid } },
    },
    yAxis: [
      {
        type: 'value',
        name: 'SpO₂ %',
        position: 'left',
        min: 70,
        max: 100,
        axisLine: { lineStyle: { color: CHART_COLORS.spo2 } },
        axisLabel: { color: CHART_COLORS.spo2 },
        splitLine: { lineStyle: { color: CHART_COLORS.grid } },
      },
      {
        type: 'value',
        name: 'Pulse (bpm)',
        position: 'right',
        axisLine: { lineStyle: { color: CHART_COLORS.pulse } },
        axisLabel: { color: CHART_COLORS.pulse },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        ...createLineSeries(
          'SpO₂ %',
          processedData.spo2.map(p => [p.time, p.value]),
          CHART_COLORS.spo2,
          { smooth: true }
        ),
        yAxisIndex: 0,
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { type: 'dashed' },
          data: [
            { yAxis: 90, lineStyle: { color: CHART_COLORS.success }, label: { formatter: 'Normal', color: CHART_COLORS.success } },
            { yAxis: 88, lineStyle: { color: CHART_COLORS.warning }, label: { formatter: 'Warning', color: CHART_COLORS.warning } },
            { yAxis: 85, lineStyle: { color: CHART_COLORS.danger }, label: { formatter: 'Critical', color: CHART_COLORS.danger } },
          ],
        },
      },
      {
        ...createLineSeries(
          'Pulse',
          processedData.pulse.map(p => [p.time, p.value]),
          CHART_COLORS.pulse,
          { smooth: true }
        ),
        yAxisIndex: 1,
      },
    ],
  }), [processedData.spo2, processedData.pulse, t]);

  // Gauge chart for SpO2
  const spo2GaugeOptions: EChartsOption = useMemo(() => ({
    series: [{
      type: 'gauge',
      startAngle: 200,
      endAngle: -20,
      min: 70,
      max: 100,
      splitNumber: 6,
      axisLine: {
        lineStyle: {
          width: 20,
          color: [
            [0.5, CHART_COLORS.danger],
            [0.6, CHART_COLORS.warning],
            [1, CHART_COLORS.success],
          ],
        },
      },
      pointer: {
        icon: 'path://M2090.36389,615.30999 L2## 90.36389,615.30999 C2## 091.48372,615.30999 2## 092.40383,616.22  2## 092.40383,617.33 L2## 092.40383,703.91  C2## 092.40383,704.46 2## 092.26972,704.98 2## 092.01383,705.44 L2061.23537,754.17 C2060.22152,755.76 2058.18498,756.17 2056.59153,755.14 C2056.07003,754.8 2055.65983,754.34 2055.40383,753.8 L2022.59,705.9 C2022.2,705.39 2021.99,704.78 2021.99,704.15 L2021.99,617.33 C2021.99,616.22 2022.91011,615.30999 2024.03,615.30999 L2090.36389,615.30999 Z',
        length: '75%',
        width: 16,
        offsetCenter: [0, '5%'],
        itemStyle: {
          color: 'auto',
        },
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'auto',
          width: 2,
        },
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'auto',
          width: 3,
        },
      },
      axisLabel: {
        color: CHART_COLORS.textMuted,
        fontSize: 12,
        distance: -60,
        formatter: '{value}%',
      },
      title: {
        offsetCenter: [0, '30%'],
        fontSize: 14,
        color: CHART_COLORS.textMuted,
      },
      detail: {
        fontSize: 40,
        offsetCenter: [0, '-10%'],
        valueAnimation: true,
        formatter: '{value}%',
        color: CHART_COLORS.text,
      },
      data: [{
        value: latestSample?.spo2 ?? 0,
        name: 'SpO₂',
      }],
    }],
  }), [latestSample?.spo2]);

  // No data view
  if (!latestSample || timeSeries.altitude.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <motion.div
          animate={{ y: [0, -10, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="mb-6"
        >
          <Activity size={64} className="text-primary-500" />
        </motion.div>
        <h2 className="text-2xl font-bold text-white mb-2">{t('dashboard.noSamples')}</h2>
        <p className="text-gray-400 max-w-md">
          Connect to an ROBD2 device or enable demo mode to see real-time data visualization.
        </p>
      </div>
    );
  }

  const isLowSpO2 = latestSample.spo2 < 88;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="section-title">
            <TrendingUp className="text-primary-500" />
            {t('dashboard.title')}
          </h1>
          <p className="text-gray-400 -mt-4">
            Real-time aerospace physiology monitoring
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="btn-secondary"
          >
            <Settings size={18} />
            {t('dashboard.chartSettings')}
          </button>
          <button onClick={onExportCsv} className="btn-primary">
            <Download size={18} />
            {t('dashboard.downloadCsv')}
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="glass-card p-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                {t('dashboard.smoothingWindow')}
              </label>
              <input
                type="range"
                min="1"
                max="20"
                value={smoothingWindow}
                onChange={(e) => setSmoothingWindow(Number(e.target.value))}
                className="w-full"
              />
              <span className="text-primary-400 font-mono">{smoothingWindow}</span>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                {t('dashboard.maxPoints')}
              </label>
              <input
                type="range"
                min="100"
                max="2000"
                step="100"
                value={maxPoints}
                onChange={(e) => setMaxPoints(Number(e.target.value))}
                className="w-full"
              />
              <span className="text-primary-400 font-mono">{maxPoints}</span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Low SpO2 Alert */}
      {isLowSpO2 && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="alert-danger"
        >
          <AlertTriangle size={24} className="text-red-500 flex-shrink-0" />
          <div>
            <h3 className="font-bold text-red-400">{t('dashboard.lowSpo2')}</h3>
            <p className="text-red-300/80 text-sm">{t('dashboard.checkMask')}</p>
            <p className="text-red-400 font-mono text-lg mt-1">SpO₂: {latestSample.spo2.toFixed(1)}%</p>
          </div>
        </motion.div>
      )}

      {/* Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <AltitudeCard value={latestSample.altitude} />
        <MetricCard
          title={t('dashboard.o2')}
          value={latestSample.o2Conc.toFixed(2)}
          unit="%"
          icon={<Wind size={18} />}
          color="from-green-400 to-emerald-400"
          min={0}
          max={21}
        />
        <SpO2Card value={latestSample.spo2} />
        <PulseCard value={latestSample.pulse} />
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Altitude Chart */}
        <div className="chart-container">
          <ReactECharts
            option={altitudeChartOptions}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>

        {/* SpO2 Gauge */}
        <div className="chart-container flex items-center justify-center">
          <ReactECharts
            option={spo2GaugeOptions}
            style={{ height: '100%', width: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>
      </div>

      {/* Secondary Charts */}
      <div className="grid grid-cols-1 gap-6">
        {/* O2 & BLP Chart */}
        <div className="chart-container h-[350px]">
          <ReactECharts
            option={o2BlpChartOptions}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>

        {/* SpO2 & Pulse Chart */}
        <div className="chart-container h-[350px]">
          <ReactECharts
            option={spo2PulseChartOptions}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>
      </div>

      {/* Scientific References Footer */}
      <div className="glass-card p-4 text-xs text-gray-500">
        <p className="font-medium text-gray-400 mb-1">{t('references.title')}:</p>
        <ul className="space-y-1">
          <li>• {t('references.physiologyRef')}</li>
          <li>• {t('references.faaRef')}</li>
          <li>• Severinghaus JW. Simple, accurate equations for human blood O2 dissociation computations. J Appl Physiol. 1979;46(3):599-602.</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
