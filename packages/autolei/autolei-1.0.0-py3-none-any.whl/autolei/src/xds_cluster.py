"""
XDS Clustering Module
=====================

Provides tools for clustering X-ray diffraction datasets using correlation coefficients
from `XSCALE.LP` files. Supports dataset filtering, dendrogram computation and plotting,
cluster formation, and Bravais lattice analysis for crystallographic data.

Features:
    - Parse `XSCALE.LP` files to extract filenames, unit cell parameters, space group, and correlation matrices.
    - Compute and visualize dendrograms for dataset clustering.
    - Filter datasets based on specific criteria such as CC1/2, resolution, and ISa.
    - Form and merge clusters based on dendrogram thresholds.
    - Analyze lattice symmetry and aggregate results by Bravais lattice types.

Classes:
    None explicitly defined in this module.

Dependencies:
    - Standard libraries: `logging`, `sys`, `collections`, `threading`, `os`, `re`, `configparser`.
    - Third-party libraries: `pandas`, `matplotlib`, `numpy`, `scipy`, `tqdm`.

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen and Lei Wang
    - License: BSD 3-clause
"""


import logging
import configparser
import sys
from collections import defaultdict
from threading import Thread
from types import SimpleNamespace

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial import distance
from tqdm import tqdm
from tkinter import messagebox

from .analysis_hkl import unit_cell_distance_procrustes
from .util import *
from .xds_analysis import extract_cluster_result, get_avg_esd_cell, extract_run_result
from .xds_shelx import convert_to_shelx

global cutoff_distance

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, '..', 'setting.ini'))

cell_cluster_distance = float(config['Cluster']['cell_cluster_distance'])
cell_cluster_symmetry = strtobool(config['Cluster']['cell_cluster_symmetry'])


def get_paths_by_indicator(file_path: str, indicator: str, comparison_operator: str, value: float) -> list:
    """Filters dataset paths based on a specified indicator and comparison operator.

    Args:
        file_path (str): Path to the Excel file containing dataset information.
        indicator (str): The column name in the Excel file to filter on.
        comparison_operator (str): Comparison operator to use ('>' or '<').
        value (float): The threshold value for filtering.

    Returns:
        list: List of dataset paths that meet the filtering criteria.

    Raises:
        ValueError: If the indicator column is not found or an invalid operator is specified.
    """
    # Read the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')

    # Check if the indicator column exists
    if indicator not in df.columns and indicator != "Reso.":
        raise ValueError(f"Indicator '{indicator}' not found in the Excel file.")
    elif indicator not in df.columns and indicator == "Reso." and "Pseudo Resolution" in df.columns:
        indicator = "Pseudo Resolution"

    # Filter based on the comparison operator
    if comparison_operator == '>':
        filtered_df = df[df[indicator] > value]
    elif comparison_operator == '<':
        filtered_df = df[df[indicator] < value]
    else:
        raise ValueError(f"Invalid comparison operator '{comparison_operator}'. Use '>' or '<'.")

    paths = filtered_df['Path'].tolist()

    return paths


def filter_data(directory_path: str, value: float, filter_type: str) -> None:
    """Filters datasets based on a specified filter type and value, then saves the filtered results.

    Args:
        directory_path (str): Path to the directory containing the data and Excel files.
        value (float): Threshold value for filtering.
        filter_type (str): Type of filter to apply ('cc12', 'isa', 'reso', 'rmeas').

    Effect:
        Saves the filtered dataset paths to `xdspicker.xlsx` within the specified directory.
    """
    if filter_type not in ['cc12', 'isa', 'reso', 'rmeas']:
        print("Invalid filter type specified. Use 'cc12', 'reso', 'rmeas' or 'isa'.")
        return

    print("********************************************")
    print("*                 XDS Picker               *")
    print("********************************************\n")

    excel_file_path = os.path.join(directory_path, 'xdsrunner2.xlsx')
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')

        # Determine the column name based on the filter type
        column_name = {"cc12": "CC1/2", "isa": "ISa" if "ISa" in df else "Isa", "reso": "Reso.", "rmeas": "Rmeas"}

        # Ensure the column exists and filter the DataFrame
        if filter_type in ['reso', 'rmeas']:
            df_filtered = df[pd.to_numeric(df[column_name[filter_type]], errors='coerce').lt(value)]
        elif column_name[filter_type] in df.columns:
            df_filtered = df[pd.to_numeric(df[column_name[filter_type]], errors='coerce').gt(value)]
        else:
            print(f"Column '{column_name}' not found in the Excel file.")
            return

        output_path = os.path.join(directory_path, 'xdspicker.xlsx')
        if df_filtered.empty:
            messagebox.showwarning("Warning", "No Entry Satisfied the Criteria")
            print("No data filtered")
            return
        else:
            df_filtered.to_excel(output_path, index=False)
            print(f"{filter_type.upper()} filtering completed and saved to {output_path}")

    except Exception as e:
        messagebox.showwarning("Warning", f"An error occurred: {e}")
        print(f"An error occurred: {e}")


