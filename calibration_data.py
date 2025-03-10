import serial
import time
from datetime import datetime
from pathlib import Path
import csv
import statistics
import math
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

class CalibrationMonitor:
    def __init__(self, ser):
        self.ser = ser
        self.monitoring = False
        self.room_air_readings = []
        self.pure_o2_readings = []
        self.room_air_voltages = []
        self.pure_o2_voltages = []
        self.device_id = self._select_device()
        self.log_file = self._create_log_file()

    def _select_device(self) -> str:
        """Let user select ROBD2 device"""
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
        
        return device_map[choice]

    def _create_log_file(self) -> Path:
        """Create a new calibration log file with device ID and timestamp"""
        log_dir = Path("calibration_logs")
        log_dir.mkdir(exist_ok=True)
        
        # Get device info
        self.ser.write("GET INFO\r\n".encode('utf-8'))
        time.sleep(0.2)
        device_info = self.ser.readline().decode('utf-8').strip() if self.ser.in_waiting else "Unknown"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = log_dir / f"ROBD2_{self.device_id}_{timestamp}.csv"
        
        headers = [
            "Device ID",
            "Device Info",
            "Timestamp",
            "O2 %",
            "ADC12 Voltage",
            "Segment"
        ]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow([self.device_id, device_info, "", "", "", ""])
        
        return filename

    def _get_calibration_data(self) -> dict:
        """Get O2 concentration and ADC12 voltage"""
        try:
            self.ser.reset_input_buffer()
            
            # Get O2 concentration
            self.ser.write("GET RUN O2CONC\r\n".encode('utf-8'))
            time.sleep(0.2)
            if self.ser.in_waiting:
                o2_conc = float(self.ser.readline().decode('utf-8').strip())
            else:
                return None
            
            # Get ADC12 voltage
            self.ser.reset_input_buffer()
            time.sleep(0.1)
            self.ser.write("GET ADC 12\r\n".encode('utf-8'))
            time.sleep(0.2)
            if self.ser.in_waiting:
                voltage = float(self.ser.readline().decode('utf-8').strip())
            else:
                return None
            
            return {
                "o2_conc": o2_conc,
                "voltage": voltage
            }
        except:
            return None

    def calculate_segment_stats(self, readings: list) -> dict:
        """Calculate min, max, median for a segment"""
        if not readings:
            return None
        return {
            "min": min(readings),
            "max": max(readings),
            "median": statistics.median(readings)
        }

    def start_calibration(self):
        """Start calibration monitoring with room air and 100% O2 segments"""
        if self.monitoring:
            console.print("[yellow]Calibration is already running[/yellow]")
            return
        
        self.monitoring = True
        console.print(f"[green]Started O2 sensor calibration for ROBD2-{self.device_id}[/green]")
        
        # Room Air Segment
        console.print("\n[cyan]Collecting Room Air readings (30 seconds)...[/cyan]")
        start_time = time.time()
        last_print_time = 0
        
        while time.time() - start_time < 30:
            data = self._get_calibration_data()
            if data:
                self.room_air_readings.append(data["o2_conc"])
                self.room_air_voltages.append(data["voltage"])
                
                # Log data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = [
                    self.device_id,
                    "",
                    timestamp,
                    f"{data['o2_conc']:.2f}",
                    f"{data['voltage']:.3f}",
                    "Room Air"
                ]
                
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(log_data)
                
                # Display status every 5 seconds
                current_time = time.time()
                if current_time - last_print_time >= 5:
                    console.print(f"O2: {data['o2_conc']:.2f}% | Voltage: {data['voltage']:.3f}V")
                    last_print_time = current_time
            
            time.sleep(0.2)
        
        # 100% O2 Segment
        console.print("\n[cyan]Collecting 100% O2 readings (30 seconds)...[/cyan]")
        start_time = time.time()
        last_print_time = 0
        
        while time.time() - start_time < 30:
            data = self._get_calibration_data()
            if data:
                self.pure_o2_readings.append(data["o2_conc"])
                self.pure_o2_voltages.append(data["voltage"])
                
                # Log data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = [
                    self.device_id,
                    "",
                    timestamp,
                    f"{data['o2_conc']:.2f}",
                    f"{data['voltage']:.3f}",
                    "100% O2"
                ]
                
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(log_data)
                
                # Display status every 5 seconds
                current_time = time.time()
                if current_time - last_print_time >= 5:
                    console.print(f"O2: {data['o2_conc']:.2f}% | Voltage: {data['voltage']:.3f}V")
                    last_print_time = current_time
            
            time.sleep(0.2)
        
        # Calculate and display results
        room_air_stats = self.calculate_segment_stats(self.room_air_voltages)
        pure_o2_stats = self.calculate_segment_stats(self.pure_o2_voltages)
        
        console.print("\n[bold cyan]O2 Sensor Calibration Results[/bold cyan]")
        console.print("─" * 50)
        
        results_table = Table(
            "Parameter",
            "Room Air",
            "100% O2",
            title="Voltage Readings (V)"
        )
        
        if room_air_stats and pure_o2_stats:
            results_table.add_row(
                "Minimum", 
                f"{room_air_stats['min']:.3f}",
                f"{pure_o2_stats['min']:.3f}"
            )
            results_table.add_row(
                "Maximum", 
                f"{room_air_stats['max']:.3f}",
                f"{pure_o2_stats['max']:.3f}"
            )
            results_table.add_row(
                "Median", 
                f"{room_air_stats['median']:.3f}",
                f"{pure_o2_stats['median']:.3f}"
            )
        
        console.print(results_table)
        console.print("\nPress Enter to exit...")
        input()
        self.monitoring = False

def handle_calibration(ser):
    """Handle calibration menu and monitoring"""
    while True:
        console.print("\n[bold cyan]O2 Sensor Calibration[/bold cyan]")
        console.print("─" * 25)
        console.print("[white]1.[/white] Start Calibration")
        console.print("[white]2.[/white] Back to Main Menu")
        
        choice = Prompt.ask("Select option", choices=['1', '2'])
        
        if choice == '2':  # Back to Main Menu
            break
            
        if choice == '1':
            monitor = CalibrationMonitor(ser)
            monitor.start_calibration() 