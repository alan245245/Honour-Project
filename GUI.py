import sys
from tkinter import *
from tkinter import Tk, ttk
from tkinter.scrolledtext import ScrolledText
import time
import re

import Simulator as Simulator
from PrintLogger import PrintLogger

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Elevator Simulator")

        # Init log frame and widget
        self.log_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=100)
        self.log_widget = ScrolledText(self.log_frame, width=200, height=8, font=("consolas", "8", "normal"))
        self.log_widget.configure(state='disabled')

        # Init options frame and label
        self.option_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=100)
        self.option_framelbl = ttk.Label(self.option_frame, text="Options")

        # Init simulator options frame, label and radio buttonw
        self.simulator_option = ttk.Frame(self.option_frame, padding=2)
        self.simulator_mode = StringVar()
        self.simulator_modelbl = ttk.Label(self.simulator_option, text="Simulation Mode")
        self.real_time = ttk.Radiobutton(self.simulator_option, text='Real-time', variable=self.simulator_mode, value='real')
        self.fixed_time = ttk.Radiobutton(self.simulator_option, text='Fixed-time', variable=self.simulator_mode, value='static')

        # Init passenger option frame, label and radio buttons
        self.passenger_options = ttk.Frame(self.option_frame, padding=2)
        self.passenger_mode = StringVar()
        self.passenger_modelbl = ttk.Label(self.passenger_options, text="Passenger Mode")
        self.random_passenger = ttk.Radiobutton(self.passenger_options, text='Random', variable=self.passenger_mode, value='random')
        self.preset_passenger = ttk.Radiobutton(self.passenger_options, text='Preset', variable=self.passenger_mode, value='preset')

        # check num wrapper
        check_num = (self.register(self.check_num), '%P')
        # Init number of passenger frame, label and entry
        self.number_of_passenger_options = ttk.Frame(self.option_frame, padding=2)
        self.number_of_passenger = StringVar()
        self.number_of_passengerlbl = ttk.Label(self.number_of_passenger_options, text="No. of Passengers: ")
        self.number_of_passenger_entry = ttk.Entry(self.number_of_passenger_options, textvariable=self.number_of_passenger, width=6, validate='key', validatecommand=check_num)

        # Init number of floor frame, label and entry
        self.number_of_floor_options = ttk.Frame(self.option_frame, padding=2)
        self.number_of_floor = StringVar()
        self.number_of_floorlbl = ttk.Label(self.number_of_floor_options, text="No. of Floor: ")
        self.number_of_floor_entry = ttk.Entry(self.number_of_floor_options, textvariable=self.number_of_floor, width=6, validate='key', validatecommand=check_num)

        # Init passenger preset frame, label and combo box
        self.passenger_preset_options = ttk.Frame(self.option_frame, padding=2)
        self.passenger_preset = StringVar()
        self.passenger_presetlbl = ttk.Label(self.passenger_preset_options, text="Select Preset")
        self.passenger_preset_menu = ttk.Combobox(self.passenger_preset_options, textvariable=self.passenger_preset)
        self.passenger_preset_menu['values'] = ('Morning Rush', 'Evening Rush', 'Distributed')

        # Init elevator algorithm frame, label and combo box
        self.elevator_algorithm_options = ttk.Frame(self.option_frame, padding=2)
        self.elevator_algorithm = StringVar()
        self.elevator_algorithmlbl = ttk.Label(self.elevator_algorithm_options, text="Select Elevator Algorithm")
        self.elevator_algorithm_menu = ttk.Combobox(self.elevator_algorithm_options, textvariable=self.elevator_algorithm)
        self.elevator_algorithm_menu['values'] = ('Proposed', 'Nearest-First')

        # Init action buttons frame, start and cancel button
        self.action_buttons_frame = ttk.Frame(self.option_frame, padding=2)
        self.button_start = ttk.Button(self.action_buttons_frame, text="Start", command=self.start_real_time_simulation)
        self.button_reset = ttk.Button(self.action_buttons_frame, text="Reset", command=self.reset_form)

        # Init output csv frame
        self.csv_output_enabled_frame = ttk.Frame(self.option_frame, padding=2)
        self.csv_output_enabledlbl = ttk.Label(self.csv_output_enabled_frame, text="CSV output")
        self.csv_output_enabled = StringVar()
        self.csv_button_enabled = ttk.Radiobutton(self.csv_output_enabled_frame, text='Enabled', variable=self.csv_output_enabled, value='True')
        self.csv_button_disabled = ttk.Radiobutton(self.csv_output_enabled_frame, text='Disabled', variable=self.csv_output_enabled, value='False')
        self.csv_file_name_frame = ttk.Frame(self.option_frame, padding=2)
        self.csv_file_namelbl = ttk.Label(self.csv_file_name_frame, text="Name of output file")
        self.csv_file_name = StringVar()
        self.csv_file_name_entry = ttk.Entry(self.csv_file_name_frame, textvariable=self.csv_file_name)
        self.csv_file_name_entry.insert(0, time.strftime("SimulationData-%Y%m%d-%H%M%S"))
        self.csv_batch_simulation_frame = ttk.Frame(self.option_frame, padding=2)
        self.csv_batch_simulationlbl = ttk.Label(self.csv_batch_simulation_frame, text="Batch Simulation (Default 1)")
        self.csv_batch_simulation = StringVar()
        self.csv_batch_simulation_entry = ttk.Entry(self.csv_batch_simulation_frame, textvariable=self.csv_batch_simulation, width=6, validate='key', validatecommand=check_num)

        summary_frame = ttk.Frame(self)

        # Positioning frames and widgets
        self.log_frame.grid(column=0, row=0, sticky='N S E W')
        self.log_widget.grid(column=0, row=0, sticky='N S E W')
        self.option_frame.grid(column=3, row=0, columnspan=2, rowspan=2, sticky='N S E W')
        self.option_framelbl.grid(column=3, row=0, sticky='N W')
        self.simulator_option.grid(column=3, row=1, columnspan=2, rowspan=2, sticky='N S E W')
        self.simulator_modelbl.grid(column=3, row=1, sticky='N W')
        self.real_time.grid(column=3, row=2, sticky='N W')
        self.fixed_time.grid(column=4, row=2, sticky='N W')
        self.passenger_options.grid(column=3, row=3, columnspan=2, rowspan=2, sticky='N S E W')
        self.passenger_modelbl.grid(column=3, row=3, sticky='N W')
        self.random_passenger.grid(column=3, row=4, sticky='N W')
        self.preset_passenger.grid(column=4, row=4, sticky='N W')
        self.number_of_passenger_options.grid(column=3, row=5, columnspan=2, sticky='N W')
        self.number_of_passengerlbl.grid(column=3, row=6, sticky='N W')
        self.number_of_passenger_entry.grid(column=4, row=6, sticky='N W')
        self.number_of_floor_options.grid(column=3, row=7, columnspan=2, sticky='N W')
        self.number_of_floorlbl.grid(column=3, row=7, sticky='N W')
        self.number_of_floor_entry.grid(column=4, row=7, sticky='N W')
        self.passenger_preset_options.grid(column=3, row=8, columnspan=2, rowspan=2, sticky='N W')
        self.passenger_presetlbl.grid(column=3, row=8, sticky='N W')
        self.passenger_preset_menu.grid(column=3, row=9, columnspan=2, sticky='N W')
        self.elevator_algorithm_options.grid(column=3, row=10, rowspan=2, sticky='N W')
        self.elevator_algorithmlbl.grid(column=3, row=10, sticky='N W')
        self.elevator_algorithm_menu.grid(column=3, row=11, sticky='N W')
        self.csv_output_enabled_frame.grid(column=3, row=12, columnspan=2, sticky='N W')
        self.csv_output_enabledlbl.grid(column=3, row=12, sticky='N W')
        self.csv_button_enabled.grid(column=3, row=13, sticky='N W')
        self.csv_button_disabled.grid(column=4, row=13, sticky='N W')
        self.csv_file_name_frame.grid(column=3, row=14, sticky='N W')
        self.csv_file_namelbl.grid(column=3, row=14, sticky='N W')
        self.csv_file_name_entry.grid(column=3, row=15, columnspan=2, sticky='N W')
        self.csv_batch_simulation_frame.grid(column=3, row=16, sticky='N W')
        self.csv_batch_simulationlbl.grid(column=3, row=16, sticky='N W')
        self.csv_batch_simulation_entry.grid(column=3, row=17, sticky='N W')

        self.action_buttons_frame.grid(column=3, row=18, columnspan=2, pady=5)
        self.button_start.grid(column=3, row=18)
        self.button_reset.grid(column=4, row=18)

        # Make log frame dynamic
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Make log frame dynamic
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

    def check_num(self, P):
        return re.match('^[0-9]*$', P) is not None

        
    def start_real_time_simulation(self):
        """
        Function for start button to start simulation
        """
        try:
            no_of_passenger = int(self.number_of_passenger.get())
            no_of_floor = int(self.number_of_floor.get())
        except:
            print("Please enter number for number of passengers or number of floors")
            return

        try:
            csv_batch_number = int(self.csv_batch_simulation.get())
        except:
            csv_batch_number = 1

        passenger_mode = self.passenger_mode.get()
        passenger_preset = self.passenger_preset.get()
        elevator_algorithm = self.elevator_algorithm.get()
        simulator_mode = self.simulator_mode.get()
        csv_enabled = self.csv_output_enabled.get()
        csv_file_name = self.csv_file_name.get()
        match simulator_mode:
            case 'real':
                if not elevator_algorithm:
                    print("Please select elevator algorithm")
                    return
                if csv_enabled == 'True' and not csv_file_name:
                    print("Please enter CSV filename")
                    return
                Simulator.start_real_time_simulation(no_of_passenger, no_of_floor, elevator_algorithm, csv_enabled, csv_file_name, csv_batch_number)
            case 'static':
                if not elevator_algorithm:
                    print("Please select elevator algorithm")
                    return
                if not passenger_mode and passenger_mode != "preset":
                    print("Please select passenger mode")
                    return
                if passenger_mode == "preset" and not passenger_preset:
                    print("Please select preset")
                    return
                if csv_enabled == 'True' and not csv_file_name:
                    print("Please enter CSV filename")
                    return
                Simulator.start_static_simulation(passenger_mode, passenger_preset, no_of_passenger, no_of_floor, elevator_algorithm, csv_enabled, csv_file_name, csv_batch_number)
        self.csv_file_name_entry.delete(0,'end')
        self.csv_file_name_entry.insert(0, time.strftime("SimulationData-%Y%m%d-%H%M%S"))

    def reset_form(self):
        """
        Function to reset all widget on the interface
        """
        self.number_of_floor_entry.delete(0, 'end')
        self.number_of_passenger_entry.delete(0, 'end')
        self.passenger_mode.set('')
        self.simulator_mode.set('')
        self.elevator_algorithm.set('')
        self.passenger_preset.set('')



