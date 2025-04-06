"""
XDS Refinement Module
=====================

This module provides a comprehensive suite of functions to refine XDS processing parameters and improve the quality
and accuracy of crystallographic data. The refinements include optimization of indexing parameters, scaling,
beam divergence, rotation axis, resolution range, and beam center coordinates.

Modules
-------
- Index Refinement
- Scale Refinement
- Beam Divergence and Mosaicity Correction
- Rotation Axis Adjustment
- Resolution Range Modification
- Beam Center Optimization

Classes:
    None

Functions:
    index_refine(xds_dir: str, threshold: float = 80) -> None
        Refines indexing parameters based on the specified threshold.

    scale_refine(xds_dir: str, outlier_scale_ratio: float = 2) -> None
        Removes scaling outliers based on the specified scale ratio.

    dev_moscaicity_refine(xds_dir: str) -> None
        Adds divergence and mosaicity corrections.

    change_resolution_range(xds_dir: str, resolution: str) -> None
        Modifies the resolution range in the XDS.INP file.

    change_axis(xds_dir: str, axis_angle: float) -> None
        Updates the rotation axis in the XDS.INP file.

    refine_axis(xds_dir: str) -> bool
        Refines the rotation axis by optimizing the omega angle.

    optimise_beam_centre(fp: str, ...) -> tuple
        Optimizes beam center coordinates using an intensity penalty approach.

    refine_beam_centre(path: str) -> None
        Refines beam center parameters and updates the XDS.INP file.

    refine_file(xds_path: str, parameter_dict: dict) -> bool
        Executes multiple refinement steps based on provided parameters.

    check_xds_progress(directory: str) -> str or None
        Checks the progress of XDS processing.

    read_error_message(lp_file: str) -> list
        Extracts error messages from an XDS log file.

    check_status(xds_list: list) -> dict
        Analyzes the status of XDS processing for multiple runs.

    refine_failed(base_directory: str, ...) -> dict
        Provides refinement strategies for failed XDS runs.

Dependencies:
    - configparser
    - os
    - shutil
    - subprocess
    - concurrent.futures
    - functools
    - numpy
    - scipy
    - numba

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen
    - License: BSD 3-clause
"""


import configparser
import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.spatial import cKDTree

from numba import njit, prange

from .util import outliers_iqr_dict, strtobool
from .xds_analysis import load_scale_list, analysis_idxref_lp, load_mosaicity_list, load_divergence_list, find_xds_files
from .xds_input import generate_exclude_data_ranges, load_XDS_excluded_range, replace_value, extract_keywords

script_dir = os.path.dirname(__file__)
# Read configuration settings
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(script_dir), 'setting.ini'))

set_max_worker = int(config["General"]["max_core"])

if not strtobool(config["General"]["multi-process"]):
    set_max_worker = 1


