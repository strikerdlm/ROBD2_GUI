import serial
import sys
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from datetime import datetime
import csv
from pathlib import Path
import time
import threading
import serial.tools.list_ports
from Performance import PerformanceMonitor
from calibration_data import handle_calibration  # Add this import

# Set up rich console
console = Console()

# Configure logging with rich handler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("com_serial")

def create_communication_table():
    """Create a simple log display instead of a table"""
    return []  # We'll use a list to store communications

def display_main_menu():
    """Display the main menu with clean formatting"""
    menu_items = [
        "[white]1.[/white] O2 Sensor Calibration",
        "[white]2.[/white] Performance Monitoring",
        "[white]3.[/white] Flight Data Log",
        "[white]4.[/white] Operating Commands",
        "[white]5.[/white] Programming & Configuration",
        "[white]6.[/white] Diagnostics",
        "[white]7.[/white] Exit"
    ]
    
    console.print("\n[bold blue]ROBD2 Command Interface[/bold blue]")
    console.print("[bold blue]by Diego Malpica MD[/bold blue]")
    console.print("─" * 30)
    for item in menu_items:
        console.print(item)
    console.print()

def display_programming_menu():
    """Display the programming and configuration menu"""
    menu_items = [
        "[white]1.[/white] Program Steps",
        "[white]2.[/white] Program Names",
        "[white]3.[/white] Configuration Settings",
        "[white]4.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Programming & Configuration[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

def display_configuration_menu():
    """Display the configuration submenu"""
    menu_items = [
        "[white]1.[/white] Gas Control Settings",
        "[white]2.[/white] Flight Simulator Settings",
        "[white]3.[/white] System Configuration",
        "[white]4.[/white] Back to Programming Menu",
        "[white]5.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Configuration Settings[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

def display_program_steps_menu():
    """Display the program steps submenu"""
    menu_items = [
        "[white]1.[/white] Create/Edit Program Step",
        "[white]2.[/white] View Program Step",
        "[white]3.[/white] Back to Programming Menu",
        "[white]4.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Program Steps[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

def display_program_names_menu():
    """Display the program names submenu"""
    menu_items = [
        "[white]1.[/white] Set Program Name",
        "[white]2.[/white] Get Program Name",
        "[white]3.[/white] Back to Programming Menu",
        "[white]4.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Program Names[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

def parse_run_all_data(data):
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

class DataLogger:
    def __init__(self, ser, communications):
        self.ser = ser
        self.communications = communications
        self.logging = False
        self.log_file = None
        self.log_thread = None
    
    def create_log_file(self, id_number):
        """Create a new log file with ID number and timestamp"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = log_dir / f"{id_number}_{timestamp}.csv"
        
        headers = [
            "Timestamp",
            "Program#",
            "Current_Alt",
            "Final_Alt",
            "O2_Conc",
            "Breathing_Loop_Pressure",
            "Elapsed_Time",
            "Remaining_Time",
            "SpO2",
            "Pulse"
        ]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        
        return filename
    
    def start_logging(self, id_number):
        """Start the logging process with ID number"""
        if self.logging:
            console.print("[yellow]Logging is already running[/yellow]")
            return
            
        self.log_file = self.create_log_file(id_number)
        self.logging = True
        self.log_thread = threading.Thread(target=self._logging_loop)
        self.log_thread.daemon = True
        self.log_thread.start()
        console.print(f"[green]Started logging to {self.log_file}[/green]")
    
    def stop_logging(self):
        """Stop the logging process"""
        if not self.logging:
            console.print("[yellow]Logging is not running[/yellow]")
            return
            
        self.logging = False
        if self.log_thread:
            self.log_thread.join()
        console.print("[green]Logging stopped[/green]")
    
    def _logging_loop(self):
        """Main logging loop"""
        while self.logging:
            try:
                # Send GET RUN ALL command
                command = "GET RUN ALL\r\n"
                self.ser.write(command.encode('utf-8'))
                
                # Wait for response
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').rstrip()
                    parsed_data = parse_run_all_data(data)
                    
                    if parsed_data:
                        # Log to CSV
                        with open(self.log_file, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                parsed_data["timestamp"],
                                parsed_data["program"],
                                parsed_data["current_alt"],
                                parsed_data["final_alt"],
                                parsed_data["o2_conc"],
                                parsed_data["bl_pressure"],
                                parsed_data["elapsed_time"],
                                parsed_data["remaining_time"],
                                parsed_data["spo2"],
                                parsed_data["pulse"]
                            ])
                        
                        # Update the display table
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        self.communications.append(f"{timestamp} ← LOGGED SpO2: {parsed_data['spo2']}% | Pulse: {parsed_data['pulse']} | Alt: {parsed_data['current_alt']}ft")
                
                # Wait 1 second before next reading
                time.sleep(1)
                
            except Exception as e:
                log.error(f"Error in logging loop: {e}")
                self.logging = False
                break

def handle_operating_commands(ser, communications):
    """Handle operating commands menu"""
    menu_items = [
        "[white]1.[/white] Enter Pilot Test Mode (RUN READY)",
        "[white]2.[/white] Exit Pilot Test Mode (RUN EXIT)",
        "[white]3.[/white] Run Program",
        "[white]4.[/white] Advance to Next Step",
        "[white]5.[/white] Abort Current Test",
        "[white]6.[/white] Set O2 Dump State",
        "[white]7.[/white] Activate O2 Failure",
        "[white]8.[/white] Back to Main Menu"
    ]
    
    while True:
        console.print("\n[bold cyan]Operating Commands[/bold cyan]")
        console.print("─" * 25)
        for item in menu_items:
            console.print(item)
        console.print()
        
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4', '5', '6', '7', '8'])
        
        if choice == '8':  # Back to Main Menu
            break
            
        command = None
        if choice == '1':
            command = "RUN READY\r\n"
        elif choice == '2':
            command = "RUN EXIT\r\n"
        elif choice == '3':
            prog_num = Prompt.ask("Program Number", choices=[str(i) for i in range(1, 21)])
            command = f"RUN {prog_num}\r\n"
        elif choice == '4':
            command = "RUN NEXT\r\n"
        elif choice == '5':
            command = "RUN ABORT\r\n"
        elif choice == '6':
            state = Prompt.ask("O2 Dump State (0=OFF, 1=ON)", choices=['0', '1'])
            command = f"SET O2DUMP {state}\r\n"
        elif choice == '7':
            command = "RUN O2FAIL\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_program_creation(ser, communications):
    """Handle program creation with user-friendly interface"""
    console.print("\n[bold cyan]Program Creation[/bold cyan]")
    console.print("─" * 25)
    
    # Get program number
    console.print("\nAvailable program slots: 1-19 (20 reserved for performance testing)")
    prog_num = Prompt.ask("Enter program number", choices=[str(i) for i in range(1, 20)])
    
    # Get program name
    while True:
        prog_name = Prompt.ask("\nEnter program name (max 10 characters)")
        if len(prog_name) <= 10:
            break
        console.print("[red]Name too long. Maximum 10 characters.[/red]")
    
    # Set program name
    command = f"PROG {prog_num} NAME {prog_name}\r\n"
    send_command(ser, command, communications)
    
    # Select program mode
    console.print("\n[bold]Select Program Mode:[/bold]")
    console.print("[white]1.[/white] HRT (Hypoxia Recognition Training)")
    console.print("[white]2.[/white] FSHT (Flight Simulator Hypoxia Training)")
    console.print("[white]3.[/white] OSFT (Oxygen System Failure Training)")
    
    mode_map = {'1': 'HRT', '2': 'FSHT', '3': 'OSFT'}
    mode_choice = Prompt.ask("Select mode", choices=['1', '2', '3'])
    mode = mode_map[mode_choice]
    
    command = f"PROG {prog_num} MODE {mode}\r\n"
    send_command(ser, command, communications)
    
    # Program steps
    step_num = 1
    while True:
        console.print(f"\n[bold cyan]Step {step_num}[/bold cyan]")
        console.print("─" * 25)
        console.print("[white]1.[/white] Add Hold Step (HLD)")
        console.print("[white]2.[/white] Add Change Step (CHG)")
        console.print("[white]3.[/white] End Program (END)")
        console.print("[white]4.[/white] Review Steps")
        console.print("[white]5.[/white] Done")
        
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4', '5'])
        
        if choice == '5':  # Done
            break
            
        elif choice == '4':  # Review steps
            for s in range(1, step_num):
                command = f"PROG {prog_num} {s} ?\r\n"
                send_command(ser, command, communications)
            continue
            
        elif choice == '3':  # End program
            command = f"PROG {prog_num} {step_num} END\r\n"
            send_command(ser, command, communications)
            break
            
        elif choice == '1':  # Hold step
            console.print("\n[bold]Hold Step Configuration[/bold]")
            altitude = Prompt.ask("Enter altitude (feet)")
            
            if mode == 'HRT':
                time_unit = "minutes"
                hold_time = Prompt.ask(f"Enter hold time ({time_unit})")
                command = f"PROG {prog_num} {step_num} HLD {altitude} {hold_time}\r\n"
            else:
                time_unit = "seconds"
                hold_time = Prompt.ask(f"Enter hold time ({time_unit})")
                command = f"PROG {prog_num} {step_num} HLD {altitude} {int(hold_time)/60}\r\n"
                
            send_command(ser, command, communications)
            step_num += 1
            
        elif choice == '2':  # Change step
            console.print("\n[bold]Change Step Configuration[/bold]")
            target_alt = Prompt.ask("Enter target altitude (feet)")
            
            if mode == 'HRT':
                rate_unit = "feet/minute"
            else:
                rate_unit = "feet/second"
                
            rate = Prompt.ask(f"Enter rate of change ({rate_unit})")
            command = f"PROG {prog_num} {step_num} CHG {target_alt} {rate}\r\n"
            send_command(ser, command, communications)
            step_num += 1
    
    console.print(f"\n[green]Program {prog_num} ({prog_name}) created successfully![/green]")
    console.print("\nPress Enter to continue...")
    input()

def handle_programming_commands(ser, communications):
    """Handle programming menu"""
    while True:
        console.print("\n[bold cyan]Programming Menu[/bold cyan]")
        console.print("─" * 25)
        console.print("[white]1.[/white] Create New Program")
        console.print("[white]2.[/white] View/Edit Existing Program")
        console.print("[white]3.[/white] Back to Main Menu")
        
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':  # Back to Main Menu
            break
            
        elif choice == '1':
            handle_program_creation(ser, communications)
            
        elif choice == '2':
            # Get program number to view/edit
            prog_num = Prompt.ask("Enter program number to view/edit", choices=[str(i) for i in range(1, 20)])
            command = f"PROG {prog_num} NAME ?\r\n"
            send_command(ser, command, communications)
            # Add edit functionality here if needed

def handle_program_steps(ser, communications):
    """Handle program steps submenu"""
    while True:
        display_program_steps_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4'])
        
        if choice == '3':  # Back to Programming Menu
            break
        elif choice == '4':  # Back to Main Menu
            return True
            
        command = None
        if choice == '1':  # Create/Edit Program Step
            prog_num = Prompt.ask("Program Number", choices=[str(i) for i in range(1, 21)])
            step_num = Prompt.ask("Step Number", choices=[str(i) for i in range(1, 99)])
            mode = Prompt.ask("Mode", choices=["HLD", "CHG", "END"])
            
            if mode != "END":
                altitude = Prompt.ask("Target Altitude (feet)")
                if mode == "HLD":
                    value = Prompt.ask("Hold Time (minutes)")
                else:
                    value = Prompt.ask("Rate of Change (ft/min)")
                command = f"PROG {prog_num} {step_num} {mode} {altitude} {value}\r\n"
            else:
                command = f"PROG {prog_num} {step_num} END\r\n"
        elif choice == '2':  # View Program Step
            prog_num = Prompt.ask("Program Number", choices=[str(i) for i in range(1, 21)])
            step_num = Prompt.ask("Step Number", choices=[str(i) for i in range(1, 99)])
            command = f"PROG {prog_num} {step_num} ?\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_program_names(ser, communications):
    """Handle program names submenu"""
    while True:
        display_program_names_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4'])
        
        if choice == '3':  # Back to Programming Menu
            break
        elif choice == '4':  # Back to Main Menu
            return True
            
        command = None
        if choice == '1':  # Set Program Name
            prog_num = Prompt.ask("Program Number", choices=[str(i) for i in range(1, 21)])
            prog_name = Prompt.ask("Program Name (max 10 chars)")
            if len(prog_name) > 10:
                console.print("[red]Warning: Name truncated to 10 characters[/red]")
                prog_name = prog_name[:10]
            command = f"PROG {prog_num} NAME {prog_name}\r\n"
        elif choice == '2':  # Get Program Name
            prog_num = Prompt.ask("Program Number", choices=[str(i) for i in range(1, 21)])
            command = f"PROG {prog_num} NAME ?\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_gas_control_settings(ser, communications):
    """Handle gas control settings submenu"""
    while True:
        display_gas_control_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4'])
        
        if choice == '3':  # Back to Programming Menu
            break
        elif choice == '4':  # Back to Main Menu
            return True
            
        command = None
        if choice == '1':  # Set Gas Concentration and Flow
            try:
                concentration = float(Prompt.ask("O2 Concentration (%, must be < 20.94)"))
                if concentration > 20.94:
                    console.print("[red]Error: Concentration must be less than 20.94%[/red]")
                    continue
                    
                flow_rate = int(Prompt.ask("Flow Rate (ccm)"))
                command = f"RUN GAS {concentration:.2f} {flow_rate}\r\n"
            except ValueError:
                console.print("[red]Error: Please enter valid numbers[/red]")
        elif choice == '2':  # Set Air Flow
            try:
                flow_rate = int(Prompt.ask("Air Flow Rate (4000-80000 ccm)"))
                if 4000 <= flow_rate <= 80000:
                    command = f"RUN AIR {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 4000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        if command:
            send_command(ser, command, communications)

def handle_flight_sim_settings(ser, communications):
    """Handle flight simulator settings submenu"""
    while True:
        display_flight_sim_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4'])
        
        if choice == '3':  # Back to Programming Menu
            break
        elif choice == '4':  # Back to Main Menu
            return True
            
        command = None
        if choice == '1':  # Enter Flight Sim Mode
            command = "RUN FLSIM\r\n"
        elif choice == '2':  # Set Flight Sim Altitude
            altitude = Prompt.ask("Flight Sim Altitude (feet, max 34000)")
            try:
                alt_value = int(altitude)
                if 0 <= alt_value <= 34000:
                    command = f"SET FSALT {alt_value}\r\n"
                else:
                    console.print("[red]Error: Altitude must be between 0 and 34000 feet[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        if command:
            send_command(ser, command, communications)

def handle_system_config(ser, communications):
    """Handle system configuration submenu"""
    while True:
        display_system_config_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4', '5', '6'])
        
        if choice == '5':  # Back to Programming Menu
            break
        elif choice == '6':  # Back to Main Menu
            return True
            
        command = None
        if choice == '1':  # Set Mask Flow Rate
            try:
                flow_rate = int(Prompt.ask("Mask Flow Rate (40000-80000 ccm)"))
                if 40000 <= flow_rate <= 80000:
                    command = f"SET MASKFLOW {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 40000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
        elif choice == '2':  # Get Mask Flow Rate
            command = "GET MASKFLOW\r\n"
        elif choice == '3':  # Set O2 Failure Flow Rate
            try:
                flow_rate = int(Prompt.ask("O2 Failure Flow Rate (4000-80000 ccm)"))
                if 4000 <= flow_rate <= 80000:
                    command = f"SET O2FAILFLOW {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 4000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        elif choice == '4':  # Get O2 Failure Flow Rate
            command = "GET O2FAILFLOW\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_performance_monitoring(ser, communications):
    """Handle performance monitoring menu options"""
    monitor = None
    
    while True:
        display_performance_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':  # Back to Main Menu
            if monitor and monitor.monitoring:
                monitor.stop_monitoring()
            break
            
        if choice == '1':
            if not monitor:
                monitor = PerformanceMonitor(ser)
            monitor.start_monitoring()
        elif choice == '2':
            if monitor and monitor.monitoring:
                monitor.stop_monitoring()
            else:
                console.print("[yellow]Monitoring is not running[/yellow]")

def send_command(ser, command, communications):
    """Send command and log response without table"""
    try:
        ser.write(command.encode('utf-8'))
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"{timestamp} → {command.strip()}"
        console.print(log_message)
        log.debug(f"Sent command: {command}")
        
        while True:
            if ser.in_waiting:
                try:
                    data = ser.readline().decode('utf-8').rstrip()
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    response_message = f"{timestamp} ← {data}"
                    console.print(response_message)
                    log.debug(f"Received data: {data}")
                    break
                except UnicodeDecodeError:
                    log.error("Error decoding received data")
                    console.print(f"{timestamp} ← [red]Decode Error[/red]")
                    break
    except Exception as e:
        log.error(f"Error sending command: {e}")
        console.print(f"{timestamp} ← [red]Error: {str(e)}[/red]")

def get_available_ports():
    """Get list of available COM ports"""
    ports = list(serial.tools.list_ports.comports())
    return ports

def select_com_port():
    """Let user select a COM port"""
    ports = get_available_ports()
    
    if not ports:
        console.print("[red]No COM ports found! Please check:[/red]")
        console.print("1. Device is properly connected")
        console.print("2. Device drivers are installed")
        console.print("3. You have necessary permissions")
        console.print("4. Try disconnecting and reconnecting the device")
        sys.exit(1)
    
    console.print("\nAvailable COM ports:")
    for i, port in enumerate(ports, 1):
        # Add more detailed port information
        console.print(f"{i}. {port.device} - {port.description}")
        console.print(f"   Hardware ID: {port.hwid}")
        console.print(f"   Manufacturer: {getattr(port, 'manufacturer', 'Unknown')}")
    
    choice = Prompt.ask(
        "\nSelect COM port",
        choices=[str(i) for i in range(1, len(ports) + 1)]
    )
    
    selected_port = ports[int(choice) - 1].device
    
    # Validate port accessibility before returning
    try:
        with serial.Serial(selected_port, timeout=1) as test_ser:
            test_ser.close()
        return selected_port
    except serial.SerialException as e:
        console.print(f"[red]Error accessing {selected_port}:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        console.print("\n[yellow]Troubleshooting steps:[/yellow]")
        console.print("1. Run the program as administrator")
        console.print("2. Check if another program is using the port")
        console.print("3. Verify the device is properly connected")
        console.print("4. Try a different USB port")
        sys.exit(1)

def handle_configuration_settings(ser, communications):
    """Handle configuration settings submenu"""
    while True:
        display_configuration_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4', '5'])
        
        if choice == '4':  # Back to Programming Menu
            break
        elif choice == '5':  # Back to Main Menu
            return True
            
        if choice == '1':  # Gas Control Settings
            handle_gas_control_settings(ser, communications)
        elif choice == '2':  # Flight Simulator Settings
            handle_flight_sim_settings(ser, communications)
        elif choice == '3':  # System Configuration
            handle_system_config(ser, communications)

def handle_diagnostics(ser, communications):
    """Handle diagnostics (status) commands menu"""
    menu_items = [
        "[white]1.[/white] Get O2 Concentration",
        "[white]2.[/white] Get Breathing Loop Pressure",
        "[white]3.[/white] Get SpO2 Reading",
        "[white]4.[/white] Get Pulse Reading",
        "[white]5.[/white] Get Current Altitude",
        "[white]6.[/white] Get Final Altitude",
        "[white]7.[/white] Get Elapsed Time",
        "[white]8.[/white] Get Remaining Time",
        "[white]9.[/white] Get All Run Data",
        "[white]10.[/white] Get System Info",
        "[white]11.[/white] Get O2 Status",
        "[white]12.[/white] Get System Status",
        "[white]13.[/white] Get MFC Flow Rate",
        "[white]14.[/white] Back to Main Menu"
    ]
    
    while True:
        console.print("\n[bold cyan]Diagnostics Commands[/bold cyan]")
        console.print("─" * 25)
        for item in menu_items:
            console.print(item)
        console.print()
        
        choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, 15)])
        
        if choice == '14':  # Back to Main Menu
            break
            
        command = None
        if choice == '1':
            command = "GET RUN O2CONC\r\n"
        elif choice == '2':
            command = "GET RUN BLPRESS\r\n"
        elif choice == '3':
            command = "GET RUN SPO2\r\n"
        elif choice == '4':
            command = "GET RUN PULSE\r\n"
        elif choice == '5':
            command = "GET RUN ALT\r\n"
        elif choice == '6':
            command = "GET RUN FINALALT\r\n"
        elif choice == '7':
            command = "GET RUN ELTIME\r\n"
        elif choice == '8':
            command = "GET RUN REMTIME\r\n"
        elif choice == '9':
            command = "GET RUN ALL\r\n"
        elif choice == '10':
            command = "GET INFO\r\n"
        elif choice == '11':
            command = "GET O2 STATUS\r\n"
        elif choice == '12':
            command = "GET STATUS\r\n"
        elif choice == '13':
            mfc_num = Prompt.ask("Enter MFC number")
            command = f"GET MFC {mfc_num}\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_flight_sim_commands(ser, communications):
    while True:
        display_flight_sim_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':
            break
            
        command = None
        if choice == '1':
            command = "RUN FLSIM\r\n"
        elif choice == '2':
            altitude = Prompt.ask("Flight Sim Altitude (feet, max 34000)")
            try:
                alt_value = int(altitude)
                if 0 <= alt_value <= 34000:
                    command = f"SET FSALT {alt_value}\r\n"
                else:
                    console.print("[red]Error: Altitude must be between 0 and 34000 feet[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        if command:
            send_command(ser, command, communications)

def handle_gas_control_commands(ser, communications):
    while True:
        display_gas_control_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':
            break
            
        command = None
        if choice == '1':
            try:
                concentration = float(Prompt.ask("O2 Concentration (%, must be < 20.94)"))
                if concentration > 20.94:
                    console.print("[red]Error: Concentration must be less than 20.94%[/red]")
                    continue
                    
                flow_rate = int(Prompt.ask("Flow Rate (ccm)"))
                command = f"RUN GAS {concentration:.2f} {flow_rate}\r\n"
            except ValueError:
                console.print("[red]Error: Please enter valid numbers[/red]")
                
        elif choice == '2':
            try:
                flow_rate = int(Prompt.ask("Air Flow Rate (4000-80000 ccm)"))
                if 4000 <= flow_rate <= 80000:
                    command = f"RUN AIR {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 4000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        if command:
            send_command(ser, command, communications)

def handle_system_config(ser, communications):
    """Handle system configuration menu and its submenus"""
    while True:
        display_system_config_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3', '4', '5', '6'])
        
        if choice == '6':  # Back to Main Menu
            break
            
        if choice == '1':
            try:
                flow_rate = int(Prompt.ask("Mask Flow Rate (40000-80000 ccm)"))
                if 40000 <= flow_rate <= 80000:
                    command = f"SET MASKFLOW {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 40000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        elif choice == '2':
            command = "GET MASKFLOW\r\n"
            
        elif choice == '3':
            try:
                flow_rate = int(Prompt.ask("O2 Failure Flow Rate (4000-80000 ccm)"))
                if 4000 <= flow_rate <= 80000:
                    command = f"SET O2FAILFLOW {flow_rate}\r\n"
                else:
                    console.print("[red]Error: Flow rate must be between 4000 and 80000 ccm[/red]")
            except ValueError:
                console.print("[red]Error: Please enter a valid number[/red]")
                
        elif choice == '4':
            command = "GET O2FAILFLOW\r\n"
            
        if command:
            send_command(ser, command, communications)

def handle_performance_monitoring(ser, communications):
    """Handle performance monitoring menu options"""
    monitor = None
    
    while True:
        display_performance_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':  # Back to Main Menu
            if monitor and monitor.monitoring:
                monitor.stop_monitoring()
            break
            
        if choice == '1':
            if not monitor:
                monitor = PerformanceMonitor(ser)
            monitor.start_monitoring()
        elif choice == '2':
            if monitor and monitor.monitoring:
                monitor.stop_monitoring()
            else:
                console.print("[yellow]Monitoring is not running[/yellow]")

def display_flight_data_menu():
    """Display the flight data logging menu"""
    menu_items = [
        "[white]1.[/white] Start Flight Data Logging",
        "[white]2.[/white] Stop Flight Data Logging",
        "[white]3.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Flight Data Logging[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

def handle_flight_data_logging(ser, communications):
    """Handle flight data logging menu options"""
    data_logger = DataLogger(ser, communications)
    
    while True:
        display_flight_data_menu()
        choice = Prompt.ask("Select option", choices=['1', '2', '3'])
        
        if choice == '3':  # Back to Main Menu
            if data_logger.logging:
                data_logger.stop_logging()
            break
            
        if choice == '1':
            # Get ID number from user
            while True:
                id_number = Prompt.ask("Enter Flight ID Number")
                if id_number.strip():  # Ensure ID is not empty
                    break
                console.print("[red]ID number cannot be empty[/red]")
            data_logger.start_logging(id_number)
        elif choice == '2':
            data_logger.stop_logging()

def read_from_com(port=None, baudrate=9600, timeout=1):
    if port is None:
        port = select_com_port()
        
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        log.info(f"Connected to {port} at {baudrate} baud")
        console.print(f"\n[bold green]Connected to {port} at {baudrate} baud[/bold green]\n")
        
        communications = create_communication_table()
        
        # Clear any initial data in the buffer
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        while True:
            console.clear()
            display_main_menu()
            try:
                choice = Prompt.ask(
                    "[bold]Select option[/bold]",
                    choices=['1', '2', '3', '4', '5', '6', '7'],  # Updated choices
                    show_choices=False
                )
                
                if choice == '7':  # Exit
                    log.info("Exiting application")
                    console.print("[yellow]Exiting application...[/yellow]")
                    break
                    
                # Handle menu choices
                menu_handlers = {
                    '1': lambda: handle_calibration(ser),  # O2 Sensor Calibration
                    '2': lambda: handle_performance_monitoring(ser, communications),  # Performance Monitoring
                    '3': lambda: handle_flight_data_logging(ser, communications),  # Flight Data Log
                    '4': lambda: handle_operating_commands(ser, communications),
                    '5': lambda: handle_programming_commands(ser, communications),
                    '6': lambda: handle_diagnostics(ser, communications),
                }
                
                if choice in menu_handlers:
                    menu_handlers[choice]()
                
            except KeyboardInterrupt:
                log.info("Received keyboard interrupt")
                console.print("\n[yellow]Interrupted by user. Exiting...[/yellow]")
                break
            except Exception as e:
                log.error(f"Error in menu handling: {e}")
                console.print(f"[red]Error: {e}[/red]")
            
        ser.close()
        
    except serial.SerialException as e:
        log.error(f"Serial error: {e}")
        console.print(f"[red]Serial error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        log.exception(f"Unexpected error: {e}")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def display_performance_menu():
    """Display the performance monitoring menu"""
    menu_items = [
        "[white]1.[/white] Start Performance Monitoring",
        "[white]2.[/white] Stop Performance Monitoring",
        "[white]3.[/white] Back to Main Menu"
    ]
    
    console.print("\n[bold cyan]Performance Monitoring[/bold cyan]")
    console.print("─" * 25)
    for item in menu_items:
        console.print(item)
    console.print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ROBD2 Command Interface')
    parser.add_argument('--port', default='COM12', help='COM port to read from')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baudrate')
    parser.add_argument('--timeout', type=float, default=1, help='Timeout in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if not args.debug:
        logging.getLogger("com_serial").setLevel(logging.INFO)
    
    read_from_com(args.port, args.baudrate, args.timeout)