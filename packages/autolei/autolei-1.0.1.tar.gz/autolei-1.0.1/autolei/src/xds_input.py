"""
XDS Input Module
================

This module provides tools for managing and modifying XDS input files (`XDS.INP`). It automates the correction and
updating of these files based on metadata and user-specified parameters, streamlining crystallographic data processing
workflows.

Features:
    - Locate and set up directories for XDS input files.
    - Update experimental parameters in `XDS.INP` files, such as detector settings, image ranges, and unit cell constants.
    - Batch processing of multiple `XDS.INP` files for corrections and compatibility.
    - Graphical user interface (GUI) for managing keywords in `XDS.INP` files with autocomplete functionality.
    - Validation utilities to ensure the correctness of input parameters.

Dependencies:
    - Standard Libraries:
        - `configparser`
        - `glob`
        - `collections.Counter`
        - `os`
        - `re`
        - `shutil`
    - Third-party Libraries:
        - `fabio`
        - `tkinter` (`tk`, `ttk`, `messagebox`)

Classes:
    - `AutocompleteEntry`: A GUI entry widget with autocomplete functionality for keywords.
    - `BaseTab`: Base class for managing the layout and behavior of the AddTab and DeleteTab in the GUI.
    - `AddTab`: Handles adding new keywords to `XDS.INP` files.
    - `DeleteTab`: Handles deleting keywords from `XDS.INP` files.
    - `CalibrateTab`: Manages detector calibration parameters through the GUI.
    - `KeywordManagerApp`: Main GUI application for managing `XDS.INP` keywords and calibration.

Functions:
    - `find_xds_inp_paths(input_path: str, path_filter: bool) -> Tuple[Dict[str, str], List[str]]`:
      Finds `XDS.INP` file paths within a directory.
    - `setup_xds_directory(img_folder_paths: List[str], paths_dict: Dict[str, str]) -> List[str]`:
      Creates or updates directories for XDS processing.
    - `update_xds_files(work_path: List[str]) -> None`:
      Updates `XDS.INP` files with image-related metadata.
    - `update_img_info(xds_inp_file: str) -> None`:
      Updates the image information in a given `XDS.INP` file.
    - `write_xds_file(input_path: str, settings_file_path: str, path_filter: bool) -> None`:
      Writes and sets up `XDS.INP` files in a directory.
    - `instamatic_modify(file_path: str) -> None`:
      Modifies `XDS.INP` files for compatibility with Instamatic data collection.
    - `cell_correct(folder_path: str, path_filter: bool) -> None`:
      Updates cell and space group information in `XDS.INP` files based on a configuration file.
    - `validate_data(keyword: str, value: str) -> str`:
      Validates the provided keyword and value against predefined rules.
    - `create_keyword_manager_app(xds_list: List[str]) -> None`:
      Launches the GUI for managing keywords in `XDS.INP` files.

Usage:
    - To set up XDS input files for data processing:
        ```python
        from xds_input_module import write_xds_file
        write_xds_file(input_path="/path/to/data", settings_file_path="/path/to/settings.txt")
        ```
    - To launch the GUI for editing `XDS.INP` files:
        ```python
        from xds_input_module import create_keyword_manager_app
        create_keyword_manager_app(["/path/to/XDS.INP"])
        ```

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen and Lei Wang
    - License: BSD 3-clause
"""


import configparser
import glob
import os.path
from collections import Counter
from tkinter import messagebox
from typing import List, Dict, Tuple

import fabio

from .util import *

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, '..', 'setting.ini'))

max_core = config["XDSInput"]["max_core"]
max_job = config["XDSInput"]["max_job"]


def find_xds_inp_paths(input_path: str, path_filter: bool = False) -> tuple:
    """Finds XDS.INP file paths in the specified directory.

    Args:
        input_path (str): Directory containing image folders.
        path_filter (bool, optional): Whether to filter paths. Defaults to False.

    Returns:
        tuple: A dictionary mapping image folder paths to XDS.INP paths and a list of image folder paths.
    """
    paths_dict = {}
    img_folder_paths = find_folders_with_images(input_path, path_filter=path_filter)
    for path in img_folder_paths:
        possible_locations = [path, os.path.dirname(path), os.path.join(path, 'xds')]
        for loc in possible_locations:
            if os.path.exists(os.path.join(loc, 'XDS.INP')):
                paths_dict[path] = os.path.join(loc, 'XDS.INP')
                break
    return paths_dict, img_folder_paths


def setup_xds_directory(img_folder_paths: List[str], paths_dict: Dict[str, str]) -> List[str]:
    """Sets up the XDS directory for image folders.

    Args:
        img_folder_paths (List[str]): List of image folder paths.
        paths_dict (Dict[str, str]): Mapping of image folder paths to XDS.INP paths.

    Returns:
        List[str]: List of paths to newly created XDS.INP files.
    """
    work_path = []
    for path in img_folder_paths:
        if path not in paths_dict:
            xds_dir = os.path.join(path, 'xds')
            os.makedirs(xds_dir, exist_ok=True)
            xds_inp_path = os.path.join(xds_dir, 'XDS.INP')
            shutil.copy(os.path.join(script_dir, "_XDSINP"), xds_inp_path)
            print(f'{os.path.abspath(xds_dir)} xds created.')
            work_path.append(xds_inp_path)
    return work_path


def update_xds_files(work_path: List[str]) -> None:
    """Updates XDS.INP files with image information.

    Args:
        work_path (List[str]): List of paths to XDS.INP files.
    """
    for xds_inp_file in work_path:
        update_img_info(xds_inp_file)


