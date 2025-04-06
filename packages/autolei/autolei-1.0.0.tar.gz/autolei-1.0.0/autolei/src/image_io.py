"""
Image IO Module
===============

This module provides a set of functions and utilities for processing, converting, and analyzing MRC, NXS, and IMG files,
specifically for electron diffraction (ED) data.

Overview:
    - Supports various image formats used in electron diffraction (ED).
    - Provides functions for loading, extracting, and converting MRC and NXS files.
    - Facilitates REDp and ED3D generation.
    - Includes tools for beam center and beam stop analysis.
    - Enables parallel processing for large datasets.

Features:
    - Process and convert MRC files to IMG format.
    - Analyze beam center and beam stop positions in diffraction images.
    - Generate `.ed3d` files for Rotation Electron Diffraction analysis.
    - Convert NeXus (NXS) files to IMG format.
    - Support for multi-threading to enhance performance.

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen and Lei Wang
    - License: BSD 3-clause

Dependencies:
    - Standard libraries:
        - glob, random, concurrent.futures, os, re
    - Third-party libraries:
        - `fabio`, `mrcfile`, `h5py`, `scipy`, `skimage`, `numpy`, `tqdm`
    - Custom modules:
        - `.util` (for sorting, path conversion)
        - `.xds_input` (for handling XDS.INP files)
"""

import configparser
import glob
import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from tkinter import messagebox

import fabio
import h5py
import mrcfile
from fabio import adscimage
from pkg_resources import parse_version
from scipy import ndimage
from scipy.ndimage import binary_closing
from scipy.optimize import minimize
from skimage import exposure, measure, filters, draw
from skimage.morphology import remove_small_objects
from tqdm import tqdm

from .util import *
from .xds_input import get_xds_inp_image_dict, replace_value, extract_keywords

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(script_dir), 'setting.ini'))

set_max_worker = int(config["General"]["max_core"])

if not strtobool(config["General"]["multi-process"]):
    set_max_worker = 1

# wavelength for different voltage
WAVELENGTHS = {
    '400': 0.016439,
    '300': 0.019687,
    '200': 0.025079,
    '150': 0.029570,
    '120': 0.033492,
    '100': 0.037014,
    '400000.0': 0.016439,
    '300000.0': 0.019687,
    '200000.0': 0.025079,
    '150000.0': 0.029570,
    '120000.0': 0.033492,
    '100000.0': 0.037014,
}


# ****************
# MRC Conversion
# ****************


def head_opener(input_mrc: str, new_version: bool = True) -> dict:
    """
    Extracts header information from an MRC file.

    Args:
        input_mrc (str): Path to the MRC file.
        new_version (bool, optional): Flag indicating the header structure version. Defaults to True.

    Returns:
        dict: Dictionary containing the extracted header information.
    """
    with mrcfile.open(input_mrc, header_only=True) as mrc:
        head_dict = {item: clean_string(str(getattr(mrc.header, item)))
                     for item in mrc.header.dtype.names}

        extended_header = 'indexed_extended_header' if new_version else 'extended_header'
        if mrc.header.exttyp in [b"FEI2", b"FEI1"]:
            for exthead_field in getattr(mrc, extended_header).dtype.names:
                head_dict[exthead_field] = clean_string(str(getattr(mrc, extended_header)[exthead_field][0]))

        return {k: v for k, v in head_dict.items() if v not in ("0", "0.0", "")}


def process_mrc_file(args: tuple) -> None:
    """
    Processes and converts an MRC file to a new format.

    Args:
        args (tuple): Tuple containing:
            - `mrc_path (str)`: Path to the MRC file.
            - `path (str)`: Output directory path.
    """
    mrc_path, path = args
    with mrcfile.open(mrc_path) as mrc:
        data = mrc.data
        mrcfile.new(os.path.join(path, 'redp', os.path.basename(mrc_path)), data, overwrite=True)


def process_single_mrc_file(
        mrc_path: str,
        new_prefix: str,
        digit: int,
        start_index: int,
        min_val: float,
        scale: float) -> tuple:
    """
    Converts a single MRC file to IMG format.

    Args:
        mrc_path (str): Path to the MRC file.
        new_prefix (str): Prefix for the output IMG files.
        digit (int): Number of digits in the filename index.
        start_index (int): Starting index for the filenames.
        min_val (float): Minimum value for scaling.
        scale (float): Scaling factor.

    Returns:
        tuple: Tuple containing the MRC file path and a boolean indicating success.
    """

    def conditional_update(dictionary, key, value):
        if value is not None and value != "":
            dictionary[key] = value

    with mrcfile.open(mrc_path) as mrc:
        img_data = mrc.data
    header = head_opener(mrc_path, parse_version(mrcfile.__version__) >= parse_version("1.5.0"))

    # Avoid division by zero in case min_val equals max_val
    pedestal = np.flip((img_data - min_val) / scale, axis=0)
    pedestal[pedestal > 65000] = 65000
    pedestal[pedestal < 0] = 0

    img = fabio.adscimage.AdscImage(data=pedestal.astype(np.uint16))
    conditional_update(img.header, 'SIZE1', header["nx"])
    conditional_update(img.header, 'SIZE2', header["ny"])

    bin_value = header.get("Binning Width", "1") + "x" + header.get("Binning Height", "1")
    if bin_value != "1x1":
        img.header['BIN'] = bin_value

    img.header['BIN_TYPE'] = "HW"

    timestamp = header.get("Timestamp", 0)
    if timestamp:
        img.header['DATE'] = timestamp_string(float(timestamp))

    conditional_update(img.header, 'TIME', header.get("Integration time", None))
    conditional_update(img.header, 'BEAMLINE', header.get("Microscope type", None))
    conditional_update(img.header, 'DETECTOR', header.get("Camera name", None))
    conditional_update(img.header, 'PEDESTAL', int(-min_val / scale))

    ht_value = header.get("HT", "0.0")
    if ht_value != "0.0":
        img.header['WAVELENGTH'] = WAVELENGTHS[ht_value]

    conditional_update(img.header, 'SPOT_SIZE', header.get("Spot index", None))

    alpha_value = header.get("Alpha tilt", 0)
    if alpha_value:
        img.header['PHI'] = "{:.4f}".format(float(alpha_value))

    if 'exttyp' in header and header['exttyp'] == "FEI2":
        img.header.update({
            "OSC_START": "{:.4f}".format(
                float(header.get("Alpha tilt", 0.0)) - float(header.get("Tilt per image", 0.0))),
            "OSC_RANGE": "{:.4f}".format(float(header.get("Tilt per image", 0.0)))
        })
    if 'Camera name' in header and header['Camera name'] == "BM-Ceta":
        img.header.update({"PIXEL_SIZE": int(header.get("Binning Width", "1")) * 0.014,
                           "DISTANCE": "{:.2f}".format(0.014 * 10 ** 10 * int(header["Binning Width"]) /
                                                       WAVELENGTHS[ht_value] / float(header['Pixel size X']))
                           })

    new_filename = f"{new_prefix}{str(start_index).zfill(digit)}.img"
    img.write(new_filename)
    return mrc_path, True