def index_refine(xds_dir: str, threshold: float = 80) -> None:
    """
    Refines the indexing parameters based on the specified threshold.

    Args:
        xds_dir (str): Directory containing the XDS files.
        threshold (float, optional): Threshold for the index ratio to trigger refinement. Defaults to 80.

    Returns:
        None
    """
    os.chdir(xds_dir)
    idxref_lp = os.path.join(xds_dir, "IDXREF.LP")
    xds_inp = os.path.join(xds_dir, "XDS.INP")
    if not os.path.isfile(idxref_lp):
        subprocess.call("xds_par")
    index_result = analysis_idxref_lp(idxref_lp)
    if index_result:
        index_number = index_result.get("index_number")
        if index_number is None:
            index_number = 0  # Default to 0 if None

        spot_number = index_result.get("spot_number")
        if spot_number is None:
            spot_number = 1  # Default to 1 if None
        initial_index_ratio = round(index_number / spot_number * 100, 1)
    else:
        initial_index_ratio = 0.0
    if initial_index_ratio > threshold:
        return

    index_dict = {}
    error_value = [0.05, 0.08, 0.10, 0.12, 0.14, 0.16]
    print("Testing suitable index error ...", end="", flush=True)
    for i, value in enumerate(error_value):
        progress_status = f"({i + 1}/{len(error_value)})"
        with open(xds_inp, "r+") as f:
            lines = f.readlines()
            lines = replace_value(lines, "JOB", ["IDXREF"], comment=False)
            lines = replace_value(lines, "INDEX_ERROR", [f"{value}"], comment=False)
            f.seek(0)
            f.writelines(lines)
            f.truncate()
        print(f"\rTesting suitable index error ... {progress_status}")
        subprocess.call("xds_par", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        index_result = analysis_idxref_lp(idxref_lp)
        if index_result:
            index_number = index_result.get("index_number")
            if index_number is None:
                index_number = 0  # Default to 0 if None
            spot_number = index_result.get("spot_number")
            if spot_number is None:
                spot_number = 1  # Default to 1 if None
            index_ratio = round(index_number / spot_number * 100, 1)
        else:
            index_ratio = 0.0
        index_dict[value] = index_ratio
    print("\rTesting best index error ... OK")
    with open(xds_inp, "r+") as f:
        lines = f.readlines()
        lines = replace_value(lines, "JOB", ["XYCORR INIT COLSPOT IDXREF",
                                             "DEFPIX INTEGRATE CORRECT", "CORRECT"], comment=True)
        lines = replace_value(lines, "INDEX_ERROR",
                              [f"{max(index_dict, key=index_dict.get)}"], comment=False)
        f.seek(0)
        f.writelines(lines)
        f.truncate()
        print(f"Correct index error ... {max(index_dict, key=index_dict.get)}/OK")


def scale_refine(xds_dir: str, outlier_scale_ratio: float = 2) -> None:
    """
    Refines scaling parameters by identifying and excluding outliers.

    Args:
        xds_dir (str): Directory containing the XDS files.
        outlier_scale_ratio (float, optional): Ratio used to identify scaling outliers. Defaults to 2.

    Returns:
        None
    """
    xds_path = os.path.join(xds_dir, "XDS.INP")
    integrate_path = os.path.join(xds_dir, "INTEGRATE.LP")
    correct_path = os.path.join(xds_dir, "CORRECT.LP")
    if not os.path.isfile(integrate_path) or not os.path.isfile(correct_path):
        return
    with open(integrate_path, "r") as f:
        lines = f.readlines()
        init_scales = load_scale_list(lines)
    with open(xds_path, "r") as f:
        first_occurrence = None
        xds_lines = f.readlines()
        output_lines = []
        for j, line in enumerate(xds_lines):
            if "EXCLUDE_DATA_RANGE=" in line:
                if first_occurrence is None:
                    first_occurrence = j
            else:
                output_lines.append(line)
    filter_list = outliers_iqr_dict(init_scales, outlier_scale_ratio)
    exclude_list = load_XDS_excluded_range(xds_lines)
    exclude_list = sorted(list(set(exclude_list + filter_list)))
    add_lines = generate_exclude_data_ranges(exclude_list)
    if first_occurrence is not None:
        for new_line in reversed(add_lines):  # Reverse to maintain order after insert
            output_lines.insert(first_occurrence, new_line)
    else:
        output_lines = output_lines + add_lines
    with open(xds_path, 'w') as file:
        file.writelines(output_lines)


def dev_moscaicity_refine(xds_dir: str) -> None:
    """
    Refines divergence and mosaicity parameters based on previous runs.

    Args:
        xds_dir (str): Directory containing the XDS files.

    Returns:
        None
    """
    xds_path = os.path.join(xds_dir, "XDS.INP")
    integrate_path = os.path.join(xds_dir, "INTEGRATE.LP")
    with open(integrate_path, "r") as f:
        lines = f.readlines()
        mosaicity_list = list(load_mosaicity_list(lines).values())
        divergence_list = list(load_divergence_list(lines).values())
    divergence = np.average([item for item in divergence_list if item])
    mosaicity = np.average([item for item in mosaicity_list if item])
    with open(xds_path, 'r+') as file:
        lines = file.readlines()
        lines = replace_value(lines, "BEAM_DIVERGENCE_E.S.D.", [f"{divergence:.3f}"], comment=False)
        lines = replace_value(lines, "REFLECTING_RANGE_E.S.D.", [f"{mosaicity:.3f}"], comment=False)
        file.seek(0)
        file.writelines(lines)
        file.truncate()


def change_resolution_range(xds_dir: str, resolution: str) -> None:
    """
    Changes the resolution range in the XDS.INP file.

    Args:
        xds_dir (str): Directory containing the XDS files.
        resolution (str): New resolution range to set, e.g., "30 1.5".

    Returns:
        None
    """
    xds_path = os.path.join(xds_dir, "XDS.INP")
    with open(xds_path, "r+") as f:
        lines = f.readlines()
        lines = replace_value(lines, "INCLUDE_RESOLUTION_RANGE", [resolution], comment=False)
        f.seek(0)
        f.writelines(lines)
        f.truncate()


def change_axis(xds_dir: str, axis_angle: float) -> None:
    """
    Updates the rotation axis based on the specified angle.

    Args:
        xds_dir (str): Directory containing the XDS files.
        axis_angle (float): Rotation axis angle in degrees.

    Returns:
        None
    """
    xds_path = os.path.join(xds_dir, "XDS.INP")
    with open(xds_path, "r+") as f:
        lines = f.readlines()
        lines = replace_value(
            lines,
            "ROTATION_AXIS",
            [
                "{:.4f} {:.4f} 0".format(
                    np.cos(np.radians(axis_angle)), np.sin(np.radians(axis_angle))
                )
            ],
            comment=False,
        )
        f.seek(0)
        f.writelines(lines)
        f.truncate()


def make_2d_rotmat(theta: float) -> np.ndarray:
    """
    Creates a 2D rotation matrix for a given angle.

    Args:
        theta (float): Angle in radians.

    Returns:
        np.ndarray: A 2x2 rotation matrix.
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],
                     [s, c]])


@njit(fastmath=True)
def xyz2cyl_single(sx: float, sy: float, sz: float) -> tuple:
    """
    Converts a single Cartesian vector to cylindrical coordinates.

    Args:
        sx (float): X-coordinate of the vector.
        sy (float): Y-coordinate of the vector.
        sz (float): Z-coordinate of the vector.

    Returns:
        tuple: Cylindrical coordinates as:
            - phi (float): Azimuthal angle in radians.
            - theta (float): Polar angle in radians.
    """
    rho = np.hypot(sx, sy)
    phi = np.arctan2(sy, sx)
    theta = np.arctan2(sz, rho)
    return phi, theta


@njit(parallel=True, fastmath=True)
def cylinder_histo_numba(
        xyz: np.ndarray, bin_edges_phi: np.ndarray,
        bin_edges_theta: np.ndarray, H: np.ndarray) -> None:
    """
    Populates a 2D histogram with cylindrical projections using Numba for parallel performance.

    Args:
        xyz (np.ndarray): Array of Cartesian coordinates.
        bin_edges_phi (np.ndarray): Bin edges for the phi dimension.
        bin_edges_theta (np.ndarray): Bin edges for the theta dimension.
        H (np.ndarray): 2D histogram array to populate.

    Returns:
        None: Modifies the histogram array in place.
    """
    N = len(xyz)
    bins_phi = len(bin_edges_phi) - 1
    bins_theta = len(bin_edges_theta) - 1
    min_phi = bin_edges_phi[0]
    min_theta = bin_edges_theta[0]
    bin_width_phi = bin_edges_phi[1] - bin_edges_phi[0]
    bin_width_theta = bin_edges_theta[1] - bin_edges_theta[0]

    for idx in prange(N * (N - 1) // 2):
        # Map the flat index back to the triangular indices
        i = int(N - 2 - int(np.sqrt(-8*idx + 4*N*(N-1)-7)/2.0 - 0.5))
        j = idx + i + 1 - N*(N-1)//2 + (N - i)*((N - i) - 1)//2

        xi, yi, zi = xyz[i]
        xj, yj, zj = xyz[j]
        sx = xi - xj
        sy = yi - yj
        sz = zi - zj

        phi, theta = xyz2cyl_single(sx, sy, sz)

        # Compute bin indices
        bin_phi = int((phi - min_phi) / bin_width_phi)
        bin_theta = int((theta - min_theta) / bin_width_theta)

        # Check boundaries
        if 0 <= bin_phi < bins_phi and 0 <= bin_theta < bins_theta:
            H[bin_phi, bin_theta] += 1


def cylinder_histo(xyz: np.ndarray, bins: tuple = (1000, 500)) -> np.ndarray:
    """
    Creates a 2D histogram of cylindrical projections.

    Args:
        xyz (np.ndarray): Array of Cartesian coordinates.
        bins (tuple, optional): Number of bins for phi and theta dimensions. Defaults to (1000, 500).

    Returns:
        np.ndarray: A 2D histogram of the cylindrical projection.
    """
    bin_edges_phi = np.linspace(-np.pi, np.pi, bins[0] + 1)
    bin_edges_theta = np.linspace(-np.pi / 2, np.pi / 2, bins[1] + 1)
    H = np.zeros((bins[0], bins[1]), dtype=np.int64)

    cylinder_histo_numba(xyz, bin_edges_phi, bin_edges_theta, H)
    return H


def make(arr: np.ndarray, omega: float, wavelength: float) -> np.ndarray:
    """
    Prepares reciprocal space coordinates from reflection positions and omega angles.

    Args:
        arr (np.ndarray): Array of reflection positions and angles, where:
            - `arr[:, 0]` contains x-coordinates.
            - `arr[:, 1]` contains y-coordinates.
            - `arr[:, 2]` contains reflection angles in degrees.
        omega (float): Rotation angle of the crystal in degrees.
        wavelength (float): Wavelength of the X-ray in Å.

    Returns:
        np.ndarray: Array of reciprocal space coordinates as:
            - x, y, and z values for each reflection point in 3D space.
    """
    reflections = arr[:, :2]
    angle = arr[:, 2]

    omega_rad = np.radians(omega)
    r = make_2d_rotmat(omega_rad)
    refs_ = np.dot(reflections, r)
    y, x = refs_.T

    R = 1 / wavelength
    sqrt_arg = R ** 2 - x ** 2 - y ** 2
    sqrt_arg = np.clip(sqrt_arg, 0, None)  # Ensure non-negative values
    sqrt_sqrt_arg = np.sqrt(sqrt_arg)
    C = (R - sqrt_sqrt_arg).reshape(-1, 1)
    sin_angle = np.sin(angle)
    cos_angle = np.cos(angle)

    xyz = np.column_stack(
        (
            x * cos_angle,
            y,
            -x * sin_angle,
        )
    ) + C * np.column_stack((-sin_angle, np.zeros_like(angle), -cos_angle))

    return xyz


def evaluate_omega(omega: float, arr: np.ndarray, wavelength: float, hist_bins: tuple) -> tuple:
    """
    Evaluates the variance of the cylindrical histogram for a given omega angle.

    Args:
        omega (float): Rotation angle in degrees.
        arr (np.ndarray): Array of reflection positions and angles.
        wavelength (float): X-ray wavelength.
        hist_bins (tuple): Number of bins for the histogram (phi_bins, theta_bins).

    Returns:
        tuple: Variance of the histogram and the corresponding omega value.
    """
    xyz = make(arr, omega, wavelength)
    H = cylinder_histo(xyz, bins=hist_bins)
    var = np.var(H, ddof=1)
    return var, omega


def find_optimised_axis(arr: np.ndarray, omega_start: float, wavelength: float,
                        plusminus: float, step: float, hist_bins: tuple = (1000, 500)) -> float:
    """
    Optimizes the omega angle around a given starting point.

    Args:
        arr (np.ndarray): Array of reflection positions and angles.
        omega_start (float): Starting omega angle in degrees.
        wavelength (float): X-ray wavelength.
        plusminus (float): Range around omega_start for optimization (± degrees).
        step (float): Step size for the optimization in degrees.
        hist_bins (tuple, optional): Number of bins for the histogram (phi_bins, theta_bins). Defaults to (1000, 500).

    Returns:
        float: Optimized omega value in degrees.
    """
    r = np.arange(omega_start - plusminus, omega_start + plusminus + step, step)
    best_score, best_omega = 0, omega_start

    with ProcessPoolExecutor(max_workers=set_max_worker) as executor:
        futures = [executor.submit(evaluate_omega, omega, arr, wavelength, hist_bins) for omega in r]
        for future in futures:
            var, omega = future.result()
            if var > best_score:
                best_score, best_omega = var, omega

    return best_omega


def parse_xds_inp(fn: str) -> tuple:
    """
    Parses the XDS.INP file to extract key parameters.

    Args:
        fn (str): Path to the XDS.INP file.

    Returns:
        tuple: A tuple containing:
            - beam_center (tuple): (ORGX, ORGY) coordinates.
            - osc_angle (float): Oscillation angle in degrees.
            - pixelsize (float): Pixel size in mm.
            - wavelength (float): X-ray wavelength in Å.
            - omega_current (float): Current omega angle in degrees.
    """
    with open(fn, "r") as f:
        params = extract_keywords(f.readlines())

    rotx, roty, rotz = map(float, params["ROTATION_AXIS"][0].split()[:3])
    omega_current = np.degrees(np.arctan2(roty, rotx))
    pixelsize = float(params["QX"][0]) / (float(params["DETECTOR_DISTANCE"][0]) * float(params["X-RAY_WAVELENGTH"][0]))

    return (
        (float(params["ORGX"][0]), float(params["ORGY"][0])),
        float(params["OSCILLATION_RANGE"][0]),
        pixelsize,
        float(params["X-RAY_WAVELENGTH"][0]),
        omega_current,
    )


def load_spot_xds(fn: str, beam_center: tuple, osc_angle: float, pixelsize: float) -> np.ndarray:
    """
    Loads the SPOT.XDS file and converts data into reciprocal coordinates.

    Args:
        fn (str): Path to the SPOT.XDS file.
        beam_center (tuple): Beam center coordinates (ORGX, ORGY).
        osc_angle (float): Oscillation angle in degrees.
        pixelsize (float): Pixel size in mm.

    Returns:
        np.ndarray: Array of reciprocal coordinates (x, y, angle). Returns None if no data is loaded.
    """
    arr = np.loadtxt(fn)
    if arr.size == 0:
        return None
    reflections = arr[:, :2] - beam_center
    angle = arr[:, 2] * np.radians(osc_angle)
    reflections *= pixelsize
    return np.column_stack((reflections, angle))


def refine_axis(xds_dir: str) -> bool:
    """
    Refines the rotation axis by optimizing the omega angle.

    Args:
        xds_dir (str): Directory containing the XDS files.

    Returns:
        bool: True if refinement was successful, False otherwise.
    """
    xds_inp = os.path.join(xds_dir, "XDS.INP")
    spot_xds = os.path.join(xds_dir, "SPOT.XDS")

    beam_center, osc_angle, pixelsize, wavelength, omega_current = parse_xds_inp(xds_inp)
    if omega_current > 180:
        omega_current -= 360

    arr = load_spot_xds(spot_xds, beam_center, osc_angle, pixelsize)
    if arr is None:
        return False
    hist_bins = (1000, 500)

    omega_start = omega_current
    omega_local = find_optimised_axis(arr, omega_start, wavelength, plusminus=10, step=1, hist_bins=hist_bins)
    print(f"Best omega (local search): {-omega_local:.3f}")
    omega_fine = find_optimised_axis(arr, omega_local, wavelength, plusminus=1, step=0.1, hist_bins=hist_bins)
    print(f"Best omega (fine search): {-omega_fine:.3f}")
    print(f"Rotation axis found: {-omega_fine:.2f} deg. / {np.radians(-omega_fine):.3f} rad.")
    if np.abs(omega_fine - omega_current) < 10:
        change_axis(xds_dir, omega_fine)
    print("Correct rotation axis ... OK")
    return True


def calculate_pairs_with_intensity_penalty(center: tuple, data_xy: np.ndarray, data_intensity: np.ndarray,
                                           tree: cKDTree, tolerance: float,
                                           intensity_penalty_factor: float = 0.25,
                                           min_distance_sq: float = 225.0) -> tuple:
    """
    Calculates pairs of points with intensity penalties based on a specified center.

    Args:
        center (tuple): Center coordinates (x, y).
        data_xy (np.ndarray): Array of data points' (x, y) coordinates.
        data_intensity (np.ndarray): Array of data points' intensities.
        tree (cKDTree): KDTree for efficient nearest-neighbor searches.
        tolerance (float): Tolerance distance for pairing.
        intensity_penalty_factor (float, optional): Penalty factor for unmatched intensities. Defaults to 0.25.
        min_distance_sq (float, optional): Minimum squared distance to consider valid pairs. Defaults to 225.0.

    Returns:
        tuple:
            - pairs_found (np.ndarray): Boolean array indicating which pairs were found.
            - score (float): Overall penalty score.
    """
    center_x, center_y = center
    reflected_points = 2 * np.array([center_x, center_y]) - data_xy  # Shape: (N, 2)

    # Calculate squared distances from the center
    delta = data_xy - center
    distances_sq = np.einsum('ij,ij->i', delta, delta)

    # Exclude points within a 15-pixel radius (15^2 = 225)
    valid_mask = distances_sq > min_distance_sq

    # Query the KDTree for nearest neighbors within tolerance
    valid_reflected = reflected_points[valid_mask]
    if valid_reflected.size == 0:
        # No valid points to process
        return np.array([], dtype=bool), 0.0

    distances, indices = tree.query(valid_reflected, distance_upper_bound=tolerance)

    # Determine which points have a valid pair
    pairs_found = distances < tolerance

    # Calculate penalty for unmatched pairs
    unmatched_intensities = data_intensity[valid_mask][~pairs_found]
    penalty = unmatched_intensities.sum() * intensity_penalty_factor

    # Calculate the score
    score = -pairs_found.sum() + penalty

    return pairs_found, score


def objective_pairs_with_intensity_penalty(center: tuple, data_xy: np.ndarray, data_intensity: np.ndarray,
                                           tree: cKDTree, tolerance: float,
                                           intensity_penalty_factor: float) -> float:
    """
    Objective function for optimizing pairs with intensity penalties.

    Args:
        center (tuple): Center coordinates (x, y).
        data_xy (np.ndarray): Array of data points' (x, y) coordinates.
        data_intensity (np.ndarray): Array of data points' intensities.
        tree (cKDTree): KDTree for efficient nearest-neighbor searches.
        tolerance (float): Tolerance distance for pairing.
        intensity_penalty_factor (float): Penalty factor applied to unmatched intensities.

    Returns:
        float: Penalty score, where a lower score indicates better optimization.
    """
    _, score = calculate_pairs_with_intensity_penalty(center, data_xy, data_intensity, tree, tolerance,
                                                      intensity_penalty_factor)
    return score


def objective_func_fixed(c: tuple, data_xy: np.ndarray, data_intensity: np.ndarray,
                         tree: cKDTree, tolerance: float, intensity_penalty_factor: float) -> float:
    """
    Fixed objective function for optimizing beam center positions.

    Args:
        c (tuple): Current center coordinates (x, y).
        data_xy (np.ndarray): Array of data points' (x, y) coordinates.
        data_intensity (np.ndarray): Array of data points' intensities.
        tree (cKDTree): KDTree for efficient nearest-neighbor searches.
        tolerance (float): Tolerance distance for pairing.
        intensity_penalty_factor (float): Penalty factor applied to unmatched intensities.

    Returns:
        float: Penalty score, where a lower score indicates better optimization.
    """
    return objective_pairs_with_intensity_penalty(c, data_xy, data_intensity, tree, tolerance, intensity_penalty_factor)


def optimise_beam_centre(fp: str,
                         length1: int = 1024,
                         length2: int = 1024,
                         tol_ratio: float = 0.003,
                         intensity_penalty_factor: float = 0.25) -> tuple:
    """
    Optimizes the beam center using intensity penalties and nearest neighbor searches.

    Args:
        fp (str): Path to the SPOT.XDS file.
        length1 (int, optional): Length of the image along axis 1. Defaults to 1024.
        length2 (int, optional): Length of the image along axis 2. Defaults to 1024.
        tol_ratio (float, optional): Tolerance ratio for pairing. Defaults to 0.003.
        intensity_penalty_factor (float, optional): Penalty factor for unmatched intensities. Defaults to 0.25.

    Returns:
        tuple: Optimized beam center coordinates (ORGX, ORGY).
    """
    tolerance = max(tol_ratio * max(length1, length2), 3)
    dtype = np.float32
    try:
        data = np.loadtxt(fp, usecols=(0, 1, 3), dtype=dtype)  # X, Y, Intensity
    except Exception as e:
        print(f"Error loading data from {fp}: {e}")
        return None

    data_xy = data[:, :2]
    data_intensity = data[:, 2]

    # Normalize the intensity to a maximum of 100
    max_intensity = data_intensity.max()
    if max_intensity == 0:
        print("Maximum intensity is zero. Cannot normalize intensities.")
        return None
    data_intensity = (data_intensity / max_intensity) * 100.0

    # Define bounds for optimization
    bounds = [(0.45 * length1, 0.55 * length1), (0.45 * length2, 0.55 * length2)]

    # Create a KDTree for efficient nearest neighbor search
    tree = cKDTree(data_xy)

    # Create a partial function with fixed parameters
    objective_func = partial(objective_func_fixed,
                             data_xy=data_xy,
                             data_intensity=data_intensity,
                             tree=tree,
                             tolerance=tolerance,
                             intensity_penalty_factor=intensity_penalty_factor)

    # Perform the global optimization using differential evolution
    result_de = differential_evolution(
        objective_func,
        bounds,
        strategy='best1bin',
        popsize=25,  # Reduced population size for speed; adjust as needed
        tol=0.01,
        workers=-1,  # Utilize all available CPU cores
        updating='deferred',  # Better memory management
        disp=False
    )
    initial_centre = result_de.x

    # Perform the local optimization using the result of the global optimization
    result_local = minimize(
        objective_func,
        initial_centre,
        method='L-BFGS-B',  # More memory-efficient than 'BFGS'
        options={'ftol': 1e-6, 'disp': False}
    )

    best_centre = result_local.x
    best_score = result_local.fun

    # Define a distance function using NumPy for efficiency
    def distance(vec1, vec2):
        return np.linalg.norm(vec1 - vec2) if not (np.array_equal(vec2, [512, 512]) or
                                                   np.array_equal(vec2, [1024, 1024])) else 0.0

    # If the score is larger than 0, perform another round of optimization with increased penalty
    if best_score > 0 or distance(best_centre, initial_centre) > 0.02 * length1:
        print("Score is larger than 0 or center moved significantly, performing refinement.")
        intensity_penalty_factor += 0.1  # Increase penalty factor

        # Create a new partial function with updated penalty factor
        objective_func_refined = partial(objective_func_fixed,
                                         data_xy=data_xy,
                                         data_intensity=data_intensity,
                                         tree=tree,
                                         tolerance=tolerance,
                                         intensity_penalty_factor=intensity_penalty_factor)

        # Perform refined global optimization
        result_de_refined = differential_evolution(
            objective_func_refined,
            bounds,
            strategy='best1bin',
            popsize=15,  # Further reduced for speed
            tol=0.01,
            workers=-1,
            updating='deferred',
            disp=False
        )
        refined_centre = result_de_refined.x

        # Perform refined local optimization
        result_local_refined = minimize(
            objective_func_refined,
            refined_centre,
            method='L-BFGS-B',
            options={'ftol': 1e-6, 'disp': False}
        )

        # Update best_centre if the refined score is better
        if result_local_refined.fun < best_score:
            best_centre = result_local_refined.x
            best_score = result_local_refined.fun

    print("Best Centre:", best_centre)
    print("Best Score:", best_score)

    # Optionally plot the results (commented out for speed; enable if needed)
    pairs_found, _ = calculate_pairs_with_intensity_penalty(
        best_centre, data_xy, data_intensity, tree, tolerance, intensity_penalty_factor)
    print("Pairs Found:", np.sum(pairs_found), f"/ {len(data_xy)}\n")

    return best_centre


def refine_beam_centre(path: str) -> None:
    """
    Refines the beam center by optimizing the ORGX and ORGY parameters.

    Args:
        path (str): Path to the directory containing XDS files.

    Returns:
        None
    """
    inp_path = os.path.join(path, "XDS.INP")
    spot_path = os.path.join(path, "SPOT.XDS")
    if not os.path.exists(inp_path):
        print("You should write the XDS.INP file first.")
        return
    elif not os.path.exists(spot_path):
        print("You should run XDS first.")
        return
    else:
        # Extract parameters from XDS.INP
        with open(inp_path, "r") as f:
            lines = f.readlines()
        input_parameter_dict = extract_keywords(lines)

        # Optimize beam center
        centre = optimise_beam_centre(
            spot_path,
            length1=int(input_parameter_dict.get("NX", [1024])[0]),
            length2=int(input_parameter_dict.get("NY", [1024])[0]),
        )
        if centre is None:
            print("Beam center optimization failed.")
            return

    # Update XDS.INP with the new center
    with open(inp_path, "r") as f:
        lines = f.readlines()

    new_orgx = f"{centre[0]:.3f}"
    new_orgy = f"{centre[1]:.3f}"
    lines = replace_value(lines, "ORGX", [new_orgx], comment=False)
    lines = replace_value(lines, "ORGY", [new_orgy], comment=False)

    with open(inp_path, "w") as f:
        f.writelines(lines)

    print(f"Updated beam center to ORGX={new_orgx}, ORGY={new_orgy} in {inp_path}")


def refine_file(xds_path: str, parameter_dict: dict) -> bool:
    """
    Executes the refinement process based on specified parameters.

    Args:
        xds_path (str): Path to the XDS.INP file.
        parameter_dict (dict): Parameters for refinement steps. Includes:
            - "divergence" (bool): Refine divergence.
            - "scale" (float): Scale outlier ratio.
            - "axis" (bool): Refine rotation axis.
            - "index" (float): Index refinement threshold.
            - "beam_centre" (bool): Refine beam center.
            - "resolution" (str): Resolution range.

    Returns:
        bool: True if refinement was successful, False otherwise.
    """
    print(f"\nEntering XDS path {xds_path}")
    xds_dir = os.path.dirname(xds_path)

    if not os.path.exists(os.path.join(xds_dir, "BACKUP-CELL")):
        shutil.copy(os.path.join(xds_dir, "XDS.INP"), os.path.join(xds_dir, "BACKUP-CELL"))
    else:
        shutil.copy(os.path.join(xds_dir, "XDS.INP"), os.path.join(xds_dir, "BACKUP-REFINE"))

    if ((parameter_dict["divergence"]) and
            (not os.path.exists(os.path.join(xds_dir, "INTEGRATE.LP")) or not os.path.exists(
                os.path.join(xds_dir, "IDXREF.LP")))):
        print(f"{xds_dir} need to be run at first.")
        return False

    if ((parameter_dict["scale"]) and
            (not os.path.exists(os.path.join(xds_dir, "CORRECT.LP")) or not os.path.exists(
                os.path.join(xds_dir, "IDXREF.LP")))):
        print(f"{xds_dir} need to be run at first.")
        return False

    try:
        if parameter_dict["axis"]:
            print("Correct Rotation Axis with refined result ...")
            result = refine_axis(xds_dir)
            if result:
                print("\rCorrect Rotation Axis with refined result ... OK")
            else:
                print("\rCorrect Rotation Axis with refined result ... Failed")

        if parameter_dict["divergence"]:
            print("Add Divergence from Previous Run ... ... ", end="", flush=True)
            dev_moscaicity_refine(xds_dir)
            print("\rAdd Divergence from Previous Run ... ... OK")

        if parameter_dict["scale"]:
            print("Remove Scale Outliers from Previous Run ...", end="", flush=True)
            scale_refine(xds_dir, parameter_dict["scale"])
            print("\rRemove Scale Outliers from Previous Run ... OK")

        if parameter_dict["index"]:
            index_refine(xds_dir, parameter_dict["index"])

        if parameter_dict["beam_centre"]:
            refine_beam_centre(xds_dir)
            print("Finding Beam Centre ... ... ... OK")

        if parameter_dict["resolution"]:
            print("Change resolution to {} ... ... ... ".format(parameter_dict["resolution"]), end="", flush=True)
            change_resolution_range(xds_dir, parameter_dict["resolution"])
            print("\rChange resolution to {} ... ... ... OK".format(parameter_dict["resolution"]))

    except Exception as e:
        print(f"Refine error because of {e}")
        return False

    return True


def check_xds_progress(directory: str) -> str or None:
    """
    Checks the progress of XDS processing by identifying the most recent log file.

    Args:
        directory (str): Directory containing the XDS files.

    Returns:
        str or None: Path of the last generated LP file, or None if processing is complete.
    """

    # Define the sequence of LP files and the final output file
    lp_files = [
        "INIT.LP", "COLSPOT.LP", "IDXREF.LP",
        "DEXREF.LP", "INTEGRATE.LP", "CORRECT.LP"
    ]
    final_file = "XDS_ASCII.HKL"

    # Check if the final output file exists
    final_path = os.path.join(directory, final_file)
    if os.path.exists(final_path):
        return None

    # Track the most recent LP file in the sequence
    last_lp_file = None
    latest_time = None

    # Iterate over the LP files to find the most recent one
    for lp_file in lp_files:
        lp_path = os.path.join(directory, lp_file)
        if os.path.exists(lp_path):
            lp_time = os.path.getmtime(lp_path)
            if last_lp_file is None or lp_time > latest_time:
                last_lp_file = lp_path
                latest_time = lp_time

    # Return the path of the last generated LP file if XDS_ASCII.HKL is not present
    return last_lp_file


def read_error_message(lp_file: str) -> list:
    """
    Extracts error messages from a given LP file.

    Args:
        lp_file (str): Path to the LP file.

    Returns:
        list: List of error messages found in the LP file.
    """
    error_messages = []
    if lp_file and os.path.exists(lp_file):
        with open(lp_file, 'r') as file:
            for line in file:
                if "!!! ERROR" in line and "CANNOT READ IMAGE" not in line:
                    error_messages.append(line.strip())
    return error_messages


def check_status(xds_list: list) -> dict:
    """
    Checks the status of multiple XDS runs and collects error messages.

    Args:
        xds_list (list): List of paths to XDS.INP files.

    Returns:
        dict: A dictionary mapping file paths to their error messages and stop files.
    """
    error_dict = {}
    for xds_file in xds_list:
        root = os.path.dirname(xds_file)
        last_lp_file = check_xds_progress(root)
        if last_lp_file is None:
            pass
        else:
            error_messages = read_error_message(last_lp_file)
            if error_messages:
                error_dict[xds_file] = {
                    "stop_file": os.path.basename(last_lp_file),
                    "error_messages": error_messages
                }
    return error_dict


def failed_refine_strategy_basic(xds_file: str, error_message: dict) -> str or None:
    """
    Suggests basic refinement strategies based on error messages.

    Args:
        xds_file (str): Path to the XDS file.
        error_message (dict): Dictionary containing error messages.

    Returns:
        str or None: Suggested refinement step, or None if no strategy is applicable.
    """
    if error_message["stop_file"] == "INTEGRATE.LP":
        if ("!!! ERROR !!! AUTOMATIC DETERMINATION OF SPOT SIZE PARAMETERS HAS FAILED."
                in error_message["error_messages"]):
            return "divergence"
    return None


def failed_refine_strategy_advanced(xds_file: str, error_message: dict) -> str or None:
    """
    Provides advanced strategies for handling failed refinements.

    Args:
        xds_file (str): Path to the XDS file.
        error_message (dict): Dictionary containing error messages.

    Returns:
        None
    """
    if error_message["stop_file"] == "INTEGRATE.LP":
        if ("!!! ERROR !!! AUTOMATIC DETERMINATION OF SPOT SIZE PARAMETERS HAS FAILED."
                in error_message["error_messages"]):
            return "divergence"
    return None


def refine_failed(base_directory: str, xds_list: list = None, mode: str = "basic") -> dict:
    """
    Provides refinement strategies for failed XDS runs.

    Args:
        base_directory (str): Base directory containing XDS files.
        xds_list (list, optional): List of paths to XDS.INP files. Defaults to None.
        mode (str, optional): Refinement mode, either "basic" or "advanced". Defaults to "basic".

    Returns:
        dict: A dictionary mapping failed XDS files to suggested refinement strategies.
    """
    suggestion_dict = {}
    if xds_list is None:
        xds_list = find_xds_files(base_directory)
    error_dict = check_status(xds_list)
    for xds_file, error_message in error_dict.items():
        if mode == "basic":
            suggestion_dict[xds_file] = failed_refine_strategy_basic(xds_file, error_message)
        elif mode == "advanced":
            suggestion_dict[xds_file] = failed_refine_strategy_advanced(xds_file, error_message)
    return suggestion_dict


if __name__ == "__main__":
    import cProfile

    cProfile.run(
        "refine_axis(\"/mnt/c/AutoLEI_demo/Tyrosine/experiment_3/SMV\")",
        sort="tottime")
