from __future__ import annotations

import io
import statistics
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Literal

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from data_store import DataStore
from gas_calculators import (
    cylinder_capacity,
    gas_consumption,
    physiological_params,
    single_session,
)
from serial_service import LiveSample, SerialService
POLL_INTERVAL_SECONDS = 2.0

DEFAULT_LANG: Literal["en", "es"] = "es"
LANGUAGES: Dict[str, str] = {"es": "Español", "en": "English"}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Generic
    "app_subtitle": {"en": "Minimal web interface", "es": "Interfaz web minimalista"},
    "sidebar_interface": {"en": "Streamlit interface", "es": "Interfaz de Streamlit"},
    "nav": {"en": "Navigation", "es": "Navegación"},
    "download_csv": {"en": "Download CSV", "es": "Descargar CSV"},
    "polling": {"en": "Polling", "es": "Lectura continua"},
    # Connection
    "device_connection": {"en": "Device Connection", "es": "Conexión del dispositivo"},
    "port": {"en": "Port", "es": "Puerto"},
    "refresh": {"en": "Refresh", "es": "Actualizar"},
    "connect": {"en": "Connect", "es": "Conectar"},
    "disconnect": {"en": "Disconnect", "es": "Desconectar"},
    "status_connected": {"en": "Connected", "es": "Conectado"},
    "status_disconnected": {"en": "Not connected", "es": "No conectado"},
    "demo_caption": {
        "en": "Demo mode synthesizes data if no device is connected.",
        "es": "El modo demo genera datos si no hay un dispositivo conectado.",
    },
    "last_sample": {
        "en": "Last sample: {age} • Poll interval {interval:.1f}s • Errors (since last sample): {errors}",
        "es": "Última muestra: {age} • Intervalo de sondeo {interval:.1f}s • Errores (desde la última muestra): {errors}",
    },
    "no_fresh_data": {
        "en": "No fresh device data in a while. Polling will restart automatically when enabled.",
        "es": "No hay datos recientes del dispositivo. El sondeo se reiniciará automáticamente cuando esté activado.",
    },
    # Diagnostics
    "diagnostics": {"en": "Diagnostics", "es": "Diagnóstico"},
    "quick_commands": {"en": "Quick commands", "es": "Comandos rápidos"},
    "custom_command": {"en": "Custom command", "es": "Comando personalizado"},
    "custom_command_ph": {"en": "e.g., GET ADC 12", "es": "ej.: GET ADC 12"},
    "mfc_num": {"en": "MFC #", "es": "MFC #"},
    "adc_num": {"en": "ADC #", "es": "ADC #"},
    "send": {"en": "Send", "es": "Enviar"},
    "get_mfc_flow": {"en": "Get MFC flow", "es": "Obtener caudal MFC"},
    "get_adc_voltage": {"en": "Get ADC voltage", "es": "Obtener voltaje ADC"},
    "command_queued": {"en": "Command queued: {msg}", "es": "Comando en cola: {msg}"},
    "no_response": {"en": "(no response)", "es": "(sin respuesta)"},
    # Dashboard
    "dashboard": {"en": "Dashboard", "es": "Tablero"},
    "chart_settings": {"en": "Chart settings", "es": "Configuración de gráficos"},
    "smoothing_window": {
        "en": "Smoothing window (points)",
        "es": "Ventana de suavizado (puntos)",
    },
    "smoothing_help": {
        "en": "Visual-only moving average",
        "es": "Promedio móvil solo visual",
    },
    "max_points": {"en": "Max points plotted", "es": "Máximo de puntos a graficar"},
    "no_samples": {
        "en": "No samples yet. Connect and wait a few seconds.",
        "es": "Aún no hay muestras. Conecta y espera unos segundos.",
    },
    "metric_altitude": {"en": "Altitude", "es": "Altitud"},
    "metric_o2": {"en": "O₂", "es": "O₂"},
    "metric_spo2": {"en": "SpO₂", "es": "SpO₂"},
    "metric_pulse": {"en": "Pulse", "es": "Pulso"},
    "low_spo2": {"en": "Low SpO₂", "es": "SpO₂ baja"},
    "check_mask": {
        "en": "Check mask seal / O₂ source.",
        "es": "Revisa el sello de la máscara / fuente de O₂.",
    },
    "plot_altitude": {"en": "Altitude", "es": "Altitud"},
    "plot_o2_blp": {"en": "O₂ & BLP", "es": "O₂ y BLP"},
    "plot_spo2_pulse": {"en": "SpO₂ & Pulse", "es": "SpO₂ y Pulso"},
    "axis_time": {"en": "Time (s)", "es": "Tiempo (s)"},
    "axis_percent_mmhg": {"en": "% / mmHg", "es": "% / mmHg"},
    "axis_percent_bpm": {"en": "% / bpm", "es": "% / bpm"},
    "axis_feet": {"en": "ft", "es": "ft"},
    # Calibration
    "calibration": {"en": "Calibration", "es": "Calibración"},
    "calibration_info": {
        "en": "Connect to a device for real readings; demo uses latest buffered sample.",
        "es": "Conecta un dispositivo para lecturas reales; el modo demo usa la última muestra en búfer.",
    },
    "record_room_air": {"en": "Record Room Air (21%)", "es": "Registrar aire ambiente (21%)"},
    "record_pure_o2": {"en": "Record 100% O₂", "es": "Registrar O₂ al 100%"},
    "clear": {"en": "Clear", "es": "Borrar"},
    "room_air_captured": {
        "en": "Room air sample captured",
        "es": "Muestra de aire ambiente guardada",
    },
    "pure_o2_captured": {
        "en": "100% O₂ sample captured",
        "es": "Muestra de O₂ al 100% guardada",
    },
    "room_air_card": {"en": "Room Air (21%)", "es": "Aire ambiente (21%)"},
    "pure_o2_card": {"en": "100% O₂", "es": "O₂ al 100%"},
    "download_calibration_csv": {
        "en": "Download calibration CSV",
        "es": "Descargar CSV de calibración",
    },
    # Gas calculators
    "gas_calculators": {"en": "Gas Calculators", "es": "Calculadoras de gas"},
    "tab_physiology": {"en": "Physiology", "es": "Fisiología"},
    "tab_consumption": {"en": "Consumption", "es": "Consumo"},
    "tab_cylinder": {"en": "Cylinder Capacity", "es": "Capacidad de cilindro"},
    "tab_single": {"en": "Single Session", "es": "Sesión individual"},
    "altitude_ft": {"en": "Altitude (ft)", "es": "Altitud (ft)"},
    "compute_physiology": {"en": "Compute physiology", "es": "Calcular fisiología"},
    "students_per_week": {"en": "Students per week", "es": "Estudiantes por semana"},
    "weeks": {"en": "Weeks", "es": "Semanas"},
    "session_duration": {"en": "Session duration (min)", "es": "Duración de sesión (min)"},
    "recovery_duration": {"en": "Recovery (min)", "es": "Recuperación (min)"},
    "price_air": {"en": "Price Air (COP/m³)", "es": "Precio Aire (COP/m³)"},
    "price_n2": {"en": "Price Nitrogen (COP/m³)", "es": "Precio N₂ (COP/m³)"},
    "price_o2": {"en": "Price Oxygen (COP/m³)", "es": "Precio O₂ (COP/m³)"},
    "contingency": {"en": "Contingency (%)", "es": "Contingencia (%)"},
    "calculate_consumption": {"en": "Calculate consumption", "es": "Calcular consumo"},
    "air_cylinder": {"en": "Air cylinder (m³)", "es": "Cilindro de aire (m³)"},
    "n2_cylinder": {"en": "Nitrogen cylinder (m³)", "es": "Cilindro de N₂ (m³)"},
    "o2_cylinder": {"en": "Oxygen cylinder (m³)", "es": "Cilindro de O₂ (m³)"},
    "calculate_capacity": {"en": "Calculate capacity", "es": "Calcular capacidad"},
    "calculate_single": {"en": "Calculate single session", "es": "Calcular sesión individual"},
    # Programs
    "programs": {"en": "Programs", "es": "Programas"},
    "program_number": {"en": "Program #", "es": "Programa #"},
    "program_name": {"en": "Program name", "es": "Nombre del programa"},
    "save_name": {"en": "Save name", "es": "Guardar nombre"},
    "add_step": {"en": "Add step", "es": "Agregar paso"},
    "step_number": {"en": "Step #", "es": "Paso #"},
    "mode": {"en": "Mode", "es": "Modo"},
    "hold_or_rate": {"en": "Hold (min) or Rate (ft/min)", "es": "Mantener (min) o Tasa (ft/min)"},
    "send_step": {"en": "Send step", "es": "Enviar paso"},
    "training_helpers": {"en": "Training helpers", "es": "Ayudas de entrenamiento"},
    "enter_fs_mode": {"en": "Enter Flight Sim Mode", "es": "Entrar en modo simulador de vuelo"},
    "o2_dump_on": {"en": "O2 Dump ON", "es": "O₂ Dump ON"},
    "o2_dump_off": {"en": "O2 Dump OFF", "es": "O₂ Dump OFF"},
    "set_fs_alt": {"en": "Set FS Altitude (ft)", "es": "Fijar altitud de simulador (ft)"},
    "send_altitude": {"en": "Send Altitude", "es": "Enviar altitud"},
    # Logging
    "logging": {"en": "Logging", "es": "Registro"},
    "export_buffered": {"en": "Export buffered samples", "es": "Exportar muestras en búfer"},
    "filename": {"en": "Filename (stored under exports/)", "es": "Nombre de archivo (guardado en exports/)"},
    "save_buffer_csv": {"en": "Save current buffer to CSV", "es": "Guardar búfer actual en CSV"},
    "saved_to": {"en": "Saved to {path}", "es": "Guardado en {path}"},
    "failed": {"en": "Failed: {error}", "es": "Error: {error}"},
    "debug_log": {"en": "Debug log", "es": "Registro de depuración"},
    "add_debug_marker": {"en": "Add debug marker", "es": "Añadir marcador de depuración"},
    "prepare_debug_download": {"en": "Prepare debug log download", "es": "Preparar descarga de log de depuración"},
    "download_debug": {"en": "Download debug log", "es": "Descargar log de depuración"},
    "marker_added": {"en": "Marker added", "es": "Marcador añadido"},
    "empty_log": {"en": "(empty)", "es": "(vacío)"},
    "marker_label": {"en": "marker", "es": "marcador"},
    # Performance
    "performance": {"en": "Performance Snapshot", "es": "Instantánea de desempeño"},
    "need_samples": {"en": "Need at least 2 samples to compute stats.", "es": "Se necesitan al menos 2 muestras para calcular estadísticas."},
    "samples": {"en": "Samples", "es": "Muestras"},
    "mean_o2": {"en": "Mean O2 (%)", "es": "Promedio O₂ (%)"},
    "std_o2": {"en": "Std Dev (%)", "es": "Desviación estándar (%)"},
    "cv_percent": {"en": "CV (%)", "es": "CV (%)"},
    # Navigation items
    "nav_connection": {"en": "Connection", "es": "Conexión"},
    "nav_dashboard": {"en": "Dashboard", "es": "Tablero"},
    "nav_diagnostics": {"en": "Diagnostics", "es": "Diagnóstico"},
    "nav_calibration": {"en": "Calibration", "es": "Calibración"},
    "nav_gas_calculators": {"en": "Gas Calculators", "es": "Calculadoras de gas"},
    "nav_programs": {"en": "Programs", "es": "Programas"},
    "nav_logging": {"en": "Logging", "es": "Registro"},
    "nav_performance": {"en": "Performance", "es": "Desempeño"},
    # CSV headers
    "csv_time_s": {"en": "Time (s)", "es": "Tiempo (s)"},
    "csv_time_min": {"en": "Time (min)", "es": "Tiempo (min)"},
    "csv_alt_ft": {"en": "Altitude (ft)", "es": "Altitud (ft)"},
    "csv_o2_conc": {"en": "O2 Concentration (%)", "es": "Concentración de O₂ (%)"},
    "csv_blp": {"en": "BLP (mmHg)", "es": "BLP (mmHg)"},
    "csv_spo2": {"en": "SpO2 (%)", "es": "SpO₂ (%)"},
    "csv_pulse": {"en": "Pulse (bpm)", "es": "Pulso (lpm)"},
    "csv_o2_voltage": {"en": "O2 Voltage (V)", "es": "Voltaje O₂ (V)"},
    "csv_error": {"en": "Error (%)", "es": "Error (%)"},
}