def parse_xscale_lp(fn: str = "XSCALE.LP") -> SimpleNamespace:
    """Parses an XSCALE.LP file to extract filenames, unit cell parameters, space group, and correlation matrix.

    Args:
        fn (str): Path to the `XSCALE.LP` file. Defaults to `"XSCALE.LP"`.

    Returns:
        SimpleNamespace: Contains parsed data:
            - filenames (dict): Dataset filenames with corresponding indices.
            - correlation_matrix (np.ndarray): Correlation coefficients between datasets.
            - unit_cell (str): Unit cell parameters.
            - space_group (str): Space group number.
    """
    space_group, unit_cell = None, None
    filenames = {}
    correlations = []

    with open(fn, "r") as file:
        content = file.readlines()

    reading_filenames = False
    reading_correlations = False

    for line in content:
        line = line.strip()

        if line.startswith("SPACE_GROUP_NUMBER="):
            space_group = line.split('=')[1].strip()
        elif line.startswith("UNIT_CELL_CONSTANTS="):
            unit_cell = line.split('=')[1].strip()
        elif "READING INPUT REFLECTION DATA FILES" in line:
            reading_filenames = True
            reading_correlations = False  # Ensure we reset other states
        elif "CORRELATIONS BETWEEN INPUT DATA SETS AFTER CORRECTIONS" in line:
            reading_filenames = False
            reading_correlations = True  # Transition to reading correlations
            continue
        elif reading_filenames:
            if line.startswith("DATA"):
                continue
            elif re.match(r"^\d+", line):
                parts = line.split()
                filenames[int(parts[0])] = parts[-1]
            elif "OVERALL SCALING AND CRYSTAL DISORDER CORRECTION" in line:
                reading_filenames = False
        elif reading_correlations:
            if not line or "NUMBER OF COMMON" in line:
                continue
            elif "K*EXP(B*SS)" in line:
                reading_correlations = False
            elif re.match(r"^\d+\s+\d+", line):
                parts = line.split()
                correlations.append((int(parts[0]), int(parts[1]), float(parts[3])))
            continue

    # Building the correlation matrix
    max_index = max(max(i, j) for i, j, _ in correlations)
    corr_matrix = np.zeros((max_index, max_index))
    for i, j, value in correlations:
        corr_matrix[i - 1, j - 1] = value  # Adjust for 0-indexing
        corr_matrix[j - 1, i - 1] = value
    np.fill_diagonal(corr_matrix, 1.0)

    return SimpleNamespace(filenames=filenames, correlation_matrix=corr_matrix, unit_cell=unit_cell,
                           space_group=space_group)


def calculate_dendrogram(parsed_data: SimpleNamespace) -> np.ndarray:
    """Calculates a linkage matrix for hierarchical clustering.

    Args:
        parsed_data (SimpleNamespace): Parsed XSCALE.LP data containing the correlation matrix.

    Returns:
        np.ndarray: Linkage matrix for dendrogram computation.

    Raises:
        ValueError: If the correlation matrix is empty.
    """
    # Check if the correlation matrix is not empty and contains data
    if parsed_data.correlation_matrix.size == 0:
        raise ValueError("Correlation matrix is empty.")

    corr_mat = parsed_data.correlation_matrix
    # Convert correlation matrix to distance matrix for dendrogram calculation
    d_mat = np.sqrt(1 - corr_mat ** 2)
    # Condense the distance matrix since linkage function expects condensed form
    tri_upper = np.triu_indices_from(d_mat, k=1)
    condensed_dmat = d_mat[tri_upper]
    z = linkage(condensed_dmat, method="average")

    return z


def extract_dendrogram(input_path: str, interactive: bool = True, callback: callable = None) -> float:
    """Extracts and displays a dendrogram based on the input path.

    Args:
        input_path (str): Path to the directory containing XSCALE.LP.
        interactive (bool): Enables interactive dendrogram adjustment if True. Defaults to True.
        callback (callable, optional): Function to execute with the selected cutoff distance.

    Returns:
        float: The threshold distance at which the dendrogram is cut to form clusters (in interactive mode).
    """
    print(f"\nDendrogram has received input path: {input_path}")
    xscale_lp_path = os.path.join(input_path, "XSCALE.LP")
    if os.path.exists(xscale_lp_path):
        print(f"Found XSCALE.LP at: {xscale_lp_path}")
        ccs = parse_xscale_lp(xscale_lp_path)
        # Check if correlation coefficients were found
        if ccs is None:
            print("No correlation coefficients found in XSCALE.LP.\n")
            if callback:
                callback(None)
            return 0
        z = calculate_dendrogram(ccs)
        if interactive:
            plot_dendrogram(z, input_path, interactive, callback)
        else:
            plot_dendrogram(z, input_path, interactive, callback)
    else:
        print("XSCALE.LP not found in the input directory.\n")
        if callback:
            callback(None)  # Notify callback of failure
        return 0


