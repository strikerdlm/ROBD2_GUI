import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
from datetime import datetime
import threading
import queue
import logging
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from collections import deque
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

class DataStore:
    """Store and manage real-time data for plotting"""
    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.data = {
            'altitude': deque(maxlen=max_points),
            'o2_conc': deque(maxlen=max_points),
            'blp': deque(maxlen=max_points),
            'spo2': deque(maxlen=max_points),
            'pulse': deque(maxlen=max_points),
            'o2_voltage': deque(maxlen=max_points),
            'error_percent': deque(maxlen=max_points)
        }
        self.timestamps = deque(maxlen=max_points)
        self.start_time = None
        
    def add_data(self, timestamp, data_dict):
        """Add new data point with validation"""
        if self.start_time is None:
            self.start_time = timestamp
            
        self.timestamps.append(timestamp)
        
        # Validate and store data
        for key, value in data_dict.items():
            if key in self.data:
                # Apply validation ranges
                if key == 'spo2':
                    value = max(50, min(100, value))  # Clamp between 50-100%
                elif key == 'o2_conc':
                    value = max(0, min(100, value))   # Clamp between 0-100%
                elif key == 'pulse':
                    value = max(20, min(220, value))  # Clamp between 20-220 bpm
                self.data[key].append(value)
                
    def get_data(self, metric):
        """Get data for a specific metric with relative time"""
        if metric in self.data:
            # Convert timestamps to relative time in seconds
            relative_times = [(t - self.start_time).total_seconds() for t in self.timestamps]
            return relative_times, list(self.data[metric])
        return [], []
        
    def clear(self):
        """Clear all data"""
        for key in self.data:
            self.data[key].clear()
        self.timestamps.clear()
        self.start_time = None
        
    def export_to_csv(self, filename):
        """Export all data to a CSV file"""
        try:
            import csv
            from datetime import datetime
            
            # Create directory if it doesn't exist
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)
            
            # Generate filename with timestamp if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = export_dir / f"robd2_data_{timestamp}.csv"
            else:
                filename = export_dir / filename
                
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                headers = ['Time (s)', 'Time (min)', 'Altitude (ft)', 'O2 Concentration (%)', 
                          'BLP (mmHg)', 'SpO2 (%)', 'Pulse (bpm)', 'O2 Voltage (V)', 
                          'Error (%)']
                writer.writerow(headers)
                
                # Write data
                for i in range(len(self.timestamps)):
                    time_s = (self.timestamps[i] - self.start_time).total_seconds()
                    time_min = time_s / 60
                    row = [
                        f"{time_s:.2f}",
                        f"{time_min:.2f}",
                        f"{self.data['altitude'][i]:.1f}",
                        f"{self.data['o2_conc'][i]:.1f}",
                        f"{self.data['blp'][i]:.1f}",
                        f"{self.data['spo2'][i]:.1f}",
                        f"{self.data['pulse'][i]:.1f}",
                        f"{self.data['o2_voltage'][i]:.3f}",
                        f"{self.data['error_percent'][i]:.1f}"
                    ]
                    writer.writerow(row)
                    
            return True, str(filename)
            
        except Exception as e:
            return False, str(e)

class ModernWidget:
    """Base class for modern-styled widgets"""
    def __init__(self):
        self.style = ttk.Style()
        self.style.configure(
            "Modern.TButton",
            padding=10,
            font=('Helvetica', 10)
        )
        self.style.configure(
            "Modern.TFrame",
            background='#f0f0f0'
        )
        self.style.configure(
            "Modern.TLabel",
            font=('Helvetica', 10)
        )
        self.style.configure(
            "Modern.TLabelframe",
            font=('Helvetica', 10)
        )
        self.style.configure(
            "Modern.TLabelframe.Label",
            font=('Helvetica', 10, 'bold')
        )

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        
    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(
            self.tooltip,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1
        )
        label.pack()
        
    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ModernButton(ttk.Button, ModernWidget):
    """Custom button with modern styling"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style="Modern.TButton")
        self.tooltip = None
        
    def set_tooltip(self, text):
        """Set tooltip text for the button"""
        self.tooltip = ToolTip(self, text)

class ModernFrame(ttk.Frame, ModernWidget):
    """Custom frame with modern styling"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style="Modern.TFrame")