def _current_lang() -> Literal["en", "es"]:
    """Return the current UI language code stored in session state."""
    lang = st.session_state.get("lang", DEFAULT_LANG)
    if lang not in LANGUAGES:
        st.session_state.lang = DEFAULT_LANG
        return DEFAULT_LANG
    return lang


def t(key: str, **kwargs: object) -> str:
    """Translate a key using the active language with fallback to the default."""
    lang = _current_lang()
    template = TRANSLATIONS.get(key, {}).get(lang) or TRANSLATIONS.get(key, {}).get(DEFAULT_LANG)
    if not template:
        return key
    return template.format(**kwargs) if kwargs else template


def _language_selector() -> Literal["en", "es"]:
    """Render language selector in the sidebar and return current language."""
    current = _current_lang()
    codes = list(LANGUAGES.keys())
    choice = st.sidebar.selectbox(
        "Idioma / Language",
        options=codes,
        format_func=lambda code: LANGUAGES[code],
        index=codes.index(current),
    )
    if choice != current:
        st.session_state.lang = choice
        st.rerun()
    return choice


# --------------------------------------------------------------------------- #
# Session helpers
# --------------------------------------------------------------------------- #


def _bootstrap_service() -> SerialService:
    if "serial_service" not in st.session_state:
        st.session_state.serial_service = SerialService(
            poll_interval=POLL_INTERVAL_SECONDS, use_demo_if_disconnected=True
        )
    return st.session_state.serial_service


