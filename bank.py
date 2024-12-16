import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Button, Label, Frame, Entry, Meter
from ttkbootstrap.tableview import Tableview
import pathlib
import pandas as pd
from os.path import exists
from os import mkdir
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import nametofont
import sys


def main():
    app = App()


class App(ttk.Window):

    def __init__(self):
        super().__init__("litera")

        self.title("The Bank")
        self.geometry("1600x900")

        self.load_data()
        self.create_layout()
        self.load_update_frames_data()

        self.mainloop()

    def create_layout(self):
        # creating a frame to be the parent of the two child frames(it's for layout)
        frame = Frame(self)
        self.top_bar = self.construct_top_bar()
        self.table_frame = self.construct_table_frame(frame)
        self.chart_frame = self.construct_charts(frame)

        self.top_bar.pack(side=TOP, fill=X)

        frame.columnconfigure(index=1, weight=3, uniform="a")
        frame.columnconfigure(index=2, weight=2, uniform="a")
        frame.rowconfigure(index=1, weight=1, uniform="a")

        self.table_frame.grid(column=1, row=1, sticky=NSEW)
        self.chart_frame.grid(column=2, row=1, sticky=NSEW)

        frame.pack(side=BOTTOM, expand=True, fill=BOTH)

    def load_data(self):
        try:
            self.data = pd.read_csv(
                r"data.csv",
            )
        except (pd.errors.EmptyDataError, FileNotFoundError):
            self.data = pd.DataFrame(
                columns=["Group Name", "Rank", "Ans. Questions", "Wealth"]
            )

    def save_data(self):
        self.data.to_csv(r"data.csv", index=False)

    def load_update_frames_data(self):
        self.table.load_update_data()
        self.wealth_chart.update_chart()
        self.answered_chart.update_chart()

    def configure_inflation(self):
        # main-setup
        configuration_window = ttk.Toplevel(
            title="Inflation configuration",
            resizable=(False, False),
        )

        configuration_window.attributes("-topmost", 1)

        # creating the widgets
        spinbox_frame = ttk.Frame(configuration_window, padding=50)

        lable = Label(
            configuration_window, text="Please Configure the Inflation", padding=10
        )
        lable.pack(side=TOP)

        minutes_spinbox = ttk.Spinbox(
            spinbox_frame,
            from_=0,
            to=59,
            font=("Helvetica", 16),
            width=5,
            justify="center",
            bootstyle=INFO,
        )
        minutes_spinbox.set(0)  # Set default value for minutes
        minutes_spinbox.pack(side=LEFT, padx=5)

        colon_label = ttk.Label(spinbox_frame, text=":", font=("Helvetica", 25))
        colon_label.pack(side=LEFT)

        seconds_spinbox = ttk.Spinbox(
            spinbox_frame,
            from_=0,
            to=59,
            font=("Helvetica", 16),
            width=5,
            justify="center",
            bootstyle=INFO,
        )
        seconds_spinbox.set(0)  # Set default value for seconds
        seconds_spinbox.pack(side=LEFT, padx=5)

        Inflation_percentage_frame = Frame(spinbox_frame)
        Inflation_percentage_spinbox = ttk.Spinbox(
            Inflation_percentage_frame,
            from_=1,
            to=250,
            font=("Helvetica", 16),
            width=5,
            justify="center",
            bootstyle=INFO,
        )
        Inflation_percentage_spinbox.set(15)
        Inflation_percentage_spinbox.pack(side=LEFT)
        percentage_label = ttk.Label(
            Inflation_percentage_frame, text="%", font=("Helvetica", 25)
        )
        percentage_label.pack(side=RIGHT)
        Inflation_percentage_frame.pack(padx=20)

        spinbox_frame.pack(pady=5)

        # Add a configure button
        configure_button = ttk.Button(
            configuration_window,
            text="Configure",
            bootstyle=PRIMARY,
            command=lambda: (
                self.inflation_count_down.start_countdown(
                    time_input=f"{int(minutes_spinbox.get()):02}:{int(seconds_spinbox.get()):02}",
                    inflation_rate=int(Inflation_percentage_spinbox.get()),
                ),
                configuration_window.destroy(),
            ),
        )
        configure_button.pack(pady=10)

    def inflate_wealth(self):
        self.data["Wealth"] = self.data["Wealth"].apply(
            lambda x: x * (self.inflation_rate + 100) / 100
        )
        self.data["Wealth"] = self.data["Wealth"].astype(int)

        self.load_update_frames_data()

    def construct_top_bar(self):
        # Set font and size
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 16))

        # configuring the frame
        frame = Frame(self)
        frame.columnconfigure(index=1, weight=1, uniform="a")
        frame.columnconfigure(index=2, weight=1, uniform="a")
        frame.columnconfigure(index=3, weight=1, uniform="a")
        frame.rowconfigure(index=1, weight=1, uniform="a")

        # creating the left side buttons
        status_controls_frame = Frame(frame)
        status_controls_frame.columnconfigure(index=1, weight=1, uniform="a")
        status_controls_frame.columnconfigure(index=2, weight=1, uniform="a")
        status_controls_frame.columnconfigure(index=3, weight=1, uniform="a")

        # creating the inflation meter
        self.inflation_count_down = InflationCountDown(frame, self)
        self.meter = self.inflation_count_down.get_meter()
        self.meter.grid(column=2, row=1)

        self.start_btn = Button(
            status_controls_frame,
            text="Start",
            style=SUCCESS,
            padding=12,
            command=self.inflation_count_down.start_countdown,
        )
        self.stop_btn = Button(
            status_controls_frame,
            text="Stop",
            style=DANGER,
            padding=12,
            command=self.inflation_count_down.stop_countdown,
        )
        self.end_btn = Button(
            status_controls_frame,
            text="End",
            style="warning-outline",
            padding=12,
            command=self.inflation_count_down.end_countdown,
        )

        self.start_btn.grid(column=1, row=1)
        self.stop_btn.grid(column=2, row=1)
        self.end_btn.grid(column=3, row=1)
        status_controls_frame.grid(column=1, row=1, sticky=EW)

        # creating the reset button
        self.reset_btn = Button(frame, text="Reset", style="info-outline", padding=12)
        self.save_btn = Button(
            frame, text="Save", style=SUCCESS, padding=12, command=self.save_data
        )
        self.config_inflation = Button(
            frame,
            text="Configure Inflation⚙️",
            style="info-outline",
            padding=12,
            command=self.configure_inflation,
        )

        self.save_btn.grid(column=3, row=1, sticky=E, padx=20)
        self.reset_btn.grid(column=3, row=1, sticky=E, padx=120)
        self.config_inflation.grid(column=3, row=1, sticky=W)

        return frame

    def construct_table_frame(self, parent):

        # Define the font for the Entry widget
        entry_font = ("Helvetica", 16)  # Font family and size

        # girding the frame
        frame = Frame(parent, padding=10)
        frame.columnconfigure(index=1, weight=1, uniform="a")
        frame.columnconfigure(index=2, weight=1, uniform="a")
        frame.columnconfigure(index=3, weight=1, uniform="a")
        frame.columnconfigure(index=4, weight=1, uniform="a")
        frame.columnconfigure(index=5, weight=1, uniform="a")
        frame.columnconfigure(index=6, weight=1, uniform="a")

        frame.rowconfigure(index=1, weight=1, uniform="a")
        frame.rowconfigure(index=2, weight=4, uniform="a")

        # creating the group tables
        self.table = GroupsTable(
            parent=frame, app=self
        )  # feeding the frame and the app instance to the class
        self.table_widget = self.table.get_table()
        """I create the table first to create the instances for the bottoms"""

        # creating the control buttons

        self.new_group_name = ttk.StringVar(value="Group name")
        group_name_entry = Entry(
            frame, textvariable=self.new_group_name, font=entry_font
        )
        add_group_btn = Button(
            frame, text="Add", style=SUCCESS, command=self.table.add_row
        )

        self.deposit_value = ttk.IntVar()
        deposit_entry = Entry(frame, textvariable=self.deposit_value, font=entry_font)
        deposit_btn = Button(
            frame, text="Deposit", style=SUCCESS, command=self.table.deposit_money
        )

        self.Withdrawal_value = ttk.IntVar()
        Withdrawal_entry = Entry(
            frame, textvariable=self.Withdrawal_value, font=entry_font
        )
        Withdrawal_btn = Button(
            frame, text="Withdrawal", style=SUCCESS, command=self.table.withdrawal_money
        )

        group_name_entry.grid(column=1, row=1)
        add_group_btn.grid(column=2, row=1)

        deposit_entry.grid(column=3, row=1)
        deposit_btn.grid(column=4, row=1)

        Withdrawal_entry.grid(column=5, row=1)
        Withdrawal_btn.grid(column=6, row=1)

        self.table_widget.grid(column=1, columnspan=6, row=2, sticky=NSEW)

        return frame

    def construct_charts(self, parent):
        frame = Frame(parent)
        frame.columnconfigure(index=1, weight=1, uniform="a")
        frame.rowconfigure(index=1, weight=1, uniform="a")
        frame.rowconfigure(index=2, weight=1, uniform="a")

        self.wealth_chart = PieChart(parent=frame, app=self, value_type="Wealth")
        self.wealth_chart_frame = self.wealth_chart.get_chart()

        self.answered_chart = PieChart(
            parent=frame, app=self, value_type="Ans. Questions"
        )
        self.answered_chart_frame = self.answered_chart.get_chart()

        self.wealth_chart_frame.grid(column=1, row=1, sticky=NSEW)
        self.answered_chart_frame.grid(column=1, row=2, sticky=NSEW)

        return frame