def plot_dendrogram(z: np.ndarray, input_path: str, interactive: bool = True, callback: callable = None) -> None:
    """Generates and optionally displays an interactive dendrogram.

    Args:
        z (np.ndarray): Linkage matrix for hierarchical clustering.
        input_path (str): Directory path to save the dendrogram image.
        interactive (bool): Enables interactive dendrogram adjustment if True. Defaults to True.
        callback (callable, optional): Function to execute with the selected cutoff distance.
    """
    n = len(z) + 1
    initial_distance = round(0.7 * max(z[:, 2]), 4)

    fig = Figure(figsize=(7, 6))
    ax = fig.add_subplot(111)
    labels = np.array([str(i) for i in range(1, n + 1)])
    if interactive:
        dendrogram(z, color_threshold=initial_distance, ax=ax,
                   above_threshold_color="lightblue", labels=labels)
        ax.set_xlabel("Index")
        ax.set_ylabel("Distance")
        ax.set_title(f"Dendrogram ($t={initial_distance:.2f}$)")
        hline = ax.axhline(y=initial_distance, color='#004c99', label='Current Cut-off')
        latest_cutoff = [initial_distance]  # Mutable holder for latest cutoff

        def onclick(event):
            # Declare hline as nonlocal before using it
            nonlocal hline
            if event.ydata:
                new_distance = round(event.ydata, 4)
                latest_cutoff[0] = new_distance  # Update the latest cutoff
                ax.set_title(f"Dendrogram ($t={new_distance:.2f}$)")
                hline.remove()
                hline = ax.axhline(y=new_distance, color='#004c99')
                # Remove old dendrogram lines
                for c in ax.collections:
                    c.remove()
                dendrogram(z, color_threshold=new_distance, ax=ax,
                           above_threshold_color="lightblue", labels=labels)
                canvas.draw()

        fig.canvas.mpl_connect('button_press_event', onclick)

    if interactive:
        top = tk.Toplevel()
        top.title("Interactive Dendrogram")

        # Ensure the window is on top
        top.attributes('-topmost', True)

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        if interactive:
            def on_close():
                # Retrieve the latest cutoff distance
                cutoff_distance = latest_cutoff[0]
                filepath = os.path.join(input_path, "dendrogram.png")
                fig.savefig(filepath)
                plt.close(fig)
                top.destroy()
                if callback:
                    callback(cutoff_distance)

            top.protocol("WM_DELETE_WINDOW", on_close)
            top.grab_set()  # Make the window modal

            # No blocking call; the function returns immediately
        return None
    else:
        # Non-interactive: Generate and save the dendrogram without user interaction
        dendrogram(z, color_threshold=1, ax=ax,
                   above_threshold_color="lightblue", labels=labels)
        ax.set_xlabel("Index")
        ax.set_ylabel("Distance")
        ax.set_title(f"Dendrogram")
        filepath = os.path.join(input_path, "dendrogram.png")
        fig.savefig(filepath)
        plt.close(fig)
        print(f"Dendrogram saved to {filepath}")
        if callback:
            callback(None)  # No cutoff distance to return in non-interactive mode
        return None


def make_cluster(input_path: str, distance: float, cover: bool = True) -> None:
    """Forms clusters from XDS datasets based on a specified dendrogram distance and optionally merges them.

    Args:
        input_path (str): Directory containing the `xdspicker.xlsx` file and `XSCALE.LP`.
        distance (float): Distance threshold for defining clusters.
        cover (bool): If True, overwrites existing clusters. Defaults to True.

    Effect:
        Clusters data and merges results into new datasets within the specified directory.
    """
    print(f"Clusters will be made based on {distance}")
    # Read Excel
    xlsx_file_path = os.path.join(input_path, "xdspicker.xlsx")
    df = pd.read_excel(xlsx_file_path, engine="openpyxl")
    df = df.dropna(how='all').reset_index(drop=True)
    # Calculate Dendrogram
    xscale_lp_path = os.path.join(input_path, "merge", "XSCALE.LP")
    ccs = parse_xscale_lp(xscale_lp_path)
    z = calculate_dendrogram(ccs)
    clusters = fcluster(z, distance, criterion='distance')
    value_to_indices = defaultdict(list)
    # Populate the dictionary with indices
    for index, value in enumerate(clusters):
        value_to_indices[value].append(index)
    # Extract indices for values that are not unique
    result = [indices for indices in value_to_indices.values() if len(indices) > 1]

    if not result:
        print("The cut-off distance may be too small to form cluster.")
        return

    # Whether cover the previous result or not
    if cover:
        for item in os.listdir(os.path.join(input_path, "merge")):
            item_path = os.path.join(os.path.join(input_path, "merge"), item)
            # Check if the item is a directory, then remove it
            if os.path.isdir(item_path) and ("cls" in item_path or "cluster" in item_path):
                shutil.rmtree(item_path)
        start_num = 1
    else:
        pattern = re.compile(r'dis(\d+)')
        # Initialize a list to store all matched numbers
        numbers = []
        # Loop through the subfolders in the parent directory
        for item in os.listdir(os.path.join(input_path, "merge")):
            # Check if the item is a directory and matches the pattern
            if os.path.isdir(os.path.join(input_path, "merge", item)):
                match = pattern.match(item)
                if match:
                    numbers.append(int(match.group(1)))

        # Find the maximum number if any matches were found
        if numbers:
            start_num = max(numbers) + 1
        else:
            start_num = 1

    print("Cluster will based on below settings:")
    with open(os.path.join(input_path, "merge", "Cluster-info.txt"), "w" if cover else "a") as file:
        for i, indices in enumerate(result):
            print("Distance{} - Cluster {}: [{}]".format(start_num, i + 1, " ".join([str(index + 1) for index in indices])))
            file.write("Distance{} - Cluster {}: [{}]\n".format(
                start_num, i + 1, ", ".join([df["Path"][df.index[index]][2:]
                                          if df["Path"][df.index[index]].startswith(".")
                                          else df["Path"][df.index[index]]
                                          for index in indices])))

    # Start merging
    for i, indices in enumerate(result):
        merge(input_path, _filter=indices, folder="merge/dis{}-cls{}".format(start_num, i + 1), exclude_mode=False)
        convert_to_shelx(input_path, xconv_folder="merge/dis{}-cls{}".format(start_num, i + 1))


