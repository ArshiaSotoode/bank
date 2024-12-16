import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


def validate_time_format(minutes, seconds):
    """Validate that minutes and seconds are within valid ranges."""
    return 0 <= minutes and 0 <= seconds < 60


def submit_time():
    """Handle the time submission."""
    try:
        minutes = int(minutes_spinbox.get())
        seconds = int(seconds_spinbox.get())
        if validate_time_format(minutes, seconds):
            time_input = f"{minutes:02}:{seconds:02}"
            messagebox.showinfo("Invalid Input", f"{time_input}")

        else:
            messagebox.showerror(
                "Invalid Input", "Please enter valid values for minutes and seconds."
            )
    except ValueError:
        messagebox.showerror("Invalid Input", "Please ensure all inputs are numeric.")


# Create the main application window
app = ttk.Window(themename="superhero")
app.title("Time Entry App")
app.geometry("300x200")

# Add a label
time_label = ttk.Label(app, text="Set time (MM:SS):", font=("Helvetica", 12))
time_label.pack(pady=10)

# Add spinboxes for minute and second selection
spinbox_frame = ttk.Frame(app)
spinbox_frame.pack(pady=5)

minutes_spinbox = ttk.Spinbox(
    spinbox_frame,
    from_=0,
    to=59,
    font=("Helvetica", 12),
    width=5,
    justify="center",
    bootstyle=INFO,
)
minutes_spinbox.set(0)  # Set default value for minutes
minutes_spinbox.pack(side=LEFT, padx=5)

colon_label = ttk.Label(spinbox_frame, text=":", font=("Helvetica", 12))
colon_label.pack(side=LEFT)

seconds_spinbox = ttk.Spinbox(
    spinbox_frame,
    from_=0,
    to=59,
    font=("Helvetica", 12),
    width=5,
    justify="center",
    bootstyle=INFO,
)
seconds_spinbox.set(0)  # Set default value for seconds
seconds_spinbox.pack(side=LEFT, padx=5)

# Add a submit button
submit_button = ttk.Button(app, text="Submit", bootstyle=PRIMARY, command=submit_time)
submit_button.pack(pady=10)

# Run the application
app.mainloop()