class InflationCountDown:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.remaining_time = 0
        self.timer_running = False
        self.meter = Meter(
            self.parent,
            subtext="00:00",
            interactive=False,
            amounttotal=600,  # Default total seconds (10 minutes)
            showtext=False,
            subtextfont=("Helvetica", 25),
            subtextstyle=DANGER,
            metertype=SEMI,
            stripethickness=6,
            meterthickness=15,
            metersize=250,
            amountused=600,
            padding=0,
        )

    def format_time(self, seconds):
        """Convert seconds to MM:SS format."""
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02}:{sec:02}"

    def update_countdown(self):
        """Update the meter during the countdown."""
        if self.timer_running and self.remaining_time >= 0:
            self.meter.configure(
                subtext=self.format_time(self.remaining_time),
                amountused=self.remaining_time,
            )
            self.remaining_time -= 1
            self.parent.after(1000, self.update_countdown)  # Schedule the next update
        elif self.remaining_time < 0:
            self.app.inflate_wealth()
            # Reset coutdown
            self.remaining_time = self.meter["amounttotal"]  # Reset to initial time
            self.update_countdown()  # Restart the countdown

    def start_countdown(self, time_input=None, inflation_rate=15):
        self.app.inflation_rate = inflation_rate
        self.time_input = time_input
        """Start or continue the countdown."""
        if not self.timer_running:
            if time_input:
                try:
                    minutes, seconds = map(int, time_input.split(":"))
                    self.remaining_time = minutes * 60 + seconds
                    self.meter.configure(
                        amounttotal=self.remaining_time, amountused=self.remaining_time
                    )
                except ValueError:
                    self.meter.configure(subtext="Invalid input")
                    return
            self.timer_running = True
            self.update_countdown()

    def stop_countdown(self):
        """Temporarily stop the countdown."""
        self.timer_running = False

    def end_countdown(self):
        """Reset the countdown to the initial state."""
        self.timer_running = False
        self.remaining_time = 0
        self.meter.configure(subtext="00:00", amountused=0)

    def get_meter(self):
        """Return the meter frame for placement."""
        return self.meter