def merge(input_path: str,
          _filter: list = None,
          folder: str = "merge",
          exclude_mode: bool = True,
          reso: float = None,
          alert: bool = True) -> None:
    """Combines multiple datasets into a single dataset based on specified criteria.

    Args:
        alert (bool): Raise alert when volume deviate a lot.
        input_path (str): Directory containing the `xdspicker.xlsx` file.
        _filter (list, optional): List of dataset indices to include or exclude.
        folder (str): Subdirectory to store the merged dataset and new `XSCALE.INP` file. Defaults to `"merge"`.
        exclude_mode (bool): If True, excludes datasets specified in `_filter`. Defaults to True.
        reso (float, optional): Resolution limit for merging. Defaults to module resolution or 0.84 Å.

    Effect:
        Creates or updates an `XSCALE.INP` file in the specified directory and runs the XSCALE process.
    """
    print("********************************************")
    print("*                 XDS-Scale                *")
    print("********************************************\n")
    # Ensure input path is provided
    if _filter is None:
        _filter = []
    if not input_path:
        print("No input path provided.\n")
        return

    # Create the merge directory inside the input path
    merge_dir = os.path.join(input_path, folder)
    os.makedirs(merge_dir, exist_ok=True)

    # Path to the xdspicker.xlsx file
    xlsx_file_path = os.path.join(input_path, "xdspicker.xlsx")

    # Read the contents of the xlsx file
    try:
        df = pd.read_excel(xlsx_file_path, engine="openpyxl")
        df = df.dropna(how='all').reset_index(drop=True)
    except FileNotFoundError:
        print("The file specified does not exist.\n")
        return

    # Check if the DataFrame is empty or does not have enough rows
    if df.empty or len(df) < 2:
        print("The xdspicker is empty or does not have enough datasets. Please check your xdspicker.xlsx\n")
        return

    if reso is None:
        reso = max(min(df.get("Pseudo Resolution") if "Pseudo Resolution" in df else df.get("Reso.")), 0.84)

    vol_list = []
    path_folders = []
    for index, row in df.iterrows():
        if index in _filter and exclude_mode:
            continue
        elif index not in _filter and not exclude_mode:
            continue
        elif pd.isnull(row["Path"]) or ' ' in row["Path"]:
            continue

        if not pd.isnull(row["Path"]) and "..." in row["Path"]:
            xds_path = os.path.join(input_path, row["Path"][4:])
            path_folders.append(xds_path)
            try:
                vol_list.append(float(row["Vol."].split("(")[0]))
            except Exception:
                pass
        elif not pd.isnull(row["Path"]):
            xds_path = row["Path"]
            path_folders.append(xds_path)
            try:
                vol_list.append(float(row["Vol."].split("(")[0]))
            except Exception:
                pass

    if vol_list:
        # Initial mean and standard deviation
        mean_vol = np.mean(vol_list)
        std_vol = np.std(vol_list)
        max_sigma = 3

        # Filter data to remove initial outliers
        filtered_vol_list = [v for v in vol_list if abs(v - mean_vol) <= max_sigma * std_vol]

        # Recalculate mean and standard deviation after removing outliers
        mean_filtered = np.mean(filtered_vol_list)
        std_filtered = np.std(filtered_vol_list)

        # Identify outliers based on the refined mean and standard deviation
        outliers = [v for v in vol_list if abs(v - mean_filtered) > max_sigma * std_filtered]
        num_outliers = len(outliers)

        # Display a message box if there are outliers
        if num_outliers > 0 and alert:
            max_deviation_sigma = max([abs(v - mean_filtered) / std_filtered for v in outliers])
            message = (f"{num_outliers} of volumes deviate by more than {max_sigma} sigma. \n"
                       f"The mean volume is {mean_filtered:.1f} ± {std_filtered:.1f} "
                       f"({(mean_filtered - 3 * std_filtered):.1f} – {(mean_filtered + 3 * std_filtered):.1f})\n"
                       f"The maximum deviation is {max_deviation_sigma:.2f} sigma. "
                       "Do you wish to continue?")
            response = messagebox.askyesno("Outlier Warning", message)
            if not response:
                print("Process aborted by the user.")
                return
    avg_cell, esd_cell, wavelength = get_avg_esd_cell(None, multi=True, mode="list", folder_list=path_folders)
    ave_unitcell_str = " ".join(["{:.4f}".format(x) for x in avg_cell])

    # Create an XSCALE.inp file in the merge directory
    inp_file_path = os.path.join(merge_dir, "XSCALE.INP")
    with open(inp_file_path, "w") as inp_file:
        space_group_number = df["Space group"][0] if "Space group" in df else df["SG"][0]
        inp_file.write(f"SPACE_GROUP_NUMBER= {space_group_number}\n")
        inp_file.write(f"UNIT_CELL_CONSTANTS= {ave_unitcell_str}\n\n")
        inp_file.write("OUTPUT_FILE=all.HKL\n")
        inp_file.write("FRIEDEL'S_LAW=TRUE MERGE=FALSE\n")
        inp_file.write("STRICT_ABSORPTION_CORRECTION=FALSE\n")

        for index, row in df.iterrows():
            if index in _filter and exclude_mode:
                continue
            elif index not in _filter and not exclude_mode:
                continue
            elif pd.isnull(row["Path"]) or ' ' in row["Path"]:
                continue

            try:
                resolution = float(row.get("Pseudo Resolution") if "Pseudo Resolution" in row else row.get("Reso."))
            except ValueError:
                resolution = 0.8  # If not, skip
            if "..." in str(row["Path"]):
                acsii_hkl_path = os.path.join(input_path, row["Path"][4:], "XDS_ASCII.HKL")
            else:
                acsii_hkl_path = os.path.join(row["Path"], "XDS_ASCII.HKL")

            # Continues writing
            inp_file.write("\n")
            inp_file.write("!{}\n".format(row["No."]))
            inp_file.write(f"INPUT_FILE={acsii_hkl_path}\n")
            inp_file.write(f"INCLUDE_RESOLUTION_RANGE=200 {resolution}\n")
            inp_file.write("CORRECTIONS= DECAY MODULATION ABSORPTION\n")
            inp_file.write(f"CRYSTAL_NAME=a{index + 1}\n")

    print("XSCALE.INP created successfully!\n")

    def run_xscale(_merge_dir):
        # Run XSCALE in the merge directory
        subprocess.run(["xscale"], cwd=_merge_dir)
        print("\nAll data from xdspicker has been merged.\n")

    xscale_thread = Thread(target=run_xscale, args=(merge_dir,))
    xscale_thread.start()
    xscale_thread.join()

    extract_thread = Thread(target=extract_cluster_result, args=(merge_dir, "SU", True, reso, True))
    extract_thread.start()
    extract_thread.join()


