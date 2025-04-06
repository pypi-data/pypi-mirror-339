"""Tools GUI Module

This module provides a graphical interface for managing various operations within the
crystallographic data processing workflow. It enables users to perform tasks such as
generating REDp files, rolling back XDS.INP files to specific stages, modifying image paths,
and creating PETS input files. The `Tools` class integrates with other AutoLEI modules to
streamline data processing and visualization.

Features:
    - **REDp File Generation**: Supports the generation of REDp files from FEI `.mrc` files.
    - **Rollback Operations**: Allows users to roll back XDS.INP files to the "P1 stage,"
      "Cell stage," or the last refinement stage.
    - **Path Modification**: Facilitates updating image paths in XDS.INP files to either
      absolute or relative paths.
    - **PETS Input Generation**: Automates the creation of PETS input files from `.mrc` files.
    - **File Deletion**: Provides functionality to delete XDS-related files with user confirmation.
    - **GUI Animations**: Includes real-time animations for task progress visualization.

Classes:
    Tools:
        Main class representing the GUI interface for managing crystallographic operations.

Attributes:
    config (configparser.ConfigParser): Configuration settings loaded from the `setting.ini` file.
    script_dir (str): The directory where the script is located.
    analysis_engine (str): The analysis engine configured for HKL analysis.
    path_filter (bool): Boolean flag indicating whether to apply a path filter.
    is_wsl (bool): Indicates whether the script is running in a Windows Subsystem for Linux (WSL) environment.

Dependencies:
    Standard Libraries:
        - configparser
        - tkinter
        - os
        - shutil
        - threading
        - warnings
    Custom Modules:
        - xds_input
        - image_io
        - generate_pets
        - util (various utility functions)

Notes:
    - The `setting.ini` file must be present and correctly configured in the script directory.
    - Ensure all required input files (e.g., `.mrc`, `XDS.INP`) are available in the specified input directories.
    - Operations such as path modification and rollback rely on valid backup files being present.
    - GUI components are designed to be compatible with high-resolution displays.

Contact:
    - Lei Wang: lei.wang@mmk.su.se
    - Yinlin Chen: yinlin.chen@mmk.su.se

License:
    BSD 3-Clause License
"""

try:
    from .src import xds_input, image_io, generate_pets
    from .src.util import *
except ImportError:
    from src import xds_input, image_io, generate_pets
    from src.util import *

import configparser
from tkinter import filedialog, messagebox

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, 'setting.ini'))

analysis_engine = config["XDSRunner"]["engine_hkl_analysis"]
path_filter = strtobool(config["General"]["path_filter"])

is_wsl = is_wsl()