class GroupsTable:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # determining the font size for the table
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=18, weight="bold")
        # Create Tableview widget
        self.table = Tableview(
            master=parent,
            paginated=False,  # Enables pagination
            searchable=True,  # Adds a search bar
            stripecolor=("#B2DF8A", None),
        )

        self.load_update_data()

    def add_row(self):
        group_name = self.app.new_group_name.get()
        self.app.new_group_name.set("")
        new_row = [group_name, 0, 0, 0]  # creating the new frame using place holders

        self.app.data.loc[len(self.app.data)] = (
            new_row  # adding the new row to the end of the dataframe
        )

        self.app.load_update_frames_data()

    def deposit_money(self):
        selected_item = self.table.view.selection()
        if selected_item:
            try:
                # finds the group name and changes the corresponding wealth value in the dataframe
                group = self.table.view.item(selected_item)["values"][0]
                group_row = self.app.data[self.app.data["Group Name"] == group].index[0]
                self.app.data.at[group_row, "Wealth"] += float(
                    self.app.deposit_value.get()
                )

                # adding the ans questions count
                self.app.data.at[group_row, "Ans. Questions"] += 1

                self.load_update_data()
            except ValueError:
                print("Enter a valid number.")

        self.app.load_update_frames_data()

    def withdrawal_money(self):
        selected_item = self.table.view.selection()
        if selected_item:
            try:
                # finds the group name and changes the corresponding wealth value in the dataframe
                group = self.table.view.item(selected_item)["values"][0]
                group_row = self.app.data[self.app.data["Group Name"] == group].index[0]
                self.app.data.at[group_row, "Wealth"] -= float(
                    self.app.Withdrawal_value.get()
                )

                self.load_update_data()
            except ValueError:
                print("Enter a valid number.")

        self.app.load_update_frames_data()

    def load_update_data(self):
        # Rank the 'Wealth' values and add the rank to a new column 'Rank'
        self.app.data["Rank"] = (
            self.app.data["Wealth"].rank(ascending=False, method="min").astype(int)
        )

        # Convert DataFrame to columns and rows for build_table_data
        columns = [{"text": col, "stretch": True} for col in self.app.data.columns]
        rows = (
            self.app.data.values.tolist()
        )  # Converts DataFrame rows to a list of lists

        # set the data
        self.table.build_table_data(
            coldata=columns,
            rowdata=rows,
        )

        # making it beautiful
        self.table.align_column_center(cid=0)
        self.table.align_column_center(cid=1)
        self.table.align_column_center(cid=2)
        self.table.align_column_center(cid=3)
        self.table.align_heading_center(cid=0)
        self.table.align_heading_center(cid=1)
        self.table.align_heading_center(cid=2)
        self.table.align_heading_center(cid=3)
        self.table.autofit_columns()

    def get_table(self):
        return self.table


class PieChart:
    def __init__(self, parent, app, value_type):
        """Initialize the PieChartWidget class."""
        self.frame = ttk.Frame(parent)
        self.app = app
        self.value_type = value_type

        self.plot_pie_chart()

    def plot_pie_chart(self):
        """Plot the pie chart based on the current data."""
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            self.app.data[self.value_type],
            labels=self.app.data["Group Name"],
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Paired.colors,
        )
        ax.set_title(f"{self.value_type} Chart")

        # Embed the plot in the frame
        self.canvas = FigureCanvasTkAgg(fig, self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=BOTH, expand=True)
        self.canvas.draw()

    def update_chart(self):
        """Update the chart with new data."""
        # Clear the existing canvas
        self.canvas_widget.pack_forget()

        # Plot the updated chart
        self.plot_pie_chart()

    def get_chart(self):
        """Return the chart widget."""
        return self.frame


if __name__ == "__main__":
    main()
