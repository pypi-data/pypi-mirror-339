"""
AutoLEI Graphical User Interface (GUI) Module
=============================================

This module provides a graphical user interface for the AutoLEI application, an integrated
tool for crystallographic data processing and analysis. The GUI is designed to enhance user
experience by offering an intuitive interface for interacting with AutoLEI's core functionalities.

The module supports dataset management, real-time monitoring of XDS processes, and easy access
to key settings and tools required for crystallographic data processing.

Features:
- Adjustable scaling for high-resolution displays.
- Integration with various AutoLEI processing modules.
- Multi-tabbed interface for seamless navigation.
- Robust error handling and user prompts.

Attributes:
    config (configparser.ConfigParser): Parses and reads the AutoLEI configuration file.
    script_dir (str): The directory where the script is located.

Classes:
    AutoLei: Main GUI application class that handles the primary window and user interaction.

Functions:
    start_gui(): Launches the AutoLEI GUI.
    main(): Entry point for the application.
    setting(): Opens the `setting.ini` file for editing.
    add_instrument(file_name: str): Adds an instrument profile to the AutoLEI instrument directory.

Notes:
    - The `setting.ini` file must be properly configured and located in the script directory.
    - XDS software must be installed and available in the system path.
    - Designed to support high-resolution displays through automatic scaling adjustments.

Dependencies:
    - Standard Libraries:
        - configparser
        - multiprocessing
        - os
        - shutil
        - subprocess
        - sys
        - warnings
    - Third-Party Libraries:
        - tkinter
        - screeninfo

Contact:
    - Lei Wang: lei.wang@mmk.su.se
    - Yinlin Chen: yinlin.chen@mmk.su.se

License:
    BSD 3-Clause License
"""

import configparser
import multiprocessing
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)

import os.path
import sys
from multiprocessing import Process
from tkinter import font, messagebox
from screeninfo import get_monitors, ScreenInfoError

try:
    from .src.util import *
    from .realtime import RealTime
    from .tool import Tools
    from .autolei_core import Input, XDSRunner, UnitCellCorr, XDSRefine, MergeData, Cluster_Output
except ImportError:
    from src.util import *
    from realtime import RealTime
    from tool import Tools
    from autolei_core import Input, XDSRunner, UnitCellCorr, XDSRefine, MergeData, Cluster_Output

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, 'setting.ini'))


