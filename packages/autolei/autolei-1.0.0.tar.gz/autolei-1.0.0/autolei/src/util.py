"""
Utility Module
==============

Provides utility functions and classes for common programming tasks, including string
manipulation, file management, GUI interactions, statistical analysis, and thread management.

Features:
    - Path and String Utilities:
        Functions for path conversions (Linux <-> Windows), natural sorting of strings, and
        string cleaning or validation.
    - File Management Utilities:
        Tools for finding, deleting, and managing files and folders in directory structures.
    - Tkinter Widget Utilities:
        Functions and classes for interacting with and enhancing Tkinter widgets, including
        tooltips and content replacement.
    - Statistical Analysis Utilities:
        Methods for detecting and handling outliers using the Interquartile Range (IQR) method.
    - Other Utilities:
        Miscellaneous tools, including thread management and environment checks.

Classes:
    Page: A custom Tkinter frame with specific styling for Combobox widgets.
    ToolTip: A widget that provides on-hover tooltips for Tkinter elements.
    KillableThread: A thread implementation that allows for safe termination.

Dependencies:
    Standard Libraries:
        - os
        - ctypes
        - platform
        - shutil
        - threading
        - tkinter
        - datetime
        - re
        - subprocess
    Third-Party Libraries:
        - numpy

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen
    - License: BSD 3-clause
"""

import ctypes
import inspect
import os
import platform
import re
import shutil
import subprocess
import threading
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

import numpy as np


# *******************************
# 1. Path and String Utilities
# *******************************


def strtobool(val: str) -> bool:
    """Converts a string representation of truth to its boolean equivalent.

    Args:
        val (str): The string to convert.

    Returns:
        bool: True for truthy values, False for falsy values.

    Raises:
        ValueError: If the input string is not recognized as a truthy or falsy value.
    """
    if isinstance(val, bool):
        return val

    true_set = {'y', 'yes', 't', 'true', 'on', '1'}
    false_set = {'n', 'no', 'f', 'false', 'off', '0'}

    val_lower = val.lower()
    if val_lower in true_set:
        return True
    elif val_lower in false_set:
        return False
    else:
        raise ValueError(f"Invalid truth value '{val}'.")


def natural_sort_key(s: str) -> list:
    """Generates a natural sort key for sorting strings.

    Args:
        s (str): The input string to process.

    Returns:
        list: A list of components for natural sorting.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def linux_to_windows_path(linux_path: str) -> str:
    """Converts a Linux path to a Windows path.

    Args:
        linux_path (str): The Linux-style path.

    Returns:
        str: The converted Windows-style path.

    Raises:
        ValueError: If the input path is not a valid Linux-style path.
    """
    if linux_path.startswith("/mnt/"):
        # Strip the leading '/mnt/' from the path
        path_without_mnt = linux_path[5:]

        # Replace the first slash with a colon to form the drive letter specifier
        if '/' not in path_without_mnt:
            raise ValueError("Invalid WSL path format.")
        drive, *rest = path_without_mnt.split('/', 1)
        windows_path = "{}:\\{}".format(drive.upper(), rest[0].replace('/', '\\')) if rest else f"{drive.upper()}:\\"
        return windows_path
    else:
        raise ValueError("Path does not start with '/mnt/', so it may not be a WSL path.")


def windows_to_linux_path(windows_path: str) -> str:
    """Converts a Windows path to a Linux path.

    Args:
        windows_path (str): The Windows-style path.

    Returns:
        str: The converted Linux-style path.

    Raises:
        ValueError: If the input path is not a valid Windows-style path.
    """
    # Ensure path contains a drive letter and backslashes
    if ":" not in windows_path or "\\" not in windows_path:
        raise ValueError("Invalid Windows path format.")

    # Split the drive letter and path
    drive, *rest = windows_path.split(":\\", 1)

    # Convert drive letter to lowercase and prepend '/mnt/'
    linux_path = f"/mnt/{drive.lower()}"

    # Replace backslashes with slashes for WSL format
    if rest:
        linux_path += '/' + rest[0].replace("\\", "/")

    return linux_path


def extract_pattern(file_list: list) -> tuple:
    """Extracts a pattern from a list of file paths.

    Args:
        file_list (list): List of file paths.

    Returns:
        tuple: A pattern string, the first number, and the last number extracted.
    """
    if not file_list:
        return "", 0, 0

    sorted_files = sorted(file_list, key=natural_sort_key)
    prefix = sorted_files[0]
    suffix = sorted_files[0]

    for path in sorted_files[1:]:
        while not path.startswith(prefix) and prefix:
            prefix = prefix[:-1]
        while not path.endswith(suffix) and suffix:
            suffix = suffix[1:]

    if len(prefix) + len(suffix) >= len(sorted_files[0]):
        return sorted_files[0], 0, 0

    varying_length = len(sorted_files[0]) - len(prefix) - len(suffix)
    pattern_varying_part = '?' * varying_length
    pattern = f"{prefix}{pattern_varying_part}{suffix}"

    # Extract varying parts and convert to integers
    varying_numbers = []
    for path in sorted_files:
        varying_part = path[len(prefix):-len(suffix)] if len(suffix) != 0 else path[len(prefix):]
        try:
            number = int(varying_part)
            varying_numbers.append(number)
        except ValueError:
            # Non-integer varying part
            pass

    first_number = min(varying_numbers) if varying_numbers else 0
    last_number = max(varying_numbers) if varying_numbers else 0

    return pattern, first_number, last_number


def timestamp_string(timestamp: float) -> str:
    """Converts a float timestamp to a formatted date string.

    Args:
        timestamp (float): The timestamp to convert.

    Returns:
        str: Formatted date string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    start_date = datetime(1899, 12, 30)
    result_date = start_date + timedelta(days=timestamp)
    return result_date.strftime('%Y-%m-%d %H:%M:%S')


