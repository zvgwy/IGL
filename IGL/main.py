"""

Ideal Gas Law Calculator for Chemical Engineers * [Sacala, Pelegro]

This application allows users to calculate properties of an ideal gas (Pressure, Volume, Moles, Temperature) 
based on the Ideal Gas Law equation PV = nRT, where:
- P stands for pressure in atmospheres (atm)
- V stands for volume in liters (L)
- n stands for amount of substance in moles (mol)
- T stands for temperature in Kelvin (K)
- R is the gas constant, here taken as 0.0821 atm·L/(mol·K)

The user interface provides input fields for three properties and calculates the fourth one. It ensures
unit consistency by processing inputs with units and extracting numerical values for calculations.

Features:
- Hovertip on 'About Us' label to show additional information about the creators.
- Real-time entry validation and recalculations triggered by the 'Enter' key.
- Clear button to reset all fields and results.
- Use of Tkinter widgets and event handling for an interactive experience.

Instructions:
1. Choose the property you want to calculate using the dropdown menu.
2. Input the known values in their respective fields. Ensure to specify correct units.
3. Press 'Enter' or click 'Calculate' to compute the desired property.
4. Use 'Clear' to reset all inputs and the result.
5. Hover over 'About Us' to view more information.

-----Make sure to place an icon file named 'atom.png' in the same directory as this script for the icon setting function-----
-------------------------------
-------------------------------
Creators: 
    Sacala, Gabriel Jesz
    Pelegro, Gwyneth C.

Program: Chemical Engineering
Semester, School Year: 2nd Semester, 2023-2024 
Subject: ESM 2039
Code: 5-919
Instructor: Tabanguil, Johna Marie

"""

# main import statements
import os
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import PhotoImage
import re 

