/**
 * Performance Analysis Page
 * 
 * Statistical analysis and visualization of ROBD2 session data
 */

import React, { useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import ReactECharts from 'echarts-for-react';
import { motion } from 'framer-motion';
import {
  Activity,
  BarChart3,
  TrendingUp,
  Target,
  Percent,
} from 'lucide-react';
import type { EChartsOption } from 'echarts';
import { CHART_COLORS, getBaseChartOptions } from '../charts/theme';
import type { PerformanceStats, LiveSample } from '../types';

interface PerformanceProps {
  performanceStats: PerformanceStats | null;
  samples: LiveSample[];
}

export function Performance({ performanceStats, samples }: PerformanceProps) {
  const { t } = useTranslation();

  // Distribution chart for O2 concentration
  const o2DistributionChart: EChartsOption = useMemo(() => {
    if (samples.length < 2) return {};

    const o2Values = samples.map(s => s.o2Conc);
    const bins = 20;
    const min = Math.min(...o2Values);
    const max = Math.max(...o2Values);
    const binWidth = (max - min) / bins;
    const histogram: number[] = new Array(bins).fill(0);

    for (const val of o2Values) {
      const binIndex = Math.min(Math.floor((val - min) / binWidth), bins - 1);
      histogram[binIndex]++;
    }

    return {
      ...getBaseChartOptions(),
      title: {
        text: 'O₂ Concentration Distribution',
        subtext: 'Histogram showing frequency distribution',
        left: 'center',
        textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
        subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
      },
      xAxis: {
        type: 'category',
        data: histogram.map((_, i) => (min + (i + 0.5) * binWidth).toFixed(1)),
        name: 'O₂ %',
        nameLocation: 'middle',
        nameGap: 30,
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.textMuted, rotate: 45 },
      },
      yAxis: {
        type: 'value',
        name: 'Frequency',
        nameLocation: 'middle',
        nameGap: 40,
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.textMuted },
        splitLine: { lineStyle: { color: CHART_COLORS.grid } },
      },
      series: [{
        type: 'bar',
        data: histogram,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: CHART_COLORS.o2 },
              { offset: 1, color: `${CHART_COLORS.o2}60` },
            ],
          },
          borderRadius: [4, 4, 0, 0],
        },
      }],
    };
  }, [samples]);

  // SpO2 distribution chart
  const spo2DistributionChart: EChartsOption = useMemo(() => {
    if (samples.length < 2) return {};

    const spo2Values = samples.map(s => s.spo2);
    const bins = 15;
    const min = Math.min(...spo2Values);
    const max = Math.max(...spo2Values);
    const binWidth = (max - min) / bins || 1;
    const histogram: number[] = new Array(bins).fill(0);

    for (const val of spo2Values) {
      const binIndex = Math.min(Math.floor((val - min) / binWidth), bins - 1);
      histogram[binIndex]++;
    }

    return {
      ...getBaseChartOptions(),
      title: {
        text: 'SpO₂ Distribution',
        subtext: 'Oxygen saturation frequency distribution',
        left: 'center',
        textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
        subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
      },
      xAxis: {
        type: 'category',
        data: histogram.map((_, i) => (min + (i + 0.5) * binWidth).toFixed(1)),
        name: 'SpO₂ %',
        nameLocation: 'middle',
        nameGap: 30,
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.textMuted },
      },
      yAxis: {
        type: 'value',
        name: 'Frequency',
        nameLocation: 'middle',
        nameGap: 40,
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.textMuted },
        splitLine: { lineStyle: { color: CHART_COLORS.grid } },
      },
      series: [{
        type: 'bar',
        data: histogram,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: CHART_COLORS.spo2 },
              { offset: 1, color: `${CHART_COLORS.spo2}60` },
            ],
          },
          borderRadius: [4, 4, 0, 0],
        },
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { type: 'dashed' },
          data: [
            { xAxis: '90.0', lineStyle: { color: CHART_COLORS.success }, label: { formatter: 'Normal', color: CHART_COLORS.success } },
            { xAxis: '85.0', lineStyle: { color: CHART_COLORS.danger }, label: { formatter: 'Critical', color: CHART_COLORS.danger } },
          ],
        },
      }],
    };
  }, [samples]);

  // Box plot data
  const boxPlotChart: EChartsOption = useMemo(() => {
    if (samples.length < 5) return {};

    const calculateBoxPlot = (values: number[]) => {
      const sorted = [...values].sort((a, b) => a - b);
      const n = sorted.length;
      const q1 = sorted[Math.floor(n * 0.25)];
      const median = sorted[Math.floor(n * 0.5)];
      const q3 = sorted[Math.floor(n * 0.75)];
      const min = sorted[0];
      const max = sorted[n - 1];
      return [min, q1, median, q3, max];
    };

    const o2Box = calculateBoxPlot(samples.map(s => s.o2Conc));
    const spo2Box = calculateBoxPlot(samples.map(s => s.spo2));

    return {
      title: {
        text: 'Parameter Distribution (Box Plot)',
        left: 'center',
        textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      },
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        textStyle: { color: CHART_COLORS.text },
        formatter: (params: unknown) => {
          const p = params as { name: string; data: number[] };
          return `${p.name}<br/>
            Min: ${p.data[0].toFixed(2)}<br/>
            Q1: ${p.data[1].toFixed(2)}<br/>
            Median: ${p.data[2].toFixed(2)}<br/>
            Q3: ${p.data[3].toFixed(2)}<br/>
            Max: ${p.data[4].toFixed(2)}`;
        },
      },
      xAxis: {
        type: 'category',
        data: ['O₂ %', 'SpO₂ %'],
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.text },
      },
      yAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
        axisLabel: { color: CHART_COLORS.textMuted },
        splitLine: { lineStyle: { color: CHART_COLORS.grid } },
      },
      series: [{
        type: 'boxplot',
        data: [
          { value: o2Box, name: 'O₂ %', itemStyle: { color: CHART_COLORS.o2, borderColor: CHART_COLORS.o2 } },
          { value: spo2Box, name: 'SpO₂ %', itemStyle: { color: CHART_COLORS.spo2, borderColor: CHART_COLORS.spo2 } },
        ],
        itemStyle: {
          borderWidth: 2,
        },
      }],
    };
  }, [samples]);

  // No data view
  if (!performanceStats) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="mb-6"
        >
          <Activity size={64} className="text-primary-500" />
        </motion.div>
        <h2 className="text-2xl font-bold text-white mb-2">{t('performance.needSamples')}</h2>
        <p className="text-gray-400">
          Connect to a device or enable demo mode to collect data.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <Activity className="text-primary-500" />
          {t('performance.title')}
        </h1>
        <p className="text-gray-400 -mt-4">
          Statistical analysis of session data for quality assurance
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label={t('performance.samples')}
          value={performanceStats.samples.toLocaleString()}
          icon={<BarChart3 size={20} />}
        />
        <StatCard
          label={t('performance.meanO2')}
          value={performanceStats.meanO2.toFixed(2)}
          icon={<TrendingUp size={20} />}
          suffix="%"
        />
        <StatCard
          label={t('performance.stdO2')}
          value={performanceStats.stdO2.toFixed(2)}
          icon={<Target size={20} />}
          suffix="%"
        />
        <StatCard
          label={t('performance.cvPercent')}
          value={performanceStats.cvPercent.toFixed(2)}
          icon={<Percent size={20} />}
          suffix="%"
          highlight={performanceStats.cvPercent < 5}
        />
      </div>

      {/* Range Cards */}
      {performanceStats.minO2 !== undefined && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="glass-card p-6">
            <h3 className="text-lg font-semibold text-white mb-4">O₂ Concentration Range</h3>
            <div className="flex items-center justify-between">
              <div>
                <span className="text-gray-500 text-sm">Minimum</span>
                <p className="text-2xl font-bold text-red-400">{performanceStats.minO2?.toFixed(2)}%</p>
              </div>
              <div className="h-12 w-px bg-white/10" />
              <div>
                <span className="text-gray-500 text-sm">Maximum</span>
                <p className="text-2xl font-bold text-green-400">{performanceStats.maxO2?.toFixed(2)}%</p>
              </div>
            </div>
          </div>
          <div className="glass-card p-6">
            <h3 className="text-lg font-semibold text-white mb-4">SpO₂ Range</h3>
            <div className="flex items-center justify-between">
              <div>
                <span className="text-gray-500 text-sm">Minimum</span>
                <p className="text-2xl font-bold text-red-400">{performanceStats.minSpO2?.toFixed(1)}%</p>
              </div>
              <div className="h-12 w-px bg-white/10" />
              <div>
                <span className="text-gray-500 text-sm">Maximum</span>
                <p className="text-2xl font-bold text-green-400">{performanceStats.maxSpO2?.toFixed(1)}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="chart-container h-[350px]">
          <ReactECharts
            option={o2DistributionChart}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>
        <div className="chart-container h-[350px]">
          <ReactECharts
            option={spo2DistributionChart}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>
      </div>

      {/* Box Plot */}
      {samples.length >= 5 && (
        <div className="chart-container h-[350px]">
          <ReactECharts
            option={boxPlotChart}
            style={{ height: '100%' }}
            opts={{ renderer: 'svg' }}
          />
        </div>
      )}

      {/* Quality Assessment */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Quality Assessment</h3>
        <div className="space-y-3">
          <QualityIndicator
            label="Coefficient of Variation (CV)"
            value={performanceStats.cvPercent}
            threshold={5}
            goodText="Excellent consistency (CV < 5%)"
            badText="High variability detected"
          />
          <QualityIndicator
            label="Sample Size"
            value={performanceStats.samples}
            threshold={100}
            goodText="Adequate sample size for analysis"
            badText="Consider collecting more samples"
          />
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  label: string;
  value: string;
  icon: React.ReactNode;
  suffix?: string;
  highlight?: boolean;
}

function StatCard({ label, value, icon, suffix, highlight }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`metric-card ${highlight ? 'border-green-500/50 bg-green-500/10' : ''}`}
    >
      <div className="flex items-center gap-2 text-gray-400 mb-2">
        {icon}
        <span className="text-sm">{label}</span>
      </div>
      <div className="flex items-end gap-1">
        <span className={`text-3xl font-bold ${highlight ? 'text-green-400' : 'text-white'}`}>
          {value}
        </span>
        {suffix && <span className="text-lg text-gray-400 mb-0.5">{suffix}</span>}
      </div>
    </motion.div>
  );
}

interface QualityIndicatorProps {
  label: string;
  value: number;
  threshold: number;
  goodText: string;
  badText: string;
}

function QualityIndicator({ label, value, threshold, goodText, badText }: QualityIndicatorProps) {
  const isGood = value < threshold;
  
  return (
    <div className={`p-4 rounded-xl ${isGood ? 'bg-green-500/10' : 'bg-yellow-500/10'}`}>
      <div className="flex items-center justify-between">
        <span className="text-gray-300">{label}</span>
        <span className={`font-mono ${isGood ? 'text-green-400' : 'text-yellow-400'}`}>
          {value.toFixed(2)}
        </span>
      </div>
      <p className={`text-sm mt-1 ${isGood ? 'text-green-400/70' : 'text-yellow-400/70'}`}>
        {isGood ? goodText : badText}
      </p>
    </div>
  );
}

export default Performance;
