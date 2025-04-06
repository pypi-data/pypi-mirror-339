"""RealTime Module

This module provides the `RealTime` class, a graphical user interface (GUI) component for the AutoLEI application. The
`RealTime` class facilitates real-time processing and monitoring of MicroED (Micro Electron Diffraction) data,
integrating functionalities such as data collection status updates, live statistics visualization, and interaction
with other AutoLEI modules for data reduction and clustering.

Features:
    - **Real-Time Data Monitoring**: Continuously monitors data collection folders to update processing statuses.
    - **Live Statistics Visualization**: Displays real-time graphs for resolution, completeness, CC1/2, and ISa metrics.
    - **Interactive Plot Annotations**: Provides interactive cursors on plots for detailed dataset information.
    - **Strategy Configuration**: Allows users to load and edit processing strategies through a GUI.
    - **Process Control**: Enables starting and stopping of real-time data processing threads.
    - **Report Access**: Facilitates opening of cluster reports and current `XSCALE.LP` files directly from the GUI.
    - **File Management**: Supports conversion of image formats, generation of REDp and PETS input files, and rollback
        of `XDS.INP` files to specific processing stages.

Classes:
    RealTime:
        A GUI component for real-time processing and monitoring of MicroED data within the AutoLEI application.

Dependencies:
    Standard Libraries:
        - hashlib
        - json
        - math
        - os
        - re
        - shutil
        - subprocess
        - sys
        - threading
        - time
        - warnings
    Third-Party Libraries:
        - tkinter
        - matplotlib
        - mplcursors
        - pandas
    Custom Modules:
        - image_io
        - xds_input
        - xds_runner
        - xds_analysis
        - analysis_hkl
        - xds_report
        - xds_cluster
        - util (various utility functions)

Contact:
    - Lei Wang: lei.wang@mmk.su.se
    - Yinlin Chen: yinlin.chen@mmk.su.se

License:
    BSD 3-Clause License
"""

from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import hashlib
import mplcursors
import json
import time
import pandas as pd

try:
    from .src import image_io, xds_input, xds_runner, xds_analysis, analysis_hkl, xds_report, xds_cluster
    from .src.util import *
except ImportError:
    from src import image_io, xds_input, xds_runner, xds_analysis, analysis_hkl, xds_report, xds_cluster
    from src.util import *

is_wsl = is_wsl()