def clean_string(input_string: str) -> str:
    """Cleans a string by removing non-ASCII characters.

    Args:
        input_string (str): The string to clean.

    Returns:
        str: The cleaned string.
    """
    cleaned_string = re.sub(r'\\x[0-9a-fA-F]{2}', '', input_string)
    if cleaned_string.startswith(("b'", 'b"')):
        cleaned_string = cleaned_string[2:-1]
    return cleaned_string


def is_suitable_linux_folder_name(name: str) -> bool:
    """Checks if a string is a valid Linux folder name.

    Args:
        name (str): The folder name to validate.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    if not name or len(name) > 255:
        return False

    valid_name_pattern = re.compile(r'^[\w.\-]+$')
    if not valid_name_pattern.match(name):
        return False

    if name.startswith(('-', '.')):
        return False

    return True


def unit_cell_with_esd(cell: list, cell_esd: list) -> list:
    """Formats unit cell values with associated errors.

    Args:
        cell (list): A list of numerical values.
        cell_esd (list): A list of associated errors.

    Returns:
        list: Formatted strings representing values with errors.
    """
    output_cell = []
    for value, error in zip(cell, cell_esd):
        if error == 0.0:
            # If there's no error, append the integer part of the value
            output_cell.append(str(int(value)))
        else:
            # Convert error to scientific notation with one decimal place
            error_str = f"{error:.1e}"
            match = re.search(r'(\d)\.?(\d*)e([+-]?\d+)', error_str)
            if match:
                first_digit = match.group(1)
                exponent = int(match.group(3))
                decimal_places = -exponent
            else:
                first_digit = '0'
                decimal_places = 0

            # Format the value to the required number of decimal places
            formatted_value = f"{value:.{decimal_places}f}"

            # Append the uncertainty digit in parentheses
            error_output_str = f"{formatted_value}({first_digit})"
            output_cell.append(error_output_str)
    return output_cell


# *******************************
# 2. File Management Utilities
# *******************************

def find_files(directory: str, filename: str, path_filter: bool = False) -> list:
    """Finds files with a specific name in a directory and its subdirectories.

    Args:
        directory (str): The directory to search.
        filename (str): The name of the file to search for.
        path_filter (bool): If True, applies filtering to exclude certain paths.

    Returns:
        list: A sorted list of matching file paths.
    """
    matching_files = []
    filename_lower = filename.lower()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower() == filename_lower:
                if path_filter and ("!" in root or "/." in root):
                    pass
                else:
                    matching_files.append(os.path.join(root, file))
    return sorted(matching_files, key=natural_sort_key)


def find_folders_with_images(root_path: str, extension: str = ".img",
                             min_img_count: int = 10,
                             path_filter: bool = False) -> list:
    """Finds folders containing a minimum number of image files.

    Args:
        root_path (str): The root directory to search.
        extension (str): The file extension to look for. Defaults to '.img'.
        min_img_count (int): Minimum number of images required. Defaults to 10.
        path_filter (bool): If True, applies filtering to exclude certain paths.

    Returns:
        list: A sorted list of folder paths containing images.
    """

    folders_paths = []
    for dirpath, _, filenames in os.walk(root_path):
        img_files_count = sum(1 for file in filenames if file.lower().endswith(extension.lower()))
        if img_files_count >= min_img_count:
            if path_filter and ("!" in dirpath or "/." in dirpath):
                pass
            else:
                folders_paths.append(dirpath)
    return sorted(folders_paths, key=natural_sort_key)


def delete_files(directory: str, target_filename: str) -> None:
    """Deletes all files with a specific name in a directory.

    Args:
        directory (str): The directory to search.
        target_filename (str): The name of the files to delete.
    """
    target_filename_lower = target_filename.lower()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower() == target_filename_lower:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")


def delete_folders(directory: str, target_foldername: str) -> None:
    """Deletes all folders with a specific name in a directory.

    Args:
        directory (str): The directory to search.
        target_foldername (str): The name of the folders to delete.
    """
    target_foldername_lower = target_foldername.lower()
    for root, dirs, _ in os.walk(directory, topdown=False):
        for _dir in dirs:
            if _dir.lower() == target_foldername_lower:
                folder_path = os.path.join(root, _dir)
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder: {folder_path}")
                except Exception as e:
                    print(f"Failed to delete {folder_path}: {e}")


# *******************************
# 3. Tkinter Widget Utilities
# *******************************

class Page(tk.Frame):
    """A custom Tkinter Frame with styling adjustments for Combobox widgets."""

    def __init__(self, parent):
        """Initializes the Page with specific styles.

        Args:
            parent (tk.Widget): The parent widget to attach this frame.
        """
        tk.Frame.__init__(self, parent, bg='white')
        ttk.Style().map('TCombobox',
                        fieldbackground=[('readonly', 'white')],
                        background=[('readonly', 'white')],
                        selectbackground=[('!readonly', 'white')],
                        selectforeground=[('!readonly', 'black')])


class ToolTip:
    """A tooltip widget for displaying additional information on hover.

    Usage:
        tooltip = ToolTip(widget, text="Your tooltip text")
    """

    def __init__(self, widget, text='widget info'):
        """Initializes the tooltip for a widget.

        Args:
            widget (tk.Widget): The widget to attach the tooltip to.
            text (str, optional): The tooltip text. Defaults to 'widget info'.
        """
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        """Handles mouse entering the widget."""
        self.schedule()

    def leave(self, event=None):
        """Handles mouse leaving the widget."""
        self.unschedule()
        self.hide_tooltip()

    def schedule(self):
        """Schedules the tooltip to appear after a delay."""
        self.unschedule()
        self.id = self.widget.after(500, self.show_tooltip)  # delay in ms

    def unschedule(self):
        """Cancels the scheduled tooltip display."""
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tooltip(self):
        """Displays the tooltip."""
        if self.tooltip_window or not self.text:
            return
        # Create a new Toplevel window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove all window decorations

        # Position the tooltip directly under the widget
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5  # Slight offset below the widget
        tw.wm_geometry(f"+{x}+{y}")

        # Add a label inside the Toplevel
        label = tk.Label(
            tw,
            text=self.text,
            justify='left',
            background="#ffffe0",  # Light yellow background
            relief='solid',
            borderwidth=1,
            font=("Liberation Sans", "12", "normal"),
        )
        label.pack(ipadx=1)

    def hide_tooltip(self):
        """Hides the tooltip."""
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


def replace_entry(entry: tk.Entry, replace_str: str) -> None:
    """Replaces the content of a Tkinter Entry widget.

    Args:
        entry (tk.Entry): The Tkinter Entry widget to modify.
        replace_str (str): The text to replace the current content.
    """
    entry.delete(0, tk.END)
    entry.insert(0, replace_str)


def replace_entry_readonly(entry: tk.Entry, replace_str: str) -> None:
    """Replaces the content of a read-only Tkinter Entry widget.

    Args:
        entry (tk.Entry): The Tkinter Entry widget to modify.
        replace_str (str): The text to replace the current content.
    """
    entry.config(state='normal')
    entry.delete(0, tk.END)
    entry.insert(0, replace_str)
    entry.config(state="readonly")


def replace_text(text_widget: tk.Text, replace_str: str) -> None:
    """Replaces the content of a Tkinter Text widget.

    Args:
        text_widget (tk.Text): The Tkinter Text widget to modify.
        replace_str (str): The text to replace the current content.
    """
    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", replace_str)


# *******************************
# 4. Statistical Analysis Utilities
# *******************************

def remove_outliers_iqr(data: list, ratio: float = 1.5, offset: float = 0) -> list:
    """Removes outliers from a dataset using the IQR method.

    Args:
        data (list): The dataset to process.
        ratio (float): Multiplier for the IQR. Defaults to 1.5.
        offset (float): Minimum IQR to prevent zero IQR. Defaults to 0.

    Returns:
        list: The dataset with outliers removed.
    """
    if not data:
        return []

    q25, q75 = np.percentile(data, [25, 75])
    iqr = max(q75 - q25, offset)
    cutoff = iqr * ratio
    lower, upper = q25 - cutoff, q75 + cutoff
    return [x for x in data if lower < x < upper]


def outliers_iqr_dict(scales: dict, ratio: float) -> list:
    """Identifies outlier keys in a dictionary based on their values.

    Args:
        scales (dict): A dictionary of numeric values to analyze.
        ratio (float): Multiplier for the IQR.

    Returns:
        list: List of keys corresponding to outlier values.
    """

    def find_outliers(_values, keys, _ratio):
        q1 = np.percentile(_values, 25)
        q3 = np.percentile(_values, 75)
        iqr = max(q3 - q1, 0.1)
        upper_bound = q3 + _ratio * iqr
        lower_bound = q1 - _ratio * iqr
        return [key for key, value in zip(keys, _values) if value == 0 or value > upper_bound or value < lower_bound]

    values = [value for value in scales.values() if value != 0.0]
    corresponding_keys = [key for key, value in scales.items() if value != 0.0]
    zero_keys = [key for key, value in scales.items() if value == 0.0]

    outlier_keys = find_outliers(values, corresponding_keys, ratio)
    return sorted(list(set(outlier_keys + zero_keys)))


# *******************************
# 5. Other Utilities
# *******************************

def get_elements_by_indices(data_list: list, indices_list: str) -> list:
    """Retrieves elements from a list based on a comma-separated list of indices.

    Args:
        data_list (list): The list of elements to retrieve from.
        indices_list (str): A comma-separated string of indices or ranges.

    Returns:
        list: The elements selected from the list.
    """
    try:
        indices = set()  # Use a set to avoid duplicate indices
        for part in indices_list.split(","):
            part = part.strip()
            if '-' in part:
                # Handle range of indices, e.g., "1-9"
                start, end = part.split('-')
                start = int(start)
                end = int(end)
                if start > end:
                    raise ValueError(f"Invalid range '{part}': start index is greater than end index.")
                indices.update(range(start, end + 1))
            else:
                # Handle single index, e.g., "10" or "11"
                index = int(part)
                indices.add(index)

        # Select elements based on the parsed indices
        selected_elements = [
            data_list[index - 1]  # Adjust for 1-based indexing
            for index in sorted(indices)  # Sort for consistent order
            if 0 < index <= len(data_list)
        ]
        return selected_elements
    except ValueError as ve:
        print(f"Value error: {ve}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


class KillableThread(threading.Thread):
    """A thread class that supports termination via raising an exception."""

    def _get_my_tid(self) -> int:
        """Retrieves the thread ID of the current thread.

        Returns:
            int: The thread ID.

        Raises:
            threading.ThreadError: If the thread is not active.
        """
        if not self.is_alive():
            raise threading.ThreadError("The thread is not active.")

        # Attempt to find thread ID from active threads
        for tid, tobj in threading._active.items():
            if tobj is self:
                return tid

        raise AssertionError("Could not determine the thread's id.")

    def raise_exc(self, exctype):
        """Raises an exception in the thread's context.

        Args:
            exctype (Exception): The exception type to raise.

        Raises:
            TypeError: If the exception type is invalid.
        """
        if not inspect.isclass(exctype):
            raise TypeError("Only exception types can be raised.")
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        """Terminates the thread by raising a SystemExit exception."""
        if self.is_alive():
            self.raise_exc(SystemExit)


def _async_raise(tid: int, exctype: Exception) -> None:
    """Raises an exception in the context of the specified thread.

    Args:
        tid (int): The thread ID in which to raise the exception.
        exctype (type): The exception type to raise.

    Raises:
        ValueError: If the thread ID is invalid.
        SystemError: If multiple threads are affected, indicating an internal failure.
    """
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread ID.")
    elif res != 1:
        # Revert the exception if multiple threads were affected
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed.")


def is_wsl() -> bool:
    """Checks if the current environment is Windows Subsystem for Linux (WSL).

    Returns:
        bool: True if running on WSL, False otherwise.
    """
    release_check = 'microsoft' in platform.uname().release.lower()
    env_check = 'WSL_DISTRO_NAME' in os.environ
    return release_check or env_check


def open_folder_linux(path: str) -> None:
    """Opens a folder in the default file manager on Linux.

    Args:
        path (str): The path to the folder to open.
    """
    file_managers = ['xdg-open', 'nautilus', 'dolphin', 'thunar', 'pcmanfm']
    for fm in file_managers:
        try:
            subprocess.Popen([fm, path])
            return
        except FileNotFoundError:
            continue
    print("No known file manager found. Please install one or open manually.")