def conversion_mrc_file(
        mrc_files: list,
        new_prefix: str,
        digit: int,
        max_worker: int = set_max_worker) -> int:
    """
    Converts multiple MRC files to IMG format using parallel processing.

    Args:
        mrc_files (list): List of MRC files to convert.
        new_prefix (str): Prefix for the output filenames.
        digit (int): Number of digits in the filename index.
        max_worker (int, optional): Maximum number of threads to use. Defaults to `set_max_worker`.

    Returns:
        int: Number of successfully converted files.
    """
    results = []
    start_index = 1

    with mrcfile.open(mrc_files[-9]) as mrc:
        img_data = mrc.data
        min_val = np.min(img_data)
        scale = ((np.max(img_data) - np.min(img_data)) / 65536) if (np.max(img_data) - np.min(img_data)) > 65000 else 1
        if scale > 3:
            scale = 1

    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        # Submit all MRC files for conversion in parallel
        future_to_mrc = {
            executor.submit(process_single_mrc_file, mrc_path, new_prefix, digit, start_index + i, min_val, scale):
                mrc_path for i, mrc_path in enumerate(mrc_files)}
        for future in tqdm(as_completed(future_to_mrc), total=len(mrc_files), desc="Converting", ascii=True):
            mrc_path = future_to_mrc[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{mrc_path} generated an exception: {exc}')
    # Log the results
    converted_count = sum(1 for _, converted in results if converted)
    print(f"{converted_count} of {len(mrc_files)} converted.\n")
    return converted_count


def convert_mrc2img(directory: str, path_filter: bool = False) -> None:
    """
    Converts all MRC files in a directory to IMG format.

    Args:
        directory (str): Directory containing MRC files.
        path_filter (bool, optional): Flag to filter paths during conversion. Defaults to False.
    """
    print("********************************************")
    print("*             MRC to SMV Image             *")
    print("********************************************\n")
    if not directory:
        print("No directory selected. Exiting.")
        return None
    """ Convert all .mrc files in a directory to .img format, with checks for specific conditions. """
    folder_paths = find_folders_with_images(directory, extension=".mrc", path_filter=path_filter)

    for path in folder_paths:
        # Check if directory is collected by specific criteria or has already been converted
        parent_folder = os.path.dirname(path)
        cred_log_path = os.path.join(parent_folder, 'cRED_log.txt')
        print(f"Entering Folder {path}")

        # Skip if path is specifically an 'redp' output directory or has a corresponding cRED log
        if path.endswith("redp") or os.path.isfile(cred_log_path) or path.lower().endswith("atlas"):
            continue

        mrc_files = sorted(glob.glob(os.path.join(path, '*.mrc')), key=natural_sort_key)

        file_groups = {}
        for file in mrc_files:
            filename = os.path.basename(file)

            # Check if the filename ends with a digit before .mrc
            if re.search(r'\d+\.mrc$', filename):
                length = len(filename)

                # Group files based on the length of the filename
                if length not in file_groups:
                    file_groups[length] = [file]
                else:
                    file_groups[length].append(file)

        # Find the largest group based on the number of files
        max_group_size = 0
        max_group = []

        for length, files in file_groups.items():
            if len(files) > max_group_size:
                max_group_size = len(files)
                max_group = files

        # mrc_files now contains only files from the largest group by filename length
        mrc_files = sorted(max_group, key=natural_sort_key)

        img_files = sorted(glob.glob(os.path.join(os.path.join(parent_folder, 'SMV', 'data'), '*.img')),
                           key=natural_sort_key)
        if not img_files:
            img_files = sorted(glob.glob(os.path.join(path, '*.img')), key=natural_sort_key)

        # Check if the count of .img files matches the count of .mrc files, indicating conversion might already be done
        if len(img_files) >= len(mrc_files):
            print(f"Directory {path} don't need to convert.\n")
            continue

        file_base_name, first, last = extract_pattern(mrc_files)
        digit = file_base_name.count("?") if last not in [9, 99, 999] else file_base_name.count("?") + 1
        new_prefix = extract_pattern(mrc_files)[0].split("?")[0] \
            if last not in [9, 99, 999] else extract_pattern(mrc_files)[0].split("?")[0][:-1]
        # Proceed with conversion if the above conditions are not met
        conversion_mrc_file(mrc_files, new_prefix, digit)
    print("Conversion Finished.\n")


def metadata_input(path_dict: dict, root_dir: str) -> tuple:
    """
    Prompts the user to input metadata for file conversion and updates the provided path dictionary.

    This function creates a GUI window that allows the user to provide metadata such as high voltage (HV),
    pixel size, range start, range end, and camera length for each file path. The user input is validated
    and used to update the `path_dict`.

    Args:
        path_dict (dict): Dictionary containing metadata for each file path. Keys represent paths,
                          and values include file details like relative path and frame count.
        root_dir (str): Root directory containing the files.

    Returns:
        tuple: A tuple containing:
            - Updated `path_dict` (dict) with user-provided metadata.
            - `wavelength` (float) calculated from the input HV.
            - `pixel_size` (float) in micrometers.

            If the user cancels the operation, returns `(None, None, None)`.
    """
    result = (None, None, None)

    if os.path.isfile(os.path.join(root_dir, "Input_parameters.txt")):
        with open(os.path.join(root_dir, "Input_parameters.txt")) as file:
            keyword = extract_keywords(file.readlines())
            cl_default = keyword.get("DETECTOR_DISTANCE", [""])[0]
            wavelength_default = keyword.get("X-RAY_WAVELENGTH", [""])[0]
            pixel_size_default = keyword.get("QX", [""])[0]
    else:
        cl_default = ""
        wavelength_default = ""
        pixel_size_default = ""
    try:
        h, m0, c, e = 6.62607015e-34, 9.10938356e-31, 2.99792458e8, 1.602176634e-19
        voltage = round((np.sqrt(
            (m0 * c ** 2) ** 2 + (h * c / (float(wavelength_default) * 1e-10)) ** 2) - m0 * c ** 2) / e / 1e4) * 10
        HV_default = str(voltage)
    except Exception as exc:
        HV_default = ""
    metadata_window = tk.Toplevel()
    metadata_window.title("Metadata Input")
    metadata_window.resizable(True, True)
    metadata_window.configure(bg="#f3f3f3")

    # Set a larger minimum size for the window
    metadata_window.geometry("750x700")  # Width x Height

    def on_close():
        nonlocal result
        metadata_window.destroy()
        result = (None, None, None)

    metadata_window.protocol("WM_DELETE_WINDOW", on_close)

    # Make the window modal
    metadata_window.grab_set()

    # Configure grid layout with padding
    for i in range(5):
        metadata_window.columnconfigure(i, weight=1, pad=10)
    metadata_window.rowconfigure(2, weight=1)

    # Initialize ttk Style
    style = ttk.Style()
    style.theme_use('alt')  # Use a theme that allows background customization

    # Define custom fonts
    regular_font = ("Liberation Sans", 12)
    header_font = ("Liberation Sans", 13, "bold")

    # Configure styles for ttk widgets
    style.configure("TLabel", font=regular_font)
    style.configure("TEntry", font=regular_font, fieldbackground="#ffffff")
    style.configure("TButton", font=("Liberation Sans", 16, "bold"))

    # Create a frame for the first line to use grid layout
    hv_frame = tk.Frame(metadata_window, bg="#f3f3f3")
    hv_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5), columnspan=5)

    hv_label = tk.Label(hv_frame, text="HV", bg="#f3f3f3")
    hv_label.pack(side='left', padx=5)

    hv_var = tk.StringVar(value=HV_default)
    hv_entry = tk.Entry(hv_frame, textvariable=hv_var, width=15)
    hv_entry.pack(side='left', padx=5)

    hv_unit_label = tk.Label(hv_frame, text="keV,  Pixel Size", bg="#f3f3f3")
    hv_unit_label.pack(side='left', padx=5)

    pixel_size_var = tk.StringVar(value=pixel_size_default)
    pixel_size_entry = ttk.Entry(hv_frame, textvariable=pixel_size_var, width=15)
    pixel_size_entry.pack(side='left', padx=5)

    pixel_size_unit_label = tk.Label(hv_frame, text="μm", bg="#f3f3f3")
    pixel_size_unit_label.pack(side='left', padx=5)

    # Separator
    separator = ttk.Separator(metadata_window, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=5, sticky='ew', padx=5, pady=5)

    # Frame to contain the path metadata
    metadata_frame = tk.Frame(metadata_window, bg="#f3f3f3")
    metadata_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky='nsew')

    # Add a canvas and scrollbar to handle multiple entries
    canvas = tk.Canvas(metadata_frame, borderwidth=0, bg="#f3f3f3", highlightthickness=0)
    scrollbar = ttk.Scrollbar(metadata_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f3f3f3")

    scrollable_frame.bind(
        "<Configure>",
        lambda x: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header row for metadata entries
    headers = ["Relative Path", "Frames", "Range Start", "Range End", "CL (mm)"]
    for col, header in enumerate(headers):
        header_label = tk.Label(scrollable_frame, text=header, font=header_font, bg="#f3f3f3")
        header_label.grid(row=0, column=col, padx=5, pady=7, sticky='w')

    # Dictionary to hold entry variables for each path
    metadata_entries = {}

    # Populate the scrollable frame with path_dict information
    for idx, (path, info) in enumerate(path_dict.items(), start=1):
        relative_path = info.get("relative_path", "N/A")
        num_frames = info.get("num", 0)
        if os.path.isfile(os.path.join(path, "metadata.txt")):
            meta_path = os.path.join(path, "metadata.txt")
        elif os.path.isfile(os.path.join(os.path.dirname(path), "metadata.txt")):
            meta_path = os.path.join(os.path.dirname(path), "metadata.txt")
        else:
            meta_path = ""
        if meta_path:
            with open(meta_path, "r") as f:
                metadata_dict = extract_keywords(f.readlines())
                start_angle = float(metadata_dict.get("START_ANGLE", [0])[0])
                end_angle = float(metadata_dict.get("END_ANGLE", [0])[0])
                osc_angle = float(metadata_dict.get("OSCILLATION_RANGE", [0])[0])
                if start_angle and not end_angle and osc_angle:
                    end_angle = str(round(start_angle + num_frames * osc_angle, 2))
                    start_angle = str(start_angle)
                elif not start_angle and end_angle and osc_angle:
                    start_angle = str(round(end_angle - num_frames * osc_angle, 2))
                    end_angle = str(end_angle)
                elif start_angle and end_angle:
                    start_angle = str(start_angle)
                    end_angle = str(end_angle)
                else:
                    start_angle = str(start_angle) if start_angle else ""
                    end_angle = str(end_angle) if end_angle else ""
        else:
            start_angle = ""
            osc_angle = ""
            end_angle = ""

        # Relative Path Label
        path_label = tk.Label(scrollable_frame, text=relative_path, wraplength=200, justify='left', bg="#f3f3f3")
        path_label.grid(row=idx, column=0, padx=5, pady=2, sticky='w')

        # Num Frames Label
        num_label = tk.Label(scrollable_frame, text=f"{num_frames}", bg="#f3f3f3")
        num_label.grid(row=idx, column=1, padx=5, pady=2, sticky='w')

        # Range Start Entry
        range_start_var = tk.StringVar(value=start_angle)
        range_start_entry = ttk.Entry(scrollable_frame, textvariable=range_start_var, width=7)
        range_start_entry.grid(row=idx, column=2, padx=5, pady=5, sticky='w')

        # Range End Entry
        range_end_var = tk.StringVar(value=end_angle)
        range_end_entry = ttk.Entry(scrollable_frame, textvariable=range_end_var, width=7)
        range_end_entry.grid(row=idx, column=3, padx=5, pady=5, sticky='w')

        # CL Entry
        cl_var = tk.StringVar(value=cl_default)
        cl_entry = ttk.Entry(scrollable_frame, textvariable=cl_var, width=9)
        cl_entry.grid(row=idx, column=4, padx=5, pady=5, sticky='w')

        # Store the variables for later use
        metadata_entries[path] = {
            'range_start': range_start_var,
            'range_end': range_end_var,
            'cl': cl_var
        }

    # Frame for buttons
    button_frame = tk.Frame(metadata_window, bg="#f3f3f3")
    button_frame.grid(row=3, column=0, columnspan=5, pady=20)

    def on_convert(window, hv_value, pixel_size_value, entries):
        nonlocal result
        hv = hv_value.get().strip()
        pixel_size = pixel_size_value.get().strip()
        if not (hv and pixel_size):
            messagebox.showerror("Error", f"HV or Pixel Size is empty!")
            return
        elif hv not in WAVELENGTHS:
            messagebox.showerror("Error", f"HV not a valid int.")
            return

        updated_path_dict = {}
        for _path, _info in path_dict.items():
            updated_info = _info.copy()
            if _path in entries:
                user_inputs = entries[_path]
                range_start = user_inputs['range_start'].get().strip()
                range_end = user_inputs['range_end'].get().strip()
                cl = user_inputs['cl'].get().strip()

                if cl and range_start and range_end:
                    updated_info['range_start'] = range_start
                    updated_info['osc_range'] = str(round((float(range_end) - float(range_start)) / _info["num"], 4))
                    updated_info['cl'] = cl
                else:
                    messagebox.showerror("Error", f"Some entries in {_path} is empty!")
                    return
            updated_path_dict[_path] = updated_info
        result = (updated_path_dict, WAVELENGTHS[hv], pixel_size)
        window.destroy()

    # "CONVERT" Button
    convert_button = ttk.Button(
        button_frame,
        text="CONVERT",
        style="TButton",
        command=lambda: on_convert(metadata_window, hv_var, pixel_size_var, metadata_entries)
    )
    convert_button.pack(side='left', padx=20)

    # "CANCEL" Button
    cancel_button = ttk.Button(
        button_frame,
        text="CANCEL",
        style="TButton",
        command=on_close
    )
    cancel_button.pack(side='left', padx=20)

    # Center the window on the screen
    metadata_window.update_idletasks()

    # Ensure the window is focused
    metadata_window.focus_set()
    metadata_window.wait_window()

    return result


def get_tiff_size(file_path: str) -> tuple:
    """
    Retrieves the dimensions of a TIFF image.

    Args:
        file_path (str): Path to the TIFF file.

    Returns:
        tuple: Dimensions of the image as (height, width).
    """
    try:
        tiff = fabio.open(file_path)
        return tiff.data.shape
    except Exception as e:
        print(f"Error opening TIFF file: {e}")
        return ()


def write_smv_tiff(
        file_path: str,
        phi: float,
        osc_range: float,
        wavelength: float,
        camera_length: float,
        pixel_size: float,
        image_size: tuple
) -> tuple:
    """
    Writes a TIFF file as an SMV image file.

    Args:
        file_path (str): Path to the TIFF file.
        phi (float): Phi angle for the image.
        osc_range (float): Oscillation range for the image.
        wavelength (float): Wavelength value.
        camera_length (float): Camera length in millimeters.
        pixel_size (float): Pixel size in micrometers.
        image_size (tuple): Size of the image (height, width).

    Returns:
        tuple: File path and success status as a boolean.
    """
    # Open the TIFF file using FabIO
    if not os.path.isfile(file_path):
        data = np.zeros(image_size, dtype=np.uint16)
        time = 0
    else:
        img = fabio.open(file_path)
        data = img.data.astype(np.uint16)
        time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')

    img = adscimage.AdscImage(data=data.astype(np.uint16))

    # Specify output filename with .img extension in the same folder
    base_name = os.path.splitext(file_path)[0]
    output_path = os.path.join(os.path.dirname(file_path), f'{base_name}.img')

    img.header = {
        'DIM': 2,
        'BYTE_ORDER': 'little_endian',
        'TYPE': 'unsigned_short',
        'HEADER_BYTES': 512,
        'DATE': time,
        'WAVELENGTH': wavelength,
        'TIME': 0,
        'PHI': round(phi, 4),
        'OSC_START': round(phi, 4),
        'OSC_RANGE': osc_range,
        'PIXEL_SIZE': pixel_size,
        'DISTANCE': camera_length,
        'Data_type': "unsigned short int"
    }
    # Write the image to an SMV file
    img.write(output_path)
    return file_path, True


def conversion_tiff_file(
        info: dict,
        wl: float,
        px_size: float,
        max_worker: int = set_max_worker
) -> int:
    """
    Converts TIFF files to SMV format using parallel processing.

    Args:
        info (dict): Metadata information for the conversion.
        wl (float): Wavelength value.
        px_size (float): Pixel size in micrometers.
        max_worker (int, optional): Maximum number of threads to use. Defaults to `set_max_worker`.

    Returns:
        int: Number of successfully converted files.
    """

    results = []
    osc_range = float(info["osc_range"])
    start_angle = float(info["range_start"])
    tiff_files = info["image"]
    cl = info["cl"]
    file_base_name = info["file_base_name"]
    first = info["first"]
    last = info["last"]

    placeholder_count = file_base_name.count('?')
    replacement_format = f"{{:0{placeholder_count}d}}"

    file_names = [
        file_base_name.replace('?' * placeholder_count, replacement_format.format(i))
        for i in range(first, last + 1)
    ]
    dimensions = get_tiff_size(file_names[0])
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        future_to_tiff = {
            executor.submit(write_smv_tiff, image_path, start_angle + i * osc_range, osc_range,
                            wl, cl, px_size, (dimensions[0], dimensions[1])):
                image_path for i, image_path in enumerate(file_names)}
        for future in tqdm(as_completed(future_to_tiff), total=len(tiff_files), desc="Converting", ascii=True):
            tiff_path = future_to_tiff[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{tiff_path} generated an exception: {exc}')
    # Log the results
    converted_count = sum(1 for _, converted in results if converted)
    print(f"{converted_count} of {len(tiff_files)} converted.\n")
    return converted_count


def convert_tiff2img(directory: str, path_filter: bool = False) -> None:
    """
    Converts all TIFF files in a directory to IMG format.

    Args:
        directory (str): Directory containing TIFF files.
        path_filter (bool, optional): Flag to filter paths during conversion. Defaults to False.
    """
    print("********************************************")
    print("*            TIFF to SMV Image             *")
    print("********************************************\n")
    if not directory:
        print("No directory selected. Exiting.")
        return None

    folder_paths = find_folders_with_images(directory, extension=".tiff", path_filter=path_filter)

    path_dict = {}

    for path in folder_paths:
        # Check if directory is collected by specific criteria or has already been converted
        parent_folder = os.path.dirname(path)
        cred_log_path = os.path.join(parent_folder, 'cRED_log.txt')

        # Skip if path is specifically an 'redp' output directory or has a corresponding cRED log
        if path.endswith("tiff_image") or os.path.isfile(cred_log_path):
            continue

        tiff_files = sorted(glob.glob(os.path.join(path, '*.tiff')), key=natural_sort_key)

        file_groups = {}
        for file in tiff_files:
            filename = os.path.basename(file)

            if re.search(r'\d+\.tiff$', filename):
                length = len(filename)

                # Group files based on the length of the filename
                if length not in file_groups:
                    file_groups[length] = [file]
                else:
                    file_groups[length].append(file)

        # Find the largest group based on the number of files
        max_group_size = 0
        max_group = []

        for length, files in file_groups.items():
            if len(files) > max_group_size:
                max_group_size = len(files)
                max_group = files

        # tiff_files now contains only files from the largest group by filename length
        tiff_files = sorted(max_group, key=natural_sort_key)

        img_files = sorted(glob.glob(os.path.join(os.path.join(parent_folder, 'SMV', 'data'), '*.img')),
                           key=natural_sort_key)
        if not img_files:
            img_files = sorted(glob.glob(os.path.join(path, '*.img')), key=natural_sort_key)

        # Check if the count of .img files matches the count of .mrc files, indicating conversion might already be done
        if len(img_files) >= len(tiff_files):
            print(f"Directory {path} don't need to convert.\n")
            continue

        file_base_name, first, last = extract_pattern(tiff_files)
        path_dict[path] = {
            "relative_path": os.path.relpath(path, directory),
            "file_base_name": file_base_name,
            "first": first,
            "last": last,
            "num": last - first + 1,
            "frame": len(tiff_files),
            "image": tiff_files,
            "base_name": file_base_name,
        }
    if not path_dict:
        print("No valid tiff documents. Exiting.")
        return
    feedback, wl, px_size = metadata_input(path_dict, directory)
    if not feedback:
        print("Conversion Terminated.\n")
        return
    for path, info in feedback.items():
        print(f"Enter f{path}")
        conversion_tiff_file(info, wl, px_size)
    print("Conversion Finished.\n")
    return


# ****************
# DLS NXS to IMG
# ****************

def read_nxs_file(file_path: str) -> tuple:
    """
    Reads a NeXus (NXS) file and extracts data and metadata.

    Args:
        file_path (str): Path to the NXS file.

    Returns:
        tuple: Tuple containing:
            - `data (numpy.ndarray)`: The image data.
            - `metadict (dict)`: Metadata extracted from the file.
    """
    metadict = {}
    with h5py.File(file_path, 'r') as file:
        # Adjust this path based on the actual structure of your NeXus file
        data = file['/entry/data/data'][()]
        metadict['wavelength'] = float(file['/entry/instrument/beam/incident_wavelength'][()])
        metadict['orgx'] = float(file['/entry/instrument/detector/beam_center_x'][()])
        metadict['orgy'] = float(file['/entry/instrument/detector/beam_center_y'][()])
        metadict['time'] = round(float(file['/entry/instrument/detector/count_time'][()]), 4)
        metadict['detector'] = file['/entry/instrument/detector/description'][()].decode('ascii')
        metadict['camera_length'] = float(file['/entry/instrument/detector/distance'][()]) * 1000
        metadict['pixel_size_x'] = float(file['/entry/instrument/detector/x_pixel_size'][()]) * 1000
        metadict['pixel_size_y'] = float(file['/entry/instrument/detector/y_pixel_size'][()]) * 1000
        metadict['HT'] = int(file['/entry/instrument/detector/photon_energy'][()]) // 1000
        metadict['overload'] = int(file['/entry/instrument/detector/saturation_value'][()])
        metadict['beamline'] = file['/entry/instrument/name'][()].decode('ascii')
        metadict['phi'] = list(file['/entry/data/alpha'][()])
        metadict['start_time'] = file['/entry/start_time'][()].decode('ascii')
    return data, metadict


def write_smv_nxs(img_data: np.ndarray, index: int, metadict: dict, img_folder: str) -> None:
    """
    Writes image data to an SMV file from NXS metadata.

    Args:
        img_data (numpy.ndarray): Image data array.
        index (int): Image index.
        metadict (dict): Metadata dictionary.
        img_folder (str): Directory to save the SMV files.
    """
    # Create a Fabio image object
    file_path = os.path.join(img_folder, f'1_{index + 1:04d}.img')

    pedestal = img_data + 0
    np.clip(pedestal, 0, metadict["overload"], out=pedestal)

    img = adscimage.AdscImage(data=pedestal.astype(np.uint16))
    # Optionally, set the header
    img.header = {
        'DIM': 2,
        'SIZE1': img_data.shape[1],
        'SIZE2': img_data.shape[0],
        'BYTE_ORDER': 'little_endian',
        'TYPE': 'unsigned_short',
        'HEADER_BYTES': 512,
        'DATE': metadict['start_time'],
        'TIME': metadict['time'],
        'BEAMLINE': metadict['beamline'],
        'DETECTOR': metadict['detector'],
        'WAVELENGTH': metadict['wavelength'],
        'PHI': metadict['phi'][index],
        'OSC_START': metadict['phi'][index],
        'OSC_RANGE': metadict['phi'][1] - metadict['phi'][0],
        'PIXEL_SIZE': metadict['pixel_size_x'],
        'DISTANCE': metadict['camera_length'],
        'Data_type': "unsigned short int"
    }
    # Write the image to an SMV file
    img.write(file_path)


def convert_nxs2img(directory: str, path_filter: bool = False) -> None:
    """
    Converts all NXS files in a directory to IMG format.

    Args:
        directory (str): Directory containing NXS files.
        path_filter (bool, optional): Flag to filter paths during conversion. Defaults to False.
    """
    print("********************************************")
    print("*           DLS NXS to SMV Image           *")
    print("********************************************\n")
    if not directory:
        print("No directory selected. Exiting.")
        return

    nxs_folders = find_folders_with_images(directory, extension=".nxs", min_img_count=1, path_filter=path_filter)
    for nxs_folder in nxs_folders:
        nxs_file_path = glob.glob(os.path.join(nxs_folder, '*.nxs'))[0]
        print(f"Convert {nxs_file_path}")
        try:
            data, metadata = read_nxs_file(nxs_file_path)
            num_images = data.shape[0]
        except Exception as exc:
            print(f"{nxs_file_path} reading fail due to {exc}.")
            continue

        img_folder = os.path.join(nxs_folder, "SMV")
        os.makedirs(img_folder, exist_ok=True)
        img_files = sorted(glob.glob(os.path.join(img_folder, '*.img')), key=natural_sort_key)
        if len(img_files) >= num_images:
            print(f"Directory {nxs_folder} is already converted.\n")
            continue

        with ThreadPoolExecutor(max_workers=set_max_worker) as executor:
            futures = [executor.submit(write_smv_nxs, data[i], i, metadata, img_folder) for i in range(num_images)]
            for future in tqdm(as_completed(futures), total=num_images, desc="Converting", ascii=True):
                future.result()
        print("Converted successfully.\n")


# ****************
# REDp input file
# ****************


def generate_redp(input_path: str, max_worker: int = set_max_worker) -> None:
    """
    Generates `.redp` files and organizes metadata for MRC files.

    Args:
        input_path (str): Directory containing MRC files.
        max_worker (int, optional): Maximum number of threads to use. Defaults to `set_max_worker`.
    """

    print("********************************************")
    print("*            REDp ED3D Generator           *")
    print("********************************************\n")
    folder_path = find_folders_with_images(input_path, extension=".mrc")
    for path in folder_path:
        redp_path = os.path.join(path, 'redp')
        os.makedirs(redp_path, exist_ok=True)
        if ([file for file in os.listdir(path) if file.endswith('.ed3d')] or path.endswith("redp")
                or path.lower().endswith("atlas")
                or [file for file in os.listdir(os.path.join(path, 'redp')) if file.endswith('.ed3d')]):
            continue

        mrc_files = sorted(glob.glob(os.path.join(path, '*.mrc')), key=natural_sort_key)
        if not mrc_files:
            continue

        # Create a dictionary to group files by their filename length
        file_groups = {}
        for file in mrc_files:
            filename = os.path.basename(file)

            # Check if the filename ends with a digit before .mrc
            if re.search(r'\d+\.mrc$', filename):
                length = len(filename)

                # Group files based on the length of the filename
                if length not in file_groups:
                    file_groups[length] = [file]
                else:
                    file_groups[length].append(file)

        # Find the largest group based on the number of files
        max_group_size = 0
        max_group = []

        for length, files in file_groups.items():
            if len(files) > max_group_size:
                max_group_size = len(files)
                max_group = files

        # mrc_files now contains only files from the largest group by filename length
        mrc_files = sorted(max_group, key=natural_sort_key)

        tilt_key = ""
        mrc_version_check = parse_version(mrcfile.__version__) >= parse_version("1.5.0")
        rot_dict, wl_list, pixel_list, steps = {}, [], [], []

        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            list(tqdm(executor.map(process_mrc_file, [(mrc_path, path) for mrc_path in mrc_files]),
                      total=len(mrc_files), desc="Converting", ascii=True))
        print("Image has downgraded to the version REDp can read.")

        for mrc_path in mrc_files:
            header = head_opener(mrc_path, new_version=mrc_version_check)
            tilt_key = "Alpha tilt" if "Alpha tilt" in header else "Beta tilt"
            rot_dict[os.path.basename(mrc_path)] = float(header.get(tilt_key, 0.0))
            wl_list.append(WAVELENGTHS[header['HT']])
            pixel_list.append(float(header['Pixel size X']) * 10 ** -10)
            steps.append(float(header["Tilt per image"]))

        with open(os.path.join(redp_path, '1.ed3d'), "w") as out_f:
            out_f.write(f"WAVELENGTH    {wl_list[0]} \n")
            out_f.write(f"CCDPIXELSIZE    {pixel_list[0]}\n")
            rotation_axis = 1.0 if tilt_key == "Alpha tilt" else -89.0
            out_f.write(f"ROTATIONAXIS    {rotation_axis}\n")
            out_f.write(f"GONIOTILTSTEP    {steps[0]:.4f}\n")
            out_f.write("BEAMTILTSTEP    0\nBEAMTILTRANGE    0.000\nSTRETCHINGMP    0.0\nSTRETCHINGAZIMUTH   0.0\n")
            out_f.write("\n\nFILELIST\n")
            sorted_dict = dict(sorted(rot_dict.items(), key=lambda item: item[1]))
            for key, value in sorted_dict.items():
                out_f.write(f"FILE {key} {value:.4f} 0 {value:.4f}\n")
            out_f.write("ENDFILELIST\n\n")
            print(f"redp input for REDp successfully generated in {redp_path}.")


# ****************
# Find Beam Centre
# ****************

def find_direct_beam_center(img_path: str) -> tuple:
    """
    Finds the approximate center of the direct beam in an IMG file.

    Args:
        img_path (str): Path to the IMG file.

    Returns:
        tuple: Tuple containing the X and Y coordinates of the beam center.
    """
    img = fabio.open(img_path)
    img_array = img.data
    max_intensity = np.max(img_array)
    total_points = img_array.size
    num_max_intensity_points = np.sum(img_array == max_intensity)
    if num_max_intensity_points / total_points > 0.02:
        # Set all points with intensity greater than or equal to the max intensity to 1
        img_array[img_array >= max_intensity] = 0
        max_intensity = np.max(img_array)
    max_position = np.unravel_index(np.argmax(img_array), img_array.shape)
    threshold = max_intensity * 0.2
    bright_mask = img_array > threshold
    if np.any(bright_mask):
        center_y, center_x = ndimage.center_of_mass(bright_mask)
    else:
        center_y, center_x = max_position
    return center_x, center_y


def process_folder_beam_centre(img_path: str, xds_path: str, max_files: int = 50) -> None:
    """
    Processes a folder of IMG files to calculate the beam center.

    Args:
        img_path (str): Directory containing IMG files.
        xds_path (str): Path to the XDS.INP file.
        max_files (int, optional): Maximum number of files to process. Defaults to 50.
    """

    img_files = sorted(glob.glob(os.path.join(img_path, '*.img')), key=natural_sort_key)
    if not img_files:
        print("No images found in that folder, please check if your path in XDS.INP is correct.\n")
        return None

    # If there are more than max_files, sample max_files evenly
    if len(img_files) > max_files:
        img_files = random.sample(img_files, max_files)

    with ThreadPoolExecutor(max_workers=set_max_worker) as executor:
        results = list(tqdm(executor.map(find_direct_beam_center, img_files),
                            total=len(img_files), desc="Processing images", ascii=True))

    x_values, y_values = [], []
    for x, y in results:
        if x != 0:
            x_values.append(x)
        if y != 0:
            y_values.append(y)

    x_values_filtered = remove_outliers_iqr(x_values, offset=1)
    y_values_filtered = remove_outliers_iqr(y_values, offset=1)

    # Calculate averages of the filtered values
    if x_values_filtered and y_values_filtered:
        avg_x = sum(x_values_filtered) / len(x_values_filtered)
        avg_y = sum(y_values_filtered) / len(y_values_filtered)
        print(f"Average beam center position: ({avg_x}, {avg_y})")
        update_beam_centers_file(img_path, avg_x, avg_y)
        update_xds_inp(xds_path, avg_x, avg_y)
    else:
        print("Unable to calculate average beam center.")


def update_beam_centers_file(img_directory: str, avr_x: float, avr_y: float) -> None:
    """
    Writes the average beam center to a text file.

    Args:
        img_directory (str): Directory containing IMG files.
        avr_x (float): Average X coordinate of the beam center.
        avr_y (float): Average Y coordinate of the beam center.
    """

    """Write the average beam center to a text file in the image directory."""
    centers_file_path = os.path.join(img_directory, 'direct_beam_centers.txt')
    with open(centers_file_path, 'w') as file:
        file.write(f"Average beam center: ({avr_x}, {avr_y})\n")


def update_xds_inp(xds_inp_path: str, avr_x: float, avr_y: float) -> None:
    """
    Updates the ORGX and ORGY values in the XDS.INP file.

    Args:
        xds_inp_path (str): Path to the XDS.INP file.
        avr_x (float): Average X coordinate of the beam center.
        avr_y (float): Average Y coordinate of the beam center.
    """
    if os.path.exists(xds_inp_path):
        with open(xds_inp_path, 'r', errors="ignore") as file:
            lines = file.readlines()
        lines = [line for line in lines if
                 not line.strip().startswith('ORGX=') and not line.strip().startswith('ORGY=')]
        with open(xds_inp_path, 'w') as file:
            file.writelines(lines)
            file.write(f'ORGX= {avr_x} ORGY= {avr_y}\n')
        print(f"xds.inp successfully updated with ORGX= {avr_x:.2f}, ORGY= {avr_y:.2f}.\n")
    else:
        print(f"xds.inp not found at the expected path: {xds_inp_path}.\n")


def centre_calculate(input_path: str) -> None:
    """
    Calculates the beam center for all IMG files in a directory.

    Args:
        input_path (str): Directory containing IMG files.
    """
    if input_path:
        print("********************************************")
        print("*            Beam Centre Finder            *")
        print("*--------   No Beam Stop Version   --------*")
        print("********************************************\n")

        print(f"Self beam centre finding has received input path: {input_path}")
        paths_dict = get_xds_inp_image_dict(input_path)
        if not paths_dict:
            print("No XDS.inp found.\n")
            return
        for xds_path in paths_dict.keys():
            img_dir = os.path.dirname(paths_dict[xds_path]["image_path"])
            img_format = paths_dict[xds_path]["image_format"]
            if img_format == "SMV":
                print(f"Entering folder: {img_dir}")
                process_folder_beam_centre(img_dir, xds_path)
        print("Beam Centre Finder Complete.\n")
    else:
        print("No input path provided.\n")


def analysis_beam_stop(image_path: str) -> tuple:
    """
    Analyzes an IMG file to find the beam stop position and radius.

    Args:
        image_path (str): Path to the IMG file.

    Returns:
        tuple: (centre, beam_stop_pos, beam_stop_r, angle_degrees) where:
            - centre: (x_center, y_center) of the beam [float, float]
            - beam_stop_pos: (x_pos, y_pos) of the beam stop [float, float]
            - beam_stop_r: radius of the beam stop [float]
            - angle_degrees: angle of the beam stop direction in degrees [float]
            Returns (None, None, None, None) if detection fails.
    """
    # Read image
    image_data = fabio.open(image_path).data.astype(np.uint16)
    # Enhance contrast
    image_data_autocontrast = exposure.equalize_hist(image_data)

    # Apply a high threshold to find bright regions (assumed direct beam area)
    threshold_value = np.percentile(image_data_autocontrast, 97.5)
    binary_image_bright_regions = image_data_autocontrast > threshold_value

    # Label the connected components for bright regions
    label_image_bright = measure.label(binary_image_bright_regions)
    regions_bright = measure.regionprops(label_image_bright)

    if not regions_bright:
        return None, None, None, None

    # Find the largest bright region, assumed the main direct beam area
    largest_bright_region = max(regions_bright, key=lambda r: r.area)
    min_row, min_col, max_row, max_col = largest_bright_region.bbox

    # Center of the main bright region
    centre = (0.5 * (min_col + max_col), 0.5 * (min_row + max_row))

    # Crop out the main bright region
    central_bright_region = image_data_autocontrast[min_row:max_row, min_col:max_col]

    # Prepare an inverted version for subsequent analysis
    inverted_central_bright_region = 1 - central_bright_region

    # Segment out dark regions within the bright region by Otsu's threshold
    otsu_threshold = filters.threshold_otsu(central_bright_region)
    binary_dark_central_otsu = central_bright_region < otsu_threshold

    # Morphological closing to reduce noise, and remove small objects
    binary_dark_central_cleaned = binary_closing(binary_dark_central_otsu, np.ones((3, 3)))
    binary_dark_central_cleaned = remove_small_objects(binary_dark_central_cleaned, min_size=5)

    # Label the connected components (dark patches in the bright region)
    label_image_dark_central_cleaned = measure.label(binary_dark_central_cleaned)
    regions_dark_central_cleaned = measure.regionprops(label_image_dark_central_cleaned)

    if not regions_dark_central_cleaned:
        return None, None, None, None

    # Find the largest dark patch, presumably the beam stop
    largest_dark_patch = max(regions_dark_central_cleaned, key=lambda r: r.area)
    coords = largest_dark_patch.coords

    # Approximate radius of that dark patch (ellipse -> average of major/minor axis)
    yc, xc = np.mean(coords, axis=0)
    a = largest_dark_patch.major_axis_length / 2
    b = largest_dark_patch.minor_axis_length / 2
    refined_circle_radius = (a + b) / 2

    # Refine location using the centroid of the detected region
    cy, cx = largest_dark_patch.centroid
    ig_yc = (cy + yc) / 2
    ig_xc = (cx + xc) / 2

    def intensity_sum(params: tuple) -> float:
        """
        A function to be minimized, summing pixel intensities inside a disk
        of a given radius in the inverted image.

        Args:
            params: (y_center, x_center, radius)

        Returns:
            float: Negative of sum of intensities inside the disk (to maximize).
        """
        _yc, _xc, radius = params
        rr, cc = draw.disk(
            center=(int(_yc), int(_xc)),
            radius=int(radius),
            shape=inverted_central_bright_region.shape
        )
        # The negative sign is because we want to maximize the sum of the
        # (inverted) intensities, which is equivalent to minimizing its negative.
        return -np.sum(inverted_central_bright_region[rr, cc]) / (radius ** 1.8)

    # Use the initial guess for the optimization
    initial_guess = [ig_yc, ig_xc, refined_circle_radius]
    result = minimize(intensity_sum, initial_guess, method='Nelder-Mead', options={'maxiter': 100})
    refined_yc, refined_xc, refined_circle_radius = result.x

    # Convert beam stop position back to the coordinate system of the original image
    beam_stop_pos = (refined_xc + min_col, refined_yc + min_row)
    beam_stop_r = refined_circle_radius + 0.015 * image_data.shape[0]

    # Determine the slope and direction (use negative to measure direction "away" from center)
    angle_radians = np.arctan2(-(refined_yc - ig_yc), -(refined_xc - ig_xc))
    angle_degrees = np.degrees(angle_radians)

    return centre, beam_stop_pos, beam_stop_r, angle_degrees if angle_degrees >= -90 else angle_degrees + 180


def process_folder_beam_stop(img_path: str, xds_path: str, max_files: int = 20) -> None:
    """
    Processes a folder of IMG files to calculate beam stop information.

    Args:
        img_path (str): Directory containing IMG files.
        xds_path (str): Path to the XDS.INP file.
        max_files (int, optional): Maximum number of files to process. Defaults to 20.
    """
    img_files = sorted(glob.glob(os.path.join(img_path, '*.img')), key=natural_sort_key)
    if not img_files:
        print("No images found in that folder, please check if your path in XDS.INP is correct.\n")
        return None

    # If there are more than max_files, sample max_files evenly
    if len(img_files) > max_files + 100:
        img_files = random.sample(img_files[10:-10], max_files + 20)
    elif len(img_files) > max_files + 50:
        img_files = random.sample(img_files[10:-10], max_files + 10)
    elif len(img_files) > max_files + 20:
        img_files = random.sample(img_files[10:-10], max_files)
    elif len(img_files) > max_files + 10:
        img_files = random.sample(img_files[5:-5], max_files)
    elif len(img_files) > max_files:
        img_files = random.sample(img_files, max_files)

    size = fabio.open(img_files[0]).data.shape[0]

    with ThreadPoolExecutor(max_workers=set_max_worker) as executor:
        results = list(tqdm(executor.map(analysis_beam_stop, img_files),
                            total=len(img_files), desc="Processing images", ascii=True))

    centre_xs, centre_ys, beam_stop_pos_xs, beam_stop_pos_ys, beam_stop_rs, angle_degrees = [], [], [], [], [], []
    for centre, beam_stop_pos, beam_stop_r, angle in results:
        if centre:
            centre_xs.append(centre[0])
            centre_ys.append(centre[1])
        if beam_stop_pos:
            beam_stop_pos_xs.append(beam_stop_pos[0])
            beam_stop_pos_ys.append(beam_stop_pos[1])
        if beam_stop_r:
            beam_stop_rs.append(beam_stop_r)
        if angle:
            angle_degrees.append(angle)

    filtered_centre_xs = remove_outliers_iqr(centre_xs)
    filtered_centre_ys = remove_outliers_iqr(centre_ys)
    filtered_beam_stop_pos_xs = remove_outliers_iqr(beam_stop_pos_xs)
    filtered_beam_stop_pos_ys = remove_outliers_iqr(beam_stop_pos_ys)
    filtered_beam_stop_rs = remove_outliers_iqr(beam_stop_rs)
    filtered_angle_degrees = angle_degrees

    update_beam_stop_file(
        img_path,
        (np.average(filtered_centre_xs), np.average(filtered_centre_ys)),
        (np.average(filtered_beam_stop_pos_xs), np.average(filtered_beam_stop_pos_ys)),
        np.average(filtered_beam_stop_rs),
        np.average(filtered_angle_degrees),
    )

    update_xds_inp_beam_stop(
        xds_path,
        size,
        (np.average(filtered_centre_xs), np.average(filtered_centre_ys)),
        (np.average(filtered_beam_stop_pos_xs), np.average(filtered_beam_stop_pos_ys)),
        np.average(filtered_beam_stop_rs),
        np.average(filtered_angle_degrees),
    )

    print("Beam Stop Information Collected.\n")
    return


def update_beam_stop_file(
        img_directory: str,
        centre: tuple,
        beam_stop_pos: tuple,
        beam_stop_r: np.floating,
        angle_degrees: np.floating) -> None:
    """
    Writes the beam stop information to a text file in the image directory.

    Args:
        img_directory (str): Directory containing IMG files.
        centre (tuple): Center of the beam.
        beam_stop_pos (tuple): Position of the beam stop.
        beam_stop_r (np.floating): Radius of the beam stop.
        angle_degrees (np.floating): Angle of the beam stop direction in degrees.
    """
    centers_file_path = os.path.join(img_directory, 'beam_stop_info.txt')
    if angle_degrees < -120 or angle_degrees > 120:
        direction = "x-"
    elif -60 < angle_degrees < 60:
        direction = "x+"
    else:
        direction = "undetermined direction"
    print(f"Est. beam center: ({centre[0]:.2f}, {centre[1]:.2f})")
    with open(centers_file_path, 'w') as file:
        file.write(f"Est. beam center: ({centre[0]}, {centre[1]})\n")
        file.write(f"Average beam stop position: ({beam_stop_pos[0]}, {beam_stop_pos[1]})\n")
        file.write(f"Average beam stop radius: {beam_stop_r}\n")
        file.write(f"Beam Stop Position: {direction}\n")


def update_xds_inp_beam_stop(
        xds_inp_path: str,
        size: int,
        centre: tuple,
        beam_stop_pos: tuple,
        beam_stop_r: np.floating,
        angle_degrees: np.floating
) -> None:
    """
    Updates the XDS.INP file with beam stop information.

    Args:
        xds_inp_path (str): Path to the XDS.INP file.
        size (int): Size of the image.
        centre (tuple): Center of the beam.
        beam_stop_pos (tuple): Position of the beam stop.
        beam_stop_r (float): Radius of the beam stop.
        angle_degrees (float): Angle of the beam stop direction in degrees.
    """
    if os.path.exists(xds_inp_path):
        with open(xds_inp_path, 'r+') as file:
            lines = file.readlines()
            lines = replace_value(lines, "ORGX", [f"{centre[0]}"], False)
            lines = replace_value(lines, "ORGY", [f"{centre[1]}"], False)
            lines = replace_value(lines, "UNTRUSTED_ELLIPSE",
                                  [f"{beam_stop_pos[0] - beam_stop_r:.0f} {beam_stop_pos[0] + beam_stop_r:.0f} "
                                   f"{beam_stop_pos[1] - beam_stop_r:.0f} {beam_stop_pos[1] + beam_stop_r:.0f}"],
                                  False)
            if angle_degrees < -120 or angle_degrees > 120:
                area = (f"0  {beam_stop_pos[0]:.0f}  "
                        f"{beam_stop_pos[1] - 0.5 * beam_stop_r:.0f}  {beam_stop_pos[1] + 0.5 * beam_stop_r:.0f}")
                lines = replace_value(lines, "UNTRUSTED_RECTANGLE", [area], False)
            elif -60 < angle_degrees < 60:
                area = (f"{beam_stop_pos[0]:.0f}  {size:.0f}  "
                        f"{beam_stop_pos[1] - 0.5 * beam_stop_r:.0f}  {beam_stop_pos[1] + 0.5 * beam_stop_r:.0f}")
                lines = replace_value(lines, "UNTRUSTED_RECTANGLE", [area], False)
            file.seek(0)
            file.writelines(lines)
            file.truncate()


def beam_stop_calculate(input_path: str) -> None:
    """
    Calculates the beam stop position for all IMG files in a directory.

    Args:
        input_path (str): Directory containing IMG files.
    """
    if input_path:
        print("\n********************************************")
        print("*            Beam Centre Finder            *")
        print("*--------   w/ Beam Stop Version   --------*")
        print("********************************************\n")

        print(f"Self beam centre finding has received input path: {input_path}")
        paths_dict = get_xds_inp_image_dict(input_path)
        if not paths_dict:
            print("No XDS.inp found.\n")
            return
        for xds_path in paths_dict.keys():
            img_dir = os.path.dirname(paths_dict[xds_path]["image_path"])
            img_format = paths_dict[xds_path]["image_format"]
            if img_format == "SMV":
                print(f"Entering folder: {img_dir}")
                process_folder_beam_stop(img_dir, xds_path)
        print("*** Beam Stop Calculation Complete. ***\n")
    else:
        print("No input path provided.\n")


if __name__ == "__main__":
    print(process_folder_beam_stop("/mnt/c/Users/Childhood/Downloads/gsi-10_2412_Cl860_beta_pf_1220_063",
                                   "/mnt/c/Users/Childhood/Downloads/gsi-10_2412_Cl860_beta_pf_1220_063/XDS/XDS.INP"))