class RealTime(Page):
    class RealTime(Page):
        """
        The RealTime class is a GUI component for monitoring and processing real-time MicroED data.

        This class provides functionality for real-time data collection, live visualizations,
        and data processing, including features such as strategy configuration, cluster report handling,
        and file management.

        Methods:
            - __init__(parent): Initializes the RealTime GUI components and variables.
            - update_plots(): Updates the displayed charts with the latest dataset statistics.
            - load_strategy(event): Loads or edits strategy configurations when triggered by user interaction.
            - write_default_strategy(): Writes a default strategy configuration file.
            - text_edit(file_path): Opens an editable text file interface for strategy or parameter files.
            - get_md5(cls, file_path): Computes and returns the MD5 checksum of a file.
            - convert_image(key): Converts MRC images to SMV format.
            - run_data_reduction(run_dict): Processes folders through states like collection, transfer, or ready state.
            - update_status_initial(): Initializes or updates the status dictionary for monitoring real-time data.
            - update_status_dict(_status_dict, initial): Updates the status dictionary with detected folder statuses.
            - meet_criteria(statistics): Evaluates dataset statistics to see if criteria are met based on strategy rules
            - update_display_initial(): Displays initial merged status or configuration from input data.
            - update_display(output): Updates the GUI with the latest dataset and processing results.
            - run_cluster(): Triggers merging and clustering analysis for good datasets.
            - monitor_folder(): Monitors the input folder, managing collection and data reduction.
            - stop_running(): Stops the folder monitoring and all active threads safely.
            - make_picker_excel(path): Generates an Excel file listing information about good datasets in the cluster.
            - run_realtime_microed(): Starts the real-time monitoring and data reduction process.
            - start_realtime_microed_animation(): Begins a canvas animation indicating the processing state.
            - realtime_microed_animate(): Handles the logic for animating the canvas during real-time processing.
            - stop_realtime_microed_animation(): Stops the animated canvas for the processing state.
            - open_report(): Opens the web-based cluster report results for the latest merged cluster.
            - open_current_xscale_lp(): Opens and displays the XSCALE.LP file contents of the current cluster.
        """

    def __init__(self, parent: tk.Widget):
        """
        Attributes:
        parent (tk.Widget): Parent widget to which this component belongs.
        P1 (bool): A boolean variable initialized as False.
        cursors (list): An empty list intended for managing cursors.
        run_bool (bool): A boolean indicating the running state of the system, initialized as False.
        reso_limit (Any): Resolution limit input, defaulted to None.
        realtime_json (Any): JSON data for real-time processing, defaulted to None.
        name (Any): Name of the session, defaulted to None.
        sg (Any): Space group input, defaulted to None.
        cell (Any): Unit cell parameters, defaulted to None.
        realtime_microed_animation_active (bool): Indicates if the real-time MicroED animation is active, defaulted to
                                                  False.
        status_dict (dict): A dictionary to store the status of data processing, defaulted to an empty dictionary.
        good_set (dict): A dictionary to track datasets that meet quality criteria, defaulted to an empty dictionary.
        thread (dict): A dictionary for managing threads, initialized as empty.
        entry (dict): A dictionary for storing input fields' Tkinter entry widgets, initialized as empty.
        sf (Any): Scale factor derived from the parent UI, shared across widgets.
        input_path (str): Path of the input file, defaulted to an empty string.
        realtime_current_average_unit_cell (str): Status of the current average unit cell, defaulted to "Waiting...".
        strategy_option_var (tk.StringVar): Variable for filter strategy selection in the UI.
        strategy_options (list): A list of available filter strategy options.
        is_beam_stop (tk.BooleanVar): Indicates whether the beam stop is being used.
        do_correct (tk.BooleanVar): Indicates whether to correct the XDS.INP based on image headers.
        running_summary (tk.Entry): Tkinter Entry widget for displaying the running summary.
        last_status (tk.Entry): Tkinter Entry widget for displaying the last run status.
        completeness_display (tk.Entry): Tkinter Entry widget for overall completeness under given resolution.
        resolution_display (tk.Entry): Tkinter Entry widget for overall resolution display.
        cc12_display (tk.Entry): Tkinter Entry widget for overall CC1/2 display.
        realtime_microed_animation_canvas (tk.Canvas): Tkinter Canvas widget for displaying real-time MicroED animation.
        realtime_microed_animation_angle (int): Angle used for animation rotation, defaulted to 0.
        """
        Page.__init__(self, parent)
        self.P1 = False
        self.cursors = []
        self.run_bool = False
        self.reso_limit = self.realtime_json = self.name = self.sg = self.cell = None
        self.realtime_microed_animation_active = False
        self.status_dict = {}
        self.good_set = {}
        self.thread = {}
        self.entry = {}
        self.sf = self.master.master.sf
        sp = 5 * self.sf ** 2.5
        self.input_path = ""  # Initialize input_path attribute

        # Initialize variables with "Waiting"
        self.realtime_current_average_unit_cell = "Waiting..."

        # Row 1: Label for realtime MicroED data processing
        introduce_label = tk.Label(self,
                                   text="RealTime MicroED data processing, compatible for EPU-D and Instamatic. "
                                        "Load the path and Save Parameters before continuing!",
                                   bg='white')
        introduce_label.grid(row=0, column=0, sticky="w", padx=10, pady=(3 * sp, sp))

        # Row 2: Note about saving input parameters and unit cell information
        note_label = tk.Label(self, text="Basic Information:",
                              font=("Liberation Sans", int(16 * self.sf), "bold"), bg='white')
        note_label.grid(row=1, column=0, sticky="w", padx=10, pady=(2 * sp, sp))

        input_frame = tk.Frame(self, bg='white')
        input_frame.grid(row=2, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        tk.Label(input_frame, text="Name:", bg='white').pack(side="left", padx=(25, 10))
        self.entry["name"] = tk.Entry(input_frame, width=10)
        self.entry["name"].pack(side="left")
        tk.Label(input_frame, text="Unit Cell:", bg='white').pack(side="left", padx=(25, 10))
        self.entry["cell"] = tk.Entry(input_frame, width=40)
        self.entry["cell"].pack(side="left")
        tk.Label(input_frame, text="Space Group:", bg='white').pack(side="left", padx=(25, 10))
        self.entry["sg"] = tk.Entry(input_frame, width=7)
        self.entry["sg"].pack(side="left")

        ToolTip(self.entry["name"], "One-Word Session Name.")
        ToolTip(self.entry["cell"], "Unit cell parameters, can be segmented by space or \", \" (space after comma)."
                                    "\nTo run RealTime in Screen Mode, leave it BLANK.")
        ToolTip(self.entry["sg"], "Space Group Number (1-230)"
                                  "\nTo run RealTime in Screen Mode, leave it BLANK.")

        strategy_frame = tk.Frame(self, bg='white')
        strategy_frame.grid(row=3, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        tk.Label(strategy_frame, text="Resolution Limit:", bg='white').pack(side="left", padx=(25, 10))
        self.entry["reso"] = tk.Entry(strategy_frame, width=5)
        self.entry["reso"].pack(side="left")
        tk.Label(strategy_frame, text="Filter Strategy:", bg='white').pack(side="left", padx=(25, 10))
        self.strategy_option_var = tk.StringVar(self)
        self.strategy_option_var.set('--')  # default value
        self.strategy_options = ["--", "default", "edit"]
        self.ins_option_menu = ttk.Combobox(strategy_frame, textvariable=self.strategy_option_var,
                                            values=self.strategy_options, state='readonly', width=10)
        self.ins_option_menu.pack(side="left", padx=20)
        self.ins_option_menu.bind('<<ComboboxSelected>>', self.load_strategy)
        self.is_beam_stop = tk.BooleanVar(value=False)
        is_beam_stop_checkbox = tk.Checkbutton(strategy_frame, variable=self.is_beam_stop, bg='white')
        is_beam_stop_checkbox.pack(side="left", padx=(20, 10))
        is_beam_stop_checkbox_label = tk.Label(strategy_frame, text="Beam Stop Used", bg='white')
        is_beam_stop_checkbox_label.pack(side="left")
        self.do_correct = tk.BooleanVar(value=True)
        do_correct_checkbox = tk.Checkbutton(strategy_frame, variable=self.do_correct, bg='white')
        do_correct_checkbox.pack(side="left", padx=(20, 10))
        do_correct_checkbox_label = tk.Label(strategy_frame, text="Correct Input", bg='white')
        do_correct_checkbox_label.pack(side="left")

        ToolTip(self.entry["reso"], "Resolution for reporting completeness and CC1/2."
                                    "\nTo run RealTime in Screen Mode, leave it BLANK.")
        ToolTip(self.ins_option_menu, "Change the cycle / waiting time or criteria for good data.")
        ToolTip(is_beam_stop_checkbox, "Tick if you have USED beam stop.")
        ToolTip(do_correct_checkbox, "Tick if you want to correct XDS.INP with image header.")

        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=4, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        realtime_button = tk.Button(buttons_frame, text="RealTime MicroED", command=self.run_realtime_microed)
        realtime_button.pack(side="left", padx=15)
        stop_realtime_button = tk.Button(buttons_frame, text="Stop Run", command=self.stop_running)
        stop_realtime_button.pack(side="left", padx=15)

        ToolTip(realtime_button, "Run the RealTime function on the working directory.")
        ToolTip(stop_realtime_button, "Stop the RealTime function after current cycle.")

        self.realtime_microed_animation_canvas = tk.Canvas(buttons_frame, width=400, height=20, bg='white',
                                                           highlightthickness=0)
        self.realtime_microed_animation_canvas.pack(side="left", padx=10)
        self.realtime_microed_animation_active = False
        self.realtime_microed_animation_angle = 0

        result_label = tk.Label(self, text="Current Result:",
                                font=("Liberation Sans", int(16 * self.sf), "bold"), bg='white')
        result_label.grid(row=5, column=0, sticky="w", padx=10, pady=(2 * sp, sp), )

        # Row 5: Refresh button and animation
        result1_frame = tk.Frame(self, bg='white')
        result1_frame.grid(row=6, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        tk.Label(result1_frame, text="Running Summary:", bg='white').pack(side="left", padx=(25, 10))
        self.running_summary = tk.Entry(result1_frame, width=10)
        self.running_summary.pack(side="left")
        tk.Label(result1_frame, text="(Good / Processable / All)      Status of Last Run:",
                 bg='white').pack(side="left", padx=(15, 15))
        self.last_status = tk.Entry(result1_frame, width=30)
        self.last_status.pack(side="left")

        result2_frame = tk.Frame(self, bg='white')
        result2_frame.grid(row=7, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        tk.Label(result2_frame, text="Overall Completeness:", bg='white').pack(side="left", padx=(25, 10))
        self.completeness_display = tk.Entry(result2_frame, width=8)
        self.completeness_display.pack(side="left")
        tk.Label(result2_frame, text="under Resolution of ",
                 bg='white').pack(side="left", padx=(10, 10))
        self.resolution_display = tk.Entry(result2_frame, width=5)
        self.resolution_display.pack(side="left")
        tk.Label(result2_frame, text="Overall CC1/2",
                 bg='white').pack(side="left", padx=(35, 10))
        self.cc12_display = tk.Entry(result2_frame, width=8)
        self.cc12_display.pack(side="left")
        replace_entry_readonly(self.running_summary, "0 / 0 / 0")
        replace_entry_readonly(self.last_status, "Waiting...")
        replace_entry_readonly(self.completeness_display, "0.0")
        replace_entry_readonly(self.resolution_display, "0.0")
        replace_entry_readonly(self.cc12_display, "0.0")
        ToolTip(self.running_summary, "The datasets which marked as Good / Processable / All by given criteria.")
        ToolTip(self.last_status, "The status of the latest dataset.")
        ToolTip(self.completeness_display, "The completeness of the latest merge cluster."
                                           "\nOnly meaningful when given unit cell and sg.")
        ToolTip(self.resolution_display, "The set resolution")
        ToolTip(self.cc12_display, "The CC1/2 of the latest merge cluster."
                                   "\nOnly meaningful when given unit cell and sg.")

        # Row 8: Current Average Unit Cell
        result3_frame = tk.Frame(self, bg='white')
        result3_frame.grid(row=8, column=0, sticky="w", padx=20, pady=(2 * sp, sp))
        self.unit_cell_label = tk.Label(result3_frame, text="Average Unit cell", bg='white')
        self.unit_cell_label.pack(side="left", padx=(25, 10))
        self.unit_cell_display = tk.Entry(result3_frame, bg='lightgrey', width=50)
        self.unit_cell_display.pack(side="left", padx=(5, 0))
        replace_entry_readonly(self.unit_cell_display, "Waiting...")
        ToolTip(self.unit_cell_display, "The cell parameter of the latest merge cluster."
                                        "\nOnly meaningful when given unit cell and sg.")

        # Row 12: Open xscale.lp button
        buttons_frame_row_12 = tk.Frame(self, bg='white')
        buttons_frame_row_12.grid(row=12, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        open_cluster_button = tk.Button(buttons_frame_row_12, text="Open Cluster Report", command=self.open_report)
        open_cluster_button.pack(side="left", padx=25)
        open_xscale_button = tk.Button(buttons_frame_row_12, text="Open Current xscale.lp",
                                       command=self.open_current_xscale_lp)
        open_xscale_button.pack(side="left", padx=25)

        ToolTip(open_cluster_button, "Open the web report of the latest merge cluster."
                                     "\nOnly meaningful when given unit cell and sg.")
        ToolTip(open_xscale_button, "Open the XSCALE.LP of the latest merge cluster."
                                    "\nOnly meaningful when given unit cell and sg.")

        # Row 13: Information
        note_label = tk.Label(self, text="Live Statistics:", bg='white',
                              font=("Liberation Sans", int(16 * self.sf), "bold"))
        note_label.grid(row=13, column=0, sticky="w", padx=15, pady=(3 * sp, 2 * sp))

        # Row 14: Add plot area at the bottom
        plot_frame = tk.Frame(self, bg='white')
        plot_frame.grid(row=14, column=0, sticky="w", padx=20, pady=0)

        self.plot_frames = [tk.Frame(plot_frame, bg='white', padx=20) for _ in range(3)]
        self.figures = [Figure(figsize=(3.5, 2.5), dpi=100 * (self.sf ** 2.50)) for _ in range(3)]
        self.plot_canvases = [FigureCanvasTkAgg(fig, plot_frame) for fig in self.figures]
        self.axes = [fig.add_subplot(111) for fig in self.figures]

        for i, (plot_frame, plot_canvas) in enumerate(zip(self.plot_frames, self.plot_canvases)):
            plot_frame.pack(side="left", fill="both", expand=True)
            plot_canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Method to update plots
        self.update_plots()

    def update_plots(self) -> None:
        """Update the live statistics plots with the latest data.

        This method retrieves the latest statistics from `status_dict` and updates the matplotlib
        plots embedded in the GUI. It handles both P1 and non-P1 modes, adjusting plot configurations
        accordingly. Interactive cursors are added to provide dataset-specific information upon hover.

        Returns:
            None
        """

        def dynamic_size(length):
            if length <= 10:
                ms, me = 8, 3
            elif length <= 20:
                ms, me = 6, 2
            elif length <= 40:
                ms, me = 4.5, 2
            else:
                ms, me = 4, 1.5
            return ms, me

        try:
            good_list = sorted([(key, item["statistics"]) for key, item in self.status_dict.items()
                                if item["status"] == "good"], key=lambda x: x[1]["mtime"])
        except KeyError:
            good_list = [("Empty", {"resolution": 1, "isa": 1, "cc12_reso": 0})]
        if not good_list:
            good_list = [("Empty", {"resolution": 1, "isa": 1, "cc12_reso": 0})]

        y1_values = [item[1]["resolution"] for item in good_list]
        x1_values = list(range(1, len(y1_values) + 1))
        ms1, me1 = dynamic_size(len(y1_values))
        name_good = [item[0] for item in good_list]

        y4_values = [item[1]["cc12_reso"] if "cc12_reso" in item[1] else item[1]["CC1/2"] for item in good_list]
        y5_values = [item[1]["isa"] if "isa" in item[1] else item[1]["ISa_meas"] for item in good_list]

        try:
            cluster_list = sorted([(key, item) for key, item in self.status_dict[self.name].items()
                                   if "resolution" in item], key=lambda pair: natural_sort_key(pair[0]))
        except KeyError:
            cluster_list = [("Empty", {"completeness": 0, "cc12_reso": 0})]
        except TypeError:
            cluster_list = [("Empty", {"completeness": 0, "cc12_reso": 0})]
        if not cluster_list:
            cluster_list = [("Empty", {"completeness": 0, "cc12_reso": 0})]

        name_cluster = [item[0].replace("cluster_", "") for item in cluster_list]

        if not self.P1:
            y2_values = [item[1]["completeness"] for item in cluster_list]
            y3_values = [item[1]["cc12_reso"] if "cc12_reso" in item[1] else item[1]["CC1/2"] for item in cluster_list]
            x2_values = list(range(1, len(y2_values) + 1))
            ms2, me2 = dynamic_size(len(y2_values))

            for cursor in self.cursors:
                cursor.remove()
            self.cursors.clear()

            for fig in self.figures:
                fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0.4)

            self.axes[0].clear()
            self.axes[0].plot(x1_values, y1_values, linestyle='--', marker='o', color='#EF9C66', linewidth=1.2,
                              markersize=ms1, markerfacecolor='white', markeredgewidth=me1)
            self.axes[0].set_title("Resolution vs Good Datasets", fontsize=11)
            self.axes[0].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)
            self.axes[0].invert_yaxis()

            self.axes[1].clear()
            self.axes[1].plot(x2_values, y2_values, linestyle='-', marker='o', color='#B3BC7A', linewidth=2,
                              markersize=ms2, markerfacecolor='white', markeredgewidth=me2)
            self.axes[1].set_title("Completeness vs Iters", fontsize=12)
            self.axes[1].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)

            self.axes[2].clear()
            self.axes[2].plot(x2_values, y3_values, linestyle='-', marker='o', color='#78ABA8', linewidth=2,
                              markersize=ms2, markerfacecolor='white', markeredgewidth=me2)
            self.axes[2].set_title("CC1/2 vs Iters", fontsize=12)
            self.axes[2].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)
        else:
            for cursor in self.cursors:
                cursor.remove()
            self.cursors.clear()

            for fig in self.figures:
                fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0.4)

            self.axes[0].clear()
            self.axes[0].plot(x1_values, y1_values, linestyle='--', marker='o', color='#EF9C66', linewidth=1.2,
                              markersize=ms1, markerfacecolor='white', markeredgewidth=me1)
            self.axes[0].set_title("Resolution vs Good Datasets", fontsize=11)
            self.axes[0].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)
            self.axes[0].invert_yaxis()

            self.axes[1].clear()
            self.axes[1].plot(x1_values, y4_values, linestyle='--', marker='o', color='#B3BC7A', linewidth=1.2,
                              markersize=ms1, markerfacecolor='white', markeredgewidth=me1)
            self.axes[1].set_title("CC1/2 vs Good Datasets", fontsize=12)
            self.axes[1].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)

            self.axes[2].clear()
            self.axes[2].plot(x1_values, y5_values, linestyle='--', marker='o', color='#78ABA8', linewidth=1.2,
                              markersize=ms1, markerfacecolor='white', markeredgewidth=me1)
            self.axes[2].set_title("I/Sigma vs Good Datasets", fontsize=12)
            self.axes[2].grid(True, which='major', axis="y", linestyle='--', linewidth=0.5)

        def on_add(sel, name, data):
            x = round(sel.target[0], 1)
            y = round(sel.target[1], 3)
            index = int(round(sel.target[0], 0) - 1)
            if index < 0:
                index = 0
            elif index > len(name) - 1:
                index = len(name) - 1
            dataset_name = name[index]
            if len(dataset_name) > 16:
                dataset_name = dataset_name[:7] + ".." + dataset_name[-7:]
            sel.annotation.set_text(f'{dataset_name}\nX: {x}\nY: {y}')
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.6)

        # Adding cursors to each axis with annotations
        for i, ax in enumerate(self.axes):
            cursor = mplcursors.cursor(ax, hover=True)
            self.cursors.append(cursor)
            if i == 0:
                data1 = y1_values
                name1 = name_good
            elif i == 1:
                data1 = y4_values if self.P1 else y2_values
                name1 = name_good if self.P1 else name_cluster
            else:
                data1 = y5_values if self.P1 else y3_values
                name1 = name_good if self.P1 else name_cluster

            cursor.connect("add", lambda sel, data=data1, name=name1: on_add(sel, name, data))

        # Redrawing each plot canvas
        for plot_canvas in self.plot_canvases:
            try:
                plot_canvas.draw()
            except Exception as e:
                print(f"Plot failed due to {e}")

    def load_strategy(self, event: tk.Event) -> None:
        """Load and apply the selected processing strategy.

        This method is triggered when the user selects a strategy from the strategy dropdown.
        It checks for the existence of a `strategy.txt` file in the input directory, creates a
        default one if absent, and opens the strategy file for editing if the "edit" option is selected.

        Args:
            event (tk.Event): The Tkinter event object.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        if self.strategy_option_var.get() == "--":
            return
        else:
            if os.path.isfile(os.path.join(self.input_path, "strategy.txt")):
                pass
            else:
                self.write_default_strategy()
        if self.strategy_option_var.get() == "edit":
            self.text_edit(os.path.join(self.input_path, "strategy.txt"))

    def write_default_strategy(self) -> None:
        """Write a default processing strategy to `strategy.txt`.

        This method creates a `strategy.txt` file in the input directory with predefined cycle
        times and filter rules. It serves as a fallback when no strategy file is present.

        Returns:
            None
        """
        with open(os.path.join(self.input_path, "strategy.txt"), "w") as f:
            f.write("! CYCLE_TIME, refresh time, default 5 s. \n")
            f.write("! WAITING_TIME, time waiting for real processing\n")
            f.write("! after folder is unchanged, default 10 s.\n")
            f.write(" CYCLE_TIME= 5\n")
            f.write(" WAITING_TIME= 20\n\n")
            f.write("! Available Filter for RUN_FILTER: CC12, ISA, REXP, RMEAS, RESOLUTION, VOLUME_DEV, unit in %\n")
            f.write(" RUN_FILTER= CC12 > 85\n")
            f.write(" RUN_FILTER= ISA > 2\n")
            f.write(" RUN_FILTER= ISA < 25\n\n")
            f.write("! Available Filter for MERGE_FILTER: CC12, DISTANCE\n")
            f.write(" MERGE_FILTER= CC12 > 0\n\n\n")

    def text_edit(self, file_path: str) -> None:
        """Open a text editor window for editing a specified file.

        Args:
            file_path (str): The path to the file to be edited.

        Returns:
            None
        """
        text_editor_window = tk.Toplevel(self)
        text_editor_window.title("Text Editor")
        text_editor_window.geometry(
            f"{int(600 * self.sf * self.sf)}x{int(400 * self.sf * self.sf)}")  # Adjust the size as needed

        def save_file():
            if current_file:
                with open(current_file, 'w') as file1:
                    file1.write(text_editor.get(1.0, tk.END))
                messagebox.showinfo("Save", "File saved successfully")

        # Create the text editor widget
        text_editor = tk.Text(text_editor_window, wrap='word', font=("Liberation Mono", int(15 * self.sf)))
        text_editor.pack(fill=tk.BOTH, expand=True)

        # Create the menu bar
        menu_bar = tk.Menu(text_editor_window)

        # Add Save and Exit directly to the menu bar
        menu_bar.add_command(label="Save", command=save_file)

        # Attach the menu bar to the window
        text_editor_window.config(menu=menu_bar)

        # Load the file content into the text editor
        with open(file_path, 'r') as file:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, file.read())
            global current_file
            current_file = file_path
            text_editor_window.title(f"Text Editor - {file_path}")

    @classmethod
    def get_md5(cls, file_path: str) -> str:
        """Compute the MD5 checksum of a file.

        Args:
            file_path (str): The path to the file for which the MD5 checksum will be computed.

        Returns:
            str: The hexadecimal MD5 checksum of the file.
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def convert_image(self, key: str) -> None:
        """Convert MRC image to SMV format.

        Initiates a separate thread to convert MRC image files to SMV format using the `image_io` module.
        Waits for the conversion process to complete before proceeding.

        Args:
            key (str): The identifier for the image to be converted.

        Returns:
            None
        """
        print(f"Convert MRC Image in {self.input_path} to SMV format.\n")
        self.thread["conversion"] = KillableThread(target=image_io.convert_mrc2img, args=(key,))
        self.thread["conversion"].start()
        self.thread["conversion"].join()  # Wait for the conversion thread to finish

    def run_data_reduction(self, run_dict: dict) -> None:
        """Process datasets through various stages and perform corresponding actions.

        This method handles the data reduction workflow by:
        - Converting collected images.
        - Writing and correcting `XDS.INP` files.
        - Running the XDS data reduction process.
        - Initiating clustering if applicable.

        Args:
            run_dict (dict): A dictionary mapping dataset folders to their current processing status.

        Returns:
            None
        """
        for key, value in run_dict.items():
            if value == "collected":
                self.convert_image(key)
                run_dict[key] = "transferred"

        # Write and correct XDS files
        for key, value in run_dict.items():
            if value == "transferred":
                xds_input.write_xds_file(key, os.path.join(self.input_path, "Input_parameters.txt"))
                if self.do_correct.get():
                    xds_input.correct_inputs(key)
                if self.is_beam_stop.get():
                    image_io.beam_stop_calculate(key)
                else:
                    image_io.centre_calculate(key)
                if not self.P1:
                    xds_input.cell_correct_online(os.path.join(key, "xds", "XDS.INP"), self.cell, self.sg)
                run_dict[key] = "ready"
            elif value == "instamatic-ready":
                xds_input.instamatic_update(key, True)
                if self.do_correct.get():
                    xds_input.correct_inputs(key)
                if not self.P1:
                    xds_input.cell_correct_online(os.path.join(key, "SMV", "XDS.INP"), self.cell, self.sg)
                run_dict[key] = "ready"

        # Run the XDS runner for ready items
        xds_list = [
            os.path.join(key, "xds", "XDS.INP") if os.path.isdir(os.path.join(key, "xds")) else os.path.join(key, "SMV",
                                                                                                             "XDS.INP")
            for key in run_dict.keys() if run_dict[key] == "ready"]
        self.thread["xds_runner"] = KillableThread(target=xds_runner.xdsrunner,
                                                   args=(self.input_path, xds_list, True, False))
        self.thread["xds_runner"].start()
        self.thread["xds_runner"].join()

        self.status_dict = self.update_status_dict(self.status_dict)
        if not self.P1:
            try:
                self.run_cluster()
            except Exception as e:
                print(f"Cluster encounter error as {e}")
        else:
            self.update_display()

    def update_status_initial(self) -> None:
        """Initialize and update the status dictionary from `realtime.json`.

        Loads the initial processing statuses from the `realtime.json` file. If the file does not exist,
        initializes an empty status dictionary.

        Returns:
            None
        """
        self.realtime_json = os.path.join(self.input_path, 'realtime.json')
        if os.path.exists(self.realtime_json):
            with open(self.realtime_json, 'r') as file:
                self.status_dict = json.load(file)
        else:
            self.status_dict = {}
        self.update_status_dict(self.status_dict, initial=True)

    def update_status_dict(self, _status_dict: dict, initial: bool = False) -> dict:
        """Update the status dictionary with the latest dataset statuses.

        This method scans the input directory for subfolders, updates their statuses based on the presence
        of specific files and processing outcomes, and writes the updated statuses back to `realtime.json`.

        Args:
            _status_dict (dict): The current status dictionary to be updated.
            initial (bool, optional): Flag indicating if this is the initial status update. Defaults to False.

        Returns:
            dict: The updated status dictionary.
        """
        backup_dict = _status_dict.copy()
        self.realtime_json = os.path.join(self.input_path, 'realtime.json')
        subfolders = {f for f in os.listdir(self.input_path) if os.path.isdir(os.path.join(self.input_path, f))}

        existing_folders = set(_status_dict.keys())
        non_existing_folders = existing_folders - subfolders
        for folder in non_existing_folders:
            del _status_dict[folder]

        for folder in {f for f in _status_dict.keys() if _status_dict[f]["status"] == "discard"}:
            if not folder.startswith("!"):
                _status_dict[folder] = "ready"

        if not initial:
            pattern = re.compile(r'iter(\d+)')
            numbers = []
            resolution = float(self.reso_limit)
            for _item in os.listdir(os.path.join(self.input_path, self.name)):
                if os.path.isdir(os.path.join(self.input_path, self.name, _item)):
                    match = pattern.match(_item)
                    if match:
                        numbers.append(int(match.group(1)))
            for num in sorted(numbers):
                all_hkl = os.path.join(self.input_path, self.name, f"iter{num}", "all.HKL")
                cluster_dir = os.path.join(self.input_path, self.name, f"iter{num}")
                if os.path.isfile(os.path.join(all_hkl)):
                    _status_dict[self.name][f"iter{num}"] = (
                        xds_analysis.extract_cluster_result(cluster_dir, reso=resolution))

        if not initial:
            finished_folder = {f for f in _status_dict.keys()
                               if _status_dict[f]["status"] in ["discard", "good", "bad", "failed", "document"]}
            subfolders = subfolders - finished_folder
        else:
            finished_folder = {f for f in _status_dict.keys()
                               if _status_dict[f]["status"] in ["document"]}
            for folder in finished_folder:
                if folder != self.name:
                    _status_dict[folder] = "empty"
            subfolders = subfolders - {self.name}

        for subfolder in sorted(subfolders):
            folder_path = os.path.join(self.input_path, subfolder)
            if subfolder.startswith("!"):
                _status_dict[subfolder] = {"status": "discard", "folder": folder_path}
                continue

            mrc_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mrc')]
            cRED_file = os.path.join(folder_path, "cRED_log.txt")
            image_no = len(mrc_files)
            mrc_md5 = ""
            statistics = {}

            if mrc_files:
                first_mrc_file = mrc_files[0]
                mrc_file_path = os.path.join(folder_path, first_mrc_file)
                mrc_md5 = self.get_md5(mrc_file_path)
                img_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.img')]
                if len(img_files) == 0:
                    folder_status = "collecting"
                elif len(img_files) >= len(mrc_files) - 5:
                    xds_folder = os.path.join(folder_path, 'xds')
                    if os.path.exists(xds_folder):
                        init_lp = os.path.join(xds_folder, 'INIT.LP')
                        hkl_file = os.path.join(xds_folder, 'XDS_ASCII.HKL')
                        if os.path.exists(init_lp) and os.path.exists(hkl_file):
                            statistics = xds_analysis.extract_run_result(os.path.join(folder_path, "xds"))
                            if self.meet_criteria(statistics):
                                folder_status = "good"
                            else:
                                folder_status = "bad"
                        elif os.path.exists(init_lp):
                            folder_status = "failed"
                            statistics["mtime"] = os.path.getmtime(init_lp)
                        else:
                            folder_status = "ready"
                    else:
                        folder_status = "transferred"
                else:
                    folder_status = "collected"
            elif os.path.isfile(cRED_file) and os.path.isdir(os.path.join(folder_path, 'SMV', 'data')):
                mrc_md5 = self.get_md5(cRED_file)
                xds_folder = os.path.join(folder_path, 'SMV')
                data_folder = os.path.join(xds_folder, 'data')
                img_files = [f for f in os.listdir(data_folder) if f.lower().endswith('.img')]
                img_collect_no = xds_input.read_cRED_log(cRED_file)
                init_lp = os.path.join(xds_folder, 'INIT.LP')
                hkl_file = os.path.join(xds_folder, 'XDS_ASCII.HKL')
                if len(img_files) >= img_collect_no - 1:
                    if os.path.exists(init_lp) and os.path.exists(hkl_file):
                        statistics = xds_analysis.extract_run_result(os.path.join(folder_path, "SMV"))
                        if self.meet_criteria(statistics):
                            folder_status = "good"
                        else:
                            folder_status = "bad"
                    elif os.path.exists(init_lp):
                        folder_status = "failed"
                        statistics["mtime"] = os.path.getmtime(init_lp)
                    else:
                        folder_status = "instamatic-ready"
                else:
                    image_no = len(img_files)
                    folder_status = "instamatic-collecting"
            else:
                folder_status = "empty"

            _status_dict[subfolder] = {
                "status": folder_status,
                "folder": folder_path,
                "MD5": mrc_md5,
                "image_no": image_no,
                "statistics": statistics
            }

        try:
            self.update_plots()
        except Exception as e:
            pass

        if {k: _status_dict[k] for k in sorted(_status_dict, key=natural_sort_key)} != backup_dict:
            if not initial:
                self.update_display(output=False)
            with open(self.realtime_json, 'w') as file:
                json.dump(_status_dict, file, indent=4)
        return {k: _status_dict[k] for k in sorted(_status_dict, key=natural_sort_key)}

    def meet_criteria(self, statistics: dict) -> bool:
        """Determine if a dataset meets the processing criteria based on statistics.

        Evaluates the dataset's statistics against the rules defined in the processing strategy.
        Returns `True` if all criteria are met, otherwise `False`.

        Args:
            statistics (dict): A dictionary containing statistical metrics of the dataset.

        Returns:
            bool: `True` if the dataset meets all criteria, `False` otherwise.
        """
        rules = self.strategy_dict["RUN_FILTER"]
        cc12 = statistics["cc12_reso"] if "cc12_reso" in statistics else statistics["CC1/2"]
        isa = statistics["ISa_model"]
        resolution = statistics["resolution"]
        rexp = statistics["rexp"] if "rexp" in statistics else statistics["R_exp"]
        rmeas = statistics["rmeas"] if "rmeas" in statistics else statistics["R_meas"]
        if self.cell:
            try:
                vol = statistics["volume"]
                if self.cell.count(", ") == 5:
                    std_vol = analysis_hkl.unit_cell_volume(*self.cell.split(", "))
                else:
                    std_vol = analysis_hkl.unit_cell_volume(*self.cell.split(" "))
                vol_dev = abs(vol - std_vol) / std_vol * 100
            except Exception as e:
                vol_dev = 0
        else:
            vol_dev = 0

        local_vars = {
            'CC12': cc12,
            'ISA': isa,
            "RESOLUTION": resolution,
            "REXP": rexp,
            "RMEAS": rmeas,
            "VOLUME_DEV": vol_dev,
        }

        for rule in rules:
            if not eval(rule, {}, local_vars):
                return False
        return True

    def update_display_initial(self) -> None:
        """Initialize the GUI display with the current status dictionary.

        Loads the `realtime.json` file, updates GUI entry widgets with dataset information,
        and sets up initial display states.

        Returns:
            None
        """
        if os.path.exists(os.path.join(self.input_path, 'online.json')):
            shutil.move(os.path.join(self.input_path, 'online.json'), os.path.join(self.input_path, 'realtime.json'))
        with open(os.path.join(self.input_path, 'realtime.json'), 'r') as file:
            self.status_dict = json.load(file)
        for key, item in self.status_dict.items():
            if item["status"] == "document":
                try:
                    replace_entry(self.entry["name"], key)
                    replace_entry(self.entry["cell"], item["input"]["cell"])
                    replace_entry(self.entry["sg"], item["input"]["sg"])
                    replace_entry(self.entry["reso"], item["input"]["reso_limit"])
                    self.is_beam_stop.set(strtobool(item["input"]["beam_stop"]))
                    self.do_correct.set(strtobool(item["input"]["do_correct"]))
                    return
                except KeyError:
                    return

    def update_display(self, output: bool = True) -> None:
        """Update the GUI display elements with the latest processing results.

        Refreshes the summary entries, status entries, and average unit cell display based on the
        current `status_dict`. It also updates the live statistics plots to reflect the latest data.

        Args:
            output (bool, optional): Flag to control whether to print status messages. Defaults to True.

        Returns:
            int: Returns 0 if no data is present; otherwise, None.
        """
        good_list = [item for key, item in self.status_dict.items() if item["status"] in ["good"]]
        failed_list = [item for key, item in self.status_dict.items() if item["status"] in ["failed"]]
        all_list = sorted(
            [(key, item) for key, item in self.status_dict.items() if item["status"] in ["good", "bad", "failed"]],
            key=lambda x: x[1]["statistics"]["mtime"],
            reverse=True
        )
        if len(all_list) < 1:
            return 0
        else:
            replace_entry_readonly(self.running_summary,
                                   f"{len(good_list)} / {len(all_list) - len(failed_list)} / {len(all_list)}")
            replace_entry_readonly(self.last_status, "{}: {}".format(all_list[0][0], all_list[0][1]["status"]))
            if self.P1:
                replace_entry_readonly(self.resolution_display, "--")
                replace_entry_readonly(self.unit_cell_display, "--")
            else:
                replace_entry_readonly(self.resolution_display, f"{self.reso_limit}")
        pattern = re.compile(r'iter(\d+)')
        # Initialize a list to store all matched numbers
        numbers = []
        # Loop through the subfolders in the parent directory
        for _item in os.listdir(os.path.join(self.input_path, self.name)):
            # Check if the item is a directory and matches the pattern
            if os.path.isdir(os.path.join(self.input_path, self.name, _item)):
                match = pattern.match(_item)
                if match:
                    numbers.append(int(match.group(1)))

        # Find the maximum number if any matches were found
        if numbers:
            last_num = max(numbers)
            folder_path = os.path.join(self.input_path, self.name, f"iter{last_num}")
            info_dict = xds_analysis.extract_cluster_result(folder_path, reso=float(self.reso_limit))
            cc12 = info_dict["cc12_reso"] if "cc12_reso" in info_dict else info_dict["CC1/2"]
            completeness = info_dict["completeness"]
            unit_cell = info_dict["unit_cell"]

            replace_entry_readonly(self.completeness_display, f"{completeness:.1f} %")
            replace_entry_readonly(self.cc12_display, f"{cc12} %")
            replace_entry_readonly(self.unit_cell_display,
                                   "{}".format(
                                       "  ".join(str(round(item, 2)) if item != 90.0 else "90" for item in unit_cell)))
        elif self.P1:
            replace_entry_readonly(self.completeness_display, "--")
            replace_entry_readonly(self.cc12_display, "--")
        else:
            if output:
                print("No merged data present. Please wait.\n")
            return

    def run_cluster(self) -> None:
        """Initiate the clustering process for good datasets.

        Identifies the latest cluster iteration, creates a new cluster folder, generates an Excel
        picker file, and runs the clustering process using the `xds_cluster` module. Updates the
        `status_dict` with the clustering results.

        Returns:
            None
        """
        pattern = re.compile(r'iter(\d+)')
        # Initialize a list to store all matched numbers
        numbers = []
        # Loop through the subfolders in the parent directory
        for _item in os.listdir(os.path.join(self.input_path, self.name)):
            # Check if the item is a directory and matches the pattern
            if os.path.isdir(os.path.join(self.input_path, self.name, _item)):
                match = pattern.match(_item)
                if match:
                    numbers.append(int(match.group(1)))

        # Find the maximum number if any matches were found
        if numbers:
            start_num = max(numbers) + 1
        else:
            start_num = 1

        new_good_set = {f for f in self.status_dict.keys() if self.status_dict[f]["status"] == "good"}

        if self.good_set != new_good_set:
            self.good_set = new_good_set
            os.mkdir(os.path.join(self.input_path, self.name, f"iter{start_num}"))
            if self.make_picker_excel(os.path.join(self.input_path, self.name, f"iter{start_num}")):
                xds_cluster.merge(os.path.join(self.input_path, self.name, f"iter{start_num}"), folder="",
                                  reso=float(self.reso_limit), alert=False)
                self.status_dict[self.name][f"iter{start_num}"] = xds_analysis.extract_cluster_result(
                    os.path.join(self.input_path, self.name, f"iter{start_num}"), self.reso_limit)
                xds_report.create_html_file(os.path.join(self.input_path, self.name, f"iter{start_num}"),
                                            "cluster")
        self.update_display()

    def monitor_folder(self) -> None:
        """Monitor the input folder for new data and manage processing workflows.

        Continuously monitors the input directory for new data collection folders, updates their
        statuses, and initiates data reduction processes when criteria are met. Handles both normal
        and single (P1) processing modes.

        Returns:
            None
        """
        self.name = self.entry["name"].get()
        self.good_set = {}
        self.cell = self.entry["cell"].get()
        self.sg = self.entry["sg"].get()
        self.beam_stop = self.is_beam_stop.get()
        self.reso_limit = self.entry["reso"].get()

        if (not self.sg) or (not self.cell):
            if messagebox.askyesno("Warning", "You haven't input the cell or spacegroup information. "
                                              "Do you want to run in the Screen mode?"):
                if messagebox.askyesno("Warning", "The Screen mode will only do the P1 stage and "
                                                  "will not do the merge. Do you wish to continue?"):
                    self.P1 = True
                    self.reso_limit = "1.0"
                else:
                    self.stop_running()
                    return
            else:
                self.stop_running()
                return

        with open(os.path.join(self.input_path, "strategy.txt"), "r") as f:
            self.strategy_dict = xds_input.extract_keywords(f.readlines())
        self.update_status_initial()
        self.run_bool = True

        if ((self.name in self.status_dict and self.status_dict[self.name]["status"] != "document") or
                not is_suitable_linux_folder_name(self.name)):
            self.name = "realtimeED"
            os.makedirs(os.path.join(self.input_path, "realtimeED"), exist_ok=True)
            if "realtimeED" in self.status_dict:
                self.status_dict["realtimeED"]["status"] = "document"
            else:
                self.status_dict["realtimeED"] = {
                    "status": "document",
                    "input": {"cell": self.cell, "sg": self.sg, "do_correct": self.do_correct.get(),
                              "beam_stop": self.is_beam_stop.get(), "reso_limit": self.reso_limit}}
        elif self.name not in self.status_dict:
            os.makedirs(os.path.join(self.input_path, self.name), exist_ok=True)
            self.status_dict[self.name] = {
                "status": "document", "input": {"cell": self.cell, "sg": self.sg, "do_correct": self.do_correct.get(),
                                                "beam_stop": self.is_beam_stop.get(), "reso_limit": self.reso_limit}}

        monitor_folder = {f for f in self.status_dict.keys()
                          if self.status_dict[f]["status"] in ["empty", "collecting"]}
        last_image_no = {folder: self.status_dict[folder]["image_no"] for folder in monitor_folder}
        last_check_time = {folder: time.time() for folder in monitor_folder}
        self.update_display()

        while self.run_bool:
            new_list = []
            print("\rThe RealTime MicroED is running... ", end="", flush=True)
            self.status_dict = self.update_status_dict(self.status_dict)

            # Update monitor_folder with new folders marked as collecting
            current_folders = set(self.status_dict.keys())
            new_folders = {folder for folder in current_folders if self.status_dict[folder]["status"] == "collecting"}
            for folder in new_folders:
                if folder not in monitor_folder:
                    new_list.append(folder)
                    monitor_folder.add(folder)
                    last_image_no[folder] = self.status_dict[folder]["image_no"]
                    last_check_time[folder] = time.time()

            if new_list:
                print("\n")
                for folder in new_list:
                    print(f"Found new folder {folder}, added to the monitor list.")
                print("\n", end="", flush=True)
            # Remove folders that are collected
            collected_folders = {folder for folder in monitor_folder if folder in self.status_dict and
                                 self.status_dict[folder]["status"] == "collected"}
            monitor_folder -= collected_folders

            for folder in monitor_folder:
                if folder not in self.status_dict:
                    continue  # Skip folders that have been removed from the status_dict
                current_image_no = self.status_dict[folder]["image_no"]

                if self.status_dict[folder]["status"] == "collecting":
                    if current_image_no != last_image_no[folder]:
                        last_image_no[folder] = current_image_no
                        last_check_time[folder] = time.time()
                    elif (time.time() - last_check_time[folder] >= int(self.strategy_dict["WAITING_TIME"][0])
                          and current_image_no > 10):
                        self.status_dict[folder]["status"] = "collected"

            run_list = {self.status_dict[f]["folder"]: self.status_dict[f]["status"] for f in self.status_dict.keys()
                        if self.status_dict[f]["status"] in ["collected", "transferred", "ready", "instamatic-ready"]}

            if run_list:
                self.run_data_reduction(run_list)

            time.sleep(int(self.strategy_dict["CYCLE_TIME"][0]))

    def stop_running(self) -> None:
        """Stop the real-time MicroED data processing.

        Sets the running flag to `False`, stops all active animations, terminates running threads,
        and updates the `realtime.json` file with the latest statuses.

        Returns:
            None
        """
        self.run_bool = False
        self.stop_realtime_microed_animation()
        for key, thread1 in self.thread.items():
            if thread1.is_alive():
                thread1.terminate()
        print("\nThe RealTime MicroED is stopped.")
        messagebox.showerror("Caution", "The RealTime MicroED is stopped.")
        with open(self.realtime_json, 'w') as file:
            json.dump(self.status_dict, file, indent=4)

    def make_picker_excel(self, path: str) -> bool:
        """Generate an Excel picker file with dataset information.

        Creates an `xdspicker.xlsx` file containing details of all "good" datasets based on the
        current `status_dict`. If there is insufficient data, the cluster folder is removed.

        Args:
            path (str): The path to the cluster iteration folder where the Excel file will be saved.

        Returns:
            bool: `True` if the Excel file was successfully created, `False` otherwise.
        """
        data = []
        columns = ["No.", "Path", "Space group", "Unit cell", "ISa", "CC1/2", "Completeness", "Reso."]
        dtypes = {
            'No.': int,
            'Path': str,
            'Space group': int,
            'Unit cell': str,
            'ISa': float,
            'CC1/2': float,
            'Completeness': float,
            'Reso.': float
        }

        for key, item in self.status_dict.items():
            num = 1
            if item["status"] == "good":
                stats = item["statistics"]
                unit_cell = stats["unit_cell"]
                unit_cell_str = " ".join(map(str, unit_cell))

                # Create a row of data
                row = [
                    num,  # No.
                    os.path.join(item["folder"], "SMV")
                    if os.path.isdir(os.path.join(item["folder"], "SMV"))
                    else os.path.join(item["folder"], "xds"),  # Path
                    self.sg,  # Space group, replace with the actual value if available
                    unit_cell_str,  # Unit cell
                    stats["ISa_model"],  # Isa
                    stats["cc12_reso"] if "cc12_reso" in stats else stats["CC1/2"],  # CC1/2
                    stats["completeness"],  # Completeness
                    stats["resolution"]
                ]

                # Append the row to the data list
                data.append(row)
                num += 1

        if len(data) <= 1:
            os.rmdir(path)
            return False

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=columns)

        # Ensure the DataFrame uses the correct data types
        for column, dtype in dtypes.items():
            df[column] = df[column].astype(dtype)

        excel_filename = os.path.join(path, "xdspicker.xlsx")
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return True

    def run_realtime_microed(self) -> None:
        """Start the real-time MicroED data processing.

        Validates the presence of necessary input files, loads the processing strategy, and
        initiates the monitoring thread for real-time data processing.

        Returns:
            None
        """
        if self.input_path:
            if not os.path.isfile(os.path.join(self.input_path, "Input_parameters.txt")):
                messagebox.showinfo("Warning", f"The input parameter file is not given.")
                return
            if not os.path.isfile(os.path.join(self.input_path, "strategy.txt")):
                self.write_default_strategy()
            self.thread["realtime"] = KillableThread(target=self.monitor_folder)
            self.thread["realtime"].start()
            self.start_realtime_microed_animation()

    def start_realtime_microed_animation(self) -> None:
        """Start the animation indicating that real-time MicroED data processing is running.

        Initiates the animation loop for visual feedback during data processing.

        Returns:
            None
        """
        self.realtime_microed_animation_active = True
        self.realtime_microed_animation_angle = 0
        self.realtime_microed_animate()

    def realtime_microed_animate(self) -> None:
        """Animate the real-time MicroED data processing status in the GUI.

        Continuously updates the animation canvas to reflect the ongoing data processing. Stops
        the animation when the processing is no longer active.

        Returns:
            None
        """
        if self.realtime_microed_animation_active:
            self.realtime_microed_animation_canvas.delete("all")

            # animate logic
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.realtime_microed_animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1,
                                                              start=self.realtime_microed_animation_angle, extent=160,
                                                              style=tk.ARC)
            self.realtime_microed_animation_canvas.create_text(50, 10, text="RealTime Data Processing Running...",
                                                               anchor="w")

            self.realtime_microed_animation_angle = (self.realtime_microed_animation_angle + 10) % 360

            self.after(100, self.realtime_microed_animate)
        else:
            self.stop_realtime_microed_animation()

    def stop_realtime_microed_animation(self) -> None:
        """Stop the real-time MicroED data processing animation and clear the canvas.

        This method is called once the data processing is complete to remove the animation from the GUI.

        Returns:
            None
        """
        self.realtime_microed_animation_active = False
        self.realtime_microed_animation_canvas.delete("all")

    def open_report(self) -> None:
        """Open the latest cluster report in a web browser.

        Identifies the most recent cluster iteration and opens its HTML report using the `xds_report`
        module. Provides user feedback if no merged data is present.

        Returns:
            None
        """
        pattern = re.compile(r'iter(\d+)')
        # Initialize a list to store all matched numbers
        numbers = []
        # Loop through the subfolders in the parent directory
        for _item in os.listdir(os.path.join(self.input_path, self.name)):
            # Check if the item is a directory and matches the pattern
            if os.path.isdir(os.path.join(self.input_path, self.name, _item)):
                match = pattern.match(_item)
                if match:
                    numbers.append(int(match.group(1)))

        # Find the maximum number if any matches were found
        if numbers:
            last_num = max(numbers)
        else:
            print("No merged data present. Please wait.\n")
            return

        xds_path = os.path.join(self.input_path, self.name, f"iter{last_num}")
        xds_report.open_html_file(xds_path, "cluster")

    def open_current_xscale_lp(self) -> None:
        """Open the `XSCALE.LP` file of the latest cluster iteration in a text editor.

        Identifies the most recent cluster iteration and displays the contents of its `XSCALE.LP` file
        in a new Tkinter Toplevel window with scrollable text.

        Returns:
            None
        """
        pattern = re.compile(r'iter(\d+)')
        # Initialize a list to store all matched numbers
        numbers = []
        # Loop through the subfolders in the parent directory
        for _item in os.listdir(os.path.join(self.input_path, self.name)):
            # Check if the item is a directory and matches the pattern
            if os.path.isdir(os.path.join(self.input_path, self.name, _item)):
                match = pattern.match(_item)
                if match:
                    numbers.append(int(match.group(1)))

        # Find the maximum number if any matches were found
        if numbers:
            last_num = max(numbers)
        else:
            print("No merged data present. Please wait.\n")
            return

        xscale_lp_path = os.path.join(self.input_path, self.name, f"iter{last_num}", "XSCALE.LP")

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
