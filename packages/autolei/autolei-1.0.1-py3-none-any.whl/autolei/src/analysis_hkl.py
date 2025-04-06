"""
HKL Analysis Module

This module provides functions to analyze HKL data files used in crystallography.
It extracts essential metadata and computes statistical measures crucial for
crystallographic data assessment, offering a comprehensive toolkit for HKL data
handling, processing, and analysis.

Overview:
    The HKL Analysis Module facilitates a wide range of operations on
    crystallographic data, including:
        - Loading and extracting HKL data.
        - Performing symmetry operations and extinction rule testing.
        - Calculating unit cell parameters and interplanar spacings.
        - Generating, slicing, and transforming reflection data.
        - Assessing unit cell similarities through reduction and distance
          measurement techniques.
        - Conducting statistical analyses for crystallographic assessment.

Key Functions:
    - File Loading and Data Extraction
    - Symmetry Operations and Extinction Rules
    - Unit Cell and Interplanar Spacing Calculations
    - Reflection Data Generation and Slicing
    - Statistical Calculations and Analysis
    - Reflection Data Loading and Transformation
    - Unit Cell Processing

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen
    - License: BSD 3-clause

Dependencies:
    - copy
    - json
    - collections.defaultdict
    - pandas as pd
    - numpy.linalg.eig
    - numpy.linalg.solve
    - scipy.spatial.procrustes
    - scipy.stats.pearsonr
    - scipy.stats.t
    - Custom modules:
        - .util
        - .symmetry_operation.symmetry_operations
        - .xds_input.extract_keywords

Notes:
    - Ensure that the `setting.ini` and `extinction.json` files are correctly
      configured and located in the appropriate directories.
    - The module relies on properly formatted HKL and LP files. Any deviations
      might lead to parsing errors.
"""

import copy
import json
import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd
from numpy.linalg import eig, solve
from scipy.spatial import procrustes
from scipy.stats import t

from .symmetry_operation import symmetry_operations
from .xds_input import extract_keywords

# Constants and Configuration
script_dir = os.path.dirname(__file__)

# Load extinction rules
with open(os.path.join(script_dir, 'extinction.json'), 'r') as file:
    extinction_rule = json.load(file)

slice_list = [
                 80.0, 20.0, 15.0, 10.2, 7.70, 6.67, 5.30, 4.62, 4.20, 3.90, 3.70, 3.46, 3.30,
                 3.14, 3.00, 2.90, 2.82, 2.76, 2.70, 2.63, 2.56, 2.48, 2.40, 2.34, 2.27,
                 2.20, 2.14, 2.07, 2.00, 1.90, 1.80, 1.70, 1.60, 1.50, 1.42, 1.35, 1.28,
                 1.23, 1.18, 1.14, 1.10, 1.07, 1.04, 1.02, 1.00, 0.98, 0.96, 0.93, 0.90,
                 0.87, 0.84] + np.round(np.arange(0.82, 0.30, -0.01), 2).tolist()

IDXV = {'P': 1, 'C': 2, 'I': 2, 'R': 3, 'F': 4}