def _init_calibration_state() -> None:
    st.session_state.setdefault(
        "calibration",
        {
            "room_air_o2": None,
            "room_air_adc": None,
            "pure_o2_o2": None,
            "pure_o2_adc": None,
        },
    )


def _init_debug_log() -> None:
    st.session_state.setdefault("debug_log", [])


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #


def _export_csv(data_store: DataStore) -> Tuple[str, bytes]:
    time_sec, altitude = data_store.get_data("altitude")
    _, o2 = data_store.get_data("o2_conc")
    _, blp = data_store.get_data("blp")
    _, spo2 = data_store.get_data("spo2")
    _, pulse = data_store.get_data("pulse")
    _, o2_v = data_store.get_data("o2_voltage")
    _, err = data_store.get_data("error_percent")

    buffer = io.StringIO()
    headers = [
        t("csv_time_s"),
        t("csv_time_min"),
        t("csv_alt_ft"),
        t("csv_o2_conc"),
        t("csv_blp"),
        t("csv_spo2"),
        t("csv_pulse"),
        t("csv_o2_voltage"),
        t("csv_error"),
    ]
    buffer.write(",".join(headers) + "\n")
    for i, t in enumerate(time_sec):
        buffer.write(
            f"{t:.2f},{t/60:.2f},{altitude[i]:.1f},{o2[i]:.2f},"
            f"{blp[i]:.2f},{spo2[i]:.2f},{pulse[i]:.2f},{o2_v[i]:.3f},{err[i]:.2f}\n"
        )
    return "robd2_data.csv", buffer.getvalue().encode("utf-8")


