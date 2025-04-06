"""
AutoLEI Core Module

This module is a core component of the AutoLEI application, designed to facilitate the processing
and analysis of electron diffraction data using XDS and related tools. It provides a comprehensive
graphical user interface (GUI) built with Tkinter, enabling users to configure experiment parameters,
manage data processing workflows, perform data merging, handle clustering based on correlation
coefficients, refine unit cell parameters, and generate detailed reports. The module ensures
efficient and user-friendly interaction by leveraging multithreading to maintain GUI responsiveness
during long-running tasks.

Key Functionalities:
    1. **Input Configuration (`Input` Class):**
        - Browse and select working directories.
        - Load and manage instrument profiles.
        - Input and save experiment parameters necessary for XDS input file generation.

    2. **Batch Data Processing (`XDSRunner` Class):**
        - Convert various image formats (MRC, NXS, TIFF) to SMV format.
        - Generate and update XDS.INP files based on user-defined parameters.
        - Execute XDS processing in batch mode across multiple datasets.
        - Estimate symmetry and perform unit cell clustering.
        - Display and manage processing results through Excel integration.

    3. **Unit Cell Correction (`UnitCellCorr` Class):**
        - Input and manage space group numbers and unit cell parameters.
        - Save and apply unit cell information to all relevant XDS.INP files.
        - Rerun XDS processing with updated cell parameters for refined data reduction.

    4. **Data Merging (`MergeData` Class):**
        - Filter datasets based on statistical criteria such as I/Sigma, CC1/2, R_meas, and Resolution.
        - Merge selected datasets using XDS's XScale tool.
        - Display and manage merging results, including the generation of SHELX input files.

    5. **Cluster Management (`Cluster_Output` Class):**
        - Cluster datasets based on correlation coefficients extracted from XSCALE.LP files.
        - Set clustering distances either from dendrogram analysis or manual input.
        - Run XPREP for generating SHELX .ins files for crystallographic refinement.
        - Generate and view web-based reports summarizing cluster analyses.

    6. **Unit Cell Refinement (`XDSRefine` Class):**
        - Refine input parameters in XDS.INP files based on user-provided space group and unit cell information.
        - Manage and apply unit cell corrections across multiple datasets.
        - Facilitate the generation of updated XDS.INP files for accurate data reduction.
        - Integrate with clustering results to ensure consistency in refined parameters.

Dependencies:
    - **Standard Libraries:**
        - `os`, `sys`, `shutil`, `glob`, `json`, `subprocess`, `threading`
    - **Third-Party Libraries:**
        - `tkinter`: For building the graphical user interface.
        - `PIL (Pillow)`: For image processing and display.
        - `pandas`: For data manipulation and Excel file handling.
        - `openpyxl`: For reading and writing Excel files.
    - **Custom Modules (Within AutoLEI Core):**
        - `xds_input`: Handling XDS.INP file generation and modification.
        - `image_io`: Managing image format conversions and beam center calculations.
        - `xds_runner`: Orchestrating XDS batch processing workflows.
        - `xds_cluster`: Performing clustering based on data correlations.
        - `xds_shelx`: Converting merged data to SHELX format.
        - `xds_report`: Generating visual and web-based reports.
        - `util`: Providing utility functions and classes (e.g., tooltips, path handling).

Configuration:
    The module reads configuration settings from a `setting.ini` file located in the same directory.
    These settings include parameters for input filtering, paths to external applications like XPREP,
    and other general configurations that influence the module's behavior.

Usage:
    The module is structured as a series of Tkinter `Page` classes, each representing a different
    section of the AutoLEI GUI. Users interact with these pages to perform various tasks related
    to data processing, parameter configuration, and result analysis. The application ensures
    that all operations are executed in separate threads to maintain a responsive user interface.

Contact:
    - Lei Wang: lei.wang@mmk.su.se
    - Yinlin Chen: yinlin.chen@mmk.su.se

License:
    BSD 3-Clause License
"""

import configparser

try:
    from .src import xds_input, image_io, xds_analysis, xds_runner, xds_cluster, xds_shelx, xds_report
    from .src.util import *
except ImportError:
    from src import xds_input, image_io, xds_analysis, xds_runner, xds_cluster, xds_shelx, xds_report
    from src.util import *

from functools import partial
import glob
from tkinter import filedialog, font, Toplevel, Label, messagebox
from PIL import Image, ImageTk
import pandas as pd
import json
from numpy import cos, radians, arccos

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, 'setting.ini'))


analysis_engine = config["XDSRunner"]["engine_hkl_analysis"]
path_filter = strtobool(config["General"]["path_filter"])

is_wsl = is_wsl()


class Input(Page):
    """Class Input

    Represents the input page for setting experiment parameters.

    Methods:
        __init__(parent): Initializes the input page and sets up the GUI components.
        set_ui(sp): Creates and arranges all GUI widgets for parameter input.
        select_path(): Opens a directory browser to select the working directory.
        load_path(): Loads and analyzes the chosen path, updates parameters and dataset count.
        load_instrument_profile(): Loads available instrument profiles from a predefined directory.
        handle_option_select(event): Handles instrument profile selection; if 'Browse...' is chosen, prompts file dialog.
        load_instrument_parameter(): Loads parameters from the selected instrument file into the UI.
        update_parameter(parameter_dict): Updates GUI fields based on extracted parameters.
        save_and_run(): Saves all input parameters into 'Input_parameters.txt' and sets them as active.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the Input GUI frame with all widgets and configurations.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this Input page will be placed.
        """
        Page.__init__(self, parent)
        self.sf = self.master.master.sf
        sp = 6 * self.sf ** 2.5
        self.set_ui(sp)

    def set_ui(self, sp: float) -> None:
        """
        Create and arrange all GUI widgets for parameter input.

        Args:
            sp (float): A spacing factor used to adjust padding and widget sizes based on scaling.
        """
        # Instruction message
        instruction_frame = tk.Frame(self, bg='white')
        instruction_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=2 * sp, columnspan=4)
        instruction_msg = ("Browse and load the work path where the program will load the measurement settings.\n"
                           "For XDS input generation, supply basic parameters and click the 'Save Parameter' button.")

        label = tk.Label(instruction_frame, text=instruction_msg, bg='white', wraplength=1100)
        label.pack(side="left", fill="both", expand=True)

        self.input_fields = {}

        # Row 1: Input path And Select Instrument Parameters
        row1_frame = tk.Frame(self, bg='white')
        row1_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=2 * sp)
        tk.Label(row1_frame, text="Input path:", bg='white').grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.path_entry = tk.Entry(row1_frame, width=30)
        self.path_entry.grid(row=0, column=1, sticky="w", padx=(0, 10))
        ToolTip(self.path_entry, "Path in linux format.")

        browse_button = tk.Button(row1_frame, text="Browse", command=self.select_path)
        browse_button.grid(row=0, column=2, sticky="w", padx=(5, 5))  # Add padding between entry and button
        ToolTip(browse_button, "Browse the working folder.")

        load_path_button = tk.Button(row1_frame, text="Load Path", command=self.load_path)
        load_path_button.grid(row=0, column=3, sticky="w", padx=(5, 5))
        ToolTip(load_path_button, "Load the working folder.")

        # Dropdown list next to the Browse button with dynamic action for "Browse..."
        tk.Label(row1_frame, text="Instrument File:", bg='white').grid(row=0, column=4, sticky="w", padx=(15, 5))
        self.option_var = tk.StringVar(self)
        self.option_var.set('Custom')  # default value
        self.path_dict = self.load_instrument_profile()
        options = ["Custom"] + list(self.path_dict.keys()) + ["Browse..."]
        self.option_menu = ttk.Combobox(row1_frame, textvariable=self.option_var, values=options, state='readonly',
                                        width=25)
        self.option_menu.grid(row=0, column=5, padx=(5, 10), sticky="w")
        self.option_menu.bind('<<ComboboxSelected>>', self.handle_option_select)
        # Button to perform action based on selected option
        load_instrument_button = tk.Button(row1_frame, text="Load", command=self.load_instrument_parameter)
        load_instrument_button.grid(row=0, column=6, padx=(5, 10), sticky="w")
        ToolTip(self.option_menu, "Select from default profiles. \n\"Browse...\" can load the XDS.INP as model.")
        ToolTip(load_instrument_button, "Load the instrument profile.")

        self.columnconfigure(1, weight=1)  # Make the entry widget expandable

        # Instrument label
        row2_frame = tk.Frame(self, bg='white')
        row2_frame.grid(row=2, column=0, sticky="w", padx=10, pady=2 * sp, columnspan=4)
        instrument_label = "I. Instrument Parameters"
        tk.Label(row2_frame, text=instrument_label, bg='white', font=("Liberation Sans", int(17 * self.sf), "bold"),
                 wraplength=1000).pack(side="left")

        # Row 3: NX, NY, QX, QY
        row3_frame = tk.Frame(self, bg='white')
        row3_frame.grid(row=3, column=0, sticky="w", padx=10, pady=sp)
        tk.Label(row3_frame, text="1. Detector parameters:     ", bg='white'
                 ).grid(row=0, column=0, sticky="w", padx=(10, 2))
        labels_row3 = ["NX=", "NY=", "QX=", "QY="]
        for i, label in enumerate(labels_row3):
            tk.Label(row3_frame, text=label, bg='white').grid(row=0, column=i * 2 + 1, sticky="w", padx=2)
            entry = tk.Entry(row3_frame, bg='white', width=8)
            entry.grid(row=0, column=i * 2 + 2, sticky="w", padx=10)
            self.input_fields[label] = entry

        # Row 4: OVERLOAD and WAVELENGTH
        row4_frame = tk.Frame(self, bg='white')
        row4_frame.grid(row=4, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row4_frame, text="2. Overloading:     OVERLOAD= ", bg='white').grid(row=0, column=0, sticky="w",
                                                                                     padx=(10, 2))
        self.input_fields["OVERLOAD="] = tk.Entry(row4_frame, bg='white', width=10)
        self.input_fields["OVERLOAD="].grid(row=0, column=1, sticky="w", padx=(10, 10))
        tk.Label(row4_frame, text="\t  3. Wavelength:    WAVELENGTH=", bg='white').grid(row=0, column=2, sticky="w",
                                                                                        padx=(45, 2))
        self.input_fields["X-RAY_WAVELENGTH="] = tk.Entry(row4_frame, bg='white', width=10)
        self.input_fields["X-RAY_WAVELENGTH="].grid(row=0, column=3, sticky="w", padx=(10, 2))
        tk.Label(row4_frame, text=" Å", bg='white').grid(row=0, column=4, sticky="w", padx=2)

        # Row 5: ROTATION_AXIS
        row5_frame = tk.Frame(self, bg='white')
        row5_frame.grid(row=5, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row5_frame, text="4. Rotation axis:    ROTATION_AXIS=", bg='white').grid(row=0, column=0, sticky="w",
                                                                                          padx=(10, 10))
        self.input_fields["ROTATION_AXIS="] = tk.Entry(row5_frame, bg='white')
        self.input_fields["ROTATION_AXIS="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row5_frame, text="    >>> Use space to segment  OR  Angle in Degree = ",
                 bg='white').grid(row=0, column=2, sticky="w", padx=2)
        self.input_fields["ROTATION_ANGLE"] = tk.Entry(row5_frame, bg='white', width=7)
        self.input_fields["ROTATION_ANGLE"].grid(row=0, column=3, sticky="w", padx=2)

        # Row 6: Beamstop Information and untrusted area
        row6_frame = tk.Frame(self, bg='white')
        row6_frame.grid(row=6, column=0, sticky="ew", padx=(5, 2), pady=2 * sp, columnspan=4)
        tk.Label(row6_frame, text="5. Additional information\n   (Please copy from XDS):    ", bg='white').pack(
            side="left")
        self.input_fields["Additional_Info"] = tk.Text(row6_frame, height=5, width=90, bg='white')
        self.input_fields["Additional_Info"].pack(side="left")

        # Measurement label
        row7_frame = tk.Frame(self, bg='white')
        row7_frame.grid(row=7, column=0, sticky="w", padx=10, pady=2 * sp)
        instrument_label = "II. Measurement Parameters"
        tk.Label(row7_frame, text=instrument_label, bg='white', font=("Liberation Sans", int(17 * self.sf), "bold"),
                 wraplength=1000).pack(side="left")

        # Row 8: ORGX, ORGY
        row8_frame = tk.Frame(self, bg='white')
        row8_frame.grid(row=8, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row8_frame, text="6. Direct beam position:    ORGX=", bg='white').grid(row=0, column=0, sticky="w",
                                                                                        padx=(10, 2))
        self.input_fields["ORGX="] = tk.Entry(row8_frame, bg='white', width=10)
        self.input_fields["ORGX="].grid(row=0, column=1, sticky="w", padx=(10, 2))
        tk.Label(row8_frame, text="ORGY=", bg='white').grid(row=0, column=2, sticky="w", padx=(20, 2))
        self.input_fields["ORGY="] = tk.Entry(row8_frame, bg='white', width=10)
        self.input_fields["ORGY="].grid(row=0, column=3, sticky="w", padx=(10, 2))

        # Row 9: INCLUDE_RESOLUTION_RANGE
        row9_frame = tk.Frame(self, bg='white')
        row9_frame.grid(row=9, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row9_frame, text="7. Resolution range:    INCLUDE_RESOLUTION_RANGE=    ",
                 bg='white').grid(row=0, column=0, sticky="w", padx=(10, 2))
        self.input_fields["INCLUDE_RESOLUTION_RANGE="] = tk.Entry(row9_frame, bg='white', width=15)
        self.input_fields["INCLUDE_RESOLUTION_RANGE="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row9_frame, text="    >>> Use space to segment", bg='white').grid(row=0, column=2, sticky="w",
                                                                                   padx=2)

        # Row 10: DETECTOR_DISTANCE And OSCILLATION ANGLE
        row10_frame = tk.Frame(self, bg='white')
        row10_frame.grid(row=10, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row10_frame, text="8. Camera Length:    DETECTOR_DISTANCE=",
                 bg='white').grid(row=0, column=0, sticky="w", padx=(10, 2))
        self.input_fields["DETECTOR_DISTANCE="] = tk.Entry(row10_frame, bg='white', width=10)
        self.input_fields["DETECTOR_DISTANCE="].grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(row10_frame, text="\t9. Rotation step:    OSCILLATION_RANGE=",
                 bg='white').grid(row=0, column=2, sticky="w", padx=2)
        self.input_fields["OSCILLATION_RANGE="] = tk.Entry(row10_frame, bg='white', width=10)
        self.input_fields["OSCILLATION_RANGE="].grid(row=0, column=3, sticky="w", padx=2)

        # Row 12: Save and Run button
        row12_frame = tk.Frame(self, bg='white')
        row12_frame.grid(row=12, column=0, sticky="w", padx=10, pady=2 * sp)
        save_input_button = tk.Button(row12_frame, text="Save Parameters", command=self.save_and_run)
        save_input_button.pack(side="left")

        ToolTip(self.input_fields["NX="], "Pixel number over x-axis.")
        ToolTip(self.input_fields["NY="], "Pixel number over y-axis.")
        ToolTip(self.input_fields["QX="], "Pixel size on x-axis in mm.")
        ToolTip(self.input_fields["QY="], "Pixel size on y-axis in mm.")
        ToolTip(self.input_fields["OVERLOAD="], "SMV image will have a highest intensity of 65535.")
        ToolTip(self.input_fields["X-RAY_WAVELENGTH="], "120 kV, 0.03349 Å; \n200 kV, 0.02508 Å; \n300 kV, 0.01969 Å.")
        ToolTip(self.input_fields["ROTATION_AXIS="], "Should leave blank if entering rotation angle.")
        ToolTip(self.input_fields["ROTATION_ANGLE"], "Rotation angle in degrees from x+.")
        ToolTip(self.input_fields["Additional_Info"], "Information on untrusted area and keywords for data reduction."
                                                      "\nCaution! Please ensure the keyword are legal in XDS.")
        ToolTip(self.input_fields["ORGX="], "X of the origin point, can be calculated later.")
        ToolTip(self.input_fields["ORGY="], "Y of the origin point, can be calculated later.")
        ToolTip(self.input_fields["INCLUDE_RESOLUTION_RANGE="], "The resolution range of the data reduction.")
        ToolTip(self.input_fields["DETECTOR_DISTANCE="],
                "Camera length in TEM, can be corrected later by image header.")
        ToolTip(self.input_fields["OSCILLATION_RANGE="],
                "Angle between frames, \ncan be corrected later by image header.")
        ToolTip(save_input_button, "All parameter will be saved in \"Input_parameters.txt\".")

    def select_path(self) -> None:
        """
        Open a directory browser for selecting the working directory and update the path_entry widget.
        """
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def load_path(self) -> None:
        """
        Load and analyze the chosen path, updates parameters and dataset counts.
        Displays a message box on success or if path contains spaces.
        """
        input_path = self.path_entry.get()
        if input_path:
            if " " in input_path:
                messagebox.showinfo("Info", f"Path contains space inside. Some functionality may not work.")
            if ("!" in input_path or "/." in input_path) and path_filter:
                messagebox.showinfo("Info", f"The Path contains \"!\" inside or with \".\" started. "
                                            f"Some functionality may not work.")
            parameter_dict, datasets_number = xds_analysis.analysis_folder(input_path)
            self.update_parameter(parameter_dict)
            main_app = self.master.master
            main_app.dataset_counts = datasets_number
            main_app.set_input_path(input_path)
            print(f"The Path is set to {input_path}\n")
            messagebox.showinfo("Info", f"The Path is set to {input_path}")

    @classmethod
    def load_instrument_profile(cls) -> dict:
        """
        Load available instrument profiles from a predefined directory.

        Returns:
            dict: A dictionary mapping profile names to their file paths.
        """
        _path_dict = {}
        _file_path = os.path.join(script_dir, "instrument_profile")
        _files_list = sorted([f for f in os.listdir(_file_path) if os.path.isfile(os.path.join(_file_path, f))])
        for f in _files_list:
            if f != "__init__.py":
                _path_dict[f] = os.path.join(_file_path, f)
        return _path_dict

    def handle_option_select(self, event: tk.Event) -> None:
        """
        Handle the selection of instrument profile option.
        If 'Browse...' is chosen, prompt the user to select a custom profile file.

        Args:
            event (object): The Tkinter event object.
        """
        if self.option_var.get() == 'Browse...':
            _file_path = filedialog.askopenfilename(
                defaultextension="INP", filetypes=[("XDS.INP", "*.INP"), ("All", "*")],
                title="Select XDS.INP as model",
            )
            if _file_path:
                _file_name = os.path.basename(_file_path)
                self.path_dict[_file_name] = _file_path
                self.option_var.set(_file_name)
            else:
                self.option_var.set("Custom")

    def load_instrument_parameter(self) -> None:
        """
        Load parameters from the selected instrument file into the GUI fields.
        """
        selected_option = self.option_var.get()
        if selected_option in ["Custom", "Browse..."]:
            return
        print(f"Reading Instrument Parameter: {selected_option}\n")
        file_path = self.path_dict[selected_option]
        if selected_option.endswith(".INP") or selected_option.endswith(".txt") or selected_option.startswith("BACKUP"):
            with open(file_path, "r", errors="ignore") as file:
                self.update_parameter(xds_input.extract_keywords(file.readlines()))
        else:
            try:
                with open(file_path, "r") as file:
                    parameters = json.load(file)
                    replace_entry(self.input_fields["NX="], parameters["NX"])
                    replace_entry(self.input_fields["NY="], parameters["NY"])
                    replace_entry(self.input_fields["QX="], parameters["QX"])
                    replace_entry(self.input_fields["QY="], parameters["QY"])
                    replace_entry(self.input_fields["OVERLOAD="], parameters["overload"])
                    replace_entry(self.input_fields["ROTATION_ANGLE"], parameters["rotation_axis"])
                    replace_entry(self.input_fields["ROTATION_AXIS="],
                                  "{:.4f} {:.4f} 0".format(cos(radians(parameters["rotation_axis"])),
                                                           cos(radians(parameters["rotation_axis"] + 90))))
                    self.input_fields["X-RAY_WAVELENGTH="].delete(0, tk.END)
                    replace_entry(self.input_fields['ORGX='], "{}".format(int(int(parameters["NX"]) / 2)))
                    replace_entry(self.input_fields['ORGY='], "{}".format(int(int(parameters["NY"]) / 2)))
                    if "wavelength" in parameters:
                        self.input_fields["X-RAY_WAVELENGTH="].insert(0, parameters["wavelength"])
                    else:
                        if parameters["energy"] == 200:
                            self.input_fields["X-RAY_WAVELENGTH="].insert(0, "0.02508")
                        elif parameters["energy"] == 300:
                            self.input_fields["X-RAY_WAVELENGTH="].insert(0, "0.01968")
                    replace_text(self.input_fields["Additional_Info"], "\n".join(parameters["addition information"]))
                    replace_entry(self.input_fields["INCLUDE_RESOLUTION_RANGE="], "30 0.8")
            except FileNotFoundError:
                messagebox.showerror("Error", "The instrument file does not exist.")

    def update_parameter(self, parameter_dict: dict) -> None:
        """
        Update GUI fields based on extracted parameters from a dictionary.

        Args:
            parameter_dict (dict): A dictionary of XDS parameters.
        """
        showing_parameters = ['NX=', 'NY=', 'QX=', 'QY=', 'OVERLOAD=', 'INCLUDE_RESOLUTION_RANGE=', 'ORGX=', 'ORGY=',
                              'DETECTOR_DISTANCE=', 'OSCILLATION_RANGE=', 'ROTATION_AXIS=', 'X-RAY_WAVELENGTH=']
        for key in showing_parameters:
            if key[:-1] in parameter_dict and parameter_dict[key[:-1]]:
                replace_entry(self.input_fields[key], "{}".format(parameter_dict[key[:-1]][0]))
            else:
                replace_entry(self.input_fields[key], " ")
        if 'ROTATION_AXIS' in parameter_dict and parameter_dict["ROTATION_AXIS"]:
            cos_rot = float(parameter_dict["ROTATION_AXIS"][0].split()[0])
            replace_entry(self.input_fields["ROTATION_ANGLE"], "-{:.2f}".format(arccos(cos_rot) * 57.296))
        additional_parameters = ["UNTRUSTED_RECTANGLE", "UNTRUSTED_ELLIPSE",
                                 "UNTRUSTED_QUADRILATERAL", "EXCLUDE_RESOLUTION_RANGE",
                                 "DELPHI", "SIGNAL_PIXEL", ]
        additional_lines = []
        for key in additional_parameters:
            if key in parameter_dict:
                if isinstance(parameter_dict[key], list):
                    for item in parameter_dict[key]:
                        additional_lines.append("{}= {}".format(key, item))
                else:
                    additional_lines.append("{}= {}".format(key, parameter_dict[key]))
        replace_text(self.input_fields["Additional_Info"], "\n".join(additional_lines))

    def save_and_run(self) -> None:
        """
        Save all input parameters into 'Input_parameters.txt' and set them as active parameters.
        Displays message boxes on success and warnings if values are missing.
        """
        input_values = {}
        if self.input_fields["ROTATION_ANGLE"].get().strip() and not self.input_fields["ROTATION_AXIS="].get().strip():
            rot_angle = float(self.input_fields["ROTATION_ANGLE"].get())
            replace_entry(self.input_fields["ROTATION_AXIS="],
                          "{:.4f} {:.4f} 0".format(cos(radians(rot_angle)), cos(radians(rot_angle + 90))))
        for label, field in self.input_fields.items():
            if isinstance(field, tk.Text):
                input_values[label] = field.get("1.0", "end-1c")  # For Text widgets
            else:
                input_values[label] = field.get()  # For Entry widgets
        input_path = self.path_entry.get()

        if not input_path:
            print("Input path is not set. Please set the input path first.")
            return

        empty_list = []
        for entry, value in input_values.items():
            if value is None or not value.strip() and "=" in entry:
                empty_list.append(entry)

        if empty_list:
            messagebox.showinfo("Caution", f"Input File Saved. \nHowever, {', '.join(empty_list)} is missing.")

        # Determine the directory to save the formatted parameters file
        output_file_path = os.path.join(input_path, "Input_parameters.txt") if input_path else "Input_parameters.txt"

        # Write input values to a file in the new format
        with open(output_file_path, "w") as file:
            file.write("###Uniform Experiment Settings###\n")

            # Writing reformatted parameters
            file.write(
                f"1. Pixel information for your camera:\n NX= {input_values.get('NX=')}   NY= {input_values.get('NY=')}"
                f"  QX= {input_values.get('QX=')}  QY= {input_values.get('QY=')}  !Number and Size (mm) of pixel\n\n")
            file.write(
                f"2. Overload range for your camera:\n "
                f"OVERLOAD= {input_values.get('OVERLOAD=')}   "
                f"!default value dependent on the detector used\n\n")
            file.write(
                f"3. Resolution range for the 1st round:\n "
                f"INCLUDE_RESOLUTION_RANGE=   {input_values.get('INCLUDE_RESOLUTION_RANGE=')}\n\n")
            file.write(
                f"4. Direct beam position\n "
                f"ORGX= {input_values.get('ORGX=')}  ORGY=  {input_values.get('ORGY=')}\n\n")
            file.write(
                f"5. Camera length\n "
                f"DETECTOR_DISTANCE=  {input_values.get('DETECTOR_DISTANCE=')}\n\n")
            file.write(
                f"6. Oscillation range, degree per frame:\n "
                f"OSCILLATION_RANGE={input_values.get('OSCILLATION_RANGE=')}\n\n")
            file.write(
                f"7. Rotation axis, depending on microscope:\n ROTATION_AXIS= {input_values.get('ROTATION_AXIS=')}  "
                f"!cos(rotation_axis) cos(axis-90)  !in XDS.INP\n\n")
            file.write(
                f"8. Wavelength, Å (200 keV 0.02508, 300 keV 0.01968):\n "
                f"X-RAY_WAVELENGTH=  {input_values.get('X-RAY_WAVELENGTH=')}     "
                f"!used by IDXREF\n\n")

            # Writing beamstop information if present
            beamstop_info = input_values.get("Additional_Info")
            if beamstop_info.strip():
                file.write("###Additional Keywords###\n")
                file.write(beamstop_info)
                file.write("\n###Additional Keywords###\n")

        main_app = self.master.master
        main_app.set_input_path(input_path)
        messagebox.showinfo("Info", f"Parameters written to {output_file_path}\n")


