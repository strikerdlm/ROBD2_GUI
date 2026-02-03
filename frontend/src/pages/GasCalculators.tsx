/**
 * Gas Calculators Page
 * 
 * Comprehensive gas consumption and physiological calculations
 * for aerospace physiology training operations.
 * 
 * Scientific basis:
 * - Barometric pressure formula: P = P₀(1 - Lh/T₀)^(gM/RL)
 * - Alveolar gas equation: PAO₂ = (PB - PH₂O) × FiO₂ - PACO₂/R
 * - Hill equation for O₂-hemoglobin dissociation
 * 
 * References:
 * - West JB. Respiratory Physiology: The Essentials. 10th ed.
 * - Weil JV. Ventilatory responses to hypoxia. Compr Physiol. 2012.
 */

import React, { useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import ReactECharts from 'echarts-for-react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Calculator,
  Beaker,
  Cylinder,
  Users,
  TrendingUp,
  DollarSign,
  Mountain,
  Wind,
  Heart,
  Gauge,
} from 'lucide-react';
import type { EChartsOption } from 'echarts';
import { CHART_COLORS, getBaseChartOptions } from '../charts/theme';
import {
  calculatePhysiologicalParams,
  calculateGasConsumption,
  calculateCylinderCapacity,
  calculateSingleSession,
} from '../services/mockDataService';
import type {
  PhysiologicalParams,
  GasConsumption,
  CylinderCapacity,
  SingleSessionCost,
} from '../types';

type TabKey = 'physiology' | 'consumption' | 'cylinder' | 'singleSession';