def calculate_distance_matrix(matrices: list, distance_function: callable) -> np.ndarray:
    """Calculates the distance matrix for a set of matrices using a specified distance function.

    Args:
        matrices (list): List of matrices to calculate distances between.
        distance_function (callable): Function to compute the distance between two matrices.

    Returns:
        np.ndarray: Distance matrix as a NumPy array representing pairwise distances.
    """
    num_matrices = len(matrices)
    distances = np.zeros((num_matrices, num_matrices))

    for i in range(num_matrices):
        for j in range(i + 1, num_matrices):
            distance = distance_function(matrices[i], matrices[j])
            distances[i, j] = distances[j, i] = distance
    return distances


def calculate_stats(data: list) -> tuple:
    """Calculates the mean and standard error of the mean (SEM) for given data.

    Args:
        data (list): Data array to calculate statistics for.

    Returns:
        tuple: Contains the mean and SEM as lists of rounded values.
    """
    mean = np.round(np.mean(data, axis=0), 3).tolist()
    sem = np.round((np.std(data, axis=0) / np.sqrt(len(data))), 3).tolist()
    return mean, sem


def sort_cell_bravais_lattice(bravais_lattice: str, cell: list) -> list:
    """
    Sort the cell parameters based on the Bravais lattice type.

    Parameters:
        bravais_lattice (str): The type of Bravais lattice.
        cell (list or tuple): The cell parameters [a, b, c, ...].

    Returns:
        list: Sorted cell parameters.
    """
    if isinstance(cell, tuple):
        cell = list(cell)
    sorted_cell = cell.copy()
    if bravais_lattice in {"oP", "oI", "oF"}:
        sorted_cell[:3] = sorted(sorted_cell[:3])
    elif bravais_lattice == "oC":
        sorted_cell[:2] = sorted(sorted_cell[:2])
    return sorted_cell


def group_similar_entries(entries: list, tolerance: float = 0.05) -> list:
    """
    Group entries where the differences in a, b, c do not exceed the tolerance.

    Parameters:
        entries (list of dict): List of entries to group.
        tolerance (float): Maximum allowed difference in a, b, c.

    Returns:
        list of list: Grouped entries.
    """
    groups = []
    for entry in entries:
        a, b, c = entry['cell_bravais_lattice'][:3]
        placed = False
        for group in groups:
            ga, gb, gc = group[0]['cell_bravais_lattice'][:3]
            if (abs(a - ga)/ga <= tolerance and
                    abs(b - gb)/gb <= tolerance and
                    abs(c - gc)/gc <= tolerance):
                group.append(entry)
                placed = True
                break
        if not placed:
            groups.append([entry])
    return groups