'''
window = Tk()

log_frame = ttk.Frame(window, borderwidth=5, relief="ridge", width=200, height=100)

log_widget = ScrolledText(log_frame, width=30, height=8, font=("consolas", "8", "normal"))
log_widget.configure(state='disabled')

option_frame = ttk.Frame(window, borderwidth=5, relief="ridge", width=200, height=100)
option_framelbl = ttk.Label(option_frame, text="Options")

simulator_option = ttk.Frame(option_frame)
simulator_mode = StringVar()
simulator_modelbl = ttk.Label(simulator_option, text="Simulation Mode")
real_time = ttk.Radiobutton(simulator_option, text='Real-time', variable=simulator_mode, value='real')
fixed_time = ttk.Radiobutton(simulator_option, text='Fixed-time', variable=simulator_mode, value='static')

passenger_options = ttk.Frame(option_frame)
passenger_mode = StringVar()
passenger_modelbl = ttk.Label(passenger_options, text="Passenger Mode")
random_passenger = ttk.Radiobutton(passenger_options, text='Random', variable=passenger_mode, value='random')
preset_passenger = ttk.Radiobutton(passenger_options, text='Preset', variable=passenger_mode, value='preset')

number_of_passenger_options = ttk.Frame(option_frame)
number_of_passenger = StringVar()
number_of_passengerlbl = ttk.Label(number_of_passenger_options, text="No. of Passengers: ")
number_of_passenger_entry = ttk.Entry(number_of_passenger_options, textvariable=number_of_passenger, width=6)

passenger_preset_options = ttk.Frame(option_frame)
passenger_preset = StringVar()
passenger_presetlbl = ttk.Label(passenger_preset_options, text="Select Preset")
passenger_preset_menu = ttk.Combobox(passenger_preset_options, textvariable=passenger_preset)
passenger_preset_menu['values'] = ('Morning Rush', 'Evening Rush', 'Distributed')

action_buttons_frame = ttk.Frame(option_frame)
button_start = ttk.Button(action_buttons_frame, text="Start")
button_cancel = ttk.Button(action_buttons_frame, text="Cancel")

summary_frame=ttk.Frame(window)

# Positioning frames and widgets
log_frame.grid(column=0, row=0, sticky='N S E W')
log_widget.grid(column=0, row=0, sticky='N S E W')
option_frame.grid(column=3, row=0, columnspan=2, rowspan=2, sticky='N S E W')
option_framelbl.grid(column=3, row=0, sticky='N W')
simulator_option.grid(column=3, row=1, columnspan=2, rowspan=2, sticky ='N S E W')
simulator_modelbl.grid(column=3, row=1, sticky='N W')
real_time.grid(column=3, row=2, sticky='N W')
fixed_time.grid(column=4, row=2, sticky='N W')
passenger_options.grid(column=3, row=3, columnspan=2, rowspan=2, sticky='N S E W')
passenger_modelbl.grid(column=3, row=3, sticky='N W')
random_passenger.grid(column=3, row=4, sticky='N W')
preset_passenger.grid(column=4, row=4, sticky='N W')
number_of_passenger_options.grid(column=3, row=5, columnspan=2, sticky='N W')
number_of_passengerlbl.grid(column=3, row=6, sticky='N W')
number_of_passenger_entry.grid(column=4, row=6, sticky='N W')
passenger_preset_options.grid(column=3, row=7, columnspan=2, rowspan=2, sticky='N W')
passenger_presetlbl.grid(column=3, row=7, sticky='N W')
passenger_preset_menu.grid(column=3, row=8, columnspan=2, sticky='N W')

action_buttons_frame.grid(column=3, row=9, columnspan=2, pady=5)
button_start.grid(column=3, row=9)
button_cancel.grid(column=4, row=9)

# Make log frame dynamic
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
# Make log frame dynamic
log_frame.columnconfigure(0,weight=1)
log_frame.rowconfigure(0, weight=1)

logger = PrintLogger(log_frame)
sys.stdout = logger
sys.stderr = logger
'''

app = GUI()
app.mainloop()