class XDSRunner(Page):
    """Class XDSRunner
    Manages batch processing of XDS from the GUI.

    Methods:
        __init__(parent): Initializes the XDSRunner page and sets up GUI elements.
        on_select(): Handles format selection changes for image conversion.
        run_mrc_to_img(): Starts MRC-to-IMG conversion in a separate thread.
        run_nxs_to_img(): Starts NXS-to-IMG conversion to SMV.
        run_tiff_to_img(): Starts TIFF-to-IMG conversion.
        run_xds_writer(): Writes XDS.INP files for the converted images.
        self_beam_center(): Finds the beam center without beam stop.
        self_beam_stop(): Finds the beam center with beam stop.
        run_xdsrunner(): Initiates XDS batch processing in a separate thread.
        stop_xdsrunner(): Stops the ongoing XDS batch process.
        show_results(): Displays results from xdsrunner.xlsx in a Treeview widget.
        update_excel(): Updates result files.
        open_xdsrunner_excel(): Opens the xdsrunner.xlsx or xdsrunner2.xlsx file in LibreOffice or Explorer.
        display_excel_data(file_path): Displays an Excel file's content in a Treeview.
        auto_adjust_columns(tree, df, sf): Automatically adjusts column widths in the Treeview.
        conversion_animation(): Animates the MRC-to-IMG conversion process.
        stop_mrc_to_img_animation(): Stops the MRC-to-IMG animation.
        xdsrunner_animate(): Animates the XDS runner process.
        stop_xdsrunner_animation(): Stops the XDS runner animation.
        correct_input(): Corrects input parameters from image metadata.
        on_beam_stop_checkbox_change(): Updates the UI when beam stop usage is toggled.
        estimate_symmetry(): Estimates symmetry and cell clustering with a new thread.
        confirm_delete_xds(): Prompts user to confirm deletion of XDS files.
        run_delete_xds_script(): Runs the script to delete all XDS files.
        instamatic_inp_update(): Updates XDS.INP files for instamatic users.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the XDSRunner GUI frame and set up widgets for batch XDS processing.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this XDSRunner page will be placed.
        """
        Page.__init__(self, parent)
        self.sf = self.master.master.sf
        self.input_path = ""
        sp = 5 * self.sf ** 2.5
        self.set_ui(sp)

    def set_ui(self, sp: float) -> None:
        """
        Create and arrange all GUI widgets for parameter input.

        Args:
            sp (float): A spacing factor used to adjust padding and widget sizes based on scaling.
        """
        # Row 1: Description text
        description = tk.Label(self,
                               text="XDSrunner aims to perform batch data processing with XDS.",
                               bg='white')
        description.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(3 * sp, sp))

        # Row 2: Format transfer label
        tk.Label(self, text="1. Select Format and Convert to SMV", bg='white').grid(row=2, column=0, sticky="w", padx=10,
                                                                                   pady=sp)

        # Row 3: Format transfer button and animation
        img_transfer_frame = tk.Frame(self, bg='white')
        img_transfer_frame.grid(row=3, column=0, sticky="w", padx=10, pady=sp)
        self.selected_format_option = tk.IntVar(value=1)

        # Create Radiobuttons and place them in a horizontal line using grid
        self.format_options = ["SMV", "MRC", "TIFF", "NXS"]
        radiobutton = {}
        for index, format_option in enumerate(self.format_options):
            radiobutton[format_option] = tk.Radiobutton(img_transfer_frame, text=format_option,
                                                        variable=self.selected_format_option,
                                                        value=index + 1, command=self.on_select, bg="white")
            radiobutton[format_option].pack(side="left", padx=(25, 5))
        ToolTip(radiobutton["SMV"], "The default image format in AutoLEI.")
        ToolTip(radiobutton["MRC"], "FEI non-stacked MRC.")
        ToolTip(radiobutton["TIFF"], "Any TIFF supported by XDS.")
        ToolTip(radiobutton["NXS"], "DLS NXS with metadata.")
        self.mrc_button = tk.Button(img_transfer_frame, text="MRC to IMG", command=self.run_mrc_to_img)
        self.tiff_button = tk.Button(img_transfer_frame, text="TIFF to IMG", command=self.run_tiff_to_img)
        self.nxs_button = tk.Button(img_transfer_frame, text="NXS to IMG", command=self.run_nxs_to_img)
        ToolTip(self.mrc_button, "Convert FEI non-stack MRC to SMV .IMG")
        ToolTip(self.tiff_button, "Convert TIFF to SMV .IMG, metadata might be needed.")
        ToolTip(self.nxs_button, "Convert DLS NXS H5 to SMV .IMG")
        self.animation_canvas = tk.Canvas(img_transfer_frame, width=125, height=20, bg='white', highlightthickness=0)
        self.mrc_to_img_animation_active = False
        self.mrc_to_img_animation_angle = 0

        self.instamatic_button = tk.Button(img_transfer_frame, text="Update Instamatic XDS.INP",
                                           command=self.instamatic_inp_update)
        self.instamatic_button.pack(side="left", padx=25)
        ToolTip(self.instamatic_button, "Add / remove some keywords on XDS.INP from Instamatic.")
        self.is_beam_stop = tk.BooleanVar(value=False)
        self.is_beam_stop_checkbox = tk.Checkbutton(img_transfer_frame, variable=self.is_beam_stop,
                                                    command=self.on_beam_stop_checkbox_change,
                                                    bg='white')
        self.is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
        self.is_beam_stop_checkbox_label = tk.Label(img_transfer_frame, text="Beam Stop Used", bg='white')
        self.is_beam_stop_checkbox_label.pack(side="left")
        ToolTip(self.is_beam_stop_checkbox, "Tick it if beam stop has been used in the measurement.")

        # Row 4: XDSINP batch writing label
        tk.Label(self, text="2. Create and Update XDS.INP",
                 bg='white').grid(row=4, column=0, sticky="w", padx=10, pady=sp)

        # Row 5: XDSINP batch writing buttons
        self.buttons_frame_row_5 = tk.Frame(self, bg='white')
        self.buttons_frame_row_5.grid(row=5, column=0, sticky="w", padx=25, pady=sp)
        generate_xds_button = tk.Button(self.buttons_frame_row_5, text="Generate XDS.INP", command=self.run_xds_writer)
        generate_xds_button.grid(row=5, column=1, sticky="w", padx=(10, 25), pady=sp)
        ToolTip(generate_xds_button, "Generate XDS.INP for converted images. \n"
                                     "Will skip images with XDS.INP already linked.")
        self.beam_centre_button = tk.Button(self.buttons_frame_row_5, text="Find Beam Center",
                                            command=self.self_beam_center)
        self.beam_centre_button.grid(row=5, column=2, sticky="w", padx=25, pady=sp)
        ToolTip(self.beam_centre_button, "Find the origin point of the beam w/o beam stop.")
        correct_metadata_button = tk.Button(self.buttons_frame_row_5, text="Correct Input with Metadata",
                                            command=self.correct_input)
        correct_metadata_button.grid(row=5, column=3, sticky="w", padx=25, pady=sp)
        # tk.Label(self.buttons_frame_row_5, text="|", bg='white').grid(row=5, column=4, sticky="w", padx=(100, 10),
        #                                                               pady=sp)
        # delete_xds_button = tk.Button(self.buttons_frame_row_5, text="Delete XDS", command=self.confirm_delete_xds,
        #                               bg="#f3e3e3")
        # delete_xds_button.grid(row=5, column=5, sticky="w", padx=25, pady=sp)
        ToolTip(correct_metadata_button, "Correct input with image header on camera length.\n"
                                         "oscillation angle, pixel number/size.")
        # ToolTip(delete_xds_button, "CAUTION! It will delete all XDS.INP with corresponding result files!")
        self.sp = sp

        # Row 6: Run XDS in all folders label
        tk.Label(self, text="3. Process Data under P1 mode and Estimate Symmetry.",
                 bg='white').grid(row=6, column=0, sticky="w", padx=10, pady=sp)

        # Row 7: Run XDS in all folders buttons and animation
        buttons_frame_row_7 = tk.Frame(self, bg='white')
        buttons_frame_row_7.grid(row=7, column=0, sticky="w", padx=10, pady=sp)
        run_xds_button = tk.Button(buttons_frame_row_7, text="Run XDS", command=self.run_xdsrunner)
        run_xds_button.pack(side="left", padx=25)
        ToolTip(run_xds_button, "Run XDS batchly under work directory.")
        stop_run_xds_button = tk.Button(buttons_frame_row_7, text="Stop Run", command=self.stop_xdsrunner)
        stop_run_xds_button.pack(side="left", padx=25)
        ToolTip(stop_run_xds_button, "Stop the processing after current XDS run.")
        self.xdsrunner_animation_canvas = tk.Canvas(buttons_frame_row_7, width=150,
                                                    height=20, bg='white', highlightthickness=0)
        self.xdsrunner_animation_canvas.pack(side="left", padx=10)
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_angle = 0
        estimate_symmetry_button = tk.Button(buttons_frame_row_7, text="Estimate Symmetry & Cell-Cluster",
                                             command=self.estimate_symmetry)
        estimate_symmetry_button.pack(side="left", padx=25)
        ToolTip(estimate_symmetry_button, "Estimate symmetry and do the unit cell clustering."
                                          "\nThe clustering information is stored in \"lattice_cluster.txt\"")

        # Row 8: Show all information label
        tk.Label(self, text="4. View Running Result", bg='white').grid(row=8, column=0, sticky="w", padx=10, pady=sp)

        # Row 9: Show all information buttons
        buttons_frame_row_9 = tk.Frame(self, bg='white')
        buttons_frame_row_9.grid(row=9, column=0, sticky="w", padx=10, pady=(sp, 3 * sp))
        show_result_button = tk.Button(buttons_frame_row_9, text="Show Results", command=self.show_results)
        show_result_button.pack(side="left", padx=25)
        update_result_button = tk.Button(buttons_frame_row_9, text="Update Results File", command=self.update_excel)
        update_result_button.pack(side="left", padx=25)
        open_result_button = tk.Button(buttons_frame_row_9, text="Open Results File", command=self.open_xdsrunner_excel)
        open_result_button.pack(side="left", padx=25)
        tk.Label(buttons_frame_row_9, text=">>> xdsrunner.xlsx", bg='white').pack(side="left", padx=5)
        ToolTip(show_result_button, "Display running result below. The result is stored in xdsrunner.xlsx")
        ToolTip(update_result_button, "Update result file with latest results.")
        ToolTip(open_result_button, "Open the result file with Excel or Libreoffice.")
        # Save thread
        self.thread = {}

    def on_select(self) -> None:
        """
        Handle format selection changes for image conversion and rearrange UI elements accordingly.
        """
        if self.selected_format_option.get() == 1:
            self.is_beam_stop_checkbox.pack_forget()
            self.is_beam_stop_checkbox_label.pack_forget()
            self.nxs_button.pack_forget()
            self.mrc_button.pack_forget()
            self.tiff_button.pack_forget()
            self.animation_canvas.pack_forget()
            self.instamatic_button.pack(side="left", padx=25)
            self.is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
            self.is_beam_stop_checkbox_label.pack(side="left")
        elif self.selected_format_option.get() == 2:
            self.is_beam_stop_checkbox.pack_forget()
            self.is_beam_stop_checkbox_label.pack_forget()
            self.animation_canvas.pack_forget()
            self.tiff_button.pack_forget()
            self.nxs_button.pack_forget()
            self.mrc_button.pack(side="left", padx=25)
            self.animation_canvas.pack(side="left", padx=10)
            self.instamatic_button.pack_forget()
            self.is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
            self.is_beam_stop_checkbox_label.pack(side="left")
        elif self.selected_format_option.get() == 3:
            self.is_beam_stop_checkbox.pack_forget()
            self.is_beam_stop_checkbox_label.pack_forget()
            self.nxs_button.pack_forget()
            self.mrc_button.pack_forget()
            self.animation_canvas.pack_forget()
            self.instamatic_button.pack_forget()
            self.tiff_button.pack(side="left", padx=25)
            self.animation_canvas.pack(side="left", padx=10)
            self.is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
            self.is_beam_stop_checkbox_label.pack(side="left")
        elif self.selected_format_option.get() == 4:
            self.is_beam_stop_checkbox.pack_forget()
            self.is_beam_stop_checkbox_label.pack_forget()
            self.animation_canvas.pack_forget()
            self.tiff_button.pack_forget()
            self.nxs_button.pack(side="left", padx=25)
            self.mrc_button.pack_forget()
            self.animation_canvas.pack(side="left", padx=10)
            self.instamatic_button.pack_forget()
            self.is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
            self.is_beam_stop_checkbox_label.pack(side="left")

    def run_mrc_to_img(self) -> None:
        """
        Start MRC-to-IMG conversion in a separate thread and animate the process.
        """
        if self.input_path:
            print(f"Convert MRC Image in {self.input_path} to SMV format.\n")
            self.mrc_to_img_animation_active = True
            self.thread["conversion"] = threading.Thread(target=image_io.convert_mrc2img,
                                                         args=(self.input_path, path_filter))
            self.thread["conversion"].start()
            self.conversion_animation()

    def run_nxs_to_img(self) -> None:
        """
        Start NXS-to-IMG conversion to SMV format in a separate thread and animate the process.
        """
        if self.input_path:
            print(f"Convert NXS Image in {self.input_path} to SMV format.\n")
            self.mrc_to_img_animation_active = True
            self.thread["conversion"] = threading.Thread(target=image_io.convert_nxs2img,
                                                         args=(self.input_path, path_filter))
            self.thread["conversion"].start()
            self.conversion_animation()

    def run_tiff_to_img(self) -> None:
        """
        Start TIFF-to-IMG conversion to SMV format in a separate thread and animate the process.
        """
        if self.input_path:
            print(f"Convert TIFF Image in {self.input_path} to SMV format.\n")
            self.mrc_to_img_animation_active = True
            self.thread["conversion"] = threading.Thread(target=image_io.convert_tiff2img,
                                                         args=(self.input_path, path_filter))
            self.thread["conversion"].start()
            self.conversion_animation()

    def run_xds_writer(self) -> None:
        """
        Write XDS.INP files for the converted images using 'write_xds_file' function.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["xds_writer"] = threading.Thread(target=xds_input.write_xds_file,
                                                     args=(self.input_path, None, path_filter))
        self.thread["xds_writer"].start()

    def self_beam_center(self) -> None:
        """
        Find the beam center without using a beam stop. Starts a thread to calculate the beam centre.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["beam_center"] = threading.Thread(target=image_io.centre_calculate, args=(self.input_path,))
        self.thread["beam_center"].start()

    def self_beam_stop(self) -> None:
        """
        Find the beam center with a beam stop in use. Starts a thread to process beam stop data.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        if messagebox.askyesno("Warning", "Are you sure you HAVE used Beam Stop?"):
            self.thread["beam_center"] = threading.Thread(target=image_io.beam_stop_calculate, args=(self.input_path,))
            self.thread["beam_center"].start()

    def run_xdsrunner(self) -> None:
        """
        Initiate XDS batch processing in a separate thread and show running animation.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.xdsrunner_animation_active = True
        self.xdsrunner_animation_angle = 0
        xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
        self.thread["xds_runner"] = KillableThread(target=xds_runner.xdsrunner, args=(self.input_path, xds_list, False))
        self.thread["xds_runner"].start()
        self.xdsrunner_animate()

    def stop_xdsrunner(self) -> None:
        """
        Stop the ongoing XDS batch process by terminating the associated thread.
        """
        if "xds_runner" in self.thread:
            self.thread["xds_runner"].terminate()
            messagebox.showinfo("Info", "XDSrunner is terminated as required.")
            self.stop_xdsrunner_animation()

    def show_results(self) -> None:
        """
        Display results from xdsrunner.xlsx in a Treeview widget within the page.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            self.display_excel_data(xdsrunner_excel_path)
        else:
            messagebox.showinfo("Error", "Cannot find xdsrunner.xlsx. Check or update it.")

    def update_excel(self) -> None:
        """
        Update the result files (xdsrunner.xlsx) with the latest processed data.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["update_excel"] = threading.Thread(target=xds_runner.excel_extract,
                                                       args=(self.input_path, False))
        self.thread["update_excel"].start()

    def open_xdsrunner_excel(self) -> None:
        """
        Open the xdsrunner.xlsx or xdsrunner2.xlsx file in LibreOffice or Explorer.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            if os.path.exists(xdsrunner_excel_path):
                try:
                    if is_wsl:
                        # Use explorer.exe to open the file
                        subprocess.call(
                            ["wsl.exe", "cmd.exe", "/C",
                             f"start explorer.exe {linux_to_windows_path(xdsrunner_excel_path)}"])
                        return

                    libreoffice_path = subprocess.run(["which", "libreoffice"], capture_output=True,
                                                      text=True).stdout.strip()
                    if libreoffice_path:
                        subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
                        return
                except Exception as e:
                    messagebox.showerror("Caution", f"Error opening the form due to {e}.")
                messagebox.showerror("Caution", f"Neither LibreOffice nor Explorer is available.")
        else:
            messagebox.showerror("Cannot find xdsrunner.xlsx at the specified input path.")

    def display_excel_data(self, file_path: str) -> None:
        """
        Display an Excel file's content in a Treeview widget.

        Args:
            file_path (str): The path to the Excel file to be displayed.
        """
        df = pd.read_excel(file_path, engine='openpyxl')
        try:
            df.drop(columns=['Rmeas'], inplace=True)
        except Exception:
            pass

        # Create Treeview widget and add a scrollbar
        tree = ttk.Treeview(self, show="headings")
        hsb = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        tree["columns"] = list(df.columns)

        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=int(28 * self.sf ** 2.5))
        style.configure("Treeview.Heading", font=("Liberation Sans", int(13 * self.sf), "bold"))

        # Design row colors
        tree.tag_configure('evenrow', background='lightgrey')
        tree.tag_configure('oddrow', background='white')

        # Set column headers and center-align the text
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Add data to the Treeview with alternating colors
        for i, row in enumerate(df.itertuples(index=False, name=None)):
            tags = ('evenrow' if i % 2 == 0 else 'oddrow',)
            tree.insert("", "end", values=row, tags=tags)

        # Automatically adjust column widths based on content
        self.auto_adjust_columns(tree, df)

        # Place Treeview and scrollbar
        tree.grid(row=15, column=0, columnspan=3, sticky='nsew')
        vsb.grid(row=15, column=3, sticky='ns')
        hsb.grid(row=16, column=0, columnspan=3, sticky='ew')

        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable
        self.grid_rowconfigure(15, weight=1)  # Make the Treeview row expandable

    def auto_adjust_columns(self, tree: ttk.Treeview, df: pd.DataFrame) -> None:

        """
            Automatically adjust column widths in the Treeview for better readability.

            Args:
                tree (ttk.Treeview): The Treeview widget containing data.
                df (pd.DataFrame): The DataFrame whose columns are displayed.
                sf (float): Scaling factor for adjusting column width.
            """
        for i, col in enumerate(tree["columns"]):
            max_width = 0
            for value in df[col]:
                width = font.Font().measure(str(value))
                if width > max_width:
                    max_width = width
            tree.column(col, width=int(max_width * self.sf * self.sf) + 20)

    def instamatic_inp_update(self) -> None:
        """
        Update XDS.INP files generated by Instamatic to the newest version, running instamatic_update.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        # Modify the xds.inp generated by @Instamatic
        user_response = messagebox.askyesno(
            "For instamatic user",
            "Do you really want to update ALL xds.inp generated by instamatic to the newest version?")
        if user_response:
            self.thread["instamatic_xds"] = threading.Thread(target=xds_input.instamatic_update,
                                                             args=(self.input_path, path_filter))
            self.thread["instamatic_xds"].start()

    def conversion_animation(self) -> None:
        """
        Animate the MRC-to-IMG conversion process, rotating an arc on a canvas until the thread finishes.
        """
        if self.mrc_to_img_animation_active:
            self.animation_canvas.delete("all")
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.mrc_to_img_animation_angle,
                                             extent=120, style=tk.ARC)
            self.animation_canvas.create_text(50, 10, text="Run... ", anchor="w")
            self.mrc_to_img_animation_angle = (self.mrc_to_img_animation_angle + 10) % 360
            if self.thread["conversion"].is_alive():
                self.after(100, self.conversion_animation)
            else:
                self.stop_mrc_to_img_animation()

    def stop_mrc_to_img_animation(self) -> None:
        """
        Stop the MRC-to-IMG conversion animation and clear the canvas.
        """
        self.mrc_to_img_animation_active = False
        self.animation_canvas.delete("all")

    def xdsrunner_animate(self) -> None:
        """
        Animate the XDS runner process by rotating an arc until the thread finishes.
        """
        if self.xdsrunner_animation_active:
            self.xdsrunner_animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.xdsrunner_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1,
                                                       start=self.xdsrunner_animation_angle, extent=120, style=tk.ARC)
            self.xdsrunner_animation_canvas.create_text(50, 10, text="Running... ", anchor="w")

            self.xdsrunner_animation_angle = (self.xdsrunner_animation_angle + 10) % 360

            # test .py processing
            if self.thread["xds_runner"].is_alive():
                self.after(100, self.xdsrunner_animate)
            else:
                self.stop_xdsrunner_animation()

    def stop_xdsrunner_animation(self) -> None:
        """
        Stop the XDS runner animation and clear the canvas.
        """
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_canvas.delete("all")

    def correct_input(self) -> None:
        """
        Correct input parameters from image metadata (distance, pixel size, etc.).
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["correct_input"] = threading.Thread(target=xds_input.correct_inputs, args=(self.input_path,))
        self.thread["correct_input"].start()

    def on_beam_stop_checkbox_change(self) -> None:
        """
        Update the UI when beam stop usage is toggled, changing the beam finding button.
        """
        if self.is_beam_stop.get():
            self.beam_centre_button.grid_remove()
            self.beam_centre_button = tk.Button(self.buttons_frame_row_5, text="Beam Stop Finding",
                                                command=self.self_beam_stop)
            self.beam_centre_button.grid(row=5, column=2, sticky="w", padx=25, pady=self.sp)
            ToolTip(self.beam_centre_button, "Find the origin point of the beam w/ beam stop.")
        else:
            self.beam_centre_button.grid_remove()
            self.beam_centre_button = tk.Button(self.buttons_frame_row_5, text="Beam Centre Finding",
                                                command=self.self_beam_center)
            self.beam_centre_button.grid(row=5, column=2, sticky="w", padx=25, pady=self.sp)
            ToolTip(self.beam_centre_button, "Find the origin point of the beam w/o beam stop.")

    def estimate_symmetry(self) -> None:
        """
        Estimate symmetry and cell clustering with a new thread by calling analysis_lattice_symmetry.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["estimate_symmetry"] = threading.Thread(
            target=xds_cluster.analysis_lattice_symmetry, args=(self.input_path, path_filter))
        self.thread["estimate_symmetry"].start()


