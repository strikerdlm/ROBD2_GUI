import tkinter as tk
from tkinter import ttk, messagebox
import sys
import logging
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from data_store import DataStore
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame
from windows import ChecklistWindow, ScriptViewerWindow, LoadingIndicator
from serial_comm import SerialCommunicator
from calibration_data import CalibrationMonitor
from Performance import PerformanceMonitor
from COM_serial import DataLogger

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("robd2_gui")

class ROBD2GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ROBD2 Diagnostic UI by Diego Malpica")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.serial_comm = SerialCommunicator()
        self.data_store = DataStore()
        self.plotting_active = False
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main container
        self.main_container = ModernFrame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create status bar
        self.status_bar = ttk.Label(
            self.main_container,
            text="Not Connected",
            font=('Helvetica', 10)
        )
        self.status_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs in specified order
        self.create_connection_tab()
        self.create_calibration_tab()
        self.create_performance_tab()
        self.create_training_tab()
        self.create_dashboard_tab()
        self.create_diagnostics_tab()
        self.create_programming_tab()
        self.create_logging_tab()
        
        # Add keyboard shortcuts
        self.add_keyboard_shortcuts()
        
        # Start plot updates
        self.root.after(1000, self.update_plots)
        
    def create_menu_bar(self):
        """Create the menu bar"""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Connect (Ctrl+C)", command=self.connect_to_device)
        file_menu.add_command(label="Disconnect (Ctrl+D)", command=self.disconnect_device)
        file_menu.add_separator()
        file_menu.add_command(label="Export Data (Ctrl+E)", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Refresh Ports (Ctrl+R)", command=self.refresh_ports)
        tools_menu.add_command(label="Start Logging (Ctrl+S)", command=self.start_logging)
        tools_menu.add_command(label="Stop Logging (Ctrl+X)", command=self.stop_logging)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        
    def add_keyboard_shortcuts(self):
        """Add keyboard shortcuts"""
        self.root.bind('<Control-r>', lambda e: self.refresh_ports())
        self.root.bind('<Control-c>', lambda e: self.connect_to_device() if not self.serial_comm.is_connected else None)
        self.root.bind('<Control-d>', lambda e: self.disconnect_device() if self.serial_comm.is_connected else None)
        self.root.bind('<Control-e>', lambda e: self.export_data() if hasattr(self, 'data_store') else None)
        self.root.bind('<Control-s>', lambda e: self.start_logging() if self.serial_comm.is_connected else None)
        self.root.bind('<Control-x>', lambda e: self.stop_logging() if hasattr(self, 'data_logger') else None)
        
    def refresh_ports(self):
        """Refresh available COM ports"""
        ports = self.serial_comm.get_available_ports()
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
            
    def connect_to_device(self):
        """Connect to the selected COM port"""
        try:
            port = self.port_var.get()
            if not port:
                messagebox.showerror("Error", "Please select a COM port")
                return
                
            # Show loading indicator
            loading = LoadingIndicator(self.root, "Connecting to device...")
            self.root.update()
            
            success, message = self.serial_comm.connect(port)
            
            if success:
                # Update UI state
                self.connect_btn.configure(state=tk.DISABLED)
                self.disconnect_btn.configure(state=tk.NORMAL)
                self.port_combo.configure(state=tk.DISABLED)
                
                # Enable features
                self.start_calibration_btn.configure(state=tk.NORMAL)
                self.start_performance_btn.configure(state=tk.NORMAL)
                self.start_logging_btn.configure(state=tk.NORMAL)
                
                # Update status
                self.status_bar.configure(text=f"Connected to {port}")
                self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Connected to {port}\n")
            else:
                messagebox.showerror("Connection Error", message)
                self.status_bar.configure(text="Connection Failed")
                self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Connection failed: {message}\n")
            
            # Destroy loading indicator
            loading.destroy()
            
        except Exception as e:
            log.error(f"Unexpected connection error: {e}", exc_info=True)
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_bar.configure(text="Connection Failed")
            self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Unexpected error: {str(e)}\n")
            
    def disconnect_device(self):
        """Disconnect from the COM port"""
        success, message = self.serial_comm.disconnect()
        
        if success:
            # Update UI state
            self.connect_btn.configure(state=tk.NORMAL)
            self.disconnect_btn.configure(state=tk.DISABLED)
            self.port_combo.configure(state=tk.NORMAL)
            
            # Disable features
            self.start_calibration_btn.configure(state=tk.DISABLED)
            self.start_performance_btn.configure(state=tk.DISABLED)
            self.start_logging_btn.configure(state=tk.DISABLED)
            self.export_btn.configure(state=tk.DISABLED)
            
            # Update status
            self.status_bar.configure(text="Disconnected")
            self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Disconnected\n")
        else:
            messagebox.showerror("Error", message)
            
    def send_diagnostic_command(self, command):
        """Send a diagnostic command to the device"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        success, message = self.serial_comm.send_command(command)
        if success:
            self.response_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} → {command}\n")
        else:
            messagebox.showerror("Error", message)
            
    def poll_responses(self):
        """Poll for responses from the device"""
        try:
            response = self.serial_comm.get_response()
            if response:
                self.response_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} ← {response}\n")
                self.response_text.see(tk.END)
                
        except Exception as e:
            log.error(f"Error polling response: {e}")
            
        # Schedule the next poll
        self.root.after(100, self.poll_responses)
        
    def start_calibration(self):
        """Start O2 sensor calibration"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        device_id = self.device_var.get()
        if not device_id:
            messagebox.showerror("Error", "Please select a device")
            return
            
        # Run calibration in a separate thread
        def run_calibration():
            monitor = CalibrationMonitor(self.serial_comm.serial_port)
            monitor.device_id = device_id
            
            # Update UI from the main thread
            self.root.after(0, lambda: self.results_text.insert(tk.END, "Starting calibration...\n"))
            
            # This is a blocking call, but it's in a separate thread
            monitor.start_calibration()
            
            # Update UI when done
            self.root.after(0, lambda: self.results_text.insert(tk.END, "Calibration complete.\n"))
        
        threading.Thread(target=run_calibration, daemon=True).start()
        
    def start_performance_monitoring(self):
        """Start performance monitoring"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        device_id = self.perf_device_var.get()
        if not device_id:
            messagebox.showerror("Error", "Please select a device")
            return
        
        try:
            # Disable/enable appropriate buttons
            self.start_performance_btn.configure(state=tk.DISABLED)
            self.stop_performance_btn.configure(state=tk.NORMAL)
            self.export_btn.configure(state=tk.DISABLED)  # Disable export while monitoring
            
            # Clear existing data
            self.data_store.clear()
            self.plotting_active = True
                
            # Run monitoring in a separate thread
            def run_monitoring():
                try:
                    self.performance_monitor = PerformanceMonitor(self.serial_comm.serial_port)
                    self.performance_monitor.device_id = device_id
                    
                    # Override the data processing to update our data store
                    def process_data(data):
                        try:
                            timestamp = datetime.now()
                            self.data_store.add_data(timestamp, {
                                'altitude': data.get('altitude', 0),
                                'o2_conc': data.get('o2_conc', 0),
                                'blp': data.get('blp', 0),
                                'spo2': data.get('spo2', 0),
                                'pulse': data.get('pulse', 0),
                                'o2_voltage': data.get('o2_voltage', 0),
                                'error_percent': data.get('error_percent', 0)
                            })
                        except Exception as e:
                            log.error(f"Error processing data: {e}", exc_info=True)
                    
                    self.performance_monitor.process_data = process_data
                    
                    # This is a blocking call, but it's in a separate thread
                    self.performance_monitor.start_monitoring()
                    
                except Exception as e:
                    log.error(f"Error in monitoring thread: {e}", exc_info=True)
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Monitoring error: {str(e)}"))
            
            threading.Thread(target=run_monitoring, daemon=True).start()
            
        except Exception as e:
            log.error(f"Error starting monitoring: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            self.start_performance_btn.configure(state=tk.NORMAL)
            self.stop_performance_btn.configure(state=tk.DISABLED)
            self.export_btn.configure(state=tk.NORMAL)
            
    def stop_performance_monitoring(self):
        """Stop performance monitoring"""
        if hasattr(self, 'performance_monitor'):
            try:
                self.performance_monitor.stop_monitoring()
                self.start_performance_btn.configure(state=tk.NORMAL)
                self.stop_performance_btn.configure(state=tk.DISABLED)
                self.export_btn.configure(state=tk.NORMAL)  # Enable export after stopping
                self.plotting_active = False
            except Exception as e:
                log.error(f"Error stopping monitoring: {e}", exc_info=True)
                messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
                
    def start_logging(self):
        """Start flight data logging"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        flight_id = self.flight_id_var.get()
        if not flight_id:
            messagebox.showerror("Error", "Please enter a Flight ID")
            return
            
        # Update UI state
        self.start_logging_btn.configure(state=tk.DISABLED)
        self.stop_logging_btn.configure(state=tk.NORMAL)
        
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"flight_{flight_id}_{timestamp}.log"
        
        # Configure file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        log.addHandler(file_handler)
        
        # Create a custom list class for communications
        class LoggingList(list):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.callback = None
                
            def append(self, item):
                super().append(item)
                if self.callback:
                    self.callback(item)
                    
        # Run logging in a separate thread
        def run_logging():
            self.data_logger = DataLogger(self.serial_comm.serial_port, [])
            
            # Create custom list for communications
            self.data_logger.communications = LoggingList()
            
            # Update the log display
            def update_log(message):
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END)
                log.info(message)
                
            # Set the callback for the custom list
            self.data_logger.communications.callback = update_log
            
            # Start logging (blocking call in the thread)
            self.data_logger.start_logging(flight_id)
        
        threading.Thread(target=run_logging, daemon=True).start()
        
    def stop_logging(self):
        """Stop flight data logging"""
        if hasattr(self, 'data_logger'):
            self.data_logger.stop_logging()
            self.start_logging_btn.configure(state=tk.NORMAL)
            self.stop_logging_btn.configure(state=tk.DISABLED)
            
            # Remove file handler
            for handler in log.handlers[:]:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
                    log.removeHandler(handler)
                    
    def export_data(self):
        """Export data to CSV file"""
        try:
            from tkinter import filedialog
            
            # Get filename from user
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialdir="exports",
                title="Export Data"
            )
            
            if filename:
                success, result = self.data_store.export_to_csv(filename)
                if success:
                    messagebox.showinfo("Success", f"Data exported to {result}")
                else:
                    messagebox.showerror("Error", f"Failed to export data: {result}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
            log.error(f"Export error: {e}", exc_info=True)
            
    def show_about(self):
        """Show the About window"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About ROBD2 Diagnostic UI")
        about_window.geometry("800x700")
        
        # Create a canvas with scrollbar for scrolling
        canvas = tk.Canvas(about_window)
        scrollbar = ttk.Scrollbar(about_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Create main container
        main_frame = ModernFrame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title with custom styling
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="ROBD2 Diagnostic UI",
            font=('Helvetica', 24, 'bold')
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="A Comprehensive Tool for ROBD2 Device Management",
            font=('Helvetica', 12)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Version with custom styling
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        version_label = ttk.Label(
            version_frame,
            text="Version 1.0.0",
            font=('Helvetica', 14, 'bold')
        )
        version_label.pack()
        
        # Author information
        author_frame = ModernLabelFrame(main_frame, text="Author", padding=15)
        author_frame.pack(fill=tk.X, pady=(0, 20))
        
        author_text = """
Diego Malpica MD
Aerospace Medicine Specialist
Aerospace Physiology Instructor
Aerospace Scientific Department
Aerospace Medicine Directorate
Colombian Aerospace Force

Initial work - [strikerdlm](https://github.com/strikerdlm)

Copyright © 2025 Diego Malpica MD. All rights reserved.

License: MIT License
Repository: https://github.com/strikerdlm/ROBD2_GUI
For contributing please read the CONTRIBUTING.md file in the repository.
"""
        author_label = ttk.Label(
            author_frame,
            text=author_text,
            wraplength=700,
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        author_label.pack()
        
        # Description
        description_frame = ModernLabelFrame(main_frame, text="Overview", padding=15)
        description_frame.pack(fill=tk.X, pady=(0, 20))
        
        description_text = """
The ROBD2 Diagnostic Interface is a comprehensive tool for monitoring, calibrating, and analyzing data from ROBD2 devices. It provides real-time visualization of critical parameters, data logging capabilities, and diagnostic tools for aerospace physiology training.

This software is EXPERIMENTAL and should only be used in controlled environments under the supervision of trained medical professionals or experts in ROBD devices for aerospace physiology training.
"""
        description_label = ttk.Label(
            description_frame,
            text=description_text,
            wraplength=700,
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        description_label.pack()
        
        # Features
        features_frame = ModernLabelFrame(main_frame, text="Key Features", padding=15)
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features_text = """
• Real-time data visualization with customizable time scales
• Comprehensive data logging and export capabilities
• Device calibration tools
• Performance monitoring
• Diagnostic command interface
• Modern, intuitive user interface
• Automatic data validation and range checking
• CSV data export with timestamps
"""
        features_label = ttk.Label(
            features_frame,
            text=features_text,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 11)
        )
        features_label.pack()
        
        # Requirements
        requirements_frame = ModernLabelFrame(main_frame, text="System Requirements", padding=15)
        requirements_frame.pack(fill=tk.X, pady=(0, 20))
        
        requirements_text = """
• Python 3.8 or higher
• Windows 10 or higher
• Required Python packages:
  - pyserial
  - rich
  - matplotlib
  - numpy
"""
        requirements_label = ttk.Label(
            requirements_frame,
            text=requirements_text,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 11)
        )
        requirements_label.pack()
        
        # Add mousewheel scrolling support with error handling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass
            
        def _on_linux_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
            except tk.TclError:
                pass
                
        # Bind mousewheel events
        if sys.platform.startswith('win'):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:
            canvas.bind_all("<Button-4>", _on_linux_mousewheel)
            canvas.bind_all("<Button-5>", _on_linux_mousewheel)
            
        # Define closing function to properly unbind events
        def _on_closing():
            try:
                canvas.unbind_all("<MouseWheel>")
                canvas.unbind_all("<Button-4>")
                canvas.unbind_all("<Button-5>")
            except tk.TclError:
                pass
            about_window.destroy()
            
        about_window.protocol("WM_DELETE_WINDOW", _on_closing)
            
        # Center the window on the screen
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Make window modal
        about_window.transient(self.root)
        about_window.grab_set()
        self.root.wait_window(about_window)
        
    def show_documentation(self):
        """Show the documentation window"""
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentation")
        doc_window.geometry("800x600")
        
        # Create main container
        main_frame = ModernFrame(doc_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="ROBD2 Diagnostic Interface Documentation",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for content
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernFrame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add documentation content
        content = """
Keyboard Shortcuts:
------------------
Ctrl+C: Connect to device
Ctrl+D: Disconnect from device
Ctrl+E: Export data
Ctrl+R: Refresh ports
Ctrl+S: Start logging
Ctrl+X: Stop logging

Connection Tab:
--------------
1. Select the COM port where the ROBD2 device is connected
2. Click "Connect" or press Ctrl+C to establish connection
3. Use the pre-flight checklist to verify device setup

Calibration Tab:
---------------
1. Select the device to calibrate
2. Follow the calibration procedure
3. Monitor results in real-time

Performance Tab:
---------------
1. Select the device to monitor
2. Start/stop performance monitoring
3. View real-time data

Training Tab:
------------
1. Access training scripts for different aircraft types
2. Use checklists during and after training
3. Follow proper procedures

Dashboard Tab:
-------------
1. View real-time plots of various parameters
2. Export data for analysis
3. Monitor statistics

Diagnostics Tab:
---------------
1. Send diagnostic commands
2. View device responses
3. Troubleshoot issues

Programming Tab:
---------------
1. Create and modify device programs
2. Add hold and change steps
3. Review program configuration

Logging Tab:
-----------
1. Start/stop data logging
2. Monitor log data
3. Export logs for analysis

For more information, please refer to the ROBD2 Technical Manual.
"""
        
        content_label = ttk.Label(
            scrollable_frame,
            text=content,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 11)
        )
        content_label.pack(pady=10)
        
        # Add mousewheel scrolling support with error handling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass
            
        def _on_linux_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
            except tk.TclError:
                pass
            
        # Bind for Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Bind for Linux
        canvas.bind_all("<Button-4>", _on_linux_mousewheel)
        canvas.bind_all("<Button-5>", _on_linux_mousewheel)
        
        # Unbind when window is closed
        def _on_closing():
            try:
                canvas.unbind_all("<MouseWheel>")
                canvas.unbind_all("<Button-4>")
                canvas.unbind_all("<Button-5>")
            except tk.TclError:
                pass
            doc_window.destroy()
            
        doc_window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Center window on screen
        doc_window.update_idletasks()
        width = doc_window.winfo_width()
        height = doc_window.winfo_height()
        x = (doc_window.winfo_screenwidth() // 2) - (width // 2)
        y = (doc_window.winfo_screenheight() // 2) - (height // 2)
        doc_window.geometry(f'{width}x{height}+{x}+{y}')
        
    def update_plots(self):
        """Update the dashboard plots with new data"""
        if not self.plotting_active:
            return
            
        try:
            # Get current data
            time_data, altitude_data = self.data_store.get_data('altitude')
            _, o2_data = self.data_store.get_data('o2_conc')
            _, blp_data = self.data_store.get_data('blp')
            _, spo2_data = self.data_store.get_data('spo2')
            _, pulse_data = self.data_store.get_data('pulse')
            
            # Update plot data
            self.plot_data['time'] = time_data
            self.plot_data['altitude'] = altitude_data
            self.plot_data['o2_conc'] = o2_data
            self.plot_data['blp'] = blp_data
            self.plot_data['spo2'] = spo2_data
            self.plot_data['pulse'] = pulse_data
            
            # Update plot lines
            self.altitude_line.set_data(time_data, altitude_data)
            self.o2_line.set_data(time_data, o2_data)
            self.blp_line.set_data(time_data, blp_data)
            self.spo2_line.set_data(time_data, spo2_data)
            self.pulse_line.set_data(time_data, pulse_data)
            
            # Update plot limits
            time_scale = float(self.time_scale_var.get())
            if time_data:
                self.altitude_ax.set_xlim(max(0, time_data[-1] - time_scale), time_data[-1])
                self.o2_ax.set_xlim(max(0, time_data[-1] - time_scale), time_data[-1])
                self.vitals_ax.set_xlim(max(0, time_data[-1] - time_scale), time_data[-1])
            
            # Redraw canvas
            self.canvas.draw()
            
        except Exception as e:
            log.error(f"Error updating plots: {e}", exc_info=True)
            
        # Schedule next update
        self.root.after(1000, self.update_plots)

    def create_connection_tab(self):
        """Create the connection tab"""
        connection_frame = ModernFrame(self.notebook)
        self.notebook.add(connection_frame, text="Connection")
        
        # Port selection
        port_frame = ModernLabelFrame(connection_frame, text="Port Selection", padding=10)
        port_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var)
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        self.connect_btn = ModernButton(port_frame, text="Connect", command=self.connect_to_device)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = ModernButton(port_frame, text="Disconnect", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ModernButton(port_frame, text="Refresh", command=self.refresh_ports)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Status display
        status_frame = ModernLabelFrame(connection_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Pre-flight checklist
        checklist_frame = ModernLabelFrame(connection_frame, text="Pre-flight Checklist", padding=10)
        checklist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        checklist_btn = ModernButton(checklist_frame, text="Open Checklist", command=lambda: ChecklistWindow(self.root, "Pre-flight Checklist", [
            "Verify ROBD2 system is properly unpacked and installed",
            "Remove and store all packaging materials for future use",
            "Confirm power connection is correct for region (115V or 230V) and securely grounded",
            "Connect air (yellow) and nitrogen (black) at 40-50 PSIG to respective ports",
            "Connect 100% oxygen (green) at 20 PSIG",
            "Connect pilot mask to Breathing Mask Connector on front panel",
            "Ensure pulse oximeter probe is connected",
            "Power on system using power switch",
            "Allow system warm-up time (10 minutes)",
            "Start self-tests by pressing SELFTST key and follow on-screen instructions",
            "Allow system to complete self-tests and auto-calibration (do not use mask during this process)",
            "Record O₂ sensor voltage values at ambient concentration (~21%) and 100% O₂",
            "Manually enter voltage values in ADC 12 table for Bogotá ambient air and 100% O₂",
            "Activate 'Bypass Self-Tests' mode as per manual (Programming and Technical Guide – Rev 8)",
            "Execute Performance Test (Profile #20 – TEST)",
            "Verify O₂ mixtures are within manufacturer's specified ranges (APPENDIX M)"
        ]))
        checklist_btn.pack(pady=5)

    def create_calibration_tab(self):
        """Create the calibration tab"""
        calibration_frame = ModernFrame(self.notebook)
        self.notebook.add(calibration_frame, text="Calibration")
        
        # Warning frame
        warning_frame = ModernLabelFrame(calibration_frame, text="Important Warnings", padding=10)
        warning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        warning_text = """
Before starting calibration recording:
1. Enable administrative credentials on the ROBD2
2. Manually bypass the self-test
3. Run program #20 to start the tests
4. Ensure all gas connections are properly set up
"""
        warning_label = ttk.Label(
            warning_frame,
            text=warning_text,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 10, 'bold')
        )
        warning_label.pack(pady=5)
        
        # Device selection
        device_frame = ModernLabelFrame(calibration_frame, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.device_var = tk.StringVar()
        device_combo = ttk.Combobox(device_frame, textvariable=self.device_var)
        device_combo.pack(side=tk.LEFT, padx=5)
        device_combo['values'] = ['Device 1', 'Device 2', 'Device 3']
        
        # Calibration controls
        control_frame = ModernLabelFrame(calibration_frame, text="Calibration Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_calibration_btn = ModernButton(control_frame, text="Record Calibration", command=self.start_calibration_recording, state=tk.DISABLED)
        self.start_calibration_btn.pack(pady=5)
        
        # Results display
        results_frame = ModernLabelFrame(calibration_frame, text="Calibration Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def start_calibration_recording(self):
        """Start recording calibration data"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        device_id = self.device_var.get()
        if not device_id:
            messagebox.showerror("Error", "Please select a device")
            return
            
        # Show confirmation dialog with warnings
        warning_message = """
Before proceeding, please confirm:
1. Administrative credentials are enabled on the ROBD2
2. Self-test has been manually bypassed
3. Program #20 is running
4. All gas connections are properly set up

Do you want to proceed with recording calibration data?
"""
        if not messagebox.askyesno("Calibration Recording", warning_message):
            return
            
        try:
            # Update UI state
            self.start_calibration_btn.configure(state=tk.DISABLED)
            
            # Create logs directory if it doesn't exist
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Create calibration log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"calibration_{device_id}_{timestamp}.log"
            
            # Configure file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            log.addHandler(file_handler)
            
            # Update status
            self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Starting calibration recording...\n")
            self.results_text.see(tk.END)
            
            # Run calibration recording in a separate thread
            def run_calibration():
                try:
                    monitor = CalibrationMonitor(self.serial_comm.serial_port)
                    monitor.device_id = device_id
                    
                    # Override the data processing to update our data store
                    def process_data(data):
                        try:
                            timestamp = datetime.now()
                            self.data_store.add_data(timestamp, {
                                'altitude': data.get('altitude', 0),
                                'o2_conc': data.get('o2_conc', 0),
                                'blp': data.get('blp', 0),
                                'spo2': data.get('spo2', 0),
                                'pulse': data.get('pulse', 0),
                                'o2_voltage': data.get('o2_voltage', 0),
                                'error_percent': data.get('error_percent', 0)
                            })
                            
                            # Update results display
                            self.root.after(0, lambda: self.results_text.insert(tk.END, 
                                f"{timestamp.strftime('%H:%M:%S')} - Altitude: {data.get('altitude', 0)}ft, "
                                f"O2: {data.get('o2_conc', 0)}%, "
                                f"SpO2: {data.get('spo2', 0)}%\n"))
                            self.root.after(0, lambda: self.results_text.see(tk.END))
                            
                        except Exception as e:
                            log.error(f"Error processing calibration data: {e}", exc_info=True)
                    
                    monitor.process_data = process_data
                    
                    # Start monitoring
                    monitor.start_calibration()
                    
                except Exception as e:
                    log.error(f"Error in calibration thread: {e}", exc_info=True)
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Calibration error: {str(e)}"))
                    self.root.after(0, lambda: self.start_calibration_btn.configure(state=tk.NORMAL))
            
            threading.Thread(target=run_calibration, daemon=True).start()
            
        except Exception as e:
            log.error(f"Error starting calibration recording: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to start calibration recording: {str(e)}")
            self.start_calibration_btn.configure(state=tk.NORMAL)

    def create_performance_tab(self):
        """Create the performance monitoring tab"""
        performance_frame = ModernFrame(self.notebook)
        self.notebook.add(performance_frame, text="Performance")
        
        # Device selection
        device_frame = ModernLabelFrame(performance_frame, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.perf_device_var = tk.StringVar()
        device_combo = ttk.Combobox(device_frame, textvariable=self.perf_device_var)
        device_combo.pack(side=tk.LEFT, padx=5)
        device_combo['values'] = ['Device 1', 'Device 2', 'Device 3']
        
        # Monitoring controls
        control_frame = ModernLabelFrame(performance_frame, text="Monitoring Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_performance_btn = ModernButton(control_frame, text="Start Monitoring", command=self.start_performance_monitoring, state=tk.DISABLED)
        self.start_performance_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_performance_btn = ModernButton(control_frame, text="Stop Monitoring", command=self.stop_performance_monitoring, state=tk.DISABLED)
        self.stop_performance_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ModernButton(control_frame, text="Export Data", command=self.export_data, state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=5)

    def create_training_tab(self):
        """Create the training tab"""
        training_frame = ModernFrame(self.notebook)
        self.notebook.add(training_frame, text="Training")
        
        # Training scripts section
        scripts_frame = ModernLabelFrame(training_frame, text="Training Scripts", padding=10)
        scripts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Fixed Wing Section
        fixed_wing_frame = ModernLabelFrame(scripts_frame, text="Fixed Wing Training", padding=10)
        fixed_wing_frame.pack(fill=tk.X, padx=10, pady=5)
        
        fixed_wing_spanish = ModernButton(
            fixed_wing_frame, 
            text="Fixed Wing (Spanish)", 
            command=lambda: ScriptViewerWindow(
                self.root, 
                "Fixed Wing Training Script (Spanish)", 
                """Libreto para instrucción de ROBD2 – Versión Español 

Bienvenido al entrenamiento de hipoxia normobárica de la Dirección de Medicina Aeroespacial, este entrenamiento está diseñado para que usted reconozca los síntomas de hipoxia y realice los procedimientos de recuperación siguiendo la lista de chequeo PRICE revisada en clase.  Vamos a presentarle un escenario de simulación de vuelo en el PREPAR3D donde usted estará al mando y al control de una aeronave, estará a una altitud de 10.000 ft y yo le daré instrucciones específicas de los procedimientos que usted tiene que realizar en su aeronave. Es importante recordarle que esta no es una evaluación de destrezas de vuelo ni una simulación precisa de una aeronave en particular, sino que el entrenamiento está diseñado para que usted identifique de los efectos de la altitud sobre el rendimiento humano en cabina.  

Como se revisó en clase, deberá reconocer los síntomas de hipoxia y, al aparecer, chequear PRICE y corregirlo con las tres palancas hacia arriba. Siguiendo las instrucciones del instructor. 

Vamos a verificar en el siguiente orden el simulador:

1. Acomodación en la silla (Ajuste abajo a la izquierda, distancia silla y control de mando)
2. Ajustarse cinturón
3. Realizar la adaptación de casco y máscara para que a orden del instructor se la ponga
4. El instructor mostrará los pedales, el bastón de mando o joke, el cuadrante de la potencia
5. Colocar oxímetro de pulso en la mano no dominante

Instrucciones de vuelo:
"TH250, Bogotá radar. Vire por derecha rumbo 130, ascienda y mantenga uno cinco mil pies con un régimen de 500 ft/min."

Colación esperada:
"Bogotá Radar, virando por derecha rumbo 130, ascendiendo y manteniendo uno cinco mil pies a 500 ft/min, TH250."

Segunda instrucción:
"TH250, Bogotá radar. Vire por derecha rumbo 210, ascienda y mantenga uno siete mil pies, a 500 ft/min"

Procedimiento de visión nocturna:
Durante la hipoxia, la disminución de oxígeno afecta significativamente la función de los conos en la retina. En condiciones de hipoxia, la capacidad de los conos para funcionar correctamente se reduce, afectando la sensibilidad a los colores y la agudeza visual.

Instrucciones específicas:
1. Presentar carta AD 2 SKGY - CHIA - FLAMINIO SUAREZ CAMACHO
2. Ejecutar perfil para visión nocturna en ROBD2
3. Identificar aeródromo y señalar montañas entre 8400 y 10200 ft
4. Indicar secuencia de puntos en salida VFR hacia ECHO entre BIMA y TIBITOC
5. Leer contenido de recuadros rojos
6. Ejecutar "Oxygen Dump" y esperar un minuto para recuperación"""
            )
        )
        fixed_wing_spanish.pack(side=tk.LEFT, padx=5, pady=5)
        
        fixed_wing_english = ModernButton(
            fixed_wing_frame, 
            text="Fixed Wing (English)", 
            command=lambda: ScriptViewerWindow(
                self.root, 
                "Fixed Wing Training Script (English)", 
                """Welcome to the normobaric hypoxia training conducted by the Aerospace Medicine Directorate. This training is designed to help you recognize the symptoms of hypoxia and perform recovery procedures using the PRICE checklist reviewed in class. We will present you with a flight simulation scenario in PREPAR3D where you will be in command of an aircraft at an altitude of 10,000 ft.

Simulator verification order:
1. Seating adjustment
2. Fastening seatbelts
3. Helmet and mask adaptation
4. Familiarization with controls (pedals, control stick/yoke, throttle quadrant)

Flight Instructions:
"TH250, Bogotá radar. Turn right heading 130, climb and maintain fifteen thousand feet at a rate of 500 ft/min."

Expected readback:
"Bogotá Radar, turning right heading 130, climbing and maintaining fifteen thousand feet at 500 ft/min, TH250."

Second instruction:
"TH250, Bogotá radar. Turn right heading 210, climb and maintain seventeen thousand feet."

Night Vision Training:
During hypoxia, oxygen reduction significantly affects retinal cone function, responsible for color perception and visual acuity. This is particularly critical during night flights.

Specific Instructions:
1. Present AD 2 SKGY - CHIA - FLAMINIO SUAREZ CAMACHO chart
2. Execute night vision profile in ROBD2
3. Identify aerodrome and mountains between 8400-10200 ft
4. State VFR departure sequence to ECHO between BIMA and TIBITOC
5. Read red box content
6. Execute "Oxygen Dump" with one-minute recovery period"""
            )
        )
        fixed_wing_english.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Rotary Wing Section
        rotary_wing_frame = ModernLabelFrame(scripts_frame, text="Rotary Wing Training", padding=10)
        rotary_wing_frame.pack(fill=tk.X, padx=10, pady=5)
        
        rotary_wing_spanish = ModernButton(
            rotary_wing_frame, 
            text="Rotary Wing (Spanish)", 
            command=lambda: ScriptViewerWindow(
                self.root, 
                "Rotary Wing Training Script (Spanish)", 
                """Bienvenido al entrenamiento de hipoxia normobárica de la Dirección de Medicina Aeroespacial. Este entrenamiento está diseñado para que usted reconozca los síntomas de hipoxia y realice los procedimientos de recuperación siguiendo la lista de chequeo PRICE.

Verificación del simulador:
1. Acomodación en la silla
2. Ajustar el cinturón
3. Realizar la adaptación de casco y máscara
4. El instructor mostrará los controles básicos

Instrucciones de vuelo:
"UH180, Bogotá radar. Vire por derecha rumbo 130, ascienda y mantenga uno tres mil pies."

Colación esperada:
"Bogotá Radar, virando por derecha rumbo 130, asciendo y manteniendo uno tres mil pies, UH180."

Segunda instrucción:
"UH180, Bogotá radar. Vire derecha rumbo 210, ascienda y mantenga uno siete mil pies"

En caso de emergencia:
El piloto debe comunicarse con CTA para declarar la emergencia y solicitar descenso para uno cero mil pies.

Respuesta CTA:
"UH180, Bogotá Radar, autorizado descenso a uno cero mil pies"

Recordatorio importante:
Al primer síntoma de hipoxia, hay que recuperarse accionando el regulador con las tres palancas hacia arriba."""
            )
        )
        rotary_wing_spanish.pack(side=tk.LEFT, padx=5, pady=5)
        
        rotary_wing_english = ModernButton(
            rotary_wing_frame, 
            text="Rotary Wing (English)", 
            command=lambda: ScriptViewerWindow(
                self.root, 
                "Rotary Wing Training Script (English)", 
                """Welcome to the normobaric hypoxia training conducted by the Aerospace Medicine Directorate. This training is designed to help you recognize hypoxia symptoms and perform recovery procedures using the PRICE checklist.

Simulator verification:
1. Seating adjustment
2. Fastening seatbelts
3. Helmet and mask adaptation
4. Basic controls familiarization

Flight Instructions:
"UH180, Bogotá radar. Turn right heading 130, climb and maintain thirteen thousand feet."

Expected readback:
"Bogotá Radar, turning right heading 130, climbing and maintaining thirteen thousand feet, UH180."

Second instruction:
"UH180, Bogotá radar. Turn right heading 210, climb and maintain seventeen thousand feet."

Emergency Procedure:
The pilot must communicate with ATC to declare emergency and request descent to ten thousand feet.

ATC Response:
"UH180, Bogotá Radar, cleared to descend to ten thousand feet."

Important Reminder:
Upon first symptom of hypoxia, recovery must be initiated by operating the regulator with all three levers up."""
            )
        )
        rotary_wing_english.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Instructions frame
        instructions_frame = ModernLabelFrame(training_frame, text="Instructions", padding=10)
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = """
Select the appropriate training script based on aircraft type and language preference.
Each script contains:
• Detailed setup instructions
• Flight commands and expected responses
• Emergency procedures
• Night vision training procedures (where applicable)
• Important reminders for hypoxia symptoms
"""
        instructions_label = ttk.Label(
            instructions_frame,
            text=instructions_text,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 10)
        )
        instructions_label.pack(pady=5)

    def create_dashboard_tab(self):
        """Create the dashboard tab"""
        dashboard_frame = ModernFrame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Time scale control
        scale_frame = ModernLabelFrame(dashboard_frame, text="Time Scale", padding=10)
        scale_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.time_scale_var = tk.StringVar(value="60")
        ttk.Label(scale_frame, text="Time window (seconds):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(scale_frame, textvariable=self.time_scale_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Create plots
        plot_frame = ModernLabelFrame(dashboard_frame, text="Real-time Data", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create figure with subplots
        self.fig = Figure(figsize=(10, 8))
        self.altitude_ax = self.fig.add_subplot(311)
        self.o2_ax = self.fig.add_subplot(312)
        self.vitals_ax = self.fig.add_subplot(313)
        
        # Initialize plot data
        self.plot_data = {
            'time': [], 'altitude': [], 'o2_conc': [], 'blp': [], 'spo2': [], 'pulse': []
        }
        
        # Create plot lines
        self.altitude_line, = self.altitude_ax.plot([], [], label='Altitude')
        self.o2_line, = self.o2_ax.plot([], [], label='O2 Concentration')
        self.blp_line, = self.vitals_ax.plot([], [], label='BLP')
        self.spo2_line, = self.vitals_ax.plot([], [], label='SpO2')
        self.pulse_line, = self.vitals_ax.plot([], [], label='Pulse')
        
        # Configure plots
        self.altitude_ax.set_title('Altitude (ft)')
        self.o2_ax.set_title('O2 Concentration (%)')
        self.vitals_ax.set_title('Vitals')
        
        for ax in [self.altitude_ax, self.o2_ax, self.vitals_ax]:
            ax.grid(True)
            ax.legend()
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_diagnostics_tab(self):
        """Create the diagnostics tab"""
        diagnostics_frame = ModernFrame(self.notebook)
        self.notebook.add(diagnostics_frame, text="Diagnostics")
        
        # Command input
        command_frame = ModernLabelFrame(diagnostics_frame, text="Send Command", padding=10)
        command_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(command_frame, textvariable=self.command_var)
        command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        send_btn = ModernButton(command_frame, text="Send", command=lambda: self.send_diagnostic_command(self.command_var.get()))
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Response display
        response_frame = ModernLabelFrame(diagnostics_frame, text="Device Response", padding=10)
        response_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.response_text = tk.Text(response_frame, height=10, wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Start polling for responses
        self.poll_responses()

    def create_programming_tab(self):
        """Create the programming tab"""
        programming_frame = ModernFrame(self.notebook)
        self.notebook.add(programming_frame, text="Programming")
        
        # Program configuration
        config_frame = ModernLabelFrame(programming_frame, text="Program Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add programming controls here
        ttk.Label(config_frame, text="Programming interface coming soon...").pack(pady=10)

    def create_logging_tab(self):
        """Create the logging tab"""
        logging_frame = ModernFrame(self.notebook)
        self.notebook.add(logging_frame, text="Logging")
        
        # Flight ID input
        id_frame = ModernLabelFrame(logging_frame, text="Flight Information", padding=10)
        id_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(id_frame, text="Flight ID:").pack(side=tk.LEFT, padx=5)
        self.flight_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.flight_id_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Logging controls
        control_frame = ModernLabelFrame(logging_frame, text="Logging Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_logging_btn = ModernButton(control_frame, text="Start Logging", command=self.start_logging, state=tk.DISABLED)
        self.start_logging_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_logging_btn = ModernButton(control_frame, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_logging_btn.pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_frame = ModernLabelFrame(logging_frame, text="Log Data", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

def main():
    try:
        root = tk.Tk()
        app = ROBD2GUI(root)
        
        def on_closing():
            """Handle application closing"""
            if hasattr(app, 'serial_comm'):
                app.serial_comm.disconnect()
            if hasattr(app, 'performance_monitor'):
                app.performance_monitor.stop_monitoring()
            if hasattr(app, 'data_logger'):
                app.data_logger.stop_logging()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        log.error(f"Application error: {e}", exc_info=True)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 