# Main window class
class AutoLei(tk.Tk):
    """
    A class representing the main GUI application for AutoLEI.

    AutoLEI is an interactive application designed to facilitate dataset
    processing, unit cell refinement, merging of data, and various other
    scientific computations. This class handles the initialization and
    configuration of the GUI, including the creation of multiple tabs
    for different functionalities. It uses the tkinter library for
    the graphical interface and ttk for styling.

    Attributes:
        sf (float): Scaling factor for GUI elements based on screen resolution.
        notebook (ttk.Notebook): The main tabbed interface for the application.
        dataset_counts (int): Number of datasets currently loaded.
        input_path (str or None): The current directory path being processed by the application.
        pages (dict): Dictionary of instantiated pages for different functionalities.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the AutoLEI GUI application.

        Arguments:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.title("AutoLEI 1.0.1")
        sf = self.adjust_scaling()
        window_width = int(1100 * sf)
        window_height = int(760 * sf)
        self.geometry(f'{window_width}x{window_height}')

        if config["General"]["window_scaling"] == "True":
            self.sf = sf ** 0.4
        else:
            self.sf = 1
        self.call('tk', 'scaling', sf)

        # Configure styles
        style = ttk.Style()
        style.theme_use('alt')

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Liberation Sans", size=int(15 * self.sf))
        self.option_add("*Font", default_font)

        style.configure(
            "TNotebook.Tab",
            font=("Liberation Sans", int(16 * self.sf), "bold"),
            padding=[20 * self.sf, 6 * self.sf, 20 * self.sf, 6 * self.sf]
        )

        # Create the notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Initialisation
        self.dataset_counts = 0
        self.input_path = None
        self.check_XDS()

        # Create pages and add them to the notebook
        self.pages = {}
        page_name_mapping = {
            "Input": "Input",
            "XDSRunner": "XDSRunner",
            "UnitCellCorr": "CellCorr",
            "XDSRefine": "XDSRefine",
            "MergeData": "DataMerge",
            "Cluster_Output": "Cluster&Output",
            "Tools": "Expert",
            "RealTime": "RealTime",
        }

        page_classes = [Input, XDSRunner, UnitCellCorr, XDSRefine, MergeData, Cluster_Output, Tools, RealTime]

        for F in page_classes:
            page = F(parent=self.notebook)
            self.pages[F.__name__] = page
            # Use the mapping to set the page name
            page_name = page_name_mapping.get(F.__name__, F.__name__)  # Fallback to class name if not in mapping
            self.notebook.add(page, text=page_name)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_input_path(self, path: str):
        """Set the input path and update pages accordingly.

        Arguments:
            path (str): The directory path to be set as input.
        """
        self.input_path = path  # refresh path
        for page_name, page in self.pages.items():
            if hasattr(page, 'input_path'):
                page.input_path = path
        os.chdir(path)
        self.update_title()
        if os.path.isdir(os.path.join(path, "merge")):
            self.pages["Cluster_Output"].update_path_dict()
        if os.path.isfile(os.path.join(path, "online.json")) or os.path.isfile(os.path.join(path, "realtime.json")):
            self.pages["RealTime"].update_display_initial()

    def update_title(self):
        """Update the application title to reflect the current input path and dataset count."""
        if self.input_path:
            self.title(f"AutoLEI 1.0.1 - {self.input_path} - {self.dataset_counts} datasets")
        else:
            self.title("AutoLEI 1.0.1")

    def on_close(self):
        """Handle the application close event.

        Prompts the user to confirm before closing the application.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to close the window? Realtime monitor will disconnect."):
            if "realtime" in self.pages["RealTime"].thread and self.pages["RealTime"].thread["realtime"].is_alive():
                self.pages["RealTime"].thread["realtime"].terminate()
            self.destroy()

    def check_XDS(self):
        """Check if the XDS program is available in the system path.

        Warns the user if the program is missing.

        Returns:
            bool: True if the check passes, otherwise exits the application.
        """
        if not shutil.which("xds") and sys.platform.startswith("linux"):
            response = messagebox.askyesno(
                "Warning",
                "XDS not existing! Do you wish to continue?",
                icon='warning',
                parent=self
            )
            if not response:
                self.destroy()
        return True

    @classmethod
    def get_monitors_safe(cls, queue: multiprocessing.Queue):
        """Safely retrieve monitor information.

        Arguments:
            queue (multiprocessing.Queue): Queue to store monitor information or errors.
        """
        try:
            monitors = get_monitors()
            queue.put(("success", monitors))
        except Exception as e:
            queue.put(("error", str(e)))

    def adjust_scaling(self) -> float:
        """Adjust GUI scaling based on the screen size or user preferences.

        Returns:
            float: The calculated scaling factor.
        """
        try:
            window_scaling_enabled = strtobool(config["General"]["window_scaling"])
        except (ValueError, KeyError) as e:
            print(f"[Error] Invalid configuration for 'window_scaling': {e}. Using default scaling (1.0).")
            return 1.0

        if not window_scaling_enabled:
            return 1.0

        # Step 2: Check if a specific scaling factor is set
        set_scaling = config["General"].get("set_scaling", "0")
        if set_scaling != "0":
            try:
                scaling = float(set_scaling)
                if scaling <= 0:
                    raise ValueError("Scaling factor must be positive.")
                self.call('tk', 'scaling', scaling)
                print(f"[Info] Applied user-specified scaling factor: {scaling}")
                return scaling
            except ValueError:
                print("[Error] Invalid 'set_scaling' value. Using default scaling (1.0).")
                return 1.0

        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=self.get_monitors_safe, args=(queue,))
        p.start()
        try:
            p.join(timeout=1)
            if p.is_alive():
                print("[Warning] get_monitors() timed out. Terminating process and falling back to Tkinter methods.")
                p.terminate()
                p.join()
                raise TimeoutError("get_monitors() timed out.")

            status, result = queue.get_nowait()
            if status == "success":
                monitors = result
                if not monitors:
                    raise ScreenInfoError("No monitors detected.")
                primary_monitor = monitors[0]
                screen_width = primary_monitor.width
                screen_height = primary_monitor.height
                print(f"[Info] Retrieved monitor dimensions via screeninfo: {screen_width}x{screen_height}")
            else:
                raise ScreenInfoError(result)

        except Exception as e:
            p.terminate()
            print(
                f"[Warning] Failed to retrieve monitor information via screeninfo{e}. Falling back to Tkinter methods.")
            screen_width = None
            screen_height = None

        if screen_width is None or screen_height is None:
            try:
                # Ensure the Tkinter window is updated to get accurate screen dimensions
                self.update_idletasks()
                self.update()

                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()

                print(f"[Info] Retrieved screen dimensions via Tkinter: {screen_width}x{screen_height}")
            except Exception as e:
                print(f"[Error] Failed to retrieve screen information via Tkinter: {e}. Using default scaling (1.0).")
                return 1.0

        # Step 5: Calculate scaling factor based on screen size
        try:
            reference_width = 1920
            reference_height = 1080

            scaling_factor_width = screen_width / reference_width
            scaling_factor_height = screen_height / reference_height

            # Choose the smaller scaling factor to ensure UI elements fit
            scaling_factor = min(scaling_factor_width, scaling_factor_height)

            # Clamp the scaling factor between 1.0 and 2.0
            scaling_factor = max(1.0, min(scaling_factor, 2.0))

            # Apply the scaling factor
            self.call('tk', 'scaling', scaling_factor)
            print(f"[Info] Applied scaling factor: {scaling_factor:.2f}")

            return scaling_factor

        except Exception as e:
            print(f"[Error] Failed to calculate or apply scaling factor: {e}. Using default scaling (1.0).")
            return 1.0


def start_gui() -> None:
    """Start the AutoLEI GUI application."""
    app = AutoLei()
    app.mainloop()


def main() -> None:
    """Main entry point for the AutoLEI application.

    Displays version information and launches the GUI.
    """
    print("Report bug: \nlei.wang@mmk.su.se\nyinlin.chen@mmk.su.se\n")

    print("AutoLEI version 1.0.1, build date 2025-03-01")
    print("Welcome using AutoLEI!\n")

    # Run the GUI in a separate process
    gui_process = Process(target=start_gui)
    gui_process.start()
    gui_process.join()


def setting():
    """Open the AutoLEI settings file for editing."""
    print("You will change the setting file of AutoLEI.")
    setting_path = os.path.join(os.path.dirname(__file__), 'setting.ini')
    subprocess.run(['nano', setting_path])


def add_instrument(file_name: str) -> None:
    """Add an instrument profile to the AutoLEI instrument directory.

    Arguments:
        file_name (str): Path to the instrument profile file.
    """
    src = file_name
    dest_dir = os.path.join(os.path.dirname(__file__), 'instrument_profile')
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest = os.path.join(dest_dir, os.path.basename(file_name))
    shutil.copyfile(src, dest)
    print(f"Copied {src} to AutoLEI Instrument Files.")


if __name__ == "__main__":
    main()
