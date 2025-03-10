from collections import deque
from datetime import datetime
from pathlib import Path
import csv
import logging

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