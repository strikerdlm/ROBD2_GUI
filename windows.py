import tkinter as tk
from tkinter import ttk
import sys
from modern_widgets import ModernFrame, ModernButton, ModernLabelFrame

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
        
    def check_completion(self):
        """Check if all items in the checklist are completed"""
        all_checked = all(var.get() for var in self.checkboxes)
        if all_checked:
            self.status_label.configure(text="All items completed!", foreground="green")
            self.complete_btn.configure(state=tk.DISABLED)
        else:
            self.status_label.configure(text="Please complete all items", foreground="red")

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