def _latest_sample(service: SerialService) -> LiveSample | None:
    times, alt = service.data_store.get_data("altitude")
    if not times:
        return None
    _, o2 = service.data_store.get_data("o2_conc")
    _, blp = service.data_store.get_data("blp")
    _, spo2 = service.data_store.get_data("spo2")
    _, pulse = service.data_store.get_data("pulse")
    idx = -1
    now = datetime.now()
    return LiveSample(
        timestamp=now,
        altitude=alt[idx],
        o2_conc=o2[idx],
        blp=blp[idx],
        spo2=spo2[idx],
        pulse=pulse[idx],
    )


def _performance_summary(service: SerialService) -> Dict[str, float]:
    _, o2 = service.data_store.get_data("o2_conc")
    if len(o2) < 2:
        return {}
    mean = statistics.mean(o2)
    stdev = statistics.stdev(o2)
    return {
        "mean_o2": mean,
        "std_o2": stdev,
        "cv_percent": (stdev / mean * 100) if mean else 0.0,
        "samples": len(o2),
    }


def _format_age(seconds: float | None) -> str:
    if seconds is None:
        return "—"
    if seconds >= 120:
        return f"{seconds/60:.1f} min"
    return f"{seconds:.1f} s"


# --------------------------------------------------------------------------- #
# Styling
# --------------------------------------------------------------------------- #


THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --secondary: #475569;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-color: #0f172a;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --accent: #2563eb;
  --accent2: #0ea5e9;
  --danger: #ef4444;
  --success: #22c55e;
  --warning: #f59e0b;
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --radius: 0.75rem;
}

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text-color);
  background-color: var(--bg-color);
}

.stApp {
  background-color: var(--bg-color);
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background-color: var(--card-bg);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

/* Inputs & Selects */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] {
  background-color: var(--card-bg) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 0.5rem !important;
  color: var(--text-color) !important;
}

/* Buttons */
div[data-testid="stButton"] button {
  border-radius: 0.5rem;
  font-weight: 500;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-color);
  transition: all 0.2s;
  box-shadow: var(--shadow-sm);
}
div[data-testid="stButton"] button:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
}
button[kind="primary"] {
  background-color: var(--primary) !important;
  border: none !important;
  color: white !important;
}
button[kind="primary"]:hover {
  background-color: var(--primary-hover) !important;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

/* Metric Cards */
.metric-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}
.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: var(--primary);
}
.metric-card h3 {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin: 0 0 0.5rem 0;
}
.metric-value {
  font-size: 2.25rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.1;
  color: var(--text-color);
}
.subtext {
  font-size: 0.875rem;
  color: var(--text-muted);
}

/* Alerts */
.alert {
  padding: 1rem;
  border-radius: var(--radius);
  border: 1px solid transparent;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.alert-danger {
  background-color: #fef2f2;
  border-color: #fecaca;
  color: #991b1b;
}

/* Titles */
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 1.5rem;
  letter-spacing: -0.025em;
}
.app-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
  background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
  height: 40px;
  border-radius: 8px;
  background-color: transparent;
  border: 1px solid transparent;
  color: var(--text-muted);
  font-weight: 500;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
  background-color: var(--card-bg);
  border-color: var(--border-color);
  color: var(--primary);
  box-shadow: var(--shadow-sm);
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  background-color: var(--success);
  color: white;
}
.badge.red {
  background-color: var(--danger);
}

