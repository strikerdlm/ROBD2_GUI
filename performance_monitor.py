import serial
import csv
import time
from pathlib import Path
from datetime import datetime
import statistics
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import math

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger("performance_monitor")

@dataclass
class AltitudeSpec:
    altitude: int
    desired_o2: float
    range_min: float
    range_max: float

# O2 specifications table
O2_SPECS = [
    AltitudeSpec(0, 21.00, 20.9, 21.1),
    AltitudeSpec(5000, 17.27, 17.0, 17.5),
    AltitudeSpec(10000, 14.05, 13.8, 14.3),
    AltitudeSpec(13000, 12.34, 12.2, 12.5),
    AltitudeSpec(15000, 11.28, 11.1, 11.4),
    AltitudeSpec(18000, 9.81, 9.66, 10.0),
    AltitudeSpec(20000, 8.91, 8.76, 9.06),
    AltitudeSpec(22000, 8.06, 7.9, 8.2),
    AltitudeSpec(25000, 6.89, 6.74, 7.05),
    AltitudeSpec(28000, 5.86, 5.73, 6.0),
    AltitudeSpec(30000, 5.22, 5.1, 5.35),
    AltitudeSpec(34000, 4.09, 4.0, 4.2),
]

class PerformanceMonitor:
    def __init__(self, serial_port: serial.Serial):
        self.ser = serial_port
        self.monitoring = False
        self.o2_readings = []
        self.last_altitude = None
        self.altitude_change_time = None
        self.device_id = None
        self.data_callback = None
        self.log_file = None

    def set_device_id(self, device_id: str):
        """Set the device ID and create log file"""
        self.device_id = device_id
        self.log_file = self._create_log_file()

    def _create_log_file(self) -> Path:
        """Create a new performance log file with timestamp"""
        if not self.device_id:
            raise ValueError("Device ID must be set before creating log file")
            
        log_dir = Path("performance_logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = log_dir / f"ROBD2_{self.device_id}_{timestamp}.csv"
        
        headers = [
            "Timestamp", "Altitude (feet)", "Desired O2 %", "Actual O2 %",
            "O2 Error %", "O2 Sensor V1", "O2 Sensor V12", "BLP (inH2O)",
            "Min Range %", "Max Range %", "Program", "Final Altitude",
            "Elapsed Time", "Remaining Time", "IC95% Status", "Median O2 %",
            "StdDev", "CV %", "SEM", "Stability %", "Drift %"
        ]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        
        return filename

    def _get_o2_spec(self, altitude: int) -> Optional[AltitudeSpec]:
        """Get O2 specifications for given altitude"""
        valid_specs = [spec for spec in O2_SPECS if spec.altitude <= altitude]
        if not valid_specs:
            return None
        return max(valid_specs, key=lambda x: x.altitude)

    def calculate_statistics(self, o2_readings: List[float], spec: AltitudeSpec) -> Dict:
        """Calculate comprehensive statistics for O2 readings"""
        try:
            mean = statistics.mean(o2_readings)
            median = statistics.median(o2_readings)
            std_dev = statistics.stdev(o2_readings) if len(o2_readings) > 1 else 0
            
            error = mean - spec.desired_o2
            cv = (std_dev / mean) * 100 if mean != 0 else 0
            sem = std_dev / math.sqrt(len(o2_readings)) if len(o2_readings) > 1 else 0
            
            readings_in_range = sum(1 for x in o2_readings 
                                  if spec.range_min <= x <= spec.range_max)
            stability = (readings_in_range / len(o2_readings)) * 100
            
            n = len(o2_readings)
            if n >= 3:
                first_third = statistics.mean(o2_readings[:n//3])
                last_third = statistics.mean(o2_readings[-n//3:])
                drift = last_third - first_third
            else:
                drift = 0
                
            return {
                "mean": mean,
                "median": median,
                "std_dev": std_dev,
                "error": error,
                "cv": cv,
                "sem": sem,
                "stability": stability,
                "drift": drift
            }
        except Exception as e:
            log.error(f"Error calculating statistics: {e}")
            return None

    def _get_o2_data(self) -> Dict:
        """Get O2 concentration and sensor voltages"""
        try:
            self.ser.reset_input_buffer()
            self.ser.write("GET RUN ALL\r\n".encode('utf-8'))
            time.sleep(0.2)
            
            if self.ser.in_waiting:
                data = self.ser.readline().decode('utf-8').rstrip()
                parsed_data = self._parse_run_all_data(data)
                if not parsed_data:
                    return None
                
                # Get voltage readings
                self.ser.reset_input_buffer()
                time.sleep(0.1)
                
                self.ser.write("GET ADC 1\r\n".encode('utf-8'))
                time.sleep(0.2)
                voltage1 = float(self.ser.readline().decode('utf-8').strip()) if self.ser.in_waiting else None
                
                self.ser.reset_input_buffer()
                time.sleep(0.1)
                self.ser.write("GET ADC 12\r\n".encode('utf-8'))
                time.sleep(0.2)
                voltage12 = float(self.ser.readline().decode('utf-8').strip()) if self.ser.in_waiting else None
                
                if voltage1 is None or voltage12 is None:
                    return None
                
                return {
                    "o2_conc": float(parsed_data["o2_conc"]),
                    "altitude": int(float(parsed_data["current_alt"])),
                    "voltage1": voltage1,
                    "voltage12": voltage12,
                    "blp": float(parsed_data["bl_pressure"]),
                    "timestamp": parsed_data["timestamp"],
                    "program": parsed_data["program"],
                    "final_alt": parsed_data["final_alt"],
                    "elapsed_time": parsed_data["elapsed_time"],
                    "remaining_time": parsed_data["remaining_time"]
                }
                
        except Exception as e:
            log.error(f"Error getting O2 data: {e}")
            return None

    def _parse_run_all_data(self, data: str) -> Dict:
        """Parse the GET RUN ALL response"""
        try:
            parts = data.split(',')
            if len(parts) != 10:
                return None
            
            return {
                "timestamp": parts[0],
                "program": parts[1],
                "current_alt": parts[2],
                "final_alt": parts[3],
                "o2_conc": parts[4],
                "bl_pressure": parts[5],
                "elapsed_time": parts[6],
                "remaining_time": parts[7],
                "spo2": parts[8],
                "pulse": parts[9]
            }
        except Exception as e:
            log.error(f"Error parsing run data: {e}")
            return None

    def start_monitoring(self):
        """Start performance monitoring"""
        if not self.device_id:
            raise ValueError("Device ID must be set before starting monitoring")
            
        self.monitoring = True
        self.o2_readings = []
        
        while self.monitoring:
            try:
                data = self._get_o2_data()
                if not data:
                    time.sleep(0.5)
                    continue
                
                # Process data and notify callback if set
                if self.data_callback:
                    self.data_callback(data)
                
                # Log data
                if self.log_file:
                    self._log_data(data)
                
                time.sleep(0.2)
                
            except Exception as e:
                log.error(f"Error in monitoring loop: {e}")
                time.sleep(0.5)

    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False

    def _log_data(self, data: Dict):
        """Log performance data to CSV file"""
        try:
            spec = self._get_o2_spec(data["altitude"])
            if not spec:
                return
                
            self.o2_readings.append(data["o2_conc"])
            if len(self.o2_readings) > 12:
                self.o2_readings.pop(0)
                
            stats = self.calculate_statistics(self.o2_readings, spec)
            if not stats:
                return
                
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data["altitude"],
                f"{spec.desired_o2:.2f}",
                f"{data['o2_conc']:.2f}",
                f"{stats['error']:.2f}",
                f"{data['voltage1']:.3f}",
                f"{data['voltage12']:.3f}",
                f"{data['blp']:.2f}",
                f"{spec.range_min:.2f}",
                f"{spec.range_max:.2f}",
                data["program"],
                data["final_alt"],
                data["elapsed_time"],
                data["remaining_time"],
                "PASS" if stats['error'] < 1.5 else "REVIEW",
                f"{stats['median']:.2f}",
                f"{stats['std_dev']:.3f}",
                f"{stats['cv']:.2f}",
                f"{stats['sem']:.3f}",
                f"{stats['stability']:.1f}",
                f"{stats['drift']:.3f}"
            ]
            
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                
        except Exception as e:
            log.error(f"Error logging data: {e}") 