def aggregate_by_bravais_lattice(cluster_data: dict) -> dict:
    """Aggregates unit cell information by Bravais lattice type.

    Args:
        cluster_data (dict): Cluster data containing unit cell and symmetry information.

    Returns:
        dict: Aggregated data categorized by Bravais lattice type, with mean and SEM of parameters.
    """
    bravais_lattice_groups = defaultdict(list)

    # Initial grouping by Bravais lattice with sorted cell parameters
    for path, cell_info in cluster_data.items():
        for bravais_lattice, entries in cell_info.items():
            for entry in entries:
                # Sort cell parameters based on Bravais lattice
                sorted_cell = sort_cell_bravais_lattice(bravais_lattice, entry['cell_bravais_lattice'])
                entry['cell_bravais_lattice'] = sorted_cell
                bravais_lattice_groups[bravais_lattice].append(entry)

    aggregated_data = {}

    for bravais_lattice, entries in bravais_lattice_groups.items():
        # For "mP" and "mC", perform secondary grouping
        if bravais_lattice in {"mP", "mC"}:
            grouped_entries = group_similar_entries(entries, tolerance=0.10)
            for idx, group in enumerate(grouped_entries, start=1):
                subgroup_name = f"{bravais_lattice} (setting {idx})"

                # Aggregate statistics for the subgroup
                cell_bravais_lattices = [entry['cell_bravais_lattice'] for entry in group]
                diffs = [entry['diff'] for entry in group]
                qof_values = [entry['qof'] for entry in group]

                mean_cell, stdev_cell = calculate_stats(cell_bravais_lattices)
                mean_diff = round(np.mean(diffs), 4)
                mean_qof = round(np.mean(qof_values), 1)

                sg_r_meas_ratios = defaultdict(list)
                sg_cc12 = defaultdict(list)
                for entry in group:
                    sg_r_meas_ratios[entry['sg_no']].append(entry['r_meas_ratio'])
                    sg_cc12[entry['sg_no']].append(entry['cc12_ratio'])

                mean_r_meas_ratios = {sg_no: round(np.mean(r_meas), 3)
                                      for sg_no, r_meas in sg_r_meas_ratios.items()}
                mean_cc12 = {sg_no: round(np.mean(cc12), 3)
                             for sg_no, cc12 in sg_cc12.items()}
                sg_counts = {sg_no: len(r_meas)
                             for sg_no, r_meas in sg_r_meas_ratios.items()}

                aggregated_data[subgroup_name] = {
                    'mean_cell_bravais_lattice': mean_cell,
                    'stdev_cell_bravais_lattice': stdev_cell,
                    'mean_diff': mean_diff,
                    'mean_qof': mean_qof,
                    'mean_r_meas_ratios': mean_r_meas_ratios,
                    'mean_cc12': mean_cc12,
                    'sg_counts': sg_counts
                }
        else:
            cell_bravais_lattices = [entry['cell_bravais_lattice'] for entry in entries]
            diffs = [entry['diff'] for entry in entries]
            qof_values = [entry['qof'] for entry in entries]

            mean_cell, stdev_cell = calculate_stats(cell_bravais_lattices)
            mean_diff = round(np.mean(diffs), 4)
            mean_qof = round(np.mean(qof_values), 1)

            sg_r_meas_ratios = defaultdict(list)
            sg_cc12 = defaultdict(list)
            for entry in entries:
                sg_r_meas_ratios[entry['sg_no']].append(entry['r_meas_ratio'])
                sg_cc12[entry['sg_no']].append(entry['cc12_ratio'])

            mean_r_meas_ratios = {sg_no: round(np.mean(r_meas), 3)
                                  for sg_no, r_meas in sg_r_meas_ratios.items()}
            mean_cc12 = {sg_no: round(np.mean(cc12), 3)
                         for sg_no, cc12 in sg_cc12.items()}
            sg_counts = {sg_no: len(r_meas)
                         for sg_no, r_meas in sg_r_meas_ratios.items()}

            aggregated_data[bravais_lattice] = {
                'mean_cell_bravais_lattice': mean_cell,
                'stdev_cell_bravais_lattice': stdev_cell,
                'mean_diff': mean_diff,
                'mean_qof': mean_qof,
                'mean_r_meas_ratios': mean_r_meas_ratios,
                'mean_cc12': mean_cc12,
                'sg_counts': sg_counts
            }
    return aggregated_data


def setup_logging(folder_path: str) -> None:
    """Sets up logging configuration for the module, directing logs to both a file and the console.

    Args:
        folder_path (str): Path to the folder where log files will be saved.

    Effect:
        Initializes logging to `lattice_cluster.txt` in the specified directory and configures console output.
    """
    log_file_path = os.path.join(folder_path, 'lattice_cluster.txt')

    with open(log_file_path, 'w') as file:
        file.write('\n')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter('%(message)s'))

    # Create a stream handler for stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(message)s'))

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def log_info(logger: logging.Logger, message: str) -> None:
    """Logs an informational message to both the console and the log file.

    Args:
        logger (logging.Logger): The logger instance to use.
        message (str): The message to log.

    Effect:
        Outputs the message to the configured logging handlers.
    """
    logger.info(message)