class ModernLabelFrame(ttk.LabelFrame, ModernWidget):
    """Custom labeled frame with modern styling"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style="Modern.TLabelframe")

class ChecklistWindow:
    def __init__(self, parent, title, items):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Create main container
        main_frame = ModernFrame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text=title,
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for checklist
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ModernFrame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Checklist items
        self.checklist_items = items
        
        # Create checkboxes for each item
        self.checkboxes = []
        for item in self.checklist_items:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=5)
            
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(frame, variable=var)
            checkbox.pack(side=tk.LEFT, padx=(0, 5))
            
            # Create label for wrapped text
            label = ttk.Label(frame, text=item, wraplength=700, justify=tk.LEFT)
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.checkboxes.append(var)
        
        # Add completion button
        self.complete_btn = ModernButton(
            main_frame,
            text="Complete Checklist",
            command=self.check_completion
        )
        self.complete_btn.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=('Helvetica', 10)
        )
        self.status_label.pack(pady=10)
        
        # Bind mouse wheel events for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        def _on_linux_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.num)), "units")
            
        # Bind for Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Bind for Linux
        canvas.bind_all("<Button-4>", _on_linux_mousewheel)
        canvas.bind_all("<Button-5>", _on_linux_mousewheel)
        
        # Unbind when window is closed
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
            self.window.destroy()
            
        self.window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Center window on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

class ScriptViewerWindow:
    def __init__(self, parent, title, content):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Create main container
        main_frame = ModernFrame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text=title,
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for content
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ModernFrame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add content with proper formatting
        content_label = ttk.Label(
            self.scrollable_frame,
            text=content,
            wraplength=700,
            justify=tk.LEFT,
            font=('Helvetica', 11)
        )
        content_label.pack(pady=10)
        
        # Bind mouse wheel events for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        def _on_linux_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.num)), "units")
            
        # Bind for Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Bind for Linux
        canvas.bind_all("<Button-4>", _on_linux_mousewheel)
        canvas.bind_all("<Button-5>", _on_linux_mousewheel)
        
        # Unbind when window is closed
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
            self.window.destroy()
            
        self.window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Center window on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

class LoadingIndicator:
    def __init__(self, parent, message="Loading..."):
        self.window = tk.Toplevel(parent)
        self.window.title("")
        self.window.geometry("300x100")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create frame
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add message
        ttk.Label(
            frame,
            text=message,
            font=('Helvetica', 10)
        ).pack(pady=(0, 10))
        
        # Add progress bar
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate'
        )
        self.progress.pack(fill=tk.X)
        self.progress.start()
        
    def destroy(self):
        self.window.destroy()

class ROBD2GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ROBD2 Diagnostic Interface")
        self.root.geometry("1200x800")
        
        # Create menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Connect (Ctrl+C)", command=self.connect_to_device)
        file_menu.add_command(label="Disconnect (Ctrl+D)", command=self.disconnect_device)
        file_menu.add_separator()
        file_menu.add_command(label="Export Data (Ctrl+E)", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Refresh Ports (Ctrl+R)", command=self.refresh_ports)
        tools_menu.add_command(label="Start Logging (Ctrl+S)", command=self.start_logging)
        tools_menu.add_command(label="Stop Logging (Ctrl+X)", command=self.stop_logging)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: self.notebook.select(self.notebook.tabs().index("About")))
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        
        # Initialize variables
        self.serial_port = None
        self.is_connected = False
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.data_store = DataStore()
        self.plotting_active = False
        
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
        self.create_about_tab()
        
        # Add keyboard shortcuts
        self.root.bind('<Control-r>', lambda e: self.refresh_ports())
        self.root.bind('<Control-c>', lambda e: self.connect_to_device() if not self.is_connected else None)
        self.root.bind('<Control-d>', lambda e: self.disconnect_device() if self.is_connected else None)
        self.root.bind('<Control-e>', lambda e: self.export_data() if hasattr(self, 'data_store') else None)
        self.root.bind('<Control-s>', lambda e: self.start_logging() if self.is_connected else None)
        self.root.bind('<Control-x>', lambda e: self.stop_logging() if hasattr(self, 'data_logger') else None)
        
        # Start command processing thread
        self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.command_thread.start()
        
        # Start polling for responses
        self.root.after(100, self.poll_responses)
        
        # Start plot updates
        self.root.after(1000, self.update_plots)

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
        
        # Bind mouse wheel events for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        def _on_linux_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.num)), "units")
            
        # Bind for Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Bind for Linux
        canvas.bind_all("<Button-4>", _on_linux_mousewheel)
        canvas.bind_all("<Button-5>", _on_linux_mousewheel)
        
        # Unbind when window is closed
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
            doc_window.destroy()
            
        doc_window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Center window on screen
        doc_window.update_idletasks()
        width = doc_window.winfo_width()
        height = doc_window.winfo_height()
        x = (doc_window.winfo_screenwidth() // 2) - (width // 2)
        y = (doc_window.winfo_screenheight() // 2) - (height // 2)
        doc_window.geometry(f'{width}x{height}+{x}+{y}')

    def create_about_tab(self):
        """Create the About tab with project information"""
        about_frame = ModernFrame(self.notebook)
        self.notebook.add(about_frame, text="About")
        
        # Create main content frame with padding
        content_frame = ModernFrame(about_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title with custom styling
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(
            title_frame,
            text="ROBD2 Diagnostic Interface",
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
        version_frame = ttk.Frame(content_frame)
        version_frame.pack(fill=tk.X, pady=(0, 30))
        
        version_label = ttk.Label(
            version_frame,
            text="Version 1.0.0",
            font=('Helvetica', 14, 'bold')
        )
        version_label.pack()
        
        # Description with custom styling
        description_frame = ModernLabelFrame(content_frame, text="Overview", padding=15)
        description_frame.pack(fill=tk.X, pady=(0, 30))
        
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
        
        # Features with custom styling
        features_frame = ModernLabelFrame(content_frame, text="Key Features", padding=15)
        features_frame.pack(fill=tk.X, pady=(0, 30))
        
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
        
        # Requirements with custom styling
        requirements_frame = ModernLabelFrame(content_frame, text="System Requirements", padding=15)
        requirements_frame.pack(fill=tk.X, pady=(0, 30))
        
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
        
        # Author information with custom styling
        author_frame = ModernLabelFrame(content_frame, text="Author", padding=15)
        author_frame.pack(fill=tk.X, pady=(0, 30))
        
        author_text = """
Diego Malpica MD
Aerospace Medicine
Aerospace Physiology Instructor
Aerospace Scientific Department
Aerospace Medicine Directorate
Colombian Aerospace Force

