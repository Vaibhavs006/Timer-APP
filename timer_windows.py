#!/usr/bin/env python3
"""
Timer - Windows System Tray Version
A lightweight Windows system tray timer application that mimics the macOS menu bar timer.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import re
import winsound
from datetime import datetime
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import sys

class TimerApp:
    def __init__(self):
        self.root = None
        self.window_hidden = True
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.is_running = False
        self.timer_thread = None
        self.tray_icon = None
        
        # UI Elements
        self.smart_input = None
        self.hours_input = None
        self.minutes_input = None
        self.seconds_input = None
        self.timer_label = None
        self.start_button = None
        self.reset_button = None
        self.status_label = None
        
        self.create_tray_icon()
        
    def create_tray_icon(self):
        """Create the system tray icon."""
        # Generate a simple timer icon (⏰ representation)
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a circle (clock face)
        draw.ellipse([8, 8, 56, 56], outline='black', width=2)
        # Draw center dot
        draw.ellipse([28, 28, 36, 36], fill='black')
        # Draw a simple hand
        draw.line([32, 32, 32, 16], fill='black', width=2)
        
        menu = Menu(
            MenuItem('Show Timer', self.show_window),
            MenuItem('Quit', self.quit_app)
        )
        
        self.tray_icon = Icon("Timer", image, menu=menu)
        self.update_tray_text()
        
        # Run tray icon in a separate thread
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def update_tray_text(self):
        """Update the tray icon title with remaining time."""
        if self.is_running and self.remaining_seconds > 0:
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            
            if hours > 0:
                time_str = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                time_str = f"{minutes}m {seconds}s"
            else:
                time_str = f"{seconds}s"
            
            if self.tray_icon:
                self.tray_icon.title = f"⏰ {time_str}"
        elif self.total_seconds > 0 and not self.is_running:
            self.tray_icon.title = "⏰ Timer Ready"
        else:
            self.tray_icon.title = "⏰ Custom Horo Timer"
    
    def show_window(self):
        """Show or focus the timer window."""
        if self.root is None:
            self.create_window()
        self.root.deiconify()
        self.root.lift()
        self.root.focus()
        self.window_hidden = False
    
    def hide_window(self):
        """Hide the window to system tray."""
        if self.root:
            self.root.withdraw()
            self.window_hidden = True
    
    def create_window(self):
        """Create the main timer window."""
        self.root = tk.Tk()
        self.root.title("Timer")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Set window icon (simplified)
        self.root.iconphoto(False, self.create_window_icon())
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Timer", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Timer Display
        self.timer_label = ttk.Label(main_frame, text="00:00:00", 
                                     font=("Segoe UI", 48, "bold"))
        self.timer_label.pack(pady=20)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                      font=("Segoe UI", 10), foreground="gray")
        self.status_label.pack(pady=(0, 20))
        
        # Separator
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.pack(fill=tk.X, pady=20)
        
        # Smart Input Section
        smart_label = ttk.Label(main_frame, text="Smart Input (e.g., 1h 25m 30s)", 
                               font=("Segoe UI", 10, "bold"))
        smart_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.smart_input = ttk.Entry(main_frame, font=("Segoe UI", 12), width=30)
        self.smart_input.pack(pady=(0, 15), fill=tk.X)
        self.smart_input.bind('<Return>', lambda e: self.start_timer())
        
        # Separator
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        
        # Custom Split Input Section
        split_label = ttk.Label(main_frame, text="Custom Input", 
                               font=("Segoe UI", 10, "bold"))
        split_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Input fields row
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Hours
        ttk.Label(input_frame, text="Hours:", font=("Segoe UI", 9)).grid(row=0, column=0, padx=(0, 5))
        self.hours_input = ttk.Entry(input_frame, font=("Segoe UI", 11), width=5)
        self.hours_input.insert(0, "0")
        self.hours_input.grid(row=0, column=1, padx=(0, 15))
        self.hours_input.bind('<Return>', lambda e: self.start_timer())
        
        # Minutes
        ttk.Label(input_frame, text="Minutes:", font=("Segoe UI", 9)).grid(row=0, column=2, padx=(0, 5))
        self.minutes_input = ttk.Entry(input_frame, font=("Segoe UI", 11), width=5)
        self.minutes_input.insert(0, "0")
        self.minutes_input.grid(row=0, column=3, padx=(0, 15))
        self.minutes_input.bind('<Return>', lambda e: self.start_timer())
        
        # Seconds
        ttk.Label(input_frame, text="Seconds:", font=("Segoe UI", 9)).grid(row=0, column=4, padx=(0, 5))
        self.seconds_input = ttk.Entry(input_frame, font=("Segoe UI", 11), width=5)
        self.seconds_input.insert(0, "0")
        self.seconds_input.grid(row=0, column=5, padx=(0, 0))
        self.seconds_input.bind('<Return>', lambda e: self.start_timer())
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Start Button
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Pause Button
        pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer)
        pause_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Reset Button
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Close Button
        close_button = ttk.Button(button_frame, text="Close", command=self.hide_window)
        close_button.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Bottom separator and quit
        separator3 = ttk.Separator(main_frame, orient='horizontal')
        separator3.pack(fill=tk.X, pady=20)
        
        quit_button = ttk.Button(main_frame, text="Quit Timer", 
                                command=self.quit_app)
        quit_button.pack(fill=tk.X, pady=(10, 0))
        
        # Handle window close button
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
    
    def create_window_icon(self):
        """Create a simple icon for the window."""
        image = Image.new('RGB', (64, 64), color='#0078D4')
        draw = ImageDraw.Draw(image)
        draw.text((20, 20), "T", fill='white')
        return image
    
    def parse_smart_input(self, input_str):
        """Parse smart input like '1h 25m 30s' into total seconds."""
        input_str = input_str.strip().lower()
        
        # Pattern matching for hours, minutes, seconds
        hours = 0
        minutes = 0
        seconds = 0
        
        # Find hours
        h_match = re.search(r'(\d+)\s*h', input_str)
        if h_match:
            hours = int(h_match.group(1))
        
        # Find minutes
        m_match = re.search(r'(\d+)\s*m(?!s)', input_str)
        if m_match:
            minutes = int(m_match.group(1))
        
        # Find seconds
        s_match = re.search(r'(\d+)\s*s', input_str)
        if s_match:
            seconds = int(s_match.group(1))
        
        total = hours * 3600 + minutes * 60 + seconds
        return total
    
    def start_timer(self):
        """Start the timer with input from either smart or custom boxes."""
        if self.is_running:
            return
        
        # Try smart input first
        smart_text = self.smart_input.get().strip()
        if smart_text:
            self.total_seconds = self.parse_smart_input(smart_text)
        else:
            # Use custom split inputs
            try:
                hours = int(self.hours_input.get() or "0")
                minutes = int(self.minutes_input.get() or "0")
                seconds = int(self.seconds_input.get() or "0")
                self.total_seconds = hours * 3600 + minutes * 60 + seconds
            except ValueError:
                self.status_label.config(text="Invalid input!", foreground="red")
                return
        
        if self.total_seconds <= 0:
            self.status_label.config(text="Please enter a valid time!", foreground="red")
            return
        
        self.remaining_seconds = self.total_seconds
        self.is_running = True
        self.status_label.config(text="Timer running...", foreground="green")
        self.start_button.config(state=tk.DISABLED)
        
        # Start timer in background thread
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
    
    def run_timer(self):
        """Run the countdown timer."""
        while self.is_running and self.remaining_seconds > 0:
            time.sleep(1)
            self.remaining_seconds -= 1
            self.update_display()
            self.update_tray_text()
        
        # Timer finished
        if self.is_running and self.remaining_seconds <= 0:
            self.is_running = False
            self.remaining_seconds = 0
            self.update_display()
            self.play_alert()
            self.status_label.config(text="Timer complete!", foreground="blue")
            self.start_button.config(state=tk.NORMAL)
            self.update_tray_text()
    
    def update_display(self):
        """Update the timer display in the UI."""
        if self.root:
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)
    
    def pause_timer(self):
        """Pause the running timer."""
        if self.is_running:
            self.is_running = False
            self.status_label.config(text="Timer paused", foreground="orange")
            self.start_button.config(state=tk.NORMAL)
            self.update_tray_text()
        elif self.remaining_seconds > 0 and not self.is_running:
            # Resume
            self.start_timer()
    
    def reset_timer(self):
        """Reset the timer."""
        self.is_running = False
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.smart_input.delete(0, tk.END)
        self.hours_input.delete(0, tk.END)
        self.hours_input.insert(0, "0")
        self.minutes_input.delete(0, tk.END)
        self.minutes_input.insert(0, "0")
        self.seconds_input.delete(0, tk.END)
        self.seconds_input.insert(0, "0")
        self.timer_label.config(text="00:00:00")
        self.status_label.config(text="Ready", foreground="gray")
        self.start_button.config(state=tk.NORMAL)
        self.update_display()
        self.update_tray_text()
    
    def play_alert(self):
        """Play a Windows system alert sound."""
        try:
            # Play Windows default alert sound (beep)
            winsound.Beep(1000, 500)  # 1000 Hz, 500 ms
            time.sleep(0.2)
            winsound.Beep(1000, 500)
        except Exception as e:
            print(f"Could not play alert sound: {e}")
    
    def quit_app(self):
        """Quit the application."""
        self.is_running = False
        if self.root:
            self.root.destroy()
        if self.tray_icon:
            self.tray_icon.stop()
        sys.exit(0)


def main():
    """Main entry point."""
    try:
        app = TimerApp()
        app.show_window()
        
        # Keep the app running
        if app.root:
            app.root.mainloop()
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("\nPlease install required packages with:")
        print("  pip install pystray pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
