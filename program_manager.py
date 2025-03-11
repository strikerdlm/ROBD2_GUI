import tkinter as tk
from tkinter import ttk, messagebox
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame

class ProgramManager(ModernFrame):
    def __init__(self, parent, serial_comm):
        super().__init__(parent)
        self.serial_comm = serial_comm
        self.create_widgets()

    def create_widgets(self):
        """Create the program manager interface"""
        # Split into left (program list) and right (program details) panels
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Program selection
        left_frame = ModernFrame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # Program selection frame
        program_list_frame = ModernLabelFrame(left_frame, text="Program List", padding=10)
        program_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Program list with scrollbar
        program_list_frame_inner = ttk.Frame(program_list_frame)
        program_list_frame_inner.pack(fill=tk.BOTH, expand=True)
        
        program_list_scrollbar = ttk.Scrollbar(program_list_frame_inner)
        program_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.program_list = ttk.Treeview(
            program_list_frame_inner, 
            columns=("number", "name"),
            show="headings",
            selectmode="browse"
        )
        self.program_list.heading("number", text="Program #")
        self.program_list.heading("name", text="Name")
        self.program_list.column("number", width=80, anchor=tk.CENTER)
        self.program_list.column("name", width=150)
        self.program_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        program_list_scrollbar.config(command=self.program_list.yview)
        self.program_list.config(yscrollcommand=program_list_scrollbar.set)
        
        # Program list buttons
        program_list_buttons = ttk.Frame(left_frame)
        program_list_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ModernButton(program_list_buttons, text="Refresh List", command=self.refresh_program_list)
        refresh_btn.pack(side=tk.LEFT, padx=2)
        
        create_btn = ModernButton(program_list_buttons, text="New Program", command=self.create_new_program)
        create_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = ModernButton(program_list_buttons, text="Delete", command=self.delete_program)
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # Right panel - Program details
        right_frame = ModernFrame(paned_window)
        paned_window.add(right_frame, weight=2)
        
        # Program details frame
        self.program_details_frame = ModernLabelFrame(right_frame, text="Program Details", padding=10)
        self.program_details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Program name
        program_name_frame = ttk.Frame(self.program_details_frame)
        program_name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(program_name_frame, text="Program #:").pack(side=tk.LEFT, padx=5)
        self.program_number_var = tk.StringVar(value="1")
        program_number_entry = ttk.Entry(program_name_frame, textvariable=self.program_number_var, width=5)
        program_number_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(program_name_frame, text="Name:").pack(side=tk.LEFT, padx=5)
        self.program_name_var = tk.StringVar()
        program_name_entry = ttk.Entry(program_name_frame, textvariable=self.program_name_var, width=25)
        program_name_entry.pack(side=tk.LEFT, padx=5)
        
        save_name_btn = ModernButton(program_name_frame, text="Save Name", command=self.save_program_name)
        save_name_btn.pack(side=tk.LEFT, padx=5)
        
        # Program steps
        steps_frame = ModernLabelFrame(self.program_details_frame, text="Program Steps", padding=10)
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Steps list with scrollbar
        steps_list_frame = ttk.Frame(steps_frame)
        steps_list_frame.pack(fill=tk.BOTH, expand=True)
        
        steps_list_scrollbar = ttk.Scrollbar(steps_list_frame)
        steps_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.steps_list = ttk.Treeview(
            steps_list_frame, 
            columns=("step", "mode", "altitude", "value"),
            show="headings",
            selectmode="browse"
        )
        self.steps_list.heading("step", text="Step #")
        self.steps_list.heading("mode", text="Mode")
        self.steps_list.heading("altitude", text="Altitude (ft)")
        self.steps_list.heading("value", text="Time/Rate")
        
        self.steps_list.column("step", width=60, anchor=tk.CENTER)
        self.steps_list.column("mode", width=80, anchor=tk.CENTER)
        self.steps_list.column("altitude", width=100, anchor=tk.CENTER)
        self.steps_list.column("value", width=100, anchor=tk.CENTER)
        
        self.steps_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        steps_list_scrollbar.config(command=self.steps_list.yview)
        self.steps_list.config(yscrollcommand=steps_list_scrollbar.set)
        
        # Step editor
        step_editor_frame = ttk.Frame(self.program_details_frame)
        step_editor_frame.pack(fill=tk.X, pady=10)
        
        # Create a grid layout for the step editor
        ttk.Label(step_editor_frame, text="Step #:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.step_number_var = tk.StringVar(value="1")
        step_number_entry = ttk.Entry(step_editor_frame, textvariable=self.step_number_var, width=5)
        step_number_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(step_editor_frame, text="Mode:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.step_mode_var = tk.StringVar()
        step_mode_combo = ttk.Combobox(step_editor_frame, textvariable=self.step_mode_var, width=10)
        step_mode_combo["values"] = ("HLD", "CHG", "END")
        step_mode_combo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        step_mode_combo.current(0)
        
        ttk.Label(step_editor_frame, text="Altitude (ft):").grid(row=0, column=4, padx=5, pady=2, sticky=tk.W)
        self.step_altitude_var = tk.StringVar(value="0")
        step_altitude_entry = ttk.Entry(step_editor_frame, textvariable=self.step_altitude_var, width=8)
        step_altitude_entry.grid(row=0, column=5, padx=5, pady=2, sticky=tk.W)
        
        # This label will change based on the mode
        self.step_value_label = ttk.Label(step_editor_frame, text="Hold Time (min):")
        self.step_value_label.grid(row=0, column=6, padx=5, pady=2, sticky=tk.W)
        self.step_value_var = tk.StringVar(value="1")
        step_value_entry = ttk.Entry(step_editor_frame, textvariable=self.step_value_var, width=8)
        step_value_entry.grid(row=0, column=7, padx=5, pady=2, sticky=tk.W)
        
        # Update label when mode changes
        def update_value_label(*args):
            mode = self.step_mode_var.get()
            if mode == "HLD":
                self.step_value_label.config(text="Hold Time (min):")
            elif mode == "CHG":
                self.step_value_label.config(text="Rate (ft/min):")
            elif mode == "END":
                self.step_value_label.config(text="N/A:")
                self.step_value_var.set("")
                
        self.step_mode_var.trace("w", update_value_label)
        
        # Step editor buttons
        step_editor_buttons = ttk.Frame(self.program_details_frame)
        step_editor_buttons.pack(fill=tk.X, pady=5)
        
        add_step_btn = ModernButton(step_editor_buttons, text="Add/Update Step", command=self.add_update_step)
        add_step_btn.pack(side=tk.LEFT, padx=2)
        
        delete_step_btn = ModernButton(step_editor_buttons, text="Delete Step", command=self.delete_step)
        delete_step_btn.pack(side=tk.LEFT, padx=2)
        
        clear_steps_btn = ModernButton(step_editor_buttons, text="Clear Steps", command=self.clear_steps)
        clear_steps_btn.pack(side=tk.LEFT, padx=2)
        
        send_program_btn = ModernButton(step_editor_buttons, text="Send Program to Device", command=self.send_program)
        send_program_btn.pack(side=tk.RIGHT, padx=2)
        
        # Flight profile templates
        templates_frame = ModernLabelFrame(self.program_details_frame, text="Flight Profile Templates", padding=10)
        templates_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(templates_frame, text="Quick Templates:").pack(side=tk.LEFT, padx=5)
        
        alt_10k_btn = ModernButton(templates_frame, text="10,000 ft", 
                                   command=lambda: self.load_altitude_template(10000))
        alt_10k_btn.pack(side=tk.LEFT, padx=2)
        
        alt_15k_btn = ModernButton(templates_frame, text="15,000 ft", 
                                   command=lambda: self.load_altitude_template(15000))
        alt_15k_btn.pack(side=tk.LEFT, padx=2)
        
        alt_20k_btn = ModernButton(templates_frame, text="20,000 ft", 
                                   command=lambda: self.load_altitude_template(20000))
        alt_20k_btn.pack(side=tk.LEFT, padx=2)
        
        alt_25k_btn = ModernButton(templates_frame, text="25,000 ft", 
                                   command=lambda: self.load_altitude_template(25000))
        alt_25k_btn.pack(side=tk.LEFT, padx=2)
        
        # Custom template generator
        custom_frame = ttk.Frame(templates_frame)
        custom_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(custom_frame, text="Custom:").pack(side=tk.LEFT, padx=5)
        
        self.custom_altitude_var = tk.StringVar(value="18000")
        custom_altitude_entry = ttk.Entry(custom_frame, textvariable=self.custom_altitude_var, width=8)
        custom_altitude_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(custom_frame, text="ft").pack(side=tk.LEFT)
        
        custom_generate_btn = ModernButton(custom_frame, text="Generate", 
                                          command=self.generate_custom_template)
        custom_generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Connect events
        self.program_list.bind("<<TreeviewSelect>>", self.on_program_selected)
        self.steps_list.bind("<<TreeviewSelect>>", self.on_step_selected)
        
        # Initialize program list
        self.refresh_program_list()

    def refresh_program_list(self):
        """Refresh the list of programs from the device"""
        # Clear existing items
        for item in self.program_list.get_children():
            self.program_list.delete(item)
            
        if self.serial_comm.is_connected:
            # Query each program slot (1-20) for its name
            for i in range(1, 21):
                command = f"PROG {i} NAME ?"
                success, response = self.serial_comm.send_command(command)
                if success:
                    self.program_list.insert("", "end", values=(i, response.strip()))
        else:
            # Add empty program slots in demo mode
            for i in range(1, 21):
                self.program_list.insert("", "end", values=(i, f"Program {i}"))

    def create_new_program(self):
        """Create a new program"""
        # Find first available program number
        program_numbers = [int(self.program_list.item(item)["values"][0]) 
                         for item in self.program_list.get_children()]
        available_numbers = set(range(1, 21)) - set(program_numbers)
        
        if not available_numbers:
            messagebox.showerror("Error", "Maximum number of programs (20) reached")
            return
            
        new_number = min(available_numbers)
        self.program_list.insert("", "end", values=(new_number, f"Program {new_number}"))
        
        # Select the new program
        for item in self.program_list.get_children():
            if int(self.program_list.item(item)["values"][0]) == new_number:
                self.program_list.selection_set(item)
                self.on_program_selected(None)
                break

    def delete_program(self):
        """Delete the selected program"""
        selected = self.program_list.selection()
        if not selected:
            messagebox.showerror("Error", "No program selected")
            return
            
        program_number = self.program_list.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete Program {program_number}?")
        
        if confirm:
            # In a real implementation, this would send a command to delete from the device
            self.program_list.delete(selected)
            messagebox.showinfo("Program Deleted", f"Program {program_number} has been deleted")

    def on_program_selected(self, event):
        """Handle program selection"""
        selected = self.program_list.selection()
        if not selected:
            return
            
        program_number = self.program_list.item(selected)["values"][0]
        program_name = self.program_list.item(selected)["values"][1]
        
        self.program_number_var.set(str(program_number))
        self.program_name_var.set(program_name)
        
        # Query device for program steps
        self.refresh_steps_list()

    def save_program_name(self):
        """Save the program name"""
        program_number = self.program_number_var.get()
        program_name = self.program_name_var.get()
        
        if not program_number.isdigit() or int(program_number) < 1 or int(program_number) > 20:
            messagebox.showerror("Error", "Program number must be between 1 and 20")
            return
            
        if not program_name:
            messagebox.showerror("Error", "Program name cannot be empty")
            return
            
        command = f"PROG {program_number} NAME {program_name}"
        
        if self.serial_comm.is_connected:
            success, message = self.serial_comm.send_command(command)
            if success:
                messagebox.showinfo("Success", f"Program {program_number} name saved")
                
                # Update the treeview
                for item in self.program_list.get_children():
                    if int(self.program_list.item(item)["values"][0]) == int(program_number):
                        self.program_list.item(item, values=(program_number, program_name))
                        break
            else:
                messagebox.showerror("Error", message)
        else:
            # Demo mode
            for item in self.program_list.get_children():
                if int(self.program_list.item(item)["values"][0]) == int(program_number):
                    self.program_list.item(item, values=(program_number, program_name))
                    break
            messagebox.showinfo("Demo Mode", "Program name would be saved (device not connected)")

    def refresh_steps_list(self):
        """Refresh the steps list for the current program"""
        # Clear existing items
        for item in self.steps_list.get_children():
            self.steps_list.delete(item)
            
        program_number = self.program_number_var.get()
        
        if self.serial_comm.is_connected:
            # Query each step until we find an END or reach step 99
            step = 1
            while step < 99:
                command = f"PROG {program_number} {step} ?"
                success, response = self.serial_comm.send_command(command)
                if success:
                    parts = response.strip().split()
                    if not parts:
                        break
                        
                    mode = parts[0]
                    if mode == "END":
                        self.steps_list.insert("", "end", values=(step, "END", "", ""))
                        break
                    elif len(parts) >= 3:
                        altitude = parts[1]
                        value = parts[2]
                        display_value = f"{value} min" if mode == "HLD" else f"{value} ft/min"
                        self.steps_list.insert("", "end", values=(step, mode, altitude, display_value))
                    step += 1
                else:
                    break
        else:
            # Demo mode - show example steps
            if program_number == "1":
                steps = [
                    (1, "HLD", 0, "1 min"),
                    (2, "CHG", 10000, "3000 ft/min"),
                    (3, "HLD", 10000, "5 min"),
                    (4, "CHG", 0, "3000 ft/min"),
                    (5, "END", "", "")
                ]
                for step in steps:
                    self.steps_list.insert("", "end", values=step)

    def on_step_selected(self, event):
        """Handle step selection"""
        selected = self.steps_list.selection()
        if not selected:
            return
            
        step_data = self.steps_list.item(selected)["values"]
        
        self.step_number_var.set(str(step_data[0]))
        self.step_mode_var.set(step_data[1])
        
        if step_data[2]:  # Altitude
            self.step_altitude_var.set(str(step_data[2]))
        else:
            self.step_altitude_var.set("0")
            
        if step_data[1] != "END":  # Value (time or rate)
            value = step_data[3].split()[0]  # Extract number from "X min" or "X ft/min"
            self.step_value_var.set(value)
        else:
            self.step_value_var.set("")

    def add_update_step(self):
        """Add or update a step in the current program"""
        program_number = self.program_number_var.get()
        step_number = self.step_number_var.get()
        step_mode = self.step_mode_var.get()
        step_altitude = self.step_altitude_var.get()
        step_value = self.step_value_var.get()
        
        # Validate inputs
        if not program_number.isdigit() or int(program_number) < 1 or int(program_number) > 20:
            messagebox.showerror("Error", "Program number must be between 1 and 20")
            return
            
        if not step_number.isdigit() or int(step_number) < 1 or int(step_number) > 98:
            messagebox.showerror("Error", "Step number must be between 1 and 98")
            return
            
        if step_mode not in ["HLD", "CHG", "END"]:
            messagebox.showerror("Error", "Mode must be HLD, CHG, or END")
            return
            
        if step_mode != "END":
            if not step_altitude.isdigit():
                messagebox.showerror("Error", "Altitude must be a number")
                return
                
            if not step_value or not step_value.isdigit():
                messagebox.showerror("Error", "Value must be a number")
                return
                
            # Validate altitude range
            if int(step_altitude) > 34000:
                messagebox.showerror("Error", "Maximum altitude is 34,000 ft")
                return
        
        # Construct the command
        if step_mode == "END":
            command = f"PROG {program_number} {step_number} END"
            display_value = ""
            display_altitude = ""
        else:
            command = f"PROG {program_number} {step_number} {step_mode} {step_altitude} {step_value}"
            display_altitude = step_altitude
            display_value = f"{step_value} min" if step_mode == "HLD" else f"{step_value} ft/min"
        
        if self.serial_comm.is_connected:
            success, message = self.serial_comm.send_command(command)
            if success:
                self._update_step_in_list(step_number, step_mode, display_altitude, display_value)
                messagebox.showinfo("Success", f"Step {step_number} saved")
            else:
                messagebox.showerror("Error", message)
        else:
            # Demo mode
            self._update_step_in_list(step_number, step_mode, display_altitude, display_value)
            messagebox.showinfo("Demo Mode", f"Step {step_number} would be saved (device not connected)")

    def _update_step_in_list(self, step_number, mode, altitude, value):
        """Helper method to update or add a step in the steps list"""
        step_exists = False
        for item in self.steps_list.get_children():
            if int(self.steps_list.item(item)["values"][0]) == int(step_number):
                self.steps_list.item(item, values=(step_number, mode, altitude, value))
                step_exists = True
                break
                
        if not step_exists:
            self.steps_list.insert("", "end", values=(step_number, mode, altitude, value))

    def delete_step(self):
        """Delete the selected step"""
        selected = self.steps_list.selection()
        if not selected:
            messagebox.showerror("Error", "No step selected")
            return
            
        step_number = self.steps_list.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete Step {step_number}?")
        
        if confirm:
            if self.serial_comm.is_connected:
                # Send command to delete step (by setting it to END)
                program_number = self.program_number_var.get()
                command = f"PROG {program_number} {step_number} END"
                success, message = self.serial_comm.send_command(command)
                if success:
                    self.steps_list.delete(selected)
                    messagebox.showinfo("Step Deleted", f"Step {step_number} has been deleted")
                else:
                    messagebox.showerror("Error", message)
            else:
                # Demo mode
                self.steps_list.delete(selected)
                messagebox.showinfo("Demo Mode", f"Step {step_number} would be deleted (device not connected)")

    def clear_steps(self):
        """Clear all steps for the current program"""
        confirm = messagebox.askyesno("Confirm Clear", "Clear all steps for this program?")
        
        if confirm:
            program_number = self.program_number_var.get()
            if self.serial_comm.is_connected:
                # Set first step to END to effectively clear the program
                command = f"PROG {program_number} 1 END"
                success, message = self.serial_comm.send_command(command)
                if success:
                    for item in self.steps_list.get_children():
                        self.steps_list.delete(item)
                    self.steps_list.insert("", "end", values=(1, "END", "", ""))
                    messagebox.showinfo("Steps Cleared", "All steps have been cleared")
                else:
                    messagebox.showerror("Error", message)
            else:
                # Demo mode
                for item in self.steps_list.get_children():
                    self.steps_list.delete(item)
                self.steps_list.insert("", "end", values=(1, "END", "", ""))
                messagebox.showinfo("Demo Mode", "Steps would be cleared (device not connected)")

    def send_program(self):
        """Send the complete program to the device"""
        if not self.serial_comm.is_connected:
            messagebox.showerror("Error", "Not connected to device")
            return
            
        program_number = self.program_number_var.get()
        steps = []
        
        for item in self.steps_list.get_children():
            steps.append(self.steps_list.item(item)["values"])
            
        if not steps:
            messagebox.showerror("Error", "No steps to send")
            return
            
        # Check if the last step is END
        last_step = steps[-1]
        if last_step[1] != "END":
            confirm = messagebox.askyesno("Missing END", 
                                         "The last step is not an END step. Add it automatically?")
            if confirm:
                next_step_num = int(last_step[0]) + 1
                if next_step_num <= 98:
                    command = f"PROG {program_number} {next_step_num} END"
                    success, message = self.serial_comm.send_command(command)
                    if success:
                        self.steps_list.insert("", "end", values=(next_step_num, "END", "", ""))
                else:
                    messagebox.showerror("Error", "Cannot add END step, maximum step number reached")
                    return
            else:
                return
                
        messagebox.showinfo("Program Sent", f"Program {program_number} has been sent to the device")

    def load_altitude_template(self, altitude):
        """Load a template for the specified altitude"""
        confirm = messagebox.askyesno("Confirm Load", 
                                     f"Load template for {altitude} ft? This will replace current steps.")
        
        if not confirm:
            return
            
        # Clear current steps
        self.clear_steps()
        
        # Calculate rate of change (3000 ft/min is a reasonable rate)
        rate = 3000
        
        # Create a standard profile:
        # 1. Hold at ground level (0 ft) for 1 minute
        # 2. Climb to target altitude at specified rate
        # 3. Hold at target altitude for 5 minutes
        # 4. Descend to ground level at specified rate
        # 5. End program
        
        steps = [
            (1, "HLD", 0, "1"),  # Hold at ground for 1 min
            (2, "CHG", altitude, str(rate)),  # Climb to target altitude
            (3, "HLD", altitude, "5"),  # Hold at altitude for 5 min
            (4, "CHG", 0, str(rate)),  # Descend to ground
            (5, "END", 0, "")  # End program
        ]
        
        # Add steps to the list and send to device if connected
        for step_num, mode, alt, value in steps:
            self.step_number_var.set(str(step_num))
            self.step_mode_var.set(mode)
            self.step_altitude_var.set(str(alt))
            self.step_value_var.set(value)
            self.add_update_step()

    def generate_custom_template(self):
        """Generate a custom altitude template"""
        try:
            altitude = int(self.custom_altitude_var.get())
            if altitude < 0 or altitude > 34000:
                messagebox.showerror("Error", "Altitude must be between 0 and 34,000 ft")
                return
                
            self.load_altitude_template(altitude)
        except ValueError:
            messagebox.showerror("Error", "Invalid altitude value") 