def log_file_only(folder_path: str, message: str) -> None:
    """Logs a message exclusively to the log file.

    Args:
        folder_path (str): Path to the folder containing the log file.
        message (str): The message to log.

    Effect:
        Appends the message to `lattice_cluster.txt` in the specified directory.
    """
    with open(os.path.join(folder_path, 'lattice_cluster.txt'), 'a') as file:
        file.write(message + '\n')


def log_header(logger: logging.Logger) -> None:
    """Logs the header information for the lattice symmetry analysis.

    Args:
        logger (logging.Logger): The logger instance to use.

    Effect:
        Outputs predefined header information to the log.
    """
    log_info(logger, "\n********************************************")
    log_info(logger, "*         Lattice Symmetry Explorer        *")
    log_info(logger, "********************************************\n")
    log_info(logger, (
        "A script using to estimate lattice symmetry based on reflection data statistics. \n"
        "The recommended lattice difference should be < 2.5, and the Figure of Merit (FOM) should be < 200.\n"
        "For a given Bravais lattice, multiple space groups may be available. The R_meas ratio of each space\n"
        "group to P1 will be provided following the space group name, with a recommended value of < 1.8\n\n"
        "                    R_meas ratio = R_meas(Space Group) / R_meas(P1)                          \n"
        "                CC1/2 ratio = [1 - CC1/2(Space Group)] / [1 - CC1/2(P1)]                     \n"))


def log_lattice_symmetry_info(logger: logging.Logger, aggregated_data: dict, sg_name_dict: dict) -> None:
    """Logs detailed lattice symmetry information based on aggregated data.

    Args:
        logger (logging.Logger): The logger instance to use.
        aggregated_data (dict): Aggregated data categorized by Bravais lattice types.
        sg_name_dict (dict): Dictionary mapping space group numbers to their names.

    Effect:
        Outputs structured lattice symmetry information to the log.
    """
    lattice_choice_info = "**  Lattice Choice:"
    log_info(logger, lattice_choice_info)

    for bravais_lattice, data in aggregated_data.items():
        lattice_info = (
            f"--  Bravais Lattice: {bravais_lattice}\n"
            f"    Averaged Cell: {tuple(data['mean_cell_bravais_lattice'])},"
            f" Lattice Difference: {data['mean_diff']}, FOM: {data['mean_qof']}\n"
            f"    SEM of Cell: {tuple(data['stdev_cell_bravais_lattice'])}"
        )
        log_info(logger, lattice_info)

        sg_stat = []
        for sg_no, r_meas in data['mean_r_meas_ratios'].items():
            sg_stat.append(f"{sg_name_dict[sg_no]} (No. {sg_no}) : {r_meas}(R), {data['mean_cc12'][sg_no]}(C)")
        if len(sg_stat) > 4:
            sg_stat[3] = "\n    Suggested Space Group: " + sg_stat[3]
        suggested_sg = f"    Suggested Space Group: {' / '.join(sg_stat)}\n"
        log_info(logger, suggested_sg)


def process_single_run(logger: logging.Logger, analysis_dict: dict, sg_name_dict: dict) -> None:
    """Processes and logs lattice symmetry information for a single dataset run.

    Args:
        logger (logging.Logger): The logger instance to use.
        analysis_dict (dict): Dictionary containing analysis results for the dataset.
        sg_name_dict (dict): Dictionary mapping space group numbers to their names.

    Effect:
        Logs detailed symmetry information for the single dataset.
    """
    cluster_info = f"\n*****************"
    data_path_info = "**  Data Path: 1 datasets, (100%) \n{}\n".format(
        '\n'.join(list(analysis_dict.keys()))
    )

    log_info(logger, cluster_info)
    log_info(logger, data_path_info)

    aggregated_data = aggregate_by_bravais_lattice(analysis_dict)
    log_lattice_symmetry_info(logger, aggregated_data, sg_name_dict)


