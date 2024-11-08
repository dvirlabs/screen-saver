import tkinter as tk
import time
from datetime import datetime

# Manually defined Hebrew months and days
HEBREW_MONTHS = [
    "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", 
    "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
]

HEBREW_DAYS = [
    "ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"
]

class Screensaver:
    def __init__(self):
        # Initialize the Tkinter root window
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Make it fullscreen
        self.root.configure(bg='black')  # Set background color to black
        self.root.overrideredirect(True)  # Remove window borders and controls

        # Set canvas size to fill the full screen
        self.canvas_width = self.root.winfo_screenwidth()  # Full screen width
        self.canvas_height = self.root.winfo_screenheight()  # Full screen height

        # Create canvas to display content
        self.canvas = tk.Canvas(self.root, bg="black", height=self.canvas_height, width=self.canvas_width, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.last_activity_time = time.time()  # Track time of last activity
        self.inactivity_threshold = 5  # Seconds of inactivity before screensaver starts

        # Setup event listeners for mouse movement, key press, and mouse click
        self.root.bind("<Motion>", self.reset_inactivity_timer)
        self.root.bind("<Key>", self.reset_inactivity_timer)
        self.root.bind("<Button-1>", self.exit_screensaver)  # Mouse click to exit
        self.root.bind("<Escape>", self.exit_screensaver)    # Escape key to exit

        # Start the screensaver
        self.run_screensaver()

        # Start the Tkinter main loop
        self.root.mainloop()

    def draw_time(self):
        """Display the current time and date in Hebrew."""
        # Get the current date and time
        now = datetime.now()
        
        # Adjust the weekday to match the Hebrew days (shift Sunday to the start)
        day_of_week = HEBREW_DAYS[(now.weekday() + 1) % 7]
        day_of_month = now.day
        month_name = HEBREW_MONTHS[now.month - 1]  # Get the month from the list
        year = now.year
        hour = now.hour
        minute = now.minute
        second = now.second
        
        # Format the date and time string in Hebrew
        time_string = f"{day_of_week}, {day_of_month} {month_name} {year} {hour:02d}:{minute:02d}:{second:02d}"

        # Wrap the text to avoid cutting off
        text_lines = self.wrap_text(time_string, self.canvas_width - 40)  # 40px padding

        # Calculate vertical position to center the text block
        total_text_height = len(text_lines) * 80  # 80px for each line of text (font size)
        y_offset = (self.canvas_height - total_text_height) // 2  # Center vertically

        # Display the wrapped time and date in a larger font
        for line in text_lines:
            # Horizontal centering
            self.canvas.create_text(self.canvas_width // 2, y_offset, text=line, fill="white", font=("Arial", 70), anchor="center")
            y_offset += 80  # Move the next line down (increased spacing)

    def wrap_text(self, text, max_width):
        """Wrap the text to fit within the canvas width."""
        words = text.split(" ")
        lines = []
        current_line = ""
        
        for word in words:
            # Add the word to the line if it fits within the width
            test_line = f"{current_line} {word}".strip()
            bbox = self.canvas.bbox(self.canvas.create_text(0, 0, text=test_line, font=("Arial", 70)))
            if bbox[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def reset_inactivity_timer(self, event=None):
        """Reset the inactivity timer when there's mouse movement or key press.""" 
        self.last_activity_time = time.time()

    def exit_screensaver(self, event=None):
        """Exit the screensaver when a key is pressed or mouse is clicked.""" 
        self.root.quit()  # This will stop the Tkinter main loop and exit the application

    def run_screensaver(self):
        """Start the screensaver and schedule the drawing updates."""
        # Initial draw
        self.canvas.delete("all")  # Clear the canvas
        self.draw_time()  # Draw the current time and date in Hebrew
        
        # Schedule the update function to run every 1000 ms (1 second)
        self.root.after(1000, self.update_screensaver)

    def update_screensaver(self):
        """Update the screensaver every second."""
        self.canvas.delete("all")  # Clear the canvas
        self.draw_time()  # Redraw the current time and date in Hebrew
        
        # Schedule the next update in 1 second
        self.root.after(1000, self.update_screensaver)

if __name__ == "__main__":
    Screensaver()