Initial work - [strikerdlm](https://github.com/strikerdlm)

Copyright © 2025 Diego Malpica MD. All rights reserved.
"""
        author_label = ttk.Label(
            author_frame,
            text=author_text,
            wraplength=700,
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        author_label.pack()
        
        # Disclaimer with custom styling
        disclaimer_frame = ModernLabelFrame(content_frame, text="Disclaimer", padding=15)
        disclaimer_frame.pack(fill=tk.X)
        
        disclaimer_text = """
This software is provided "as is" without any warranties, express or implied. The authors and developers are not responsible for any damages or injuries that may occur from the use of this software.

This software is not intended for clinical use or any other settings without proper medical supervision.
"""
        disclaimer_label = ttk.Label(
            disclaimer_frame,
            text=disclaimer_text,
            wraplength=700,
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        disclaimer_label.pack()

    def create_dashboard_tab(self):
        """Create the dashboard tab with real-time plots"""
        dashboard_frame = ModernFrame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Create top frame for controls
        top_frame = ModernFrame(dashboard_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add export button
        self.export_btn = ModernButton(
            top_frame,
            text="Export Data",
            command=self.export_data,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add time unit selector
        time_frame = ttk.Frame(top_frame)
        time_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(time_frame, text="Time Unit:").pack(side=tk.LEFT)
        self.time_unit_var = tk.StringVar(value="seconds")
        time_combo = ttk.Combobox(
            time_frame,
            textvariable=self.time_unit_var,
            values=["seconds", "minutes"],
            state="readonly",
            width=10
        )
        time_combo.pack(side=tk.LEFT, padx=5)
        
        # Create left and right frames for plots
        left_frame = ttk.Frame(dashboard_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        right_frame = ttk.Frame(dashboard_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create plots
        self.create_plot(left_frame, "Altitude", 'altitude', 'Altitude (ft)')
        self.create_plot(left_frame, "O2 Concentration", 'o2_conc', 'O2 Concentration (%)')
        self.create_plot(left_frame, "Breathing Loop Pressure", 'blp', 'BLP (mmHg)')
        
        self.create_plot(right_frame, "SpO2", 'spo2', 'SpO2 (%)')
        self.create_plot(right_frame, "Pulse Rate", 'pulse', 'Pulse Rate (bpm)')
        self.create_plot(right_frame, "O2 Sensor Voltage", 'o2_voltage', 'Voltage (V)')
        
        # Create statistics frame
        stats_frame = ModernLabelFrame(dashboard_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_labels = {}
        row = 0
        for metric in ['altitude', 'o2_conc', 'blp', 'spo2', 'pulse', 'o2_voltage']:
            ttk.Label(stats_frame, text=metric.replace('_', ' ').title()).grid(row=row, column=0, padx=5, pady=2)
            self.stats_labels[metric] = ttk.Label(stats_frame, text="--")
            self.stats_labels[metric].grid(row=row, column=1, padx=5, pady=2)
            row += 1

    def create_plot(self, parent, title, metric, ylabel):
        """Create a matplotlib plot widget"""
        frame = ModernLabelFrame(parent, text=title, padding=5)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create figure and canvas
        fig = Figure(figsize=(6, 2), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create subplot
        ax = fig.add_subplot(111)
        line, = ax.plot([], [], '-')
        
        # Configure plot
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        
        # Store plot objects
        if not hasattr(self, 'plots'):
            self.plots = {}
        self.plots[metric] = {
            'figure': fig,
            'canvas': canvas,
            'ax': ax,
            'line': line
        }

    def update_plots(self):
        """Update all plots with new data"""
        if self.plotting_active:
            time_unit = self.time_unit_var.get()
            for metric, plot in self.plots.items():
                timestamps, values = self.data_store.get_data(metric)
                if timestamps and values:
                    # Convert time units if needed
                    if time_unit == "minutes":
                        timestamps = [t/60 for t in timestamps]
                        xlabel = "Time (minutes)"
                    else:
                        xlabel = "Time (seconds)"
                    
                    plot['line'].set_data(timestamps, values)
                    plot['ax'].relim()
                    plot['ax'].autoscale_view()
                    plot['ax'].set_xlabel(xlabel)
                    plot['canvas'].draw()
                    
            # Update statistics
            for metric, label in self.stats_labels.items():
                timestamps, values = self.data_store.get_data(metric)
                if values:
                    stats = f"Min: {min(values):.1f} | Max: {max(values):.1f} | Avg: {sum(values)/len(values):.1f}"
                    label.configure(text=stats)
        
        # Schedule next update
        self.root.after(1000, self.update_plots)

    def create_connection_tab(self):
        """Create the connection tab"""
        connection_frame = ModernFrame(self.notebook)
        self.notebook.add(connection_frame, text="Connection")
        
        # Port selection
        port_frame = ttk.LabelFrame(connection_frame, text="Port Selection", padding=10)
        port_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var)
        self.port_combo.pack(fill=tk.X, pady=5)
        ToolTip(self.port_combo, "Select the COM port where the ROBD2 device is connected")
        
        refresh_btn = ModernButton(
            port_frame,
            text="Refresh Ports",
            command=self.refresh_ports
        )
        refresh_btn.pack(pady=5)
        refresh_btn.set_tooltip("Scan for available COM ports")
        
        # Connection controls
        control_frame = ttk.LabelFrame(connection_frame, text="Connection Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.connect_btn = ModernButton(
            control_frame,
            text="Connect",
            command=self.connect_to_device
        )
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        self.connect_btn.set_tooltip("Connect to the selected ROBD2 device")
        
        self.disconnect_btn = ModernButton(
            control_frame,
            text="Disconnect",
            command=self.disconnect_device,
            state=tk.DISABLED
        )
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        self.disconnect_btn.set_tooltip("Disconnect from the ROBD2 device")
        
        # Pre-flight checklist button
        checklist_btn = ModernButton(
            control_frame,
            text="Pre-flight Checklist",
            command=lambda: ChecklistWindow(self.root, "Pre-flight Checklist", [
                "Asegurar que el sistema ROBD2 esté correctamente desempacado e instalado.",
                "Verificar que todos los materiales de empaque sean removidos y guardados para uso futuro.",
                "Confirmar que la conexión de energía sea correcta para su región (115V o 230V) y esté conectada de manera segura a un enchufe con conexión a tierra.",
                "Conectar el aire (amarillo) y nitrógeno (negro) a 40 a 50 PSIG a sus respectivos puertos.",
                "Conectar el 100% de oxígeno (verde) a 20 PSIG.",
                "Conectar la máscara de piloto al Conector de Máscara de Respiración en el panel frontal.",
                "Asegurar que la sonda del oxímetro de pulso esté conectada.",
                "Encender el sistema utilizando el interruptor de energía.",
                "Permitir que el sistema se caliente durante el tiempo indicado (10 minutos).",
                "Iniciar las auto-pruebas presionando la tecla SELFTST y seguir las instrucciones en pantalla.",
                "Permitir que el sistema complete las auto-pruebas y auto-calibración. No utilizar la máscara durante este proceso ya que el oxígeno puede no estar presente. Permitir que el proceso muestre el error.",
                "Registrar los valores de voltaje del sensor de O₂ tanto a concentración ambiente (aprox. 21%) como al 100% O₂, según las indicaciones del manual técnico.",
                "Ingresar manualmente en la tabla ADC 12 los valores de voltaje obtenidos durante la fase de calibración fallida. Estos valores corresponderán al aire ambiente de Bogotá (con menor concentración de O₂ debido a la altitud) y al O₂ al 100%.",
                "Omisión de la calibración automática: activar el modo 'Bypass Self-Tests' según las indicaciones del manual (Programming and Technical Guide – Rev 8) para permitir el funcionamiento del ROBD2 sin la calibración automática del sensor de O₂.",
                "Ejecución de la Prueba de Rendimiento (Profile #20 – TEST):",
                "Realizar la prueba de rendimiento indicada en la documentación del fabricante con el perfil #20.",
                "Verificar que las mezclas de O₂ entregadas por el ROBD2 se encuentren dentro de los rangos permitidos establecidos en las tablas de referencia proporcionadas por el fabricante (APPENDIX M en el manual).",
                "Si las mediciones de O₂ se mantienen dentro de los rangos especificados, se considerará la prueba satisfactoria."
            ])
        )
        checklist_btn.pack(side=tk.LEFT, padx=5)
        checklist_btn.set_tooltip("Open the pre-flight checklist for device setup")
        
        # Status display
        status_frame = ttk.LabelFrame(connection_frame, text="Connection Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial port refresh
        self.refresh_ports()

    def create_calibration_tab(self):
        """Create the calibration tab"""
        calibration_frame = ModernFrame(self.notebook)
        self.notebook.add(calibration_frame, text="Calibration")
        
        # Device selection
        device_frame = ttk.LabelFrame(calibration_frame, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.device_var = tk.StringVar()
        for i, device in enumerate(['ROBD2-9515', 'ROBD2-9516', 'ROBD2-9471']):
            ttk.Radiobutton(
                device_frame,
                text=device,
                variable=self.device_var,
                value=str(i + 1)
            ).pack(anchor=tk.W, pady=2)
        
        # Calibration controls
        control_frame = ttk.LabelFrame(calibration_frame, text="Calibration Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_calibration_btn = ModernButton(
            control_frame,
            text="Start Calibration",
            command=self.start_calibration,
            state=tk.DISABLED
        )
        self.start_calibration_btn.pack(pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(calibration_frame, text="Calibration Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def create_performance_tab(self):
        """Create the performance monitoring tab"""
        performance_frame = ModernFrame(self.notebook)
        self.notebook.add(performance_frame, text="Performance")
        
        # Device selection
        device_frame = ttk.LabelFrame(performance_frame, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.perf_device_var = tk.StringVar()
        for i, device in enumerate(['ROBD2-9515', 'ROBD2-9516', 'ROBD2-9471']):
            ttk.Radiobutton(
                device_frame,
                text=device,
                variable=self.perf_device_var,
                value=str(i + 1)
            ).pack(anchor=tk.W, pady=2)
        
        # Performance controls
        control_frame = ttk.LabelFrame(performance_frame, text="Performance Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_performance_btn = ModernButton(
            control_frame,
            text="Start Performance Monitoring",
            command=self.start_performance_monitoring,
            state=tk.DISABLED
        )
        self.start_performance_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_performance_btn = ModernButton(
            control_frame,
            text="Stop Performance Monitoring",
            command=self.stop_performance_monitoring,
            state=tk.DISABLED
        )
        self.stop_performance_btn.pack(side=tk.LEFT, padx=5)
        
        # Real-time display
        display_frame = ttk.LabelFrame(performance_frame, text="Real-time Data", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create grid for real-time data
        self.perf_data_labels = {}
        row = 0
        for label in ['Altitude', 'O2 Concentration', 'BLP', 'SpO2', 'Pulse']:
            ttk.Label(display_frame, text=label).grid(row=row, column=0, padx=5, pady=2)
            self.perf_data_labels[label] = ttk.Label(display_frame, text="--")
            self.perf_data_labels[label].grid(row=row, column=1, padx=5, pady=2)
            row += 1

    def create_training_tab(self):
        """Create the training tab with script viewers and checklists"""
        training_frame = ModernFrame(self.notebook)
        self.notebook.add(training_frame, text="Training")
        
        # Create main container with padding
        main_container = ModernFrame(training_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="Training Scripts",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Script buttons frame
        script_frame = ModernLabelFrame(main_container, text="Training Scripts", padding=15)
        script_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create buttons for each script
        scripts = [
            ("Fixed Wing (ES)", "Libreto ala fija"),
            ("Rotary Wing (ES)", "Libreto Ala Rotatoria"),
            ("Fixed Wing (EN)", "Script Fixed-Wing"),
            ("Rotary Wing (EN)", "Script Rotary Wing")
        ]
        
        for text, script_name in scripts:
            btn = ModernButton(
                script_frame,
                text=text,
                command=lambda s=script_name: self.show_script(s)
            )
            btn.pack(fill=tk.X, pady=5)
        
        # Checklists frame
        checklist_frame = ModernLabelFrame(main_container, text="Training Checklists", padding=15)
        checklist_frame.pack(fill=tk.X)
        
        # During training checklist button
        during_btn = ModernButton(
            checklist_frame,
            text="During Training Checklist",
            command=lambda: ChecklistWindow(self.root, "During Training Checklist", [
                "Monitorear las lecturas del oxímetro de pulso y asegurar que permanezcan dentro de los límites seguros. (Mínimo SpO2 65%)",
                "Seguir todas las pautas de seguridad y estar preparado para usar el interruptor de descarga de oxígeno en caso de emergencia de acuerdo con el MANTA vigente",
                "Asegurar que el sujeto bajo prueba sea monitoreado por cualquier señal de incomodidad o por síntomas que incapaciten al piloto"
            ])
        )
        during_btn.pack(fill=tk.X, pady=5)
        
        # After training checklist button
        after_btn = ModernButton(
            checklist_frame,
            text="After Training Checklist",
            command=lambda: ChecklistWindow(self.root, "After Training Checklist", [
                "Después de completar el programa, asegurarse de apagar correctamente el sistema.",
                "Desconectar las fuentes de gas y fuente de energía.",
                "Realizar una inspección visual del sistema en busca de signos de desgaste o daño.",
                "Guardar el sistema y accesorios en un lugar seguro y seco.",
                "Diligenciar el registro en línea del consumo de gases, la retroalimentación del curso por parte de los alumnos y el formato electrónico de novedades"
            ])
        )
        after_btn.pack(fill=tk.X, pady=5)

    def show_script(self, script_name):
        """Show the selected training script"""
        # Get script content from notepad context
        script_content = self.get_script_content(script_name)
        if script_content:
            ScriptViewerWindow(self.root, script_name, script_content)
        else:
            messagebox.showerror("Error", f"Script '{script_name}' not found")

    def get_script_content(self, script_name):
        """Get the content of a script from the notepad context"""
        script_mapping = {
            "Libreto ala fija": """
Bienvenido al entrenamiento de hipoxia normobárica de la Dirección de Medicina Aeroespacial, este entrenamiento está diseñado para que usted reconozca los síntomas de hipoxia y realice los procedimientos de recuperación siguiendo la lista de chequeo PRICE revisada en clase. Vamos a presentarle un escenario de simulación de vuelo en el PREPAR3D donde usted estará al mando y al control de una aeronave, estará a una altitud de 10.000 ft y yo le daré instrucciones específicas de los procedimientos que usted tiene que realizar en su aeronave. Es importante recordarle que esta no es una evaluación de destrezas de vuelo ni una simulación precisa de una aeronave en particular, sino que el entrenamiento está diseñado para que usted identifique de los efectos de la altitud sobre el rendimiento humano en cabina.

Como se revisó en clase, deberá reconocer los síntomas de hipoxia y, al aparecer, chequear PRICE y corregirlo con las tres palancas hacia arriba. Siguiendo las instrucciones del instructor.

Vamos a verificar en el siguiente orden el simulador.

Acomodación en la silla (Ajuste abajo a la izquierda, distancia silla y control de mando)

Ajustarse cinturón

Realizar la adaptación de casco y máscara para que a orden del instructor se la ponga

El instructor en este paso mostrará los pedales, el bastón de mando o joke, el cuadrante de la potencia. No será requerido manipular más controles del simulador o configuraciones especificas dado que todo este control manual debe ser ejecutado por el alumno.

Colocar oxímetro de pulso en la mano no dominante

Al cargar el vuelo en el Prepar3D el instructor debe pausar el simulador para iniciar el vuelo. Se ejecuta el perfil en el ROBD y una vez se inicie se debe dar las siguientes instrucciones.

"TH250, Bogotá radar. Vire por derecha rumbo 130, ascienda y mantenga uno cinco mil pies con un régimen de 500 ft/min.

El alumno debe colacionar de la siguiente manera:

"Bogotá Radar, virando por derecha rumbo 130, ascendiendo y manteniendo uno cinco mil pies a 500 ft/min, TH250."

Al completar la orden del CTA, el instructor dará otra orden siguiendo el esquema:

"TH250, Bogotá radar. Vire por derecha rumbo 210, ascienda y mantenga "uno siete mil pies, a 500 ft/min"

Durante el vuelo, el instructor debe preguntarle al alumno:

"Qué debe hacer usted al tener un síntoma de hipoxia?"

Luego de realizar la recuperación, el piloto debe comunicarse con CTA para declarar la emergencia y solicitar descenso para uno cero mil pies y el CTA debe autorizar al alumno:

"TH250, Bogota Radar, autorizado descenso a uno cero mil pies"

Tras terminar este escenario, se le hace la retroalimentación al piloto de los parámetros de vuelo, problemas de comunicación, seguimiento de ordenes etc. El alumno tuvo en hipoxia y recordó que en el primer síntoma hay que recuperarse accionando el regulador con las tres palancas hacia arriba.

El entrenamiento para visión nocturna se debe ejecutar siguiendo el procedimiento:

"Durante la hipoxia, la disminución de oxígeno en el cuerpo afecta de manera significativa la función de los conos en la retina, que son responsables de la percepción del color y la agudeza visual. En condiciones de hipoxia, la capacidad de los conos para funcionar correctamente se reduce, lo que lleva a una disminución de la sensibilidad a los colores y una reducción en la agudeza visual.

Esto es particularmente crítico durante el vuelo nocturno, ya que la visión ya está comprometida por la falta de luz. La hipoxia puede hacer que los colores sean menos distinguibles y que los objetos en el entorno sean más difíciles de identificar, lo cual puede llevar a errores en la interpretación de las señales y los instrumentos de la aeronave

Es fundamental que reconozca estos síntomas y actúe rápidamente. Al primer signo de hipoxia, debe realizar el chequeo PRICE y ajustar el suministro de oxígeno utilizando el regulador con las tres palancas hacia arriba. Esto ayudará a restablecer los niveles adecuados de oxígeno y mejorar la capacidad visual y cognitiva, reduciendo el riesgo de errores durante el vuelo nocturno.

Recuerde que, en condiciones de baja visibilidad y alta demanda cognitiva, como el vuelo nocturno, la hipoxia puede ser particularmente peligrosa, por lo que la vigilancia y la corrección inmediata son esenciales.

Se presenta la carta de navegación AD 2 SKGY - CHIA - FLAMINIO SUAREZ CAMACHO impresa.

Se ejecuta el perfil para visión nocturna en el ROBD2.

En la Carta Visual OACI de SKGY identifique el aeródromo y señale en la carta las montañas entre 8400 y 10200 ft.

Diga la secuencia de puntos en la salida normalizada VFR hacia ECHO entre BIMA y TIBITOC

Lea el contenido de los recuadros rojos en la carta.

El instructor presiona "Oxygen Dump" y se espera un minuto para la recuperación.

Debe indicar al alumno que vea la diferencia entre los colores durante la hipoxia y cuando se suple oxígeno al 100%. Explicar las implicaciones de interpretar señales aeronáuticas en hipoxia en condiciones de oscuridad, que pueden llevar al piloto a mal interpretar señales y a partir de esto cometer errores en la cabina.""",
            "Libreto Ala Rotatoria": """
Bienvenido al entrenamiento de hipoxia normobárica de la Dirección de Medicina Aeroespacial, este entrenamiento está diseñado para que usted reconozca los síntomas de hipoxia y realice los procedimientos de recuperación siguiendo la lista de chequeo PRICE revisada en clase. Vamos a presentarle un escenario de simulación de vuelo en el PREPAR3D donde usted estará al mando y al control de una aeronave, estará a una altitud de 10.000 ft y yo le daré instrucciones específicas de los procedimientos que usted tiene que realizar en su aeronave. Es importante recordarle que esta no es una evaluación de destrezas de vuelo ni una simulación precisa de una aeronave en particular, sino que el entrenamiento está diseñado para que usted identifique de los efectos de la altitud sobre el rendimiento humano en cabina.

Como se revisó en clase, deberá reconocer los síntomas de hipoxia y, al aparecer, chequear PRICE y corregirlo con las tres palancas hacia arriba. Siguiendo las instrucciones del instructor.

Vamos a verificar en el siguiente orden el simulador.

Acomodación en la silla

Ajustar el cinturón.

Realizar la adaptación de casco y máscara para que a orden del instructor se la ponga

El instructor en este paso mostrará los pedales, el bastón de mando o joke, el cuadrante de la potencia. No será requerido manipular más controles del simulador o configuraciones especificas dado que todo este control manual debe ser ejecutado por el alumno.

Al cargar el vuelo en el Prepar3D el instructor debe pausar el simulador para iniciar el vuelo. Se ejecuta el perfil en el ROBD y una vez se inicie se debe dar las siguientes instrucciones.

"UH180, Bogotá radar. Vire por derecha rumbo 130, ascienda y mantenga uno tres mil pies".

El alumno debe colacionar de la siguiente manera:

"Bogotá Radar, virando por derecha rumbo 130, asciendo y manteniendo uno tres mil pies, UH180."

Al completar la orden del CTA, el instructor dará otra orden siguiendo el esquema:

"UH180, Bogotá radar. Vire derecha rumbo 210, ascienda y mantenga "uno siete mil pies"

Durante el vuelo, el instructor debe preguntarle al alumno:

"Qué debe hacer usted al tener un síntoma de hipoxia?"

Luego de realizar la recuperación, el piloto debe comunicarse con CTA para declarar la emergencia y solicitar descenso para uno cero mil pies y el CTA debe autorizar al alumno:

"UH180, Bogotá Radar, autorizado descenso a uno cero mil pies"

Tras terminar este escenario, se le hace la retroalimentación al piloto de los parámetros de vuelo, problemas de comunicación, seguimiento de ordenes etc. El alumno tuvo en hipoxia y recordó que en el primer síntoma hay que recuperarse accionando el regulador con las tres palancas hacia arriba.""",
            "Script Fixed-Wing": """
Welcome to the normobaric hypoxia training conducted by the Aerospace Medicine Directorate. This training is designed to help you recognize the symptoms of hypoxia and perform recovery procedures using the PRICE checklist reviewed in class. We will present you with a flight simulation scenario in PREPAR3D where you will be in command of an aircraft at an altitude of 10,000 ft, and I will provide specific instructions on the procedures you need to perform. It is important to note that this is not a flight skills evaluation or a precise simulation of any particular aircraft but rather training to help you identify the effects of altitude on human performance in the cockpit.

As reviewed in class, you should recognize the symptoms of hypoxia, and upon the appearance of the first symptom, perform the PRICE checklist and correct it by manipulating the regulator with the three levers up, following the instructor's instructions.

We will verify the simulator in the following order:

1. Seating adjustment

2. Fastening seatbelts

3. Helmet and mask adaptation to be put on at the instructor's command

4. The instructor will show the pedals, control stick or yoke, and the throttle quadrant. No other simulator controls or specific configurations will be required, as all manual control must be executed by the student.

When loading the flight in Prepar3D, the instructor should pause the simulator to start the flight. The profile is executed in the ROBD, and once it begins, the following instructions should be given:

"TH250, Bogotá radar. Turn right heading 130, climb and maintain fifteen thousand feet at a rate of 500 ft/min."

The student should read back as follows:

"Bogotá Radar, turning right heading 130, climbing and maintaining fifteen thousand feet at 500 ft/min, TH250."

Upon completing the ATC order, the instructor will give another order following the scheme:

"TH250, Bogotá radar. Turn right heading "210", climb and maintain "seventeen thousand feet."

During the flight, the instructor should ask the student:

"What should you do upon experiencing a hypoxia symptom?"

After performing the recovery, the pilot must communicate with ATC to declare the emergency and request a descent to ten thousand feet, and ATC should authorize the student:

"TH250, Bogotá Radar, cleared to descend to ten thousand feet."

After completing this scenario, the pilot will receive feedback on flight parameters, communication issues, adherence to orders, etc., experienced during hypoxia. It is crucial to remember that upon the first symptom, recovery is necessary by operating the regulator with the three levers up.

Night Vision Training Procedure:

During hypoxia, the reduction of oxygen in the body significantly affects the function of the cones in the retina, responsible for color perception and visual acuity. In hypoxic conditions, the cones' ability to function correctly is diminished, leading to decreased color sensitivity and visual acuity.

This is particularly critical during night flights, where vision is already compromised by the lack of light. Hypoxia can make colors less distinguishable and objects in the environment harder to identify, which can lead to errors in interpreting signals and instruments in the aircraft.

It is essential to recognize these symptoms and act quickly. At the first sign of hypoxia, you should perform the PRICE checklist and adjust the oxygen supply using the regulator with the three levers up. This will help restore adequate oxygen levels and improve your visual and cognitive capacity, reducing the risk of errors during night flights.

Remember that in conditions of low visibility and high cognitive demand, such as night flights, hypoxia can be particularly dangerous, so vigilance and immediate correction are crucial.

1. The navigation chart AD 2 SKGY - CHIA - FLAMINIO SUAREZ CAMACHO is presented in printed form.

2. The night vision profile is executed in the ROBD2.

3. On the SKGY Visual OACI Chart, identify the aerodrome and point out the mountains between 8400 and 10200 ft.

4. State the sequence of points in the VFR standardized departure to ECHO between BIMA and TIBITOC.

5. Read the content of the red boxes on the chart.

6. The instructor presses "Oxygen Dump" and waits one minute for recovery.

The student should observe the difference in colors during hypoxia and when 100% oxygen is supplied. Explain the implications of interpreting aeronautical signals in hypoxia under dark conditions, which can lead the pilot to misinterpret signals and thus commit errors in the cockpit.""",
            "Script Rotary Wing": """
Welcome to the normobaric hypoxia training conducted by the Aerospace Medicine Directorate. This training is designed to help you recognize the symptoms of hypoxia and perform recovery procedures using the PRICE checklist reviewed in class. We will present you with a flight simulation scenario in PREPAR3D where you will be in command of an aircraft at an altitude of 10,000 ft, and I will provide specific instructions on the procedures you need to perform. It is important to note that this is not a flight skills evaluation or a precise simulation of any particular aircraft but rather training to help you identify the effects of altitude on human performance in the cockpit.

As reviewed in class, you should recognize the symptoms of hypoxia, and upon the appearance of the first symptom, perform the PRICE checklist and correct it by manipulating the regulator with the three levers up, following the instructor's instructions.

We will verify the simulator in the following order:

1. Seating adjustment

2. Fastening seatbelts

3. Helmet and mask adaptation to be put on at the instructor's command

4. The instructor will show the pedals, control stick or yoke, and the throttle quadrant. No other simulator controls or specific configurations will be required, as all manual control must be executed by the student.

When loading the flight in Prepar3D, the instructor should pause the simulator to start the flight. The profile is executed in the ROBD, and once it begins, the following instructions should be given:

"TH250, Bogotá radar. Turn right heading 130, climb and maintain fifteen thousand feet at a rate of 500 ft/min."

The student should read back as follows:

"Bogotá Radar, turning right heading 130, climbing and maintaining fifteen thousand feet at 500 ft/min, TH250."

Upon completing the ATC order, the instructor will give another order following the scheme:

"TH250, Bogotá radar. Turn right heading "210", climb and maintain "seventeen thousand feet."

During the flight, the instructor should ask the student:

"What should you do upon experiencing a hypoxia symptom?"

After performing the recovery, the pilot must communicate with ATC to declare the emergency and request a descent to ten thousand feet, and ATC should authorize the student:

"TH250, Bogotá Radar, cleared to descend to ten thousand feet."

After completing this scenario, the pilot will receive feedback on flight parameters, communication issues, adherence to orders, etc., experienced during hypoxia. It is crucial to remember that upon the first symptom, recovery is necessary by operating the regulator with the three levers up.

Night Vision Training Procedure:

During hypoxia, the reduction of oxygen in the body significantly affects the function of the cones in the retina, responsible for color perception and visual acuity. In hypoxic conditions, the cones' ability to function correctly is diminished, leading to decreased color sensitivity and visual acuity.

This is particularly critical during night flights, where vision is already compromised by the lack of light. Hypoxia can make colors less distinguishable and objects in the environment harder to identify, which can lead to errors in interpreting signals and instruments in the aircraft.

It is essential to recognize these symptoms and act quickly. At the first sign of hypoxia, you should perform the PRICE checklist and adjust the oxygen supply using the regulator with the three levers up. This will help restore adequate oxygen levels and improve your visual and cognitive capacity, reducing the risk of errors during night flights.

Remember that in conditions of low visibility and high cognitive demand, such as night flights, hypoxia can be particularly dangerous, so vigilance and immediate correction are crucial.

1. The navigation chart AD 2 SKGY - CHIA - FLAMINIO SUAREZ CAMACHO is presented in printed form.

2. The night vision profile is executed in the ROBD2.

3. On the SKGY Visual OACI Chart, identify the aerodrome and point out the mountains between 8400 and 10200 ft.

4. State the sequence of points in the VFR standardized departure to ECHO between BIMA and TIBITOC.

5. Read the content of the red boxes on the chart.

6. The instructor presses "Oxygen Dump" and waits one minute for recovery.

The student should observe the difference in colors during hypoxia and when 100% oxygen is supplied. Explain the implications of interpreting aeronautical signals in hypoxia under dark conditions, which can lead the pilot to misinterpret signals and thus commit errors in the cockpit."""
        }
        
        return script_mapping.get(script_name, None)

    def create_diagnostics_tab(self):
        """Create the diagnostics tab"""
        diagnostics_frame = ModernFrame(self.notebook)
        self.notebook.add(diagnostics_frame, text="Diagnostics")
        
        # Create left and right frames
        left_frame = ttk.Frame(diagnostics_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        right_frame = ttk.Frame(diagnostics_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Command buttons
        commands_frame = ttk.LabelFrame(left_frame, text="Diagnostic Commands", padding=10)
        commands_frame.pack(fill=tk.BOTH, expand=True)
        
        commands = [
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
            ("Get System Status", "GET STATUS")
        ]
        
        for text, command in commands:
            btn = ModernButton(
                commands_frame,
                text=text,
                command=lambda cmd=command: self.send_diagnostic_command(cmd),
                state=tk.DISABLED
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Response display
        response_frame = ttk.LabelFrame(right_frame, text="Response", padding=10)
        response_frame.pack(fill=tk.BOTH, expand=True)
        
        self.response_text = tk.Text(response_frame, height=20, wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)

    def create_programming_tab(self):
        """Create the programming tab"""
        programming_frame = ModernFrame(self.notebook)
        self.notebook.add(programming_frame, text="Programming")
        
        # Create left and right frames
        left_frame = ttk.Frame(programming_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        right_frame = ttk.Frame(programming_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Program creation
        create_frame = ttk.LabelFrame(left_frame, text="Program Creation", padding=10)
        create_frame.pack(fill=tk.BOTH, expand=True)
        
        # Program number
        prog_frame = ttk.Frame(create_frame)
        prog_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prog_frame, text="Program Number:").pack(side=tk.LEFT)
        self.prog_num_var = tk.StringVar()
        self.prog_num_combo = ttk.Combobox(
            prog_frame,
            textvariable=self.prog_num_var,
            values=[str(i) for i in range(1, 20)]
        )
        self.prog_num_combo.pack(side=tk.LEFT, padx=5)
        
        # Program name
        name_frame = ttk.Frame(create_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Program Name:").pack(side=tk.LEFT)
        self.prog_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.prog_name_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Program mode
        mode_frame = ttk.Frame(create_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        ttk.Label(mode_frame, text="Program Mode:").pack(side=tk.LEFT)
        self.prog_mode_var = tk.StringVar()
        mode_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.prog_mode_var,
            values=['HRT', 'FSHT', 'OSFT']
        )
        mode_combo.pack(side=tk.LEFT, padx=5)
        
        # Step controls
        step_frame = ttk.LabelFrame(create_frame, text="Step Controls", padding=10)
        step_frame.pack(fill=tk.X, pady=5)
        
        self.add_hold_btn = ModernButton(
            step_frame,
            text="Add Hold Step",
            command=self.add_hold_step,
            state=tk.DISABLED
        )
        self.add_hold_btn.pack(fill=tk.X, pady=2)
        
        self.add_change_btn = ModernButton(
            step_frame,
            text="Add Change Step",
            command=self.add_change_step,
            state=tk.DISABLED
        )
        self.add_change_btn.pack(fill=tk.X, pady=2)
        
        # Program review
        review_frame = ttk.LabelFrame(right_frame, text="Program Review", padding=10)
        review_frame.pack(fill=tk.BOTH, expand=True)
        
        self.program_text = tk.Text(review_frame, height=20, wrap=tk.WORD)
        self.program_text.pack(fill=tk.BOTH, expand=True)

    def create_logging_tab(self):
        """Create the logging tab"""
        logging_frame = ModernFrame(self.notebook)
        self.notebook.add(logging_frame, text="Logging")
        
        # Logging controls
        control_frame = ttk.LabelFrame(logging_frame, text="Logging Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Flight ID
        id_frame = ttk.Frame(control_frame)
        id_frame.pack(fill=tk.X, pady=5)
        ttk.Label(id_frame, text="Flight ID:").pack(side=tk.LEFT)
        self.flight_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.flight_id_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Control buttons
        self.start_logging_btn = ModernButton(
            control_frame,
            text="Start Logging",
            command=self.start_logging,
            state=tk.DISABLED
        )
        self.start_logging_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_logging_btn = ModernButton(
            control_frame,
            text="Stop Logging",
            command=self.stop_logging,
            state=tk.DISABLED
        )
        self.stop_logging_btn.pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_frame = ttk.LabelFrame(logging_frame, text="Log Display", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def refresh_ports(self):
        """Refresh available COM ports"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
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
            
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            self.is_connected = True
            
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
            
            # Destroy loading indicator
            loading.destroy()
            
        except serial.SerialException as e:
            log.error(f"Serial connection error: {e}", exc_info=True)
            messagebox.showerror("Connection Error", f"Failed to connect to {port}: {str(e)}")
            self.status_bar.configure(text="Connection Failed")
            self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Connection failed: {str(e)}\n")
        except Exception as e:
            log.error(f"Unexpected connection error: {e}", exc_info=True)
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_bar.configure(text="Connection Failed")
            self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - Unexpected error: {str(e)}\n")

    def disconnect_device(self):
        """Disconnect from the COM port"""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                self.is_connected = False
                
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
                
            except Exception as e:
                log.error(f"Error disconnecting: {e}", exc_info=True)
                messagebox.showerror("Error", f"Failed to disconnect: {str(e)}")

    def process_commands(self):
        """Process commands from the queue"""
        while True:
            try:
                command = self.command_queue.get(timeout=0.1)  # Add timeout to prevent blocking
                if command is None:
                    break
                    
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.write(command.encode('utf-8'))
                    
            except queue.Empty:
                # Just continue if queue is empty
                continue
            except Exception as e:
                log.error(f"Error processing command: {e}")
                self.response_queue.put(f"Error: {str(e)}")

    def poll_responses(self):
        """Poll for responses without blocking the main thread"""
        try:
            if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting:
                response = self.serial_port.readline().decode('utf-8').rstrip()
                if response:
                    self.response_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} ← {response}\n")
                    self.response_text.see(tk.END)  # Auto-scroll to the end
            
            # Process any items in the response queue
            while not self.response_queue.empty():
                try:
                    response = self.response_queue.get_nowait()
                    self.response_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} ← {response}\n")
                    self.response_text.see(tk.END)
                except queue.Empty:
                    break
                    
        except Exception as e:
            log.error(f"Error polling response: {e}")
            
        # Schedule the next poll
        self.root.after(100, self.poll_responses)

    def send_diagnostic_command(self, command):
        """Send a diagnostic command to the device"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        self.command_queue.put(f"{command}\r\n")
        self.response_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} → {command}\n")

    def start_calibration(self):
        """Start O2 sensor calibration"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        device_id = self.device_var.get()
        if not device_id:
            messagebox.showerror("Error", "Please select a device")
            return
            
        # Run calibration in a separate thread to avoid blocking the UI
        def run_calibration():
            monitor = CalibrationMonitor(self.serial_port)
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
        if not self.is_connected:
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
                    self.performance_monitor = PerformanceMonitor(self.serial_port)
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
        if not self.is_connected:
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
        
        # Run logging in a separate thread
        def run_logging():
            self.data_logger = DataLogger(self.serial_port, [])
            
            # Update the log display
            def update_log(message):
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END)
                log.info(message)
                
            # Store the original communications list append method
            original_append = self.data_logger.communications.append
            
            # Override the append method to update the UI
            def new_append(message):
                original_append(message)
                self.root.after(0, lambda: update_log(message))
                
            self.data_logger.communications.append = new_append
            
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

    def add_hold_step(self):
        """Add a hold step to the program"""
        # Implementation for adding hold step
        pass

    def add_change_step(self):
        """Add a change step to the program"""
        # Implementation for adding change step
        pass

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

def main():
    try:
        root = tk.Tk()
        app = ROBD2GUI(root)
        
        def on_closing():
            """Handle application closing"""
            if hasattr(app, 'serial_port') and app.serial_port and app.serial_port.is_open:
                app.serial_port.close()
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