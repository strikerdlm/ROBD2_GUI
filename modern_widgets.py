import tkinter as tk
from tkinter import ttk

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