def load_xdsascii_hkl(hkl_path: str) -> tuple:
    """Loads HKL data from an XDS ASCII file.

    Args:
        hkl_path (str): Path to the XDS ASCII HKL file.

    Returns:
        tuple: Contains space group number (int), unit cell constants (list),
            and reflection data (np.ndarray).
    """
    sg_no = 1  # Default space group number
    unit_cell_constants = []
    data = []
    header_ended = False

    with open(hkl_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            stripped_line = line.strip()

            if not header_ended:
                # Parse header information
                if stripped_line.startswith('!SPACE_GROUP_NUMBER='):
                    try:
                        sg_no = int(stripped_line.split('=', 1)[1])
                    except ValueError:
                        print(f"Invalid space group number format on line {line_number}. Using default sg_no=1.")
                elif stripped_line.startswith('!UNIT_CELL_CONSTANTS='):
                    try:
                        unit_cell_constants = list(map(float, stripped_line.split('=', 1)[1].split()))
                        if len(unit_cell_constants) != 6:
                            raise ValueError
                    except ValueError:
                        print(f"Invalid unit cell constants format on line {line_number}.")
                        raise ValueError("Unit cell constants must contain exactly 6 floating-point numbers.")
                elif stripped_line == '!END_OF_HEADER':
                    if not unit_cell_constants:
                        print("Unit cell constants not found before !END_OF_HEADER.")
                        raise ValueError("Unit cell constants not found in the header.")
                    header_ended = True
            else:
                # Parse data lines
                if not stripped_line or stripped_line.startswith('#'):
                    continue  # Skip empty lines or comments

                parts = stripped_line.split()

                # Check if the line has at least 10 columns
                if len(parts) < 10:
                    continue

                try:
                    h = int(parts[0])
                    k = int(parts[1])
                    l = int(parts[2])
                    float1 = float(parts[3])
                    float2 = float(parts[4])
                    flag = int(parts[9])
                    if float2 <= 0:
                        continue
                    data.append([h, k, l, float1, float2, flag])

                except ValueError as ve:
                    print(f"Skipping line {line_number}: value conversion error ({ve}).")
                    continue  # Skip lines with invalid data types
                except IndexError as ie:
                    print(f"Skipping line {line_number}: index error ({ie}).")
                    continue  # Skip lines with unexpected structure

    if not unit_cell_constants:
        print("Unit cell constants not found in the file.")
        raise ValueError("Unit cell constants not found in the file.")

    if not data:
        print("No valid reflection data found.")
        raise ValueError("No valid reflection data found.")

    data_array = np.array(data, dtype=np.float64)

    # Verify that data_array has exactly 6 columns
    if data_array.shape[1] != 6:
        print(f"Data array has {data_array.shape[1]} columns, expected 6.")
        raise ValueError(f"Expected 6 columns in data_array, but got {data_array.shape[1]}.")

    return sg_no, unit_cell_constants, data_array


def combine_hkl(refls: list, exclude: list = None) -> list:
    """Combines reflection data of same hkl by averaging intensities and sigmas.

    Args:
        refls (list): List of reflection data.
        exclude (list, optional): List of data sources to exclude.
            Defaults to None.

    Returns:
        list: Averaged reflection data for unique (h, k, l) combinations.
    """
    if exclude is None:
        exclude = []

    # Convert the input list to a numpy array for efficient processing
    data = np.array(refls)

    # Extract columns
    hkl = data[:, :3]
    I = data[:, 3]
    sigma = data[:, 4]
    data_source = data[:, 5]

    # Filter out reflections from the exclude list
    mask = np.isin(data_source, exclude, invert=True)
    hkl = hkl[mask]
    # After masking
    I = I[mask]
    sigma = sigma[mask]

    # Flatten and ensure numeric data types
    I = I.flatten().astype(float)
    sigma = sigma.flatten().astype(float)

    # Get unique (h, k, l) combinations and their indices
    unique_hkl, indices, inverse_indices, counts = np.unique(
        hkl, axis=0, return_index=True, return_inverse=True, return_counts=True)

    # Ensure inverse_indices is integer
    inverse_indices = inverse_indices.flatten().astype(int)

    # Sum intensities and sigma inverse squared
    sum_I = np.bincount(inverse_indices, weights=I)
    sum_sigma_inv_sq = np.bincount(inverse_indices, weights=1 / sigma ** 2)

    # Calculate average intensity
    avg_I = sum_I / counts
    # Calculate average sigma
    avg_sigma = 1 / np.sqrt(sum_sigma_inv_sq)

    # Combine results into a single array
    result = np.column_stack((unique_hkl, avg_I, avg_sigma)).tolist()

    return result


# Space Group and Laue Group Operations
def get_laue_group(sg_no: int) -> str:
    """Determines the Laue group based on the space group number.

    Args:
        sg_no (int): Space group number.

    Returns:
        str: Laue group corresponding to the given space group number.
    """
    laue_groups = {
        range(1, 3): "-1",
        range(3, 16): "2/m",
        range(16, 75): "mmm",
        range(75, 89): "4/m",
        range(89, 143): "4/mmm",
        range(143, 149): "-3",
        range(149, 168): "-3m",
        range(168, 177): "6/m",
        range(177, 195): "6/mmm",
        range(195, 207): "m-3",
        range(207, 231): "m-3m"
    }
    for rg, laue in laue_groups.items():
        if sg_no in rg:
            if laue != "-3m":
                return laue
            else:
                if sg_no in [149, 151, 153, 157, 159, 162, 163]:
                    return "-31m"
                else:
                    return "-3m1"

    return "Invalid space group number"


# Symmetry Operations and Extinction Rules
def combine_rules(rules: dict) -> tuple:
    """Combines extinction rules into a condition string and a function.

    Args:
        rules (dict): Dictionary of extinction rules.

    Returns:
        tuple: A condition string (str) and a lambda function for evaluating
            extinction rules.
    """
    condition_dict = {
        "hkl": "",
        "0kl": "h == 0 and ",
        "h0l": "k == 0 and ",
        "hk0": "l == 0 and ",
        "h00": "k == 0 and l == 0 and ",
        "0k0": "h == 0 and l == 0 and ",
        "00l": "h == 0 and k == 0 and ",
        "2h-hl": "h == -2 * k and ",
        "h-2hl": "k == -2 * h and ",
        "hhl": "h == k and ",
        "h-hl": "h == -k and ",
        "hll": "k == l and ",
        "hl-l": "k == -l and ",
        "lk-l": "h == -l and ",
        "lkl": "h == l and "
    }

    combined_conditions = []
    rule_text = ""
    for rule_key, rule_expression in rules.items():
        rule_expression = rule_expression.replace(", ", " and ")
        rule_text = rule_text + f"{rule_key}: {rule_expression}, "
        base_condition = condition_dict.get(rule_key, "")
        if not rule_expression:
            continue
        if base_condition:
            full_condition = f"({base_condition}({rule_expression}))"
        else:
            full_condition = f"({rule_expression})"
        combined_conditions.append(full_condition)

    if not combined_conditions:
        # If no conditions are combined, return a function that always returns False
        return "", lambda h, k, l: False
    # Combine all conditions with logical OR
    final_condition_str = " or ".join(combined_conditions)

    # Compile the combined condition into a Python function
    try:
        condition_func = eval(f"lambda h, k, l: {final_condition_str}")
    except Exception as e:
        raise ValueError(f"Error compiling extinction rules: {e}")

    return rule_text, condition_func


def test_rules(refls: list, sg_number: int, _rule: dict, is_R: bool = False) -> tuple:
    """Tests space group rules against reflection data.

    Args:
        refls (list): List of reflection data.
        sg_number (int): Space group number.
        _rule (dict): Extinction rule dictionary.
        is_R (bool, optional): Indicates rhombohedral cell. Defaults to False.

    Returns:
        tuple: Extinction rule text, a lambda function, and space group name.
    """

    def sum_intensity(forbidden_reflections, pos):
        total = 0.0
        for reflection in forbidden_reflections:
            intensity = reflection[pos]
            if isinstance(intensity, list):
                total += sum(intensity)
            else:
                total += intensity
        return total

    sub_sgs = _rule[sg_number].get("SG", [])

    if not sub_sgs:
        return "", "False", "Unknown"

    if is_R:
        return "", eval(f"lambda h, k, l: 0"), sub_sgs[0].get("name", "Unknown")[:-1] + "h"

    if len(sub_sgs) == 1:
        extinction_rules = sub_sgs[0].get("extinction", {})
        if extinction_rules:
            rule_text, combined_condition = combine_rules(extinction_rules)
            return rule_text, combined_condition, sub_sgs[0].get("name", "Unknown")
        else:
            return "", eval(f"lambda h, k, l: 0"), sub_sgs[0].get("name", "Unknown")

    best_rule = None
    best_name = "Unknown"
    rule = ""
    min_total_intensity = float('inf')

    # Determine if reflections have five columns
    try:
        has_five_columns = len(refls[0]) == 5 if refls else False
    except ValueError:
        has_five_columns = len(refls[0]) == 5 if refls.any() else False

    for sub_sg in sub_sgs:
        sg_name = sub_sg.get("name", "Unknown")
        extinction_rules = sub_sg.get("extinction", {})
        if not extinction_rules:
            continue  # Skip if no extinction rules are defined

        rule_text, combined_condition = combine_rules(extinction_rules)
        forbidden_indices = mark_forbidden_reflections(refls, combined_condition)
        forbidden_refls = [refls[idx] for idx in forbidden_indices]

        if not forbidden_refls:
            # No forbidden reflections, select this rule immediately
            return rule_text, combined_condition, sg_name

        intensity_pos = 3 if has_five_columns else 4
        total_intensity = sum_intensity(forbidden_refls, intensity_pos)

        if total_intensity < min_total_intensity:
            min_total_intensity = total_intensity
            best_rule = copy.deepcopy(combined_condition)  # Make a deep copy here
            best_name = sg_name
            rule = rule_text
        elif total_intensity == 0:
            best_rule = copy.deepcopy(combined_condition)  # And here
            best_name = sg_name
            rule = rule_text
            break

    if best_rule:
        return rule, best_rule, best_name
    else:
        return "", "False", "Unknown"


def mark_forbidden_reflections(refls: list, condition_func: callable) -> list:
    """Marks forbidden reflections based on a condition function.

    Args:
        refls (list): List of reflection data.
        condition_func (callable): Function to evaluate extinction conditions.

    Returns:
        list: Indices of forbidden reflections.
    """
    if condition_func is None:
        return []
    forbidden_indices = []
    for idx, reflection in enumerate(refls):
        h, k, l = reflection[:3]
        try:
            if condition_func(h, k, l):
                forbidden_indices.append(idx)
        except Exception as e:
            print(f"Error evaluating condition for reflection {reflection}: {e}")
            continue

    return forbidden_indices


# Reflection Data Operations
def unit_cell_volume(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> float:
    """Calculates the unit cell volume.

    Args:
        a (float): Unit cell parameter a.
        b (float): Unit cell parameter b.
        c (float): Unit cell parameter c.
        alpha (float): Unit cell angle alpha in degrees.
        beta (float): Unit cell angle beta in degrees.
        gamma (float): Unit cell angle gamma in degrees.

    Returns:
        float: Volume of the unit cell.
    """
    alpha, beta, gamma = np.deg2rad([alpha, beta, gamma])
    return a * b * c * np.sqrt(1 - np.cos(alpha) ** 2 - np.cos(beta) ** 2 - np.cos(gamma) ** 2 +
                               2 * np.cos(alpha) * np.cos(beta) * np.cos(gamma))


def interplanar_spacing(h: int, k: int, l: int, a_star: float, b_star: float, c_star: float,
                        cos_alpha_star: float, cos_beta_star: float, cos_gamma_star: float) -> float:
    """Calculates the interplanar spacing for given Miller indices.

    Args:
        h (int): Miller index h.
        k (int): Miller index k.
        l (int): Miller index l.
        a_star (float): Reciprocal lattice parameter a*.
        b_star (float): Reciprocal lattice parameter b*.
        c_star (float): Reciprocal lattice parameter c*.
        cos_alpha_star (float): Cosine of reciprocal angle alpha*.
        cos_beta_star (float): Cosine of reciprocal angle beta*.
        cos_gamma_star (float): Cosine of reciprocal angle gamma*.

    Returns:
        float: Interplanar spacing (d-spacing).
    """
    d_hkl_sq = 1 / (h ** 2 * a_star ** 2 + k ** 2 * b_star ** 2 + l ** 2 * c_star ** 2 +
                    2 * h * k * a_star * b_star * cos_gamma_star +
                    2 * h * l * a_star * c_star * cos_beta_star +
                    2 * k * l * b_star * c_star * cos_alpha_star)
    return np.sqrt(d_hkl_sq)


def generate_complete_reflection_list(uc: list, d_min: float = 0.79, MM: bool = False) -> list:
    """Generates a list of complete reflections up to a specified d-spacing.

    Args:
        uc (list): Unit cell parameters [a, b, c, alpha, beta, gamma].
        d_min (float, optional): Minimum d-spacing. Defaults to 0.79.
        MM (bool, optional): Macromolecular mode. Defaults to False.

    Returns:
        list: List of reflection indices (h, k, l).
    """
    a, b, c, alpha, beta, gamma = uc

    # Convert angles to radians
    alpha_r = np.radians(alpha)
    beta_r = np.radians(beta)
    gamma_r = np.radians(gamma)

    # Construct direct metric tensor G
    G = np.array([
        [a ** 2, a * b * np.cos(gamma_r), a * c * np.cos(beta_r)],
        [a * b * np.cos(gamma_r), b ** 2, b * c * np.cos(alpha_r)],
        [a * c * np.cos(beta_r), b * c * np.cos(alpha_r), c ** 2]
    ])

    # Invert G to get reciprocal metric tensor G*
    G_inv = np.linalg.inv(G)

    # Estimate initial bounds
    max_h = int(np.ceil(a / d_min))
    max_k = int(np.ceil(b / d_min))
    max_l = int(np.ceil(c / d_min))

    max_int = int(np.sqrt(3) * max(max_h, max_k, max_l)) + 1

    # Heuristic limit check
    if max_h + max_k + max_l > 250 and not MM:
        return []

    # Generate all possible h, k, l indices
    hs = np.arange(-max_h, max_h + 1)
    ks = np.arange(-max_k, max_k + 1)
    ls = np.arange(0, max_l + 1)

    # Create a meshgrid and then flatten
    H, K, L = np.meshgrid(hs, ks, ls, indexing='ij')
    H_flat = H.ravel()
    K_flat = K.ravel()
    L_flat = L.ravel()

    # Filter out (h, k, l) = (0, 0, 0)
    non_zero_mask = ~((H_flat == 0) & (K_flat == 0) & (L_flat == 0))

    # Filter based on the (h + k + l) < max_int condition
    sum_mask = (H_flat + K_flat + L_flat) < max_int

    # Combine masks
    combined_mask = non_zero_mask & sum_mask

    H_sel = H_flat[combined_mask]
    K_sel = K_flat[combined_mask]
    L_sel = L_flat[combined_mask]

    # Form the hkl matrix: shape (N, 3)
    hkl_matrix = np.stack((H_sel, K_sel, L_sel), axis=-1)
    inv_d2 = np.sum((hkl_matrix @ G_inv) * hkl_matrix, axis=1)

    # inv_d2 must be > 0 to have a valid d
    valid_mask = inv_d2 > 0

    hkl_matrix = hkl_matrix[valid_mask]
    inv_d2 = inv_d2[valid_mask]

    # Compute d and filter by d >= d_min
    d = 1.0 / np.sqrt(inv_d2)
    resolution_mask = d >= d_min

    hkl_matrix = hkl_matrix[resolution_mask]

    # Convert back to list of tuples
    refls = [tuple(row) for row in hkl_matrix]

    return refls


def generate_unique_reflections(refls: list, sg_no: int, uc: list) -> list:
    """Generates unique reflections considering symmetry operations.

    Args:
        refls (list): List of reflection data.
        sg_no (int): Space group number.
        uc (list): Unit cell parameters [a, b, c, alpha, beta, gamma].

    Returns:
        list: Unique reflections with interplanar spacings and intensities.
    """
    laue_group = get_laue_group(sg_no)
    symmetry_ops = symmetry_operations.get(laue_group, [])
    has_intensity_sigma = (len(refls[0]) > 3)
    use_intensity_sigma = has_intensity_sigma

    a, b, c, alpha, beta, gamma = uc
    V = unit_cell_volume(a, b, c, alpha, beta, gamma)

    alpha_r, beta_r, gamma_r = np.deg2rad([alpha, beta, gamma])
    sin_alpha, sin_beta, sin_gamma = np.sin([alpha_r, beta_r, gamma_r])
    cos_alpha, cos_beta, cos_gamma = np.cos([alpha_r, beta_r, gamma_r])

    a_star = b * c * sin_alpha / V
    b_star = a * c * sin_beta / V
    c_star = a * b * sin_gamma / V

    cos_alpha_star = (cos_beta * cos_gamma - cos_alpha) / (sin_beta * sin_gamma)
    cos_beta_star = (cos_alpha * cos_gamma - cos_beta) / (sin_alpha * sin_gamma)
    cos_gamma_star = (cos_alpha * cos_beta - cos_gamma) / (sin_alpha * sin_beta)

    unique_reflections_dict = defaultdict(lambda: ([], []))

    # Process all reflections without chunking
    if use_intensity_sigma:
        for reflection in refls:
            h, k, l, I, sig = reflection
            if symmetry_ops:
                # Apply symmetry operations and take minimum key
                key = min(op(h, k, l) for op in symmetry_ops)
            else:
                key = (h, k, l)
            unique_reflections_dict[key][0].append(I)
            unique_reflections_dict[key][1].append(sig)
    else:
        for reflection in refls:
            h, k, l = reflection[:3]
            if symmetry_ops:
                # Apply symmetry operations and take minimum key
                key = min(op(h, k, l) for op in symmetry_ops)
            else:
                key = (h, k, l)
            if key not in unique_reflections_dict:
                unique_reflections_dict[key] = ([], [])

    unique_reflections_keys = list(unique_reflections_dict.keys())

    # Compute final results
    results = []
    for r in unique_reflections_keys:
        h, k, l = r
        d = interplanar_spacing(h, k, l, a_star, b_star, c_star,
                                cos_alpha_star, cos_beta_star, cos_gamma_star)
        if has_intensity_sigma:
            intensities = np.array(unique_reflections_dict[r][0])
            sigmas = np.array(unique_reflections_dict[r][1])
            mean_sigma = np.sqrt(np.mean(np.square(sigmas)) / len(sigmas)) if sigmas.any() else 0.0
            if len(intensities) > 1:
                weights = 1 / np.square(sigmas)
                weighted_mean_intensity = np.sum(weights * intensities) / np.sum(weights)
                weighted_variance = np.sum(weights * (intensities - weighted_mean_intensity) ** 2) / np.sum(weights)
                weighted_sigma = np.sqrt(weighted_variance / (len(intensities) - 1))
            else:
                weighted_mean_intensity = intensities[0]
                weighted_sigma = sigmas[0]
            results.append((h, k, l, d, list(intensities), list(sigmas), weighted_mean_intensity, weighted_sigma, mean_sigma))
        else:
            results.append((h, k, l, d))

    return sorted(results)


def slice_reflections(refls: list, d_max: float, d_min: float) -> list:
    """Slices reflections based on a d-spacing range.

    Args:
        refls (list): List of reflection data.
        d_max (float): Maximum d-spacing.
        d_min (float): Minimum d-spacing.

    Returns:
        list: Reflections within the specified d-spacing range.
    """
    return [
        refl for refl in refls
        if (d_min < refl[3] <= d_max)
    ]


def generate_slice_d(df: pd.DataFrame, num_slices: int = 15) -> list:
    """Generates slicing points for reflections based on the number of slices.

    Args:
        df (pd.DataFrame): DataFrame containing reflection data.
        num_slices (int, optional): Number of slices. Defaults to 15.

    Returns:
        list: Slicing points for the reflection data.
    """

    sorted_df = df.sort_values(by='d')
    slice_size = len(df) // num_slices + 1
    if slice_size < 40:
        slice_size = len(df) // 12 + 1
    if slice_size < 40:
        slice_size = len(df) // 9 + 1
    if slice_size < 40:
        slice_size = len(df) // 6 + 1
    slices = []

    for i in range(num_slices):
        start = i * slice_size
        end = start + slice_size if i < num_slices - 1 else len(df)
        slice_df = sorted_df.iloc[start:end]
        slices.append(slice_df)

    slicing_points = [slices[i]['d'].min() for i in range(num_slices)]

    adjusted_slicing_points = sorted({min(slice_list, key=lambda x: x >= point) for point in slicing_points},
                                     reverse=True)
    if len(adjusted_slicing_points) <= 3:
        return []
    if 80.0 not in adjusted_slicing_points:
        adjusted_slicing_points = ([80.0] + adjusted_slicing_points[:-1] +
                                   ([round(min(slicing_points), 2)]
                                    if adjusted_slicing_points[-2] != round(min(slicing_points), 2) else []))
    else:
        adjusted_slicing_points = (adjusted_slicing_points[:-1] +
                                   ([round(min(slicing_points), 2)]
                                    if adjusted_slicing_points[-2] != round(min(slicing_points), 2) else []))
    if adjusted_slicing_points[1] < 0.90:
        adjusted_slicing_points = [80.0, 1.0] + adjusted_slicing_points[1:]
    elif adjusted_slicing_points[1] < 0.84:
        adjusted_slicing_points = [80.0, 1.0, 0.90] + adjusted_slicing_points[1:]
    elif adjusted_slicing_points[1] < 0.80:
        adjusted_slicing_points = [80.0, 1.0, 0.90, 0.94] + adjusted_slicing_points[1:]

    return adjusted_slicing_points


def generate_slice_report(ideal_refl: list, refls: list, half1: pd.DataFrame) -> list:
    """Generates a report of reflection data slices.

    Args:
        ideal_refl (list): List of ideal reflections.
        refls (list): List of observed reflections.
        half1 (pd.DataFrame): Data for the first half of reflections.

    Returns:
        list: Slice report containing statistics for each resolution slice.
    """
    result_list = []
    resolution_slices = generate_slice_d(half1)

    for i in range(len(resolution_slices) - 1):
        low_res, high_res = resolution_slices[i], resolution_slices[i + 1]
        temp_refls = slice_reflections(refls, low_res, high_res)
        temp_ideals = slice_reflections(ideal_refl, low_res, high_res)
        if temp_refls > temp_ideals:
            temp_refls = temp_refls

        I_values = [row[4] for row in temp_refls]
        total_count = sum(len(I) if isinstance(I, list) else 1 for I in I_values)

        rint, rmeas, rexp = calculate_r_factors(temp_refls)

        cc12, cc_crit = calculate_cc_half(temp_refls)

        # Create a dictionary for the current slice
        result = {
            "low_res": low_res,
            "high_res": high_res,
            "N_obs": total_count,
            "N_uni": len(temp_refls),
            "ideal_N": len(temp_ideals),
            "completeness": round(100 * len(temp_refls) / len(temp_ideals), 2),
            "multiplicity": round(total_count / len(temp_refls), 2),
            "Isa_meas": calculate_mean_i_over_sigma(temp_refls),
            "R_int": rint,
            "R_meas": rmeas,
            "R_exp": rexp,
            "CC1/2": cc12,
            "CC_crit": cc_crit
        }
        result_list.append(result)
    return result_list


def accumulate_statistics(refls: list, reso: float) -> tuple:
    """Accumulates statistical data for reflections within a resolution limit.

    Args:
        refls (list): List of reflections.
        reso (float): Resolution limit.
        half1 (pd.DataFrame): Data for the first half of reflections.
        half2 (pd.DataFrame): Data for the second half of reflections.

    Returns:
        tuple: Statistical metrics (number of reflections, mean intensity,
            R factors, CC1/2).
    """
    temp_refls = slice_reflections(refls, 999, reso)
    return (len(temp_refls), calculate_mean_i_over_sigma(temp_refls), calculate_r_factors(temp_refls),
            calculate_cc_half((temp_refls)))


def calculate_resolution_limit(unique_refls: list, half1: pd.DataFrame, p: float = 0.005) -> float:
    """Calculates the resolution limit based on CC, Rmeas and I/S.

    Args:
        unique_refls (list): List of unique reflections.
        half1 (pd.DataFrame): Data for the first half of reflections.
        half2 (pd.DataFrame): Data for the second half of reflections.
        p (float, optional): p-value for the correlation test. Defaults to 0.01.

    Returns:
        float: Resolution limit.
    """
    _list = generate_slice_d(half1)
    if len(_list) <= 3:
        return 999
    reso = 999
    for i in range(1, len(_list) - 1):
        cc12, cc_crit = calculate_cc_half(slice_reflections(unique_refls, _list[i], _list[i + 1]), p)
        if cc12 >= cc_crit:
            reso = _list[i + 1]
        elif cc12 < cc_crit:
            break
        r_int, _, _ = calculate_r_factors(slice_reflections(unique_refls, _list[i], _list[i + 1]))
        if abs(r_int) > 180:
            break
        elif r_int > 100 or r_int < 0:
            isa = calculate_mean_i_over_sigma(slice_reflections(unique_refls, _list[i], _list[i + 1]))
            if isa < 0.5:
                break
    return reso


def calculate_cc_half(uniq_refls: list, p_value: float = 0.005) -> tuple:
    """
    Calculate CC1/2 based on the provided unique reflections.

    Parameters:
    - uniq_refls: List of tuples containing reflection data.
    - p_value: Statistical significance threshold (default is 0.005).

    Returns:
    - A tuple containing CC1/2, sigma_I, and sigma_e^2.
    """

    # Step 1: Filter reflections with len(element5) > 1
    filtered_refls = [refl for refl in uniq_refls if len(refl[4]) > 1]

    if not filtered_refls:
        raise ValueError("No reflections with more than one intensity measurement found.")

    # Extract mean intensities (element7) and sigma (element8)
    mean_intensities = [refl[6] for refl in filtered_refls]
    sigmas = [refl[7] for refl in filtered_refls]

    # Step 2: Calculate sigma_I (standard deviation of mean intensities)
    sigma_I = np.std(mean_intensities, ddof=1)  # Using sample standard deviation

    # Step 3: Calculate average sigma_e^2
    sigma_e_squared = np.mean([sigma ** 2 for sigma in sigmas])

    # Ensure denominator is not zero or negative
    denominator = sigma_I ** 2 + sigma_e_squared
    if denominator <= 0:
        raise ValueError("Denominator in CC1/2 calculation is non-positive.")

    # Step 4: Calculate CC1/2
    cc_half = (sigma_I ** 2 - sigma_e_squared) / denominator

    # Degrees of freedom
    df = len(filtered_refls) - 2
    # Get the critical t-value
    t_critical = t.ppf(1 - p_value / 2, df)
    # Convert t-value to critical correlation coefficient
    cc_critical = np.sqrt(t_critical ** 2 / (t_critical ** 2 + df))

    return np.round(100 * cc_half, 2), np.round(100 * cc_critical, 2)


def calculate_r_factors(refls: list) -> tuple:
    """Calculates R factors for reflection data.

    Args:
        refls (list): List of reflection data.

    Returns:
        tuple: R_int, R_meas, and R_exp values.
    """

    if not refls:
        return 100, 100, 100

    # Extract relevant data
    intensities_list = [np.array(reflection[4]) for reflection in refls]
    sigmas_list = [np.array(reflection[5]) for reflection in refls]
    mean_intensities = np.array([reflection[6] for reflection in refls])

    # Flatten lists for vectorized operations
    all_intensities = np.concatenate(intensities_list)
    all_sigmas = np.concatenate(sigmas_list)

    # Compute sums
    sum_sigma = np.sum(all_sigmas)
    sum_intensity = np.sum(all_intensities)

    # Filter reflections with more than one intensity
    lengths = np.array([len(intensities) for intensities in intensities_list])
    multiple_intensity_mask = lengths > 1

    if not multiple_intensity_mask.any():
        return None, None, None

    # Extract mult_intensities and their mean intensities
    mult_intensities_list = [intensities_list[i] for i in np.where(multiple_intensity_mask)[0]]
    mult_mean_intensities = mean_intensities[multiple_intensity_mask]
    mult_lengths = lengths[multiple_intensity_mask]

    # Flatten lists for vectorized operations
    mult_all_intensities = np.concatenate(mult_intensities_list)
    mult_mean_intensities_repeated = np.concatenate([np.full_like(intensities, mean_intensity)
                                                     for intensities, mean_intensity
                                                     in zip(mult_intensities_list, mult_mean_intensities)])

    # Compute intensity differences
    int_diff = np.abs(mult_all_intensities - mult_mean_intensities_repeated)
    sum_int_diff = np.sum(int_diff)

    # Compute the final sum_meas_diff using vectorized operations
    sqrt_factors = np.sqrt(mult_lengths / (mult_lengths - 1))
    starts = np.cumsum(np.concatenate(([0], mult_lengths[:-1])))
    sum_meas_diff = np.sum(sqrt_factors * np.add.reduceat(int_diff, starts))

    sum_meas_intensity = np.sum(mult_all_intensities)

    # Check for division by zero
    if sum_intensity == 0 or sum_meas_intensity == 0:
        return None, None, None

    # Compute R factors
    r_exp = np.round(100 * sum_sigma / sum_intensity, 2)
    r_meas = np.round(100 * sum_meas_diff / sum_meas_intensity, 2)
    r_int = np.round(100 * sum_int_diff / sum_intensity, 2)

    return r_int, r_meas, r_exp


def calculate_mean_i_over_sigma(refls: list) -> float:
    """Calculates the mean intensity over sigma for reflection data.

    Args:
        refls (list): List of reflection data.

    Returns:
        float: Mean intensity over sigma.
    """
    valid_entries = [
        mean_intensity / mean_sigma
        for _, _, _, _, intensities, sigmas, mean_intensity, _, mean_sigma in refls
        if len(sigmas) > 0 and mean_sigma > 0
    ]

    if not valid_entries:
        return 0.0

    return float(np.round(np.mean(valid_entries), 4))


def mark_multiple_reflections(refls: list) -> pd.DataFrame:
    """Splits reflections into two halves for CC1/2 calculation.

    Args:
        refls (list): List of reflection data.

    Returns:
        tuple: DataFrames for the first and second halves of the reflections.
    """
    half1 = []
    for reflection in refls:
        h, k, l, d, intensities, sigmas, _, _, _ = reflection
        if len(intensities) >= 2:
            half1.append([h, k, l, d, 0])

    half1_df = pd.DataFrame(half1, columns=['h', 'k', 'l', 'd', 'I'])
    return half1_df


def get_unique_ideal_reflection(cell: list, sg: int, resolution: float, rule=None, MM: bool = False) -> list:
    """Generates unique ideal reflections based on unit cell, space group, and resolution.

    Args:
        cell (list): Unit cell parameters [a, b, c, alpha, beta, gamma].
        sg (int): Space group number.
        resolution (float): Resolution limit.
        rule (callable, optional): Extinction rule function. Defaults to None.
        MM (bool, optional): Macromolecular mode. Defaults to False.

    Returns:
        list: Unique ideal reflections.
    """

    a, b, c, al, be, ga = cell
    if abs(a - b) < 0.01 and abs(b - c) < 0.01 and abs(al - be) < 0.1 and abs(be - ga) < 0.1:
        is_R = True
    else:
        is_R = False
    total_refls = generate_complete_reflection_list(cell, resolution, MM)
    if not total_refls:
        return []
    unique_refls = generate_unique_reflections(total_refls, sg, cell)
    unique_refls = slice_reflections(unique_refls, 100, resolution)
    if not rule:
        _, _rule, _ = test_rules(unique_refls, sg, extinction_rule, is_R=is_R)
    else:
        _rule = rule
    forbid_idces = set(mark_forbidden_reflections(unique_refls, _rule))
    unique_refls = [reflection for idx, reflection in enumerate(unique_refls) if idx not in forbid_idces]
    return unique_refls


def analysis_xds_hkl(hkl_file: str, merge: bool = False, reso: float = None, output: bool = False, exclude: list = None,
                     MM: bool = False) -> dict:
    """Analyzes an HKL file to extract and compute crystallographic parameters.

    Args:
        hkl_file (str): Path to the HKL file.
        merge (bool, optional): Whether to merge reflections by identical hkl. Defaults to False.
        reso (float, optional): Resolution limit. Defaults to None.
        output (bool, optional): Whether to print progress messages. Defaults to False.
        exclude (list, optional): Data sources to exclude during merging. Defaults to None.
        MM (bool, optional): Macromolecular mode. Defaults to False.

    Returns:
        dict: Analysis results, including unit cell parameters, reflection statistics, and resolution limit.
    """
    if output:
        print(f"Analysis {hkl_file}.")
    # Load reflections and space group information
    space_group_number, unit_cell, reflections = load_xdsascii_hkl(hkl_file)

    if unit_cell[0] * unit_cell[1] * unit_cell[2] > 300000 and not MM:
        return {"mtime": os.path.getmtime(hkl_file),
                "space_group_number": space_group_number,
                "unit_cell": unit_cell,
                "volume": unit_cell_volume(*unit_cell),
                }

    if merge:
        if output:
            print("Merging peak with same (hkl) ...", end="", flush=True)
        reflections = combine_hkl(reflections, exclude=exclude)
        if output:
            print("\rMerging peak with same (hkl) ... OK")
    else:
        reflections = reflections[:, :5]

    if output:
        print("Test space group and Generate unique reflection ...", end="", flush=True)
    a, b, c, al, be, ga = unit_cell
    if abs(a - b) < 0.01 and abs(b - c) < 0.01 and abs(al - be) < 0.1 and abs(be - ga) < 0.1:
        is_R = True
    else:
        is_R = False
    rule_text, rule, sg_name = test_rules(reflections, space_group_number, extinction_rule, is_R=is_R)
    unique_reflections = generate_unique_reflections(reflections, space_group_number, unit_cell)
    forbidden_indices = mark_forbidden_reflections(unique_reflections, rule)
    unique_reflections = [reflection for idx, reflection in enumerate(unique_reflections) if
                          idx not in forbidden_indices]

    fourth_column = []
    for reflection in unique_reflections:
        try:
            fourth_column.append(float(reflection[3]))
        except ValueError:
            continue

    fourth_column = np.array(fourth_column)

    # Find the max and min values
    max_d = np.max(fourth_column)
    min_d = np.min(fourth_column)

    if output:
        print("\rTest space group and Generate unique reflection ... OK")

    if output:
        print("Analysis the statistics ...", end="", flush=True)

    multi_refls = mark_multiple_reflections(unique_reflections)
    reso_limit = calculate_resolution_limit(unique_reflections, multi_refls)

    if reso_limit == 999 and not reso:
        print(f"\nThe data {hkl_file} is really bad.")
        return {"mtime": os.path.getmtime(hkl_file),
                "space_group_number": space_group_number,
                "unit_cell": unit_cell}

    ideal_reflections = get_unique_ideal_reflection(unit_cell, space_group_number, min(min_d, reso) if reso else min_d,
                                                    rule=rule, MM=MM)

    if not ideal_reflections:
        print(f"\nHuge Unit Cell Detected in {hkl_file}.")
        return {"mtime": os.path.getmtime(hkl_file),
                "space_group_number": space_group_number,
                "unit_cell": unit_cell,
                "volume": unit_cell_volume(*unit_cell),
                }

    num_reso, isa_reso, r_values, cc12_reso = accumulate_statistics(unique_reflections, reso_limit)
    rint_reso, rmeas_reso, rexp_reso = r_values

    if not reso:
        ideal_unique_num = len(slice_reflections(ideal_reflections, 999, reso_limit))
        completeness = num_reso / ideal_unique_num
    else:
        ideal_unique_num = len(slice_reflections(ideal_reflections, 999, reso))
        completeness = len(slice_reflections(unique_reflections, 999, reso)) / ideal_unique_num

    slice_report = generate_slice_report(ideal_reflections, unique_reflections, multi_refls)
    if output:
        print("\rAnalysis the statistics ... OK")

    refl_reso = 0
    ideal_refl_reso = 0
    for item in slice_report:
        if item["high_res"] >= reso_limit:
            refl_reso += item["N_obs"]
            ideal_refl_reso += item["ideal_N"]

    # Compile information dictionary
    info_dict = {
        "mtime": os.path.getmtime(hkl_file),
        "max_res": np.round(max_d, 3),
        "min_res": np.round(min_d, 3),
        "space_group_number": space_group_number,
        "space_group_name": sg_name,
        "rule": rule_text,
        "unit_cell": unit_cell,
        "volume": np.round(unit_cell_volume(*unit_cell), 3),
        "refls_all": len(reflections),
        "refls_reso": refl_reso,
        "uniq_reso": num_reso,
        "multi_reso": round(refl_reso / num_reso, 2),
        "ideal_reso": len(slice_reflections(ideal_reflections, 999, reso_limit)),
        "completeness": round(100 * completeness, 2),
        "resolution": reso_limit,
        "isa": isa_reso,
        "rint": rint_reso,
        "rmeas": rmeas_reso,
        "rexp": rexp_reso,
        "cc12_reso": cc12_reso[0],
        "cc12_crit": cc12_reso[1],
        "slice_report": slice_report
    }

    return info_dict


def load_refls_bravais(xds_hkl: str, reso_low: float, reso_high: float) -> tuple:
    """Loads reflections from XDS HKL file within specified resolution range.

    Args:
        xds_hkl (str): Path to the XDS ASCII HKL file.
        reso_low (float): Low resolution limit.
        reso_high (float): High resolution limit.

    Returns:
        tuple: Filtered reflection data (np.ndarray) and header information (dict).
    """
    with open(xds_hkl, 'r') as f:
        lines = f.readlines()

    header_lines = [line[1:].strip() for line in lines if line.startswith('!')]
    header_dict = extract_keywords(header_lines)

    try:
        data_start = lines.index('!END_OF_HEADER\n') + 1
    except ValueError:
        data_start = next(i for i, line in enumerate(lines) if line.strip() == '!END_OF_HEADER') + 1

    # Efficiently parse the data using NumPy
    data = []
    for line in lines[data_start:]:
        parts = line.split()
        if len(parts) < 5:
            continue
        sigma = float(parts[4])
        if sigma <= 0:
            continue
        h, k, l = map(int, parts[:3])
        intensity, sig_intensity, x, y = map(float, parts[3:7])
        data.append([h, k, l, intensity, sig_intensity, x, y])

    data_array = np.array(data)
    scale_factor = (float(header_dict["QX"][0]) / float(header_dict["DETECTOR_DISTANCE"][0]) /
                    float(header_dict["X-RAY_WAVELENGTH"][0]))
    min_distance = 1 / reso_low / scale_factor
    max_distance = 1 / reso_high / scale_factor
    X0, Y0 = float(header_dict["ORGX"][0]), float(header_dict["ORGY"][0])

    # Calculate distances using vectorized operations
    distances = np.sqrt((data_array[:, -2] - X0) ** 2 + (data_array[:, -1] - Y0) ** 2)

    # Apply all filters at once
    mask = (
            (distances >= min_distance) &
            (distances <= max_distance) &
            (data_array[:, 3] / data_array[:, 4] > 0)
    )
    filtered_data = data_array[mask]

    return filtered_data, (
        header_dict["SPACE_GROUP_NUMBER"],
        header_dict["UNIT_CELL_CONSTANTS"]
    )


def transform_hkl(data_array: np.ndarray, REIDX: list, IDXV_value: int) -> np.ndarray:
    """Transforms HKL data using a transformation matrix and index vector.

    Args:
        data_array (np.ndarray): Array of HKL data.
        REIDX (list): Transformation matrix.
        IDXV_value (int): Lattice centre code.

    Returns:
        np.ndarray: Transformed HKL data.
    """
    transformation_matrix = np.array(REIDX).reshape(3, 4)
    hkl = data_array[:, :3].T  # Shape: (3, N)

    transformed_hkl = (transformation_matrix[:, :3] @ hkl + transformation_matrix[:, 3].reshape(3, 1)) / IDXV_value
    transformed_array = data_array.copy()
    transformed_array[:, :3] = transformed_hkl.T
    return transformed_array


def inverse_transform_hkl(transformed_array: np.ndarray, REIDX: list, IDXV_value: int) -> np.ndarray:
    """Inversely transforms HKL data to obtain the original.

    Args:
        transformed_array (np.ndarray): Transformed HKL data.
        REIDX (list): Transformation matrix.
        IDXV_value (int): Lattice centre code.

    Returns:
        np.ndarray: Original HKL data.
    """
    A = np.array(REIDX).reshape(3, 4)[:, :3]
    b = np.array(REIDX).reshape(3, 4)[:, 3]

    original_hkl = solve(A, (transformed_array[:, :3].T * IDXV_value) - b.reshape(3, 1))
    original_array = transformed_array.copy()
    original_array[:, :3] = original_hkl.T
    return original_array


def shape_cell_parameter_bravais(value_dict: dict, bravais_lattice: str) -> tuple:
    """Shapes cell parameters according to the Bravais lattice type.

    Args:
        value_dict (dict): Dictionary containing cell parameters.
        bravais_lattice (str): Bravais lattice type.

    Returns:
        tuple: Shaped cell parameters.
    """
    a, b, c, alpha, beta, gamma = value_dict["cell_parameters"]
    tolerance_angle = 3
    tolerance_length = 0.03

    def within(value, target, tol):
        return abs(value - target) <= tol

    if bravais_lattice.startswith("a"):  # Triclinic
        return a, b, c, alpha, beta, gamma
    elif bravais_lattice.startswith("h"):  # Hexagonal or Rhombohedral
        if not (within(gamma, 120, tolerance_angle) and
                within(alpha, 90, tolerance_angle) and
                within(beta, 90, tolerance_angle) and
                abs(a - b) <= tolerance_length * (a + b)):
            return ()
        avg_ab = np.mean([a, b])
        return avg_ab, avg_ab, c, 90, 90, 120
    elif bravais_lattice.startswith("m"):  # Monoclinic
        if not (within(gamma, 90, 3) and within(alpha, 90, 3)):
            return ()
        return a, b, c, 90, beta, 90
    elif bravais_lattice.startswith("o"):  # Orthorhombic
        if not all(within(angle, 90, 2) for angle in [alpha, beta, gamma]):
            return ()
        return a, b, c, 90, 90, 90
    elif bravais_lattice.startswith("t"):  # Tetragonal
        if not (within(gamma, 90, 3) and within(alpha, 90, 3) and
                within(beta, 90, 2) and abs(a - b) <= tolerance_length * (a + b)):
            return ()
        avg_ab = np.mean([a, b])
        return avg_ab, avg_ab, c, 90, 90, 90
    elif bravais_lattice.startswith("c"):  # Cubic
        if not (all(within(angle, 90, 3) for angle in [alpha, beta, gamma]) and
                abs(a - b) <= tolerance_length * (a + b) and
                abs(a - c) <= tolerance_length * (a + c)):
            return ()
        avg_abc = np.mean([a, b, c])
        return avg_abc, avg_abc, avg_abc, 90, 90, 90
    return ()


def jordan_form(A: np.ndarray) -> np.ndarray:
    """Calculates the Jordan form of a matrix.

    Args:
        A (np.ndarray): Input matrix.

    Returns:
        np.ndarray: Jordan form of the matrix.
    """
    eigenvalues, _ = eig(A)
    n = A.shape[0]
    J = np.zeros((n, n), dtype=complex)

    eigen_counts = {}
    for val in eigenvalues:
        eigen_counts[np.round(val, decimals=10)] = eigen_counts.get(np.round(val, decimals=10), 0) + 1

    idx = 0
    for eigval, count in eigen_counts.items():
        for _ in range(count):
            J[idx, idx] = eigval
            if idx < n - 1 and count > 1:
                J[idx, idx + 1] = 1
            idx += 1
    return J


def cell_to_matrix(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> np.ndarray:
    """Converts unit cell parameters to matrix form.

    Args:
        a (float): Unit cell parameter a.
        b (float): Unit cell parameter b.
        c (float): Unit cell parameter c.
        alpha (float): Unit cell angle alpha in degrees.
        beta (float): Unit cell angle beta in degrees.
        gamma (float): Unit cell angle gamma in degrees.

    Returns:
        np.ndarray: Matrix representation of the unit cell.
    """
    alpha_rad, beta_rad, gamma_rad = np.radians([alpha, beta, gamma])
    cos_alpha, cos_beta, cos_gamma = np.cos([alpha_rad, beta_rad, gamma_rad])
    sin_gamma = np.sin(gamma_rad)

    v_a = np.array([a, 0, 0])
    v_b = np.array([b * cos_gamma, b * sin_gamma, 0])
    v_c_x = c * cos_beta
    v_c_y = c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma
    v_c_z = c * np.sqrt(1 - cos_beta ** 2 - ((cos_alpha - cos_beta * cos_gamma) / sin_gamma) ** 2)
    v_c = np.array([v_c_x, v_c_y, v_c_z])

    return np.vstack([v_a, v_b, v_c])


def generate_unique_no_d(reflections: np.ndarray, symmetry_ops: list) -> list:
    """Generates unique reflections without considering d-spacing.

    Args:
        reflections (np.ndarray): List of reflection data.
        symmetry_ops (list): List of symmetry operations.

    Returns:
        list: Unique reflections.
    """
    unique_reflections = {}
    has_intensity_sigma = reflections.shape[1] > 4

    for reflection in reflections:
        h, k, l = reflection[:3]
        if has_intensity_sigma:
            intensity, sigma = reflection[3], reflection[4]
        else:
            intensity, sigma = None, None

        # Apply symmetry operations and find the minimum equivalent reflection
        sym_equivs = [tuple(op(h, k, l)) for op in symmetry_ops]
        min_sym_op = min(sym_equivs)

        if min_sym_op in unique_reflections:
            if has_intensity_sigma:
                unique_reflections[min_sym_op][0].append(intensity)
                unique_reflections[min_sym_op][1].append(sigma)
        else:
            if has_intensity_sigma:
                unique_reflections[min_sym_op] = ([intensity], [sigma])
            else:
                unique_reflections[min_sym_op] = ([], [])

    # Compile unique reflections
    unique_list = []
    for (h, k, l), (intensities, sigmas) in unique_reflections.items():
        if has_intensity_sigma and intensities:
            intensities = np.array(intensities)
            sigmas = np.array(sigmas)
            mean_sigma = np.sqrt(np.mean(np.square(sigmas)) / len(sigmas)) if sigmas.any() else 0.0
            if len(intensities) > 1:
                weights = 1 / np.square(sigmas)
                weighted_mean_intensity = np.sum(weights * intensities) / np.sum(weights)
                weighted_variance = np.sum(weights * (intensities - weighted_mean_intensity) ** 2) / np.sum(weights)
                weighted_sigma = np.sqrt(weighted_variance / (len(intensities) - 1))
            else:
                weighted_mean_intensity = intensities[0]
                weighted_sigma = sigmas[0]
            unique_list.append(
                (h, k, l, 0, list(intensities), list(sigmas), weighted_mean_intensity, weighted_sigma, mean_sigma))
        else:
            unique_list.append((h, k, l))
    return unique_list


def real_to_reciprocal(lattice: np.ndarray) -> tuple:
    """Converts real space lattice to reciprocal space lattice.

    Args:
        lattice (np.ndarray): Real space lattice matrix.

    Returns:
        tuple: Reciprocal space lattice matrix and volume of the real lattice.
    """
    volume = np.dot(lattice[0], np.cross(lattice[1], lattice[2]))
    reciprocal_lattice = np.array([
        np.cross(lattice[1], lattice[2]),
        np.cross(lattice[2], lattice[0]),
        np.cross(lattice[0], lattice[1])
    ]) / volume
    return reciprocal_lattice, volume


def unit_cell_distance_procrustes(cell_a: tuple, cell_b: tuple) -> float:
    """Calculates the distance between two unit cells using Procrustes analysis.

    Args:
        cell_a (tuple): Unit cell parameters for the first cell.
        cell_b (tuple): Unit cell parameters for the second cell.

    Returns:
        float: Distance between the two unit cells.
    """
    A_real = cell_to_matrix(*niggli_reduce_cell(*cell_a))
    B_real = cell_to_matrix(*niggli_reduce_cell(*cell_b))

    A_recip, vol_A = real_to_reciprocal(A_real)
    B_recip, vol_B = real_to_reciprocal(B_real)

    A_recip[np.abs(A_recip) < 1e-10] = 0
    B_recip[np.abs(B_recip) < 1e-10] = 0

    try:
        A_jordan = jordan_form(A_recip)
        B_jordan = jordan_form(B_recip)
        _, _, disparity_jordan = procrustes(A_jordan, B_jordan)
    except Exception:
        disparity_jordan = float('inf')

    _, _, disparity_original = procrustes(A_recip, B_recip)
    disparity = min(disparity_jordan, disparity_original)
    rmsd_affine = disparity ** 0.25
    volume_ratio = max(vol_A / vol_B, vol_B / vol_A)

    return round(rmsd_affine * min(np.exp(volume_ratio - 1), 100), 3)


def unit_cell_metric_tensor(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> np.ndarray:
    """Calculates the metric tensor for a unit cell.

    Args:
        a (float): Unit cell parameter a.
        b (float): Unit cell parameter b.
        c (float): Unit cell parameter c.
        alpha (float): Unit cell angle alpha in degrees.
        beta (float): Unit cell angle beta in degrees.
        gamma (float): Unit cell angle gamma in degrees.

    Returns:
        np.ndarray: Metric tensor (3x3 matrix).
    """
    # Convert angles from degrees to radians
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)

    # Compute cosines of the angles
    cos_alpha = np.cos(alpha_rad)
    cos_beta = np.cos(beta_rad)
    cos_gamma = np.cos(gamma_rad)

    # Compute metric tensor components
    G = np.array([
        [a ** 2, a * b * cos_gamma, a * c * cos_beta],
        [a * b * cos_gamma, b ** 2, b * c * cos_alpha],
        [a * c * cos_beta, b * c * cos_alpha, c ** 2]
    ])
    return G


def lll_reduction(basis: np.ndarray, delta: float = 0.75) -> np.ndarray:
    """Performs LLL reduction on a lattice basis.

    Args:
        basis (np.ndarray): Lattice basis vectors (rows of the matrix).
        delta (float, optional): Reduction parameter. Defaults to 0.75.

    Returns:
        np.ndarray: LLL-reduced lattice basis.
    """
    n = basis.shape[0]
    basis = basis.copy()
    # Gram-Schmidt Orthogonalization
    B = np.zeros_like(basis)
    mu = np.zeros((n, n))
    norm_B = np.zeros(n)
    for i in range(n):
        B[i] = basis[i]
        for j in range(i):
            denom = np.dot(B[j], B[j])
            if denom == 0:
                raise ValueError(f"Zero norm encountered in B[{j}]; basis vectors may be linearly dependent.")
            mu[i, j] = np.dot(B[i], B[j]) / denom
        for j in range(i):
            B[i] -= mu[i, j] * B[j]
        norm_B[i] = np.dot(B[i], B[i])
        if norm_B[i] == 0:
            raise ValueError(f"Vector B[{i}] has zero norm; basis vectors may be linearly dependent.")

    k = 1
    while k < n:
        # Size reduction
        for j in range(k - 1, -1, -1):
            q = round(mu[k, j])
            if q != 0:
                basis[k] -= q * basis[j]
                mu[k, j] -= q
        # Recompute B[k] and norm_B[k] after size reduction
        B[k] = basis[k]
        for j in range(k):
            mu[k, j] = np.dot(B[k], B[j]) / np.dot(B[j], B[j])
            B[k] -= mu[k, j] * B[j]
        norm_B[k] = np.dot(B[k], B[k])
        if norm_B[k] == 0:
            raise ValueError(
                f"Vector B[{k}] has zero norm after size reduction; basis vectors may be linearly dependent.")
        # Lovász condition
        if norm_B[k] >= (delta - mu[k, k - 1] ** 2) * norm_B[k - 1]:
            k += 1
        else:
            # Swap basis vectors
            basis[[k, k - 1]] = basis[[k - 1, k]]
            # Recompute Gram-Schmidt coefficients and norms
            for i in range(k - 1, n):
                B[i] = basis[i]
                for j in range(i):
                    denom = np.dot(B[j], B[j])
                    if denom == 0:
                        raise ValueError(
                            f"Zero norm encountered in B[{j}] after swapping; basis vectors may be linearly dependent.")
                    mu[i, j] = np.dot(B[i], B[j]) / denom
                for j in range(i):
                    B[i] -= mu[i, j] * B[j]
                norm_B[i] = np.dot(B[i], B[i])
                if norm_B[i] == 0:
                    raise ValueError(
                        f"Vector B[{i}] has zero norm after swapping; basis vectors may be linearly dependent.")
            k = max(k - 1, 1)
    return basis


def niggli_reduce_cell(a: float, b: float, c: float, alpha: float, beta: float, gamma: float,
                       tol: float = 1e-5) -> tuple:
    """
    Get the Niggli reduced lattice using the numerically stable algorithm
    proposed by R. W. Grosse-Kunstleve, N. K. Sauter, & P. D. Adams,
    Acta Crystallographica Section A Foundations of Crystallography, 2003,
    60(1), 1-6. doi:10.1107/S010876730302186X.

    Args:
        a (float): Unit cell parameter a.
        b (float): Unit cell parameter b.
        c (float): Unit cell parameter c.
        alpha (float): Unit cell angle alpha in degrees.
        beta (float): Unit cell angle beta in degrees.
        gamma (float): Unit cell angle gamma in degrees.
        tol (float, optional): Numerical tolerance. Defaults to 1e-5.

    Returns:
        tuple: Niggli-reduced unit cell parameters.
    """
    # Convert angles from degrees to radians
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)

    # Compute the lattice vectors in Cartesian coordinates
    v_a = np.array([a, 0.0, 0.0])
    v_b = np.array([b * np.cos(gamma_rad), b * np.sin(gamma_rad), 0.0])
    c_x = c * np.cos(beta_rad)
    sin_gamma = np.sin(gamma_rad)
    if sin_gamma == 0:
        raise ValueError("Invalid gamma angle resulting in division by zero.")
    c_y = c * (np.cos(alpha_rad) - np.cos(beta_rad) * np.cos(gamma_rad)) / sin_gamma
    c_z_sq = c ** 2 - c_x ** 2 - c_y ** 2
    if c_z_sq < 0:
        c_z_sq = 0.0  # Correct for numerical errors
    c_z = np.sqrt(c_z_sq)
    v_c = np.array([c_x, c_y, c_z])

    # Lattice matrix
    matrix = np.array([v_a, v_b, v_c])
    matrix = lll_reduction(matrix)

    # Compute the volume of the unit cell
    volume = np.dot(v_a, np.cross(v_b, v_c))
    if volume <= 0:
        raise ValueError("Invalid unit cell parameters resulting in non-positive volume.")

    e = tol * volume ** (1 / 3)

    # Define metric tensor
    G = np.dot(matrix, matrix.T)
    G = (G + G.T) / 2  # Ensure symmetry

    # This sets an upper limit on the number of iterations.

    for _ in range(100):
        # The steps are labelled as Ax as per the labelling scheme in the
        # paper.
        A, B, C, E, N, Y = (
            G[0, 0], G[1, 1], G[2, 2],
            2 * G[1, 2], 2 * G[0, 2], 2 * G[0, 1]
        )

        if B + e < A or (abs(A - B) < e and abs(E) > abs(N) + e):
            # A1
            M = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            A, B, C, E, N, Y = (
                G[0, 0],
                G[1, 1],
                G[2, 2],
                2 * G[1, 2],
                2 * G[0, 2],
                2 * G[0, 1],
            )

        if (C + e < B) or (abs(B - C) < e and abs(N) > abs(Y) + e):
            # A2
            M = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            continue

        ll = 0 if abs(E) < e else E / abs(E)
        m = 0 if abs(N) < e else N / abs(N)
        n = 0 if abs(Y) < e else Y / abs(Y)
        if ll * m * n == 1:
            # A3
            i = -1 if ll == -1 else 1
            j = -1 if m == -1 else 1
            k = -1 if n == -1 else 1
            M = np.diag((i, j, k))
            G = np.dot(np.transpose(M), np.dot(G, M))
        elif ll * m * n in (0, -1):
            # A4
            i = -1 if ll == 1 else 1
            j = -1 if m == 1 else 1
            k = -1 if n == 1 else 1

            if i * j * k == -1:
                if n == 0:
                    k = -1
                elif m == 0:
                    j = -1
                elif ll == 0:
                    i = -1
            M = np.diag((i, j, k))
            G = np.dot(np.transpose(M), np.dot(G, M))

        A, B, C, E, N, Y = (
            G[0, 0],
            G[1, 1],
            G[2, 2],
            2 * G[1, 2],
            2 * G[0, 2],
            2 * G[0, 1],
        )

        # A5
        if abs(E) > B + e or (abs(E - B) < e and Y - e > 2 * N) or (abs(E + B) < e and -e > Y):
            M = np.array([[1, 0, 0], [0, 1, -E / abs(E)], [0, 0, 1]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            continue

        # A6
        if abs(N) > A + e or (abs(A - N) < e and Y - e > 2 * E) or (abs(A + N) < e and -e > Y):
            M = np.array([[1, 0, -N / abs(N)], [0, 1, 0], [0, 0, 1]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            continue

        # A7
        if abs(Y) > A + e or (abs(A - Y) < e and N - e > 2 * E) or (abs(A + Y) < e and -e > N):
            M = np.array([[1, -Y / abs(Y), 0], [0, 1, 0], [0, 0, 1]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            continue

        # A8
        if -e > E + N + Y + A + B or (abs(E + N + Y + A + B) < e < Y + (A + N) * 2):
            M = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
            G = np.dot(np.transpose(M), np.dot(G, M))
            continue

        break

    # Extract reduced lattice parameters from G
    A, B, C = G[0, 0], G[1, 1], G[2, 2]
    E, N, Y = 2 * G[1, 2], 2 * G[0, 2], 2 * G[0, 1]

    a_r = np.sqrt(A)
    b_r = np.sqrt(B)
    c_r = np.sqrt(C)

    cos_alpha_r = E / (2 * b_r * c_r)
    cos_beta_r = N / (2 * a_r * c_r)
    cos_gamma_r = Y / (2 * a_r * b_r)

    # Ensure cosine values are within valid range due to numerical errors
    cos_alpha_r = max(min(cos_alpha_r, 1.0), -1.0)
    cos_beta_r = max(min(cos_beta_r, 1.0), -1.0)
    cos_gamma_r = max(min(cos_gamma_r, 1.0), -1.0)

    alpha_r = np.degrees(np.arccos(cos_alpha_r))
    beta_r = np.degrees(np.arccos(cos_beta_r))
    gamma_r = np.degrees(np.arccos(cos_gamma_r))

    return a_r, b_r, c_r, alpha_r, beta_r, gamma_r


def unit_cell_distance_niggli(cell_a: tuple, cell_b: tuple) -> float:
    """Calculates the distance between two Niggli-reduced unit cells.

    Args:
        cell_a (tuple): Unit cell parameters for the first cell.
        cell_b (tuple): Unit cell parameters for the second cell.

    Returns:
        float: Distance between the two reduced unit cells.
    """
    a_r1, b_r1, c_r1, alpha_r1, beta_r1, gamma_r1 = niggli_reduce_cell(*cell_a)
    cell_a_reduced = (a_r1, b_r1, c_r1, alpha_r1, beta_r1, gamma_r1)

    a_r2, b_r2, c_r2, alpha_r2, beta_r2, gamma_r2 = niggli_reduce_cell(*cell_b)
    cell_b_reduced = (a_r2, b_r2, c_r2, alpha_r2, beta_r2, gamma_r2)

    # Compute metric tensors of the reduced cells
    G_a = unit_cell_metric_tensor(*cell_a_reduced)
    G_b = unit_cell_metric_tensor(*cell_b_reduced)

    # Compute the difference between the metric tensors
    delta_G = G_a - G_b

    # Compute the Frobenius norm of the difference
    distance = np.linalg.norm(delta_G, ord='fro')

    return distance


def parse_and_rank_marked_lines(marked_lines: list) -> dict:
    """Parses and ranks marked lines from the file content.

    Args:
        marked_lines (list): List of marked lines from the file.

    Returns:
        dict: Parsed and ranked data grouped by Bravais lattice type.
    """
    parsed_data = {}
    for line in marked_lines:
        line = re.sub(r'(\d)-', r'\1 -', line)
        parts = line.split()
        if len(parts) < 12:
            continue
        lattice_char, bravais, qof = parts[:3]
        if float(qof) >= 500:
            continue
        cell_params = list(map(float, parts[3:9]))
        transformation_matrix = list(map(int, parts[9:]))
        parsed_data.setdefault(bravais, []).append({
            "lattice_char": lattice_char,
            "bravais_lattice": bravais,
            "qof": float(qof),
            "cell_parameters": cell_params,
            "transformation_matrix": transformation_matrix
        })

    # Sort each Bravais lattice's entries by FOM (qof)
    for bravais in parsed_data:
        parsed_data[bravais].sort(key=lambda x: x["qof"])

    return parsed_data


def find_lattice_correct_lp(file_path: str) -> tuple:
    """Finds and parses the lattice from the correct LP file.

    Args:
        file_path (str): Path to the correct LP file.

    Returns:
        tuple: Test list, resolution range, and selected lattice data.
    """
    with open(file_path, 'r') as f:
        file_content = f.readlines()

    auto_sg_idx = next((i for i, line in enumerate(file_content) if 'AUTOMATIC SPACE GROUP ASSIGNMENT' in line), None)
    if auto_sg_idx is None:
        return ()

    space_group_number = None
    reso_low, reso_high = None, None
    marked_lines = []

    # Extract SPACE_GROUP_NUMBER
    for line in file_content[auto_sg_idx:]:
        if 'SPACE_GROUP_NUMBER' in line:
            space_group_number = int(line.split('=')[1].strip().split()[0])
            break

    if space_group_number == 0:
        # Extract lattice determination section
        lattice_det_idx = next((i for i, line in enumerate(file_content) if
                                'DETERMINATION OF LATTICE CHARACTER AND BRAVAIS LATTICE' in line), None)
        sym_ref_idx = next((i for i, line in enumerate(file_content) if
                            'SYMMETRY OF REFLECTION INTENSITIES' in line), None)
        if lattice_det_idx is None or sym_ref_idx is None:
            return ()

        lattice_section = file_content[lattice_det_idx:sym_ref_idx]
        symmetry_section = file_content[sym_ref_idx:]

        record = False
        for line in lattice_section:
            stripped = line.strip()
            if stripped.startswith('*') and not stripped.startswith('**'):
                record = True
                marked_lines.append(line.replace("*", "").strip())
            elif stripped.startswith('**') and record:
                break
            elif record:
                marked_lines.append(line.replace("*", "").strip())

        # Extract resolution range and final lattice
        final_lattice = None
        for line in symmetry_section:
            if "TEST_RESOLUTION_RANGE=" in line:
                match = re.search(r'([\d\.]+)\s+([\d\.]+)', line)
                if match:
                    reso_low, reso_high = map(float, match.groups())
            if line.strip().startswith('*') and not line.strip().startswith('**'):
                final_lattice = line.split()[-2]
                break

        parsed_data = parse_and_rank_marked_lines(marked_lines[:-1])
        test_list = []

        # Define the lattices that can have multiple entries
        multiple_option_lattices = {"aP", "mP", "mC", "mI"}

        for bravais, entries in parsed_data.items():
            if bravais in multiple_option_lattices:
                # Select up to 3 distinct entries based on a, b, c parameters
                selected_entries = []
                for entry in entries:
                    shaped = shape_cell_parameter_bravais(entry, bravais)
                    if shaped:
                        a_new, b_new, c_new = shaped[:3]
                        is_distinct = True
                        for selected in selected_entries:
                            a_sel, b_sel, c_sel = selected["cell_bravais_lattice"][:3]
                            if (abs(a_new - a_sel) <= 0.5 and
                                    abs(b_new - b_sel) <= 0.5 and
                                    abs(c_new - c_sel) <= 0.5):
                                if selected["lattice_char"] not in ["44", "31"]:
                                    is_distinct = False
                                    break
                        if is_distinct:
                            selected_entries.append({
                                **entry,
                                "cell_bravais_lattice": shaped
                            })
                            if len(selected_entries) == 3:
                                break
                test_list.extend(selected_entries)
            else:
                # For other lattices, select only the top entry
                top_entry = entries[0]
                shaped = shape_cell_parameter_bravais(top_entry, bravais)
                if shaped:
                    test_list.append({
                        **top_entry,
                        "cell_bravais_lattice": shaped
                    })
        try:
            for value_list in parsed_data.values():
                for value in value_list:
                    if final_lattice in value['lattice_char']:
                        selected_lattice = value
        except Exception:
            selected_lattice = next(iter(parsed_data.values()), [None])[0]
        return test_list, reso_low, reso_high, selected_lattice
    return ()


def test_lattice_symmetry_hkl(dir_path: str, output: bool = False) -> dict:
    """Tests lattice symmetry using HKL file and correct LP file.

    Args:
        dir_path (str): Directory containing HKL and LP files.
        output (bool, optional): Whether to print progress messages. Defaults to False.

    Returns:
        dict: Results of the lattice symmetry test, grouped by Bravais lattice.
    """
    correct_lp_path = os.path.join(dir_path, 'CORRECT.LP')
    xds_hkl_path = os.path.join(dir_path, 'XDS_ASCII.HKL')

    lattice_data = find_lattice_correct_lp(correct_lp_path)
    if not lattice_data:
        return {}

    bravais_lattice_sg = {
        'aP': [1], 'mP': [3], 'mC': [5], 'mI': [5], 'oP': [16], 'oC': [21], 'oI': [23], 'oF': [22],
        'tP': [75, 89], 'tI': [79, 97], 'hP': [143, 149, 150, 168, 177], 'hR': [146, 155],
        'cP': [195, 207], 'cI': [197, 211], 'cF': [196, 209]
    }

    test_list, reso_low, reso_high, lattice_used = lattice_data
    refls, _ = load_refls_bravais(xds_hkl_path, 30, 1)
    if refls.shape[0] < 200:
        refls, _ = load_refls_bravais(xds_hkl_path, 30, 0.8)
    if refls.shape[0] < 20:
        if output:
            print("Too few strong reflections in HKL file")
        return {}
    # Inverse transform reflections
    transformed_refls = inverse_transform_hkl(
        refls,
        lattice_used["transformation_matrix"],
        IDXV[lattice_used["bravais_lattice"][-1]]
    )

    result_list = []
    for value in test_list:
        bravais = value["bravais_lattice"]
        transformed = transform_hkl(
            transformed_refls,
            value["transformation_matrix"],
            IDXV[value["bravais_lattice"][-1]]
        )
        distance = unit_cell_distance_procrustes(value["cell_parameters"], value["cell_bravais_lattice"])

        for sg in bravais_lattice_sg.get(bravais, []):
            symmetry_ops = symmetry_operations.get(get_laue_group(sg), [])
            unique = generate_unique_no_d(transformed, symmetry_ops)
            r_meas = calculate_r_factors(unique)[1]

            result_list.append({
                "uniq": len(unique),
                "r_meas": r_meas,
                "diff": distance * 20,
                "sg_no": sg,
                "cc12": calculate_cc_half(unique)[0],
                "bravais_lattice": bravais,
                **value
            })

    # Compute base R_meas and base CC12 from space group 1 if available
    base_r_meas = next((res["r_meas"] for res in result_list if res["sg_no"] == 1), 1)
    base_cc12 = 100 - next((res["cc12"] for res in result_list if res["sg_no"] == 1), 100)

    if not base_r_meas:
        return {}

    for res in result_list:
        res["r_meas_ratio"] = np.round(res["r_meas"] / base_r_meas, 3) if base_r_meas != 0 else float('inf')
        res["cc12_ratio"] = np.round((100 - res["cc12"]) / base_cc12, 3) if base_cc12 != 0 else float('inf')

    # Organize results by Bravais lattice
    return_dict = {}
    for res in sorted(result_list, key=lambda x: x["sg_no"], reverse=True):
        bravais = res["bravais_lattice"]
        return_dict.setdefault(bravais, []).append(res)

    # Filter out unwanted Bravais lattice groups
    filtered_return_dict = {}
    for bravais, values in return_dict.items():
        r_ratios = [v["r_meas_ratio"] for v in values]
        r_values = [v["r_meas"] for v in values]

        if not (all(r > 5 for r in r_ratios) or
                all(r > 3 and rm > 60 for r, rm in zip(r_ratios, r_values))):
            filtered_return_dict[bravais] = values

    ap_entry = filtered_return_dict["aP"]
    if len(ap_entry) == 1:
        pass
    else:
        for entry in ap_entry:
            if entry["lattice_char"] == '31':
                aP_31 = entry
            elif entry["lattice_char"] == '44':
                aP_44 = entry
        if aP_31["qof"] < 40 and all(x < 92 for x in aP_31["cell_parameters"][3:7]):
            aP_31["cc12_ratio"] = 1
            filtered_return_dict["aP"] = [aP_31]
        else:
            filtered_return_dict["aP"] = [aP_44]

    return filtered_return_dict


if __name__ == "__main__":
    print(test_lattice_symmetry_hkl("/mnt/d/AutoLEI-TEST/Test/LaB6/SM-I/7848921/RR-1/raw_data/1/xds/xds", True))
