import sys
from tkinter import *
from tkinter import Tk, ttk
from tkinter.scrolledtext import ScrolledText

import Simulator as Simulator
from PrintLogger import PrintLogger

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.log_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=100)
        self.log_widget = ScrolledText(self.log_frame, width=30, height=8, font=("consolas", "8", "normal"))
        self.log_widget.configure(state='disabled')

        self.option_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=100)
        self.option_framelbl = ttk.Label(self.option_frame, text="Options")

        self.simulator_option = ttk.Frame(self.option_frame)
        self.simulator_mode = StringVar()
        self.simulator_modelbl = ttk.Label(self.simulator_option, text="Simulation Mode")
        self.real_time = ttk.Radiobutton(self.simulator_option, text='Real-time', variable=self.simulator_mode, value='real')
        self.fixed_time = ttk.Radiobutton(self.simulator_option, text='Fixed-time', variable=self.simulator_mode, value='static')

        self.passenger_options = ttk.Frame(self.option_frame)
        self. passenger_mode = StringVar()
        self.passenger_modelbl = ttk.Label(self.passenger_options, text="Passenger Mode")
        self.random_passenger = ttk.Radiobutton(self.passenger_options, text='Random', variable=self.passenger_mode, value='random')
        self.preset_passenger = ttk.Radiobutton(self.passenger_options, text='Preset', variable=self.passenger_mode, value='preset')

        self.number_of_passenger_options = ttk.Frame(self.option_frame)
        self.number_of_passenger = StringVar()
        self.number_of_passengerlbl = ttk.Label(self.number_of_passenger_options, text="No. of Passengers: ")
        self.number_of_passenger_entry = ttk.Entry(self.number_of_passenger_options, textvariable=self.number_of_passenger, width=6)

        self.number_of_floor_options = ttk.Frame(self.option_frame)
        self.number_of_floor = StringVar()
        self.number_of_floorlbl = ttk.Label(self.number_of_floor_options, text="No. of Floor: ")
        self.number_of_floor_entry = ttk.Entry(self.number_of_floor_options, textvariable=self.number_of_floor, width=6)

        self.passenger_preset_options = ttk.Frame(self.option_frame)
        self.passenger_preset = StringVar()
        self.passenger_presetlbl = ttk.Label(self.passenger_preset_options, text="Select Preset")
        self.passenger_preset_menu = ttk.Combobox(self.passenger_preset_options, textvariable=self.passenger_preset)
        self.passenger_preset_menu['values'] = ('Morning Rush', 'Evening Rush', 'Distributed')

        self.elevator_algorithm_options = ttk.Frame(self.option_frame)
        self.elevator_algorithm = StringVar()
        self.elevator_algorithmlbl = ttk.Label(self.elevator_algorithm_options, text="Select Elevator Algorithm")
        self.elevator_algorithm_menu = ttk.Combobox(self.elevator_algorithm_options, textvariable=self.elevator_algorithm)
        self.elevator_algorithm_menu['values'] = ('Proposed', 'Nearest-First')

        self.action_buttons_frame = ttk.Frame(self.option_frame)
        self.button_start = ttk.Button(self.action_buttons_frame, text="Start", command=self.start_real_time_simulation)
        self.button_cancel = ttk.Button(self.action_buttons_frame, text="Cancel")

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

        self.action_buttons_frame.grid(column=3, row=12, columnspan=2, pady=5)
        self.button_start.grid(column=3, row=12)
        self.button_cancel.grid(column=4, row=12)

        # Make log frame dynamic
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Make log frame dynamic
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger
        
    def start_real_time_simulation(self):
        no_of_passenger = int(self.number_of_passenger.get())
        no_of_floor = int(self.number_of_floor.get())
        elevator_algorithm = self.elevator_algorithm.get()
        Simulator.start_real_time_simulation(no_of_passenger, no_of_floor, elevator_algorithm)

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