class UnitCellCorr(Page):
    """Class UnitCellCorr
    Updates and applies unit cell parameters to all XDS.INP files.

    Methods:
        __init__(parent): Initializes the UnitCellCorr page and sets up GUI elements.
        save_cell_info(): Saves space group and unit cell parameters into 'Cell_information.txt'.
        run_xdsrunner2(): Runs XDS again with the updated cell parameters.
        stop_xdsrunner2(): Stops the ongoing XDS batch run.
        show_results(): Shows updated results from xdsrunner2.xlsx.
        open_xdsrunner_excel(): Opens the xdsrunner2.xlsx file for inspection.
        update_excel(): Updates results based on latest processed data.
        display_excel_data(file_path): Displays the content of an Excel results file in a Treeview.
        auto_adjust_columns(tree, df, sf): Automatically adjusts column widths for readability.
        xdsrunner_animate(): Animates the XDS runner process.
        stop_xdsrunner_animation(): Stops the XDS runner animation.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the UnitCellCorr page and set up GUI elements for applying unit cell parameters.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this page will be placed.
        """
        Page.__init__(self, parent)
        self.thread = {}
        self.sf = self.master.master.sf
        sp = 5 * self.sf ** 2.5
        self.input_path = ""

        # Row 1: Instruction message
        instruction_msg = "Input Space group and unit cell parameters."
        tk.Label(self, text=instruction_msg, bg='white').grid(row=0, column=0, columnspan=2, sticky="w", padx=10,
                                                              pady=(3 * sp, 2 * sp))

        # Row 2: Additional information
        additional_info = (
            "Providing unit cell and space group keywords for all datasets is suggested for later data merging. "
            "Fetch results from xdsrunner.xlsx / estimate_symmetry")
        tk.Label(self, text=additional_info, font=("Liberation Sans", int(14 * self.sf), "italic"),
                 bg='white').grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=sp)

        # Row 3: Blind unit cell searching information
        blind_search_info = "XDS will refine unit cells individually."
        tk.Label(self, text=blind_search_info, font=("Liberation Sans", int(14 * self.sf), "italic"),
                 bg='white').grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 2 * sp))

        # Row 4: Cell information input
        cell_info_frame = tk.Frame(self, bg='white')
        cell_info_frame.grid(row=4, column=0, sticky="w", padx=10, pady=sp)
        tk.Label(cell_info_frame, text="Space group:", bg='white').pack(side="left", padx=(10, 5))
        self.space_group_entry = tk.Entry(cell_info_frame, width=8)
        self.space_group_entry.pack(side="left")
        ToolTip(self.space_group_entry, "Space group number (1-230)")
        tk.Label(cell_info_frame, text="Unit cell:", bg='white').pack(side="left", padx=(20, 5))
        self.unit_cell_entry = tk.Entry(cell_info_frame, width=35)
        self.unit_cell_entry.pack(side="left")
        ToolTip(self.unit_cell_entry, "Unit cell parameters, can be segmented by space or \", \" (space after comma).")

        # Row 5: Save button，Update cell information button
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=5, column=0, sticky="w", padx=10, pady=2 * sp)
        update_cell_button = tk.Button(buttons_frame, text="Update Cell Parameters", command=self.save_cell_info)
        update_cell_button.pack(side="left", padx=(25, 25))
        ToolTip(update_cell_button, "Copy the sg and cell to all XDS.INP under work directory."
                                    "\nThe information is stored in \"Cell_information.txt\"")

        # Row 6: RUN xds again label
        run_xds_again_msg = "* Run XDS with updated .inp files."
        tk.Label(self, text=run_xds_again_msg, bg='white').grid(row=6, column=0,
                                                                columnspan=2, sticky="w", padx=10, pady=sp)

        # Row 7: RUN xds again buttons
        buttons_frame_row_7 = tk.Frame(self, bg='white')
        buttons_frame_row_7.grid(row=7, column=0, sticky="w", padx=10, pady=2 * sp)
        run_xds_button = tk.Button(buttons_frame_row_7, text="Run XDS with Cell", command=self.run_xdsrunner2)
        run_xds_button.pack(side="left", padx=25)
        ToolTip(run_xds_button, "Run XDS batchly under work directory with given cell.")
        stop_run_xds_button = tk.Button(buttons_frame_row_7, text="Stop Run", command=self.stop_xdsrunner2)
        stop_run_xds_button.pack(side="left", padx=25)
        ToolTip(stop_run_xds_button, "Stop the processing after current XDS run.")
        self.xdsrunner_animation_canvas = tk.Canvas(buttons_frame_row_7, width=150, height=20, bg='white',
                                                    highlightthickness=0)
        self.xdsrunner_animation_canvas.pack(side="left", padx=10)
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_angle = 0

        # Row 8: Show all information label
        tk.Label(self, text="* Show running result", bg='white').grid(row=8, column=0, sticky="w", padx=10, pady=sp)

        # Row 9: Show all information buttons
        buttons_frame_row_9 = tk.Frame(self, bg='white')
        buttons_frame_row_9.grid(row=9, column=0, sticky="w", padx=10, pady=2 * sp)
        show_result_button = tk.Button(buttons_frame_row_9, text="Show Results", command=self.show_results)
        show_result_button.pack(side="left", padx=25)
        update_result_button = tk.Button(buttons_frame_row_9, text="Update Results File", command=self.update_excel)
        update_result_button.pack(side="left", padx=25)
        open_result_button = tk.Button(buttons_frame_row_9, text="Open Result File", command=self.open_xdsrunner_excel)
        open_result_button.pack(side="left", padx=25)
        tk.Label(buttons_frame_row_9, text=">>> xdsrunner2.xlsx", bg='white').pack(side="left", padx=5)
        ToolTip(show_result_button, "Display running result below. The result is stored in xdsrunner2.xlsx")
        ToolTip(update_result_button, "Update result file with latest results.")
        ToolTip(open_result_button, "Open the result file with Excel or Libreoffice.")

    def save_cell_info(self) -> None:
        """
        Save space group and unit cell parameters into 'Cell_information.txt' in the input path.
        Apply these parameters to all XDS.INP files.
        """
        space_group = self.space_group_entry.get()
        unit_cell = self.unit_cell_entry.get()

        # Get the input path from the main application
        main_app = self.master.master
        input_path = main_app.input_path

        if not input_path:
            print("Please select an input path first.")
            return  # Exit the method if no input path is set
        if not space_group or not unit_cell or len(unit_cell.split()) != 6:
            messagebox.showinfo("Caution", f"You need to fill both entries properly.")
            return
        if "," in unit_cell:
            if len(unit_cell.split(", ")) == 6:
                unit_cell = unit_cell.replace(",", " ")
            else:
                unit_cell = unit_cell.replace(",", ".")
        output_file_path = os.path.join(input_path, "Cell_information.txt")

        with open(output_file_path, "w") as file:
            file.write("#####Crystal Information#####\n\n")
            file.write(f"1. Space group\nSPACE_GROUP_NUMBER= {space_group}\n\n")
            file.write(f"2. Unit cell\nUNIT_CELL_CONSTANTS= {unit_cell}\n")

        messagebox.showinfo("Info", f"Cell information saved to {output_file_path}\n")
        self.thread["cell_correct"] = threading.Thread(target=xds_input.cell_correct,
                                                       args=(self.input_path, path_filter))
        self.thread["cell_correct"].start()

    def run_xdsrunner2(self) -> None:
        """
        Run XDS again with updated cell parameters. Animate the process while running.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.xdsrunner_animation_active = True
        self.xdsrunner_animation_angle = 0
        xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
        self.thread["xds_runner"] = KillableThread(target=xds_runner.xdsrunner, args=(self.input_path, xds_list, True))
        self.thread["xds_runner"].start()
        self.xdsrunner_animate()

    def stop_xdsrunner2(self) -> None:
        """
        Stop the ongoing XDS batch run by terminating the associated thread.
        """
        if "xds_runner" in self.thread:
            self.thread["xds_runner"].terminate()
            messagebox.showerror("Caution", "XDSrunner is terminated as required.")
            self.stop_xdsrunner_animation()

    def show_results(self) -> None:
        """
        Show updated results from xdsrunner2.xlsx in a Treeview.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            self.display_excel_data(xdsrunner_excel_path)
        else:
            messagebox.showinfo("Error", "Cannot find xdsrunner2.xlsx. Check or update it.")

    def open_xdsrunner_excel(self) -> None:
        """
        Open xdsrunner2.xlsx file in LibreOffice or Explorer for inspection.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            if os.path.exists(xdsrunner_excel_path):
                try:
                    if is_wsl:
                        # Use explorer.exe to open the file
                        subprocess.call(
                            ["wsl.exe", "cmd.exe", "/C",
                             f"start explorer.exe {linux_to_windows_path(xdsrunner_excel_path)}"])
                        return

                    libreoffice_path = subprocess.run(["which", "libreoffice"], capture_output=True,
                                                      text=True).stdout.strip()
                    if libreoffice_path:
                        subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
                        return
                except Exception as e:
                    messagebox.showerror("Caution", f"Error opening the form due to {e}.")
                messagebox.showerror("Caution", f"Neither LibreOffice nor Explorer is available.")
        else:
            messagebox.showerror("Caution", "Cannot find xdsrunner2.xlsx at the specified input path.")

    def update_excel(self) -> None:
        """
        Update the results based on the latest processed data after applying cell parameters.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["update_excel"] = threading.Thread(target=xds_runner.excel_extract, args=(self.input_path, True))
        self.thread["update_excel"].start()

    def display_excel_data(self, file_path: str) -> None:
        """
        Display the content of an Excel results file in a Treeview widget.

        Args:
            file_path (str): The path to the Excel file to display.
        """
        df = pd.read_excel(file_path, engine='openpyxl')
        try:
            df.drop(columns=['Integration Cell'], inplace=True)
        except Exception:
            pass

        # Create Treeview widget and add a scrollbar
        tree = ttk.Treeview(self, show="headings")
        hsb = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        tree["columns"] = list(df.columns)

        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=int(28 * self.sf ** 2.5))
        style.configure("Treeview.Heading", font=("Liberation Sans", int(13 * self.sf), "bold"))

        # Design row colors
        tree.tag_configure('evenrow', background='lightgrey')
        tree.tag_configure('oddrow', background='white')

        # Set column headers and center-align the text
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Add data to the Treeview with alternating colors
        for i, row in enumerate(df.itertuples(index=False, name=None)):
            tags = ('evenrow' if i % 2 == 0 else 'oddrow',)
            tree.insert("", "end", values=row, tags=tags)

        # Automatically adjust column widths based on content
        self.auto_adjust_columns(tree, df, self.sf)

        # Place Treeview and scrollbar
        tree.grid(row=15, column=0, columnspan=3, sticky='nsew')
        vsb.grid(row=15, column=3, sticky='ns')
        hsb.grid(row=16, column=0, columnspan=3, sticky='ew')

        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable
        self.grid_rowconfigure(15, weight=1)  # Make the Treeview row expandable

    @classmethod
    def auto_adjust_columns(cls, tree: ttk.Treeview, df: pd.DataFrame, sf: float) -> None:
        """
        Automatically adjust column widths in the Treeview for the displayed DataFrame.

        Args:
            tree (ttk.Treeview): The Treeview widget.
            df (pd.DataFrame): The DataFrame with data.
            sf (float): Scaling factor for adjusting column width.
        """
        for i, col in enumerate(tree["columns"]):
            max_width = 0
            for value in df[col]:
                width = font.Font().measure(str(value))
                if width > max_width:
                    max_width = width
            tree.column(col, width=int(sf * sf * max_width) + 10)

    def xdsrunner_animate(self) -> None:
        """
        Animate the XDS runner process after applying cell parameters until the thread finishes.
        """
        if self.xdsrunner_animation_active:
            self.xdsrunner_animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.xdsrunner_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1,
                                                       start=self.xdsrunner_animation_angle, extent=120, style=tk.ARC)
            self.xdsrunner_animation_canvas.create_text(50, 10, text="Running... ", anchor="w")

            self.xdsrunner_animation_angle = (self.xdsrunner_animation_angle + 10) % 360

            # test .py processing
            if self.thread["xds_runner"].is_alive():
                self.after(100, self.xdsrunner_animate)
            else:
                self.stop_xdsrunner_animation()

    def stop_xdsrunner_animation(self) -> None:
        """
        Stop the XDS runner animation and clear the canvas.
        """
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_canvas.delete("all")