/* Hide Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""


def metric_card(title: str, value: str, color: str | None = None) -> None:
    style = f'style="color:{color}"' if color else ""
    st.markdown(
        f"""
        <div class="metric-card">
          <h3>{title}</h3>
          <div class="metric-value" {style}>{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def calibration_card(title: str, o2_pct: float | None, adc: float | None) -> None:
    o2_text = f"{o2_pct:.2f} %" if o2_pct is not None else "—"
    adc_text = f"{adc:.3f}" if adc is not None else "—"

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>{title}</h3>
          <div class="metric-value" style="color:var(--primary)">{o2_text}</div>
          <div class="subtext" style="margin-top:auto; padding-top:0.5rem; border-top:1px solid var(--border-color)">
            ADC Value: <strong>{adc_text}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# UI sections
# --------------------------------------------------------------------------- #


def connection_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("device_connection")}</div>',
        unsafe_allow_html=True,
    )

    ports = service.list_ports()

    row1 = st.columns([3, 1])
    with row1[0]:
        selected = st.selectbox(
            t("port"),
            ports,
            index=0 if ports else None,
            key="port_select",
            label_visibility="collapsed",
        )
    with row1[1]:
        if st.button(t("refresh"), use_container_width=True):
            st.rerun()

    row2 = st.columns([1.2, 1.2, 1.2])
    with row2[0]:
        if st.button(
            t("connect"),
            disabled=service.connected or not ports,
            type="primary",
            use_container_width=True,
        ):
            if selected:
                ok, msg = service.connect(selected)
                st.toast(msg)
                if ok:
                    service.start_polling()
    with row2[1]:
        if st.button(
            t("disconnect"),
            disabled=not service.connected,
            use_container_width=True,
        ):
            ok, msg = service.disconnect()
            st.toast(msg)
    with row2[2]:
        live = st.toggle(
            t("polling"),
            value=service.connected,
            disabled=not service.connected,
            key="poll_toggle",
        )
        if not live:
            service.stop_polling()
        elif service.connected:
            service.start_polling()

    status = t("status_connected") if service.connected else t("status_disconnected")
    badge_class = "badge" if service.connected else "badge red"
    st.markdown(f'<span class="{badge_class}">{status}</span>', unsafe_allow_html=True)
    st.caption(t("demo_caption"))

    health = service.health()
    age_text = _format_age(health["sample_age_sec"])
    err_count = health["consecutive_errors"]
    st.caption(
        t(
            "last_sample",
            age=age_text,
            interval=health["poll_interval"] or 0.0,
            errors=err_count,
        )
    )
    if (
        health["sample_age_sec"] is not None
        and health["poll_interval"] is not None
        and health["sample_age_sec"] > health["poll_interval"] * 2.5
    ):
        st.warning(t("no_fresh_data"))


def diagnostics_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("diagnostics")}</div>',
        unsafe_allow_html=True,
    )
    preset = st.selectbox(
        t("quick_commands"),
        [
            "GET RUN ALL",
            "GET RUN O2CONC",
            "GET RUN BLPRESS",
            "GET RUN SPO2",
            "GET RUN PULSE",
            "GET RUN ALT",
            "GET RUN FINALALT",
            "GET RUN ELTIME",
            "GET RUN REMTIME",
            "GET INFO",
            "GET STATUS",
        ],
    )
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        manual = st.text_input(t("custom_command"), placeholder=t("custom_command_ph"))
    with col2:
        mfc_num = st.number_input(
            t("mfc_num"), min_value=0, max_value=9, value=1, step=1
        )
    with col3:
        adc_num = st.number_input(
            t("adc_num"), min_value=1, max_value=16, value=12, step=1
        )

    cmd_choice = manual.strip() or preset
    cols = st.columns(3)
    send_clicked = cols[0].button(t("send"), type="primary")
    if cols[1].button(t("get_mfc_flow")):
        cmd_choice = f"GET MFC {int(mfc_num)}"
        send_clicked = True
    if cols[2].button(t("get_adc_voltage")):
        cmd_choice = f"GET ADC {int(adc_num)}"
        send_clicked = True

    if send_clicked:
        ok, msg = service.send_command(cmd_choice)
        st.write(t("command_queued", msg=msg))
        if ok:
            resp = service.get_response()
            st.code(resp or t("no_response"), language="text")


def dashboard_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("dashboard")}</div>',
        unsafe_allow_html=True,
    )

    with st.expander(t("chart_settings"), expanded=False):
        smoothing = st.slider(
            t("smoothing_window"),
            1,
            20,
            3,
            1,
            help=t("smoothing_help"),
        )
        max_pts = st.slider(t("max_points"), 100, 2000, 800, 100)

    ds = service.data_store
    time_sec, altitude = ds.get_data("altitude")
    _, o2 = ds.get_data("o2_conc")
    _, blp = ds.get_data("blp")
    _, spo2 = ds.get_data("spo2")
    _, pulse = ds.get_data("pulse")

    if not time_sec:
        st.warning(t("no_samples"))
        return

    latest = _latest_sample(service)
    card_cols = st.columns(4)
    if latest:
        with card_cols[0]:
            metric_card(t("metric_altitude"), f"{latest.altitude:,.0f} ft")
        with card_cols[1]:
            metric_card(t("metric_o2"), f"{latest.o2_conc:.2f} %")
        with card_cols[2]:
            metric_card(t("metric_spo2"), f"{latest.spo2:.1f} %", color="var(--accent2)")
        with card_cols[3]:
            metric_card(t("metric_pulse"), f"{latest.pulse:.0f} bpm", color="#f59e0b")

    if latest and latest.spo2 < 88:
        st.markdown(
            f"""
            <div class="alert alert-danger">
              <strong>{t("low_spo2")}</strong> — {latest.spo2:.1f}%.
              <span class="subtext">{t("check_mask")}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _smooth(arr):
        if smoothing <= 1 or len(arr) == 0:
            return arr
        out = []
        for i in range(len(arr)):
            window = arr[max(0, i - smoothing + 1) : i + 1]
            out.append(sum(window) / len(window))
        return out

    def _tail(arr):
        return arr[-max_pts:] if len(arr) > max_pts else arr

    times = _tail(time_sec)
    altitude_p = _smooth(_tail(altitude))
    o2_p = _smooth(_tail(o2))
    blp_p = _smooth(_tail(blp))
    spo2_p = _smooth(_tail(spo2))
    pulse_p = _smooth(_tail(pulse))

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(t("plot_altitude"), t("plot_o2_blp"), t("plot_spo2_pulse")),
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=altitude_p,
            mode="lines",
            line=dict(color="#2563eb", width=2),
            name=t("metric_altitude"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=o2_p,
            mode="lines",
            line=dict(color="#16a34a", width=2),
            name=t("metric_o2"),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=blp_p,
            mode="lines",
            line=dict(color="#f97316", width=2),
            name="BLP",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=spo2_p,
            mode="lines",
            line=dict(color="#7c3aed", width=2),
            name=t("metric_spo2"),
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=pulse_p,
            mode="lines",
            line=dict(color="#eab308", width=2),
            name=t("metric_pulse"),
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        height=820,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_orientation="h",
        legend_y=1.04,
        margin=dict(t=40, b=40, l=60, r=20),
        font=dict(color="#0f172a"),
    )
    fig.update_yaxes(title_text=t("axis_feet"), row=1, col=1)
    fig.update_yaxes(title_text=t("axis_percent_mmhg"), row=2, col=1)
    fig.update_yaxes(title_text=t("axis_percent_bpm"), row=3, col=1)
    fig.update_xaxes(title_text=t("axis_time"), row=3, col=1)

    st.plotly_chart(fig, use_container_width=True, theme=None)

    fname, data = _export_csv(ds)
    st.download_button(
        t("download_csv"),
        data=data,
        file_name=fname,
        mime="text/csv",
        type="primary",
    )


def calibration_section(service: SerialService) -> None:
    _init_calibration_state()
    st.markdown(
        f'<div class="section-title">{t("calibration")}</div>',
        unsafe_allow_html=True,
    )
    if not service.connected:
        st.info(t("calibration_info"))

    cal = st.session_state.calibration
    has_any = any(v is not None for v in cal.values())

    actions = st.columns([1.3, 1.3, 1.0])
    with actions[0]:
        if st.button(t("record_room_air"), type="primary", use_container_width=True):
            sample = _latest_sample(service)
            if sample:
                st.session_state.calibration["room_air_o2"] = sample.o2_conc
                st.session_state.calibration["room_air_adc"] = sample.o2_conc / 10.0
                st.toast(t("room_air_captured"))
    with actions[1]:
        if st.button(t("record_pure_o2"), type="primary", use_container_width=True):
            sample = _latest_sample(service)
            if sample:
                st.session_state.calibration["pure_o2_o2"] = max(sample.o2_conc, 95.0)
                st.session_state.calibration["pure_o2_adc"] = (sample.o2_conc / 10.0) + 1.0
                st.toast(t("pure_o2_captured"))
    with actions[2]:
        if st.button(t("clear"), disabled=not has_any, use_container_width=True):
            st.session_state.calibration = {
                "room_air_o2": None,
                "room_air_adc": None,
                "pure_o2_o2": None,
                "pure_o2_adc": None,
            }
            st.rerun()

    cards = st.columns(2)
    with cards[0]:
        calibration_card(t("room_air_card"), cal["room_air_o2"], cal["room_air_adc"])
    with cards[1]:
        calibration_card(t("pure_o2_card"), cal["pure_o2_o2"], cal["pure_o2_adc"])

    if has_any:
        csv_buf = io.StringIO()
        csv_buf.write("type,o2_pct,adc\n")
        if cal["room_air_o2"] is not None:
            csv_buf.write(f"room_air,{cal['room_air_o2']},{cal['room_air_adc']}\n")
        if cal["pure_o2_o2"] is not None:
            csv_buf.write(f"pure_o2,{cal['pure_o2_o2']},{cal['pure_o2_adc']}\n")
        st.download_button(
            t("download_calibration_csv"),
            csv_buf.getvalue(),
            file_name="calibration.csv",
            mime="text/csv",
            type="primary",
        )


def gas_calculators_section() -> None:
    st.markdown(
        f'<div class="section-title">{t("gas_calculators")}</div>',
        unsafe_allow_html=True,
    )
    tabs = st.tabs(
        [
            t("tab_physiology"),
            t("tab_consumption"),
            t("tab_cylinder"),
            t("tab_single"),
        ]
    )

    with tabs[0]:
        alt = st.number_input(
            t("altitude_ft"),
            value=25000.0,
            min_value=0.0,
            max_value=40000.0,
            step=500.0,
            key="phys_alt",
        )
        if st.button(t("compute_physiology")):
            res = physiological_params(alt)
            st.json(res)

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            students = st.number_input(
                t("students_per_week"), value=20, min_value=1, step=1, key="cons_students"
            )
            weeks = st.number_input(t("weeks"), value=26, min_value=1, step=1, key="cons_weeks")
            session_min = st.number_input(
                t("session_duration"), value=20.0, min_value=1.0, step=1.0, key="cons_session"
            )
            recovery_min = st.number_input(
                t("recovery_duration"), value=5.0, min_value=0.0, step=1.0, key="cons_recov"
            )
            alt = st.number_input(
                t("altitude_ft"),
                value=25000.0,
                min_value=0.0,
                max_value=40000.0,
                step=500.0,
                key="cons_alt",
            )
        with col2:
            price_air = st.number_input(
                t("price_air"), value=17853.0, min_value=0.0, step=100.0, key="cons_air"
            )
            price_n2 = st.number_input(
                t("price_n2"), value=17838.0, min_value=0.0, step=100.0, key="cons_n2"
            )
            price_o2 = st.number_input(
                t("price_o2"), value=19654.0, min_value=0.0, step=100.0, key="cons_o2"
            )
            contingency = st.number_input(
                t("contingency"), value=10.0, min_value=0.0, max_value=100.0, step=1.0, key="cons_contingency"
            )
        if st.button(t("calculate_consumption")):
            res = gas_consumption(
                students_per_week=students,
                weeks=weeks,
                session_duration_min=session_min,
                recovery_duration_min=recovery_min,
                altitude_ft=alt,
                price_air=price_air,
                price_nitrogen=price_n2,
                price_oxygen=price_o2,
                contingency=contingency / 100.0,
            )
            st.json(res)

    with tabs[2]:
        air_cyl = st.number_input(
            t("air_cylinder"), value=10.0, min_value=0.0, step=0.5
        )
        n2_cyl = st.number_input(
            t("n2_cylinder"), value=9.0, min_value=0.0, step=0.5
        )
        o2_cyl = st.number_input(
            t("o2_cylinder"), value=10.0, min_value=0.0, step=0.5
        )
        session_min = st.number_input(
            t("session_duration"),
            value=20.0,
            min_value=1.0,
            step=1.0,
            key="cap_session",
        )
        recovery_min = st.number_input(
            t("recovery_duration"),
            value=5.0,
            min_value=0.0,
            step=1.0,
            key="cap_recov",
        )
        alt = st.number_input(
            t("altitude_ft"),
            value=25000.0,
            min_value=0.0,
            max_value=40000.0,
            step=500.0,
            key="cap_alt",
        )
        if st.button(t("calculate_capacity")):
            res = cylinder_capacity(air_cyl, n2_cyl, o2_cyl, session_min, recovery_min, alt)
            st.json(res)

    with tabs[3]:
        session_min = st.number_input(
            t("session_duration"),
            value=20.0,
            min_value=1.0,
            step=1.0,
            key="ss_session",
        )
        recovery_min = st.number_input(
            t("recovery_duration"),
            value=5.0,
            min_value=0.0,
            step=1.0,
            key="ss_recov",
        )
        alt = st.number_input(
            t("altitude_ft"),
            value=25000.0,
            min_value=0.0,
            max_value=40000.0,
            step=500.0,
            key="ss_alt",
        )
        price_air = st.number_input(
            t("price_air"), value=17853.0, min_value=0.0, step=100.0, key="ss_air"
        )
        price_n2 = st.number_input(
            t("price_n2"), value=17838.0, min_value=0.0, step=100.0, key="ss_n2"
        )
        price_o2 = st.number_input(
            t("price_o2"), value=19654.0, min_value=0.0, step=100.0, key="ss_o2"
        )
        if st.button(t("calculate_single")):
            res = single_session(session_min, recovery_min, alt, price_air, price_n2, price_o2)
            st.json(res)


def programs_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("programs")}</div>',
        unsafe_allow_html=True,
    )
    program_num = st.number_input(t("program_number"), value=1, min_value=1, max_value=20, step=1)
    prog_name = st.text_input(t("program_name"))
    if st.button(t("save_name")):
        cmd = f"PROG {int(program_num)} NAME {prog_name or 'PROGRAM'}"
        ok, msg = service.send_command(cmd)
        st.toast(msg)
    st.markdown(t("add_step"))
    col1, col2, col3 = st.columns(3)
    with col1:
        step_num = st.number_input(t("step_number"), value=1, min_value=1, max_value=98, step=1)
    with col2:
        mode = st.selectbox(t("mode"), ["HLD", "CHG", "END"])
    with col3:
        altitude = st.number_input(t("altitude_ft"), value=0, min_value=0, max_value=34000, step=500)
    value = st.number_input(t("hold_or_rate"), value=1, min_value=0)
    if st.button(t("send_step")):
        if mode == "END":
            cmd = f"PROG {int(program_num)} {int(step_num)} END"
        else:
            cmd = f"PROG {int(program_num)} {int(step_num)} {mode} {int(altitude)} {int(value)}"
        ok, msg = service.send_command(cmd)
        st.toast(msg)

    st.markdown("---")
    st.markdown(f"### {t('training_helpers')}")
    train_cols = st.columns(3)
    if train_cols[0].button(t("enter_fs_mode")):
        service.send_command("RUN FLSIM")
    if train_cols[1].button(t("o2_dump_on")):
        service.send_command("SET O2DUMP 1")
    if train_cols[2].button(t("o2_dump_off")):
        service.send_command("SET O2DUMP 0")
    alt_set = st.number_input(t("set_fs_alt"), value=10000, min_value=0, max_value=34000, step=500)
    if st.button(t("send_altitude")):
        service.send_command(f"SET FSALT {int(alt_set)}")


def logging_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("logging")}</div>',
        unsafe_allow_html=True,
    )
    _init_debug_log()
    ds = service.data_store

    with st.expander(t("export_buffered"), expanded=True):
        suggested = f"flight_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fname = st.text_input(t("filename"), value=suggested)
        if st.button(t("save_buffer_csv"), type="primary"):
            target_dir = Path("exports")
            try:
                target_dir.mkdir(exist_ok=True)
                _, data_bytes = _export_csv(ds)
                target = target_dir / fname
                target.write_bytes(data_bytes)
                st.toast(t("saved_to", path=str(target)))
            except Exception as exc:  # pragma: no cover - UI notification
                st.toast(t("failed", error=str(exc)))

    with st.expander(t("debug_log"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t("add_debug_marker")):
                st.session_state.debug_log.append(
                    f"{datetime.now().isoformat()} - {t('marker_label')}"
                )
                st.toast(t("marker_added"))
        with col2:
            if st.button(t("prepare_debug_download")):
                content = "\n".join(st.session_state.debug_log) or t("empty_log")
                st.download_button(
                    t("download_debug"),
                    data=content,
                    file_name=f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                    mime="text/plain",
                )


def performance_section(service: SerialService) -> None:
    st.markdown(
        f'<div class="section-title">{t("performance")}</div>',
        unsafe_allow_html=True,
    )
    summary = _performance_summary(service)
    if not summary:
        st.info(t("need_samples"))
        return
    st.metric(t("samples"), summary["samples"])
    st.metric(t("mean_o2"), f"{summary['mean_o2']:.2f}")
    st.metric(t("std_o2"), f"{summary['std_o2']:.2f}")
    st.metric(t("cv_percent"), f"{summary['cv_percent']:.2f}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> None:
    st.set_page_config(page_title="ROBD2", layout="wide", initial_sidebar_state="expanded")
    st.markdown(THEME, unsafe_allow_html=True)
    _language_selector()

    service = _bootstrap_service()
    if "poll_toggle" not in st.session_state:
        st.session_state.poll_toggle = service.connected
    poll_live = bool(st.session_state.get("poll_toggle", False))
    if service.connected and poll_live:
        service.ensure_polling(stale_after=POLL_INTERVAL_SECONDS * 2.5)

    st.sidebar.markdown('<div class="nav-title">ROBD2</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="subtext">{t("sidebar_interface")}</div>', unsafe_allow_html=True)
    status = t("status_connected") if service.connected else t("status_disconnected")
    badge_class = "badge" if service.connected else "badge red"
    st.sidebar.markdown(f'<span class="{badge_class}">{status}</span>', unsafe_allow_html=True)

    st.markdown('<div class="app-title">ROBD2</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtext" style="margin-top:-2px;">{t("app_subtitle")}</div>',
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        t("nav"),
        [
            "connection",
            "dashboard",
            "diagnostics",
            "calibration",
            "gas_calculators",
            "programs",
            "logging",
            "performance",
        ],
        format_func=lambda value: {
            "connection": t("nav_connection"),
            "dashboard": t("nav_dashboard"),
            "diagnostics": t("nav_diagnostics"),
            "calibration": t("nav_calibration"),
            "gas_calculators": t("nav_gas_calculators"),
            "programs": t("nav_programs"),
            "logging": t("nav_logging"),
            "performance": t("nav_performance"),
        }.get(value, value),
        label_visibility="collapsed",
    )
    if page == "connection":
        connection_section(service)
    elif page == "dashboard":
        dashboard_section(service)
    elif page == "diagnostics":
        diagnostics_section(service)
    elif page == "calibration":
        calibration_section(service)
    elif page == "gas_calculators":
        gas_calculators_section()
    elif page == "programs":
        programs_section(service)
    elif page == "logging":
        logging_section(service)
    elif page == "performance":
        performance_section(service)


if __name__ == "__main__":
    main()