def update_img_info(xds_inp_file: str) -> None:
    """Updates image-specific information in an XDS.INP file.

    Args:
        xds_inp_file (str): Path to the XDS.INP file to update.
    """
    parent_path = os.path.abspath(os.path.join(xds_inp_file, "../../"))
    image_files = sorted(glob.glob(os.path.join(parent_path, '*.img')))
    if not image_files:
        return

    template, start, end = extract_pattern(image_files)
    template = f"../{os.path.basename(template)}" if config["XDSInput"]["use_relative_path"] else template
    start = max(start, 1)

    try:
        start_angle = fabio.open(image_files[0]).header.get("PHI", "0.0")
    except Exception as e:
        print(f"{xds_inp_file} cannot be created due to {e}")
        os.remove(xds_inp_file)
        return

    with open(xds_inp_file, 'r+') as file:
        content = file.read().replace('{$1}', f"{max_job}").replace('{$2}', f"{max_core}")
        file.seek(0)
        file.write(content)
        file.truncate()

    with open(xds_inp_file, 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "NAME_TEMPLATE_OF_DATA_FRAMES=" in line:
                lines[i] = f" NAME_TEMPLATE_OF_DATA_FRAMES= {template}  SMV\n"
            elif any(key in line for key in ["DATA_RANGE=", "SPOT_RANGE=", "BACKGROUND_RANGE="]):
                lines[i] = f" {line.split('=')[0]}=  {start}  {end}\n"
            elif "STARTING_ANGLE=" in line:
                lines[i] = f" STARTING_ANGLE= {start_angle}\n"
        file.seek(0)
        file.writelines(lines)
        file.truncate()


def update_experiment_information(
        input_path: str, xds_inp_files: List[str],
        settings_file_path: str = None) -> None:
    """Updates experiment information in XDS.INP files.

    Args:
        input_path (str): Directory containing the settings file.
        xds_inp_files (List[str]): List of paths to XDS.INP files.
        settings_file_path (str, optional): Path to the settings file. Defaults to `Input_parameters.txt`.
    """

    single_line_dict = {'NX': "NY", "QX": "QY", "ORGX": "ORGY"}
    if not settings_file_path:
        settings_file_path = os.path.join(input_path, 'Input_parameters.txt')
    with open(settings_file_path, 'r') as file:
        settings = extract_keywords(file.readlines())

    for xds_inp_file in xds_inp_files:
        if not os.path.isfile(xds_inp_file):
            continue
        with open(xds_inp_file, 'r+') as file:
            updated_settings = set()
            updated_lines = []
            lines = file.readlines()
            for line in lines:
                for key, values in settings.items():
                    if line.strip().startswith(key + "="):
                        if key in single_line_dict:
                            paired_key = single_line_dict[key]
                            line = f" {key}= {settings[key][0]} {paired_key}= {settings[paired_key][0]}\n"
                            updated_settings.add(key)
                            updated_settings.add(paired_key)
                            break
                        else:
                            line = "".join([f" {key}= {val}\n" for val in values])
                            updated_settings.add(key)
                            break
                updated_lines.append(line)

            # Append settings that weren't found and updated
            for key, values in settings.items():
                if key not in updated_settings:
                    if key in single_line_dict:
                        paired_key = single_line_dict[key]
                        updated_lines.append(f" {key}= {settings[key][0]} {paired_key}= {settings[paired_key][0]}\n")
                    else:
                        updated_lines.extend([f" {key}= {val}\n" for val in values])
            file.seek(0)
            file.writelines(updated_lines)
            file.truncate()


def write_xds_file(
    input_path: str, settings_file_path: str = None, path_filter: bool = False
) -> None:
    """Writes and sets up XDS.INP files in a directory.

    Args:
        input_path (str): Directory to process.
        settings_file_path (str, optional): Path to the settings file. Defaults to None.
        path_filter (bool, optional): Whether to filter paths. Defaults to False.
    """


    if not settings_file_path:
        settings_file_path = os.path.join(input_path, 'Input_parameters.txt')
    if not os.path.isfile(settings_file_path):
        print("The specified settings file does not exist.")
        return

    required_keys = ['NX', 'NY', 'OVERLOAD', 'QX', 'QY', 'DETECTOR_DISTANCE', 'OSCILLATION_RANGE',
                     'ROTATION_AXIS', 'X-RAY_WAVELENGTH', 'INCLUDE_RESOLUTION_RANGE']
    with open(settings_file_path, 'r') as file:
        settings = extract_keywords(file.readlines())
    missing_keys = [key for key in required_keys if not (key in settings and settings[key])]
    if missing_keys:
        print(f'Missing settings: {", ".join(missing_keys)}')
        return

    print("********************************************")
    print("*                 XDS Writer               *")
    print("********************************************\n")
    paths_dict, img_folder_paths = find_xds_inp_paths(input_path, path_filter)
    work_paths = setup_xds_directory(img_folder_paths, paths_dict)
    update_xds_files(work_paths)
    update_experiment_information(input_path, work_paths, settings_file_path)
    print("Setup complete.\n")


def extract_keywords(lines: List[str]) -> Dict[str, List[str]]:
    """Extracts key-value pairs from XDS input file lines.

    Args:
        lines (List[str]): Lines from an XDS input file.

    Returns:
        Dict[str, List[str]]: Dictionary of extracted parameters.
    """

    # pattern = r'(\b[A-Z_\'\.\-]+\b)\s*=\s*([^=]*?)(?=\b[A-Z_\'\.\-]+\b\s*=|$)'
    pattern = r'(\b[A-Z_\'\.\-\/]+\b)\s*=\s*((?:(?!\b[A-Z_\'\.\-\/]+\b=).)*?)\s*(?=\b[A-Z_\'\.\-\/]+\b\s*=|$)'
    extracted_values = {}
    for line in lines:
        line = line.split('!', 1)[0].strip()
        matches = re.findall(pattern, line)
        for key, value in matches:
            value = value.strip()
            if key in extracted_values:
                if value and value not in extracted_values[key]:
                    extracted_values[key].append(value)
            else:
                extracted_values[key] = [value] if value else []
    return extracted_values


def load_XDS_excluded_range(lines: List[str]) -> List[int]:
    """Extracts ranges to exclude from XDS.INP lines.

    Args:
        lines (List[str]): Lines from an XDS.INP file.

    Returns:
        List[int]: Excluded frame ranges.
    """
    excluded_ranges = []
    for line in lines:
        line = line.strip()
        if line.startswith("EXCLUDE_DATA_RANGE=") and not line.startswith("!"):
            start, end = map(int, line.split("=")[-1].split())
            excluded_ranges.extend(range(start, end + 1))
    return excluded_ranges


def generate_exclude_data_ranges(exclude_list: List[int]) -> List[str]:
    """Generates EXCLUDE_DATA_RANGE lines for an XDS.INP file.

    Args:
        exclude_list (List[int]): List of excluded frame numbers.

    Returns:
        List[str]: Lines for the EXCLUDE_DATA_RANGE parameter.
    """
    add_lines = []
    if exclude_list:
        start = exclude_list[0]
        prev = start
        for num in exclude_list[1:]:
            if num != prev + 1:
                if start == prev:
                    add_lines.append(f" EXCLUDE_DATA_RANGE= {start} {start}\n")
                else:
                    add_lines.append(f" EXCLUDE_DATA_RANGE= {start} {prev}\n")
                start = num
            prev = num
        if start == prev:
            add_lines.append(f" EXCLUDE_DATA_RANGE= {start} {start}\n")
        else:
            add_lines.append(f" EXCLUDE_DATA_RANGE= {start} {prev}\n")
    return add_lines


def instamatic_modify(file_path: str) -> None:
    """Modifies an XDS.INP file for compatibility with Instamatic.

    Args:
        file_path (str): Path to the XDS.INP file.
    """
    with open(file_path, 'r', errors="replace") as file:
        content = file.readlines()
    # Modify the content as require
    exist_corr = False
    new_content = []
    xds_dir = os.path.dirname(file_path)
    if os.path.isfile(os.path.join(xds_dir, 'XCORR.cbf')):
        exist_corr = True
    for line in content:
        temp_line = line.strip()
        # Replace the problematic character
        line = line.replace('�', '-')
        # Modify lines based on specific starts
        if any(temp_line.startswith(prefix) for prefix in [
            "AIR=", "SENSOR_THICKNESS=",  "STRONG_PIXEL=", "MINIMUM_FRACTION_OF_BACKGROUND_REGION=", "BACKGROUND_PIXEL="
        ] + (["X-GEO_CORR=", "Y-GEO_CORR="] if not exist_corr else [])):
            line = "! " + line
        elif temp_line.startswith("TRUSTED_REGION="):
            line = " TRUSTED_REGION= 0.0  1.35   !default 0.0 1.05. Corners for square detector max 0.0 1.4142\n"
        new_content.append(line)
    # Write the modified content back to the file using UTF-8 encoding
    with open(file_path, 'w') as file:
        file.writelines(new_content)


def instamatic_update(folder: str, path_filter: bool) -> None:
    """Updates all XDS.INP files in a directory for Instamatic.

    Args:
        folder (str): Directory containing XDS.INP files.
        path_filter (bool): Whether to apply filtering.
    """
    matching_files = find_files(folder, "XDS.INP", path_filter=path_filter)
    for file_path in matching_files:
        instamatic_modify(file_path)
        print(f"{file_path} from Instamatic has been updated.")
    print("All XDS.INP files have been updated.\n")


def cell_correct(folder_path: str, path_filter: bool = False) -> None:
    """Corrects unit cell and space group information in XDS.INP files.

    Args:
        folder_path (str): Directory containing Cell_information.txt.
        path_filter (bool, optional): Whether to filter paths. Defaults to False.
    """
    if folder_path:
        print(f"cell_correct has received input path: {folder_path}")

        txt_path = os.path.join(folder_path, "Cell_information.txt")
        print(f"Using txt file: {txt_path}")

        try:
            with open(txt_path, 'r') as file:
                txt_content = file.readlines()
        except FileNotFoundError:
            print(f"Could not find the file: {txt_path}")
            return

        space_group_provided_by_user = None
        unitcell_provided_by_user = None

        for line in txt_content:
            if "SPACE_GROUP_NUMBER=" in line:
                space_group_provided_by_user = line.strip()
            elif "UNIT_CELL_CONSTANTS=" in line:
                unitcell_provided_by_user = line.strip()

        if not space_group_provided_by_user:
            print("There is no crystal information of space group!")
            return
        if not unitcell_provided_by_user:
            print("There is no crystal information of unit cell!")
            return

            # Find and update xds.inp in all folders
        for dirpath, dirnames, filenames in os.walk(folder_path):
            if path_filter and ("!" in dirpath or "/." in dirpath or "!" in dirnames or "/." in dirnames):
                pass
            else:
                for filename in filenames:
                    if filename.lower() == "xds.inp":
                        inp_file_path = os.path.join(dirpath, filename)
                        if not os.path.exists(os.path.join(dirpath, "BACKUP-P1")):
                            shutil.copy(inp_file_path, os.path.join(dirpath, "BACKUP-P1"))
                        with open(inp_file_path, 'r', errors="ignore") as file:
                            inp_content = file.readlines()

                        # Modify the unit cell and space group in xds.inp
                        for i, line in enumerate(inp_content):
                            if "SPACE_GROUP_NUMBER=" in line and space_group_provided_by_user:
                                inp_content[i] = space_group_provided_by_user + "\n"
                            elif "UNIT_CELL_CONSTANTS=" in line and unitcell_provided_by_user:
                                inp_content[i] = unitcell_provided_by_user + "\n"

                        # Write the changes back to xds.inp
                        with open(inp_file_path, 'w') as file:
                            file.writelines(inp_content)

        print("Finished processing all xds.inp files in the selected folder.\n")
    else:
        print("No input path provided.\n")


def cell_correct_online(xds: str, cell: str, sg: str) -> None:
    """Corrects cell parameters and space group information online.

    Args:
        xds (str): Path to the XDS.INP file.
        cell (str): Cell parameters to update.
        sg (str): Space group to update.
    """
    with open(xds, "r+") as f:
        lines = f.readlines()
        lines = replace_value(lines, "SPACE_GROUP_NUMBER", [sg], comment=False)
        lines = replace_value(lines, "UNIT_CELL_CONSTANTS", [cell], comment=False)
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    print("Finished processing all xds.inp files in the selected folder.\n")


def correct_xds_file_SMV(img_path: str, xds_path: str) -> None:
    """Corrects an XDS.INP file using image metadata.

    Args:
        img_path (str): Directory containing image files.
        xds_path (str): Path to the XDS.INP file.
    """
    print(f"Correct {xds_path} with \nimage in {img_path}.\n")
    replace_nx, replace_ny, replace_q, replace_d, replace_wl, replace_a = [False] * 6
    img_files = sorted(glob.glob(os.path.join(img_path, '*.img')), key=natural_sort_key)
    if len(img_files) < 10:
        print("Too few images found.")
        return
    try:
        img = fabio.open(img_files[0])
    except Exception as e:
        print(f"image file may be broken due to {e}")
        return
    header_dict = dict(img.header)
    img2 = fabio.open(img_files[-1])
    header_dict_last = dict(img2.header)
    if "PHI" in header_dict:
        try:
            osc_total = float(header_dict_last["PHI"]) - float(header_dict["PHI"])
            osc_range = round(osc_total / (len(img_files) - 1), 4)
        except KeyError:
            osc_range = None
    else:
        osc_range = None

    first_occurrence = 0
    rotation_axis_inverse = False
    with open(xds_path, "r") as _file:
        xds_lines = _file.readlines()
        xds_parameters = extract_keywords(xds_lines)
    if "SIZE1" in header_dict and int(header_dict["SIZE1"]) != int(xds_parameters["NX"][0]):
        replace_nx = True
    if "SIZE2" in header_dict and int(header_dict["SIZE2"]) != int(xds_parameters["NY"][0]):
        replace_ny = True
    if ("PIXEL_SIZE" in header_dict and float(header_dict["PIXEL_SIZE"]) != float(xds_parameters["QX"][0])
            or float(header_dict["PIXEL_SIZE"]) != float(xds_parameters["QY"][0])):
        replace_q = True
    if "DISTANCE" in header_dict and float(header_dict["DISTANCE"]) != float(xds_parameters["DETECTOR_DISTANCE"][0]):
        replace_d = True
    if "WAVELENGTH" in header_dict and float(header_dict["WAVELENGTH"]) != float(xds_parameters["X-RAY_WAVELENGTH"][0]):
        replace_wl = True
    if osc_range != 0 and osc_range != float(xds_parameters["OSCILLATION_RANGE"][0]):
        replace_a = True
    if replace_nx or replace_ny or replace_q or replace_d or replace_wl or replace_a:
        new_line = []
        for i, line in enumerate(xds_lines):
            if (replace_nx or replace_ny) and (line.strip().startswith("NX") or line.strip().startswith("NY")):
                first_occurrence = i
                if "QX" in line:
                    replace_q = True
            elif replace_q and (" QX=" in line or line.strip().startswith("QY")):
                first_occurrence = i
                if " NX=" in line:
                    replace_q = True
            elif replace_wl and line.strip().startswith("X-RAY_WAVELENGTH"):
                new_line.append(" X-RAY_WAVELENGTH= {}\n".format(header_dict["WAVELENGTH"]))
            elif replace_d and line.strip().startswith("DETECTOR_DISTANCE"):
                new_line.append(" DETECTOR_DISTANCE= {}\n".format(header_dict["DISTANCE"]))
            elif replace_a and line.strip().startswith("OSCILLATION_RANGE"):
                if osc_range > 0:
                    new_line.append(" OSCILLATION_RANGE= {}\n".format(osc_range))
                else:
                    new_line.append(" OSCILLATION_RANGE= {}\n".format(-osc_range))
                    rotation_axis_inverse = True
            else:
                new_line.append(line)
        if replace_q:
            new_line.insert(first_occurrence,
                            " QX= {}  QY= {}\n".format(header_dict["PIXEL_SIZE"], header_dict["PIXEL_SIZE"]))
        if replace_nx or replace_ny:
            new_line.insert(first_occurrence, " NX= {}  NY= {}\n".format(header_dict["SIZE1"], header_dict["SIZE2"]))
        if rotation_axis_inverse:
            rotation_axis_text = xds_parameters["ROTATION_AXIS"][0]
            rotation_axis_text_new = "  ".join(str(-float(element)) for element in rotation_axis_text.split())
            new_line = replace_value(new_line, "ROTATION_AXIS", [rotation_axis_text_new], comment=False)
        with open(xds_path, "w") as _file:
            _file.writelines(new_line)


def correct_inputs(input_path: str) -> None:
    """Processes and corrects XDS.INP files using metadata.

    Args:
        input_path (str): Directory containing image folders and XDS.INP files.
    """
    if input_path:
        print(f"Try to correct input with metadate in {input_path}")
        paths_dict = get_xds_inp_image_dict(input_path)
        for xds_path in paths_dict.keys():
            img_dir = os.path.dirname(paths_dict[xds_path]["image_path"])
            img_format = paths_dict[xds_path]["image_format"]
            if img_format == "SMV":
                print(f"Entering folder: {img_dir}")
                correct_xds_file_SMV(img_dir, xds_path)
        print(f"Finished Correct input with metadata in {input_path}.\n")


def replace_value(
    lines: List[str], keyword: str, values: List[str], comment: bool, add: bool = False
) -> List[str]:
    """Replaces or adds values for a keyword in XDS.INP lines.

    Args:
        lines (List[str]): Lines from an XDS input file.
        keyword (str): The keyword to replace or add.
        values (List[str]): Values to set for the keyword.
        comment (bool): Whether to comment out old values.
        add (bool, optional): Whether to add new entries instead of replacing. Defaults to False.

    Returns:
        List[str]: Modified lines.
    """
    keyword_eq = f"{keyword}="
    underscore_keyword_eq = f"_{keyword}="
    comment_prefix = " !" if comment else " "
    assignment_suffix = "\n"

    new_assignments = [
        f"{comment_prefix}{keyword}= {value}{assignment_suffix}"
        for value in values
    ]

    new_lines = []
    action_performed = False  # Flag to ensure single replace/add action

    for line in lines:
        contains_keyword = keyword_eq in line and underscore_keyword_eq not in line

        if contains_keyword:
            if not action_performed:
                if add:
                    new_lines.append(line)
                    new_lines.extend(new_assignments)
                else:
                    if line.count('=') >= 2:
                        temp_dict = extract_keywords([line])
                        for key, _values in temp_dict.items():
                            if key != keyword:
                                for _value in _values:
                                    new_lines.append(f"{key}={_value}{assignment_suffix}")
                    new_lines.extend(new_assignments)
                action_performed = True
            else:
                if add:
                    new_lines.append(line)
        else:
            new_lines.append(line)

    if not action_performed:
        new_lines.extend(new_assignments)

    return new_lines


def delete_xds(input_path: str) -> None:
    """Deletes XDS.INP files and related folders in a directory.

    Args:
        input_path (str): Directory containing XDS.INP files and folders.
    """
    if input_path:
        print(f"Deleted XDS files and folders in: {input_path}")
        delete_files(input_path, 'xds.inp')
        delete_folders(input_path, 'xds')
        print(f"XDS folders have been removed under the path.\n")
    else:
        print("No input path provided.")


def get_xds_inp_image_dict(input_path: str) -> Dict[str, Dict[str, str]]:
    """Retrieves a mapping of XDS.INP files to image paths and formats.

    Args:
        input_path (str): Directory containing XDS.INP files.

    Returns:
        Dict[str, Dict[str, str]]: Dictionary mapping XDS.INP paths to image information.
    """
    xds_files = find_files(input_path, "XDS.INP")
    xds_image_dict = {}
    for xds_path in xds_files:
        with open(xds_path) as _file:
            keyword_dict = extract_keywords(_file.readlines())
        if not keyword_dict["NAME_TEMPLATE_OF_DATA_FRAMES"]:
            print(f"{xds_path} is not valid. Check it carefully.")
        image_path, file_format = (" ".join(keyword_dict["NAME_TEMPLATE_OF_DATA_FRAMES"][0].split()[:-1]),
                                   keyword_dict["NAME_TEMPLATE_OF_DATA_FRAMES"][0].split()[-1])
        if "?" in file_format:
            image_path = file_format
            file_format = "SMV"
        if not (image_path.startswith("/") or image_path.startswith("~")):
            xds_dir = os.path.dirname(xds_path)
            image_path = os.path.abspath(os.path.join(xds_dir, image_path))
        xds_image_dict[xds_path] = {"image_path": image_path,
                                    "image_format": file_format}
    return xds_image_dict


def change_path_input(input_path: str, mode: str = "absolute") -> None:
    """Changes paths in XDS.INP files to absolute or relative.

    Args:
        input_path (str): Directory containing XDS.INP files.
        mode (str): Path mode ("absolute" or "relative"). Defaults to "absolute".
    """
    xds_image_dict = get_xds_inp_image_dict(input_path)
    for xds_path in xds_image_dict.keys():
        if not os.path.isdir(os.path.dirname(xds_image_dict[xds_path]["image_path"])):
            image_list = find_folders_with_images(os.path.dirname(xds_path))
            if not image_list:
                image_list = find_folders_with_images(os.path.dirname(os.path.dirname(xds_path)))
            if not image_list:
                image_list = find_folders_with_images(os.path.dirname(os.path.dirname(os.path.dirname(xds_path))))
            try:
                xds_image_dict[xds_path]["image_path"] = os.path.join(
                    image_list[0], os.path.basename(xds_image_dict[xds_path]["image_path"]))
            except IndexError:
                print(f"No image folder found for {xds_path}")
                continue
        else:
            img_files = sorted(glob.glob(
                os.path.join(os.path.dirname(xds_image_dict[xds_path]["image_path"]), '*.img')), key=natural_sort_key)
            file_groups = {}
            for file in img_files:
                filename = os.path.basename(file)
                # Check if the filename ends with a digit before .mrc
                if re.search(r'\d+\.img$', filename):
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
            img_files = sorted(max_group, key=natural_sort_key)
            if len(xds_image_dict[xds_path]["image_path"]) != len(img_files[0]):
                (xds_image_dict[xds_path]["image_path"], xds_image_dict[xds_path]["start"],
                 xds_image_dict[xds_path]["end"]) = extract_pattern(img_files)
        with open(xds_path, "r+") as f:
            if mode == "absolute":
                path = os.path.abspath(xds_image_dict[xds_path]["image_path"])
            elif mode == "relative":
                path = os.path.relpath(xds_image_dict[xds_path]["image_path"], os.path.dirname(xds_path))
            lines = f.readlines()
            lines = replace_value(lines,
                                  "NAME_TEMPLATE_OF_DATA_FRAMES",
                                  ["{} {}".format(path, xds_image_dict[xds_path]["image_format"])],
                                  comment=False)
            if "start" in xds_image_dict[xds_path]:
                lines = replace_value(lines,
                                      "DATA_RANGE",
                                      ["{} {}".format(xds_image_dict[xds_path]["start"],
                                                      xds_image_dict[xds_path]["end"])],
                                      comment=False)
                lines = replace_value(lines,
                                      "SPOT_RANGE",
                                      ["{} {}".format(xds_image_dict[xds_path]["start"],
                                                      xds_image_dict[xds_path]["end"])],
                                      comment=False)
                lines = replace_value(lines,
                                      "BACKGROUND_RANGE",
                                      ["{} {}".format(xds_image_dict[xds_path]["start"],
                                                      xds_image_dict[xds_path]["end"])],
                                      comment=False)
            f.seek(0)
            f.writelines(lines)
            f.truncate()


class AutocompleteEntry(ttk.Entry):
    """An entry widget with autocomplete functionality."""

    def __init__(self, master: tk.Widget, keyword_list: List[str], *args,
                 list_font: Tuple[str, int] = ("Liberation Sans", 15), **kwargs):
        """
        Initializes the AutocompleteEntry.

        Args:
            master (tk.Widget): Parent widget.
            keyword_list (List[str]): List of keywords for autocomplete.
            list_font (tuple[str, int], optional): Font for the dropdown list. Defaults to ("Liberation Sans", 15).
        """
        self.listbox = None
        self.lb = None
        self.keyword_list = sorted(keyword_list, key=lambda x: x.lower())
        self.list_font = list_font

        if "font" not in kwargs:
            kwargs["font"] = ("Liberation Sans", 15)
        super().__init__(master, *args, **kwargs)

        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add("write", self.on_change)

        # Bind navigation and selection keys
        self.bind("<Down>", self.on_down_key)
        self.bind("<Up>", self.on_up_key)
        self.bind("<Return>", self.on_return_key)
        self.bind("<Escape>", self.close_listbox)
        self.bind("<FocusOut>", self.on_focus_out)

    def show_listbox(self, matching_keywords: List[str]) -> None:
        """Displays the listbox with matching keywords.

        Args:
            matching_keywords (List[str]): List of keywords matching the input.
        """
        if not self.listbox:
            self.listbox = tk.Toplevel(self)
            self.listbox.wm_overrideredirect(True)
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.listbox.wm_geometry(f"+{x}+{y}")
            self.listbox.attributes("-topmost", True)

            self.lb = tk.Listbox(
                self.listbox,
                selectmode=tk.SINGLE,
                activestyle="none",
                font=self.list_font,
                bg="#f0f0f0",
                fg="black",
                highlightthickness=1,
                highlightbackground="#b0c4de",
            )
            self.lb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

            # Bind selection events
            self.lb.bind("<<ListboxSelect>>", self.on_listbox_select)
            self.lb.bind("<ButtonRelease-1>", self.on_listbox_click)
            self.lb.bind("<Motion>", self.on_listbox_motion)
            self.lb.bind("<Leave>", self.on_listbox_leave)

        # Populate the listbox
        self.lb.delete(0, tk.END)
        display_limit = 5
        total_matches = len(matching_keywords)

        if total_matches > display_limit:
            for kw in matching_keywords[: display_limit - 1]:
                self.lb.insert(tk.END, kw)
            self.lb.insert(tk.END, "...")
        else:
            for kw in matching_keywords:
                self.lb.insert(tk.END, kw)

        # Adjust listbox size
        listbox_height = min(total_matches, display_limit)
        self.lb.config(height=listbox_height, width=self["width"])
        self.listbox.update_idletasks()

    def on_change(self, *args) -> None:
        """Handles changes in the entry widget."""
        input_text = self.var.get()
        if not input_text:
            self.close_listbox()
            return

        matching_keywords = [
            kw for kw in self.keyword_list if input_text.lower() in kw.lower()
        ]
        if matching_keywords:
            self.show_listbox(matching_keywords)
        else:
            self.close_listbox()

    def close_listbox(self, event: tk.Event = None) -> None:
        """Closes the dropdown listbox.

        Args:
            event (tk.Event): Event triggering the closure. Defaults to None.
        """
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
            self.lb = None

    def on_listbox_select(self, event: tk.Event) -> None:
        """Handles selection from the listbox.

        Args:
            event (tk.Event): Event for listbox selection.
        """
        if self.listbox:
            selected = self.lb.get(tk.ACTIVE)
            if selected != "...":
                self.var.set(selected)
                self.close_listbox()
                self.icursor(tk.END)

    def on_listbox_click(self, event: tk.Event) -> None:
        """Handles mouse click on the listbox.

        Args:
            event (tk.Event): Mouse click event.
        """
        if self.listbox:
            clicked_index = self.lb.nearest(event.y)
            if clicked_index >= 0:
                selected = self.lb.get(clicked_index)
                if selected != "...":
                    self.var.set(selected)
                    self.close_listbox()
                    self.icursor(tk.END)

    def on_listbox_motion(self, event: tk.Event) -> None:
        """Handles mouse movement over the listbox.

        Args:
            event (tk.Event): Mouse movement event.
        """
        if self.listbox:
            index = self.lb.nearest(event.y)
            self.lb.selection_clear(0, tk.END)
            self.lb.selection_set(index)
            self.lb.activate(index)

    def on_listbox_leave(self, event: tk.Event) -> None:
        """Clears selection when mouse leaves the listbox.

        Args:
            event (tk.Event): Mouse leave event.
        """
        if self.listbox:
            self.lb.selection_clear(0, tk.END)

    def on_down_key(self, event: tk.Event) -> None:
        """Navigates down in the listbox.

        Args:
            event (tk.Event): Key press event.

        """
        if self.listbox:
            self.lb.focus()
            self.lb.selection_set(0)
            self.lb.activate(0)
            self.lb.focus_set()

    def on_up_key(self, event: tk.Event) -> None:
        """Navigates up in the listbox.

        Args:
            event (tk.Event): Key press event.

        """
        if self.listbox:
            self.lb.focus()
            last_index = self.lb.size() - 1
            self.lb.selection_set(last_index)
            self.lb.activate(last_index)
            self.lb.focus_set()

    def on_return_key(self, event: tk.Event) -> str:
        """Selects the active item on pressing Return.

        Args:
            event (tk.Event): Key press event.

        Returns:
            str: Event status.
        """
        if self.listbox:
            selected = self.lb.get(tk.ACTIVE)
            if selected != "...":
                self.var.set(selected)
                self.close_listbox()
                self.icursor(tk.END)
                return "break"

    def on_focus_out(self, event: tk.Event) -> None:
        """Closes the listbox when focus is lost.

        Args:
            event (tk.Event): Focus out event.
        """
        self.close_listbox()


class BaseTab:
    """Base class for AddTab and DeleteTab to reduce redundancy."""

    def __init__(self, parent: ttk.Frame, keywords: List[str], max_rows: int = 8, has_value: bool = True):
        """
        Initializes the base tab.

        Args:
            parent (ttk.Frame): Parent frame.
            keywords (List[str]): List of keywords for autocomplete.
            max_rows (int, optional): Maximum number of rows allowed. Defaults to 8.
            has_value (bool, optional): Whether the tab includes a value entry. Defaults to True.
        """
        self.parent = parent
        self.keywords = keywords
        self.max_rows = max_rows
        self.has_value = has_value
        self.rows = []

        self.parent.configure(style="ConfigManager.TFrame")
        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the user interface components."""
        button_frame = ttk.Frame(self.parent, style="ConfigManager.TFrame")
        button_frame.pack(anchor=tk.W, pady=(20, 10))

        # Add Row Button
        self.add_row_button = ttk.Button(
            button_frame, text="Add Row", command=self.add_row, style="ConfigManager.TButton"
        )
        self.add_row_button.pack(side=tk.LEFT, padx=(10, 5))

        # Delete Row Button
        self.delete_row_button = ttk.Button(
            button_frame, text="Delete Row", command=self.delete_row, style="ConfigManager.TButton"
        )
        self.delete_row_button.pack(side=tk.LEFT, padx=5)

        # Reset Button
        self.reset_button = ttk.Button(
            button_frame, text="Reset", command=self.reset_rows, style="ConfigManager.TButton"
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Container for rows
        self.rows_container = ttk.Frame(self.parent, style="ConfigManager.TFrame")
        self.rows_container.pack(fill=tk.BOTH, expand=True)

        # Initialize with three rows
        for _ in range(3):
            self.add_row()

    def add_row(self) -> None:
        """Adds a new row to the tab."""
        if len(self.rows) >= self.max_rows:
            messagebox.showwarning(
                "Maximum Rows Reached",
                f"Cannot add more than {self.max_rows} rows.",
            )
            return

        row_frame = ttk.Frame(self.rows_container, style="ConfigManager.TFrame")
        row_frame.pack(fill=tk.X, pady=10)

        # Autocomplete Entry
        autocomplete = AutocompleteEntry(row_frame, self.keywords, width=30)
        autocomplete.configure(background="#f3f3f3")
        autocomplete.pack(side=tk.LEFT, padx=(20, 5))

        row_data = {"autocomplete": autocomplete}

        if self.has_value:
            # "=" Label
            equals_label = ttk.Label(
                row_frame,
                text="=",
                font=("Liberation Sans", 15),
                style="ConfigManager.TLabel",
            )
            equals_label.pack(side=tk.LEFT, padx=(0, 5))

            # Value Entry
            value_entry = ttk.Entry(row_frame, width=30, font=("Liberation Sans", 15))
            value_entry.configure(background="#f3f3f3")
            value_entry.pack(side=tk.LEFT, padx=5)

            row_data["value"] = value_entry

        row_data["frame"] = row_frame
        self.rows.append(row_data)

    def delete_row(self) -> None:
        """Deletes the last unfilled row."""
        if len(self.rows) < 2:
            return

        for row in reversed(self.rows):
            key = row["autocomplete"].get().strip()
            value = row.get("value", tk.StringVar()).get().strip() if self.has_value else ""
            if key == "" and value == "":
                row["frame"].destroy()
                self.rows.remove(row)
                return

        messagebox.showinfo("No Unfilled Rows", "There are no unfilled rows to delete.")

    def reset_rows(self) -> None:
        """Resets all rows to empty."""
        for row in self.rows:
            row["autocomplete"].delete(0, tk.END)
            if self.has_value:
                row["value"].delete(0, tk.END)

    def get_data(self) -> List[Dict[str, str]]:
        """Retrieves data from the rows.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing key-value pairs or keys.
            Returns "error" if there are incomplete entries.
        """
        data = []
        key_incomplete = []
        value_incomplete = []

        for row in self.rows:
            key = row["autocomplete"].get().strip()
            value = row["value"].get().strip() if self.has_value else ""

            if self.has_value:
                if key and value:
                    data.append({"key": key, "value": value})
                elif key:
                    key_incomplete.append(key)
                elif value:
                    value_incomplete.append(value)
            else:
                if key:
                    data.append({"key": key, "value": ""})

        if self.has_value and (key_incomplete or value_incomplete):
            messagebox.showwarning(
                "Warning",
                f"You have {len(key_incomplete)} values and {len(value_incomplete)} keywords unfilled.",
            )
            return "error"

        return data


class AddTab(BaseTab):
    """Tab for adding keywords with corresponding values in the GUI."""
    def __init__(self, parent: ttk.Frame, keywords: List[str]):
        super().__init__(parent, keywords, has_value=True)


class DeleteTab(BaseTab):
    """Tab for deleting keywords in the GUI."""
    def __init__(self, parent: ttk.Frame, keywords: List[str]):
        super().__init__(parent, keywords, has_value=False)


class CalibrateTab:
    """Tab for calibrating detector parameters within the GUI."""

    def __init__(self, parent: ttk.Frame, keywords: List[str], xds_list: List[str]):
        """
        Initializes the CalibrateTab.

        Args:
            parent (ttk.Frame): Parent frame.
            keywords (List[str]): List of keywords for calibration.
            xds_list (List[str]): List of XDS.INP file paths.
        """
        self.parent = parent
        self.keywords = keywords
        self.xds_list = xds_list
        self.calibration_entries = {}  # To store CL-specific ratio entries

        self.setup_calibrate_ui()

    def setup_calibrate_ui(self) -> None:
        """Sets up the user interface components for the Calibrate tab."""
        # First Line: Load and Clean Buttons
        button_frame = ttk.Frame(self.parent, style="ConfigManager.TFrame")
        button_frame.pack(anchor=tk.W, pady=(10, 5), padx=20)

        load_button = ttk.Button(
            button_frame,
            text="Load",
            command=self.load_calibration,
            style="ConfigManager.TButton",
        )
        load_button.pack(side=tk.LEFT, padx=(0, 10))

        clean_button = ttk.Button(
            button_frame,
            text="Clean",
            command=self.clean_calibration,
            style="ConfigManager.TButton",
        )
        clean_button.pack(side=tk.LEFT)

        # Second Line: Descriptive Text
        description_label = ttk.Label(
            self.parent,
            text="Calibration Ratio will be > 1 when the measured cell is larger than the ideal one.",
            style="ConfigManager.TLabel",
            wraplength=600,
        )
        description_label.pack(anchor=tk.W, pady=(10, 5), padx=20)

        # Third Line: Universe Ratio and Distance Factor
        ratio_frame = ttk.Frame(self.parent, style="ConfigManager.TFrame")
        ratio_frame.pack(anchor=tk.W, pady=(5, 10), padx=20)

        # Universe Ratio
        universe_label = ttk.Label(
            ratio_frame,
            text="Universe Ratio:",
            font=("Liberation Sans", 15),
            style="ConfigManager.TLabel",
        )
        universe_label.pack(side=tk.LEFT)

        self.universe_ratio_var = tk.DoubleVar(value=1.00)
        universe_entry = ttk.Entry(
            ratio_frame,
            textvariable=self.universe_ratio_var,
            width=10,
            font=("Liberation Sans", 15),
        )
        universe_entry.pack(side=tk.LEFT, padx=(10, 20))

        # Distance Factor
        distance_label = ttk.Label(
            ratio_frame,
            text="Distance Factor:",
            font=("Liberation Sans", 15),
            style="ConfigManager.TLabel",
        )
        distance_label.pack(side=tk.LEFT)

        self.distance_factor_var = tk.DoubleVar(value=1.00)
        distance_entry = ttk.Entry(
            ratio_frame,
            textvariable=self.distance_factor_var,
            width=10,
            font=("Liberation Sans", 15),
        )
        distance_entry.pack(side=tk.LEFT, padx=(10, 0))

        # Separator
        separator = ttk.Separator(self.parent, orient='horizontal')
        separator.pack(fill='x', pady=10, padx=20)

        # Frame to hold dynamic CL entries
        self.cl_entries_frame = ttk.Frame(self.parent, style="ConfigManager.TFrame")
        self.cl_entries_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

    def load_calibration(self) -> None:
        """Handle the Load button click to populate calibration entries."""
        cl_dict = get_detector_distances(self.xds_list)
        unique_cl = set(cl_dict.values())
        unique_count = len(unique_cl)

        if unique_count > 5:
            messagebox.showwarning(
                "Too Many Camera Lengths",
                f"Too many different Camera Lengths: {unique_count} kinds.",
            )
            return

        for widget in self.cl_entries_frame.winfo_children():
            widget.destroy()
        self.calibration_entries.clear()

        # Get Distance Factor for display
        try:
            distance_factor = self.distance_factor_var.get()
            if distance_factor == 0:
                messagebox.showerror("Invalid Input", "Distance Factor cannot be zero.")
                return
        except tk.TclError:
            messagebox.showerror("Invalid Input", "Distance Factor must be a number.")
            return

        # Get Universe Ratio
        try:
            universe_ratio = self.universe_ratio_var.get()
        except tk.TclError:
            messagebox.showerror("Invalid Input", "Universe Ratio must be a number.")
            return

        # Create entries for each unique CL
        for cl in unique_cl:
            cl_frame = ttk.Frame(self.cl_entries_frame, style="ConfigManager.TFrame")
            cl_frame.pack(anchor=tk.W, pady=5)

            cl_real = cl / distance_factor
            cl_label = ttk.Label(
                cl_frame,
                text=f"CL {cl_real:.2f} mm, Ratio:",
                font=("Liberation Sans", 15),
                style="ConfigManager.TLabel",
            )
            cl_label.pack(side=tk.LEFT)

            cl_ratio_var = tk.DoubleVar(value=universe_ratio)
            cl_entry = ttk.Entry(
                cl_frame,
                textvariable=cl_ratio_var,
                width=10,
                font=("Liberation Sans", 15),
            )
            cl_entry.pack(side=tk.LEFT, padx=(10, 0))

            self.calibration_entries[cl] = cl_ratio_var

    def clean_calibration(self) -> None:
        """Handle the Clean button click to reset calibration entries."""
        for widget in self.cl_entries_frame.winfo_children():
            widget.destroy()
        self.calibration_entries.clear()
        self.universe_ratio_var.set(1.00)
        self.distance_factor_var.set(1.00)

    def get_calibration_data(self) -> Dict[float, float]:
        """Retrieves calibration data.

        Returns:
            Dict[float, float]: Calibration data mapping camera lengths to ratios.
            Returns "error" for invalid input.
        """
        calibration_data = {}
        for cl, var in self.calibration_entries.items():
            try:
                ratio = var.get()
                calibration_data[cl] = ratio
            except tk.TclError:
                messagebox.showerror("Invalid Input", f"Invalid ratio for CL {cl} mm.")
                return "error"
        return calibration_data

    def has_calibration_changes(self) -> bool:
        """Checks if calibration parameters have changes.

        Returns:
            bool: True if there are changes, otherwise False.
        """
        try:
            if self.universe_ratio_var.get() != 1.00:
                return True
            if self.distance_factor_var.get() != 1.00:
                return True
        except tk.TclError:
            return True  # Treat invalid input as a change

        for ratio in self.calibration_entries.values():
            try:
                if ratio.get() != 1.00:
                    return True
            except tk.TclError:
                return True  # Treat invalid input as a change
        return False


def get_detector_distances(xds_list: List[str]) -> Dict[str, float]:
    """Retrieves the detector distances from XDS.INP files.

    Args:
        xds_list (List[str]): List of XDS.INP file paths.

    Returns:
        Dict[str, float]: Dictionary mapping XDS.INP paths to detector distances.
    """
    detector_distances = {}
    for xds_inp in xds_list:
        try:
            with open(xds_inp, 'r') as file:
                keyword_temp = extract_keywords(file.readlines())
                distance = float(keyword_temp["DETECTOR_DISTANCE"][0])
                detector_distances[xds_inp] = distance
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read {xds_inp}: {e}")
    return detector_distances


class KeywordManagerApp(ttk.Frame):
    """Main application frame for managing keywords in XDS.INP files."""

    def __init__(self, parent: tk.Tk, xds_list: List[str], *args, **kwargs):
        """
        Initializes the KeywordManagerApp.

        Args:
            parent (tk.Tk): Parent window.
            xds_list (List[str]): List of XDS.INP file paths.
        """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.xds_list = xds_list
        self.setup_styles()
        self.setup_ui()

    @staticmethod
    def setup_styles() -> None:
        """Configures styles for the application components."""
        style = ttk.Style()

        style.configure("ConfigManager.TFrame", background="#f3f3f3")
        style.configure(
            "ConfigManager.TLabel", background="#f3f3f3", foreground="#333333"
        )
        style.configure("ConfigManager.TNotebook", background="#f3f3f3")
        style.configure("ConfigManager.TNotebook.Tab", font=("Liberation Sans", 16))
        style.map(
            "ConfigManager.TNotebook.Tab",
            background=[("selected", "#ffffff"), ("!selected", "#dddddd")],
        )
        style.configure("ConfigManager.TButton", font=("Liberation Sans", 15), padding=6)
        style.configure(
            "ConfigManager.TCheckbutton",
            background="#f3f3f3",
            font=("Liberation Sans", 15),
        )

    def setup_ui(self) -> None:
        """Sets up the user interface components."""
        self.configure(style="ConfigManager.TFrame")

        # Title Label
        title_label = ttk.Label(
            self,
            text=(
                "Add, Replace or Delete Keywords in XDS.INPs.\n"
                "The Keyword Entry has AutoComplete Function."
            ),
            style="ConfigManager.TLabel",
        )
        title_label.pack(padx=10, pady=10, fill="x")

        # Notebook (Tabs)
        notebook = ttk.Notebook(self, style="ConfigManager.TNotebook")
        notebook.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Create Add, Delete, and Calibrate Tabs
        add_frame = ttk.Frame(notebook, style="ConfigManager.TFrame")
        notebook.add(add_frame, text="Add")

        delete_frame = ttk.Frame(notebook, style="ConfigManager.TFrame")
        notebook.add(delete_frame, text="Delete")

        calibrate_frame = ttk.Frame(notebook, style="ConfigManager.TFrame")
        notebook.add(calibrate_frame, text="Calibrate")  # New Calibrate Tab

        # Initialize Tabs
        keywords = self.get_keywords()
        self.add_tab = AddTab(add_frame, keywords)
        self.delete_tab = DeleteTab(delete_frame, keywords)
        self.calibrate_tab = CalibrateTab(calibrate_frame, keywords, self.xds_list)  # Initialize CalibrateTab

        # Bottom Frame for Save, Cancel Buttons, and Checkbox
        bottom_frame = ttk.Frame(self, style="ConfigManager.TFrame")
        bottom_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Checkbox for Force Replace Multivalue Keyword
        self.force_replace_var = tk.BooleanVar()
        force_replace_checkbox = ttk.Checkbutton(
            bottom_frame,
            text="  Force Replace",
            variable=self.force_replace_var,
            onvalue=True,
            offvalue=False,
            style="ConfigManager.TCheckbutton",
        )
        force_replace_checkbox.pack(side=tk.LEFT, padx=(0, 20))

        # Spacer
        spacer = ttk.Label(bottom_frame, text="", style="ConfigManager.TLabel")
        spacer.pack(side=tk.LEFT, expand=True)

        # Cancel Button
        cancel_button = ttk.Button(
            bottom_frame,
            text="Cancel",
            command=self.cancel_data,
            style="ConfigManager.TButton",
        )
        cancel_button.pack(side=tk.RIGHT, padx=(20, 0))

        # Save Button
        save_button = ttk.Button(
            bottom_frame,
            text="Save",
            command=self.save_data,
            style="ConfigManager.TButton",
        )
        save_button.pack(side=tk.RIGHT, padx=(20, 0))

    @classmethod
    def get_keywords(cls) -> List[str]:
        """Defines and returns the list of keywords for autocomplete.

        Returns:
            List[str]: List of available keywords.
        """
        return [
            "MAXIMUM_NUMBER_OF_JOBS",
            "MAXIMUM_NUMBER_OF_PROCESSORS",
            "SECONDS",
            "NUMBER_OF_IMAGES_IN_CACHE",
            "TEST",
            "OVERLOAD",
            "GAIN",
            "TRUSTED_REGION",
            "VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS",
            "INCLUDE_RESOLUTION_RANGE",
            "MINIMUM_ZETA",
            "ORGX",
            "ORGY",
            "ROTATION_AXIS",
            "WFAC1",
            "FRACTION_OF_POLARIZATION",
            "AIR",
            "FRIEDEL'S_LAW",
            "MAX_CELL_AXIS_ERROR",
            "MAX_CELL_ANGLE_ERROR",
            "TEST_RESOLUTION_RANGE",
            "MIN_RFL_Rmeas",
            "MAX_FAC_Rmeas",
            "NBX",
            "NBY",
            "BACKGROUND_PIXEL",
            "STRONG_PIXEL",
            "MAXIMUM_NUMBER_OF_STRONG_PIXELS",
            "MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT",
            "MAXIMUM_IMAGE_GAP_FOR_ADDING_PARTIALS",
            "SPOT_MAXIMUM-CENTROID",
            "RGRID",
            "SEPMIN",
            "CLUSTER_RADIUS",
            "INDEX_ERROR",
            "INDEX_MAGNITUDE",
            "INDEX_QUALITY",
            "MERGE_TREE",
            "MAXIMUM_ERROR_OF_SPOT_POSITION",
            "MAXIMUM_ERROR_OF_SPINDLE_POSITION",
            "MINIMUM_FRACTION_OF_INDEXED_SPOTS",
            "DEFAULT_REFINE_SEGMENT",
            "MINIMUM_I/SIGMA",
            "REFLECTING_RANGE",
            "REFLECTING_RANGE_E.S.D.",
            "BEAM_DIVERGENCE",
            "MINPK",
            "BEAM_DIVERGENCE_E.S.D.",
            "RELRAD",
            "RELBET",
            "NUMBER_OF_PROFILE_GRID_POINTS_ALONG_ALPHA/BETA",
            "NUMBER_OF_PROFILE_GRID_POINTS_ALONG_GAMMA",
            "CUT",
            "DELPHI",
            "SIGNAL_PIXEL",
            "NBATCH",
            "STRICT_ABSORPTION_CORRECTION",
            "SNRC",
            "BATCHSIZE",
            "REFLECTIONS/CORRECTION_FACTOR",
            "DETECTOR_DISTANCE",
            "UNIT_CELL_CONSTANTS",
            "UNTRUSTED_RECTANGLE",
            "UNTRUSTED_ELLIPSE",
            "UNTRUSTED_QUADRILATERAL",
            "EXCLUDE_RESOLUTION_RANGE",
            "JOB",
            'SPACE_GROUP_NUMBER'
        ]

    def save_data(self) -> None:
        """Handles the save action by validating and processing data."""
        add_data = self.add_tab.get_data()
        delete_data = self.delete_tab.get_data()
        calibration_data = self.calibrate_tab.get_calibration_data()
        force_replace = self.force_replace_var.get()

        # Check if Add/Delete and Calibration are both being used
        add_delete_active = (add_data != "error" and add_data) or (delete_data != "error" and delete_data)
        calibration_active = self.calibrate_tab.has_calibration_changes()

        if add_delete_active and calibration_active:
            messagebox.showwarning(
                "Operation Conflict",
                "Add/Delete Keyword cannot perform at the same time with Calibration.",
            )
            return

        if add_delete_active:
            if add_data == "error" or delete_data == "error":
                return

            # Validate add_data and delete_data
            for item in add_data or []:
                item["result"] = validate_data(item["key"], item["value"])
            for item in delete_data or []:
                item["result"] = validate_data(item["key"], "0")

            # Summary lists for different validation results
            unsupported_params = []
            wrong_params = []
            value_err_params = []
            multi_times_params = []

            # Helper function to classify validation results
            def classify_results(data_list, append_value_err=False):
                for item in data_list:
                    if item["result"] == "fix":
                        unsupported_params.append(f"{item['key']}= {item['value']}")
                    elif item["result"] == "wrong":
                        wrong_params.append(f"{item['key']}= {item['value']}")
                    elif append_value_err and item["result"] == "value-err":
                        value_err_params.append(f"{item['key']}= {item['value']}")

            # Classify add_data and delete_data
            if add_data:
                classify_results(add_data, append_value_err=True)
            if delete_data:
                classify_results(delete_data)

            # Check for keyword overlaps between add_data and delete_data
            add_keys = {item["key"] for item in add_data} if add_data else set()
            delete_keys = {item["key"] for item in delete_data} if delete_data else set()
            multi_times_params.extend(add_keys.intersection(delete_keys))

            # Check for multiple occurrences of the same key in add_data
            if add_data:
                key_counter = Counter(item["key"] for item in add_data)
                for key, count in key_counter.items():
                    if count > 1:
                        results = [item["result"] for item in add_data if item["key"] == key]
                        if not all(result == "pass-multi" for result in results):
                            multi_times_params.append(key)

            # Build the warning message
            warning_message_parts = []
            if unsupported_params:
                warning_message_parts.append(
                    "Below Parameters are not supported:\n" + "\n".join(unsupported_params)
                )
            if wrong_params:
                warning_message_parts.append(
                    "Below Parameters are incorrect:\n" + "\n".join(wrong_params)
                )
            if value_err_params:
                warning_message_parts.append(
                    "Below Parameters have incorrect number of variables:\n"
                    + "\n".join(value_err_params)
                )
            if multi_times_params:
                warning_message_parts.append(
                    "Below Parameters appear multiple times:\n" + "\n".join(multi_times_params)
                )

            # Display the warning message box if there is any message to show
            if warning_message_parts:
                warning_message = "\n\n".join(warning_message_parts)
                messagebox.showwarning("Data Validation Warning", warning_message)
                return

            # Proceed with saving data if no warnings
            if messagebox.askokcancel(
                    "Add/Delete Keywords",
                    f"{len(add_data)} Parameters will be {'replaced' if force_replace else 'added'} "
                    f"and {len(delete_data)} Parameters will be muted. Do you wish to continue?"):
                self.process_save(add_data, delete_data, None, force_replace, self.xds_list)
            return

        if calibration_active:
            # Retrieve calibration data
            if calibration_data == "error":
                return
            calibration_data = self.calibrate_tab.get_calibration_data()
            universe_ratio = self.calibrate_tab.universe_ratio_var.get()
            distance_factor = self.calibrate_tab.distance_factor_var.get()

            if calibration_data == "error":
                return

            # Build calibration details for confirmation message
            calibration_details = ""
            for cl, ratio in calibration_data.items():
                cl_real = cl / distance_factor
                calibration_details += f"CL {cl_real:.2f} mm: {ratio:.2f}\n"

            if messagebox.askokcancel(
                    "Calibrate Keywords",
                    f"Calibration will be applied with Universe Ratio = {universe_ratio:.2f} and "
                    f"Distance Factor = {distance_factor:.2f}.\n\n"
                    f"Camera Length Ratios:\n{calibration_details}\nDo you wish to continue?"):
                self.calibrate_CL(calibration_data, universe_ratio)
                self.parent.destroy()
            return

        # If neither Add/Delete nor Calibration is active
        messagebox.showinfo("No Action", "No data to save.")
        return

    def process_save(
        self, add_data: List[Dict[str, str]],
            delete_data: List[Dict[str, str]],
            calibrate_data: Dict[float, float],
            force_replace: bool, xds_list: List[str]) -> None:
        """
        Processes and saves the validated data to XDS.INP files.

        Args:
            add_data (List[Dict[str, str]]): Keywords to add or replace.
            delete_data (List[Dict[str, str]]): Keywords to delete.
            calibrate_data (Dict[float, float]): Calibration data. Defaults to None.
            force_replace (bool): Whether to force replace existing keywords.
            xds_list (List[str]): List of XDS.INP file paths.
        """
        for xds_inp in xds_list:
            try:
                with open(xds_inp, "r+") as f:
                    lines = f.readlines()
                    for data in add_data:
                        lines = replace_value(lines, data["key"], [data["value"]], comment=False,
                                              add=(not force_replace and data["result"] == "pass-multi"))
                    for data in delete_data:
                        lines = replace_value(lines, data["key"], [data["value"]], comment=True)
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                print(f"{xds_inp} has been changed.\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save {xds_inp}: {e}")
        print("\n")
        self.parent.destroy()

    def calibrate_CL(self, calibration_data: Dict[float, float], universe_ratio: float) -> None:
        """
        Applies calibration changes to XDS.INP files.

        Args:
            calibration_data (Dict[float, float]): Calibration data mapping camera lengths to ratios.
            universe_ratio (float): Universal calibration ratio.
        """
        if calibration_data:
            cl_dict = get_detector_distances(self.xds_list)
            for path, camera_length in cl_dict.items():
                with open(path, "r+") as f:
                    lines = f.readlines()
                    lines = replace_value(lines,
                                          "DETECTOR_DISTANCE",
                                          [f"{camera_length / calibration_data[camera_length]:.2f}"],
                                          comment=False)
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
        else:
            cl_dict = get_detector_distances(self.xds_list)
            for path, camera_length in cl_dict.items():
                with open(path, "r+") as f:
                    lines = f.readlines()
                    lines = replace_value(lines,
                                          "DETECTOR_DISTANCE",
                                          [f"{camera_length / universe_ratio:.2f}"],
                                          comment=False)
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()

    def cancel_data(self) -> None:
        """Handles the cancel action by confirming and closing the window."""
        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to discard and close the window?"
        )
        if confirm:
            self.parent.destroy()


def create_keyword_manager_app(xds_list: List[str]) -> None:
    """Creates and displays the Keyword Manager application window.

    Args:
        xds_list (List[str]): List of XDS.INP file paths to manage.
    """
    keyword_window = tk.Toplevel()
    keyword_window.title("Keyword Manager")
    keyword_window.geometry("800x700")  # Increased height to accommodate Calibrate tab
    keyword_window.configure(bg="#f3f3f3")  # Light background

    # Initialize KeywordManagerApp within the pop-up window
    app = KeywordManagerApp(keyword_window, xds_list)
    app.pack(fill=tk.BOTH, expand=True)

    # Handle window close
    keyword_window.protocol("WM_DELETE_WINDOW", keyword_window.destroy)


def validate_data(keyword: str, value: str) -> str:
    """Validates a keyword and its value.

    Args:
        keyword (str): Keyword to validate.
        value (str): Associated value.

    Returns:
        str: Validation result ("fix", "pass-single", "pass-multi", "value-err", or "wrong").
    """
    keyword_dict = {
        "fix": [
            "CLUSTER_NODES",
            "DETECTOR",
            "NX",
            "NY",
            "QX",
            "QY",
            "MINIMUM_VALID_PIXEL_VALUE",
            "SILICON",
            "SENSOR_THICKNESS",
            "ROFF",
            "TOFF",
            "STOE_CALIBRATION_PARAMETERS",
            "BRASS_PLATE_IMAGE",
            "HOLE_DISTANCE",
            "MXHOLE",
            "MNHOLE",
            "X-GEO_CORR",
            "Y-GEO_CORR",
            "DARK_CURRENT_IMAGE",
            "OFFSET",
            "DIRECTION_OF_DETECTOR_X-AXIS",
            "DIRECTION_OF_DETECTOR_Y-AXIS",
            "SEGMENT",
            "REFINE_SEGMENT",
            "DIRECTION_OF_SEGMENT_X-AXIS",
            "DIRECTION_OF_SEGMENT_Y-AXIS",
            "SEGMENT_ORGX",
            "SEGMENT_ORGY",
            "SEGMENT_DISTANCE",
            "OSCILLATION_RANGE",
            "STARTING_ANGLE",
            "STARTING_FRAME",
            "STARTING_ANGLES_OF_SPINDLE_ROTATION",
            "TOTAL_SPINDLE_ROTATION_RANGES",
            "RESOLUTION_SHELLS",
            "X-RAY_WAVELENGTH",
            "INCIDENT_BEAM_DIRECTION",
            "POLARIZATION_PLANE_NORMAL",
            "UNIT_CELL_A-AXIS",
            "UNIT_CELL_B-AXIS",
            "UNIT_CELL_C-AXIS",
            "REIDX",
            "INDEX_ORIGIN",
            "PROFILE_FITTING",
            "PATCH_SHUTTER_PROBLEM",
            "CORRECTIONS",
            "REFERENCE_DATA_SET",
            "FIT_B-FACTOR_TO_REFERENCE_DATA_SET",
            "REJECT_ALIEN",
            "DATA_RANGE_FIXED_SCALE_FACTOR",
            "NAME_TEMPLATE_OF_DATA_FRAMES",
            "LIB",
            "DATA_RANGE",
            "EXCLUDE_DATA_RANGE",
            "SPOT_RANGE",
            "BACKGROUND_RANGE",
            "MINIMUM_NUMBER_OF_REFLECTIONS/SEGMENT",
        ],
        "single_value": [
            "MAXIMUM_NUMBER_OF_JOBS",
            "MAXIMUM_NUMBER_OF_PROCESSORS",
            "SECONDS",
            "NUMBER_OF_IMAGES_IN_CACHE",
            "TEST",
            "OVERLOAD",
            "GAIN",
            "TRUSTED_REGION",
            "VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS",
            "INCLUDE_RESOLUTION_RANGE",
            "MINIMUM_ZETA",
            "ORGX",
            "ORGY",
            "ROTATION_AXIS",
            "WFAC1",
            "FRACTION_OF_POLARIZATION",
            "AIR",
            "FRIEDEL'S_LAW",
            "MAX_CELL_AXIS_ERROR",
            "MAX_CELL_ANGLE_ERROR",
            "TEST_RESOLUTION_RANGE",
            "MIN_RFL_Rmeas",
            "MAX_FAC_Rmeas",
            "NBX",
            "NBY",
            "BACKGROUND_PIXEL",
            "STRONG_PIXEL",
            "MAXIMUM_NUMBER_OF_STRONG_PIXELS",
            "MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT",
            "MAXIMUM_IMAGE_GAP_FOR_ADDING_PARTIALS",
            "SPOT_MAXIMUM-CENTROID",
            "RGRID",
            "SEPMIN",
            "CLUSTER_RADIUS",
            "INDEX_ERROR",
            "INDEX_MAGNITUDE",
            "INDEX_QUALITY",
            "MERGE_TREE",
            "MAXIMUM_ERROR_OF_SPOT_POSITION",
            "MAXIMUM_ERROR_OF_SPINDLE_POSITION",
            "MINIMUM_FRACTION_OF_INDEXED_SPOTS",
            "DEFAULT_REFINE_SEGMENT",
            "MINIMUM_I/SIGMA",
            "REFLECTING_RANGE",
            "REFLECTING_RANGE_E.S.D.",
            "BEAM_DIVERGENCE",
            "MINPK",
            "BEAM_DIVERGENCE_E.S.D.",
            "RELRAD",
            "RELBET",
            "NUMBER_OF_PROFILE_GRID_POINTS_ALONG_ALPHA/BETA",
            "NUMBER_OF_PROFILE_GRID_POINTS_ALONG_GAMMA",
            "CUT",
            "DELPHI",
            "SIGNAL_PIXEL",
            "NBATCH",
            "STRICT_ABSORPTION_CORRECTION",
            "SNRC",
            "BATCHSIZE",
            "REFLECTIONS/CORRECTION_FACTOR",
            "DETECTOR_DISTANCE",
            "UNIT_CELL_CONSTANTS",
            'SPACE_GROUP_NUMBER'
        ],
        "multi_value": [
            "UNTRUSTED_RECTANGLE",
            "UNTRUSTED_ELLIPSE",
            "UNTRUSTED_QUADRILATERAL",
            "EXCLUDE_RESOLUTION_RANGE",
            "JOB",
        ],
    }

    value_num = {
        "JOB": 0,
        "TRUSTED_REGION": 2,
        "UNTRUSTED_RECTANGLE": 4,
        "UNTRUSTED_ELLIPSE": 4,
        "UNTRUSTED_QUADRILATERAL": 8,
        "VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS": 2,
        "INCLUDE_RESOLUTION_RANGE": 2,
        "EXCLUDE_RESOLUTION_RANGE": 2,
        "ROTATION_AXIS": 3,
        "UNIT_CELL_CONSTANTS": 6,
        "TEST_RESOLUTION_RANGE": 2,
    }

    if keyword in keyword_dict["fix"]:
        return "fix"

    if keyword in keyword_dict["single_value"] or keyword in keyword_dict["multi_value"]:
        split_value = value.split()
        expected_num = value_num.get(keyword)

        if expected_num is None:
            return (
                "pass-single"
                if keyword in keyword_dict["single_value"]
                else "pass-multi"
            )

        if len(split_value) == expected_num or expected_num == 0:
            return (
                "pass-single"
                if keyword in keyword_dict["single_value"]
                else "pass-multi"
            )
        else:
            return "value-err"
    return "wrong"


def read_cRED_log(file_path: str) -> int:
    """Reads a cRED log file and extracts the total number of frames and images.

    Args:
        file_path (str): Path to the cRED log file.

    Returns:
        int: Total number of frames and images combined.
    """
    frames = 0
    images = 0
    with open(file_path, 'r', errors="ignore") as file:
        for line in file.readlines():
            if "Number of frames" in line:
                frames = int(line.split(":")[1].strip())
            elif "Number of images" in line:
                images = int(line.split(":")[1].strip())

    return frames + images
