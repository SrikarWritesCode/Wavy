import tkinter as tk
import numpy as np
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from Measurement00 import MeasurementController  # Adjust the import path as needed

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.measurement_controller = MeasurementController(record_seconds=5)
        self.style = ttk.Style(self.root)
        self.setup_ui()
        self.measurements_data = {}
        self.plot_lines = {}  # Key: measurement name, Value: line object


    def setup_ui(self):
        # Set the theme to 'alt' which is more modern
        self.style.theme_use('alt')

        # Configure the colors for the dark theme
        self.style.configure('TFrame', background='#333333')
        self.style.configure('TButton', background='#555555', foreground='white', borderwidth=1)
        self.style.configure('TLabel', background='#333333', foreground='white')
        self.style.configure('TNotebook', background='#333333', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#555555', foreground='white', padding=[5, 2], borderwidth=0)
        self.style.map('TButton', background=[('active', '#666666')])
        self.style.map('TNotebook.Tab', background=[('selected', '#333333')], expand=[('selected', [1, 1, 1, 0])])
        
        # Treeview (Checklist) style for dark theme
        self.style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
        self.style.configure("Treeview.Heading", background="#555555", foreground="white")
        self.style.map('Treeview', background=[('selected', '#666666')], foreground=[('selected', 'white')])

        # Customizing the Combobox dropdown list color
        self.root.option_add('*TCombobox*Listbox*Background', '#555555')
        self.root.option_add('*TCombobox*Listbox*Foreground', 'white')
        self.root.option_add('*TCombobox*Listbox*selectBackground', '#333333')
        self.root.option_add('*TCombobox*Listbox*selectForeground', 'white')

        # Create the tab control
        self.tab_control = ttk.Notebook(self.root)

        # Tab 1
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Tab 1')

        # Tab 2
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Tab 2')

        # Place the tab control
        self.tab_control.pack(expand=1, fill="both")

        # Configuring button callbacks
        self.button1 = ttk.Button(self.tab1, text="Start Measurement", command=self.start_measurement)
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Button 2 in Tab 1
        self.button2 = ttk.Button(self.tab1, text="Button2")
        self.button2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Dropdown menu in Tab 1
        self.dropdown = ttk.Combobox(self.tab1, values=["Option 1", "Option 2", "Option 3"])
        self.dropdown.grid(row=0, column=2, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Configure the column weights to allow resizing
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)
        for i in range(2, 6):
            self.tab1.grid_columnconfigure(i, weight=1)

        # Custom Treeview for list items with checkboxes
        # Custom Treeview for list items
        self.checklist = ttk.Treeview(self.tab1, columns=("item",), show="headings", height=10)
        self.checklist.heading("item", text="Measurements")
        self.checklist.column("item", width=200)
        
        # Dictionary to keep track of check states
        self.check_states = {}  # Key: item ID, Value: Boolean indicating checked state

        
        # Add checkboxes and items to the Treeview
        self.check_states = {}
        self.checklist.grid(row=1, column=0, columnspan=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.checklist.bind("<Button-1>", self.handle_check_click)

        # Frequency Plot
        # Setup for matplotlib figure embedded in Tkinter
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot1 = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.tab1)
        self.canvas.draw()
        
        # Embed the canvas widget in the GUI
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=1, columnspan=6, padx=10, pady=10, sticky="nsew")
        
        # Create a Frame for the toolbar
        self.toolbar_frame = tk.Frame(self.tab1)
        self.toolbar_frame.grid(row=1, column=1, columnspan=6, padx=10, pady=10, sticky="w")
        
        # Add the navigation toolbar within the new frame
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
    
        # Correct placement of the toolbar using grid
        self.toolbar.pack_configure(side=tk.TOP, fill=tk.X)  # Adjust toolbar packing
        
        # Plot 2 Placeholder in Tab 1
        # self.plot2_placeholder = tk.Label(self.tab1, text="Plot 2", relief="sunken", bg='#444444', fg='white')
        # self.plot2_placeholder.grid(row=3, column=1, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Configure the row and column weights of Tab 1 to allocate space
        self.tab1.grid_rowconfigure(1, weight=0)
        self.tab1.grid_rowconfigure(2, weight=5)
        # self.tab1.grid_rowconfigure(3, weight=5)

        # Configure button callbacks
        self.button1.config(command=self.start_measurement)
        self.button2.config(command=self.abort_measurement)

        # Configure dropdown callback
        self.dropdown.bind('<<ComboboxSelected>>', self.dropdown_selected)

    def start_measurement(self):
        print("Start measurement...")
        self.measurement_controller.record_audio()
        xf, yf = self.measurement_controller.perform_fft_and_plot()  # Get FFT data
        print(f"New data length: {len(xf)}, {len(yf)}")  # Debug print to check data
        measurement_count = len(self.measurements_data) + 1
        measurement_name = f"Measurement {measurement_count}"
        
        # Ensure the key (measurement_name) is unique for each measurement
        self.measurements_data[measurement_name] = (xf, yf)
        
        # Add to Treeview and store initial check state
        self.check_states[measurement_name] = True  # Assuming new measurements are checked by default
        self.checklist.insert('', 'end', iid=measurement_name, text="", values=(measurement_name,), tags=('checked',))
        print(f"Measurements stored: {list(self.measurements_data.keys())}")

        self.update_plot()
        
    def update_plot(self):
        self.plot1.clear()
        for measurement_name, (xf, yf) in self.measurements_data.items():
            if self.check_states.get(measurement_name, False):  # Check if this measurement is checked
                yf_db = 20 * np.log10(yf / np.max(yf))  # Convert yf to dB SPL
                self.plot1.semilogx(xf, yf_db, label=measurement_name)  # Plot checked measurements
                    
        self.plot1.set_xlabel('Frequency (Hz)')
        self.plot1.set_ylabel('Magnitude (dB SPL)')
        self.plot1.set_title('FFT Analysis')
        self.plot1.set_xlim(20, 20000)  # Set x-axis limits to 20Hz - 20,000Hz
        self.plot1.grid(True)  # Show grid
        self.plot1.legend()
        self.canvas.draw()
    def handle_check_click(self, event):
        item_id = self.checklist.identify_row(event.y)
        if item_id:  # Ensure a row is clicked
            self.toggle_check(item_id)
            self.update_plot()

    def toggle_check(self, item_id):
        # Toggle the check state for the item and update its display
        current_state = self.check_states.get(item_id, False)
        self.check_states[item_id] = not current_state
        # Update the Treeview item to reflect the new state, if needed

    def abort_measurement(self):
        # Placeholder for the abort_measurement functionality
        print("Abort measurement...")  # Example action

    def dropdown_selected(self, event):
        # Placeholder for the dropdown selected functionality
        print(f"Dropdown selected: {self.dropdown.get()}")  # Example action

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Waivy - Dark Mode")
    root.geometry("1920x10800")  # Adjust the size as needed

    # Changing the color of the main window to match the dark theme
    root.configure(bg='#333333')

    app = GUIManager(root)
    root.mainloop()