# about us hovertip
class Hovertip:
    def __init__(self, widget, text, delay=200):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.unschedule)

    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.showtip)

    def unschedule(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        self.hidetip()

    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

def update_fields(*args): # code below this line is to retain the previous choice if the user wants to calculate again 
    previous_choice = getattr(update_fields, 'previous_choice', None)
    current_choice = choice_var.get()

    if previous_choice != current_choice: # to clear everything if the user chooses to calculate a different property
        clear_fields()

    update_fields.previous_choice = current_choice  # set the current property as the previous property for the next calculation

    for entry in [pressure_entry, volume_entry, moles_entry, temperature_entry]: # to introduce input fields
        entry.config(state=tk.NORMAL)

    # disabling the input box of the chosen property na i calculate
    if current_choice == 'Pressure':
        pressure_entry.config(state=tk.DISABLED)
    elif current_choice == 'Volume':
        volume_entry.config(state=tk.DISABLED)
    elif current_choice == 'Moles':
        moles_entry.config(state=tk.DISABLED)
    elif current_choice == 'Temperature':
        temperature_entry.config(state=tk.DISABLED)

''' 

the whole point of this part below is to let the program know the 
acceptable units for each property so that 
even if the input is a string, it would still
accept the numbers as an integer

'''

def convert_input(input_string, measurement_type):
    unit_patterns = {
        'Pressure': r'\s*(atm|Atm|ATM)\s*$',
        'Volume': r'\s*(L|liters|l|Liters|LITERS)\s*$',
        'Moles': r'\s*(mol|Mol|moles|MOLES|MOL)\s*$',
        'Temperature': r'\s*(K|Kelvin|kelvin|k|KELVIN)\s*$'
    }
    pattern = unit_patterns.get(measurement_type, '')
    cleaned_input = re.sub(pattern, '', input_string.strip())
    return float(cleaned_input)

def calculate(): # for calculations
    try:
        pressure = volume = moles = temperature = None

        # conditionally get values from entries based on their state
        if pressure_entry.cget('state') != 'disabled':
            pressure = convert_input(pressure_entry.get(), 'Pressure')
        if volume_entry.cget('state') != 'disabled':
            volume = convert_input(volume_entry.get(), 'Volume')
        if moles_entry.cget('state') != 'disabled':
            moles = convert_input(moles_entry.get(), 'Moles')
        if temperature_entry.cget('state') != 'disabled':
            temperature = convert_input(temperature_entry.get(), 'Temperature')
        result_label.config(text="")

        # main calculation
        if choice_var.get() == 'Pressure' and None not in (volume, moles, temperature):
            result = (moles * 0.0821 * temperature) / volume
            pressure_entry.config(state=tk.NORMAL)
            pressure_entry.delete(0, tk.END)
            pressure_entry.insert(0, f"{result:.2f} atm")
            pressure_entry.config(state=tk.DISABLED)
        elif choice_var.get() == 'Volume' and None not in (pressure, moles, temperature):
            result = (moles * 0.0821 * temperature) / pressure
            volume_entry.config(state=tk.NORMAL)
            volume_entry.delete(0, tk.END)
            volume_entry.insert(0, f"{result:.2f} liters")
            volume_entry.config(state=tk.DISABLED)
        elif choice_var.get() == 'Moles' and None not in (pressure, volume, temperature):
            result = (pressure * volume) / (0.0821 * temperature)
            moles_entry.config(state=tk.NORMAL)
            moles_entry.delete(0, tk.END)
            moles_entry.insert(0, f"{result:.2f} moles")
            moles_entry.config(state=tk.DISABLED)
        elif choice_var.get() == 'Temperature' and None not in (pressure, volume, moles):
            result = (pressure * volume) / (moles * 0.0821)
            temperature_entry.config(state=tk.NORMAL)
            temperature_entry.delete(0, tk.END)
            temperature_entry.insert(0, f"{result:.2f} K")
            temperature_entry.config(state=tk.DISABLED)
        else:
            result_label.config(text="")

    except ValueError:
        result_label.config(text="Invalid/Missing input! Please enter valid values.") # error if the conversion of inputs fails
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def clear_fields(): # for the clearing sa everything
    for entry in [pressure_entry, volume_entry, moles_entry, temperature_entry]:
        state = entry.cget('state')
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.config(state=state)
    result_label.config(text="")

def set_icon(window): # atom icon
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(dir_path, 'atom.png')
        icon = PhotoImage(file=icon_path)
        window.tk.call('wm', 'iconphoto', window._w, icon)
    except Exception as e:
        print(f"Failed to load icon: {e}")

root = tk.Tk() # GUI
root.title("Ideal Gas Law Calculator")
set_icon(root)

choose_label = tk.Label(root, text="Choose what property to calculate:") # dropdown menu for the choosing of properties
choose_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
choice_var = tk.StringVar()
choices = ['Pressure', 'Volume', 'Moles', 'Temperature']
choice_menu = ttk.Combobox(root, textvariable=choice_var, values=choices, state="readonly", width=18)
choice_menu.grid(row=0, column=1, padx=10, pady=10)
choice_menu.current(0)


# forda entry stuff (input)
pressure_entry = tk.Entry(root, width=20)
volume_entry = tk.Entry(root, width=20)
moles_entry = tk.Entry(root, width=20)
temperature_entry = tk.Entry(root, width=20)

def on_enter_press(event): # to calculate every time 'enter' keyboard is used
    calculate()
pressure_entry.bind("<Return>", on_enter_press)
volume_entry.bind("<Return>", on_enter_press)
moles_entry.bind("<Return>", on_enter_press)
temperature_entry.bind("<Return>", on_enter_press)

# labels (sana all) and buttons stuff
labels = ["Pressure (atm):", "Volume (liters):", "Moles:", "Temperature (Kelvin):"]
for i, (label, entry) in enumerate(zip(labels, [pressure_entry, volume_entry, moles_entry, temperature_entry]), start=1):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=10)
    entry.grid(row=i, column=1, padx=10, pady=10)
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=5, column=0, padx=10, pady=10)
clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=5, column=1, padx=10, pady=10)
result_label = tk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
choice_menu.bind("<<ComboboxSelected>>", update_fields)
update_fields()

# about us hovertip
credits_font = tkFont.Font(family='Helvetica', size=8)
thanks_font = tkFont.Font(family='Helvetica', size=6, slant='italic')
more_info_label = tk.Label(root, text="About Us", fg="blue", cursor="hand2", font=credits_font)
more_info_label.grid(row=9, column=1, sticky='s', padx=10, pady=20)
tooltip_text = "Made by Gabriel Sacala and Gwyneth Pelegro for ESM 2039\nSpecial thanks to Stack Overflow forums ^-^"
hovertip = Hovertip(more_info_label, tooltip_text)

root.mainloop()