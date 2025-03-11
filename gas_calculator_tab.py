import tkinter as tk
from tkinter import ttk, messagebox
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Dict, Any, Optional
import logging
import sys

log = logging.getLogger(__name__)

class GasCalculatorTab(ModernFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.active_scrollables = []  # Keep track of scrollable widgets
        self.notebook = None
        self.create_widgets()
        
    def create_widgets(self):
        """Create all widgets for the gas calculator tab"""
        # Create notebook for different calculation types
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_physiological_tab()
        self.create_consumption_tab()
        self.create_capacity_tab()
        self.create_single_session_tab()
        
        # Bind cleanup to tab change
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
    def _on_tab_changed(self, event):
        """Handle tab changes by ensuring scrolling works properly"""
        try:
            # Re-enable scrolling when switching tabs
            self.cleanup_scrolling()
        except Exception as e:
            log.error(f"Error handling tab change: {e}")
            
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
                                self.unbind_all(event)
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
            
    def destroy(self):
        """Clean up resources when the widget is destroyed"""
        self.cleanup_scrolling()
        super().destroy()
        
    def _setup_scrolling(self, canvas):
        """Set up scrolling for a canvas"""
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    if sys.platform.startswith('win'):
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    else:
                        if event.num == 4:
                            canvas.yview_scroll(-1, "units")
                        elif event.num == 5:
                            canvas.yview_scroll(1, "units")
            except tk.TclError:
                pass

        # Store the widget and its bindings for cleanup
        if sys.platform.startswith('win'):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self.active_scrollables.append({
                'widget': canvas,
                'bindings': [("<MouseWheel>", _on_mousewheel)]
            })
        else:
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)
            self.active_scrollables.append({
                'widget': canvas,
                'bindings': [
                    ("<Button-4>", _on_mousewheel),
                    ("<Button-5>", _on_mousewheel)
                ]
            })
        
    def create_physiological_tab(self):
        """Create the physiological parameters calculation tab"""
        frame = ModernFrame(self.notebook)
        self.notebook.add(frame, text="Physiological Parameters")
        
        # Input frame at the top
        input_frame = ModernLabelFrame(frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Altitude input
        altitude_frame = ttk.Frame(input_frame)
        altitude_frame.pack(fill=tk.X, pady=5)
        ttk.Label(altitude_frame, text="Altitude (ft):").pack(side=tk.LEFT, padx=5)
        self.altitude_var = tk.StringVar(value="25000")
        altitude_entry = ttk.Entry(altitude_frame, textvariable=self.altitude_var, width=10)
        altitude_entry.pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calc_btn = ModernButton(
            input_frame,
            text="Calculate Parameters",
            command=self.calculate_physiological
        )
        calc_btn.pack(pady=10)
        
        # Create paned window for results and graph
        results_pane = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        results_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left pane - Graph
        graph_frame = ModernLabelFrame(results_pane, text="Visualization", padding=10)
        results_pane.add(graph_frame, weight=2)
        
        # Create matplotlib figure for visualization
        self.physio_fig = Figure(figsize=(8, 6))
        self.physio_canvas = FigureCanvasTkAgg(self.physio_fig, master=graph_frame)
        self.physio_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right pane - Results
        self.physio_results_frame = ModernLabelFrame(results_pane, text="Results", padding=10)
        results_pane.add(self.physio_results_frame, weight=1)
        
        # Style for result labels
        style = ttk.Style()
        style.configure("Result.TLabel", font=('Helvetica', 10))
        
        # Create a canvas for the results with scrollbar
        results_canvas = tk.Canvas(self.physio_results_frame)
        results_scrollbar = ttk.Scrollbar(self.physio_results_frame, orient="vertical", command=results_canvas.yview)
        results_scrollable_frame = ttk.Frame(results_canvas)
        
        results_scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_scrollbar.pack(side="right", fill="y")
        results_canvas.pack(side="left", fill="both", expand=True)
        
        # Set up scrolling for this canvas
        self._setup_scrolling(results_canvas)
        
        # Store the scrollable frame reference
        self.physio_results_scrollable_frame = results_scrollable_frame

    def calculate_physiological(self):
        """Calculate physiological parameters"""
        try:
            altitude = float(self.altitude_var.get())
            
            # Calculate parameters using the formulas from GasCalc_updated.py
            altitude_m = altitude * 0.3048
            pressure_at_altitude = 760 * (1 - (2.25577e-5 * altitude_m)) ** 5.25588
            FiO2 = 0.2095
            PiO2 = (pressure_at_altitude - 47) * FiO2
            PaO2 = PiO2 - 5
            SaO2 = 100 * (PaO2 ** 3) / (PaO2 ** 3 + 150 ** 3)
            
            # Calculate ventilation rate
            altitude_above_1500_m = max(0, altitude_m - 1500)
            ventilation_increase_factor = (altitude_above_1500_m / 1000)
            ventilation_rate = 6 * (1 + ventilation_increase_factor)
            ventilation_rate = min(ventilation_rate, 60)
            
            # Calculate heart rate
            altitude_above_1000_m = max(0, altitude_m - 1000)
            heart_rate_increase = altitude_above_1000_m / 100
            heart_rate = 70 + heart_rate_increase
            
            # Clear previous results
            for widget in self.physio_results_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Display results with modern styling
            results = [
                ("Altitude", f"{altitude:.0f} ft ({altitude_m:.1f} m)"),
                ("Pressure at Altitude", f"{pressure_at_altitude:.1f} mmHg"),
                ("PaO2", f"{PaO2:.1f} mmHg"),
                ("SaO2", f"{SaO2:.1f}%"),
                ("Ventilation Rate", f"{ventilation_rate:.1f} L/min"),
                ("Heart Rate", f"{heart_rate:.1f} bpm")
            ]
            
            # Create a modern result display
            for i, (label, value) in enumerate(results):
                result_frame = ttk.Frame(self.physio_results_scrollable_frame)
                result_frame.pack(fill=tk.X, pady=5, padx=5)
                
                # Label in bold
                ttk.Label(
                    result_frame,
                    text=label + ":",
                    style="Result.TLabel",
                    font=('Helvetica', 10, 'bold')
                ).pack(anchor="w")
                
                # Value
                ttk.Label(
                    result_frame,
                    text=value,
                    style="Result.TLabel"
                ).pack(anchor="w", padx=10)
                
                # Add separator except for last item
                if i < len(results) - 1:
                    ttk.Separator(self.physio_results_scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
            
            # Update visualization
            self.physio_fig.clear()
            ax = self.physio_fig.add_subplot(111)
            
            # Create bar chart of key parameters
            params = ['SaO2', 'PaO2', 'Ventilation\nRate', 'Heart\nRate']
            values = [SaO2, PaO2, ventilation_rate, heart_rate]
            
            bars = ax.bar(params, values)
            ax.set_title('Physiological Parameters')
            ax.set_ylabel('Value')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom')
            
            # Customize the appearance
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=0)
            
            # Adjust layout
            self.physio_fig.tight_layout()
            self.physio_canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            log.error(f"Error in physiological calculation: {e}")
            
    def create_consumption_tab(self):
        """Create the gas consumption calculation tab"""
        frame = ModernFrame(self.notebook)
        self.notebook.add(frame, text="Gas Consumption")
        
        # Input frame
        input_frame = ModernLabelFrame(frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create input fields
        inputs = [
            ("Number of Students per Week:", "students_per_week", "20"),
            ("Number of Weeks:", "weeks", "26"),
            ("Session Duration (minutes):", "session_duration", "20"),
            ("Recovery Duration (minutes):", "recovery_duration", "5"),
            ("Altitude (ft):", "altitude", "25000"),
            ("Price of Air (COP/m³):", "price_air", "17853"),
            ("Price of Nitrogen (COP/m³):", "price_nitrogen", "17838"),
            ("Price of Oxygen (COP/m³):", "price_oxygen", "19654"),
            ("Contingency Percentage:", "contingency", "0.10")
        ]
        
        self.consumption_vars = {}
        for label, var_name, default in inputs:
            frame_row = ttk.Frame(input_frame)
            frame_row.pack(fill=tk.X, pady=2)
            ttk.Label(frame_row, text=label).pack(side=tk.LEFT, padx=5)
            var = tk.StringVar(value=default)
            self.consumption_vars[var_name] = var
            ttk.Entry(frame_row, textvariable=var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calc_btn = ModernButton(
            input_frame,
            text="Calculate Consumption",
            command=self.calculate_consumption
        )
        calc_btn.pack(pady=10)
        
        # Create paned window for results and graph
        results_pane = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        results_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left pane - Graph
        graph_frame = ModernLabelFrame(results_pane, text="Cost Distribution", padding=10)
        results_pane.add(graph_frame, weight=2)
        
        # Create matplotlib figure for visualization
        self.consumption_fig = Figure(figsize=(8, 6))
        self.consumption_canvas = FigureCanvasTkAgg(self.consumption_fig, master=graph_frame)
        self.consumption_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right pane - Results
        self.consumption_results_frame = ModernLabelFrame(results_pane, text="Results", padding=10)
        results_pane.add(self.consumption_results_frame, weight=1)
        
        # Create scrollable results area
        results_canvas = tk.Canvas(self.consumption_results_frame)
        results_scrollbar = ttk.Scrollbar(self.consumption_results_frame, orient="vertical", command=results_canvas.yview)
        self.consumption_results_scrollable_frame = ttk.Frame(results_canvas)
        
        self.consumption_results_scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=self.consumption_results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_scrollbar.pack(side="right", fill="y")
        results_canvas.pack(side="left", fill="both", expand=True)
        
        # Set up scrolling for this canvas
        self._setup_scrolling(results_canvas)
        
    def create_capacity_tab(self):
        """Create the cylinder capacity calculation tab"""
        frame = ModernFrame(self.notebook)
        self.notebook.add(frame, text="Cylinder Capacity")
        
        # Input frame
        input_frame = ModernLabelFrame(frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create input fields
        inputs = [
            ("Air Cylinder Volume (m³):", "air_cylinder", "10"),
            ("Nitrogen Cylinder Volume (m³):", "nitrogen_cylinder", "9"),
            ("Oxygen Cylinder Volume (m³):", "oxygen_cylinder", "10"),
            ("Session Duration (minutes):", "session_duration", "20"),
            ("Recovery Duration (minutes):", "recovery_duration", "5"),
            ("Altitude (ft):", "altitude", "25000")
        ]
        
        self.capacity_vars = {}
        for label, var_name, default in inputs:
            frame_row = ttk.Frame(input_frame)
            frame_row.pack(fill=tk.X, pady=2)
            ttk.Label(frame_row, text=label).pack(side=tk.LEFT, padx=5)
            var = tk.StringVar(value=default)
            self.capacity_vars[var_name] = var
            ttk.Entry(frame_row, textvariable=var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calc_btn = ModernButton(
            input_frame,
            text="Calculate Capacity",
            command=self.calculate_capacity
        )
        calc_btn.pack(pady=10)
        
        # Create paned window for results and graph
        results_pane = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        results_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left pane - Graph
        graph_frame = ModernLabelFrame(results_pane, text="Maximum Students per Gas Type", padding=10)
        results_pane.add(graph_frame, weight=2)
        
        # Create matplotlib figure for visualization
        self.capacity_fig = Figure(figsize=(8, 6))
        self.capacity_canvas = FigureCanvasTkAgg(self.capacity_fig, master=graph_frame)
        self.capacity_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right pane - Results
        self.capacity_results_frame = ModernLabelFrame(results_pane, text="Results", padding=10)
        results_pane.add(self.capacity_results_frame, weight=1)
        
        # Create scrollable results area
        results_canvas = tk.Canvas(self.capacity_results_frame)
        results_scrollbar = ttk.Scrollbar(self.capacity_results_frame, orient="vertical", command=results_canvas.yview)
        self.capacity_results_scrollable_frame = ttk.Frame(results_canvas)
        
        self.capacity_results_scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=self.capacity_results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_scrollbar.pack(side="right", fill="y")
        results_canvas.pack(side="left", fill="both", expand=True)
        
        # Set up scrolling for this canvas
        self._setup_scrolling(results_canvas)
        
    def create_single_session_tab(self):
        """Create the single session calculation tab"""
        frame = ModernFrame(self.notebook)
        self.notebook.add(frame, text="Single Session")
        
        # Input frame
        input_frame = ModernLabelFrame(frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create input fields
        inputs = [
            ("Session Duration (minutes):", "session_duration", "20"),
            ("Recovery Duration (minutes):", "recovery_duration", "5"),
            ("Altitude (ft):", "altitude", "25000"),
            ("Price of Air (COP/m³):", "price_air", "17853"),
            ("Price of Nitrogen (COP/m³):", "price_nitrogen", "17838"),
            ("Price of Oxygen (COP/m³):", "price_oxygen", "19654")
        ]
        
        self.session_vars = {}
        for label, var_name, default in inputs:
            frame_row = ttk.Frame(input_frame)
            frame_row.pack(fill=tk.X, pady=2)
            ttk.Label(frame_row, text=label).pack(side=tk.LEFT, padx=5)
            var = tk.StringVar(value=default)
            self.session_vars[var_name] = var
            ttk.Entry(frame_row, textvariable=var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calc_btn = ModernButton(
            input_frame,
            text="Calculate Session",
            command=self.calculate_single_session
        )
        calc_btn.pack(pady=10)
        
        # Create paned window for results and graph
        results_pane = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        results_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left pane - Graph
        graph_frame = ModernLabelFrame(results_pane, text="Cost Distribution", padding=10)
        results_pane.add(graph_frame, weight=2)
        
        # Create matplotlib figure for visualization
        self.session_fig = Figure(figsize=(8, 6))
        self.session_canvas = FigureCanvasTkAgg(self.session_fig, master=graph_frame)
        self.session_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right pane - Results
        self.session_results_frame = ModernLabelFrame(results_pane, text="Results", padding=10)
        results_pane.add(self.session_results_frame, weight=1)
        
        # Create scrollable results area
        results_canvas = tk.Canvas(self.session_results_frame)
        results_scrollbar = ttk.Scrollbar(self.session_results_frame, orient="vertical", command=results_canvas.yview)
        self.session_results_scrollable_frame = ttk.Frame(results_canvas)
        
        self.session_results_scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=self.session_results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_scrollbar.pack(side="right", fill="y")
        results_canvas.pack(side="left", fill="both", expand=True)
        
        # Set up scrolling for this canvas
        self._setup_scrolling(results_canvas)

    def calculate_consumption(self):
        """Calculate gas consumption and costs"""
        try:
            # Get input values
            students_per_week = int(self.consumption_vars['students_per_week'].get())
            weeks = int(self.consumption_vars['weeks'].get())
            session_duration = float(self.consumption_vars['session_duration'].get())
            recovery_duration = float(self.consumption_vars['recovery_duration'].get())
            altitude = float(self.consumption_vars['altitude'].get())
            price_air = float(self.consumption_vars['price_air'].get())
            price_nitrogen = float(self.consumption_vars['price_nitrogen'].get())
            price_oxygen = float(self.consumption_vars['price_oxygen'].get())
            contingency = float(self.consumption_vars['contingency'].get())
            
            # Calculate physiological parameters for ventilation rate
            altitude_m = altitude * 0.3048
            altitude_above_1500_m = max(0, altitude_m - 1500)
            ventilation_increase_factor = (altitude_above_1500_m / 1000)
            ventilation_rate = 6 * (1 + ventilation_increase_factor)
            ventilation_rate = min(ventilation_rate, 60)
            
            # Calculate consumption
            air_consumed_per_session = (ventilation_rate * session_duration) / 1000  # m³
            nitrogen_consumed_per_session = air_consumed_per_session * 0.05
            oxygen_consumed_per_session = (ventilation_rate * recovery_duration) / 1000
            
            # Weekly consumption
            weekly_air = air_consumed_per_session * students_per_week
            weekly_nitrogen = nitrogen_consumed_per_session * students_per_week
            weekly_oxygen = oxygen_consumed_per_session * students_per_week
            
            # Total consumption
            total_air = weekly_air * weeks
            total_nitrogen = weekly_nitrogen * weeks
            total_oxygen = weekly_oxygen * weeks
            
            # Costs
            total_cost_air = total_air * price_air
            total_cost_nitrogen = total_nitrogen * price_nitrogen
            total_cost_oxygen = total_oxygen * price_oxygen
            total_cost = total_cost_air + total_cost_nitrogen + total_cost_oxygen
            total_cost_with_contingency = total_cost * (1 + contingency)
            
            # Clear previous results
            for widget in self.consumption_results_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Display results with modern styling
            results = [
                ("Weekly Consumption", [
                    ("Air", f"{weekly_air:.2f} m³"),
                    ("Nitrogen", f"{weekly_nitrogen:.2f} m³"),
                    ("Oxygen", f"{weekly_oxygen:.2f} m³")
                ]),
                ("Total Consumption", [
                    ("Air", f"{total_air:.2f} m³"),
                    ("Nitrogen", f"{total_nitrogen:.2f} m³"),
                    ("Oxygen", f"{total_oxygen:.2f} m³")
                ]),
                ("Costs", [
                    ("Air", f"{total_cost_air:,.0f} COP"),
                    ("Nitrogen", f"{total_cost_nitrogen:,.0f} COP"),
                    ("Oxygen", f"{total_cost_oxygen:,.0f} COP"),
                    ("Total", f"{total_cost:,.0f} COP"),
                    ("With Contingency", f"{total_cost_with_contingency:,.0f} COP")
                ])
            ]
            
            # Create a modern result display
            for i, (section, items) in enumerate(results):
                # Section header
                section_frame = ttk.Frame(self.consumption_results_scrollable_frame)
                section_frame.pack(fill=tk.X, pady=5, padx=5)
                
                ttk.Label(
                    section_frame,
                    text=section,
                    style="Result.TLabel",
                    font=('Helvetica', 11, 'bold')
                ).pack(anchor="w")
                
                # Items in the section
                for label, value in items:
                    item_frame = ttk.Frame(self.consumption_results_scrollable_frame)
                    item_frame.pack(fill=tk.X, pady=2, padx=15)
                    
                    ttk.Label(
                        item_frame,
                        text=label + ":",
                        style="Result.TLabel",
                        font=('Helvetica', 10, 'bold')
                    ).pack(side=tk.LEFT)
                    
                    ttk.Label(
                        item_frame,
                        text=value,
                        style="Result.TLabel"
                    ).pack(side=tk.RIGHT)
                
                # Add separator except for last section
                if i < len(results) - 1:
                    ttk.Separator(self.consumption_results_scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
            
            # Update visualization
            self.consumption_fig.clear()
            ax = self.consumption_fig.add_subplot(111)
            
            # Create pie chart of costs
            costs = [total_cost_air, total_cost_nitrogen, total_cost_oxygen]
            labels = ['Air', 'Nitrogen', 'Oxygen']
            
            ax.pie(costs, labels=labels, autopct='%1.1f%%')
            ax.set_title('Cost Distribution')
            
            self.consumption_canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            log.error(f"Error in consumption calculation: {e}")
            
    def calculate_capacity(self):
        """Calculate cylinder capacity"""
        try:
            # Get input values
            air_cylinder = float(self.capacity_vars['air_cylinder'].get())
            nitrogen_cylinder = float(self.capacity_vars['nitrogen_cylinder'].get())
            oxygen_cylinder = float(self.capacity_vars['oxygen_cylinder'].get())
            session_duration = float(self.capacity_vars['session_duration'].get())
            recovery_duration = float(self.capacity_vars['recovery_duration'].get())
            altitude = float(self.capacity_vars['altitude'].get())
            
            # Calculate physiological parameters for ventilation rate
            altitude_m = altitude * 0.3048
            altitude_above_1500_m = max(0, altitude_m - 1500)
            ventilation_increase_factor = (altitude_above_1500_m / 1000)
            ventilation_rate = 6 * (1 + ventilation_increase_factor)
            ventilation_rate = min(ventilation_rate, 60)
            
            # Calculate consumption per session
            air_per_session = (ventilation_rate * session_duration) / 1000  # m³
            nitrogen_per_session = air_per_session * 0.05
            oxygen_per_session = (ventilation_rate * recovery_duration) / 1000
            
            # Calculate maximum students for each gas
            max_students_air = int(air_cylinder / air_per_session)
            max_students_nitrogen = int(nitrogen_cylinder / nitrogen_per_session)
            max_students_oxygen = int(oxygen_cylinder / oxygen_per_session)
            
            # The limiting factor is the minimum of all three
            max_students = min(max_students_air, max_students_nitrogen, max_students_oxygen)
            
            # Clear previous results
            for widget in self.capacity_results_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Display results with modern styling
            results = [
                ("Maximum Students", [
                    ("Air", f"{max_students_air}"),
                    ("Nitrogen", f"{max_students_nitrogen}"),
                    ("Oxygen", f"{max_students_oxygen}"),
                    ("Total Limit", f"{max_students}")
                ]),
                ("Consumption per Session", [
                    ("Air", f"{air_per_session:.2f} m³"),
                    ("Nitrogen", f"{nitrogen_per_session:.2f} m³"),
                    ("Oxygen", f"{oxygen_per_session:.2f} m³")
                ])
            ]
            
            # Create a modern result display
            for i, (section, items) in enumerate(results):
                # Section header
                section_frame = ttk.Frame(self.capacity_results_scrollable_frame)
                section_frame.pack(fill=tk.X, pady=5, padx=5)
                
                ttk.Label(
                    section_frame,
                    text=section,
                    style="Result.TLabel",
                    font=('Helvetica', 11, 'bold')
                ).pack(anchor="w")
                
                # Items in the section
                for label, value in items:
                    item_frame = ttk.Frame(self.capacity_results_scrollable_frame)
                    item_frame.pack(fill=tk.X, pady=2, padx=15)
                    
                    ttk.Label(
                        item_frame,
                        text=label + ":",
                        style="Result.TLabel",
                        font=('Helvetica', 10, 'bold')
                    ).pack(side=tk.LEFT)
                    
                    ttk.Label(
                        item_frame,
                        text=value,
                        style="Result.TLabel"
                    ).pack(side=tk.RIGHT)
                
                # Add separator except for last section
                if i < len(results) - 1:
                    ttk.Separator(self.capacity_results_scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
            
            # Update visualization
            self.capacity_fig.clear()
            ax = self.capacity_fig.add_subplot(111)
            
            # Create bar chart of maximum students
            students = [max_students_air, max_students_nitrogen, max_students_oxygen]
            labels = ['Air', 'Nitrogen', 'Oxygen']
            
            bars = ax.bar(labels, students)
            ax.set_title('Maximum Students per Gas Type')
            ax.set_ylabel('Number of Students')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom')
            
            # Customize the appearance
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            self.capacity_canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            log.error(f"Error in capacity calculation: {e}")
            
    def calculate_single_session(self):
        """Calculate single session consumption and costs"""
        try:
            # Get input values
            session_duration = float(self.session_vars['session_duration'].get())
            recovery_duration = float(self.session_vars['recovery_duration'].get())
            altitude = float(self.session_vars['altitude'].get())
            price_air = float(self.session_vars['price_air'].get())
            price_nitrogen = float(self.session_vars['price_nitrogen'].get())
            price_oxygen = float(self.session_vars['price_oxygen'].get())
            
            # Calculate physiological parameters for ventilation rate
            altitude_m = altitude * 0.3048
            altitude_above_1500_m = max(0, altitude_m - 1500)
            ventilation_increase_factor = (altitude_above_1500_m / 1000)
            ventilation_rate = 6 * (1 + ventilation_increase_factor)
            ventilation_rate = min(ventilation_rate, 60)
            
            # Calculate consumption
            air_consumed = (ventilation_rate * session_duration) / 1000  # m³
            nitrogen_consumed = air_consumed * 0.05
            oxygen_consumed = (ventilation_rate * recovery_duration) / 1000
            
            # Calculate costs
            cost_air = air_consumed * price_air
            cost_nitrogen = nitrogen_consumed * price_nitrogen
            cost_oxygen = oxygen_consumed * price_oxygen
            total_cost = cost_air + cost_nitrogen + cost_oxygen
            
            # Clear previous results
            for widget in self.session_results_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Display results with modern styling
            results = [
                ("Gas Consumption", [
                    ("Air", f"{air_consumed:.2f} m³"),
                    ("Nitrogen", f"{nitrogen_consumed:.2f} m³"),
                    ("Oxygen", f"{oxygen_consumed:.2f} m³")
                ]),
                ("Costs", [
                    ("Air", f"{cost_air:,.0f} COP"),
                    ("Nitrogen", f"{cost_nitrogen:,.0f} COP"),
                    ("Oxygen", f"{cost_oxygen:,.0f} COP"),
                    ("Total", f"{total_cost:,.0f} COP")
                ])
            ]
            
            # Create a modern result display
            for i, (section, items) in enumerate(results):
                # Section header
                section_frame = ttk.Frame(self.session_results_scrollable_frame)
                section_frame.pack(fill=tk.X, pady=5, padx=5)
                
                ttk.Label(
                    section_frame,
                    text=section,
                    style="Result.TLabel",
                    font=('Helvetica', 11, 'bold')
                ).pack(anchor="w")
                
                # Items in the section
                for label, value in items:
                    item_frame = ttk.Frame(self.session_results_scrollable_frame)
                    item_frame.pack(fill=tk.X, pady=2, padx=15)
                    
                    ttk.Label(
                        item_frame,
                        text=label + ":",
                        style="Result.TLabel",
                        font=('Helvetica', 10, 'bold')
                    ).pack(side=tk.LEFT)
                    
                    ttk.Label(
                        item_frame,
                        text=value,
                        style="Result.TLabel"
                    ).pack(side=tk.RIGHT)
                
                # Add separator except for last section
                if i < len(results) - 1:
                    ttk.Separator(self.session_results_scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
            
            # Update visualization
            self.session_fig.clear()
            ax = self.session_fig.add_subplot(111)
            
            # Create pie chart of costs
            costs = [cost_air, cost_nitrogen, cost_oxygen]
            labels = ['Air', 'Nitrogen', 'Oxygen']
            
            ax.pie(costs, labels=labels, autopct='%1.1f%%')
            ax.set_title('Cost Distribution')
            
            self.session_canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            log.error(f"Error in single session calculation: {e}") 