import serial
import csv
import time
from pathlib import Path
from datetime import datetime
import statistics
from rich.console import Console
from rich.table import Table
from rich.live import Live
import logging
from rich.logging import RichHandler
from dataclasses import dataclass
from typing import List, Dict, Optional
from rich.prompt import Prompt
import math


# Configure rich console and logging
console = Console()

# Create file handler for debug logs
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
file_handler = logging.FileHandler(log_dir / "debug.log")
file_handler.setLevel(logging.DEBUG)

# Create console handler with higher level
console_handler = RichHandler(rich_tracebacks=True, console=console)
console_handler.setLevel(logging.INFO)  # Only show INFO and above in console

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[file_handler, console_handler]
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
    def __init__(self, ser: serial.Serial):
        self.ser = ser
        self.monitoring = False
        self.o2_readings = []
        self.last_altitude = None
        self.altitude_change_time = None
        self.log_file = self._create_log_file()

    def _create_log_file(self) -> Path:
        """Create a new performance log file with timestamp"""
        log_dir = Path("performance_logs")
        log_dir.mkdir(exist_ok=True)
        
        # Prompt user to select ROBD2 device
        console.print("\n[bold cyan]Select ROBD2 Device:[/bold cyan]")
        console.print("[white]1.[/white] ROBD2-9515")
        console.print("[white]2.[/white] ROBD2-9516")
        console.print("[white]3.[/white] ROBD2-9471")
        
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        device_map = {
            '1': '9515',
            '2': '9516',
            '3': '9471'
        }
        
        device_id = device_map[choice]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = log_dir / f"ROBD2_{device_id}_{timestamp}.csv"
        
        # Define headers for the CSV file
        headers = [
            "Timestamp",
            "Altitude (feet)",
            "Desired O2 %",
            "Actual O2 %",
            "O2 Error %",
            "O2 Sensor V1",
            "O2 Sensor V12",
            "BLP (inH2O)",
            "Min Range %",
            "Max Range %",
            "Program",
            "Final Altitude",
            "Elapsed Time",
            "Remaining Time",
            "IC95% Status",
            "Median O2 %",
            "StdDev",
            "CV %",
            "SEM",
            "Stability %",
            "Drift %"
        ]
        
        # Create the CSV file with headers
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        
        # Store device ID for later use
        self.device_id = device_id
        
        return filename

    def _is_stabilization_period(self, current_altitude: int) -> bool:
        """Check if we're in the 25-second stabilization period after altitude change"""
        current_time = time.time()
        
        # If this is our first reading
        if self.last_altitude is None:
            self.last_altitude = current_altitude
            self.altitude_change_time = current_time
            return True
        
        # If altitude has changed
        if current_altitude != self.last_altitude:
            self.last_altitude = current_altitude
            self.altitude_change_time = current_time
            self.o2_readings.clear()  # Clear readings from previous altitude
            return True
        
        # If we're within 25 seconds of an altitude change
        if self.altitude_change_time and (current_time - self.altitude_change_time) < 25:
            return True
            
        return False

    def _get_o2_spec(self, altitude: int) -> Optional[AltitudeSpec]:
        """Get O2 specifications for given altitude"""
        # Find the closest altitude spec that's not exceeding our current altitude
        valid_specs = [spec for spec in O2_SPECS if spec.altitude <= altitude]
        if not valid_specs:
            return None
        return max(valid_specs, key=lambda x: x.altitude)

    def _get_performance_status(self, actual_o2: float, spec: AltitudeSpec) -> tuple[str, str]:
        """Determine performance status and color based on O2 readings"""
        if spec.range_min <= actual_o2 <= spec.range_max:
            return "PASSED", "green"
        elif (spec.range_min - 0.5) <= actual_o2 <= (spec.range_max + 0.5):
            return "REVIEW", "yellow"
        else:
            return "NOT PASSED", "red"

    def parse_run_all_data(self, data):
        """Parse the GET RUN ALL response into a dictionary"""
        try:
            # Format: mm-dd-yy hh-mm-ss,program#,current alt,final alt,o2conc,breathing loop pressure,
            # elapsed time,remaining time,spo2,pulse
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

    def _get_o2_data(self) -> Dict:
        """Get O2 concentration and sensor voltages in real time"""
        try:
            # Clear input buffer before starting
            self.ser.reset_input_buffer()
            
            # Get all run data in one command
            self.ser.write("GET RUN ALL\r\n".encode('utf-8'))
            time.sleep(0.2)
            
            if self.ser.in_waiting:
                data = self.ser.readline().decode('utf-8').rstrip()
                parsed_data = self.parse_run_all_data(data)
                if not parsed_data:
                    return None
                
                # Still need to get the voltage readings
                self.ser.reset_input_buffer()
                time.sleep(0.1)
                
                # Get V1 reading
                self.ser.write("GET ADC 1\r\n".encode('utf-8'))
                time.sleep(0.2)
                if self.ser.in_waiting:
                    voltage1 = float(self.ser.readline().decode('utf-8').strip())
                else:
                    log.debug("No response for V1 voltage")
                    return None
                
                # Get V12 reading
                self.ser.reset_input_buffer()
                time.sleep(0.1)
                self.ser.write("GET ADC 12\r\n".encode('utf-8'))
                time.sleep(0.2)
                if self.ser.in_waiting:
                    voltage12 = float(self.ser.readline().decode('utf-8').strip())
                else:
                    log.debug("No response for V12 voltage")
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
            log.debug(f"Error getting O2 data: {e}")
            return None

    def calculate_ic95(self, error: float, spec: AltitudeSpec) -> tuple[str, str]:
        """Calculate 95% confidence interval and determine status"""
        try:
            # Calculate standard error (using 1.96 for 95% CI)
            margin_of_error = 1.96 * abs(error) / math.sqrt(len(self.o2_readings))
            lower_bound = error - margin_of_error
            upper_bound = error + margin_of_error
            
            # Check if the error range falls within acceptable limits
            if (spec.range_min <= (spec.desired_o2 + upper_bound) <= spec.range_max and 
                spec.range_min <= (spec.desired_o2 + lower_bound) <= spec.range_max):
                return "PASS", "green"
            else:
                # If initial check results in REVIEW, check error percentage
                if abs(error) < 1.5:  # If error is less than 1.5%
                    return "PASS", "green"
                else:
                    return "REVIEW", "yellow"
        except Exception as e:
            log.error(f"Error calculating IC95: {e}")
            return "ERROR", "red"

    def _create_altitude_results(self):
        """Create dictionary to store results for each altitude"""
        self.altitude_results = {alt.altitude: {
            'passes': 0,
            'total_readings': 0,
            'stats': [],
            'completed': False
        } for alt in O2_SPECS}

    def _check_test_completion(self) -> bool:
        """Check if we've completed testing all altitudes"""
        # Check if we're back at sea level (0 ft) after testing higher altitudes
        if self.last_altitude == 0 and any(results['completed'] for alt, results in self.altitude_results.items() if alt > 0):
            return True
        return False

    def _print_final_results(self):
        """Print final test results table and statistics"""
        console.print("\n[bold cyan]ROBD2 Performance Test Results[/bold cyan]")
        console.print("─" * 80)
        
        all_altitudes_passed = True
        
        # Create and print results table
        results_table = Table(
            "Altitude (ft)", 
            "Passes", 
            "Total Readings", 
            "Status",
            title="Test Results by Altitude"
        )
        
        for altitude, data in sorted(self.altitude_results.items(), reverse=True):
            if data['total_readings'] > 0:  # Only show altitudes that were tested
                passes = data['passes']
                total = data['total_readings']
                status = "[green]PASS[/green]" if passes >= 3 else "[red]FAIL[/red]"
                
                if passes < 3:
                    all_altitudes_passed = False
                    
                results_table.add_row(
                    str(altitude),
                    str(passes),
                    str(total),
                    status
                )
        
        console.print(results_table)
        console.print("\n[bold cyan]Statistical Analysis by Altitude[/bold cyan]")
        console.print("─" * 80)
        
        # Print statistics for each altitude
        for altitude, data in sorted(self.altitude_results.items(), reverse=True):
            if data['stats']:
                avg_stats = {
                    key: sum(stat[key] for stat in data['stats']) / len(data['stats'])
                    for key in ['median', 'std_dev', 'cv', 'sem', 'stability', 'drift']
                }
                
                console.print(f"\nAltitude: {altitude} ft")
                console.print(
                    f"Median O2: {avg_stats['median']:.2f}% | "
                    f"StdDev: {avg_stats['std_dev']:.3f} | "
                    f"CV: {avg_stats['cv']:.2f}% | "
                    f"SEM: {avg_stats['sem']:.3f} | "
                    f"Stability: {avg_stats['stability']:.1f}% | "
                    f"Drift: {avg_stats['drift']:.3f}%"
                )
        
        console.print("\n" + "─" * 80)
        if all_altitudes_passed:
            console.print("\n[green bold]TEST PASSED - ROBD2 SAFE TO USE[/green bold]")
        else:
            console.print("\n[red bold]TEST FAILED - ROBD2 NEEDS REVIEW[/red bold]")
        
        console.print("\nPress Enter to exit...")
        input()
        self.stop_monitoring()

    def start_monitoring(self):
        """Start performance monitoring with test completion check"""
        if self.monitoring:
            console.print("[yellow]Monitoring is already running[/yellow]")
            return
        
        # Temporarily disable debug logging
        original_level = log.getEffectiveLevel()
        log.setLevel(logging.ERROR)  # Only show ERROR level logs
        
        try:
            self.monitoring = True
            self._create_altitude_results()
            console.print(f"[green]Started performance monitoring for ROBD2-{self.device_id} to {self.log_file}[/green]")
            
            last_print_time = 0
            
            while self.monitoring:
                try:
                    data = self._get_o2_data()
                    if not data:
                        time.sleep(0.5)
                        continue
                    
                    current_altitude = data["altitude"]
                    
                    # Check for test completion
                    if self._check_test_completion():
                        self._print_final_results()
                        break
                    
                    in_stabilization = self._is_stabilization_period(current_altitude)
                    
                    # Always append the reading for monitoring
                    self.o2_readings.append(data["o2_conc"])
                    
                    # Calculate average using available readings
                    avg_o2 = statistics.mean(self.o2_readings[-12:])
                    spec = self._get_o2_spec(data["altitude"])
                    
                    if spec:
                        error = avg_o2 - spec.desired_o2
                        
                        # Only calculate statistics if we're past stabilization period
                        if not in_stabilization:
                            ic95_status, color = self.calculate_ic95(error, spec)
                            stats = self.calculate_statistics(self.o2_readings[-12:], spec)
                        else:
                            ic95_status, color = "STABILIZING", "yellow"
                            stats = {
                                "median": avg_o2,
                                "std_dev": 0.0,
                                "cv": 0.0,
                                "sem": 0.0,
                                "stability": 0.0,
                                "drift": 0.0
                            }
                        
                        # Enhanced logging with more details
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_data = [
                            timestamp,
                            data["altitude"],
                            f"{spec.desired_o2:.2f}",
                            f"{avg_o2:.2f}",
                            f"{error:.2f}",
                            f"{data['voltage1']:.3f}",
                            f"{data['voltage12']:.3f}",
                            f"{data['blp']:.2f}",
                            f"{spec.range_min:.2f}",
                            f"{spec.range_max:.2f}",
                            data["program"],
                            data["final_alt"],
                            data["elapsed_time"],
                            data["remaining_time"],
                            ic95_status,
                            f"{stats['median']:.2f}",
                            f"{stats['std_dev']:.3f}",
                            f"{stats['cv']:.2f}",
                            f"{stats['sem']:.3f}",
                            f"{stats['stability']:.1f}",
                            f"{stats['drift']:.3f}"
                        ]
                        
                        # Write to CSV file
                        try:
                            with open(self.log_file, 'a', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow(log_data)
                        except Exception as e:
                            log.error(f"Error writing to CSV: {e}")
                        
                        # Display current values every 5 seconds
                        current_time = time.time()
                        if current_time - last_print_time >= 5:
                            status_message = (
                                f"{timestamp} | "
                                f"Program: {data['program']} | "
                                f"Alt: {data['altitude']}ft | "
                                f"Target Alt: {data['final_alt']}ft | "
                                f"O2: {avg_o2:.2f}% | "
                                f"Target: {spec.desired_o2:.2f}% | "
                                f"Error: {error:.2f}% | "
                                f"BLP: {data['blp']:.2f}inH2O | "
                                f"V1: {data['voltage1']:.3f}V | "
                                f"V12: {data['voltage12']:.3f}V | "
                                f"Time: {data['elapsed_time']}/{data['remaining_time']} | "
                            )
                            
                            if in_stabilization:
                                remaining_stabilization = 25 - (current_time - self.altitude_change_time)
                                status_message += f"[yellow]STABILIZING ({remaining_stabilization:.0f}s)[/yellow]"
                            else:
                                status_message += f"[{color}]IC95: {ic95_status}[/{color}]"
                            
                            # Add statistical analysis as a separate line (only if not stabilizing)
                            if not in_stabilization:
                                stats_message = (
                                    f"\n[blue]Statistical Analysis:[/blue] "
                                    f"Median: {stats['median']:.2f}% | "
                                    f"StdDev: {stats['std_dev']:.3f} | "
                                    f"CV: {stats['cv']:.2f}% | "
                                    f"SEM: {stats['sem']:.3f} | "
                                    f"Stability: {stats['stability']:.1f}% | "
                                    f"Drift: {stats['drift']:.3f}%"
                                )
                                console.print(status_message)
                                console.print(stats_message)
                            else:
                                console.print(status_message)
                                
                            last_print_time = current_time
                    
                    # When recording a PASS status:
                    if not in_stabilization and current_altitude in self.altitude_results:
                        self.altitude_results[current_altitude]['total_readings'] += 1
                        if ic95_status == "PASS":
                            self.altitude_results[current_altitude]['passes'] += 1
                        if stats:
                            self.altitude_results[current_altitude]['stats'].append(stats)
                        self.altitude_results[current_altitude]['completed'] = True
                    
                    time.sleep(0.2)
                    
                except Exception as e:
                    log.debug(f"Error in monitoring loop: {e}")
                    time.sleep(0.5)
            
        finally:
            # Restore original logging level when done
            log.setLevel(original_level)

    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring:
            console.print("[yellow]Monitoring is not running[/yellow]")
            return
        
        self.monitoring = False
        console.print("[green]Performance monitoring stopped[/green]")

    def calculate_statistics(self, o2_readings: List[float], spec: AltitudeSpec) -> Dict:
        """Calculate comprehensive statistics for O2 readings"""
        try:
            # Basic statistics
            mean = statistics.mean(o2_readings)
            median = statistics.median(o2_readings)
            std_dev = statistics.stdev(o2_readings) if len(o2_readings) > 1 else 0
            
            # Calculate error
            error = mean - spec.desired_o2
            
            # Calculate coefficient of variation (CV)
            cv = (std_dev / mean) * 100 if mean != 0 else 0
            
            # Calculate standard error of mean (SEM)
            sem = std_dev / math.sqrt(len(o2_readings)) if len(o2_readings) > 1 else 0
            
            # Calculate stability (percentage of readings within range)
            readings_in_range = sum(1 for x in o2_readings 
                                  if spec.range_min <= x <= spec.range_max)
            stability = (readings_in_range / len(o2_readings)) * 100
            
            # Calculate drift (difference between first and last third of readings)
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
 