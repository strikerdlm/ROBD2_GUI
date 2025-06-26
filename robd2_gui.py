import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import logging
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import csv
import time
import threading

from data_store import DataStore
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame
from windows import ChecklistWindow, ScriptViewerWindow, LoadingIndicator
from serial_comm import SerialCommunicator
from calibration_data import CalibrationMonitor
from Performance import PerformanceMonitor
from COM_serial import DataLogger
from program_manager import ProgramManager
from performance_gui import PerformanceTab
from gas_calculator_tab import GasCalculatorTab

# Configure standard logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger("robd2_gui")

# Ensure log messages also appear in the terminal in real time
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
if not any(isinstance(h, logging.StreamHandler) for h in log.handlers):
    log.addHandler(console_handler)

class ROBD2GUI:
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("ROBD2 Diagnostic Interface")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize scrolling management
        self.active_scrollables = []
        
        # Initialize data store
        self.data_store = DataStore()
        
        # Initialize serial communicator
        self.serial_comm = SerialCommunicator()
        
        # Create the main frame
        main_frame = ModernFrame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the menu bar
        self.create_menu_bar()
        
        # Create the status bar
        status_frame = ttk.Frame(main_frame, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_bar = ttk.Label(status_frame, text="Not connected", anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.LEFT, padx=5)
        
        # Create tabs
        self.create_gas_calculator_tab()  # Add the gas calculator tab first
        self.create_connection_tab()
        self.create_calibration_tab()
        self.create_performance_tab()
        self.create_training_tab()
        self.create_dashboard_tab()
        self.create_diagnostics_tab()
        self.create_programming_tab()
        self.create_logging_tab()
        
        # Add tab selection callback to handle starting/stopping data collection
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Setup keyboard shortcuts
        self.add_keyboard_shortcuts()
        
        # Flag for plotting
        self.plotting_active = False
        
        # Track the after event ID
        self.poll_after_id = None
        
    def enable_scrolling(self, widget):
        """Enable mouse wheel scrolling for a widget"""
        def _on_mousewheel(event):
            try:
                if widget.winfo_exists():
                    if sys.platform.startswith('win'):
                        widget.yview_scroll(int(-1*(event.delta/120)), "units")
                    else:
                        if event.num == 4:
                            widget.yview_scroll(-1, "units")
                        elif event.num == 5:
                            widget.yview_scroll(1, "units")
            except tk.TclError:
                pass

        if sys.platform.startswith('win'):
            widget.bind_all("<MouseWheel>", _on_mousewheel)
        else:
            widget.bind_all("<Button-4>", _on_mousewheel)
            widget.bind_all("<Button-5>", _on_mousewheel)
            
        # Store the widget and its bindings for cleanup
        self.active_scrollables.append({
            'widget': widget,
            'bindings': [
                ("<MouseWheel>", _on_mousewheel) if sys.platform.startswith('win') 
                else ("<Button-4>", _on_mousewheel),
                ("<Button-5>", _on_mousewheel)
            ]
        })

    def cleanup_scrolling(self):
        """Clean up all mouse wheel bindings"""
        try:
            for scrollable in self.active_scrollables:
                if isinstance(scrollable, dict):
                    # Handle dictionary format
                    widget = scrollable.get('widget')
                    bindings = scrollable.get('bindings', [])
                    if widget:
                        for event, _ in bindings:
                            try:
                                widget.unbind_all(event)
                            except tk.TclError:
                                pass
                elif isinstance(scrollable, tuple):
                    # Handle tuple format
                    event, _ = scrollable
                    try:
                        self.unbind_all(event)
                    except tk.TclError:
                        pass
            self.active_scrollables.clear()
        except Exception as e:
            log.error(f"Error cleaning up scrolling: {e}")

    def create_scrollable_frame(self, parent, **kwargs):
        """Create a scrollable frame and return both the canvas and the frame"""
        canvas = tk.Canvas(parent, **kwargs)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernFrame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        self.enable_scrolling(canvas)
        
        return canvas, scrollable_frame

    def create_gas_calculator_tab(self):
        """Create the gas calculator tab"""
        gas_calculator_tab = GasCalculatorTab(self.notebook)
        self.notebook.add(gas_calculator_tab, text="Gas Calculator")
        
        # Add the gas calculator's scrollable widgets to our tracking
        if hasattr(gas_calculator_tab, 'active_scrollables'):
            self.active_scrollables.extend(gas_calculator_tab.active_scrollables)
            
        # Bind cleanup to tab destruction
        gas_calculator_tab.bind("<Destroy>", lambda e: self.cleanup_scrolling())
        
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
                self.start_logging_btn.configure(state=tk.NORMAL)
                
                # Update status
                self.status_bar.configure(text=f"Connected to {port}")
                self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Connected to {port}\n")
                
                # Check if dashboard tab is visible and start data collection
                if self.notebook.tab(self.notebook.select(), "text") == "Dashboard":
                    self.start_data_collection()
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
            self.start_logging_btn.configure(state=tk.DISABLED)
            
            # Update status
            self.status_bar.configure(text="Disconnected")
            self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Disconnected\n")
            
            # Stop data collection if active
            self.plotting_active = False
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
            
        # Schedule the next poll and store the after ID (reduced frequency to 500ms)
        self.poll_after_id = self.root.after(500, self.poll_responses)
        
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
            text="Advanced Control and Analysis Interface for ROBD2 Devices",
            font=('Helvetica', 12)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Version with custom styling
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        version_label = ttk.Label(
            version_frame,
            text="Version 2.0.0",
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

Copyright © 2024 Diego Malpica MD. All rights reserved.

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

This software is designed for use in controlled environments under the supervision of trained medical professionals or experts in ROBD devices for aerospace physiology training. It includes advanced features for gas calculations, performance monitoring, and training management.
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
• Advanced gas calculator with physiological parameters, consumption analysis, and capacity planning
• Real-time data visualization with customizable time scales
• Comprehensive data logging and export capabilities
• Device calibration tools with automated procedures
• Performance monitoring with real-time graphs
• Training session management and checklists
• Diagnostic command interface with error handling
• Modern, intuitive user interface with dark mode support
• Automatic data validation and range checking
• CSV data export with timestamps
• Multi-platform support (Windows, Linux)
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
• Windows 10/11 or Linux
• Required Python packages:
  - pyserial >= 3.5
  - matplotlib >= 3.7
  - numpy >= 1.24
  - tkinter (included with Python)
  - pillow >= 10.0
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
                self.altitude_ax.set_xlim(max(0, time_data[-1] - time_scale), max(time_data[-1], time_scale))
                self.o2_ax.set_xlim(max(0, time_data[-1] - time_scale), max(time_data[-1], time_scale))
                self.vitals_ax.set_xlim(max(0, time_data[-1] - time_scale), max(time_data[-1], time_scale))
                
                # Update y-axis limits based on data
                if altitude_data:
                    self.altitude_ax.set_ylim(0, max(35000, max(altitude_data) * 1.1))
                if o2_data:
                    self.o2_ax.set_ylim(0, max(30, max(o2_data) * 1.1))
                if spo2_data:
                    max_vitals = max(max(spo2_data) if spo2_data else 100, 
                                   max(pulse_data) if pulse_data else 100,
                                   max(blp_data) if blp_data else 10)
                    self.vitals_ax.set_ylim(0, max_vitals * 1.1)
            
            # Redraw canvas
            self.canvas.draw()
            
        except Exception as e:
            log.error(f"Error updating plots: {e}", exc_info=True)

    def create_connection_tab(self):
        """Create the connection tab"""
        connection_frame = ModernFrame(self.notebook)
        self.notebook.add(connection_frame, text="Connection")
        
        # Create scrollable frame
        canvas, scrollable_frame = self.create_scrollable_frame(connection_frame)
        
        # Port selection
        port_frame = ModernLabelFrame(scrollable_frame, text="Port Selection", padding=10)
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
        status_frame = ModernLabelFrame(scrollable_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Enable scrolling for status text
        status_scroll = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        status_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.configure(yscrollcommand=status_scroll.set)
        
        # Pre-flight checklist
        checklist_frame = ModernLabelFrame(scrollable_frame, text="Pretraining Setup", padding=10)
        checklist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        checklist_btn = ModernButton(checklist_frame, text="Open Checklist", command=lambda: ChecklistWindow(self.root, "Before Start (Daily) Checklist", [
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
        """Create the calibration tab with self-calibration functionality"""
        calibration_frame = ModernFrame(self.notebook)
        self.notebook.add(calibration_frame, text="Calibration")
        
        # Create a horizontal paned window for main layout
        main_paned = ttk.PanedWindow(calibration_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - Controls and inputs
        left_frame = ModernFrame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # Right side - Calibration results
        right_frame = ModernFrame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Create scrollable frame for left side
        canvas, scrollable_frame = self.create_scrollable_frame(left_frame)
        
        # Warning frame
        warning_frame = ModernLabelFrame(scrollable_frame, text="Important Warnings", padding=10)
        warning_frame.pack(fill=tk.X, padx=5, pady=5)
        
        warning_text = """
Before starting calibration:
1. Enable administrative credentials on the ROBD2
2. Manually bypass the self-test if required
3. Ensure all gas connections are properly set up
4. For manual calibration, run program #20 to start the tests
"""
        warning_label = ttk.Label(
            warning_frame,
            text=warning_text,
            wraplength=500,
            justify=tk.LEFT,
            font=('Helvetica', 10, 'bold')
        )
        warning_label.pack(pady=5)
        
        # Status indicator frame
        self.calibration_status_frame = ModernLabelFrame(scrollable_frame, text="Calibration Status", padding=10)
        self.calibration_status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_var = tk.StringVar(value="Ready for calibration")
        self.status_label = ttk.Label(
            self.calibration_status_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10, 'bold'),
            foreground='blue'
        )
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.calibration_progress = ttk.Progressbar(
            self.calibration_status_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate'
        )
        self.calibration_progress.pack(pady=5, fill=tk.X)
        
        # Device selection
        device_frame = ModernLabelFrame(scrollable_frame, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(device_frame, text="ROBD2 Device ID:").pack(side=tk.LEFT, padx=5)
        self.device_var = tk.StringVar(value="9515")
        device_combo = ttk.Combobox(device_frame, textvariable=self.device_var, width=10)
        device_combo.pack(side=tk.LEFT, padx=5)
        device_combo['values'] = ['9515', '9516', '9471']
        
        # Self-calibration section
        self_cal_frame = ModernLabelFrame(scrollable_frame, text="Self-Calibration", padding=10)
        self_cal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Room air and 100% O2 values display
        values_frame = ttk.Frame(self_cal_frame)
        values_frame.pack(fill=tk.X, pady=5)
        
        # Room air calibration
        room_air_frame = ttk.LabelFrame(values_frame, text="Room Air (21% O2)")
        room_air_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(room_air_frame, text="ADC Voltage (V):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.room_air_voltage_var = tk.StringVar(value="---")
        ttk.Label(room_air_frame, textvariable=self.room_air_voltage_var).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(room_air_frame, text="O2 Concentration (%):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.room_air_o2_var = tk.StringVar(value="---")
        ttk.Label(room_air_frame, textvariable=self.room_air_o2_var).grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        self.record_room_air_btn = ModernButton(
            room_air_frame, 
            text="Record Room Air", 
            command=self.record_room_air_calibration,
            width=18
        )
        self.record_room_air_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # 100% O2 calibration
        pure_o2_frame = ttk.LabelFrame(values_frame, text="100% O2")
        pure_o2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(pure_o2_frame, text="ADC Voltage (V):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.pure_o2_voltage_var = tk.StringVar(value="---")
        ttk.Label(pure_o2_frame, textvariable=self.pure_o2_voltage_var).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(pure_o2_frame, text="O2 Concentration (%):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.pure_o2_o2_var = tk.StringVar(value="---")
        ttk.Label(pure_o2_frame, textvariable=self.pure_o2_o2_var).grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        self.record_pure_o2_btn = ModernButton(
            pure_o2_frame, 
            text="Record 100% O2", 
            command=self.record_pure_o2_calibration,
            width=18
        )
        self.record_pure_o2_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Calibration controls
        control_frame = ttk.Frame(self_cal_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Save calibration button
        self.save_calibration_btn = ModernButton(
            control_frame, 
            text="Save Calibration Values", 
            command=self.save_calibration_values,
            width=22,
            state=tk.DISABLED
        )
        self.save_calibration_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear calibration button
        self.clear_calibration_btn = ModernButton(
            control_frame, 
            text="Clear Calibration Values", 
            command=self.clear_calibration_values,
            width=22
        )
        self.clear_calibration_btn.pack(side=tk.LEFT, padx=5)
        
        # Manual Calibration section
        manual_cal_frame = ModernLabelFrame(scrollable_frame, text="Manual Calibration Recording", padding=10)
        manual_cal_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_calibration_btn = ModernButton(
            manual_cal_frame, 
            text="Record Full Calibration Sequence", 
            command=self.start_calibration_recording, 
            state=tk.DISABLED
        )
        self.start_calibration_btn.pack(pady=5)
        
        # Results display (moved to right_frame)
        results_frame = ModernLabelFrame(right_frame, text="Calibration Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add scrollbar to results text
        results_scroll = ttk.Scrollbar(results_frame)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD, yscrollcommand=results_scroll.set)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        results_scroll.config(command=self.results_text.yview)
        
        # Store calibration data for sharing between methods
        self.calibration_data = {
            'room_air': {
                'o2_values': [],
                'voltage_values': []
            },
            'pure_o2': {
                'o2_values': [],
                'voltage_values': []
            }
        }
        
        # Initialize calibration in progress flag
        self.calibration_in_progress = False
        
    def update_calibration_status(self, message, color='blue', progress=None):
        """Update the calibration status indicator"""
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        
        if progress is not None:
            self.calibration_progress['value'] = progress
        
        self.root.update_idletasks()
        
    def update_calibration_ui_state(self, in_progress=False):
        """Update UI state based on calibration progress"""
        self.calibration_in_progress = in_progress
        
        # Set button states based on calibration progress
        state = tk.DISABLED if in_progress else tk.NORMAL
        self.record_room_air_btn.config(state=state)
        self.record_pure_o2_btn.config(state=state)
        self.clear_calibration_btn.config(state=state)
        
        # The save button should only be enabled if both values are recorded and not in progress
        save_state = tk.NORMAL if (
            not in_progress and 
            self.room_air_voltage_var.get() != "---" and 
            self.pure_o2_voltage_var.get() != "---"
        ) else tk.DISABLED
        self.save_calibration_btn.config(state=save_state)
        
        # Start calibration button state
        self.start_calibration_btn.config(state=state if self.serial_comm.is_connected else tk.DISABLED)
        
        # Update progress bar
        if in_progress:
            self.calibration_progress.config(mode='indeterminate')
            self.calibration_progress.start(10)
        else:
            self.calibration_progress.config(mode='determinate')
            self.calibration_progress.stop()
            self.calibration_progress['value'] = 0 if in_progress is False else 100
        
    def record_room_air_calibration(self):
        """Record room air (21% O2) calibration values"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        try:
            # Update UI state
            self.update_calibration_status("Recording room air values...", "blue")
            self.update_calibration_ui_state(in_progress=True)
            
            # Collect multiple samples to ensure stability
            o2_values = []
            voltage_values = []
            
            # Add header to results
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.results_text.insert(tk.END, f"\n", 'header')
            self.results_text.insert(tk.END, f"=== Room Air Calibration Started at {timestamp} ===\n", 'header')
            
            for i in range(5):
                # Update progress
                self.calibration_progress['value'] = (i + 1) * 20
                self.root.update_idletasks()
                
                try:
                    # Get O2 concentration
                    success, _ = self.serial_comm.send_command("GET RUN O2CONC")
                    if not success:
                        raise Exception("Failed to send O2CONC command")
                    
                    time.sleep(0.1)  # Wait for response
                    o2_response = self.serial_comm.get_response()
                    if not o2_response:
                        raise Exception("No O2 concentration response")
                    
                    o2_conc = float(o2_response.strip())
                    o2_values.append(o2_conc)
                    
                    # Get ADC voltage
                    success, _ = self.serial_comm.send_command("GET ADC 12")
                    if not success:
                        raise Exception("Failed to send ADC command")
                    
                    time.sleep(0.1)  # Wait for response
                    voltage_response = self.serial_comm.get_response()
                    if not voltage_response:
                        raise Exception("No ADC voltage response")
                    
                    voltage = float(voltage_response.strip())
                    voltage_values.append(voltage)
                    
                    # Add sample data with timestamp
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    self.results_text.insert(tk.END, f"Sample {i+1}: ", 'info')
                    self.results_text.insert(tk.END, f"O2={o2_conc:.2f}%, Voltage={voltage:.3f}V\n")
                    self.results_text.see(tk.END)
                    time.sleep(0.5)
                except Exception as e:
                    log.error(f"Error collecting sample {i+1}: {e}")
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    self.results_text.insert(tk.END, f"Error in sample {i+1}: {str(e)}\n", 'error')
                    self.results_text.see(tk.END)
                    
            # Calculate averages if we have data
            if o2_values and voltage_values:
                avg_o2 = sum(o2_values) / len(o2_values)
                avg_voltage = sum(voltage_values) / len(voltage_values)
                
                # Update display
                self.room_air_o2_var.set(f"{avg_o2:.2f}")
                self.room_air_voltage_var.set(f"{avg_voltage:.3f}")
                
                # Store in shared data structure
                self.calibration_data['room_air']['o2_values'] = o2_values
                self.calibration_data['room_air']['voltage_values'] = voltage_values
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.results_text.insert(tk.END, f"\n[{timestamp}] ", 'timestamp')
                self.results_text.insert(tk.END, "Room air calibration completed successfully\n", 'success')
                self.results_text.insert(tk.END, f"Average O2: {avg_o2:.2f}%\n")
                self.results_text.insert(tk.END, f"Average Voltage: {avg_voltage:.3f}V\n")
                self.results_text.see(tk.END)
                
                # Update status to success
                self.update_calibration_status("Room air calibration complete ✓", "green", 100)
            else:
                self.update_calibration_status("Room air calibration failed", "red", 0)
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                self.results_text.insert(tk.END, "Error: Failed to collect valid data\n", 'error')
                self.results_text.see(tk.END)
                
        except Exception as e:
            log.error(f"Error in room air calibration: {e}", exc_info=True)
            self.update_calibration_status(f"Error: {str(e)}", "red", 0)
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.results_text.insert(tk.END, f"Error: {str(e)}\n", 'error')
            self.results_text.see(tk.END)
            
        finally:
            # Restore UI state
            self.update_calibration_ui_state(in_progress=False)
            
    def record_pure_o2_calibration(self):
        """Record 100% O2 calibration values"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        try:
            # Update UI state
            self.update_calibration_status("Recording 100% O2 values...", "blue")
            self.update_calibration_ui_state(in_progress=True)
            
            # Collect multiple samples to ensure stability
            o2_values = []
            voltage_values = []
            
            # Add header to results
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.results_text.insert(tk.END, f"\n", 'header')
            self.results_text.insert(tk.END, f"=== 100% O2 Calibration Started at {timestamp} ===\n", 'header')
            
            for i in range(5):
                # Update progress
                self.calibration_progress['value'] = (i + 1) * 20
                self.root.update_idletasks()
                
                try:
                    # Get O2 concentration
                    success, _ = self.serial_comm.send_command("GET RUN O2CONC")
                    if not success:
                        raise Exception("Failed to send O2CONC command")
                    
                    time.sleep(0.1)  # Wait for response
                    o2_response = self.serial_comm.get_response()
                    if not o2_response:
                        raise Exception("No O2 concentration response")
                    
                    o2_conc = float(o2_response.strip())
                    o2_values.append(o2_conc)
                    
                    # Get ADC voltage
                    success, _ = self.serial_comm.send_command("GET ADC 12")
                    if not success:
                        raise Exception("Failed to send ADC command")
                    
                    time.sleep(0.1)  # Wait for response
                    voltage_response = self.serial_comm.get_response()
                    if not voltage_response:
                        raise Exception("No ADC voltage response")
                    
                    voltage = float(voltage_response.strip())
                    voltage_values.append(voltage)
                    
                    # Add sample data with timestamp
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    self.results_text.insert(tk.END, f"Sample {i+1}: ", 'info')
                    self.results_text.insert(tk.END, f"O2={o2_conc:.2f}%, Voltage={voltage:.3f}V\n")
                    self.results_text.see(tk.END)
                    time.sleep(0.5)
                except Exception as e:
                    log.error(f"Error collecting sample {i+1}: {e}")
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    self.results_text.insert(tk.END, f"Error in sample {i+1}: {str(e)}\n", 'error')
                    self.results_text.see(tk.END)
                    
            # Calculate averages if we have data
            if o2_values and voltage_values:
                avg_o2 = sum(o2_values) / len(o2_values)
                avg_voltage = sum(voltage_values) / len(voltage_values)
                
                # Update display
                self.pure_o2_o2_var.set(f"{avg_o2:.2f}")
                self.pure_o2_voltage_var.set(f"{avg_voltage:.3f}")
                
                # Store in shared data structure
                self.calibration_data['pure_o2']['o2_values'] = o2_values
                self.calibration_data['pure_o2']['voltage_values'] = voltage_values
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.results_text.insert(tk.END, f"\n[{timestamp}] ", 'timestamp')
                self.results_text.insert(tk.END, "100% O2 calibration completed successfully\n", 'success')
                self.results_text.insert(tk.END, f"Average O2: {avg_o2:.2f}%\n")
                self.results_text.insert(tk.END, f"Average Voltage: {avg_voltage:.3f}V\n")
                self.results_text.see(tk.END)
                
                # Update status to success
                self.update_calibration_status("100% O2 calibration complete ✓", "green", 100)
            else:
                self.update_calibration_status("100% O2 calibration failed", "red", 0)
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                self.results_text.insert(tk.END, "Error: Failed to collect valid data\n", 'error')
                self.results_text.see(tk.END)
                
        except Exception as e:
            log.error(f"Error in 100% O2 calibration: {e}", exc_info=True)
            self.update_calibration_status(f"Error: {str(e)}", "red", 0)
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.results_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.results_text.insert(tk.END, f"Error: {str(e)}\n", 'error')
            self.results_text.see(tk.END)
            
        finally:
            # Restore UI state
            self.update_calibration_ui_state(in_progress=False)
            
    def save_calibration_values(self):
        """Save calibration values to the ROBD2 device and to a file"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        try:
            # Update UI state
            self.update_calibration_status("Saving calibration values...", "blue")
            self.update_calibration_ui_state(in_progress=True)
            
            device_id = self.device_var.get()
            room_air_voltage = float(self.room_air_voltage_var.get())
            pure_o2_voltage = float(self.pure_o2_voltage_var.get())
            
            # Send calibration values to the device
            # Note: This is where you would normally send the calibration commands
            # to the ROBD2 device. Since the exact command format isn't provided,
            # we're just simulating this with a message
            
            self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Saving calibration values to ROBD2-{device_id}...\n")
            self.results_text.see(tk.END)
            
            # Create logs directory if it doesn't exist
            logs_dir = Path("calibration_logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Create calibration log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"ROBD2_{device_id}_{timestamp}_cal.csv"
            
            # Get device info
            device_info = "Unknown Device"
            try:
                success, _ = self.serial_comm.send_command("GET INFO")
                if success:
                    time.sleep(0.1)  # Wait for response
                    info_response = self.serial_comm.get_response()
                    if info_response:
                        device_info = info_response.strip()
            except Exception as e:
                log.warning(f"Could not get device info: {e}")
            
            # Update progress
            self.calibration_progress['value'] = 50
            self.root.update_idletasks()
            
            # Write calibration data to file
            with open(log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Device ID", "Device Info", "Timestamp", "Parameter", "Value"])
                writer.writerow([device_id, device_info, timestamp, "Room Air Voltage", f"{room_air_voltage:.3f}"])
                writer.writerow([device_id, device_info, timestamp, "100% O2 Voltage", f"{pure_o2_voltage:.3f}"])
                writer.writerow([device_id, device_info, timestamp, "Room Air O2", self.room_air_o2_var.get()])
                writer.writerow([device_id, device_info, timestamp, "100% O2", self.pure_o2_o2_var.get()])
                
                # Add individual sample data
                writer.writerow([])
                writer.writerow(["Detailed Samples"])
                writer.writerow(["Type", "Sample #", "O2 Concentration", "ADC Voltage"])
                
                # Write room air samples
                for i, (o2, voltage) in enumerate(zip(
                    self.calibration_data['room_air']['o2_values'],
                    self.calibration_data['room_air']['voltage_values']
                )):
                    writer.writerow(["Room Air", i+1, f"{o2:.2f}", f"{voltage:.3f}"])
                    
                # Write 100% O2 samples
                for i, (o2, voltage) in enumerate(zip(
                    self.calibration_data['pure_o2']['o2_values'],
                    self.calibration_data['pure_o2']['voltage_values']
                )):
                    writer.writerow(["100% O2", i+1, f"{o2:.2f}", f"{voltage:.3f}"])
            
            # Update progress
            self.calibration_progress['value'] = 100
            self.root.update_idletasks()
            
            # Display success message
            msg = f"Calibration values saved to {log_file}"
            self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {msg}\n")
            self.results_text.see(tk.END)
            
            # Show success dialog
            messagebox.showinfo("Calibration Saved", f"Calibration values have been successfully saved.\n\nFile: {log_file}")
            
            # Update status
            self.update_calibration_status("Calibration successfully saved ✓", "green", 100)
            
        except Exception as e:
            log.error(f"Error saving calibration: {e}", exc_info=True)
            self.update_calibration_status(f"Error saving calibration: {str(e)}", "red", 0)
            self.results_text.insert(tk.END, f"Error saving calibration: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to save calibration: {str(e)}")
            
        finally:
            # Restore UI state
            self.update_calibration_ui_state(in_progress=False)
            
    def clear_calibration_values(self):
        """Clear the recorded calibration values"""
        # Clear display values
        self.room_air_voltage_var.set("---")
        self.room_air_o2_var.set("---")
        self.pure_o2_voltage_var.set("---")
        self.pure_o2_o2_var.set("---")
        
        # Clear stored data
        self.calibration_data = {
            'room_air': {
                'o2_values': [],
                'voltage_values': []
            },
            'pure_o2': {
                'o2_values': [],
                'voltage_values': []
            }
        }
        
        # Update button states
        self.save_calibration_btn.config(state=tk.DISABLED)
        
        # Update status
        self.update_calibration_status("Calibration values cleared", "blue", 0)
        self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Calibration values cleared\n")
        self.results_text.see(tk.END)
        
    def start_calibration_recording(self):
        """Start recording full calibration sequence data"""
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
            self.update_calibration_status("Starting full calibration sequence...", "blue")
            self.update_calibration_ui_state(in_progress=True)
            
            # Disable all buttons during full calibration
            self.record_room_air_btn.config(state=tk.DISABLED)
            self.record_pure_o2_btn.config(state=tk.DISABLED)
            self.save_calibration_btn.config(state=tk.DISABLED)
            self.clear_calibration_btn.config(state=tk.DISABLED)
            
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
                            
                            # Update progress
                            progress_value = min(100, int(self.calibration_progress['value'] + 1))
                            self.root.after(0, lambda: self.calibration_progress.config(value=progress_value))
                            
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
                    
                    # Update UI when done
                    self.root.after(0, lambda: self.update_calibration_status("Full calibration complete ✓", "green", 100))
                    self.root.after(0, lambda: self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Full calibration sequence completed\n"))
                    self.root.after(0, lambda: self.results_text.see(tk.END))
                    self.root.after(0, lambda: messagebox.showinfo("Calibration Complete", f"Full calibration sequence completed successfully.\n\nLog file: {log_file}"))
                    
                except Exception as e:
                    log.error(f"Error in calibration thread: {e}", exc_info=True)
                    self.root.after(0, lambda: self.update_calibration_status(f"Calibration error: {str(e)}", "red", 0))
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Calibration error: {str(e)}"))
                
                finally:
                    # Clean up
                    log.removeHandler(file_handler)
                    file_handler.close()
                    
                    # Restore UI state
                    self.root.after(0, lambda: self.update_calibration_ui_state(in_progress=False))
            
            threading.Thread(target=run_calibration, daemon=True).start()
            
        except Exception as e:
            log.error(f"Error starting calibration recording: {e}", exc_info=True)
            self.update_calibration_status(f"Error: {str(e)}", "red", 0)
            messagebox.showerror("Error", f"Failed to start calibration recording: {str(e)}")
            
            # Restore UI state
            self.update_calibration_ui_state(in_progress=False)

    def create_performance_tab(self):
        """Create the performance tab"""
        performance_tab = PerformanceTab(self.notebook, self.serial_comm)
        self.notebook.add(performance_tab, text="Performance")

    def create_training_tab(self):
        """Create the training tab with simulation, checklists, and ROBD2 commands"""
        training_frame = ModernFrame(self.notebook)
        self.notebook.add(training_frame, text="Training")
        
        # Create a horizontal paned window
        paned = ttk.PanedWindow(training_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - ROBD2 Commands
        command_frame = ModernLabelFrame(paned, text="ROBD2 Commands")
        paned.add(command_frame, weight=1)
        
        # Command categories
        status_frame = ModernLabelFrame(command_frame, text="Status Commands")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Status commands
        status_buttons = [
            ("O2 Concentration", "GET RUN O2CONC"),
            ("Breathing Loop Pressure", "GET RUN BLPRESS"),
            ("SpO2 Reading", "GET RUN SPO2"),
            ("Pulse Reading", "GET RUN PULSE"),
            ("Current Altitude", "GET RUN ALT"),
            ("Final Altitude", "GET RUN FINALALT"),
            ("Elapsed Time", "GET RUN ELTIME"),
            ("Remaining Time", "GET RUN REMTIME"),
            ("All Run Data", "GET RUN ALL"),
            ("System Info", "GET INFO"),
            ("O2 Source Status", "GET O2 STATUS"),
            ("System Status", "GET STATUS")
        ]
        
        for i, (label, cmd) in enumerate(status_buttons):
            row, col = divmod(i, 2)
            btn = ModernButton(
                status_frame, 
                text=label,
                command=lambda cmd=cmd: self.send_training_command(cmd),
                width=20
            )
            btn.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        
        # Control commands
        control_frame = ModernLabelFrame(command_frame, text="Control Commands")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # First row - O2 Dump controls
        dump_frame = ttk.Frame(control_frame)
        dump_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(dump_frame, text="O2 Dump Control:").pack(side=tk.LEFT, padx=5)
        
        dump_on_btn = ModernButton(
            dump_frame,
            text="O2 Dump ON",
            command=lambda: self.send_training_command("SET O2DUMP 1"),
            width=12
        )
        dump_on_btn.pack(side=tk.LEFT, padx=5)
        
        dump_off_btn = ModernButton(
            dump_frame,
            text="O2 Dump OFF",
            command=lambda: self.send_training_command("SET O2DUMP 0"),
            width=12
        )
        dump_off_btn.pack(side=tk.LEFT, padx=5)
        
        # Second row - O2 Failure control
        o2fail_btn = ModernButton(
            control_frame,
            text="Simulate O2 Failure",
            command=lambda: self.send_training_command("RUN O2FAIL"),
            width=20
        )
        o2fail_btn.pack(padx=5, pady=2)
        
        # Program control commands
        program_frame = ModernLabelFrame(command_frame, text="Program Control")
        program_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Program control buttons in grid layout
        program_buttons = [
            ("Enter Pilot Test Mode", "RUN READY"),
            ("Exit Pilot Test Mode", "RUN EXIT"),
            ("Advance to Next Step", "RUN NEXT"),
            ("Abort Current Test", "RUN ABORT")
        ]
        
        for i, (label, cmd) in enumerate(program_buttons):
            row, col = divmod(i, 2)
            btn = ModernButton(
                program_frame, 
                text=label,
                command=lambda cmd=cmd: self.send_training_command(cmd),
                width=20
            )
            btn.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        
        # PPT control commands
        ppt_frame = ModernLabelFrame(command_frame, text="Positive Pressure Test")
        ppt_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ppt_buttons = [
            ("Enter PPT Mode", "RUN PPT IDLE"),
            ("Start PPT", "RUN PPT START"),
            ("Stop PPT", "RUN PPT STOP")
        ]
        
        for i, (label, cmd) in enumerate(ppt_buttons):
            btn = ModernButton(
                ppt_frame, 
                text=label,
                command=lambda cmd=cmd: self.send_training_command(cmd),
                width=20
            )
            btn.pack(padx=5, pady=2)
        
        # Flight simulator commands
        flsim_frame = ModernLabelFrame(command_frame, text="Flight Simulator")
        flsim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Run Flight Sim button
        flsim_btn = ModernButton(
            flsim_frame,
            text="Enter Flight Sim Mode",
            command=lambda: self.send_training_command("RUN FLSIM"),
            width=20
        )
        flsim_btn.pack(padx=5, pady=2)
        
        # Altitude entry
        alt_frame = ttk.Frame(flsim_frame)
        alt_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(alt_frame, text="Set Altitude (ft):").pack(side=tk.LEFT, padx=5)
        
        self.flsim_alt_var = tk.StringVar()
        alt_entry = ttk.Entry(alt_frame, textvariable=self.flsim_alt_var, width=10)
        alt_entry.pack(side=tk.LEFT, padx=5)
        
        set_alt_btn = ModernButton(
            alt_frame,
            text="Set Altitude",
            command=self.set_flsim_altitude,
            width=12
        )
        set_alt_btn.pack(side=tk.LEFT, padx=5)
        
        # Response display area
        response_frame = ModernLabelFrame(command_frame, text="Command Responses")
        response_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text area for responses
        self.training_response_text = tk.Text(response_frame, height=8, wrap=tk.WORD)
        self.training_response_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar for text area
        response_scrollbar = ttk.Scrollbar(response_frame, command=self.training_response_text.yview)
        response_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.training_response_text.config(yscrollcommand=response_scrollbar.set)
        
        # Clear responses button
        clear_btn = ModernButton(
            response_frame,
            text="Clear Responses",
            command=lambda: self.training_response_text.delete(1.0, tk.END),
            width=15
        )
        clear_btn.pack(pady=5)
        
        # Right side - Training materials
        materials_frame = ModernLabelFrame(paned, text="Training Materials")
        paned.add(materials_frame, weight=1)
        
        # Add training content
        ttk.Label(
            materials_frame,
            text="ROBD2 Training Instructions",
            font=("Arial", 12, "bold")
        ).pack(padx=10, pady=5)
        
        instructions = """
1. Before starting any training:
   - Ensure the ROBD2 device is properly connected
   - Verify O2 source pressure is adequate
   - Check that breathing loop is properly installed

2. Basic Training Procedure:
   a. Enter Pilot Test Mode with "Enter Pilot Test Mode" button
   b. Select and run a program or use Flight Sim mode
   c. Monitor SpO2 and pulse rate during the session
   d. Use O2 Dump in case of emergency or for demonstration

3. Using Positive Pressure Test:
   a. Enter PPT Mode with "Enter PPT Mode" button
   b. Start the test with "Start PPT" button
   c. Monitor breathing loop pressure
   d. Stop the test with "Stop PPT" button

4. Emergency Procedures:
   - Activate O2 Dump ON for immediate oxygen
   - Use "Abort Current Test" to stop any running program
   - Exit Pilot Test Mode when session is complete

5. Monitoring Vitals:
   - Use SpO2 Reading and Pulse Reading commands
   - Monitor O2 Concentration regularly
   - Check breathing loop pressure
        """
        
        instruction_text = tk.Text(materials_frame, wrap=tk.WORD, height=20)
        instruction_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        instruction_text.insert(tk.END, instructions)
        instruction_text.config(state=tk.DISABLED)
        
        # Checklist button
        checklist_btn = ModernButton(
            materials_frame,
            text="Open Training Checklist",
            command=lambda: ChecklistWindow(self.root, "Training Checklist", [
                "Connect ROBD2 device",
                "Verify O2 source pressure",
                "Install breathing loop properly",
                "Set up pulse oximeter",
                "Configure desired training program",
                "Brief trainee on emergency procedures",
                "Enter Pilot Test Mode",
                "Run selected program",
                "Monitor vital signs throughout session",
                "Conclude session with proper shutdown"
            ])
        )
        checklist_btn.pack(pady=10)
        
        return training_frame
        
    def send_training_command(self, command):
        """Send a command from the training tab and display the response"""
        if not self.serial_comm.is_connected:
            self.training_response_text.insert(tk.END, "Error: Device not connected\n")
            return
            
        try:
            # Send the command
            success, message = self.serial_comm.send_command(command)
            
            # Display command
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.training_response_text.insert(tk.END, f"[{timestamp}] >> {command}\n")
            
            if not success:
                self.training_response_text.insert(tk.END, f"[{timestamp}] Error: {message}\n\n")
                self.training_response_text.see(tk.END)
                return
            
            # Wait for and get response
            def get_response():
                try:
                    response = self.serial_comm.get_response()
                    if response:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        self.training_response_text.insert(tk.END, f"[{timestamp}] << {response}\n\n")
                    else:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        self.training_response_text.insert(tk.END, f"[{timestamp}] << (no response)\n\n")
                    self.training_response_text.see(tk.END)
                except Exception as e:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.training_response_text.insert(tk.END, f"[{timestamp}] Error getting response: {str(e)}\n\n")
                    self.training_response_text.see(tk.END)
            
            # Schedule response check after a short delay
            self.root.after(100, get_response)
            
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.training_response_text.insert(tk.END, f"[{timestamp}] Error: {str(e)}\n\n")
            self.training_response_text.see(tk.END)
            
    def set_flsim_altitude(self):
        """Set flight simulator altitude"""
        try:
            altitude = int(self.flsim_alt_var.get())
            if altitude < 0 or altitude > 34000:
                self.training_response_text.insert(tk.END, "Error: Altitude must be between 0 and 34000 ft\n")
                return
                
            command = f"SET FSALT {altitude}"
            self.send_training_command(command)
            
        except ValueError:
            self.training_response_text.insert(tk.END, "Error: Invalid altitude value\n")

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
        
        # Data collection control
        control_frame = ModernLabelFrame(dashboard_frame, text="Plot Controls (0.2Hz - every 5 seconds)", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        start_btn = ModernButton(
            control_frame,
            text="Start Plotting",
            command=self.start_data_collection,
            width=15
        )
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ModernButton(
            control_frame,
            text="Stop Plotting",
            command=self.stop_data_collection,
            width=15
        )
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Performance info
        info_label = ttk.Label(
            control_frame,
            text="Note: Data collection optimized for device performance",
            font=('Helvetica', 9, 'italic')
        )
        info_label.pack(side=tk.LEFT, padx=10)
        
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
        self.altitude_line, = self.altitude_ax.plot([], [], 'b-', label='Altitude')
        self.o2_line, = self.o2_ax.plot([], [], 'g-', label='O2 Concentration')
        self.blp_line, = self.vitals_ax.plot([], [], 'r-', label='BLP')
        self.spo2_line, = self.vitals_ax.plot([], [], 'm-', label='SpO2')
        self.pulse_line, = self.vitals_ax.plot([], [], 'c-', label='Pulse')
        
        # Configure plots
        self.altitude_ax.set_ylabel('Altitude (ft)')
        self.o2_ax.set_ylabel('O2 (%)')
        self.vitals_ax.set_ylabel('Value')
        self.vitals_ax.set_xlabel('Time (s)')
        
        for ax in [self.altitude_ax, self.o2_ax, self.vitals_ax]:
            ax.grid(True)
            ax.legend()
            
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.pack(fill=tk.X)
        NavigationToolbar2Tk(self.canvas, toolbar_frame)
        
        return dashboard_frame
        
    def start_data_collection(self):
        """Start collecting data at 0.2Hz (every 5 seconds) for visualization only"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Please connect to the device first")
            return
            
        # Clear existing data
        self.data_store.clear()
        self.plotting_active = True
        
        # Start data collection for plots only (not saved to file)
        self.collect_data_for_plots()
        
    def stop_data_collection(self):
        """Stop collecting data for plots"""
        self.plotting_active = False

    def collect_data_for_plots(self):
        """Collect data at 0.2Hz (every 5 seconds) for plotting"""
        if not self.serial_comm.is_connected or not self.plotting_active:
            # Schedule next data collection
            self.root.after(5000, self.collect_data_for_plots)
            return
            
        try:
            # Send command to get current data from the device
            success, message = self.serial_comm.send_command("GET RUN ALL")
            if not success:
                log.warning(f"Failed to send command: {message}")
                # Schedule next data collection
                self.root.after(5000, self.collect_data_for_plots)
                return
            
            # Wait a moment for response, then get it
            self.root.after(200, self._process_data_response)
            
        except Exception as e:
            log.error(f"Error collecting data: {e}")
        
        # Schedule next data collection (0.2Hz - every 5 seconds)
        self.root.after(5000, self.collect_data_for_plots)
        
    def _process_data_response(self):
        """Process the response from the data collection command"""
        try:
            # Get the response
            response = self.serial_comm.get_response()
            if not response:
                return
                
            data = response.strip().split(',')
            
            # Parse the data if valid
            if len(data) >= 10:
                # Format: timestamp, program, current_alt, final_alt, o2_conc, bl_pressure, elapsed_time, remaining_time, spo2, pulse
                timestamp = datetime.now()
                
                # Skip additional O2 voltage request to reduce device load
                o2_voltage = 0.0
                
                # Process the data without additional requests
                self._process_parsed_data(timestamp, data, o2_voltage)
                
        except Exception as e:
            log.error(f"Error processing data response: {e}")
            

        
    def _process_parsed_data(self, timestamp, data, o2_voltage):
        """Process the parsed data and update plots"""
        try:
            altitude = float(data[2])
            o2_conc = float(data[4])
            blp = float(data[5])
            spo2 = float(data[8])
            pulse = float(data[9])
            
            # Add data to data store
            self.data_store.add_data(timestamp, {
                'altitude': altitude,
                'o2_conc': o2_conc,
                'blp': blp,
                'spo2': spo2,
                'pulse': pulse,
                'o2_voltage': o2_voltage,
                'error_percent': 0.0  # Calculate if needed
            })
            
            # Trigger plot update
            self.update_plots()
            
        except Exception as e:
            log.error(f"Error processing parsed data: {e}")

    def create_diagnostics_tab(self):
        """Create the diagnostics tab with command buttons"""
        diagnostics_frame = ModernFrame(self.notebook)
        self.notebook.add(diagnostics_frame, text="Diagnostics")
        
        # Command buttons section
        commands_frame = ModernLabelFrame(diagnostics_frame, text="ROBD2 Commands", padding=10)
        commands_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create a scrollable frame for the commands
        commands_canvas = tk.Canvas(commands_frame)
        scrollbar = ttk.Scrollbar(commands_frame, orient="vertical", command=commands_canvas.yview)
        scrollable_frame = ttk.Frame(commands_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: commands_canvas.configure(scrollregion=commands_canvas.bbox("all"))
        )
        
        commands_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        commands_canvas.configure(yscrollcommand=scrollbar.set)
        
        commands_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define the commands
        diagnostic_commands = [
            ("Get O2 Concentration", "GET RUN O2CONC"),
            ("Get Breathing Loop Pressure", "GET RUN BLPRESS"),
            ("Get SpO2 Reading", "GET RUN SPO2"),
            ("Get Pulse Reading", "GET RUN PULSE"),
            ("Get Current Altitude", "GET RUN ALT"),
            ("Get Final Altitude", "GET RUN FINALALT"),
            ("Get Elapsed Time", "GET RUN ELTIME"),
            ("Get Remaining Time", "GET RUN REMTIME"),
            ("Get All Run Data", "GET RUN ALL"),
            ("Get System Info", "GET INFO"),
            ("Get O2 Status", "GET O2 STATUS"),
            ("Get System Status", "GET STATUS"),
        ]
        
        # Create command buttons (2 columns)
        for i, (label, command) in enumerate(diagnostic_commands):
            row = i // 2
            col = i % 2
            cmd_btn = ModernButton(
                scrollable_frame, 
                text=label,
                command=lambda cmd=command: self.send_diagnostic_command(cmd),
                width=25
            )
            cmd_btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
        
        # Special case for MFC flow rate which needs input
        mfc_frame = ttk.Frame(scrollable_frame)
        mfc_frame.grid(row=(len(diagnostic_commands) // 2) + 1, column=0, columnspan=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(mfc_frame, text="MFC Number:").pack(side=tk.LEFT, padx=5)
        self.mfc_num_var = tk.StringVar()
        mfc_entry = ttk.Entry(mfc_frame, textvariable=self.mfc_num_var, width=5)
        mfc_entry.pack(side=tk.LEFT, padx=5)
        
        mfc_btn = ModernButton(
            mfc_frame,
            text="Get MFC Flow Rate",
            command=lambda: self.send_diagnostic_command(f"GET MFC {self.mfc_num_var.get()}")
        )
        mfc_btn.pack(side=tk.LEFT, padx=5)
        
        # Special case for ADC device voltage which needs input
        adc_frame = ttk.Frame(scrollable_frame)
        adc_frame.grid(row=(len(diagnostic_commands) // 2) + 1, column=1, columnspan=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(adc_frame, text="ADC Device:").pack(side=tk.LEFT, padx=5)
        self.adc_num_var = tk.StringVar()
        adc_entry = ttk.Entry(adc_frame, textvariable=self.adc_num_var, width=5)
        adc_entry.pack(side=tk.LEFT, padx=5)
        
        adc_btn = ModernButton(
            adc_frame,
            text="Get ADC Voltage",
            command=lambda: self.send_diagnostic_command(f"GET ADC {self.adc_num_var.get()}")
        )
        adc_btn.pack(side=tk.LEFT, padx=5)
        
        # Custom command input
        custom_frame = ModernLabelFrame(diagnostics_frame, text="Custom Command", padding=10)
        custom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(custom_frame, textvariable=self.command_var)
        command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        send_btn = ModernButton(custom_frame, text="Send", command=lambda: self.send_diagnostic_command(self.command_var.get()))
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Response display
        response_frame = ModernLabelFrame(diagnostics_frame, text="Device Response", padding=10)
        response_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add a scrollbar to the response text area
        response_scroll = ttk.Scrollbar(response_frame)
        response_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.response_text = tk.Text(response_frame, height=10, wrap=tk.WORD, yscrollcommand=response_scroll.set)
        self.response_text.pack(fill=tk.BOTH, expand=True)
        response_scroll.config(command=self.response_text.yview)
        
        # Start polling for responses
        self.poll_responses()
        
        return diagnostics_frame
        
    def create_programming_tab(self):
        """Create the programming tab"""
        programming_frame = ModernFrame(self.notebook)
        self.notebook.add(programming_frame, text="Programming")
        
        # Create and pack the program manager
        self.program_manager = ProgramManager(programming_frame, self.serial_comm)
        self.program_manager.pack(fill=tk.BOTH, expand=True)
        
        return programming_frame

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
        
        return logging_frame

    def on_tab_changed(self, event):
        """Handle tab change events"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        # Handle dashboard tab selection
        if selected_tab == "Dashboard":
            if self.serial_comm.is_connected and not self.plotting_active:
                # Start data collection if connected and not already plotting
                self.start_data_collection()
        else:
            # Stop data collection if leaving dashboard tab
            if self.plotting_active:
                self.stop_data_collection()

def main():
    try:
        root = tk.Tk()
        app = ROBD2GUI(root)
        
        def on_closing():
            try:
                # Stop any ongoing monitoring or data collection
                app.plotting_active = False
                if hasattr(app, 'performance_monitor'):
                    app.performance_monitor.stop_monitoring()
                
                # Stop any ongoing logging
                if hasattr(app, 'data_logger'):
                    app.data_logger.stop_logging()
                
                # Cancel any pending after events
                if hasattr(app, 'poll_after_id'):
                    root.after_cancel(app.poll_after_id)
                
                # Clean up scrolling
                app.cleanup_scrolling()
                
                # Disconnect device if connected
                if app.serial_comm.is_connected:
                    app.disconnect_device()
                    
                # Wait for any remaining threads to finish
                for thread in threading.enumerate():
                    if thread != threading.current_thread() and thread.daemon:
                        thread.join(timeout=1.0)
                
            except Exception as e:
                log.error(f"Error during cleanup: {e}")
            finally:
                root.quit()
                root.destroy()
                sys.exit(0)  # Ensure complete exit
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        log.error(f"Application error: {e}", exc_info=True)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 