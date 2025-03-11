#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normobaric Hypoxia Training Budget Calculator with Physiological Parameters

This script calculates the weekly and total costs associated with using Compressed Air, Nitrogen, and Oxygen
gases for a normobaric hypoxia training program based on user inputs.
It also calculates physiological parameters for an average adult at different altitudes.

Author: Diego Malpica
Date: 21-01-2025

Assumptions:
- The primary gas used is compressed air from the air tank (21% O₂, 78% N₂).
- Nitrogen is added to the compressed air to simulate altitude (hypoxic conditions).
- 100% Oxygen is provided during the recovery phase.
- Physiological responses are based on average adult data and standard physiological models.
- Standard gas cylinder sizes: Type T (50L), Type K (45L), Type G (50L) at 200 bar pressure.
"""

import sys
import logging
from typing import Dict, Any, Optional, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.align import Align
from rich import box
from rich.text import Text
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Initialize rich console
console = Console()

# Default values for all calculations
DEFAULTS = {
    "students_per_week": 20,
    "weeks": 26,
    "session_duration_minutes": 20,
    "recovery_duration_minutes": 5,
    "price_air": 17853,
    "price_nitrogen": 17838,
    "price_oxygen": 19654,
    "contingency_percentage": 0.10,
    "altitude_ft": 25000,
    # Standard gas cylinder volumes (m3) at 200 bar
    "air_cylinder_volume": 10,  # Type T (50L)
    "nitrogen_cylinder_volume": 9,  # Type K (45L)
    "oxygen_cylinder_volume": 10,  # Type G (50L)
}

# Help text for different functions
HELP_TEXT = {
    "main": """
This calculator helps you estimate gas consumption and costs for hypoxia training.
Choose one of the options from the menu to perform specific calculations.
    """,
    "physiological": """
This calculation estimates physiological parameters for an average adult at a given altitude:
- Altitude in feet or meters
- Atmospheric pressure at that altitude
- Partial pressure of oxygen (PaO2)
- Arterial oxygen saturation (SaO2)
- Ventilation rate
- Heart rate

These values are based on standard physiological models.
    """,
    "consumption": """
This calculation estimates the total gas consumption and costs for a training program:
- Number of sessions per week
- Duration of the program in weeks
- Session duration
- Recovery duration
- Ventilation rate (calculated based on altitude)
- Gas prices (Air, Nitrogen, Oxygen)

The results include weekly and total consumption for each gas, and total costs.
    """,
    "capacity": """
This calculation estimates how many students can be trained with given gas cylinder volumes:
- Cylinder volumes for Air, Nitrogen, and Oxygen
- Session duration
- Recovery duration
- Ventilation rate (calculated based on altitude)

The results show the maximum number of students that can be trained with the available gas.
    """,
    "single_session": """
This calculation estimates gas consumption and costs for a single training session:
- Session duration
- Recovery duration
- Altitude (to calculate ventilation rate)
- Gas prices (Air, Nitrogen, and Oxygen)