class Tools(tk.Frame):  # Assuming this inherits from tk.Frame
    """
    Tools class provides a graphical user interface (GUI) for managing various operations such as generating REDp files,
    rolling back XDS.INP files, modifying image paths, and creating PETS input files.

    Methods:
        __init__(parent): Initializes the Tools class with GUI components and configurations.
        absolute_path(): Updates the input path in XDS.INP files to absolute paths.
        relative_path(): Updates the input path in XDS.INP files to relative paths.
        select_path(): Opens a directory browser for selecting input paths and updates the GUI entry for REDp generation.
        load_path(): Starts the REDp file generation process for selected input paths.
        mrc_process_animate(): Animates the REDp file generation process in the GUI.
        stop_mrc_process_animation(): Stops the REDp process animation.
        rollback_P1(): Rolls back XDS.INP files to the "P1 stage" using backup files.
        rollback_cell(): Rolls back XDS.INP files to the "Cell stage" or "P1 stage" if applicable.
        rollback_refine(): Rolls back XDS.INP files to the latest refinement stage using backup files.
        select_path_pets(): Opens a directory browser for selecting input paths and updates the GUI entry for PETS generation.
        load_path_pets(): Starts the PETS input file generation process for selected input paths.
        pets_process_animate(): Animates the PETS file generation process in the GUI.
        stop_pets_process_animation(): Stops the PETS process animation.
        confirm_delete_xds(): Displays a confirmation dialog to delete XDS files.
        run_delete_xds_script(): Runs the deletion process for XDS files in the specified input path.
    """

    def __init__(self, parent: tk.Frame):
        """Initialize the Tools GUI frame with all widgets and configurations.

        Args:
            parent (tk.Frame): The parent Tkinter frame where this Tools frame will be placed.
        """
        super().__init__(parent, bg='white')
        self.thread = {}
        self.sf = self.master.master.sf
        sp = 5 * self.sf ** 2.5
        self.input_path = ""

        # Function 1 label
        intro_frame = tk.Frame(self, bg='white')
        intro_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        instruction_msg = "1. Make REDp file based on FEI .mrc files."
        label = tk.Label(intro_frame, text=instruction_msg, bg='white')
        label.pack(side="left", fill="both", expand=True)  # Ensure it fills the frame horizontally

        # Function 1
        row1_frame = tk.Frame(self, bg='white')
        row1_frame.grid(row=1, column=0, sticky="w", padx=10, pady=sp)
        tk.Label(row1_frame, text="Input folder:", bg='white').grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.path_entry = tk.Entry(row1_frame, width=30)
        self.path_entry.grid(row=0, column=1, sticky="w", padx=(0, 10))  # Add padding between label and entry
        redp_browse_button = tk.Button(row1_frame, text="Browse", command=self.select_path)
        redp_browse_button.grid(row=0, column=2, sticky="w", padx=(5, 5))
        run_redp_button = tk.Button(row1_frame, text="Run", command=self.load_path)
        run_redp_button.grid(row=0, column=3, sticky="w", padx=(5, 5))
        self.animation_canvas = tk.Canvas(row1_frame, width=150, height=20, bg='white', highlightthickness=0)
        self.animation_canvas.grid(row=0, column=4, sticky="w", padx=(5, 5))
        self.mrc_process_animation_active = False
        self.mrc_process_animation_angle = 0
        ToolTip(self.path_entry, "The linux path for generating REDp input file")
        ToolTip(redp_browse_button, "Browser the linux path.")
        ToolTip(run_redp_button, "Tidy-up FEI mrc and Perform REDp input file generation.")

        # Function 4 label
        intro_frame = tk.Frame(self, bg='white')
        intro_frame.grid(row=2, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        instruction_msg = "2. Generate PETS input from FEI .mrc files."
        label = tk.Label(intro_frame, text=instruction_msg, bg='white')
        label.pack(side="left", fill="both", expand=True)  # Ensure it fills the frame horizontally

        # Function 4
        row7_frame = tk.Frame(self, bg='white')
        row7_frame.grid(row=3, column=0, sticky="w", padx=10, pady=sp)
        tk.Label(row7_frame, text="Input folder:", bg='white').pack(side="left", padx=(0, 10))
        self.path_entry_pets = tk.Entry(row7_frame, width=30)
        self.path_entry_pets.pack(side="left", padx=(10, 10))  # Add padding between label and entry
        pets_browse_button = tk.Button(row7_frame, text="Browse", command=self.select_path_pets)
        pets_browse_button.pack(side="left", padx=(0, 10))
        self.overwrite = tk.BooleanVar(value=False)
        overwrite_checkbox = tk.Checkbutton(row7_frame, variable=self.overwrite, bg='white')
        overwrite_checkbox.pack(side="left", padx=(10, 10))
        overwrite_label = tk.Label(row7_frame, text="Overwrite Existing TIFF", bg='white')
        overwrite_label.pack(side="left")
        pets_run_button = tk.Button(row7_frame, text="Run", command=self.load_path_pets)
        pets_run_button.pack(side="left", padx=(10, 10))
        self.animation_canvas_pets = tk.Canvas(row7_frame, width=150, height=20, bg='white', highlightthickness=0)
        self.animation_canvas_pets.pack(side="left", padx=(10, 10))
        self.pets_process_animation_active = False
        self.pets_process_animation_angle = 0
        ToolTip(self.path_entry_pets, "Data path in linux system.")
        ToolTip(pets_browse_button, "Browser the linux path.")
        ToolTip(overwrite_checkbox, "Overwrite Existing Tiff file for Pets.")
        ToolTip(pets_run_button, "Perform PETS conversion and PETS auto-workflow.")

        # Function 2 label
        intro_frame = tk.Frame(self, bg='white')
        intro_frame.grid(row=4, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        instruction_msg = "3. Roll back XDS.INP to certain stage."
        label = tk.Label(intro_frame, text=instruction_msg, bg='white')
        label.pack(side="left", fill="both", expand=True)  # Ensure it fills the frame horizontally

        # Function 2
        row3_frame = tk.Frame(self, bg='white')
        row3_frame.grid(row=5, column=0, sticky="w", padx=10, pady=sp)
        P1_button = tk.Button(row3_frame, text="Back to P1 Stage", command=self.rollback_P1)
        P1_button.grid(row=0, column=0, sticky="w", padx=(15, 5))
        cell_button = tk.Button(row3_frame, text="Back to Cell Stage", command=self.rollback_cell)
        cell_button.grid(row=0, column=1, sticky="w", padx=(15, 5))
        refine_button = tk.Button(row3_frame, text="Back to Last Refine", command=self.rollback_refine)
        refine_button.grid(row=0, column=2, sticky="w", padx=(15, 5))
        ToolTip(P1_button, "Restore XDS.INP to the state before running with cell.")
        ToolTip(cell_button, "Restore XDS.INP to the state before running refinement.")
        ToolTip(refine_button, "Restore XDS.INP to the state to last refinement.")

        # Function 3 label
        intro_frame = tk.Frame(self, bg='white')
        intro_frame.grid(row=6, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        instruction_msg = "4. Change image path in XDS.INP (SMV .img only)"
        label = tk.Label(intro_frame, text=instruction_msg, bg='white')
        label.pack(side="left", fill="both", expand=True)  # Ensure it fills the frame horizontally

        # Function 3
        row5_frame = tk.Frame(self, bg='white')
        row5_frame.grid(row=7, column=0, sticky="w", padx=10, pady=sp)
        abs_path_button = tk.Button(row5_frame, text="Absolute Path", command=self.absolute_path)
        abs_path_button.grid(row=0, column=0, sticky="w", padx=(15, 5))
        rel_path_button = tk.Button(row5_frame, text="Relative Path", command=self.relative_path)
        rel_path_button.grid(row=0, column=1, sticky="w", padx=(15, 5))
        ToolTip(abs_path_button, "Change image path in XDS.INP to absolute path.")
        ToolTip(rel_path_button, "Change image path in XDS.INP to relative path..")

        # Function 3 label
        batch_process_frame = tk.Frame(self, bg='white')
        batch_process_frame.grid(row=8, column=0, sticky="w", padx=10, pady=(3 * sp, sp))
        instruction_msg = "5. Batch operate on XDS.INP files."
        label = tk.Label(batch_process_frame, text=instruction_msg, bg='white')
        label.pack(side="left", fill="both", expand=True)  # Ensure it fills the frame horizontally

        # Function 3
        row9_frame = tk.Frame(self, bg='white')
        row9_frame.grid(row=9, column=0, sticky="w", padx=10, pady=sp)
        delete_xds_button = tk.Button(row9_frame, text="Delete XDS", command=self.confirm_delete_xds, bg="#f3e3e3")
        delete_xds_button.grid(row=0, column=1, sticky="w", padx=25, pady=sp)
        ToolTip(delete_xds_button, "CAUTION! It will delete all XDS.INP with corresponding result files!")


    def absolute_path(self) -> None:
        """Update the image paths in XDS.INP files to absolute paths.

        This function searches for all `XDS.INP` files within the specified input path and updates
        the image paths to their absolute locations. It provides user feedback upon successful completion.

        Returns:
            None
        """
        if self.input_path:
            print("Change the input path in XDS.INPs to absolute path ...", end="", flush=True)
            xds_input.change_path_input(self.input_path, "absolute")
            print("\rChange the input path in XDS.INPs to absolute path ... OK\n")
            messagebox.showinfo("Caution", "The image path is updated successfully.")

    def relative_path(self) -> None:
        """Update the image paths in XDS.INP files to relative paths.

        This function searches for all `XDS.INP` files within the specified input path and updates
        the image paths to be relative to the input directory. It provides user feedback upon successful completion.

        Returns:
            None
        """
        if self.input_path:
            print("Change the input path in XDS.INPs to relative path ...", end="", flush=True)
            xds_input.change_path_input(self.input_path, "relative")
            print("\rChange the input path in XDS.INPs to relative path ... OK\n ")
            messagebox.showinfo("Caution", "The image path is updated successfully.")

    def select_path(self) -> None:
        """Open a directory browser dialog for selecting the input path.

        Allows the user to browse and select a directory containing XDS datasets. The selected path
        is then displayed in the corresponding entry widget for REDp generation.

        Returns:
            None
        """
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def load_path(self) -> None:
        """Start the REDp file generation process for the selected input path.

        Retrieves the input path from the entry widget, verifies its validity, and initiates a separate
        thread to generate REDp files. It also starts an animation to indicate the ongoing process.

        Returns:
            None
        """
        input_path = self.path_entry.get()
        if input_path and os.path.isdir(input_path):
            self.mrc_process_animation_active = True
            self.thread["conversion_thread_redp"] = threading.Thread(target=image_io.generate_redp, args=(input_path,))
            self.thread["conversion_thread_redp"].start()
            self.mrc_process_animate()

    def mrc_process_animate(self) -> None:
        """Animate the REDp file generation process in the GUI.

        Continuously updates the animation canvas to provide visual feedback to the user while
        the REDp generation thread is active. Stops the animation once the process is complete.

        Returns:
            None
        """
        if self.mrc_process_animation_active:
            self.animation_canvas.delete("all")
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.animation_canvas.create_arc(arc_x0, arc_y0, arc_x1, arc_y1, start=self.mrc_process_animation_angle,
                                             extent=120, style=tk.ARC)
            self.animation_canvas.create_text(50, 10, text="Running... ", anchor="w")
            self.mrc_process_animation_angle = (self.mrc_process_animation_angle + 10) % 360
            if self.thread["conversion_thread_redp"].is_alive():
                self.after(100, self.mrc_process_animate)
            else:
                self.stop_mrc_process_animation()

    def stop_mrc_process_animation(self) -> None:
        """Stop the REDp process animation and clear the animation canvas.

        This function is called once the REDp generation process is complete to remove the animation.

        Returns:
            None
        """
        self.mrc_process_animation_active = False
        self.animation_canvas.delete("all")

    def rollback_P1(self) -> None:
        """Rollback XDS.INP files to the "P1 stage" using backup files.

        Prompts the user for confirmation and, upon acceptance, restores `XDS.INP` files from their
        "BACKUP-P1" counterparts within the specified input path.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        response = messagebox.askyesno("Warning", "Warning! Do you want to Rollback File to P1 stage?")
        if response:
            xds_files = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
            for xds_path in xds_files:
                backup_path = os.path.join(os.path.dirname(xds_path), "BACKUP-P1")
                if os.path.isfile(backup_path):
                    shutil.copy(backup_path, xds_path)
                    print(f"Copied {backup_path} to {xds_path}")

    def rollback_cell(self) -> None:
        """Rollback XDS.INP files to the "Cell stage" or "P1 stage" if applicable.

        Prompts the user for confirmation and, upon acceptance, restores `XDS.INP` files from their
        "BACKUP-CELL" or "BACKUP-P1" counterparts within the specified input path.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        response = messagebox.askyesno("Warning", "Warning! Do you want to Rollback File to Cell stage?")
        if response:
            xds_files = find_files(self.input_path, "XDS.INP", path_filter=path_filter)
            for xds_path in xds_files:
                backup_cell_path = os.path.join(os.path.dirname(xds_path), "BACKUP-CELL")
                backup_P1_path = os.path.join(os.path.dirname(xds_path), "BACKUP-P1")
                if os.path.isfile(backup_cell_path):
                    shutil.copy(backup_cell_path, xds_path)
                    print(f"Copied {backup_cell_path} to {xds_path}")
                elif os.path.isfile(backup_P1_path):
                    shutil.copy(backup_P1_path, xds_path)
                    print(f"Copied {backup_P1_path} to {xds_path}")

    def rollback_refine(self) -> None:
        """Rollback XDS.INP files to the latest refinement stage using backup files.

        Prompts the user for confirmation and, upon acceptance, restores `XDS.INP` files from their
        "BACKUP-REFINE" counterparts within the specified input path.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        response = messagebox.askyesno("Warning", "Warning! Do you want to Rollback File to Last Refine?")
        if response:
            xds_files = find_files(self.input_path, "XDS.INP")
            for xds_path in xds_files:
                backup_path = os.path.join(os.path.dirname(xds_path), "BACKUP-REFINE")
                if os.path.isfile(backup_path):
                    shutil.copy(backup_path, xds_path)
                    print(f"Copied {backup_path} to {xds_path}")

    def select_path_pets(self) -> None:
        """Open a directory browser dialog for selecting the input path for PETS generation.

        Allows the user to browse and select a directory containing `.mrc` files. The selected path
        is then displayed in the corresponding entry widget for PETS input file generation.

        Returns:
            None
        """
        path = filedialog.askdirectory()
        self.path_entry_pets.delete(0, tk.END)
        self.path_entry_pets.insert(0, path)

    def load_path_pets(self) -> None:
        """Start the PETS input file generation process for the selected input path.

        Retrieves the input path and overwrite option from the GUI, verifies the path's validity,
        and initiates a separate thread to generate PETS input files. It also starts an animation
        to indicate the ongoing process.

        Returns:
            None
        """
        input_path = self.path_entry_pets.get()
        if input_path and os.path.isdir(input_path):
            self.pets_process_animation_active = True
            self.thread["conversion_thread_pets"] = threading.Thread(target=generate_pets.run_pets_function,
                                                                     args=(input_path, self.overwrite.get()))
            self.thread["conversion_thread_pets"].start()
            self.pets_process_animate()

    def pets_process_animate(self) -> None:
        """Animate the PETS file generation process in the GUI.

        Continuously updates the animation canvas to provide visual feedback to the user while
        the PETS generation thread is active. Stops the animation once the process is complete.

        Returns:
            None
        """
        if self.pets_process_animation_active:
            self.animation_canvas_pets.delete("all")
            arc_x0, arc_y0, arc_x1, arc_y1 = 10, 2, 30, 20
            self.animation_canvas_pets.create_arc(arc_x0, arc_y0, arc_x1, arc_y1,
                                                  start=self.pets_process_animation_angle, extent=120, style=tk.ARC)
            self.animation_canvas_pets.create_text(50, 10, text="Running... ", anchor="w")
            self.pets_process_animation_angle = (self.pets_process_animation_angle + 10) % 360
            if self.thread["conversion_thread_pets"].is_alive():
                self.after(100, self.pets_process_animate)
            else:
                self.stop_pets_process_animation()

    def stop_pets_process_animation(self) -> None:
        """Stop the PETS process animation and clear the animation canvas.

        This function is called once the PETS generation process is complete to remove the animation.

        Returns:
            None
        """
        self.mrc_process_animation_active = False
        self.animation_canvas_pets.delete("all")

    def confirm_delete_xds(self) -> None:
        """Display a confirmation dialog to delete all XDS-related files.

        Prompts the user with a warning dialog to confirm the deletion of all XDS.INP files and
        their associated result files within the specified input path. If confirmed, initiates
        the deletion process.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        # Display confirmation dialog for deleting xds files.
        response = messagebox.askyesno("Warning", "Warning! All xds files will be deleted. Are you sure?")
        if response:
            self.run_delete_xds_script()

    def run_delete_xds_script(self) -> None:
        """Run the deletion process for all XDS.INP files in the specified input path.

        Initiates a separate thread to execute the deletion of XDS.INP files using the
        `xds_input.delete_xds` function. Provides user feedback upon completion.

        Returns:
            None
        """
        if not self.input_path:
            print("Input path is not set. Please set the input path first.")
            return
        self.thread["delete_xds"] = threading.Thread(target=xds_input.delete_xds, args=(self.input_path,))
        self.thread["delete_xds"].start()
