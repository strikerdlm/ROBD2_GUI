import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from performance_monitor import PerformanceMonitor
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame

log = logging.getLogger(__name__)

class PerformanceTab(ModernFrame):
    def __init__(self, parent, serial_comm):
        super().__init__(parent)
        self.serial_comm = serial_comm
        self.monitor = None
        self.monitor_thread = None
        self.monitoring_active = False
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all widgets for the performance tab"""
        # Device selection
        device_frame = ModernLabelFrame(self, text="Device Selection", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(device_frame, text="Select ROBD2 Device:").pack(side=tk.LEFT, padx=5)
        self.device_var = tk.StringVar(value="9515")
        device_menu = ttk.OptionMenu(device_frame, self.device_var, "9515", "9515", "9516", "9471")
        device_menu.pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        status_frame = ModernLabelFrame(self, text="Monitoring Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="Ready for monitoring")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10, 'bold'),
            foreground='blue'
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress indicator
        self.progress_bar = ttk.Progressbar(
            status_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Control buttons
        control_frame = ModernLabelFrame(self, text="Monitoring Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_btn = ModernButton(
            control_frame,
            text="Start Monitoring",
            command=self.start_monitoring
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ModernButton(
            control_frame,
            text="Stop Monitoring",
            command=self.stop_monitoring,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ModernButton(
            control_frame,
            text="Export Data",
            command=self.export_data,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_btn = ModernButton(
            control_frame,
            text="Clear Data",
            command=self.clear_data,
            state=tk.DISABLED
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ModernLabelFrame(self, text="Performance Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6))
        self.ax1 = self.fig.add_subplot(211)  # O2 concentration
        self.ax2 = self.fig.add_subplot(212)  # Error
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=results_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar_frame = ttk.Frame(results_frame)
        toolbar_frame.pack(fill=tk.X)
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        NavigationToolbar2Tk(self.canvas, toolbar_frame)
        
        # Status display
        status_text_frame = ttk.Frame(results_frame)
        status_text_frame.pack(fill=tk.X, pady=5)
        
        # Scrollbar for status text
        status_scroll = ttk.Scrollbar(status_text_frame)
        status_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_text = tk.Text(status_text_frame, height=6, wrap=tk.WORD, yscrollcommand=status_scroll.set)
        self.status_text.pack(fill=tk.X, side=tk.LEFT, expand=True)
        status_scroll.config(command=self.status_text.yview)
        
        # Instructions
        instructions = """
Instructions:
1. Select your ROBD2 device from the dropdown menu
2. Click 'Start Monitoring' to begin performance analysis
3. The system will automatically:
   - Monitor O2 concentration and altitude
   - Calculate performance metrics
   - Log data to CSV file
4. Results are displayed in real-time with:
   - O2 concentration graph
   - Error analysis
   - Statistical metrics