The results show the exact amount of each gas consumed and the cost breakdown.
    """
}

# Store previous calculation results for comparison
previous_results = {
    "physiological": None,
    "consumption": None,
    "capacity": None,
    "single_session": None
}

def get_user_input(prompt: str, default_value=None, value_type=float):
    """
    Prompt the user to enter a value, allowing for a default if no input is given.
    Enhanced with rich formatting.
    
    Parameters:
    - prompt: The prompt text to display to the user.
    - default_value: Default value if the user presses Enter.
    - value_type: The expected type of the input value (float, int).
    
    Returns:
    - The user input value, converted to the appropriate type.
    """
    while True:
        try:
            if default_value is not None:
                value = Prompt.ask(prompt, default=str(default_value))
            else:
                value = Prompt.ask(prompt)
                
            if value == '':
                return default_value
            return value_type(value)
        except ValueError:
            console.print(f"[bold red]Invalid input. Please enter a valid {value_type.__name__}.[/bold red]")

def calculate_physiological_parameters(altitude_ft: float) -> dict:
    """
    Calculate physiological parameters for an average adult at a given altitude.

    Parameters:
    - altitude_ft: Altitude in feet.

    Returns:
    - Dictionary containing physiological parameters.
    """
    # Constants
    SEA_LEVEL_PRESSURE = 760  # mmHg
    AVG_VENTILATION_RATE_SL = 6  # L/min at sea level (resting)
    AVG_HEART_RATE_SL = 70  # bpm at sea level (resting)

    # Calculate atmospheric pressure at altitude
    altitude_m = altitude_ft * 0.3048  # Convert feet to meters
    pressure_at_altitude = SEA_LEVEL_PRESSURE * (1 - (2.25577e-5 * altitude_m)) ** 5.25588  # Barometric formula

    # Calculate inspired oxygen partial pressure (PiO2)
    FiO2 = 0.2095  # Fraction of inspired oxygen in dry air
    PiO2 = (pressure_at_altitude - 47) * FiO2  # Subtract water vapor pressure (47 mmHg)

    # Estimate arterial oxygen saturation (SaO2)
    PaO2 = PiO2 - 5  # Approximate alveolar-arterial gradient
    SaO2 = 100 * (PaO2 ** 3) / (PaO2 ** 3 + 150 ** 3)

    # Adjust ventilation rate based on hypoxic ventilatory response
    altitude_above_1500_m = max(0, altitude_m - 1500)
    ventilation_increase_factor = (altitude_above_1500_m / 1000)  # 100% increase per 1,000 m
    ventilation_rate = AVG_VENTILATION_RATE_SL * (1 + ventilation_increase_factor)
    ventilation_rate = min(ventilation_rate, 60)  # Cap ventilation rate to avoid unrealistic values

    # Adjust heart rate based on hypoxia
    altitude_above_1000_m = max(0, altitude_m - 1000)
    heart_rate_increase = altitude_above_1000_m / 100
    heart_rate = AVG_HEART_RATE_SL + heart_rate_increase

    return {
        "altitude_ft": altitude_ft,
        "altitude_m": altitude_m,
        "pressure_at_altitude_mmHg": pressure_at_altitude,
        "PaO2_mmHg": PaO2,
        "SaO2_percent": SaO2,
        "ventilation_rate_L_per_min": ventilation_rate,
        "heart_rate_bpm": heart_rate
    }

def calculate_gas_consumption(sessions_per_week: int, weeks: int, session_duration_minutes: float, ventilation_rate: float, recovery_duration_minutes: float, price_air: float, price_nitrogen: float, price_oxygen: float, contingency_percentage: float = 0.10) -> dict:
    """
    Calculate gas consumption and costs for the training program.
    
    Parameters:
    - sessions_per_week: Number of sessions per week.
    - weeks: Number of weeks.
    - session_duration_minutes: Duration of each session in minutes.
    - ventilation_rate: Ventilation rate in L/min.
    - recovery_duration_minutes: Duration of recovery in minutes.
    - price_air: Price of compressed air per m3.
    - price_nitrogen: Price of nitrogen per m3.
    - price_oxygen: Price of oxygen per m3.
    - contingency_percentage: Additional cost contingency.
    
    Returns:
    - Dictionary with consumption and cost details.
    """
    # Calculate per-session consumption in m3
    air_consumed_per_session = (ventilation_rate * session_duration_minutes) / 1000  # Convert to m3
    nitrogen_consumed_per_session = air_consumed_per_session * 0.05  # Additional nitrogen
    oxygen_consumed_per_session = (ventilation_rate * recovery_duration_minutes) / 1000  # During recovery

    # Weekly consumption
    weekly_air_consumption = air_consumed_per_session * sessions_per_week
    weekly_nitrogen_consumption = nitrogen_consumed_per_session * sessions_per_week
    weekly_oxygen_consumption = oxygen_consumed_per_session * sessions_per_week

    # Total consumption over training period
    total_air_consumption = weekly_air_consumption * weeks
    total_nitrogen_consumption = weekly_nitrogen_consumption * weeks
    total_oxygen_consumption = weekly_oxygen_consumption * weeks

    # Costs
    total_cost_air = total_air_consumption * price_air
    total_cost_nitrogen = total_nitrogen_consumption * price_nitrogen
    total_cost_oxygen = total_oxygen_consumption * price_oxygen

    total_cost = total_cost_air + total_cost_nitrogen + total_cost_oxygen
    total_cost_with_contingency = total_cost * (1 + contingency_percentage)

    return {
        "weekly_air_consumption_m3": weekly_air_consumption,
        "weekly_nitrogen_consumption_m3": weekly_nitrogen_consumption,
        "weekly_oxygen_consumption_m3": weekly_oxygen_consumption,
        "total_air_consumption_m3": total_air_consumption,
        "total_nitrogen_consumption_m3": total_nitrogen_consumption,
        "total_oxygen_consumption_m3": total_oxygen_consumption,
        "total_cost_air_COP": total_cost_air,
        "total_cost_nitrogen_COP": total_cost_nitrogen,
        "total_cost_oxygen_COP": total_cost_oxygen,
        "total_cost_COP": total_cost,
        "total_cost_with_contingency_COP": total_cost_with_contingency
    }

def calculate_student_capacity(air_cylinder_volume: float, nitrogen_cylinder_volume: float, oxygen_cylinder_volume: float, 
                            session_duration_minutes: float, ventilation_rate: float, recovery_duration_minutes: float) -> dict:
    """
    Calculate how many students can be trained with given gas cylinder volumes.
    
    Parameters:
    - air_cylinder_volume: Volume of compressed air cylinder in m3
    - nitrogen_cylinder_volume: Volume of nitrogen cylinder in m3
    - oxygen_cylinder_volume: Volume of oxygen cylinder in m3
    - session_duration_minutes: Duration of each session in minutes
    - ventilation_rate: Ventilation rate in L/min
    - recovery_duration_minutes: Duration of recovery in minutes
    
    Returns:
    - Dictionary with capacity details
    """
    # Calculate consumption per student session
    air_per_session = (ventilation_rate * session_duration_minutes) / 1000  # m3
    nitrogen_per_session = air_per_session * 0.05  # m3
    oxygen_per_session = (ventilation_rate * recovery_duration_minutes) / 1000  # m3
    
    # Calculate maximum students for each gas type
    max_students_air = int(air_cylinder_volume / air_per_session)
    max_students_nitrogen = int(nitrogen_cylinder_volume / nitrogen_per_session)
    max_students_oxygen = int(oxygen_cylinder_volume / oxygen_per_session)
    
    # The limiting factor will be the minimum of all three
    max_students = min(max_students_air, max_students_nitrogen, max_students_oxygen)
    
    return {
        "max_students_total": max_students,
        "max_students_air": max_students_air,
        "max_students_nitrogen": max_students_nitrogen,
        "max_students_oxygen": max_students_oxygen,
        "air_per_session_m3": air_per_session,
        "nitrogen_per_session_m3": nitrogen_per_session,
        "oxygen_per_session_m3": oxygen_per_session
    }

def calculate_single_session_consumption(session_duration_minutes: float, ventilation_rate: float, 
                                       recovery_duration_minutes: float, price_air: float, 
                                       price_nitrogen: float, price_oxygen: float) -> dict:
    """
    Calculate gas consumption and costs for a single person in one training session.
    
    Parameters:
    - session_duration_minutes: Duration of the session in minutes.
    - ventilation_rate: Ventilation rate in L/min.
    - recovery_duration_minutes: Duration of recovery in minutes.
    - price_air: Price of compressed air per m3.
    - price_nitrogen: Price of nitrogen per m3.
    - price_oxygen: Price of oxygen per m3.
    
    Returns:
    - Dictionary with consumption and cost details for a single person's session.
    """
    # Calculate consumption in m3
    air_consumed = (ventilation_rate * session_duration_minutes) / 1000  # Convert to m3
    nitrogen_consumed = air_consumed * 0.05  # Additional nitrogen
    oxygen_consumed = (ventilation_rate * recovery_duration_minutes) / 1000  # During recovery

    # Calculate costs
    cost_air = air_consumed * price_air
    cost_nitrogen = nitrogen_consumed * price_nitrogen
    cost_oxygen = oxygen_consumed * price_oxygen
    
    total_cost = cost_air + cost_nitrogen + cost_oxygen

    return {
        "air_consumption_m3": air_consumed,
        "nitrogen_consumption_m3": nitrogen_consumed,
        "oxygen_consumption_m3": oxygen_consumed,
        "cost_air_COP": cost_air,
        "cost_nitrogen_COP": cost_nitrogen,
        "cost_oxygen_COP": cost_oxygen,
        "total_cost_COP": total_cost
    }

def display_menu():
    """
    Display the main menu options with improved formatting.
    """
    menu_table = Table(show_header=False, box=None)
    menu_table.add_column("Option", style="cyan")
    menu_table.add_column("Description", style="white")
    
    menu_table.add_row("1.", "Calculate Physiological Parameters")
    menu_table.add_row("2.", "Calculate Gas Consumption and Costs")
    menu_table.add_row("3.", "Calculate Training Capacity from Cylinder Volumes")
    menu_table.add_row("4.", "Calculate Consumption for a Single Person (One Session)")
    menu_table.add_row("5.", "Run All Calculations")
    menu_table.add_row("6.", "Compare Previous Results")
    menu_table.add_row("7.", "Help")
    menu_table.add_row("8.", "Exit")
    
    console.print(Panel(menu_table, title="[bold]Normobaric Hypoxia Training Calculator Menu[/bold]", 
                 border_style="blue", expand=False))

def show_help(topic="main"):
    """
    Display help information for a specific topic.
    
    Parameters:
    - topic: The help topic to display (main, physiological, consumption, capacity, single_session)
    """
    if topic in HELP_TEXT:
        console.print(Panel(HELP_TEXT[topic], title=f"[bold]Help: {topic.title()}[/bold]", 
                      border_style="green"))
    else:
        console.print(Panel(HELP_TEXT["main"], title="[bold]Help: General[/bold]", 
                      border_style="green"))
    
    # Display available help topics
    console.print("\n[bold]Available Help Topics:[/bold]")
    for key in HELP_TEXT.keys():
        console.print(f"- {key.replace('_', ' ').title()}")

def compare_results():
    """
    Compare results from previous calculations.
    """
    # Check what results are available
    available_results = [k for k, v in previous_results.items() if v is not None]
    
    if not available_results:
        console.print("[yellow]No previous results available for comparison.[/yellow]")
        return
    
    # For single session calculations, we can compare different parameter sets
    if "single_session" in available_results and len(previous_results["single_session"]) > 1:
        compare_single_sessions()
        return
    
    console.print("[yellow]No comparable results available. Run multiple calculations of the same type to enable comparison.[/yellow]")

def compare_single_sessions():
    """
    Compare multiple single session calculations.
    """
    sessions = previous_results["single_session"]
    
    if len(sessions) < 2:
        console.print("[yellow]Need at least two single session calculations to compare.[/yellow]")
        return
    
    # Create a comparison table
    comparison_table = Table(title="Single Session Comparison")
    comparison_table.add_column("Parameter", style="cyan")
    
    # Add a column for each session
    for i in range(len(sessions)):
        comparison_table.add_column(f"Session {i+1}", style="green")
    
    # Compare parameters
    params_to_compare = [
        ("altitude_ft", "Altitude (ft)"),
        ("ventilation_rate", "Ventilation Rate (L/min)"),
        ("session_duration", "Session Duration (min)"),
        ("recovery_duration", "Recovery Duration (min)"),
        ("air_consumption", "Air Consumption (L)"),
        ("nitrogen_consumption", "Nitrogen Consumption (L)"),
        ("oxygen_consumption", "Oxygen Consumption (L)"),
        ("total_cost", "Total Cost (COP)")
    ]
    
    for param_key, param_name in params_to_compare:
        row_values = [param_name]
        
        for session in sessions:
            # Find the corresponding value in the session data
            if param_key == "altitude_ft":
                row_values.append(str(session["inputs"]["altitude_ft"]))
            elif param_key == "ventilation_rate":
                row_values.append(f"{session['ventilation_rate']:.2f}")
            elif param_key == "session_duration":
                row_values.append(str(session["inputs"]["session_duration_minutes"]))
            elif param_key == "recovery_duration":
                row_values.append(str(session["inputs"]["recovery_duration_minutes"]))
            elif param_key == "air_consumption":
                row_values.append(f"{session['results']['air_consumption_m3']*1000:.2f}")
            elif param_key == "nitrogen_consumption":
                row_values.append(f"{session['results']['nitrogen_consumption_m3']*1000:.2f}")
            elif param_key == "oxygen_consumption":
                row_values.append(f"{session['results']['oxygen_consumption_m3']*1000:.2f}")
            elif param_key == "total_cost":
                row_values.append(f"{session['results']['total_cost_COP']:.2f}")
        
        comparison_table.add_row(*row_values)
    
    console.print(comparison_table)
    
    # Option to save comparison
    if Confirm.ask("Would you like to save this comparison to a file?"):
        filename = Prompt.ask("Enter filename", default="session_comparison.txt")
        with open(filename, "w") as f:
            f.write("=== Single Session Comparison ===\n\n")
            
            for i, session in enumerate(sessions):
                f.write(f"Session {i+1}:\n")
                f.write(f"- Altitude: {session['inputs']['altitude_ft']} ft\n")
                f.write(f"- Ventilation Rate: {session['ventilation_rate']:.2f} L/min\n")
                f.write(f"- Session Duration: {session['inputs']['session_duration_minutes']} minutes\n")
                f.write(f"- Recovery Duration: {session['inputs']['recovery_duration_minutes']} minutes\n")
                f.write(f"- Air Consumption: {session['results']['air_consumption_m3']*1000:.2f} L\n")
                f.write(f"- Nitrogen Consumption: {session['results']['nitrogen_consumption_m3']*1000:.2f} L\n")
                f.write(f"- Oxygen Consumption: {session['results']['oxygen_consumption_m3']*1000:.2f} L\n")
                f.write(f"- Total Cost: {session['results']['total_cost_COP']:.2f} COP\n\n")
            
        console.print(f"[green]Comparison saved to {filename}[/green]")

def get_basic_inputs() -> dict:
    """
    Get the basic inputs needed for most calculations with improved UI.
    """
    console.print(Panel("[bold]Basic Parameters[/bold]", style="cyan"))
    inputs = {}
    
    inputs["session_duration_minutes"] = get_user_input(
        f"Enter the duration of each session in minutes [cyan](default is {DEFAULTS['session_duration_minutes']})[/cyan]: ", 
        DEFAULTS['session_duration_minutes']
    )
    inputs["recovery_duration_minutes"] = get_user_input(
        f"Enter the recovery duration in minutes [cyan](default is {DEFAULTS['recovery_duration_minutes']})[/cyan]: ", 
        DEFAULTS['recovery_duration_minutes']
    )
    inputs["altitude_ft"] = get_user_input(
        f"Enter the simulated altitude in feet [cyan](default is {DEFAULTS['altitude_ft']} ft)[/cyan]: ", 
        DEFAULTS['altitude_ft']
    )
    return inputs

def create_visualization(data: Dict[str, float], title: str) -> Panel:
    """
    Create a visualization of proportional data using rich's capabilities.
    
    Parameters:
    - data: Dictionary of labels and values
    - title: Title for the visualization
    
    Returns:
    - Panel containing the visualization
    """
    # Calculate the total for percentage calculations
    total = sum(data.values())
    max_value = max(data.values())
    max_bar_length = 30  # Maximum number of characters for the longest bar
    
    # Create a table for the visualization
    table = Table(box=box.SIMPLE)
    table.add_column("Item", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Percentage", style="yellow")
    table.add_column("Visualization", style="cyan")
    
    # Add rows with visualization bars
    for label, value in data.items():
        percentage = (value / total) * 100
        bar_length = int((value / max_value) * max_bar_length)
        bar = "█" * bar_length
        
        table.add_row(
            label, 
            f"{value:.2f}", 
            f"{percentage:.1f}%",
            bar
        )
    
    # Add a total row
    table.add_row(
        "[bold]Total[/bold]", 
        f"[bold]{total:.2f}[/bold]", 
        "[bold]100.0%[/bold]",
        ""
    )
    
    return Panel(table, title=title, border_style="green")

def visualize_physiological_data(data: Dict[str, float]) -> Panel:
    """
    Create visualization specifically for physiological data.
    
    Parameters:
    - data: Dictionary of physiological parameters
    
    Returns:
    - Panel containing visualizations
    """
    # Prepare layout for multiple visualizations
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )
    
    # Create header
    layout["header"].update(Panel(
        f"Altitude: {data['altitude_ft']} ft ({data['altitude_m']:.2f} m)", 
        style="cyan", border_style="cyan"
    ))
    
    # Create visualization for SaO2
    sao2 = data['SaO2_percent']
    sao2_text = Text()
    for i in range(100):
        if i < int(sao2):
            sao2_text.append("█", style="green")
        else:
            sao2_text.append("░", style="dim")
    
    sao2_panel = Panel(
        Align.center(Text.from_markup(f"[bold]{sao2:.1f}%[/bold]"), vertical="middle") + 
        Align.center(sao2_text, vertical="middle"),
        title="Arterial Oxygen Saturation (SaO2)"
    )
    
    # Create visualization for other key parameters
    params = {
        "Heart Rate": data['heart_rate_bpm'],
        "Ventilation Rate": data['ventilation_rate_L_per_min'],
        "PaO2": data['PaO2_mmHg']
    }
    
    param_panel = create_visualization(params, "Key Physiological Parameters")
    
    # Update the main layout
    layout["main"].update(sao2_panel)
    
    return layout

def run_physiological_calculation():
    """
    Run only the physiological parameters calculation with improved output formatting.
    """
    # Show help first if requested
    if Confirm.ask("Would you like to see help information about this calculation?", default=False):
        show_help("physiological")
        
    inputs = get_basic_inputs()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Calculating physiological parameters...", total=1)
        physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
        time.sleep(0.5)  # Small delay for visual effect
        progress.update(task, advance=1)
    
    # Create a formatted table for results
    results_table = Table(title=f"Physiological Parameters at {inputs['altitude_ft']} ft")
    results_table.add_column("Parameter", style="cyan")
    results_table.add_column("Value", style="green")
    
    for key, value in physio_params.items():
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)
        
        # Format the parameter name for better readability
        param_name = key.replace('_', ' ').title()
        results_table.add_row(param_name, formatted_value)
    
    console.print(results_table)
    
    # Add visualization of physiological data
    console.print(Panel("Physiological Data Visualization", border_style="blue", title="Visualization"))
    
    # Visualize O2 saturation with a progress bar
    o2_saturation = physio_params["SaO2_percent"]
    console.print("Arterial Oxygen Saturation (SaO2):")
    
    bar_length = 50  # Characters
    filled_length = int(o2_saturation / 100 * bar_length)
    
    # Determine color based on saturation level
    if o2_saturation >= 95:
        bar_color = "green"
    elif o2_saturation >= 90:
        bar_color = "yellow"
    elif o2_saturation >= 80:
        bar_color = "dark_orange"
    else:
        bar_color = "red"
    
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    console.print(f"[{bar_color}]{bar}[/{bar_color}] {o2_saturation:.1f}%")
    
    # Add context
    if o2_saturation >= 95:
        context = "[green]Normal oxygen saturation[/green]"
    elif o2_saturation >= 90:
        context = "[yellow]Mild hypoxemia[/yellow]"
    elif o2_saturation >= 80:
        context = "[dark_orange]Moderate hypoxemia[/dark_orange]"
    else:
        context = "[red]Severe hypoxemia[/red]"
    
    console.print(f"Status: {context}")
    
    # Visualize other physiological parameters
    para_vis_data = {
        "Heart Rate (bpm)": physio_params["heart_rate_bpm"],
        "Ventilation Rate (L/min)": physio_params["ventilation_rate_L_per_min"],
        "Ambient Pressure (mmHg)": physio_params["pressure_at_altitude_mmHg"]
    }
    
    console.print(create_visualization(para_vis_data, "Key Physiological Parameters"))
    
    # Store results for later comparison
    previous_results["physiological"] = physio_params
    
    return physio_params

def run_consumption_calculation():
    """
    Run only the gas consumption and cost calculation.
    """
    inputs = get_basic_inputs()
    students_per_week = get_user_input(
        f"Enter the number of students per week (default is {DEFAULTS['students_per_week']}): ", 
        DEFAULTS['students_per_week'], 
        int
    )
    weeks = get_user_input(
        f"Enter the number of weeks for the training program (default is {DEFAULTS['weeks']}): ", 
        DEFAULTS['weeks'], 
        int
    )
    
    # Get gas prices
    price_air = get_user_input(
        f"Enter the price of Compressed Air per m3 in COP (default is {DEFAULTS['price_air']}): ", 
        DEFAULTS['price_air']
    )
    price_nitrogen = get_user_input(
        f"Enter the price of Nitrogen per m3 in COP (default is {DEFAULTS['price_nitrogen']}): ", 
        DEFAULTS['price_nitrogen']
    )
    price_oxygen = get_user_input(
        f"Enter the price of Oxygen per m3 in COP (default is {DEFAULTS['price_oxygen']}): ", 
        DEFAULTS['price_oxygen']
    )
    contingency_percentage = get_user_input(
        f"Enter the contingency percentage as a decimal (default is {DEFAULTS['contingency_percentage']}): ", 
        DEFAULTS['contingency_percentage']
    )
    
    physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
    ventilation_rate = physio_params['ventilation_rate_L_per_min']
    
    results = calculate_gas_consumption(
        students_per_week, weeks, inputs["session_duration_minutes"], ventilation_rate,
        inputs["recovery_duration_minutes"], price_air, price_nitrogen, price_oxygen, contingency_percentage
    )
    
    print("\n=== Budget Summary ===\n")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    return results

def run_capacity_calculation():
    """
    Run only the cylinder capacity calculation.
    """
    inputs = get_basic_inputs()
    print("\n=== Gas Cylinder Configuration ===")
    print("Standard cylinder sizes: Type T (50L), Type K (45L), Type G (50L) at 200 bar pressure")
    
    air_cylinder_volume = get_user_input(
        f"Enter the Compressed Air cylinder volume in m3 (default is {DEFAULTS['air_cylinder_volume']}): ", 
        DEFAULTS['air_cylinder_volume']
    )
    nitrogen_cylinder_volume = get_user_input(
        f"Enter the Nitrogen cylinder volume in m3 (default is {DEFAULTS['nitrogen_cylinder_volume']}): ", 
        DEFAULTS['nitrogen_cylinder_volume']
    )
    oxygen_cylinder_volume = get_user_input(
        f"Enter the Oxygen cylinder volume in m3 (default is {DEFAULTS['oxygen_cylinder_volume']}): ", 
        DEFAULTS['oxygen_cylinder_volume']
    )
    
    physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
    ventilation_rate = physio_params['ventilation_rate_L_per_min']
    
    capacity_results = calculate_student_capacity(
        air_cylinder_volume, nitrogen_cylinder_volume, oxygen_cylinder_volume,
        inputs["session_duration_minutes"], ventilation_rate, inputs["recovery_duration_minutes"]
    )
    
    print("\n=== Cylinder Capacity Analysis ===\n")
    for key, value in capacity_results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    return capacity_results

def run_single_session_calculation():
    """
    Run the calculation for a single person in one training session with improved output.
    """
    # Show help first if requested
    if Confirm.ask("Would you like to see help information about this calculation?", default=False):
        show_help("single_session")
        
    inputs = get_basic_inputs()
    
    console.print(Panel("[bold]Gas Prices[/bold]", style="cyan"))
    # Get gas prices
    price_air = get_user_input(
        f"Enter the price of Compressed Air per m3 in COP [cyan](default is {DEFAULTS['price_air']})[/cyan]: ", 
        DEFAULTS['price_air']
    )
    price_nitrogen = get_user_input(
        f"Enter the price of Nitrogen per m3 in COP [cyan](default is {DEFAULTS['price_nitrogen']})[/cyan]: ", 
        DEFAULTS['price_nitrogen']
    )
    price_oxygen = get_user_input(
        f"Enter the price of Oxygen per m3 in COP [cyan](default is {DEFAULTS['price_oxygen']})[/cyan]: ", 
        DEFAULTS['price_oxygen']
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task1 = progress.add_task("Calculating physiological parameters...", total=1)
        physio_params = calculate_physiological_parameters(inputs["altitude_ft"])
        time.sleep(0.5)  # Small delay for visual effect
        progress.update(task1, advance=1)
        
        ventilation_rate = physio_params['ventilation_rate_L_per_min']
        
        task2 = progress.add_task("Calculating session consumption...", total=1)
        results = calculate_single_session_consumption(
            inputs["session_duration_minutes"], ventilation_rate,
            inputs["recovery_duration_minutes"], price_air, price_nitrogen, price_oxygen
        )
        time.sleep(0.5)  # Small delay for visual effect
        progress.update(task2, advance=1)
    
    # Summary Panel
    summary_data = (
        f"[bold]Simulated Altitude:[/bold] {inputs['altitude_ft']} ft\n"
        f"[bold]Ventilation Rate:[/bold] {ventilation_rate:.2f} L/min\n"
        f"[bold]Session Duration:[/bold] {inputs['session_duration_minutes']} minutes\n"
        f"[bold]Recovery Duration:[/bold] {inputs['recovery_duration_minutes']} minutes"
    )
    console.print(Panel(summary_data, title="Session Parameters", border_style="green"))
    
    # Gas Consumption Table
    consumption_table = Table(title="Gas Consumption")
    consumption_table.add_column("Gas Type", style="cyan")
    consumption_table.add_column("Cubic Meters (m³)", style="green")
    consumption_table.add_column("Liters (L)", style="green")
    
    consumption_table.add_row(
        "Compressed Air", 
        f"{results['air_consumption_m3']:.6f}", 
        f"{results['air_consumption_m3']*1000:.2f}"
    )
    consumption_table.add_row(
        "Nitrogen", 
        f"{results['nitrogen_consumption_m3']:.6f}", 
        f"{results['nitrogen_consumption_m3']*1000:.2f}"
    )
    consumption_table.add_row(
        "Oxygen", 
        f"{results['oxygen_consumption_m3']:.6f}", 
        f"{results['oxygen_consumption_m3']*1000:.2f}"
    )
    
    console.print(consumption_table)
    
    # Visualize gas consumption
    gas_visualization_data = {
        "Compressed Air": results['air_consumption_m3']*1000,  # Convert to L
        "Nitrogen": results['nitrogen_consumption_m3']*1000,
        "Oxygen": results['oxygen_consumption_m3']*1000
    }
    console.print(create_visualization(gas_visualization_data, "Gas Consumption Visualization (L)"))
    
    # Cost Table
    cost_table = Table(title="Cost Breakdown")
    cost_table.add_column("Gas Type", style="cyan")
    cost_table.add_column("Cost (COP)", style="green")
    cost_table.add_column("Percentage", style="yellow")
    
    total_cost = results['total_cost_COP']
    
    cost_table.add_row(
        "Compressed Air", 
        f"{results['cost_air_COP']:.2f}", 
        f"{(results['cost_air_COP']/total_cost*100):.1f}%"
    )
    cost_table.add_row(
        "Nitrogen", 
        f"{results['cost_nitrogen_COP']:.2f}", 
        f"{(results['cost_nitrogen_COP']/total_cost*100):.1f}%"
    )
    cost_table.add_row(
        "Oxygen", 
        f"{results['cost_oxygen_COP']:.2f}", 
        f"{(results['cost_oxygen_COP']/total_cost*100):.1f}%"
    )
    cost_table.add_row(
        "[bold]Total[/bold]", 
        f"[bold]{results['total_cost_COP']:.2f}[/bold]", 
        "[bold]100.0%[/bold]"
    )
    
    console.print(cost_table)
    
    # Visualize cost breakdown
    cost_visualization_data = {
        "Compressed Air": results['cost_air_COP'],
        "Nitrogen": results['cost_nitrogen_COP'],
        "Oxygen": results['cost_oxygen_COP']
    }
    console.print(create_visualization(cost_visualization_data, "Cost Breakdown Visualization (COP)"))
    
    # Store results for later comparison
    session_data = {
        "inputs": inputs,
        "ventilation_rate": ventilation_rate,
        "results": results
    }
    
    if previous_results["single_session"] is None:
        previous_results["single_session"] = [session_data]
    else:
        previous_results["single_session"].append(session_data)
    
    # Inform user about comparison feature
    if len(previous_results["single_session"]) > 1:
        console.print("[yellow]You can compare this result with previous calculations using option 6 in the main menu.[/yellow]")
    
    # Add option to save the results
    if Confirm.ask("Would you like to save these results to a file?"):
        filename = Prompt.ask("Enter filename", default="single_session_results.txt")
        with open(filename, "w") as f:
            f.write(f"=== Single Session Consumption Summary ===\n\n")
            f.write(f"Simulated Altitude: {inputs['altitude_ft']} ft\n")
            f.write(f"Ventilation Rate: {ventilation_rate:.2f} L/min\n")
            f.write(f"Session Duration: {inputs['session_duration_minutes']} minutes\n")
            f.write(f"Recovery Duration: {inputs['recovery_duration_minutes']} minutes\n\n")
            
            f.write("=== Gas Consumption ===\n")
            f.write(f"Compressed Air: {results['air_consumption_m3']:.6f} m3 ({results['air_consumption_m3']*1000:.2f} L)\n")
            f.write(f"Nitrogen: {results['nitrogen_consumption_m3']:.6f} m3 ({results['nitrogen_consumption_m3']*1000:.2f} L)\n")
            f.write(f"Oxygen: {results['oxygen_consumption_m3']:.6f} m3 ({results['oxygen_consumption_m3']*1000:.2f} L)\n\n")
            
            f.write("=== Cost Breakdown ===\n")
            f.write(f"Compressed Air: {results['cost_air_COP']:.2f} COP ({(results['cost_air_COP']/total_cost*100):.1f}%)\n")
            f.write(f"Nitrogen: {results['cost_nitrogen_COP']:.2f} COP ({(results['cost_nitrogen_COP']/total_cost*100):.1f}%)\n")
            f.write(f"Oxygen: {results['cost_oxygen_COP']:.2f} COP ({(results['cost_oxygen_COP']/total_cost*100):.1f}%)\n")
            f.write(f"Total Cost per Session: {results['total_cost_COP']:.2f} COP\n")
        
        console.print(f"[green]Results saved to {filename}[/green]")
        
    return results

def run_all_calculations():
    """
    Run all calculations in sequence.
    """
    physio_params = run_physiological_calculation()
    consumption_results = run_consumption_calculation()
    capacity_results = run_capacity_calculation()
    return physio_params, consumption_results, capacity_results

def main():
    """
    Main function to execute the Budget Calculator with menu system.
    """
    console.print(Panel("Normobaric Hypoxia Training Budget Calculator\nby Diego Malpica", 
                  style="bold green", border_style="green"))
    
    # Show help at first launch
    show_help("main")
    
    while True:
        display_menu()
        choice = get_user_input("Enter your choice (1-8): ", 1, int)
        
        if choice == 1:
            run_physiological_calculation()
        elif choice == 2:
            run_consumption_calculation()
        elif choice == 3:
            run_capacity_calculation()
        elif choice == 4:
            run_single_session_calculation()
        elif choice == 5:
            run_all_calculations()
        elif choice == 6:
            compare_results()
        elif choice == 7:
            topic = Prompt.ask("Which topic would you like help with?", 
                              default="main", 
                              choices=list(HELP_TEXT.keys()))
            show_help(topic)
        elif choice == 8:
            console.print("[bold green]Thank you for using the Normobaric Hypoxia Training Calculator![/bold green]")
            return
        else:
            console.print("[bold red]Invalid choice. Please select a number between 1 and 8.[/bold red]")
        
        console.print("\nPress Enter to continue...", style="dim")
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCalculation interrupted by user.")
        print("Returning to main menu...")