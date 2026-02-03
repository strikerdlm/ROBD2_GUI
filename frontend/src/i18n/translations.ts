/**
 * ROBD2 Safety Dashboard - Internationalization
 * 
 * Bilingual support for English and Spanish
 * All translations verified for aerospace/medical terminology accuracy
 */

export const translations = {
  en: {
    // App
    appTitle: 'ROBD2 Safety Dashboard',
    appSubtitle: 'Aerospace Physiology Monitoring System',
    
    // Navigation
    nav: {
      dashboard: 'Dashboard',
      connection: 'Connection',
      diagnostics: 'Diagnostics',
      calibration: 'Calibration',
      gasCalculators: 'Gas Calculators',
      programs: 'Programs',
      logging: 'Logging',
      performance: 'Performance',
    },
    
    // Connection
    connection: {
      title: 'Device Connection',
      port: 'Port',
      refresh: 'Refresh',
      connect: 'Connect',
      disconnect: 'Disconnect',
      connected: 'Connected',
      disconnected: 'Not Connected',
      polling: 'Live Polling',
      demoMode: 'Demo mode synthesizes data when no device is connected.',
      lastSample: 'Last sample: {age} • Poll interval: {interval}s • Errors: {errors}',
      noFreshData: 'No fresh device data. Polling will restart automatically.',
    },
    
    // Dashboard
    dashboard: {
      title: 'Real-Time Monitoring',
      altitude: 'Altitude',
      o2: 'O₂ Concentration',
      spo2: 'SpO₂',
      pulse: 'Pulse Rate',
      blp: 'BLP',
      chartSettings: 'Chart Settings',
      smoothingWindow: 'Smoothing Window (points)',
      maxPoints: 'Max Points Displayed',
      noSamples: 'No samples yet. Connect and wait a few seconds.',
      lowSpo2: 'Low SpO₂ Warning',
      checkMask: 'Check mask seal and O₂ source.',
      downloadCsv: 'Download CSV',
    },
    
    // Units
    units: {
      feet: 'ft',
      percent: '%',
      bpm: 'bpm',
      mmhg: 'mmHg',
      seconds: 's',
      minutes: 'min',
      m3: 'm³',
    },
    
    // Calibration
    calibration: {
      title: 'Sensor Calibration',
      info: 'Connect to a device for real readings. Demo mode uses simulated data.',
      recordRoomAir: 'Record Room Air (21%)',
      recordPureO2: 'Record 100% O₂',
      clear: 'Clear',
      roomAirCard: 'Room Air (21%)',
      pureO2Card: '100% O₂',
      adcValue: 'ADC Value',
      downloadCsv: 'Download Calibration CSV',
      captured: '{type} sample captured',
    },
    
    // Gas Calculators
    gasCalc: {
      title: 'Gas Calculators',
      physiology: 'Physiology',
      consumption: 'Consumption',
      cylinder: 'Cylinder Capacity',
      singleSession: 'Single Session',
      compute: 'Compute',
      calculate: 'Calculate',
      
      // Inputs
      altitudeFt: 'Altitude (ft)',
      studentsPerWeek: 'Students per Week',
      weeks: 'Weeks',
      sessionDuration: 'Session Duration (min)',
      recoveryDuration: 'Recovery Duration (min)',
      priceAir: 'Price Air (COP/m³)',
      priceN2: 'Price Nitrogen (COP/m³)',
      priceO2: 'Price Oxygen (COP/m³)',
      contingency: 'Contingency (%)',
      airCylinder: 'Air Cylinder (m³)',
      n2Cylinder: 'Nitrogen Cylinder (m³)',
      o2Cylinder: 'Oxygen Cylinder (m³)',
      
      // Results
      results: 'Results',
      pressureMmHg: 'Barometric Pressure',
      pao2: 'PAO₂',
      sao2: 'SAO₂',
      ventilationRate: 'Ventilation Rate',
      heartRate: 'Heart Rate',
      weeklyConsumption: 'Weekly Consumption',
      totalConsumption: 'Total Consumption',
      totalCost: 'Total Cost',
      maxStudents: 'Max Students per Cylinder Set',
      perSessionCost: 'Per Session Cost',
    },
    
    // Diagnostics
    diagnostics: {
      title: 'Device Diagnostics',
      quickCommands: 'Quick Commands',
      customCommand: 'Custom Command',
      placeholder: 'e.g., GET ADC 12',
      mfcNum: 'MFC #',
      adcNum: 'ADC #',
      send: 'Send',
      getMfcFlow: 'Get MFC Flow',
      getAdcVoltage: 'Get ADC Voltage',
      commandQueued: 'Command queued: {cmd}',
      noResponse: '(no response)',
    },
    
    // Programs
    programs: {
      title: 'Training Programs',
      programNumber: 'Program #',
      programName: 'Program Name',
      saveName: 'Save Name',
      addStep: 'Add Step',
      stepNumber: 'Step #',
      mode: 'Mode',
      holdOrRate: 'Hold (min) or Rate (ft/min)',
      sendStep: 'Send Step',
      trainingHelpers: 'Training Helpers',
      enterFsMode: 'Enter Flight Sim Mode',
      o2DumpOn: 'O₂ Dump ON',
      o2DumpOff: 'O₂ Dump OFF',
      setFsAlt: 'Set FS Altitude (ft)',
      sendAltitude: 'Send Altitude',
    },
    
    // Logging
    logging: {
      title: 'Data Logging',
      exportBuffered: 'Export Buffered Samples',
      filename: 'Filename (stored in exports/)',
      saveBuffer: 'Save Current Buffer to CSV',
      savedTo: 'Saved to {path}',
      failed: 'Failed: {error}',
      debugLog: 'Debug Log',
      addMarker: 'Add Debug Marker',
      prepareDownload: 'Prepare Debug Download',
      downloadDebug: 'Download Debug Log',
      markerAdded: 'Marker added',
      empty: '(empty)',
    },
    
    // Performance
    performance: {
      title: 'Performance Analysis',
      needSamples: 'Need at least 2 samples to compute statistics.',
      samples: 'Total Samples',
      meanO2: 'Mean O₂ (%)',
      stdO2: 'Std Dev (%)',
      cvPercent: 'CV (%)',
      minMax: 'Min/Max Range',
    },
    
    // Alerts & Status
    alerts: {
      warning: 'Warning',
      error: 'Error',
      success: 'Success',
      info: 'Information',
    },
    
    // References
    references: {
      title: 'Scientific References',
      physiologyRef: 'West JB. Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.',
      faaRef: 'FAA-H-8083-25B Pilot\'s Handbook of Aeronautical Knowledge, Chapter 17.',
      hypoxiaRef: 'Richalet JP. Altitude and the cardiovascular system. Presse Med. 2012;41(6):638-43.',
    },
  },
  
  es: {
    // App
    appTitle: 'Panel de Seguridad ROBD2',
    appSubtitle: 'Sistema de Monitoreo de Fisiología Aeroespacial',
    
    // Navigation
    nav: {
      dashboard: 'Panel',
      connection: 'Conexión',
      diagnostics: 'Diagnóstico',
      calibration: 'Calibración',
      gasCalculators: 'Calculadoras de Gas',
      programs: 'Programas',
      logging: 'Registro',
      performance: 'Desempeño',
    },
    
    // Connection
    connection: {
      title: 'Conexión del Dispositivo',
      port: 'Puerto',
      refresh: 'Actualizar',
      connect: 'Conectar',
      disconnect: 'Desconectar',
      connected: 'Conectado',
      disconnected: 'No Conectado',
      polling: 'Lectura Continua',
      demoMode: 'El modo demo genera datos cuando no hay dispositivo conectado.',
      lastSample: 'Última muestra: {age} • Intervalo: {interval}s • Errores: {errors}',
      noFreshData: 'Sin datos recientes. El sondeo se reiniciará automáticamente.',
    },
    
    // Dashboard
    dashboard: {
      title: 'Monitoreo en Tiempo Real',
      altitude: 'Altitud',
      o2: 'Concentración de O₂',
      spo2: 'SpO₂',
      pulse: 'Frecuencia Cardíaca',
      blp: 'BLP',
      chartSettings: 'Configuración de Gráficos',
      smoothingWindow: 'Ventana de Suavizado (puntos)',
      maxPoints: 'Máximo de Puntos',
      noSamples: 'Sin muestras aún. Conecta y espera unos segundos.',
      lowSpo2: 'Alerta de SpO₂ Baja',
      checkMask: 'Revisa el sello de la máscara y la fuente de O₂.',
      downloadCsv: 'Descargar CSV',
    },
    
    // Units
    units: {
      feet: 'ft',
      percent: '%',
      bpm: 'lpm',
      mmhg: 'mmHg',
      seconds: 's',
      minutes: 'min',
      m3: 'm³',
    },
    
    // Calibration
    calibration: {
      title: 'Calibración del Sensor',
      info: 'Conecta un dispositivo para lecturas reales. El modo demo usa datos simulados.',
      recordRoomAir: 'Registrar Aire Ambiente (21%)',
      recordPureO2: 'Registrar O₂ al 100%',
      clear: 'Borrar',
      roomAirCard: 'Aire Ambiente (21%)',
      pureO2Card: 'O₂ al 100%',
      adcValue: 'Valor ADC',
      downloadCsv: 'Descargar CSV de Calibración',
      captured: 'Muestra de {type} capturada',
    },
    
    // Gas Calculators
    gasCalc: {
      title: 'Calculadoras de Gas',
      physiology: 'Fisiología',
      consumption: 'Consumo',
      cylinder: 'Capacidad de Cilindro',
      singleSession: 'Sesión Individual',
      compute: 'Calcular',
      calculate: 'Calcular',
      
      // Inputs
      altitudeFt: 'Altitud (ft)',
      studentsPerWeek: 'Estudiantes por Semana',
      weeks: 'Semanas',
      sessionDuration: 'Duración de Sesión (min)',
      recoveryDuration: 'Duración de Recuperación (min)',
      priceAir: 'Precio Aire (COP/m³)',
      priceN2: 'Precio Nitrógeno (COP/m³)',
      priceO2: 'Precio Oxígeno (COP/m³)',
      contingency: 'Contingencia (%)',
      airCylinder: 'Cilindro de Aire (m³)',
      n2Cylinder: 'Cilindro de Nitrógeno (m³)',
      o2Cylinder: 'Cilindro de Oxígeno (m³)',
      
      // Results
      results: 'Resultados',
      pressureMmHg: 'Presión Barométrica',
      pao2: 'PAO₂',
      sao2: 'SAO₂',
      ventilationRate: 'Frecuencia Ventilatoria',
      heartRate: 'Frecuencia Cardíaca',
      weeklyConsumption: 'Consumo Semanal',
      totalConsumption: 'Consumo Total',
      totalCost: 'Costo Total',
      maxStudents: 'Máximo de Estudiantes por Juego de Cilindros',
      perSessionCost: 'Costo por Sesión',
    },
    
    // Diagnostics
    diagnostics: {
      title: 'Diagnóstico del Dispositivo',
      quickCommands: 'Comandos Rápidos',
      customCommand: 'Comando Personalizado',
      placeholder: 'ej.: GET ADC 12',
      mfcNum: 'MFC #',
      adcNum: 'ADC #',
      send: 'Enviar',
      getMfcFlow: 'Obtener Caudal MFC',
      getAdcVoltage: 'Obtener Voltaje ADC',
      commandQueued: 'Comando en cola: {cmd}',
      noResponse: '(sin respuesta)',
    },
    
    // Programs
    programs: {
      title: 'Programas de Entrenamiento',
      programNumber: 'Programa #',
      programName: 'Nombre del Programa',
      saveName: 'Guardar Nombre',
      addStep: 'Agregar Paso',
      stepNumber: 'Paso #',
      mode: 'Modo',
      holdOrRate: 'Mantener (min) o Tasa (ft/min)',
      sendStep: 'Enviar Paso',
      trainingHelpers: 'Ayudas de Entrenamiento',
      enterFsMode: 'Entrar en Modo Simulador',
      o2DumpOn: 'O₂ Dump ON',
      o2DumpOff: 'O₂ Dump OFF',
      setFsAlt: 'Fijar Altitud FS (ft)',
      sendAltitude: 'Enviar Altitud',
    },
    
    // Logging
    logging: {
      title: 'Registro de Datos',
      exportBuffered: 'Exportar Muestras en Búfer',
      filename: 'Nombre de archivo (guardado en exports/)',
      saveBuffer: 'Guardar Búfer Actual en CSV',
      savedTo: 'Guardado en {path}',
      failed: 'Error: {error}',
      debugLog: 'Registro de Depuración',
      addMarker: 'Añadir Marcador',
      prepareDownload: 'Preparar Descarga',
      downloadDebug: 'Descargar Log de Depuración',
      markerAdded: 'Marcador añadido',
      empty: '(vacío)',
    },
    
    // Performance
    performance: {
      title: 'Análisis de Desempeño',
      needSamples: 'Se necesitan al menos 2 muestras para calcular estadísticas.',
      samples: 'Total de Muestras',
      meanO2: 'Promedio O₂ (%)',
      stdO2: 'Desviación Estándar (%)',
      cvPercent: 'CV (%)',
      minMax: 'Rango Mín/Máx',
    },
    
    // Alerts & Status
    alerts: {
      warning: 'Advertencia',
      error: 'Error',
      success: 'Éxito',
      info: 'Información',
    },
    
    // References
    references: {
      title: 'Referencias Científicas',
      physiologyRef: 'West JB. Respiratory Physiology: The Essentials. 10th ed. Wolters Kluwer; 2021.',
      faaRef: 'FAA-H-8083-25B Pilot\'s Handbook of Aeronautical Knowledge, Capítulo 17.',
      hypoxiaRef: 'Richalet JP. Altitude and the cardiovascular system. Presse Med. 2012;41(6):638-43.',
    },
  },
};

export type TranslationKey = keyof typeof translations.en;
export default translations;
