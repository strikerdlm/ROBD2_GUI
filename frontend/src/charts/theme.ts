/**
 * ECharts Theme Configuration for ROBD2 Safety Dashboard
 * 
 * Designed for publication-quality scientific visualizations
 * Following best practices for aerospace physiology data presentation
 * 
 * Color scheme optimized for:
 * - Color blind accessibility (WCAG 2.1 AA compliant)
 * - Print reproduction
 * - Dark theme readability
 */

import type { EChartsOption } from 'echarts';

// Professional color palette for scientific publications
export const CHART_COLORS = {
  altitude: '#3B82F6',     // Blue - Primary metric
  o2: '#22C55E',           // Green - O2 concentration
  blp: '#F97316',          // Orange - Barometric lung pressure
  spo2: '#8B5CF6',         // Purple - Oxygen saturation
  pulse: '#EAB308',        // Yellow - Heart rate
  warning: '#F59E0B',      // Amber - Warning threshold
  danger: '#EF4444',       // Red - Critical threshold
  success: '#10B981',      // Emerald - Normal range
  grid: 'rgba(255, 255, 255, 0.1)',
  axis: 'rgba(255, 255, 255, 0.5)',
  text: 'rgba(255, 255, 255, 0.9)',
  textMuted: 'rgba(255, 255, 255, 0.6)',
  background: 'transparent',
};

// Theme configuration for ECharts
export const darkTheme: EChartsOption = {
  backgroundColor: 'transparent',
  textStyle: {
    color: CHART_COLORS.text,
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  title: {
    textStyle: {
      color: CHART_COLORS.text,
      fontSize: 16,
      fontWeight: 600,
    },
    subtextStyle: {
      color: CHART_COLORS.textMuted,
      fontSize: 12,
    },
  },
  legend: {
    textStyle: {
      color: CHART_COLORS.text,
    },
  },
  tooltip: {
    backgroundColor: 'rgba(15, 23, 42, 0.95)',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderWidth: 1,
    textStyle: {
      color: CHART_COLORS.text,
    },
    extraCssText: 'backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);',
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    axisLine: {
      lineStyle: {
        color: CHART_COLORS.axis,
      },
    },
    axisTick: {
      lineStyle: {
        color: CHART_COLORS.axis,
      },
    },
    axisLabel: {
      color: CHART_COLORS.textMuted,
    },
    splitLine: {
      lineStyle: {
        color: CHART_COLORS.grid,
      },
    },
  },
  yAxis: {
    axisLine: {
      lineStyle: {
        color: CHART_COLORS.axis,
      },
    },
    axisTick: {
      lineStyle: {
        color: CHART_COLORS.axis,
      },
    },
    axisLabel: {
      color: CHART_COLORS.textMuted,
    },
    splitLine: {
      lineStyle: {
        color: CHART_COLORS.grid,
      },
    },
  },
};

/**
 * Get base chart options with consistent styling
 */
export function getBaseChartOptions(title?: string, subtitle?: string): EChartsOption {
  return {
    ...darkTheme,
    title: title ? {
      text: title,
      subtext: subtitle,
      left: 'center',
      textStyle: {
        color: CHART_COLORS.text,
        fontSize: 16,
        fontWeight: 600,
      },
      subtextStyle: {
        color: CHART_COLORS.textMuted,
        fontSize: 12,
      },
    } : undefined,
    tooltip: {
      ...darkTheme.tooltip,
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: CHART_COLORS.textMuted,
        },
        lineStyle: {
          color: CHART_COLORS.textMuted,
          type: 'dashed',
        },
      },
    },
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
        },
        restore: {},
        saveAsImage: {
          backgroundColor: '#0a1628',
          pixelRatio: 2,
        },
      },
      iconStyle: {
        borderColor: CHART_COLORS.textMuted,
      },
      emphasis: {
        iconStyle: {
          borderColor: CHART_COLORS.text,
        },
      },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 100,
        height: 20,
        borderColor: CHART_COLORS.grid,
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        fillerColor: 'rgba(59, 130, 246, 0.3)',
        handleStyle: {
          color: CHART_COLORS.altitude,
        },
        textStyle: {
          color: CHART_COLORS.textMuted,
        },
      },
    ],
    animation: true,
    animationDuration: 500,
    animationEasing: 'cubicOut',
  };
}

/**
 * Create line series configuration
 */
export function createLineSeries(
  name: string,
  data: [number, number][],
  color: string,
  options?: {
    smooth?: boolean;
    areaStyle?: boolean;
    showSymbol?: boolean;
    lineWidth?: number;
  }
): EChartsOption['series'] {
  const { smooth = true, areaStyle = false, showSymbol = false, lineWidth = 2 } = options ?? {};
  
  return {
    name,
    type: 'line',
    data,
    smooth,
    showSymbol,
    symbolSize: 6,
    lineStyle: {
      color,
      width: lineWidth,
    },
    itemStyle: {
      color,
    },
    areaStyle: areaStyle ? {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: `${color}40` },
          { offset: 1, color: `${color}05` },
        ],
      },
    } : undefined,
    emphasis: {
      focus: 'series',
      lineStyle: {
        width: lineWidth + 1,
      },
    },
  };
}

/**
 * Create gauge chart options for vital signs
 */
export function createGaugeOptions(
  value: number,
  min: number,
  max: number,
  title: string,
  unit: string,
  colorStops: { value: number; color: string }[]
): EChartsOption {
  return {
    series: [{
      type: 'gauge',
      startAngle: 200,
      endAngle: -20,
      min,
      max,
      splitNumber: 5,
      itemStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: colorStops.map((stop, idx) => ({
            offset: idx / (colorStops.length - 1),
            color: stop.color,
          })),
        },
      },
      progress: {
        show: true,
        width: 18,
      },
      pointer: {
        show: false,
      },
      axisLine: {
        lineStyle: {
          width: 18,
          color: [[1, 'rgba(255, 255, 255, 0.1)']],
        },
      },
      axisTick: {
        show: false,
      },
      splitLine: {
        show: false,
      },
      axisLabel: {
        show: false,
      },
      anchor: {
        show: false,
      },
      title: {
        show: true,
        offsetCenter: [0, '70%'],
        fontSize: 14,
        color: CHART_COLORS.textMuted,
      },
      detail: {
        valueAnimation: true,
        fontSize: 32,
        fontWeight: 700,
        offsetCenter: [0, '0%'],
        color: CHART_COLORS.text,
        formatter: `{value} ${unit}`,
      },
      data: [{
        value,
        name: title,
      }],
    }],
  };
}

/**
 * Create radar chart options for physiological parameters
 */
export function createRadarOptions(
  indicators: { name: string; max: number }[],
  values: number[],
  name: string
): EChartsOption {
  return {
    radar: {
      indicator: indicators,
      shape: 'polygon',
      splitNumber: 5,
      axisName: {
        color: CHART_COLORS.textMuted,
        fontSize: 12,
      },
      splitLine: {
        lineStyle: {
          color: CHART_COLORS.grid,
        },
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.02)', 'rgba(255, 255, 255, 0.04)'],
        },
      },
      axisLine: {
        lineStyle: {
          color: CHART_COLORS.grid,
        },
      },
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name,
        lineStyle: {
          color: CHART_COLORS.altitude,
          width: 2,
        },
        areaStyle: {
          color: `${CHART_COLORS.altitude}30`,
        },
        itemStyle: {
          color: CHART_COLORS.altitude,
        },
      }],
    }],
  };
}

export default { CHART_COLORS, darkTheme, getBaseChartOptions, createLineSeries, createGaugeOptions, createRadarOptions };