class XDSRefine(Page):
    """Class XDSRefine
    Refines XDS.INP files based on chosen subsets and criteria.

    Methods:
        __init__(parent): Initializes the refinement page and GUI elements.
        handle_range_option_select(event): Changes the UI depending on selected range mode (All, Selected, Ranged, Single).
        hide_all_widgets(): Hides all range selection widgets.
        show_selected_widgets(): Shows widgets for filtering data by a certain statistic.
        show_ranged_widgets(): Shows widgets for specifying a range of datasets by index.
        show_single_widgets(): Shows widgets for selecting a single dataset.
        show_failed_widgets(): Shows widgets for selecting failed datasets to retry.
        view_lattice(): Displays reciprocal lattice visualization for a chosen dataset.
        run_xdsgui(): Launches XDSGUI on the selected dataset.
        open_html_report(): Opens the HTML report for the selected single dataset.
        run_xdsconv_shelx(): Converts data to SHELX format (.hkl and .p4p).
        handle_filter_option_select(event): Adjusts default threshold values when a filter option is selected.
        refresh_list(): Updates the single dataset list from xdsrunner2.xlsx.
        refresh_failed_list(): Updates the failed dataset list from results.
        get_xds_list(): Retrieves a list of XDS.INP files based on the selected criteria.
        run_xds(): Runs XDS refinements based on chosen criteria and parameters.
        open_keyword_manager(): Opens a Keyword Manager app for adding/deleting/calibrating keywords.
        stop_xds(): Stops the ongoing refinement process.
        show_results(): Displays updated results in a Treeview.
        open_xdsrunner_excel(): Opens xdsrunner2.xlsx in an external viewer.
        update_excel(): Updates the results file.
        display_excel_data(file_path): Displays Excel data in a Treeview widget.
        auto_adjust_columns(tree, df, sf): Adjusts column widths dynamically.
        xdsrunner_animate(): Animates the XDS refinement process.
        stop_xdsrunner_animation(): Stops the refinement animation.
        open_folder(): Opens the folder of the selected dataset.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the refinement page and set up GUI elements for advanced XDS parameter refinement.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this page will be placed.
        """
        super().__init__(parent)
        self.relative_paths = None
        self.thread = {}
        self.sf = self.master.master.sf
        sp = 5 * self.sf ** 2.5
        self.input_path = ""

        # Row 1: Instruction2
        note_label = tk.Label(self,
                              text="Refine Input Parameters in XDS.INP. Get data reduction result from single dataset.",
                              bg='white', )
        note_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(4 * sp, 0))

        # Row 2: Instruction1
        note_label = tk.Label(self,
                              text="Use AutoLEI to refine XDS.INP files in the target folder.",
                              font=("Liberation Sans", int(14 * self.sf), "italic"),
                              bg='white')
        note_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(3 * sp, sp))

        # Loading default setting from setting.ini
        outlier_scale_ratio = float(config["Inp_Refine"]["outlier_scale_ratio"])
        bool_update_index_ratio = strtobool(config["Inp_Refine"]["update_index_ratio"])
        bool_update_axis = strtobool(config["Inp_Refine"]["update_rotation_axis"])
        bool_outlier_remove = strtobool(config["Inp_Refine"]["remove_scale_outlier"])
        bool_divergence = strtobool(config["Inp_Refine"]["add_divergence"])
        bool_update_resolution = strtobool(config["Inp_Refine"]["update_resolution"])
        bool_correct_centre = strtobool(config["Inp_Refine"]["correct_centre"])

        # Line 1: Select range for refinement
        checkbox_frame_l1 = tk.Frame(self, bg='white')
        checkbox_frame_l1.grid(row=2, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(checkbox_frame_l1, text="Refine on data as ", bg='white').pack(side="left", padx=(5, 5))
        self.range_option_var = tk.StringVar(self)
        self.range_option_var.set('--')  # default value
        self.range_options = ["All", "Selected", "Ranged", "Single", "Failed"]
        self.range_option_menu = ttk.Combobox(checkbox_frame_l1, textvariable=self.range_option_var,
                                              values=self.range_options, state='readonly', width=10)
        self.range_option_menu.pack(side="left", padx=(5, 5))
        self.range_option_menu.bind('<<ComboboxSelected>>', self.handle_range_option_select)
        self.range_option_menu.set(self.range_options[0])
        ToolTip(self.range_option_menu, "Can select range for inp refinement.\n"
                                        "If ins/hkl for single data set is needed, please select \"single\".")

        # For selected
        self.select_label = tk.Label(checkbox_frame_l1, text="with ", bg='white')

        self.filter_option_var = tk.StringVar(self)
        self.filter_option_var.set('--')  # default value
        filter_options = ["--", "Index%", "I/Sigma", "CC1/2", "Resolution"]
        self.filter_option_menu = ttk.Combobox(checkbox_frame_l1, textvariable=self.filter_option_var,
                                               values=filter_options, state='readonly', width=10)
        ToolTip(self.filter_option_menu, "Select data based on statistics.")

        self.filter_option_menu.bind('<<ComboboxSelected>>', self.handle_filter_option_select)

        self.sign_option_var = tk.StringVar(self)
        self.sign_options = [">", "<"]
        self.sign_option_menu = ttk.Combobox(checkbox_frame_l1, textvariable=self.sign_option_var,
                                             values=self.sign_options, state='readonly', width=3)
        self.sign_option_menu.set(self.sign_options[1])
        self.statistic_threshold = tk.Entry(checkbox_frame_l1, bg='white', width=5)

        # For range
        self.range_input = tk.Entry(checkbox_frame_l1, bg='white', width=30)
        ToolTip(self.range_input, "Use \",\" to separate the datasets ranges. (1st row in excel)")
        self.range_label = tk.Label(checkbox_frame_l1,
                                    text=">> Example: 1, 2-4",
                                    bg='white')

        # For single
        self.single_label = tk.Label(checkbox_frame_l1, text="on ", bg='white')
        self.single_file_option_var = tk.StringVar(self)
        self.single_file_options = ["--"]
        self.single_file_option_menu = ttk.Combobox(checkbox_frame_l1, textvariable=self.single_file_option_var,
                                                    values=self.single_file_options, state='readonly', width=65)
        self.single_file_option_menu.set("--")
        ToolTip(self.single_file_option_menu, "Select dataset for web report, hkl conversion or open with XDS.")

        # For failed
        self.failed_label = tk.Label(checkbox_frame_l1, text="on ", bg='white')
        self.failed_file_option_var = tk.StringVar(self)
        self.failed_file_options = ["--"]
        self.failed_file_option_menu = ttk.Combobox(checkbox_frame_l1, textvariable=self.failed_file_option_var,
                                                    values=self.failed_file_options, state='readonly', width=65)
        self.failed_file_option_menu.set("--")
        ToolTip(self.failed_file_option_menu, "Select failed dataset to improve.")

        # Line 2
        checkbox_frame_l2 = tk.Frame(self, bg='white')
        checkbox_frame_l2.grid(row=4, column=0, sticky="w", padx=10, pady=2 * sp)

        # Update Axis
        self.update_axis = tk.BooleanVar(value=bool_update_axis)
        axis_checkbox = tk.Checkbutton(checkbox_frame_l2, variable=self.update_axis, bg='white')
        axis_checkbox.grid(row=1, column=2, padx=(30, 10), pady=sp, sticky="w")
        axis_checkbox_label = tk.Label(checkbox_frame_l2, text="Rotation Axis", bg='white')
        axis_checkbox_label.grid(row=1, column=3, sticky="w", padx=(0, 20))
        ToolTip(axis_checkbox, "Refine the rotation axis by AutoLEI")

        # Add Divergence
        self.add_divergence = tk.BooleanVar(value=bool_divergence)
        add_divergence_checkbox = tk.Checkbutton(checkbox_frame_l2, variable=self.add_divergence, bg='white')
        add_divergence_checkbox.grid(row=1, column=4, padx=10, pady=sp, sticky="w")
        add_divergence_checkbox_label = tk.Label(checkbox_frame_l2, text="Divergence & Mosaicity", bg='white')
        add_divergence_checkbox_label.grid(row=1, column=5, sticky="w", padx=(0, 20))
        ToolTip(add_divergence_checkbox, "Add the Divergence & Mosaicity from INTEGRATE.LP")

        # Update outlier_remove
        self.remove_scale_outlier = tk.BooleanVar(value=bool_outlier_remove)
        scale_outlier_checkbox = tk.Checkbutton(checkbox_frame_l2, variable=self.remove_scale_outlier, bg='white')
        scale_outlier_checkbox.grid(row=1, column=6, padx=10, pady=sp, sticky="w")
        scale_outlier_checkbox_label1 = tk.Label(checkbox_frame_l2, text="Remove Scale Outlier >", bg='white')
        scale_outlier_checkbox_label1.grid(row=1, column=7, sticky="w", padx=(0, 10))
        self.scale_outlier_ratio = tk.Entry(checkbox_frame_l2, bg='white', width=4)
        self.scale_outlier_ratio.grid(row=1, column=8, sticky="w", padx=2)
        scale_outlier_checkbox_label2 = tk.Label(checkbox_frame_l2, text="IQR", bg='white')
        scale_outlier_checkbox_label2.grid(row=1, column=9, sticky="w", padx=(5, 15))
        replace_entry(self.scale_outlier_ratio, "{:.1f}".format(outlier_scale_ratio))
        ToolTip(scale_outlier_checkbox, "Remove bad frames on scale.")
        ToolTip(self.scale_outlier_ratio, "Default 2.0, in IQR.")

        # Correct Beam Centre
        self.correct_centre = tk.BooleanVar(value=bool_correct_centre)
        correct_centre_checkbox = tk.Checkbutton(checkbox_frame_l2, variable=self.correct_centre, bg='white')
        correct_centre_checkbox.grid(row=1, column=10, padx=10, pady=sp, sticky="w")
        correct_centre_checkbox_label = tk.Label(checkbox_frame_l2, text="Beam Centre", bg='white')
        correct_centre_checkbox_label.grid(row=1, column=11, sticky="w", padx=(0, 20))
        ToolTip(correct_centre_checkbox, "(For Beam Stop only) Refine the beam centre by Friedel's Pair.")

        checkbox_frame_l3 = tk.Frame(self, bg='white')
        checkbox_frame_l3.grid(row=5, column=0, sticky="w", padx=10, pady=2 * sp)

        # Update Ratio %
        self.update_index_ratio = tk.BooleanVar(value=bool_update_index_ratio)
        index_ratio_checkbox = tk.Checkbutton(checkbox_frame_l3, variable=self.update_index_ratio, bg='white')
        index_ratio_checkbox.pack(side="left", padx=(30, 5))
        index_ratio_checkbox_label = tk.Label(checkbox_frame_l3,
                                              text="Refine Index Ratio on datasets with index% <",
                                              bg='white')
        index_ratio_checkbox_label.pack(side="left", padx=(5, 5))
        self.index_ratio_threshold = tk.Entry(checkbox_frame_l3, bg='white', width=4)
        self.index_ratio_threshold.pack(side="left", padx=(5, 5))
        index_ratio_checkbox_label2 = tk.Label(checkbox_frame_l3, text="%", bg='white')
        index_ratio_checkbox_label2.pack(side="left", padx=(5, 5))
        replace_entry(self.index_ratio_threshold, "85.0")
        ToolTip(index_ratio_checkbox, "Increase the index tolerance for better result.")
        ToolTip(self.index_ratio_threshold, "Default 85%, can be changed by autolei_setting.")

        # Update Resolution Range
        self.update_resolution = tk.BooleanVar(value=bool_update_resolution)
        index_update_resolution = tk.Checkbutton(checkbox_frame_l3, variable=self.update_resolution, bg='white')
        index_update_resolution.pack(side="left", padx=(15, 5))
        index_resolution_checkbox_label = tk.Label(checkbox_frame_l3, text="Change Resolution to", bg='white')
        index_resolution_checkbox_label.pack(side="left", padx=(5, 5))
        self.resolution_range = tk.Entry(checkbox_frame_l3, bg='white', width=7)
        self.resolution_range.pack(side="left", padx=(5, 5))
        replace_entry(self.resolution_range, "30  0.8")
        ToolTip(index_update_resolution, "Change the resolution range for data reduction on XDS.")
        ToolTip(self.resolution_range, "Suggest 30 2, for normal protein data.")

        buttons_frame_row_7 = tk.Frame(self, bg='white')
        buttons_frame_row_7.grid(row=8, column=0, sticky="w", padx=10, pady=3 * sp)
        run_xds_button = tk.Button(buttons_frame_row_7, text="Run XDS with Cell", command=self.run_xds)
        run_xds_button.pack(side="left", padx=10)
        ToolTip(run_xds_button, "Refine the input parameter and Run XDS batchly under work directory.")
        stop_run_xds_button = tk.Button(buttons_frame_row_7, text="Stop Run", command=self.stop_xds)
        stop_run_xds_button.pack(side="left", padx=10)
        ToolTip(stop_run_xds_button, "Stop the processing after current XDS run.")
        self.xdsgui_button = tk.Button(buttons_frame_row_7, text="Run XDSGUI", command=self.run_xdsgui)
        ToolTip(self.xdsgui_button, "Open XDSGUI on current working data.")
        self.view_lattice_button = tk.Button(buttons_frame_row_7, text="View Reciprocal Space",
                                             command=self.view_lattice)
        ToolTip(self.view_lattice_button, "View the reciprocal space on current working data.")
        self.xdsrunner_animation_canvas = tk.Canvas(buttons_frame_row_7, width=120, height=20, bg='white',
                                                    highlightthickness=0)
        self.xdsrunner_animation_canvas.pack(side="left", padx=10)
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_angle = 0

        tk.Label(buttons_frame_row_7, text="|", bg='white').pack(side="left", padx=(5, 5))
        change_parameter_button = tk.Button(buttons_frame_row_7,
                                            text="Change Input Parameters", command=self.open_keyword_manager)
        change_parameter_button.pack(side="left", padx=10)
        ToolTip(change_parameter_button, "Change / Delete Keywords, Calibrate Camera Length by Ratio.")

        buttons_frame_row_8 = tk.Frame(self, bg='white')
        buttons_frame_row_8.grid(row=9, column=0, sticky="w", padx=10, pady=(1.5 * sp, 4 * sp))
        show_result_button = tk.Button(buttons_frame_row_8, text="Show Results", command=self.show_results)
        show_result_button.pack(side="left", padx=(10, 20))
        update_result_button = tk.Button(buttons_frame_row_8, text="Update Results File", command=self.update_excel)
        update_result_button.pack(side="left", padx=20)
        ToolTip(show_result_button, "Display running result below. The result is stored in xdsrunner.xlsx")
        ToolTip(update_result_button, "Update result file with latest results.")

        self.bus2shelx_button = tk.Button(buttons_frame_row_8, text="Bus to SHELX", command=self.run_xdsconv_shelx)
        ToolTip(self.bus2shelx_button, "Generate hkl, p4p and cif_od file on current working data.")
        self.excel_open_button = tk.Button(buttons_frame_row_8, text="Open Results File",
                                           command=self.open_xdsrunner_excel)
        self.excel_open_button.pack(side="left", padx=20)
        ToolTip(self.excel_open_button, "Open the result file with Excel or Libreoffice.")
        self.html_button = tk.Button(buttons_frame_row_8, text="Web Report", command=self.open_html_report)
        ToolTip(self.html_button, "Open the web report on current working data.")
        self.folder_button = tk.Button(buttons_frame_row_8, text="Open Folder", command=self.open_folder)
        ToolTip(self.folder_button, "Open the folder of current working data.")

    def handle_range_option_select(self, event: tk.Event) -> None:
        """
        Change the UI based on the selected range mode (All, Selected, Ranged, Single, Failed).

        Args:
            event (object): The Tkinter event object.
        """
        selected_option = self.range_option_menu.get()
        self.hide_all_widgets()

        if selected_option == "Selected":
            self.show_selected_widgets()
        elif selected_option == "Ranged":
            self.show_ranged_widgets()
        elif selected_option == "Single":
            self.show_single_widgets()
            self.refresh_list()
        elif selected_option == "Failed":
            self.show_failed_widgets()
            self.refresh_failed_list()
        else:
            self.excel_open_button.pack(side="left", padx=20)

    def hide_all_widgets(self) -> None:
        """
        Hide all range selection widgets when switching modes.
        """
        self.range_input.pack_forget()
        self.range_label.pack_forget()
        self.select_label.pack_forget()
        self.filter_option_menu.pack_forget()
        self.sign_option_menu.pack_forget()
        self.statistic_threshold.pack_forget()
        self.single_file_option_menu.pack_forget()
        self.failed_file_option_menu.pack_forget()
        self.xdsgui_button.pack_forget()
        self.view_lattice_button.pack_forget()
        self.excel_open_button.pack_forget()
        self.bus2shelx_button.pack_forget()
        self.html_button.pack_forget()
        self.folder_button.pack_forget()

    def show_selected_widgets(self) -> None:
        """
        Show widgets for filtering data by a certain statistic.
        """
        self.select_label.pack(side="left", padx=(5, 10))
        self.filter_option_menu.pack(side="left", padx=(5, 5))
        self.sign_option_menu.pack(side="left", padx=(5, 5))
        self.statistic_threshold.pack(side="left", padx=(5, 5))
        self.excel_open_button.pack(side="left", padx=20)

    def show_ranged_widgets(self) -> None:
        """
        Show widgets for specifying a range of datasets by their indices.
        """
        self.range_input.pack(side="left", padx=(15, 10))
        self.range_label.pack(side="left", padx=(5, 10))
        self.excel_open_button.pack(side="left", padx=20)

    def show_single_widgets(self) -> None:
        """
        Show widgets for selecting a single dataset, including reciprocal lattice visualization and keyword management.
        Refresh the dataset list from xdsrunner2.xlsx.
        """
        self.single_file_option_menu.pack(side="left", padx=(5, 10))
        self.xdsgui_button.pack(side="left", padx=(5, 10))
        self.view_lattice_button.pack(side="left", padx=(5, 10))
        self.bus2shelx_button.pack(side="left", padx=20)
        self.html_button.pack(side="left", padx=20)
        self.folder_button.pack(side="left", padx=20)

    def show_failed_widgets(self) -> None:
        """
        Show widgets for selecting failed datasets to retry processing.
        Refresh the failed dataset list from results.
        """
        self.failed_file_option_menu.pack(side="left", padx=(5, 10))
        self.xdsgui_button.pack(side="left", padx=(5, 10))
        self.view_lattice_button.pack(side="left", padx=(5, 10))
        self.folder_button.pack(side="left", padx=20)

    def view_lattice(self) -> None:
        """
        Display reciprocal lattice visualization for the selected single dataset.
        """
        if self.range_option_menu.get() == "Single":
            selected_option = self.single_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.relative_paths[selected_option]
        elif self.range_option_menu.get() == "Failed":
            selected_option = self.failed_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.failed_relative_paths[selected_option]
        else:
            return None

        if os.path.exists(os.path.join(_path, "IDXREF.LP")):
            xds_report.visualise_lattice(_path)
        else:
            messagebox.showerror("Caution", "This run haven't got spot information.")

    def run_xdsgui(self) -> None:
        """
        Launch XDSGUI on the selected dataset (if single or failed mode).
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        if self.range_option_menu.get() == "Single":
            selected_option = self.single_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.relative_paths[selected_option]
        elif self.range_option_menu.get() == "Failed":
            selected_option = self.failed_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.failed_relative_paths[selected_option]
        else:
            return

        def run_command(_path):
            print("The output of XDSGUI is as below.")
            command = f'xdsgui'
            os.chdir(_path)
            os.system(command)

        command_thread = threading.Thread(target=run_command, args=(_path,))
        command_thread.start()

    def open_html_report(self) -> None:
        """
        Open the HTML report for the selected single dataset.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        selected_option = self.single_file_option_menu.get()
        _path = self.relative_paths[selected_option]

        def open_html_with_error_handling(_path):
            try:
                xds_report.open_html_file(_path, "single")
            except Exception as e:
                messagebox.showerror("Caution", f"Error occurred while opening HTML file: {e}")

        if selected_option == "--":
            pass
        else:
            html_thread = threading.Thread(target=open_html_with_error_handling, args=(_path,))
            html_thread.start()

    def run_xdsconv_shelx(self) -> None:
        """
        Convert data of the selected single dataset to SHELX format (.hkl and .p4p files).
        """
        # Check if input_path is set before running the script
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        selected_option = self.single_file_option_menu.get()
        _path = self.relative_paths[selected_option]

        if selected_option == "--":
            pass
        else:
            self.thread["xdsconv"] = threading.Thread(target=xds_shelx.convert_to_shelx, args=(_path,))
            self.thread["xdsconv"].start()
            self.thread["report"] = threading.Thread(target=xds_report.create_html_file, args=(_path, "single"))
            self.thread["report"].start()

    def handle_filter_option_select(self, event: tk.Event) -> None:
        """
        Adjust default threshold values upon selecting a statistic to filter data by.

        Args:
            event (object): The Tkinter event object.
        """
        selected_option = self.filter_option_menu.get()
        if selected_option == "Resolution":
            self.sign_option_menu.set(self.sign_options[0])
            replace_entry(self.statistic_threshold, "1.10")
        elif selected_option == "Index%":
            self.sign_option_menu.set(self.sign_options[1])
            replace_entry(self.statistic_threshold, "65.0")
        elif selected_option == "CC1/2":
            self.sign_option_menu.set(self.sign_options[1])
            replace_entry(self.statistic_threshold, "95.0")
        elif selected_option == "I/Sigma":
            self.sign_option_menu.set(self.sign_options[1])
            replace_entry(self.statistic_threshold, "4.50")

    def refresh_list(self) -> None:
        """
        Update the single dataset list from xdsrunner2.xlsx for single mode.
        """
        if self.input_path:
            xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
            self.relative_paths = {
                f"{i + 1}:" + os.path.relpath(os.path.dirname(xds_path), self.input_path): os.path.dirname(xds_path)
                for i, xds_path in enumerate(xds_list)}
            self.single_file_options = ["--"] + list(self.relative_paths.keys())
            self.single_file_option_menu['values'] = self.single_file_options
            self.single_file_option_var.set('--')  # Reset to default
        else:
            print("Input path is not set. Please set the input path first.")

    def refresh_failed_list(self) -> None:
        """
        Update the failed dataset list from results for failed mode.
        """
        if self.input_path:
            try:
                result_pd = pd.read_excel(os.path.join(self.input_path, "xdsrunner2.xlsx"), engine="openpyxl")
            except:
                try:
                    result_pd = pd.read_excel(os.path.join(self.input_path, "xdsrunner.xlsx"), engine="openpyxl")
                except:
                    messagebox.showerror("Caution", "No results found. Please update excel or run xds first.")
                    return
            success_list = [os.path.join(self.input_path, path[4:]) if path.startswith("...") else
                            path
                            for path in result_pd["Path"]]
            xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
            self.relative_paths = {
                f"{i + 1}:" + os.path.relpath(os.path.dirname(xds_path), self.input_path): os.path.dirname(xds_path)
                for i, xds_path in enumerate(xds_list)}
            self.failed_relative_paths = {}
            for key, value in self.relative_paths.items():
                if value not in success_list:
                    self.failed_relative_paths[key] = value
            self.failed_file_options = ["--", "all"] + list(self.failed_relative_paths.keys())
            self.failed_file_option_menu['values'] = self.failed_file_options
            self.failed_file_option_var.set('--')  # Reset to default
        else:
            print("Input path is not set. Please set the input path first.")

    def get_xds_list(self) -> list:
        """
        Retrieve a list of XDS.INP files based on the selected criteria in the UI.

        Returns:
            list: A list of paths to XDS.INP files matching the selected criteria.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return []
        xds_list = []
        if self.range_option_menu.get() == "All":
            xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
        elif self.range_option_menu.get() == "Ranged":
            all_xds_list = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
            xds_list = get_elements_by_indices(all_xds_list, self.range_input.get())
        elif self.range_option_menu.get() == "Selected":
            indicator = {"Resolution": "Reso.", "Index%": "Index%", "I/Sigma": "Isa", "CC1/2": "CC1/2"}
            if self.filter_option_menu.get() == "--":
                return []
            xds_list = xds_cluster.get_paths_by_indicator(os.path.join(self.input_path, "xdsrunner2.xlsx"),
                                                          indicator[self.filter_option_menu.get()],
                                                          self.sign_option_menu.get(),
                                                          float(self.statistic_threshold.get()))
            for i, path in enumerate(xds_list):
                if path.startswith("..."):
                    xds_list[i] = os.path.join(self.input_path, path[4:], "XDS.INP")
        elif self.range_option_menu.get() == "Single":
            if self.single_file_option_menu.get() == "--":
                print("Please select data.")
                return []
            else:
                xds_list = [os.path.join(self.relative_paths[self.single_file_option_menu.get()], "XDS.INP")]
        elif self.range_option_menu.get() == "Failed":
            if self.failed_file_option_menu.get() == "all":
                xds_list = [os.path.join(path, "XDS.INP") for path in self.failed_relative_paths.values()]
            elif self.failed_file_option_menu.get() == "--":
                print("Please select data.")
                return []
            else:
                xds_list = [os.path.join(self.failed_relative_paths[self.failed_file_option_menu.get()], "XDS.INP")]
        return xds_list

    def run_xds(self) -> None:
        """
        Run XDS refinements based on chosen criteria and parameters. Animate the process until done.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        xds_list = self.get_xds_list()
        if not xds_list:
            messagebox.showerror("Warning", "You need to select data to continue.")
            return
        parameter_dict = {"axis": self.update_axis.get(), "divergence": self.add_divergence.get(),
                          "scale": float(self.scale_outlier_ratio.get()) if self.remove_scale_outlier.get() else False,
                          "index": float(self.index_ratio_threshold.get()) if self.update_index_ratio.get() else False,
                          "resolution": self.resolution_range.get() if self.update_resolution.get() else False,
                          "beam_centre": self.correct_centre.get()}
        if self.range_option_menu.get() == "Failed":
            parameter_dict["scale"] = False
        self.xdsrunner_animation_active = True
        self.xdsrunner_animation_angle = 0
        self.thread["xds_runner"] = KillableThread(target=xds_runner.refine_run,
                                                   args=(self.input_path, xds_list, parameter_dict))
        self.thread["xds_runner"].start()
        self.xdsrunner_animate()

    def open_keyword_manager(self) -> None:
        """
        Open a Keyword Manager app for adding/deleting/calibrating keywords for XDS.INP files.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        xds_list = self.get_xds_list()
        if not xds_list:
            messagebox.showerror("Warning", "You need to select data to continue.")
            return
        xds_input.create_keyword_manager_app(xds_list)

    def stop_xds(self) -> None:
        """
        Stop the ongoing refinement process by terminating the associated thread.
        """
        if "xds_runner" in self.thread:
            self.thread["xds_runner"].terminate()
            messagebox.showerror("Caution", "xdsrunner is terminated as required.")
            self.stop_xdsrunner_animation()

    def show_results(self) -> None:
        """
        Display updated results from xdsrunner2.xlsx in a Treeview widget.
        """

        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            self.display_excel_data(xdsrunner_excel_path)
        else:
            messagebox.showinfo("Error", "Cannot find xdsrunner2.xlsx. Check or update it.")

    def open_xdsrunner_excel(self) -> None:
        """
        Open xdsrunner2.xlsx in LibreOffice or Explorer.
        """

        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        xdsrunner_excel_path = os.path.join(self.input_path, "xdsrunner2.xlsx")
        if os.path.exists(xdsrunner_excel_path):
            try:
                if is_wsl:
                    # Use explorer.exe to open the file
                    subprocess.call(
                        ["wsl.exe", "cmd.exe", "/C",
                         f"start explorer.exe {linux_to_windows_path(xdsrunner_excel_path)}"])
                    return

                libreoffice_path = subprocess.run(["which", "libreoffice"], capture_output=True,
                                                  text=True).stdout.strip()
                if libreoffice_path:
                    subprocess.call(["libreoffice", "--calc", xdsrunner_excel_path])
                    return
            except Exception as e:
                messagebox.showerror("Caution", f"Error opening the form due to {e}.")
            messagebox.showerror("Caution", f"Neither LibreOffice nor Explorer is available.")
        else:
            messagebox.showerror("Caution", "Cannot find xdsrunner2.xlsx at the specified input path.")

    def update_excel(self) -> None:
        """
        Update the xdsrunner2.xlsx file with the latest processed data after refinement.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["update_excel"] = threading.Thread(target=xds_runner.excel_extract, args=(self.input_path, True))
        self.thread["update_excel"].start()

    def display_excel_data(self, file_path: str) -> None:
        """
        Display Excel data in a Treeview widget for refined datasets.

        Args:
            file_path (str): The path to the Excel file.
        """
        df = pd.read_excel(file_path, engine='openpyxl')
        try:
            df.drop(columns=['Integration Cell'], inplace=True)
        except Exception:
            pass
        # Create Treeview widget and add a scrollbar
        tree = ttk.Treeview(self, show="headings")
        hsb = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        tree["columns"] = list(df.columns)

        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=int(28 * self.sf ** 2.5))
        style.configure("Treeview.Heading", font=("Liberation Sans", int(13 * self.sf), "bold"))

        # Design row colors
        tree.tag_configure('evenrow', background='lightgrey')
        tree.tag_configure('oddrow', background='white')

        # Set column headers and center-align the text
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Add data to the Treeview with alternating colors
        for i, row in enumerate(df.itertuples(index=False, name=None)):
            tags = ('evenrow' if i % 2 == 0 else 'oddrow',)
            tree.insert("", "end", values=row, tags=tags)

        # Automatically adjust column widths based on content
        self.auto_adjust_columns(tree, df, self.sf)

        # Place Treeview and scrollbar
        tree.grid(row=15, column=0, columnspan=3, sticky='nsew')
        vsb.grid(row=15, column=3, sticky='ns')
        hsb.grid(row=16, column=0, columnspan=3, sticky='ew')

        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable
        self.grid_rowconfigure(15, weight=1)  # Make the Treeview row expandable

    @classmethod
    def auto_adjust_columns(cls, tree: ttk.Treeview, df: pd.DataFrame, sf: float) -> None:
        """
        Automatically adjust column widths in the Treeview for the displayed DataFrame.

        Args:
            tree (ttk.Treeview): The Treeview widget.
            df (pd.DataFrame): The DataFrame with data.
            sf (float): Scaling factor for adjusting column width.
        """
        for i, col in enumerate(tree["columns"]):
            max_width = 0
            for value in df[col]:
                width = font.Font().measure(str(value))
                if width > max_width:
                    max_width = width
            tree.column(col, width=int(sf * sf * max_width) + 10)

    def xdsrunner_animate(self) -> None:
        """
        Animate the XDS refinement process until the associated thread finishes.
        """
        if self.xdsrunner_animation_active:
            self.xdsrunner_animation_canvas.delete("all")

            # logic for anime
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.xdsrunner_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1,
                                                       start=self.xdsrunner_animation_angle, extent=120, style=tk.ARC)
            self.xdsrunner_animation_canvas.create_text(50, 10, text="Running... ", anchor="w")

            self.xdsrunner_animation_angle = (self.xdsrunner_animation_angle + 10) % 360

            # test .py processing
            if self.thread["xds_runner"].is_alive():
                self.after(100, self.xdsrunner_animate)
            else:
                self.stop_xdsrunner_animation()

    def stop_xdsrunner_animation(self) -> None:
        """
        Stop the refinement process animation and clear the canvas.
        """
        self.xdsrunner_animation_active = False
        self.xdsrunner_animation_canvas.delete("all")
        self.refresh_failed_list()
        self.refresh_list()

    def open_folder(self) -> None:
        """
        Open the folder of the selected dataset (single or failed mode).
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        if self.range_option_menu.get() == "Single":
            selected_option = self.single_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.relative_paths[selected_option]
        elif self.range_option_menu.get() == "Failed":
            selected_option = self.failed_file_option_menu.get()
            if selected_option in ["--", "all"]:
                return
            _path = self.failed_relative_paths[selected_option]
        else:
            return
        if is_wsl:
            subprocess.Popen(["explorer.exe", "."], cwd=_path)
        else:
            open_folder_linux(_path)


class MergeData(Page):
    """Class MergeData
    Handles merging datasets after filtering them using xdspicker.xlsx.

    Methods:
        __init__(parent): Initializes the MergeData page and sets up its GUI elements.
        run_xds_merge(): Calls the merge function to run XSCALE on the filtered data.
        run_xdsconv_shelx(): Generates .hkl and .p4p files for SHELX from merged data.
        show_result(): Displays partial content of XSCALE.LP focusing on output statistics.
        open_xscale_lp(): Opens the entire XSCALE.LP file in a separate window.
        run_filter(): Filters data by chosen criteria (I/Sigma, CC1/2, etc.) and generates xdspicker.xlsx.
        handle_option_select(event): Adjusts default filter values upon selecting a filter criterion.
        open_picker_xlsx(): Opens xdspicker.xlsx in LibreOffice or Explorer for manual editing.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the MergeData page and set up its GUI for filtering and merging data.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this page will be placed.
        """
        Page.__init__(self, parent)
        self.thread = {}
        self.sf = self.master.master.sf
        sp = 5 * self.sf ** 2.5
        self.input_path = ""  # Initialize input_path attribute, to be set elsewhere

        # Label for merging data instruction
        merge_data_label = tk.Label(self, text="Generate and Merge data from xdspicker.xlsx.", bg='white')
        merge_data_label.grid(row=0, column=0, sticky="w", padx=10, pady=(3 * sp, sp))

        tk.Label(self, text="Note: Average unit cell parameters will be used during merging. ",
                 bg='white', font=("Liberation Sans", int(14 * self.sf), "italic")).grid(
            row=1, column=0, sticky="w", padx=10, pady=(2 * sp, sp))

        xdspicker_label = tk.Label(self, text="I. Filter data for merging", bg='white')
        xdspicker_label.grid(row=2, column=0, sticky="w", padx=10, pady=(2 * sp, sp))

        # Row 1.1: Label for merging data instruction (row 2)
        row1_frame = tk.Frame(self, bg='white')
        row1_frame.grid(row=3, column=0, sticky="w", padx=10, pady=sp)

        tk.Label(row1_frame, text="Use the data with ", bg='white').pack(side="left", padx=(20, 5))

        self.option_var = tk.StringVar(self)
        self.option_var.set('--')  # default value
        options = ["--", "I/Sigma", "CC1/2", "R_meas", "Reso."]
        self.option_menu = ttk.Combobox(row1_frame, textvariable=self.option_var, values=options, state='readonly',
                                        width=10)
        self.option_menu.pack(side="left", padx=(5, 5))
        self.option_menu.bind('<<ComboboxSelected>>', self.handle_option_select)
        ToolTip(self.option_menu, "Choose a filter for initial data merging.")

        tk.Label(row1_frame, text="better than", bg='white').pack(side="left", padx=(5, 10))
        self.input_filter = tk.Entry(row1_frame, width=5)
        self.input_filter.pack(side="left")
        tk.Label(row1_frame, text="for merging.", bg='white').pack(side="left", padx=(10, 5))
        ToolTip(self.input_filter, "Use the default value or customise.")
        # Button to perform action based on selected option
        action_button = tk.Button(row1_frame, text="Filter Data", command=self.run_filter)
        action_button.pack(side="left", padx=(10, 20))
        ToolTip(action_button, "Generate \"xdspicker.xlsx\" for data merging.")
        # Manual Filter
        open_picker_button = tk.Button(row1_frame, text="Manually Filter", command=self.open_picker_xlsx)
        open_picker_button.pack(side="left", padx=15)
        ToolTip(open_picker_button, "Open \"xdspicker.xlsx\" to delete "
                                    "\nundesired data in excel / libreoffice.")

        merge_label = tk.Label(self, text="II. Merge Data", bg='white')
        merge_label.grid(row=4, column=0, sticky="w", padx=10, pady=(2 * sp, sp))

        row2_frame = tk.Frame(self, bg='white')
        row2_frame.grid(row=5, column=0, sticky="w", padx=10, pady=sp)
        merge_data_button = tk.Button(row2_frame, text="Merge Data", command=self.run_xds_merge)
        merge_data_button.pack(side="left", padx=20)
        ToolTip(merge_data_button, "Run XScale and merge data in \"merge\" subfolder.")
        # Inside Row 5: Button to show results
        show_result_button = tk.Button(row2_frame, text="Show Result", command=self.show_result)
        show_result_button.pack(side="left", padx=20)
        ToolTip(show_result_button, "Display statistic table from XSCALE.LP in \"merge\" subfolder.")
        # Inside Row 5: Button to open xscale.lp file
        open_xscale_lp_button = tk.Button(row2_frame, text="Open XSCALE.LP", command=self.open_xscale_lp)
        open_xscale_lp_button.pack(side="left", padx=20)
        ToolTip(open_xscale_lp_button, "Open XSCALE.LP of merged data in \"merge\" subfolder.")
        tk.Label(row2_frame, text="* Strongly recommend to cluster before", bg='white').pack(side="left", padx=(5, 5))
        bus2shelx_button = tk.Button(row2_frame, text="Bus to SHELX", command=self.run_xdsconv_shelx)
        bus2shelx_button.pack(side="left", padx=5)
        ToolTip(bus2shelx_button, "Generate hkl and p4p file on merged data.")

        # Row 6: Create an area to display the xscale.lp content
        self.result_text = tk.Text(self, wrap="word", height=15, font=("Liberation Mono", int(12 * self.sf)))
        self.result_scrollbar = tk.Scrollbar(self, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=self.result_scrollbar.set)
        self.result_text.grid(row=6, column=0, sticky="nsew", padx=10, pady=sp)
        self.result_scrollbar.grid(row=6, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def run_xds_merge(self) -> None:
        """
        Run XSCALE to merge filtered datasets. Executed in a separate thread.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        self.thread["merge"] = threading.Thread(target=xds_cluster.merge, args=(self.input_path,))
        self.thread["merge"].start()

    def run_xdsconv_shelx(self) -> None:
        """
        Generate .hkl and .p4p files for SHELX from the merged data.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        self.thread["xdsconv"] = threading.Thread(target=xds_shelx.convert_to_shelx, args=(self.input_path,))
        self.thread["xdsconv"].start()
        self.thread["report"] = threading.Thread(target=xds_report.create_html_file,
                                                 args=(os.path.join(self.input_path, "merge"), "cluster"))
        self.thread["report"].start()

    def show_result(self) -> None:
        """
        Display partial content of XSCALE.LP focusing on output statistics of merged data.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Define the path to the merge directory inside the input path
        merge_dir_path = os.path.join(self.input_path, "merge")

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(merge_dir_path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(merge_dir_path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            messagebox.showerror("Caution", "xscale.lp file not found in the merge directory.")
            return

        # Read the content of xscale.lp and extract the required part
        start_keyword = "SUBSET OF INTENSITY DATA"
        end_keyword = "STATISTICS OF INPUT DATA SET"
        content_to_display = ""
        capture = False

        with open(xscale_lp_path, "r") as file:
            for line in file:
                stripped_line = line.strip()  # Remove leading/trailing whitespace and special characters
                if start_keyword in stripped_line:
                    capture = True
                elif end_keyword in stripped_line:
                    break
                if capture:
                    content_to_display += line

        # Insert the extracted content into the Text widget
        self.result_text.delete("1.0", tk.END)  # Clear previous content
        self.result_text.insert("1.0", content_to_display)

    def open_xscale_lp(self) -> None:
        """
        Open the entire XSCALE.LP file in a separate window to inspect merged data statistics.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return

        # Define the path to the merge directory inside the input path
        merge_dir_path = os.path.join(self.input_path, "merge")

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(merge_dir_path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(merge_dir_path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            messagebox.showerror("Caution", "xscale.lp file not found in the merge directory.")
            return

        # Create a Toplevel window to display the content
        result_window = tk.Toplevel(self)
        result_window.title("Xscale.lp Content")
        result_window.geometry(
            f"{int(1200 * self.sf * self.sf)}x{int(600 * self.sf * self.sf)}")  # Adjust the size as needed

        # Create a Text widget with a Scrollbar
        text_widget = tk.Text(result_window, wrap="word", font=("Liberation Mono", int(11 * self.sf)))
        scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Grid the Text widget and Scrollbar in the Toplevel window
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        result_window.grid_columnconfigure(0, weight=1)
        result_window.grid_rowconfigure(0, weight=1)

        # Read the content of xscale.lp and insert it into the Text widget
        with open(xscale_lp_path, "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)

    def run_filter(self) -> None:
        """
        Filter data by chosen criteria (I/Sigma, CC1/2, etc.) and generate xdspicker.xlsx for merging.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        try:
            xdspicker_filter_value = float(self.input_filter.get())
        except:
            messagebox.showerror("Please enter some value in the filter.")
            return
        selected_option = self.option_var.get()
        keyword_dict = {'I/Sigma': 'isa', 'CC1/2': 'cc12', 'Reso.': 'reso', 'R_meas': 'rmeas'}
        if xdspicker_filter_value and selected_option in keyword_dict:
            self.thread["xds_picker"] = threading.Thread(
                target=xds_cluster.filter_data,
                args=(self.input_path, xdspicker_filter_value, keyword_dict[selected_option]))
            self.thread["xds_picker"].start()

    def handle_option_select(self, event: tk.Event) -> None:
        """
        Adjust default filter values upon selecting a filter criterion.

        Args:
            event (object): The Tkinter event object.
        """
        if self.option_var.get() == 'I/Sigma':
            replace_entry(self.input_filter, "5")
        elif self.option_var.get() == 'R_meas':
            replace_entry(self.input_filter, "50")
        elif self.option_var.get() == 'CC1/2':
            replace_entry(self.input_filter, "95")
        elif self.option_var.get() == 'Reso.':
            replace_entry(self.input_filter, "1.0")

    def open_picker_xlsx(self) -> None:
        """
        Open xdspicker.xlsx in LibreOffice or Explorer for manual editing of the filtered data list.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        if not os.path.exists(os.path.join(self.input_path, "xdspicker.xlsx")):
            shutil.copy(os.path.join(self.input_path, "xdsrunner2.xlsx"),
                        os.path.join(self.input_path, "xdspicker.xlsx"))
        excel_path = os.path.join(self.input_path, "xdspicker.xlsx")
        try:
            if is_wsl:
                # Use explorer.exe to open the file
                subprocess.call(["wsl.exe", "cmd.exe", "/C", f"start explorer.exe {linux_to_windows_path(excel_path)}"])
                return

            libreoffice_path = subprocess.run(["which", "libreoffice"], capture_output=True, text=True).stdout.strip()
            if libreoffice_path:
                subprocess.call(["libreoffice", "--calc", excel_path])
                return
        except Exception as e:
            messagebox.showerror("Caution", f"Error opening the form due to {e}.")
        messagebox.showerror("Caution", f"Neither LibreOffice nor Explorer is available.")


class Cluster_Output(Page):
    """Class Cluster_Output
    Manages intensity-based clustering results and related outputs.

    Methods:
        __init__(parent): Initializes the Cluster_Output page.
        run_clustering(): Extracts dendrogram and sets cutoff distance from user interaction.
        update_distance(distance): Callback that updates the distance entry after dendrogram interaction.
        disable_set_distance_button(): Disables the dendrogram-related button.
        enable_set_distance_button(): Enables the dendrogram-related button.
        open_graph(): Generates and displays the dendrogram in a popup.
        generate_and_display_dendrogram(var): Generates dendrogram in a thread and displays on completion.
        show_image_popup(image_path): Shows the dendrogram image in a popup window.
        open_html(): Opens the HTML report for a chosen cluster.
        make_clusters(): Creates clusters using a specified cutoff distance and runs XSCALE on them.
        update_path_dict(output=False): Refreshes and displays the list of clusters and their statistics.
        run_xprep(): Runs XPREP on the chosen cluster if configured.
        on_cryo_checkbox_change(): Updates temperature field if cryo conditions are toggled.
        update_metadata(): Updates .ins and .cif_od files with metadata.
        output_p4p_option(event): Prints information about the selected cluster option.
        open_folder(): Opens the folder corresponding to the selected cluster.
    """

    def __init__(self, parent: tk.Frame) -> None:
        """
        Initialize the Cluster_Output page for intensity-based clustering and merging.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this page will be placed.
        """

        super().__init__(parent)
        self.sf = self.master.master.sf
        self.thread = {}
        self.p4p_path_dict = {}
        sp = 5 * self.sf ** 2.5
        self.input_path = ""  # Initialize input_path attribute, to be set elsewhere

        # Row 1.1: Label for clustering
        merge_data_label = tk.Label(self, text="Intensity-Cluster based on Correlation Coefficients in XSCALE.LP",
                                    bg='white')
        merge_data_label.grid(row=0, column=0, sticky="w", padx=10, pady=(3 * sp, sp))

        merge_distance_label = tk.Label(self, text="The distance can either gather from the Dendrogram"
                                                   " or manually input.",
                                        font=("Liberation Sans", int(14 * self.sf), "italic"), bg='white')
        merge_distance_label.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=sp)

        # Row 1.2: Frame containing buttons for clustering
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=2, column=0, sticky="w", padx=10, pady=sp)

        set_distance_button = tk.Button(buttons_frame, text="Set Distance from Dendrogram", command=self.run_clustering)
        set_distance_button.pack(side="left", padx=15)
        ToolTip(set_distance_button, "Set the cut-off distance from the dendrogram.")
        distance_label = tk.Label(buttons_frame, text="Distance", bg='white')
        distance_label.pack(side="left", padx=10)
        self.input_distance = tk.Entry(buttons_frame, width=7)
        self.input_distance.pack(side="left")
        replace_entry(self.input_distance, "1.0")
        ToolTip(self.input_distance, "Distance used for clustering.")

        self.overwrite = tk.BooleanVar(value=True)
        id_overwrite_checkbox = tk.Checkbutton(buttons_frame, variable=self.overwrite, bg='white')
        id_overwrite_checkbox.pack(side="left", padx=(20, 10))
        id_overwrite_checkbox_label = tk.Label(buttons_frame, text="Overwrite previous result", bg='white')
        id_overwrite_checkbox_label.pack(side="left")
        ToolTip(id_overwrite_checkbox, "If ticked, existed cluster folders will be overwrote.")

        merge_data_button = tk.Button(buttons_frame, text="Make Cluster based on Distance", command=self.make_clusters)
        merge_data_button.pack(side="left", padx=15)
        ToolTip(merge_data_button, "Use the input distance for cluster making and data merging")

        # Row 2.1: Label for clustering
        process_label = tk.Label(self,
                                 text=r"Process Clusters and Generate .INS",
                                 bg='white', )
        process_label.grid(row=4, column=0, sticky="w", padx=10, pady=(8 * sp, 1 * sp))
        shelx_label = tk.Label(self,
                               text="Press Refresh to view the information of all clusters. "
                                    "Run XPREP will raise XPREP in Windows. Set the XPREP path in `setting.ini` first!",
                               bg='white', font=("Liberation Sans", int(14 * self.sf), "italic"))
        shelx_label.grid(row=5, column=0, sticky="w", padx=(20, 10), pady=(1 * sp, 1 * sp))

        # Row 2.2 Load data
        row22_frame = tk.Frame(self, bg='white')
        row22_frame.grid(row=6, column=0, sticky="w", padx=10, pady=sp)

        row22_label1 = tk.Label(row22_frame, text="Data Processing Based on",
                                bg='white')
        row22_label1.pack(side="left", padx=15)

        self.p4p_option_var = tk.StringVar(self)
        self.p4p_option_var.set('--')  # default value
        self.p4p_options = ["--"]
        self.p4p_option_menu = ttk.Combobox(row22_frame, textvariable=self.p4p_option_var, values=self.p4p_options,
                                            state='readonly', width=20)
        self.p4p_option_menu.bind('<<ComboboxSelected>>', self.output_p4p_option)
        self.p4p_option_menu.pack(side="left", padx=(5, 5))
        ToolTip(self.p4p_option_menu, "Choose the cluster to work with.")

        refresh_button = tk.Button(row22_frame, text="Refresh and Show Summary",
                                   command=lambda: self.update_path_dict(output=True))
        refresh_button.pack(side="left", padx=25)
        ToolTip(refresh_button, "Refresh and show clusters summary in the command window.")

        # Row 2.3 Load data
        row23_frame = tk.Frame(self, bg='white')
        row23_frame.grid(row=7, column=0, sticky="w", padx=10, pady=3 * sp)
        open_graph_button = tk.Button(row23_frame, text="Open Dendrogram", command=self.open_graph)
        open_graph_button.pack(side="left", padx=20)
        ToolTip(open_graph_button, "Show the dendrogram of current clusters.")
        open_scale_button = tk.Button(row23_frame, text="Open XSCALE.LP", command=self.open_xscale_lp)
        open_scale_button.pack(side="left", padx=20)
        ToolTip(open_scale_button, "Open XSCALE.LP of current clusters.")
        run_xprep_button = tk.Button(row23_frame, text="Run XPREP", command=self.run_xprep)
        run_xprep_button.pack(side="left", padx=20)
        ToolTip(run_xprep_button, "Run XPREP of the chosen cluster to generate shelx .ins file.")
        open_html_button = tk.Button(row23_frame, text="Open Report", command=self.open_html)
        open_html_button.pack(side="left", padx=20)
        ToolTip(open_html_button, "Generate and Open the web report on current working data.")

        # Row 3.1 Metadata Process
        CIF_label = tk.Label(self,
                             text=r"Collect and Generate Metadata File",
                             bg='white', )
        CIF_label.grid(row=8, column=0, sticky="w", padx=10, pady=(8 * sp, 1 * sp))
        metadata_label = tk.Label(self,
                                  text="Metadata will be updated with provided information and headers in .img file,"
                                       " and saved in the .CIF_OD file. Olex2 will pick it up automatically.",
                                  bg='white', font=("Liberation Sans", int(14 * self.sf), "italic"))
        metadata_label.grid(row=9, column=0, sticky="w", padx=(20, 10), pady=1 * sp)
        tk.Label(self, text="The compound name in short should be only one word.",
                 bg='white', font=("Liberation Sans", int(14 * self.sf), "italic")).grid(
            row=10, column=0, sticky="w", padx=(20, 10), pady=(0, 2 * sp))

        # Row 3.2 Metadata Process
        row32_frame = tk.Frame(self, bg='white')
        row32_frame.grid(row=11, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row32_frame, text="Instrument Profile:", bg='white').grid(column=0, padx=(15, 5))
        self.ins_option_var = tk.StringVar(self)
        self.ins_option_var.set('--')  # default value
        self.ins_path_dict = self.load_instrument_profile()
        ins_options = ["--"] + list(self.ins_path_dict.keys())
        self.ins_option_menu = ttk.Combobox(row32_frame, textvariable=self.ins_option_var, values=ins_options,
                                            state='readonly', width=25)
        self.ins_option_menu.grid(row=0, column=5, padx=(20, 10), sticky="w")
        self.ins_option_menu.bind('<<ComboboxSelected>>', self.load_instrument_parameter)
        ToolTip(self.ins_option_menu, "Default Instrument Profile can be loaded.")

        # Row 3.3 Metadata Process
        row33_frame = tk.Frame(self, bg='white')
        row33_frame.grid(row=12, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row33_frame, text="TEM Instrument Name", bg='white').pack(side="left", padx=(15, 5))
        self.instrument = tk.Entry(row33_frame, width=15)
        self.instrument.pack(side="left")
        tk.Label(row33_frame, text="Detector Name", bg='white').pack(side="left", padx=(15, 5))
        self.detector = tk.Entry(row33_frame, width=15)
        self.detector.pack(side="left")
        tk.Label(row33_frame, text="Temperature", bg='white').pack(side="left", padx=(15, 5))
        self.temperature = tk.Entry(row33_frame, width=5)
        self.temperature.pack(side="left")
        tk.Label(row33_frame, text="K", bg='white').pack(side="left", padx=(5, 5))
        self.is_cryo = tk.BooleanVar(value=True)
        is_cryo_checkbox = tk.Checkbutton(row33_frame, variable=self.is_cryo,
                                          command=self.on_cryo_checkbox_change, bg='white')
        is_cryo_checkbox.pack(side="left", padx=(10, 10))
        is_cryo_checkbox_label = tk.Label(row33_frame, text="Cryoholder", bg='white')
        is_cryo_checkbox_label.pack(side="left")
        replace_entry(self.temperature, "100")

        row34_frame = tk.Frame(self, bg='white')
        row34_frame.grid(row=13, column=0, sticky="w", padx=10, pady=2 * sp)
        tk.Label(row34_frame, text="Compound Name\t Short Name:", bg='white').pack(side="left", padx=(15, 5))
        self.short_name = tk.Entry(row34_frame, width=15)
        self.short_name.pack(side="left")
        tk.Label(row34_frame, text="  Long Name:", bg='white').pack(side="left", padx=(15, 5))
        self.long_name = tk.Entry(row34_frame, width=25)
        self.long_name.pack(side="left")

        ToolTip(self.instrument, "The name of the microscope")
        ToolTip(self.detector, "The name of the detector")
        ToolTip(self.temperature, "Data collection temperature")
        ToolTip(is_cryo_checkbox, "Tick if cryoholder is used.")
        ToolTip(self.short_name, "One-word name for your compound")
        ToolTip(self.long_name, "Whole name for your compound")

        row35_frame = tk.Frame(self, bg='white')
        row35_frame.grid(row=14, column=0, sticky="w", padx=10, pady=2 * sp)
        update_metadata_button = tk.Button(row35_frame, text="Update INS and Metadata",
                                           command=self.update_metadata)
        update_metadata_button.pack(side="left", padx=20)
        open_folder_button = tk.Button(row35_frame, text="Open Folder",
                                       command=self.open_folder)
        open_folder_button.pack(side="left", padx=20)
        ToolTip(update_metadata_button, "Generate .CIF_OD containing metadata and data reduction detail.")
        ToolTip(open_folder_button, "Open the folder of selected cluster.")

    @classmethod
    def load_instrument_profile(cls) -> dict:
        """
        Class method to load and return a dictionary of instrument profile file paths.

        Returns:
            dict: A dictionary where keys are file names and values are the respective
            file paths.
        """
        _path_dict = {}
        _file_path = os.path.join(script_dir, "instrument_profile")
        _files_list = sorted([f for f in os.listdir(_file_path) if os.path.isfile(os.path.join(_file_path, f))])
        for f in _files_list:
            if f != "__init__.py":
                _path_dict[f] = os.path.join(_file_path, f)
        return _path_dict

    def open_xscale_lp(self) -> None:
        """
        Opens and displays the content of an `xscale.lp` file located in the specified path.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return
        path = self.p4p_path_dict[var]

        # Path to xscale.lp file
        xscale_lp_path = None
        for file in os.listdir(path):
            if file.lower() == 'xscale.lp':
                xscale_lp_path = os.path.join(path, file)
                break

        if not xscale_lp_path or not os.path.exists(xscale_lp_path):
            messagebox.showerror("Caution", "xscale.lp file not found in the merge directory.")
            return

        # Create a Toplevel window to display the content
        result_window = tk.Toplevel(self)
        result_window.title("Xscale.lp Content")
        result_window.geometry(
            f"{int(1200 * self.sf * self.sf)}x{int(600 * self.sf * self.sf)}")  # Adjust the size as needed

        # Create a Text widget with a Scrollbar
        text_widget = tk.Text(result_window, wrap="word", font=("Liberation Mono", int(11 * self.sf)))
        scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Grid the Text widget and Scrollbar in the Toplevel window
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid layout for auto resizing
        result_window.grid_columnconfigure(0, weight=1)
        result_window.grid_rowconfigure(0, weight=1)

        # Read the content of xscale.lp and insert it into the Text widget
        with open(xscale_lp_path, "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)

    def load_instrument_parameter(self, event: tk.Event) -> None:

        """
            Loads instrument parameters based on the selected dropdown option and updates the corresponding entries
            in the graphical interface.
            """
        selected_option = self.ins_option_var.get()
        if selected_option in ["--"]:
            return 0
        print(f"Reading Instrument Parameter: {selected_option}")
        file_path = self.ins_path_dict[selected_option]
        try:
            with open(file_path, "r") as file:
                parameters = json.load(file)
                replace_entry(self.instrument, parameters["instrument"])
                replace_entry(self.detector, parameters["detector"])
        except FileNotFoundError:
            messagebox.showerror("Caution", "Error: The file does not exist.")

    def run_clustering(self) -> None:
        """
        Extract the dendrogram and allow user interaction to select a cutoff distance.
        """
        if not self.input_path:
            messagebox.showwarning("Input Path Missing", "Please select an input path first.")
            return

        merge_path = os.path.join(self.input_path, "merge")
        if not os.path.exists(merge_path):
            messagebox.showerror("Merge Directory Missing", f"The directory '{merge_path}' does not exist.")
            return

        # Disable the button to prevent multiple clicks
        self.disable_set_distance_button()

        # Define the callback function using partial to pass self
        callback_with_self = partial(self.update_distance)

        # Call extract_dendrogram in interactive mode
        xds_cluster.extract_dendrogram(
            input_path=merge_path,
            interactive=True,
            callback=callback_with_self
        )

    def update_distance(self, distance: float) -> None:
        """
        Update the distance entry after dendrogram interaction.

        Args:
            distance (float): The selected cutoff distance from the dendrogram.
        """
        if distance is not None:
            replace_entry(self.input_distance, f"{distance:.4f}")
        else:
            messagebox.showerror("Error", "Failed to extract cutoff distance.")

        # Re-enable the button
        self.enable_set_distance_button()

    def disable_set_distance_button(self) -> None:
        """
        Disable the 'Set Distance from Dendrogram' button to prevent multiple calls.
        """
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and child['text'] == "Set Distance from Dendrogram":
                        child.config(state=tk.DISABLED)

    def enable_set_distance_button(self) -> None:
        """
        Enable the 'Set Distance from Dendrogram' button after interaction completes.
        """
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and child['text'] == "Set Distance from Dendrogram":
                        child.config(state=tk.NORMAL)

    def open_graph(self) -> None:
        """
        Generate and display the dendrogram image in a popup, running in a separate thread.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return

        # Start a new thread to generate the dendrogram
        thread = threading.Thread(target=self.generate_and_display_dendrogram, args=(var,), daemon=True)
        thread.start()

    def generate_and_display_dendrogram(self, var: str) -> None:
        """
        Generate dendrogram image and display it in a popup upon completion.

        Args:
            var (str): The selected cluster or 'merge' key.
        """
        try:
            # Generate the dendrogram (this might take time)
            xds_cluster.extract_dendrogram(self.p4p_path_dict[var], interactive=False)

            # Path to the generated image
            image_path = os.path.join(self.p4p_path_dict[var], "dendrogram.png")

            # Check if the image was created successfully
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Dendrogram image not found at {image_path}")

            # Schedule the display of the image in the main thread
            self.master.after(0, lambda: self.show_image_popup(image_path))

        except Exception as e:
            # Handle exceptions and show error message in the main thread
            self.master.after(0, lambda: messagebox.showerror("Error", str(e)))

    def show_image_popup(self, image_path: str) -> None:
        """
        Show the dendrogram image in a popup window.

        Args:
            image_path (str): The path to the dendrogram image file.
        """
        popup = Toplevel(self.master)
        popup.title("Dendrogram")
        popup.resizable(True, True)

        try:
            # Open the image using PIL
            img = Image.open(image_path)
            photo = ImageTk.PhotoImage(img)
            label = Label(popup, image=photo)
            label.image = photo  # Keep a reference to prevent garbage collection
            label.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            popup.destroy()

    def open_html(self) -> None:
        """
        Open the HTML report for the selected cluster or merged data.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return
        xds_report.open_html_file(self.p4p_path_dict[var], "cluster")

    def make_clusters(self) -> None:
        """
        Create clusters using the specified cutoff distance and run XSCALE on them.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        distance = float(self.input_distance.get())
        overwrite = self.overwrite.get()
        self.thread["cluster_maker"] = threading.Thread(target=xds_cluster.make_cluster,
                                                        args=(self.input_path, distance, overwrite))
        self.thread["cluster_maker"].start()

    def update_path_dict(self, output: bool = False) -> None:
        """
        Refresh and display the list of clusters and their statistics.

        Args:
            output (bool): If True, print cluster summary to command output.
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.p4p_path_dict = {}
        self.p4p_options = ["--"]
        merge_folder_path = os.path.join(self.input_path, "merge")

        if not os.path.isdir(merge_folder_path):
            for root, dirs, files in os.walk(self.input_path):
                for dir_name in dirs:
                    if "cluster" in dir_name or "iter" in dir_name or "cls" in dir_name:
                        merge_folder_path = root
                        break

        for item in os.listdir(merge_folder_path):
            item_path = os.path.join(merge_folder_path, item)
            if os.path.isdir(item_path) and ('cluster' in item_path.lower() or "iter" in item_path.lower() or 'cls' in item_path.lower()):
                self.p4p_path_dict[item] = item_path
            elif os.path.isfile(item_path) and item.lower().endswith('.p4p'):
                self.p4p_path_dict["merge"] = merge_folder_path

        self.p4p_path_dict = {key: self.p4p_path_dict[key]
                              for key in sorted(self.p4p_path_dict.keys(), key=natural_sort_key)}
        self.p4p_options += list(self.p4p_path_dict.keys())
        self.p4p_option_menu['values'] = self.p4p_options
        self.p4p_option_var.set('--')  # Reset to default

        if output:
            columns = ["Cluster", "#Datasets", "Completeness", "Redundancy", "Resolution", "ISa",
                       "CC1/2", "R_meas"]
            results_df = pd.DataFrame(columns=columns)
            reso_report = None
            for key, path in self.p4p_path_dict.items():
                if not os.path.isfile(os.path.join(path, "all.HKL")):
                    continue
                result_dict = xds_analysis.extract_cluster_result(path)
                if result_dict:
                    result = [key, len(result_dict.get("input", [])),
                              result_dict.get("completeness", 0.0),
                              "{:.2f}".format(result_dict.get("N_obs", 0) / result_dict.get("N_uni", 1)),
                              result_dict.get("resolution", 5.0),
                              result_dict.get("ISa_meas", 5.0),
                              result_dict["cc12_reso"] if "cc12_reso" in result_dict else result_dict.get("CC1/2", 0.0),
                              result_dict["rmeas"] if "rmeas" in result_dict else result_dict.get("R_meas", 0.0)]
                    new_row = pd.DataFrame([result], columns=columns)
                    results_df = pd.concat([results_df, new_row], ignore_index=True)
                    reso_report = result_dict.get("merge_resolution", None)
            headers = ["Cluster", "#Set.", "Complete.", "Redun.", "Reso.", "ISa",
                       "CC1/2", "R_meas"]
            col_widths = [15, 5, 9, 6, 6, 6, 6, 6]
            # Formatting the header
            header_str = "  ".join(f"{header:<{width}}" for header, width in zip(headers, col_widths))
            # Formatting the rows
            row_strs = []
            for index, row in results_df.iterrows():
                row_strs.append("  ".join(f"{str(val):<{width}}" for val, width in zip(row, col_widths)))
            # Combining everything into a formatted table
            table = f"  {header_str}\n{'-' * (len(header_str) + 2)}\n  " + "\n  ".join(row_strs)
            # Adding the title
            title = ("\nList of Clusters (Abbr. = Datasets, Completeness, Redundancy, Resolution):\n" +
                     ("\n" if analysis_engine == "XDS" else f"Completeness calculates based on {reso_report} A\n\n"))
            print(title + table + "\n")

    def run_xprep(self) -> None:
        """
        Run XPREP on the chosen cluster if configured.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return
        xprep_path = "\"{}\"".format(config["General"]["xprep_location"]) if config["General"][
            "xprep_location"] else "xprep"

        def run_command(xprep, directory):
            print(f"\nRun XPREP under {directory}.\n")
            command = f'cmd.exe /c {xprep} 1' if is_wsl else "xprep 1"
            os.chdir(directory)
            os.system(command)

        command_thread = threading.Thread(target=run_command, args=(xprep_path, self.p4p_path_dict[var]))
        command_thread.start()

    def on_cryo_checkbox_change(self) -> None:
        """
        Update the temperature field if cryo conditions are toggled.
        """
        if self.is_cryo.get():
            replace_entry(self.temperature, "100")
        else:
            replace_entry(self.temperature, "298")

    def update_metadata(self) -> None:
        """
        Update .ins and .cif_od files with metadata for the chosen cluster.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return
        ins_path = self.p4p_path_dict[var]
        print()
        ins_files = glob.glob(os.path.join(ins_path, "*.ins"))
        pcf_files = glob.glob(os.path.join(ins_path, "*.pcf"))
        if ins_files and pcf_files:
            newest_ins_file = max(ins_files, key=os.path.getmtime)
            newest_pcf_file = max(pcf_files, key=os.path.getmtime)
            xds_analysis.collect_metadata(self.input_path)
            info_dict = {
                "detector": self.detector.get(),
                "instrument": self.instrument.get(),
                "temperature": self.temperature.get(),
                "short_name": self.short_name.get(),
                "long_name": self.long_name.get()
            }
            update_thread = threading.Thread(target=xds_shelx.update_after_prep,
                                             args=(self.input_path, newest_ins_file, newest_pcf_file, info_dict))
            update_thread.start()
            if self.short_name.get():
                if " " in self.short_name.get():
                    short_name = self.short_name.get()[0]
                else:
                    short_name = info_dict.get("short_name", "1")
                old_hkl_path = newest_ins_file[:-3] + "hkl"
                new_hkl_path = os.path.join(os.path.dirname(newest_ins_file), short_name + ".hkl")
                if old_hkl_path != new_hkl_path:
                    shutil.copy(old_hkl_path, new_hkl_path)
            messagebox.showinfo("Info", "The INS file is updated and data reduction information is within cif_od file.")
        else:
            messagebox.showerror("Caution", "XPREP needs to run before implementing metadata.")

    def output_p4p_option(self, event: tk.Event) -> None:
        """
        Print information about the selected cluster option when changed.

        Args:
            event (object): The Tkinter event object.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            return
        print(f"Process on {self.p4p_path_dict[var]}.")

    def open_folder(self) -> None:
        """
        Open the folder of the selected cluster.
        """
        var = self.p4p_option_var.get()
        if var == "--":
            if self.input_path:
                if messagebox.askyesno("Caution", "Do you want to open the root folder?"):
                    subprocess.Popen(["explorer.exe", "."], cwd=self.input_path) if is_wsl \
                        else open_folder_linux(self.input_path)
        elif is_wsl:
            subprocess.Popen(["explorer.exe", "."], cwd=self.p4p_path_dict[var])
        else:
            open_folder_linux(self.p4p_path_dict[var])
