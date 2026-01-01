#!/usr/bin/env python3
"""
Time & Energy Audit Tracker
Inspired by Dan Martell's time tracking strategy
Pops up every 15 minutes to log activities with color coding and dollar values

Copyright (c) 2026 Arty McLabin
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font
import os
import re
import sys

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Tracker - Dan Martell Method")
        self.root.geometry("600x400")

        # Excel file setup
        self.excel_file = "time_audit.xlsx"
        self.setup_excel()

        # Timer setup
        self.timer_minutes = 15
        self.timer_thread = None
        self.timer_running = False
        self.has_popped = False  # Track if we've already popped up for this cycle

        # Color mapping for Excel
        self.color_fills = {
            'green': PatternFill(start_color='90EE90', end_color='90EE90', fill_type='solid'),
            'red': PatternFill(start_color='FFB6C1', end_color='FFB6C1', fill_type='solid'),
            'white': PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        }

        self.setup_ui()
        self.start_timer()

    def setup_excel(self):
        """Initialize Excel file with headers if it doesn't exist"""
        if not os.path.exists(self.excel_file):
            wb = Workbook()
            ws = wb.active
            ws.title = "Time Audit"

            # Headers
            headers = ['Date & Time', 'Energy', 'Value', 'Activity']
            ws.append(headers)

            # Make headers bold
            for cell in ws[1]:
                cell.font = Font(bold=True)

            wb.save(self.excel_file)

    def setup_ui(self):
        """Create the UI"""
        # Instructions
        instructions = tk.Label(
            self.root,
            text='Enter your activities (one per line):\nFormat: "green $$ did some coding" or "red $$$ boring meeting"',
            font=('Consolas', 10),
            justify=tk.LEFT,
            bg='#1e1e1e',
            fg='#00ff00',
            padx=10,
            pady=10
        )
        instructions.pack(fill=tk.X)

        # Timer display
        self.timer_label = tk.Label(
            self.root,
            text="Next reminder in: 15:00",
            font=('Consolas', 12, 'bold'),
            bg='#1e1e1e',
            fg='#ffff00'
        )
        self.timer_label.pack(pady=5)

        # Text input area (CLI-style)
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            width=70,
            height=15,
            font=('Consolas', 11),
            bg='#0c0c0c',
            fg='#00ff00',
            insertbackground='#00ff00',
            selectbackground='#264f78',
            wrap=tk.WORD
        )
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.focus()

        # Submit button
        submit_btn = tk.Button(
            self.root,
            text="Submit Entries",
            command=self.submit_entries,
            font=('Consolas', 11, 'bold'),
            bg='#0e639c',
            fg='#ffffff',
            activebackground='#1177bb',
            activeforeground='#ffffff',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        submit_btn.pack(pady=10)

        # Bind Ctrl+Enter to submit
        self.root.bind('<Control-Return>', lambda e: self.submit_entries())

        # Set window colors
        self.root.configure(bg='#1e1e1e')

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_timer(self):
        """Start the 15-minute countdown timer"""
        self.timer_running = True
        self.has_popped = False
        self.timer_thread = threading.Thread(target=self.countdown, daemon=True)
        self.timer_thread.start()

    def countdown(self):
        """Countdown from 15 minutes and pop window when done"""
        total_seconds = self.timer_minutes * 60

        while total_seconds > 0 and self.timer_running:
            mins, secs = divmod(total_seconds, 60)
            time_str = f"Next reminder in: {mins:02d}:{secs:02d}"

            # Update timer display
            self.timer_label.config(text=time_str)

            time.sleep(1)
            total_seconds -= 1

        if self.timer_running and not self.has_popped:
            # Time's up! Pop the window to foreground
            self.pop_window()
            self.has_popped = True

    def pop_window(self):
        """Bring window to foreground (pop up)"""
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()
        self.text_area.focus()

        # Flash the window to get attention
        self.root.state('normal')  # Ensure it's not minimized

        # Update timer label to show it's time
        self.timer_label.config(text="⏰ TIME TO LOG! ⏰", fg='#ff0000')

    def parse_entry(self, line):
        """Parse a single entry line
        Format: "green $$ did some coding"
        Returns: (color, dollars, activity) or None if invalid
        """
        line = line.strip()
        if not line:
            return None

        # Pattern: (color) (dollars) (activity)
        pattern = r'^(green|red|white)\s+(\$+)\s+(.+)$'
        match = re.match(pattern, line, re.IGNORECASE)

        if match:
            color = match.group(1).lower()
            dollars = match.group(2)
            activity = match.group(3)
            return (color, dollars, activity)
        else:
            return None

    def submit_entries(self):
        """Process and save all entries to Excel"""
        text = self.text_area.get("1.0", tk.END)
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        if not lines:
            messagebox.showwarning("No entries", "Please enter at least one activity.")
            return

        # Parse all entries
        entries = []
        invalid_lines = []

        for line in lines:
            parsed = self.parse_entry(line)
            if parsed:
                entries.append(parsed)
            else:
                invalid_lines.append(line)

        if invalid_lines:
            msg = "Invalid format in these lines:\n" + "\n".join(invalid_lines)
            msg += '\n\nExpected format: "green $$ activity description"'
            messagebox.showerror("Invalid Format", msg)
            return

        if not entries:
            messagebox.showwarning("No valid entries", "No valid entries to save.")
            return

        # Save to Excel
        try:
            wb = load_workbook(self.excel_file)
            ws = wb.active

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for color, dollars, activity in entries:
                row = [timestamp, color.capitalize(), dollars, activity]
                ws.append(row)

                # Apply color to the entire row
                row_num = ws.max_row
                for col in range(1, 5):
                    cell = ws.cell(row=row_num, column=col)
                    cell.fill = self.color_fills[color]

            wb.save(self.excel_file)

            # Clear text area
            self.text_area.delete("1.0", tk.END)

            # Reset timer
            self.timer_running = False
            time.sleep(0.1)  # Give time for thread to stop
            self.start_timer()

            # Show success message
            messagebox.showinfo("Success", f"Saved {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} to {self.excel_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entries:\n{str(e)}")

    def on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit the Time Tracker?"):
            self.timer_running = False
            self.root.destroy()
            sys.exit(0)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()