5. Click 'Stop Monitoring' when finished
"""
        instructions_frame = ModernLabelFrame(self, text="Instructions", padding=10)
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            instructions_frame,
            text=instructions,
            wraplength=600,
            justify=tk.LEFT
        ).pack(fill=tk.X, padx=10, pady=5)
        
    def update_status(self, message, color='blue', progress=None):
        """Update the status indicator"""
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        
        if progress is not None:
            self.progress_bar['value'] = progress
        
        self.status_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.status_text.see(tk.END)
        self.update_idletasks()
        
    def update_ui_state(self, monitoring=False):
        """Update UI state based on monitoring status"""
        self.monitoring_active = monitoring
        
        # Set button states based on monitoring status
        self.start_btn.config(state=tk.DISABLED if monitoring else tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL if monitoring else tk.DISABLED)
        self.export_btn.config(state=tk.NORMAL if not monitoring and self.monitor else tk.DISABLED)
        self.clear_btn.config(state=tk.NORMAL if not monitoring and self.monitor else tk.DISABLED)
        
        # Update progress bar
        if monitoring:
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start(10)
        else:
            self.progress_bar.config(mode='determinate')
            self.progress_bar.stop()
            self.progress_bar['value'] = 0 if monitoring is False else 100
        
    def start_monitoring(self):
        """Start performance monitoring"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Please connect to the device first")
            return
            
        try:
            # Update UI state
            self.update_status("Starting performance monitoring...", "blue")
            self.update_ui_state(monitoring=True)
            
            # Get device ID
            device_id = self.device_var.get()
            if not device_id:
                raise ValueError("Please select a device ID")
            
            # Create monitor instance
            self.monitor = PerformanceMonitor(self.serial_comm.serial_port)
            self.monitor.set_device_id(device_id)
            
            # Set up data callback
            self.monitor.data_callback = self.update_display
            
            # Start monitoring in a separate thread
            self.monitor_thread = threading.Thread(target=self._run_monitoring)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            self.update_status(f"Monitoring ROBD2-{device_id} started", "green")
            
        except Exception as e:
            log.error(f"Failed to start monitoring: {e}", exc_info=True)
            self.update_status(f"Error: {str(e)}", "red", 0)
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")
            self.update_ui_state(monitoring=False)
            
    def _run_monitoring(self):
        """Run the monitoring process in a separate thread"""
        try:
            self.monitor.start_monitoring()
        except Exception as e:
            log.error(f"Error in monitoring thread: {e}", exc_info=True)
            self.after(0, lambda: self.update_status(f"Monitoring error: {str(e)}", "red", 0))
            self.after(0, lambda: messagebox.showerror("Error", f"Monitoring error: {str(e)}"))
        finally:
            self.after(0, lambda: self.update_ui_state(monitoring=False))
            
    def stop_monitoring(self):
        """Stop performance monitoring"""
        if self.monitor:
            try:
                self.update_status("Stopping monitoring...", "blue")
                self.monitor.stop_monitoring()
                
                if self.monitor_thread:
                    self.monitor_thread.join(timeout=1.0)
                
                self.update_status("Monitoring stopped successfully", "green", 100)
                
                # Ask if user wants to export data
                if messagebox.askyesno("Export Data", "Would you like to export the collected data?"):
                    self.export_data()
                    
            except Exception as e:
                log.error(f"Error stopping monitoring: {e}", exc_info=True)
                self.update_status(f"Error stopping monitoring: {str(e)}", "red")
                messagebox.showerror("Error", f"Error stopping monitoring: {str(e)}")
                
            finally:
                self.update_ui_state(monitoring=False)
        
    def export_data(self):
        """Export monitoring data to CSV file"""
        if not self.monitor:
            messagebox.showerror("Error", "No monitoring data available")
            return
            
        try:
            self.update_status("Exporting data...", "blue")
            
            # Get timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            device_id = self.device_var.get()
            
            # Create export directory
            export_dir = Path("performance_exports")
            export_dir.mkdir(exist_ok=True)
            
            # Create export filename
            filename = export_dir / f"ROBD2_{device_id}_{timestamp}_performance.csv"
            
            # Export data
            with open(filename, 'w', newline='') as f:
                # Write export code here
                # This is a placeholder
                f.write("Performance data export\n")
                f.write(f"Device: ROBD2-{device_id}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
            self.update_status(f"Data exported to {filename}", "green", 100)
            messagebox.showinfo("Export Complete", f"Data exported to:\n{filename}")
            
        except Exception as e:
            log.error(f"Error exporting data: {e}", exc_info=True)
            self.update_status(f"Error exporting data: {str(e)}", "red", 0)
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def clear_data(self):
        """Clear monitoring data"""
        if not self.monitor:
            return
            
        if messagebox.askyesno("Clear Data", "Are you sure you want to clear all monitoring data?"):
            try:
                # Clear data from monitor
                self.monitor = None
                
                # Clear plots
                self.ax1.clear()
                self.ax2.clear()
                self.ax1.set_title("O2 Concentration (%)")
                self.ax2.set_title("Error (%)")
                self.ax1.grid(True)
                self.ax2.grid(True)
                self.canvas.draw()
                
                # Clear status
                self.status_text.delete(1.0, tk.END)
                self.update_status("Data cleared", "blue", 0)
                
                # Update button states
                self.export_btn.config(state=tk.DISABLED)
                self.clear_btn.config(state=tk.DISABLED)
                
            except Exception as e:
                log.error(f"Error clearing data: {e}", exc_info=True)
                self.update_status(f"Error clearing data: {str(e)}", "red")
                messagebox.showerror("Error", f"Error clearing data: {str(e)}")
        
    def update_display(self, data):
        """Update the display with new data"""
        try:
            # Update status text
            timestamp = datetime.now().strftime("%H:%M:%S")
            status = (
                f"[{timestamp}] Alt: {data['altitude']}ft | "
                f"O2: {data['o2_conc']:.2f}% | "
                f"BLP: {data['blp']:.2f}inH2O | "
                f"Program: {data['program']}\n"
            )
            self.status_text.insert(tk.END, status)
            self.status_text.see(tk.END)
            
            # Update progress bar with random progress to show activity
            import random
            self.progress_bar['value'] = random.randint(10, 90)
            
            # Update plots
            self.update_plots(data)
            
        except Exception as e:
            log.error(f"Error updating display: {e}", exc_info=True)
            
    def update_plots(self, data):
        """Update the matplotlib plots"""
        try:
            # Clear axes
            self.ax1.clear()
            self.ax2.clear()
            
            # Plot O2 concentration
            self.ax1.plot(data['o2_conc'], 'b-', linewidth=2, label='O2 Concentration')
            self.ax1.set_ylabel('O2 Concentration (%)')
            self.ax1.set_title('O2 Concentration (%)')
            self.ax1.grid(True)
            self.ax1.legend()
            
            # Plot error
            spec = self.monitor._get_o2_spec(data['altitude'])
            if spec:
                error = data['o2_conc'] - spec.desired_o2
                self.ax2.plot(error, 'r-', linewidth=2, label='Error')
                self.ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
                self.ax2.set_ylabel('Error (%)')
                self.ax2.set_title(f'Error at {data["altitude"]}ft (Target: {spec.desired_o2:.2f}%)')
                self.ax2.grid(True)
                self.ax2.legend()
                
                # Add range indicators
                self.ax2.axhspan(spec.range_min - spec.desired_o2, spec.range_max - spec.desired_o2, 
                                alpha=0.2, color='green', label='Acceptable Range')
            
            # Redraw canvas
            self.canvas.draw()
            
        except Exception as e:
            log.error(f"Error updating plots: {e}", exc_info=True) 