def process_multiple_runs(logger: logging.Logger, analysis_dict: dict, sg_name_dict: dict, folder_path: str) -> None:
    """Processes and logs lattice symmetry information for multiple dataset runs.

    Args:
        logger (logging.Logger): The logger instance to use.
        analysis_dict (dict): Dictionary containing analysis results for all datasets.
        sg_name_dict (dict): Dictionary mapping space group numbers to their names.
        folder_path (str): Path to the folder where logs and results will be saved.

    Effect:
        Logs detailed symmetry information for each cluster of datasets.
    """
    unit_cell_matrices = [list(cell.values())[0][0]["cell_parameters"] for cell in analysis_dict.values()]
    Z = linkage(distance.squareform(calculate_distance_matrix(unit_cell_matrices, unit_cell_distance_procrustes)),
                method='average')
    labels = fcluster(Z, t=cell_cluster_distance, criterion='distance')

    # import matplotlib.pyplot as plt
    # from scipy.cluster.hierarchy import dendrogram
    #
    # # Plot the dendrogram
    # plt.figure(figsize=(10, 7))
    # dendrogram(Z, color_threshold=0.2)
    # plt.title('Dendrogram')
    # plt.xlabel('Sample')
    # plt.ylabel('Distance')
    # plt.show()

    clustered_dicts = {}
    for label, path in zip(labels, analysis_dict.keys()):
        if label not in clustered_dicts:
            clustered_dicts[label] = {}
        clustered_dicts[label][path] = analysis_dict[path]

    new_clusters = defaultdict(dict)
    if cell_cluster_symmetry:
        for cluster_id, cluster_data in clustered_dicts.items():
            sub_clusters = defaultdict(dict)
            for path, cell in cluster_data.items():
                bravais_lattice = list(cell.values())[0][0]['bravais_lattice']
                sub_clusters[bravais_lattice][path] = cell
            for sub_cluster_id, sub_cluster_data in sub_clusters.items():
                new_cluster_id = f"{cluster_id}-{sub_cluster_id}"
                new_clusters[new_cluster_id] = sub_cluster_data
        sorted_clusters = sorted(new_clusters.items(), key=lambda item: len(item[1]), reverse=True)
    else:
        sorted_clusters = sorted(clustered_dicts.items(), key=lambda item: len(item[1]), reverse=True)

    ranked_clusters = {f"Cluster-{rank + 1}": cluster_data for rank, (cluster_id, cluster_data) in
                       enumerate(sorted_clusters)}

    for cluster_id, cluster_data in ranked_clusters.items():
        cluster_info = f"\n******* {cluster_id}: *******"
        data_path_info = "**  Data Path: {} datasets, ({}%) \n{}\n".format(
            len(cluster_data), round(len(cluster_data) / len(analysis_dict) * 100, 1),
            '\n'.join(list(cluster_data.keys()))
        )

        # Log to console and file
        log_info(logger, cluster_info)
        log_info(logger, data_path_info)

        aggregated_data = aggregate_by_bravais_lattice(cluster_data)

        # Log lattice symmetry info to console
        log_lattice_symmetry_info(logger, aggregated_data, sg_name_dict)

        log_file_only(folder_path, "\n***********************************************")
        log_file_only(folder_path, "***********************************************")
        log_file_only(folder_path, "*       Information for Single Dataset        *\n")

        # Log individual dataset information to file only
        for path, sets in cluster_data.items():
            individual_info = f"\nDetailed Info for Dataset: {path}"
            log_file_only(folder_path, individual_info)
            aggregated_data = aggregate_by_bravais_lattice({path: sets})

            for bravais_lattice, data in aggregated_data.items():
                lattice_info = (
                    f"--  Bravais Lattice: {bravais_lattice}\n"
                    f"    Averaged Cell: {tuple(data['mean_cell_bravais_lattice'])},"
                    f" Lattice Difference: {data['mean_diff']}, FOM: {data['mean_qof']}\n"
                    f"    SEM of Cell: {tuple(data['stdev_cell_bravais_lattice'])}"
                )
                log_file_only(folder_path, lattice_info)

                sg_stat = []
                for sg_no, r_meas in data['mean_r_meas_ratios'].items():
                    sg_stat.append(
                        f"{sg_name_dict[sg_no]} (No. {sg_no}) : {r_meas}(R), {data['mean_cc12'][sg_no]}(C)")
                suggested_sg = f"    Suggested Space Group: {' / '.join(sg_stat)}\n"
                log_file_only(folder_path, suggested_sg)


def analysis_lattice_symmetry(folder_path: str, path_filter: bool = None) -> None:
    """Analyzes lattice symmetry for datasets within a specified folder, logging detailed results.

    Args:
        folder_path (str): Path to the folder containing datasets and `XDS_ASCII.HKL` files.
        path_filter (bool): Filter path starting with "!" or ".".

    Effect:
        Generates a comprehensive lattice symmetry analysis, logs the results, and saves them
        to `lattice_cluster.txt` within the folder.
    """
    setup_logging(folder_path)
    logger = logging.getLogger()

    sg_name_dict = {
        1: "P1", 3: "P121", 5: "C121", 16: "P222", 21: "C222", 22: "F222", 23: "I222", 75: "P4", 79: "I4", 89: "P422",
        97: "I422", 143: "P3", 146: "R3", 149: "P321", 150: "P312", 155: "R32", 168: "P6", 177: "P622", 195: "P23",
        196: "F23", 197: "I23", 207: "P432", 209: "F432", 211: "I432"
    }

    log_header(logger)

    dir_list = [os.path.dirname(path) for path in find_files(folder_path, "XDS_ASCII.HKL", path_filter=path_filter)]
    analysis_dict = {}
    for path in tqdm(dir_list, ascii=True, desc="Testing Lattice Symmetry"):
        try:
            temp_results = extract_run_result(path)
            if temp_results["lattice_choice"]:
                analysis_dict[path] = temp_results["lattice_choice"]
        except Exception as e:
            pass

    if len(analysis_dict) == 0:
        log_info(logger, "Either XDS are running under cell mode or Insufficient Runs.")
        return
    elif len(analysis_dict) == 1:
        process_single_run(logger, analysis_dict, sg_name_dict)
        return

    process_multiple_runs(logger, analysis_dict, sg_name_dict, folder_path)


if __name__ == "__main__":
    pass