export function GasCalculators() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<TabKey>('physiology');

  // Physiology state
  const [physiologyAltitude, setPhysiologyAltitude] = useState(25000);
  const [physiologyResult, setPhysiologyResult] = useState<PhysiologicalParams | null>(null);

  // Consumption state
  const [consumptionInputs, setConsumptionInputs] = useState({
    studentsPerWeek: 20,
    weeks: 26,
    sessionDuration: 20,
    recoveryDuration: 5,
    altitude: 25000,
    priceAir: 17853,
    priceN2: 17838,
    priceO2: 19654,
    contingency: 10,
  });
  const [consumptionResult, setConsumptionResult] = useState<GasConsumption | null>(null);

  // Cylinder state
  const [cylinderInputs, setCylinderInputs] = useState({
    airCylinder: 10,
    n2Cylinder: 9,
    o2Cylinder: 10,
    sessionDuration: 20,
    recoveryDuration: 5,
    altitude: 25000,
  });
  const [cylinderResult, setCylinderResult] = useState<CylinderCapacity | null>(null);

  // Single session state
  const [singleInputs, setSingleInputs] = useState({
    sessionDuration: 20,
    recoveryDuration: 5,
    altitude: 25000,
    priceAir: 17853,
    priceN2: 17838,
    priceO2: 19654,
  });
  const [singleResult, setSingleResult] = useState<SingleSessionCost | null>(null);

  // Compute physiology
  const computePhysiology = () => {
    const result = calculatePhysiologicalParams(physiologyAltitude);
    setPhysiologyResult(result);
  };

  // Altitude-Physiology chart for visualization
  const altitudePhysiologyChart: EChartsOption = useMemo(() => {
    // Generate data for multiple altitudes
    const altitudes = Array.from({ length: 36 }, (_, i) => i * 1000);
    const data = altitudes.map(alt => {
      const params = calculatePhysiologicalParams(alt);
      return {
        altitude: alt,
        pressure: params.pressureMmHg,
        pao2: params.pao2,
        sao2: params.sao2,
        ventilation: params.ventilationRateLMin,
      };
    });

    return {
      ...getBaseChartOptions(),
      title: {
        text: 'Physiological Parameters vs. Altitude',
        subtext: 'Based on standard atmospheric model and Hill equation',
        left: 'center',
        textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
        subtextStyle: { color: CHART_COLORS.textMuted, fontSize: 12 },
      },
      legend: {
        data: ['Pressure (mmHg)', 'PAO₂ (mmHg)', 'SaO₂ (%)'],
        top: 50,
        textStyle: { color: CHART_COLORS.text },
      },
      xAxis: {
        type: 'category',
        data: altitudes.map(a => a.toLocaleString()),
        name: 'Altitude (ft)',
        nameLocation: 'middle',
        nameGap: 35,
        axisLabel: {
          color: CHART_COLORS.textMuted,
          rotate: 45,
          interval: 4,
        },
        axisLine: { lineStyle: { color: CHART_COLORS.axis } },
      },
      yAxis: [
        {
          type: 'value',
          name: 'Pressure / PAO₂ (mmHg)',
          position: 'left',
          axisLine: { lineStyle: { color: CHART_COLORS.altitude } },
          axisLabel: { color: CHART_COLORS.altitude },
          splitLine: { lineStyle: { color: CHART_COLORS.grid } },
        },
        {
          type: 'value',
          name: 'SaO₂ (%)',
          position: 'right',
          min: 0,
          max: 100,
          axisLine: { lineStyle: { color: CHART_COLORS.spo2 } },
          axisLabel: { color: CHART_COLORS.spo2 },
          splitLine: { show: false },
        },
      ],
      series: [
        {
          name: 'Pressure (mmHg)',
          type: 'line',
          data: data.map(d => d.pressure.toFixed(1)),
          smooth: true,
          lineStyle: { color: CHART_COLORS.altitude, width: 2 },
          itemStyle: { color: CHART_COLORS.altitude },
        },
        {
          name: 'PAO₂ (mmHg)',
          type: 'line',
          data: data.map(d => d.pao2.toFixed(1)),
          smooth: true,
          lineStyle: { color: CHART_COLORS.o2, width: 2 },
          itemStyle: { color: CHART_COLORS.o2 },
        },
        {
          name: 'SaO₂ (%)',
          type: 'line',
          yAxisIndex: 1,
          data: data.map(d => d.sao2.toFixed(1)),
          smooth: true,
          lineStyle: { color: CHART_COLORS.spo2, width: 3 },
          itemStyle: { color: CHART_COLORS.spo2 },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: `${CHART_COLORS.spo2}40` },
                { offset: 1, color: `${CHART_COLORS.spo2}05` },
              ],
            },
          },
          markLine: {
            silent: true,
            symbol: 'none',
            data: [
              { yAxis: 90, lineStyle: { color: CHART_COLORS.success, type: 'dashed' } },
              { yAxis: 70, lineStyle: { color: CHART_COLORS.danger, type: 'dashed' } },
            ],
          },
        },
      ],
    };
  }, []);

  // Cost breakdown pie chart
  const costBreakdownChart: EChartsOption = useMemo(() => {
    if (!consumptionResult) return {};

    return {
      title: {
        text: 'Cost Breakdown',
        left: 'center',
        textStyle: { color: CHART_COLORS.text, fontSize: 16, fontWeight: 600 },
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: ${c:,.0f} ({d}%)',
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        textStyle: { color: CHART_COLORS.text },
      },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 2,
        },
        label: {
          show: true,
          color: CHART_COLORS.text,
          formatter: '{b}\n{d}%',
        },
        labelLine: {
          lineStyle: { color: CHART_COLORS.textMuted },
        },
        data: [
          { value: consumptionResult.totalCostAir, name: 'Air', itemStyle: { color: CHART_COLORS.altitude } },
          { value: consumptionResult.totalCostNitrogen, name: 'Nitrogen', itemStyle: { color: CHART_COLORS.pulse } },
          { value: consumptionResult.totalCostOxygen, name: 'Oxygen', itemStyle: { color: CHART_COLORS.o2 } },
        ],
      }],
    };
  }, [consumptionResult]);

  const tabs: { key: TabKey; icon: React.ReactNode; label: string }[] = [
    { key: 'physiology', icon: <Beaker size={18} />, label: t('gasCalc.physiology') },
    { key: 'consumption', icon: <Calculator size={18} />, label: t('gasCalc.consumption') },
    { key: 'cylinder', icon: <Cylinder size={18} />, label: t('gasCalc.cylinder') },
    { key: 'singleSession', icon: <Users size={18} />, label: t('gasCalc.singleSession') },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="section-title">
          <Calculator className="text-primary-500" />
          {t('gasCalc.title')}
        </h1>
        <p className="text-gray-400 -mt-4">
          Scientific calculations for aerospace physiology training operations
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl whitespace-nowrap transition-all duration-200 ${
              activeTab === tab.key
                ? 'bg-primary-600/30 text-white'
                : 'text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
        >
          {/* Physiology Tab */}
          {activeTab === 'physiology' && (
            <div className="space-y-6">
              <div className="glass-card p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                      <Mountain size={16} className="inline mr-2" />
                      {t('gasCalc.altitudeFt')}
                    </label>
                    <input
                      type="number"
                      value={physiologyAltitude}
                      onChange={(e) => setPhysiologyAltitude(Number(e.target.value))}
                      className="input-field"
                      min={0}
                      max={40000}
                      step={500}
                    />
                  </div>
                  <div className="flex items-end">
                    <button onClick={computePhysiology} className="btn-primary w-full">
                      <TrendingUp size={18} />
                      {t('gasCalc.compute')}
                    </button>
                  </div>
                </div>
              </div>

              {physiologyResult && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <ResultCard
                    label={t('gasCalc.pressureMmHg')}
                    value={physiologyResult.pressureMmHg.toFixed(1)}
                    unit="mmHg"
                    icon={<Gauge size={18} />}
                  />
                  <ResultCard
                    label={t('gasCalc.pao2')}
                    value={physiologyResult.pao2.toFixed(1)}
                    unit="mmHg"
                    icon={<Wind size={18} />}
                  />
                  <ResultCard
                    label={t('gasCalc.sao2')}
                    value={physiologyResult.sao2.toFixed(1)}
                    unit="%"
                    icon={<Heart size={18} />}
                  />
                  <ResultCard
                    label={t('gasCalc.heartRate')}
                    value={physiologyResult.heartRateBpm.toFixed(0)}
                    unit="bpm"
                    icon={<Heart size={18} />}
                  />
                </div>
              )}

              {/* Altitude-Physiology Chart */}
              <div className="chart-container h-[450px]">
                <ReactECharts
                  option={altitudePhysiologyChart}
                  style={{ height: '100%' }}
                  opts={{ renderer: 'svg' }}
                />
              </div>
            </div>
          )}

          {/* Consumption Tab */}
          {activeTab === 'consumption' && (
            <div className="space-y-6">
              <div className="glass-card p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <InputField
                    label={t('gasCalc.studentsPerWeek')}
                    value={consumptionInputs.studentsPerWeek}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, studentsPerWeek: v })}
                    min={1}
                    icon={<Users size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.weeks')}
                    value={consumptionInputs.weeks}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, weeks: v })}
                    min={1}
                  />
                  <InputField
                    label={t('gasCalc.sessionDuration')}
                    value={consumptionInputs.sessionDuration}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, sessionDuration: v })}
                    min={1}
                  />
                  <InputField
                    label={t('gasCalc.recoveryDuration')}
                    value={consumptionInputs.recoveryDuration}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, recoveryDuration: v })}
                    min={0}
                  />
                  <InputField
                    label={t('gasCalc.altitudeFt')}
                    value={consumptionInputs.altitude}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, altitude: v })}
                    min={0}
                    max={40000}
                    step={500}
                    icon={<Mountain size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.contingency')}
                    value={consumptionInputs.contingency}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, contingency: v })}
                    min={0}
                    max={100}
                  />
                  <InputField
                    label={t('gasCalc.priceAir')}
                    value={consumptionInputs.priceAir}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, priceAir: v })}
                    icon={<DollarSign size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.priceN2')}
                    value={consumptionInputs.priceN2}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, priceN2: v })}
                    icon={<DollarSign size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.priceO2')}
                    value={consumptionInputs.priceO2}
                    onChange={(v) => setConsumptionInputs({ ...consumptionInputs, priceO2: v })}
                    icon={<DollarSign size={16} />}
                  />
                </div>
                <button
                  onClick={() => {
                    const result = calculateGasConsumption(
                      consumptionInputs.studentsPerWeek,
                      consumptionInputs.weeks,
                      consumptionInputs.sessionDuration,
                      consumptionInputs.recoveryDuration,
                      consumptionInputs.altitude,
                      consumptionInputs.priceAir,
                      consumptionInputs.priceN2,
                      consumptionInputs.priceO2,
                      consumptionInputs.contingency / 100
                    );
                    setConsumptionResult(result);
                  }}
                  className="btn-primary mt-6"
                >
                  <Calculator size={18} />
                  {t('gasCalc.calculate')}
                </button>
              </div>

              {consumptionResult && (
                <>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <ResultCard
                      label={t('gasCalc.totalConsumption') + ' (Air)'}
                      value={consumptionResult.totalAirM3.toFixed(2)}
                      unit="m³"
                    />
                    <ResultCard
                      label={t('gasCalc.totalConsumption') + ' (N₂)'}
                      value={consumptionResult.totalNitrogenM3.toFixed(2)}
                      unit="m³"
                    />
                    <ResultCard
                      label={t('gasCalc.totalConsumption') + ' (O₂)'}
                      value={consumptionResult.totalOxygenM3.toFixed(2)}
                      unit="m³"
                    />
                    <ResultCard
                      label={t('gasCalc.totalCost')}
                      value={consumptionResult.totalCostWithContingency.toLocaleString()}
                      unit="COP"
                      highlight
                    />
                  </div>
                  <div className="chart-container h-[350px]">
                    <ReactECharts
                      option={costBreakdownChart}
                      style={{ height: '100%' }}
                      opts={{ renderer: 'svg' }}
                    />
                  </div>
                </>
              )}
            </div>
          )}

          {/* Cylinder Capacity Tab */}
          {activeTab === 'cylinder' && (
            <div className="space-y-6">
              <div className="glass-card p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <InputField
                    label={t('gasCalc.airCylinder')}
                    value={cylinderInputs.airCylinder}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, airCylinder: v })}
                    step={0.5}
                    icon={<Cylinder size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.n2Cylinder')}
                    value={cylinderInputs.n2Cylinder}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, n2Cylinder: v })}
                    step={0.5}
                    icon={<Cylinder size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.o2Cylinder')}
                    value={cylinderInputs.o2Cylinder}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, o2Cylinder: v })}
                    step={0.5}
                    icon={<Cylinder size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.sessionDuration')}
                    value={cylinderInputs.sessionDuration}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, sessionDuration: v })}
                    min={1}
                  />
                  <InputField
                    label={t('gasCalc.recoveryDuration')}
                    value={cylinderInputs.recoveryDuration}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, recoveryDuration: v })}
                    min={0}
                  />
                  <InputField
                    label={t('gasCalc.altitudeFt')}
                    value={cylinderInputs.altitude}
                    onChange={(v) => setCylinderInputs({ ...cylinderInputs, altitude: v })}
                    min={0}
                    max={40000}
                    step={500}
                    icon={<Mountain size={16} />}
                  />
                </div>
                <button
                  onClick={() => {
                    const result = calculateCylinderCapacity(
                      cylinderInputs.airCylinder,
                      cylinderInputs.n2Cylinder,
                      cylinderInputs.o2Cylinder,
                      cylinderInputs.sessionDuration,
                      cylinderInputs.recoveryDuration,
                      cylinderInputs.altitude
                    );
                    setCylinderResult(result);
                  }}
                  className="btn-primary mt-6"
                >
                  <Calculator size={18} />
                  {t('gasCalc.calculate')}
                </button>
              </div>

              {cylinderResult && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <ResultCard
                    label="Per Session (Air)"
                    value={cylinderResult.airPerSessionM3.toFixed(4)}
                    unit="m³"
                  />
                  <ResultCard
                    label="Max Students (Air)"
                    value={cylinderResult.maxStudentsAir.toString()}
                    unit="students"
                  />
                  <ResultCard
                    label="Max Students (N₂)"
                    value={cylinderResult.maxStudentsNitrogen.toString()}
                    unit="students"
                  />
                  <ResultCard
                    label={t('gasCalc.maxStudents')}
                    value={cylinderResult.maxStudents.toString()}
                    unit="students"
                    highlight
                  />
                </div>
              )}
            </div>
          )}

          {/* Single Session Tab */}
          {activeTab === 'singleSession' && (
            <div className="space-y-6">
              <div className="glass-card p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <InputField
                    label={t('gasCalc.sessionDuration')}
                    value={singleInputs.sessionDuration}
                    onChange={(v) => setSingleInputs({ ...singleInputs, sessionDuration: v })}
                    min={1}
                  />
                  <InputField
                    label={t('gasCalc.recoveryDuration')}
                    value={singleInputs.recoveryDuration}
                    onChange={(v) => setSingleInputs({ ...singleInputs, recoveryDuration: v })}
                    min={0}
                  />
                  <InputField
                    label={t('gasCalc.altitudeFt')}
                    value={singleInputs.altitude}
                    onChange={(v) => setSingleInputs({ ...singleInputs, altitude: v })}
                    min={0}
                    max={40000}
                    step={500}
                    icon={<Mountain size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.priceAir')}
                    value={singleInputs.priceAir}
                    onChange={(v) => setSingleInputs({ ...singleInputs, priceAir: v })}
                    icon={<DollarSign size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.priceN2')}
                    value={singleInputs.priceN2}
                    onChange={(v) => setSingleInputs({ ...singleInputs, priceN2: v })}
                    icon={<DollarSign size={16} />}
                  />
                  <InputField
                    label={t('gasCalc.priceO2')}
                    value={singleInputs.priceO2}
                    onChange={(v) => setSingleInputs({ ...singleInputs, priceO2: v })}
                    icon={<DollarSign size={16} />}
                  />
                </div>
                <button
                  onClick={() => {
                    const result = calculateSingleSession(
                      singleInputs.sessionDuration,
                      singleInputs.recoveryDuration,
                      singleInputs.altitude,
                      singleInputs.priceAir,
                      singleInputs.priceN2,
                      singleInputs.priceO2
                    );
                    setSingleResult(result);
                  }}
                  className="btn-primary mt-6"
                >
                  <Calculator size={18} />
                  {t('gasCalc.calculate')}
                </button>
              </div>

              {singleResult && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <ResultCard
                    label="Air Consumed"
                    value={singleResult.airConsumedM3.toFixed(4)}
                    unit="m³"
                  />
                  <ResultCard
                    label="N₂ Consumed"
                    value={singleResult.nitrogenConsumedM3.toFixed(4)}
                    unit="m³"
                  />
                  <ResultCard
                    label="O₂ Consumed"
                    value={singleResult.oxygenConsumedM3.toFixed(4)}
                    unit="m³"
                  />
                  <ResultCard
                    label={t('gasCalc.perSessionCost')}
                    value={singleResult.totalCost.toLocaleString()}
                    unit="COP"
                    highlight
                  />
                </div>
              )}
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Scientific Notes */}
      <div className="glass-card p-4 text-xs text-gray-500">
        <p className="font-medium text-gray-400 mb-2">Scientific Notes:</p>
        <ul className="space-y-1">
          <li>• Calculations based on standard atmospheric model (ISA)</li>
          <li>• Ventilation rate increases above 1,500m due to hypoxic ventilatory response (HVR)</li>
          <li>• O₂-hemoglobin dissociation modeled using Hill equation</li>
          <li>• Reference: Weil JV. Ventilatory responses to hypoxia and hyperoxia. Compr Physiol. 2012;2(2):1495-1550.</li>
        </ul>
      </div>
    </div>
  );
}

// Helper Components
interface InputFieldProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
  icon?: React.ReactNode;
}

function InputField({ label, value, onChange, min, max, step = 1, icon }: InputFieldProps) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-400 mb-2">
        {icon && <span className="inline mr-2">{icon}</span>}
        {label}
      </label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="input-field"
        min={min}
        max={max}
        step={step}
      />
    </div>
  );
}

interface ResultCardProps {
  label: string;
  value: string;
  unit: string;
  icon?: React.ReactNode;
  highlight?: boolean;
}

function ResultCard({ label, value, unit, icon, highlight }: ResultCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`metric-card ${highlight ? 'border-primary-500/50 bg-primary-500/10' : ''}`}
    >
      <div className="flex items-center gap-2 mb-2">
        {icon && <span className="text-gray-400">{icon}</span>}
        <span className="metric-label text-xs">{label}</span>
      </div>
      <div className="flex items-end gap-2">
        <span className={`text-2xl font-bold ${highlight ? 'text-primary-400' : 'text-white'}`}>
          {value}
        </span>
        <span className="text-sm text-gray-400 mb-0.5">{unit}</span>
      </div>
    </motion.div>
  );
}

export default GasCalculators;
