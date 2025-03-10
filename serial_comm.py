import serial
import serial.tools.list_ports
import threading
import queue
import logging
from datetime import datetime

log = logging.getLogger("robd2_gui")

class SerialCommunicator:
    def __init__(self):
        self.serial_port = None
        self.is_connected = False
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.command_thread = None
        self.running = False
        
    def connect(self, port):
        """Connect to the specified COM port"""
        try:
            if not port:
                raise ValueError("No port specified")
                
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            self.is_connected = True
            
            # Start command processing thread
            self.running = True
            self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
            self.command_thread.start()
            
            return True, "Connected successfully"
            
        except serial.SerialException as e:
            log.error(f"Serial connection error: {e}", exc_info=True)
            return False, f"Failed to connect to {port}: {str(e)}"
        except Exception as e:
            log.error(f"Unexpected connection error: {e}", exc_info=True)
            return False, f"An unexpected error occurred: {str(e)}"
            
    def disconnect(self):
        """Disconnect from the COM port"""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.running = False
                if self.command_thread:
                    self.command_thread.join(timeout=1)
                self.serial_port.close()
                self.is_connected = False
                return True, "Disconnected successfully"
            except Exception as e:
                log.error(f"Error disconnecting: {e}", exc_info=True)
                return False, f"Failed to disconnect: {str(e)}"
        return True, "Already disconnected"
        
    def send_command(self, command):
        """Send a command to the device"""
        if not self.is_connected:
            return False, "Not connected to device"
            
        try:
            self.command_queue.put(f"{command}\r\n")
            return True, "Command queued successfully"
        except Exception as e:
            log.error(f"Error sending command: {e}", exc_info=True)
            return False, f"Failed to send command: {str(e)}"
            
    def process_commands(self):
        """Process commands from the queue"""
        while self.running:
            try:
                command = self.command_queue.get(timeout=0.1)
                if command is None:
                    break
                    
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.write(command.encode('utf-8'))
                    
            except queue.Empty:
                continue
            except Exception as e:
                log.error(f"Error processing command: {e}")
                self.response_queue.put(f"Error: {str(e)}")
                
    def get_response(self):
        """Get response from the device"""
        if not self.is_connected:
            return None
            
        try:
            if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting:
                response = self.serial_port.readline().decode('utf-8').rstrip()
                if response:
                    return response
                    
            # Check response queue
            while not self.response_queue.empty():
                try:
                    return self.response_queue.get_nowait()
                except queue.Empty:
                    break
                    
            return None
            
        except Exception as e:
            log.error(f"Error getting response: {e}")
            return None
            
    def get_available_ports(self):
        """Get list of available COM ports"""
        return [port.device for port in serial.tools.list_ports.comports()] 