"""
XDS Report Module.

This module provides a comprehensive set of functions for processing XDS data, visualising diffraction patterns,
and analyzing crystallographic information derived from XDS output files. It includes utilities for generating
rotation matrices, computing distances to planes, parsing `XDS.INP` files, creating interactive 3D scatter plots,
and generating HTML reports summarizing the analysis and visualisations.

Typical usage example:
    # Visualise lattice from an XDS directory
    visualise_lattice("/path/to/xds_directory")

    # Generate an HTML report for XDS data
    create_html_file("/path/to/report_directory", mode="single")

Attributes:
    html_head (str): HTML header for the report, containing styles and external script references.

Functions:
    rotation_matrix(axis: np.ndarray, theta: float) -> np.ndarray:
        Computes the rotation matrix for a specified axis and angle.

    distance_to_plane(points: np.ndarray, vec_a: np.ndarray, vec_b: np.ndarray) -> np.ndarray:
        Calculates the perpendicular distance of each point to a plane defined by two vectors.

    parse_xds_inp(fn: str) -> tuple:
        Parses the `XDS.INP` file to extract essential crystallographic parameters.

    process_data(xds_dir: str, root: Tk) -> None:
        Processes XDS data for visualisation by extracting and rotating reflection coordinates.

    plot_data(X_rot: np.ndarray, Y_rot: np.ndarray, Z_rot: np.ndarray, ...) -> None:
        Generates a 3D scatter plot of rotated reflection coordinates with interactive controls.

    set_view_direction(ax: plt.Axes, a_star: np.ndarray) -> None:
        Adjusts the view direction of the 3D plot to align with a specified reciprocal lattice vector.

    visualise_lattice(xds_dir: str) -> None:
        Initiates the lattice visualisation process by setting up the GUI and processing data.

    create_html_file(report_path: str, mode: str) -> str:
        Generates an HTML report summarizing the XDS analysis and visualisations.

    open_html_file(path: str, mode: str, open: bool) -> None:
        Opens the generated HTML report in the default web browser.

Dependencies:
    - Standard libraries: os, subprocess, threading, webbrowser, tkinter, matplotlib, numpy, pandas, scipy
    - Third-party libraries: mpld3, plotly
    - Custom modules:
        - util: linux_to_windows_path, is_wsl, unit_cell_with_esd
        - xds_analysis: load_spot_binned, analysis_idxref_lp, etc.
        - xds_cluster: parse_xscale_lp, calculate_dendrogram
        - xds_input: extract_keywords

Credits:
    - Date: 2024-12-15
    - Authors: Developed by Yinlin Chen
    - License: BSD 3-clause

"""

import os
import queue
import subprocess
import threading
import tkinter as tk
import webbrowser
from tkinter import font, messagebox

import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.cluster.hierarchy import dendrogram

from .util import linux_to_windows_path, is_wsl, unit_cell_with_esd
from .xds_analysis import load_spot_binned, load_mosaicity_list, load_divergence_list, load_scale_list, \
    extract_run_result, extract_cluster_result, analysis_idxref_lp
from .xds_cluster import parse_xscale_lp, calculate_dendrogram
from .xds_input import extract_keywords


def rotation_matrix(axis, theta):
    """Computes the rotation matrix for a specified axis and angle.

    Args:
        axis (np.ndarray): A 3-element array representing the axis of rotation.
        theta (float): The rotation angle in radians.

    Returns:
        np.ndarray: A 3x3 matrix representing the rotation matrix.
    """
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    sin_theta_over2 = -axis * np.sin(theta / 2.0)
    b, c, d = sin_theta_over2
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc - ad), 2 * (bd + ac)],
                     [2 * (bc + ad), aa + cc - bb - dd, 2 * (cd - ab)],
                     [2 * (bd - ac), 2 * (cd + ab), aa + dd - bb - cc]])


def distance_to_plane(points, vec_a, vec_b):
    """Calculates the perpendicular distance of each point to a plane defined by two vectors.

    Args:
        points (np.ndarray): Array of points with shape (N, 3).
        vec_a (np.ndarray): First vector defining the plane.
        vec_b (np.ndarray): Second vector defining the plane.

    Returns:
        np.ndarray: A 1D array of distances of each point to the plane.
    """
    normal_vector = np.cross(vec_a, vec_b)
    normal_vector = normal_vector / np.linalg.norm(normal_vector)
    distances = np.abs(np.dot(points, normal_vector))
    return distances


def parse_xds_inp(fn):
    """Parses the `XDS.INP` file to extract essential crystallographic parameters.

    Args:
        fn (str): Path to the `XDS.INP` file.

    Returns:
        tuple: A tuple containing:
            - beam_center (tuple): Beam center coordinates (ORGX, ORGY).
            - osc_angle (float): Oscillation angle in degrees.
            - pixelsize (float): Pixel size.
            - wavelength (float): X-ray wavelength.
            - omega_current (float): Current omega angle in degrees.
            - starting_angle (float): Starting angle in degrees.
            - starting_frame (int): Starting frame number.
            - rotation_axis (np.ndarray): A 3-element array representing the rotation axis.

    Raises:
        FileNotFoundError: If the `XDS.INP` file does not exist.
        Exception: If an error occurs while reading the file.
    """
    try:
        with open(fn, "r") as f:
            params = extract_keywords(f.readlines())
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {fn} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading {fn}: {e}")

    try:
        rotx, roty, rotz = map(float, params["ROTATION_AXIS"][0].split()[:3])
        omega_current = np.degrees(np.arctan2(roty, rotx))
        pixelsize = float(params["QX"][0]) / (
                    float(params["DETECTOR_DISTANCE"][0]) * float(params["X-RAY_WAVELENGTH"][0]))
        beam_center = (float(params["ORGX"][0]), float(params["ORGY"][0]))
        osc_angle = float(params["OSCILLATION_RANGE"][0])
        wavelength = float(params["X-RAY_WAVELENGTH"][0])
        starting_angle = float(params["STARTING_ANGLE"][0])
        starting_frame = int(params["STARTING_FRAME"][0])
        rotation_axis = np.array([rotx, roty, rotz])
    except KeyError as e:
        raise KeyError(f"Missing parameter in XDS.INP: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid parameter format in XDS.INP: {e}")

    return (beam_center, osc_angle, pixelsize, wavelength, omega_current,
            starting_angle, starting_frame, rotation_axis)


class LatticeVisualizer(tk.Toplevel):
    """A pop-out window for visualising lattice data."""

    def __init__(self, parent, xds_dir, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Lattice Visualisation")
        self.geometry("600x750")  # Set desired size
        self.resizable(True, True)
        self.xds_dir = xds_dir
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Initialize queue for thread communication
        self.data_queue = queue.Queue()

        # Initialize plot variables
        self.X_rot = None
        self.Y_rot = None
        self.Z_rot = None
        self.hkl = None
        self.intensity = None
        self.a_star = None
        self.b_star = None
        self.c_star = None

        # Initialize visualisation parameters
        self.current_mode = 'all'
        self.show_intensity = False

        # Set up GUI components
        self.create_widgets()

        # Start data processing in a separate thread
        self.processing_thread = threading.Thread(target=self.process_data, daemon=True)
        self.processing_thread.start()

        # Periodically check the queue for data
        self.after(100, self.check_queue)

    def create_widgets(self):
        """Sets up the GUI components."""
        # Create Matplotlib figure and axis
        self.figure = Figure(figsize=(5, 6.5))
        self.ax = self.figure.add_subplot(111, projection='3d', proj_type='ortho')

        # Embed the plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        # Define font for buttons
        self.button_font = font.Font(family="Liberation Sans", size=12)

        # Create control frames
        control_frame_top = tk.Frame(self)
        control_frame_bottom = tk.Frame(self)
        control_frame_top.pack(side='top', fill='x', padx=5, pady=5)
        control_frame_bottom.pack(side='top', fill='x', padx=5, pady=5)

        # First Line (Left): "All", "Indexed", "Unindexed"
        btn_all = tk.Button(control_frame_top, text='All', command=lambda: self.set_mode('all'), font=self.button_font)
        btn_indexed = tk.Button(control_frame_top, text='Indexed', command=lambda: self.set_mode('indexed'),
                                font=self.button_font)
        btn_unindexed = tk.Button(control_frame_top, text='Unindexed', command=lambda: self.set_mode('unindexed'),
                                  font=self.button_font)
        btn_all.pack(side='left', padx=5, pady=5)
        btn_indexed.pack(side='left', padx=5, pady=5)
        btn_unindexed.pack(side='left', padx=5, pady=5)

        # First Line (Right): "Show Intensity", "Hide Intensity"
        btn_show_intensity = tk.Button(control_frame_top, text='Show Intensity',
                                       command=lambda: self.toggle_intensity(True), font=self.button_font)
        btn_hide_intensity = tk.Button(control_frame_top, text='Hide Intensity',
                                       command=lambda: self.toggle_intensity(False), font=self.button_font)
        btn_show_intensity.pack(side='right', padx=5, pady=5)
        btn_hide_intensity.pack(side='right', padx=5, pady=5)

        # Second Line (Left): "HK0", "H0L", "0KL"
        btn_hk0 = tk.Button(control_frame_bottom, text='HK0', command=lambda: self.set_mode('hk0'),
                            font=self.button_font)
        btn_h0l = tk.Button(control_frame_bottom, text='H0L', command=lambda: self.set_mode('h0l'),
                            font=self.button_font)
        btn_0kl = tk.Button(control_frame_bottom, text='0KL', command=lambda: self.set_mode('0kl'),
                            font=self.button_font)
        btn_hk0.pack(side='left', padx=5, pady=5)
        btn_h0l.pack(side='left', padx=5, pady=5)
        btn_0kl.pack(side='left', padx=5, pady=5)

        # Second Line (Right): "View [100]", "View [010]", "View [001]"
        btn_view_a_star = tk.Button(control_frame_bottom, text='View [100]',
                                    command=lambda: self.set_view_to_vector('a_star'), font=self.button_font)
        btn_view_b_star = tk.Button(control_frame_bottom, text='View [010]',
                                    command=lambda: self.set_view_to_vector('b_star'), font=self.button_font)
        btn_view_c_star = tk.Button(control_frame_bottom, text='View [001]',
                                    command=lambda: self.set_view_to_vector('c_star'), font=self.button_font)
        btn_view_a_star.pack(side='right', padx=5, pady=5)
        btn_view_b_star.pack(side='right', padx=5, pady=5)
        btn_view_c_star.pack(side='right', padx=5, pady=5)

    def process_data(self):
        """Processes XDS data for visualisation by extracting and rotating reflection coordinates."""
        spot_xds = os.path.join(self.xds_dir, "SPOT.XDS")
        idxref_lp = os.path.join(self.xds_dir, "IDXREF.LP")
        xds_inp = os.path.join(self.xds_dir, "XDS.INP")

        try:
            # Parse the SPOT.XDS data
            data = np.loadtxt(spot_xds)
        except FileNotFoundError:
            self.data_queue.put(("error", f"The file {spot_xds} was not found."))
            return
        except Exception as e:
            self.data_queue.put(("error", f"An error occurred while reading {spot_xds}: {e}"))
            return

        if data.size == 0:
            self.data_queue.put(("empty", None))
            return

        # Extract columns
        try:
            x, y = data[:, 0], data[:, 1]
            frame, intensity = data[:, 2], data[:, 3]
            hkl = data[:, 4:7]
        except IndexError:
            self.data_queue.put(("error", "SPOT.XDS does not contain the expected number of columns."))
            return

        try:
            (beam_center, osc_angle, pixelsize, wavelength, omega_current, starting_angle,
             starting_frame, rotation_axis) = (parse_xds_inp(xds_inp))
        except Exception as e:
            self.data_queue.put(("error", f"An error occurred while parsing XDS.INP: {e}"))
            return

        orgx, orgy = beam_center

        # Calculate phi values
        phi = starting_angle + osc_angle * (frame - starting_frame)
        phi_rad = np.deg2rad(phi)  # Convert phi to radians

        X = x - orgx
        Y = y - orgy
        Z = np.zeros_like(X)  # Initialize Z coordinates

        distances = np.sqrt(X ** 2 + Y ** 2)

        mask = distances >= 20
        X = X[mask]
        Y = Y[mask]
        Z = Z[mask]
        intensity = intensity[mask]
        hkl = hkl[mask]
        phi_rad = phi_rad[mask]  # Update phi_rad to reflect filtered points

        coords = np.column_stack((X, Y, Z))

        rot_matrices = np.array([rotation_matrix(rotation_axis, angle) for angle in phi_rad])
        rotated_coords = np.einsum('ijk,ik->ij', rot_matrices, coords) * pixelsize

        # Extract rotated coordinates
        X_rot, Y_rot, Z_rot = rotated_coords[:, 0], rotated_coords[:, 1], rotated_coords[:, 2]

        try:
            coordinate = analysis_idxref_lp(idxref_lp)["cell_coordinates"]
            # Basis vectors
            a = np.array(coordinate[0])
            b = np.array(coordinate[1])
            c = np.array(coordinate[2])
            V = np.dot(a, np.cross(b, c))
            a_star = np.cross(b, c) / V
            b_star = np.cross(c, a) / V
            c_star = np.cross(a, b) / V
        except Exception as e:
            a_star, b_star, c_star = None, None, None

        # Package data for the main thread
        self.data_queue.put(("data", {
            "X_rot": X_rot,
            "Y_rot": Y_rot,
            "Z_rot": Z_rot,
            "hkl": hkl,
            "intensity": intensity,
            "a_star": a_star,
            "b_star": b_star,
            "c_star": c_star
        }))

    def check_queue(self):
        """Checks the data queue and updates the plot accordingly."""
        try:
            while True:
                msg, content = self.data_queue.get_nowait()
                if msg == "data":
                    self.X_rot = content["X_rot"]
                    self.Y_rot = content["Y_rot"]
                    self.Z_rot = content["Z_rot"]
                    self.hkl = content["hkl"]
                    self.intensity = content["intensity"]
                    self.a_star = content["a_star"]
                    self.b_star = content["b_star"]
                    self.c_star = content["c_star"]
                    self.update_plot()
                elif msg == "error":
                    messagebox.showerror("Error", content, parent=self)
                elif msg == "empty":
                    messagebox.showinfo("Info", "No data found in SPOT.XDS.", parent=self)
        except queue.Empty:
            pass
        self.after(100, self.check_queue)

    def set_mode(self, mode):
        """Sets the current visualisation mode and updates the plot."""
        self.current_mode = mode
        self.update_plot()

    def toggle_intensity(self, show):
        """Toggles the intensity display and updates the plot."""
        self.show_intensity = show
        self.update_plot()

    def set_view_to_vector(self, vector_name):
        """Sets the view direction based on the specified reciprocal lattice vector."""
        vector = getattr(self, vector_name, None)
        if vector is not None:
            self.set_view_direction(vector)
            self.canvas.draw()

    def set_view_direction(self, vector):
        """Adjusts the view direction of the 3D plot to align with a specified reciprocal lattice vector."""
        if vector is None:
            return
        norm_vector = vector / np.linalg.norm(vector)
        elev = np.degrees(np.arctan2(norm_vector[2], np.sqrt(norm_vector[0] ** 2 + norm_vector[1] ** 2)))
        azim = np.degrees(np.arctan2(norm_vector[1], norm_vector[0]))
        self.ax.view_init(elev=elev, azim=azim)

    def update_plot(self):
        """Updates the 3D scatter plot based on the current settings."""
        if self.X_rot is None:
            return

        self.ax.clear()

        # Determine marker sizes based on intensity
        if self.show_intensity:
            sizes = np.sqrt(self.intensity)
            sizes = 50 * (sizes / np.max(sizes))  # Normalize and scale sizes
        else:
            sizes = 20

        # Determine colors based on mode
        if self.current_mode == 'indexed' and self.a_star is not None:
            indexed_mask = (self.hkl[:, 0] != 0) | (self.hkl[:, 1] != 0) | (self.hkl[:, 2] != 0)
            colors = np.where(indexed_mask, 'k', 'none')
        elif self.current_mode == 'unindexed' and self.a_star is not None:
            unindexed_mask = (self.hkl[:, 0] == 0) & (self.hkl[:, 1] == 0) & (self.hkl[:, 2] == 0)
            colors = np.where(unindexed_mask, 'r', 'none')
        elif self.current_mode in ['hk0', 'h0l', '0kl'] and self.a_star is not None and self.b_star is not None:
            coords = np.column_stack((self.X_rot, self.Y_rot, self.Z_rot))
            if self.current_mode == 'hk0':
                distances = distance_to_plane(coords, self.a_star, self.b_star)
            elif self.current_mode == 'h0l':
                distances = distance_to_plane(coords, self.a_star, self.c_star)
            else:  # '0kl'
                distances = distance_to_plane(coords, self.b_star, self.c_star)
            close_to_plane = distances < 0.005
            indexed_mask = (self.hkl[:, 0] != 0) | (self.hkl[:, 1] != 0) | (self.hkl[:, 2] != 0)
            unindexed_mask = ~indexed_mask
            colors = np.full(len(distances), 'none')
            colors[close_to_plane & indexed_mask] = 'k'
            colors[close_to_plane & unindexed_mask] = 'r'
        else:  # 'all'
            try:
                indexed_mask = (self.hkl[:, 0] != 0) | (self.hkl[:, 1] != 0) | (self.hkl[:, 2] != 0)
                colors = np.where(indexed_mask, 'k', 'r')
            except Exception as e:
                print(f"No hkl information found due to {e}")
                colors = 'b'

        # Scatter plot
        self.ax.scatter(self.X_rot, self.Y_rot, self.Z_rot, c=colors, s=sizes)

        # Plot reciprocal lattice vectors if available
        if self.a_star is not None and self.b_star is not None and self.c_star is not None:
            # Define scale for arrows
            arrow_length = 2.0  # Adjust as needed
            self.ax.quiver(0, 0, 0, self.a_star[0], self.a_star[1], self.a_star[2],
                           color='blue', length=arrow_length, normalize=False, label='a*')
            self.ax.quiver(0, 0, 0, self.b_star[0], self.b_star[1], self.b_star[2],
                           color='green', length=arrow_length, normalize=False, label='b*')
            self.ax.quiver(0, 0, 0, self.c_star[0], self.c_star[1], self.c_star[2],
                           color='red', length=arrow_length, normalize=False, label='c*')

            # Add text labels at the end of the arrows
            self.ax.text(self.a_star[0] * arrow_length * 1.1, self.a_star[1] * arrow_length * 1.1,
                         self.a_star[2] * arrow_length * 1.1, 'a*', color='blue')
            self.ax.text(self.b_star[0] * arrow_length * 1.1, self.b_star[1] * arrow_length * 1.1,
                         self.b_star[2] * arrow_length * 1.1, 'b*', color='green')
            self.ax.text(self.c_star[0] * arrow_length * 1.1, self.c_star[1] * arrow_length * 1.1,
                         self.c_star[2] * arrow_length * 1.1, 'c*', color='red')

        # Set plot labels
        self.ax.set_xlabel('X (rotated)')
        self.ax.set_ylabel('Y (rotated)')
        self.ax.set_zlabel('Z (rotated)')

        # Set plot limits
        max_range = min(0.6, 1.2 * np.max(np.abs([self.X_rot, self.Y_rot, self.Z_rot])))
        self.ax.set_xlim([-max_range, max_range])
        self.ax.set_ylim([-max_range, max_range])
        self.ax.set_zlim([-max_range, max_range])
        self.ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

        # Remove grid and axes for a cleaner look
        self.ax.grid(False)
        self.ax.set_axis_off()

        self.figure.tight_layout()

        # Redraw the canvas
        self.canvas.draw()

    def on_close(self):
        """Handles the closing of the visualiser window."""
        if messagebox.askokcancel("Quit", "Do you want to close the visualiser?", parent=self):
            self.destroy()


def visualise_lattice(parent, xds_dir):
    """
    Initiates the lattice visualisation by creating a pop-out window.

    Args:
        parent (tk.Widget): The parent Tkinter widget.
        xds_dir (str): Directory containing the XDS output files.
    """
    LatticeVisualizer(parent, xds_dir)


html_head = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" charset="UTF-8"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css"/>
    <style type="text/css">
        body {
            margin: 0;
            min-width: 240px;
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            color: #495057;
        }
        .container-fluid {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 40px auto;
            max-width: 80%;
        }
        .page-header {
            margin-top: 0;
            padding-bottom: 20px;
            border-bottom: 2px solid #004085;
        }
        h1 {
            font-size: 2.5em;
            margin: 0;
            color: #004085;
        }
        h2 {
            font-size: 2em;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #004085;
        }
        h5 {
            margin-left: 20px;
            margin-right: 20px;
        }
        .panel {
            margin-top: 20px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            box-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
        }
        .panel-heading {
            padding: 10px 15px;
            border-bottom: 1px solid #dee2e6;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            background-color: #f5f5f5;
            cursor: pointer;
        }
        .panel-heading h3 {
            margin: 0;
            font-size: 1.25em;
        }
        .panel-body {
            padding: 15px;
        }
        .table-responsive {
            margin-top: 20px;
            overflow-x: auto;
        }
        table {
            table-layout: auto;
            margin-bottom: 20px;
            border-collapse: collapse;
            width: auto;
            max-width: 100%;
            border: 1px solid #dee2e6;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
            font-size: 0.95em;
        }
        th {
            background-color: #f2f2f2;
            color: #343a40;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:nth-child(odd) {
            background-color: #ffffff;
        }
        tr:hover {
            background-color: #e9ecef;
        }
        .plot-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .plot {
            width: 48%;
            margin-bottom: 10px;
        }
        .plot_one_line {
            width: 78%;
            margin-bottom: 30px;
        }
    </style>
</head>\n"""


def create_plotly_figure_cc12(df):
    """Creates a Plotly figure for CC<sub>1/2</sub> vs. resolution.

    Args:
        df (pd.DataFrame): DataFrame containing CC<sub>1/2</sub> and resolution data.

    Returns:
        str: HTML string of the Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["high_res"],
        y=df["CC1/2"],
        mode='lines',
        name='CC<sub>1/2</sub>',
        hovertemplate='%{y}',
        line=dict(color='rgb(34, 193, 195)')
    ))
    fig.add_trace(go.Scatter(
        x=df["high_res"],
        y=df["CC_crit"],
        mode='lines',
        name='CC<sub>1/2</sub> crit. (p=0.5%)',
        hovertemplate='%{y}',
        line=dict(color='rgb(34, 193, 195)', dash='dot')
    ))
    fig.update_layout(
        title='CC<sub>1/2</sub> vs resolution',
        xaxis=dict(title='Resolution (Å)', type='log', gridcolor='lightgrey', showline=True, linewidth=2,
                   linecolor='black', autorange='reversed'),
        yaxis=dict(range=[0, 100], title='CC<sub>1/2</sub>', gridcolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        spikedistance=-1,
        hovermode='x'
    )
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', showline=True)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_plotly_figure_R(df):
    """Creates a Plotly figure for R-values vs. resolution.

    Args:
        df (pd.DataFrame): DataFrame containing R<sub>meas</sub>, R<sub>int</sub>, and resolution data.

    Returns:
        str: HTML string of the Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["high_res"],
        y=df["R_meas"],
        mode='lines+markers',
        name='R<sub>meas</sub>',
        hovertemplate='%{y}',
        line=dict(color='rgb(102, 194, 165)')
    ))
    fig.add_trace(go.Scatter(
        x=df["high_res"],
        y=df["R_int"],
        mode='lines+markers',
        name='R<sub>int</sub>',
        hovertemplate='%{y}',
        line=dict(color='rgb(102, 194, 165)', dash='dot')
    ))
    fig.update_layout(
        title='R value vs Resolution',
        xaxis=dict(title='Resolution (Å)', type='log', gridcolor='lightgrey', showline=True, linewidth=2,
                   linecolor='black', autorange='reversed'),
        yaxis=dict(range=[-20, 200], title='R-value (%)', gridcolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        spikedistance=-1,
        hovermode='x',
        legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
        margin=dict(r=20, l=20)
    )
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', showline=True)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_plotly_figure_reso(plot_type, df):
    """Creates a Plotly figure for resolution-based metrics.

    Args:
        plot_type (str): Type of resolution plot. Options:
            - "isa" for I/Sigma.
            - "completeness" for completeness.
            - "multiplicity" for multiplicity.
        df (pd.DataFrame): DataFrame containing the relevant data for plotting.

    Returns:
        str: HTML string of the Plotly figure.

    Raises:
        ValueError: If an invalid `plot_type` is provided.
    """
    if plot_type == 'isa':
        x_data = df["high_res"]
        y_data = df["Isa_meas"]
        title = 'I/Sigma vs Resolution'
        yaxis_title = 'I/σ'
        line_color = 'rgb(141, 160, 203)'
    elif plot_type == 'completeness':
        x_data = df["high_res"]
        y_data = df["completeness"]
        title = 'Completeness vs Resolution'
        yaxis_title = 'Completeness (%)'
        line_color = 'rgb(231, 138, 195)'
    elif plot_type == 'multiplicity':
        x_data = df["high_res"]
        y_data = df["multiplicity"]
        title = 'Multiplicity vs Resolution'
        yaxis_title = 'Multiplicity'
        line_color = 'rgb(166, 216, 84)'
    else:
        raise ValueError("Invalid plot type. Must be 'isa', 'completeness', or 'multiplicity'.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        name=plot_type.capitalize(),
        hovertemplate='%{y}',
        line=dict(color=line_color)
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(
            title='Resolution (Å)', type='log', gridcolor='lightgrey', showline=True,
            linewidth=2, linecolor='black', autorange='reversed'
        ),
        yaxis=dict(title=yaxis_title, gridcolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        spikedistance=-1,
        hovermode='x',
        margin=dict(r=20, l=20)
    )
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', showline=True)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_plotly_spot(spot_xds):
    """Creates a Plotly figure for spots vs. frames from the `SPOT.XDS` file.

    Args:
        spot_xds (str): Path to the `SPOT.XDS` file.

    Returns:
        str: HTML string of the Plotly figure.
    """

    spot_pd = load_spot_binned(spot_xds)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=spot_pd["rebinned_frame"],
        y=spot_pd["count"],
        mode='lines',
        name='Spot',
        hovertemplate='%{y}',
        line=dict(color='rgb(55, 126, 184)', shape='hv')
    ))
    fig.add_trace(go.Scatter(
        x=spot_pd["rebinned_frame"],
        y=spot_pd["unindexed_count"],
        mode='lines',
        name='Unindexed Spot',
        hovertemplate='%{y}',
        line=dict(color='red', dash='dot', shape='hv')
    ))
    fig.update_layout(
        title='Spots vs Frames',
        xaxis=dict(title='Frames', gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black'),
        yaxis=dict(title='No. of Spots', gridcolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        spikedistance=-1,
        hovermode='x',
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        margin=dict(r=20, l=20)
    )
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_plotly_figure_frame(integrate_lp, plot_type):
    """Creates a Plotly figure for frame-specific statistics.

    Args:
        integrate_lp (str): Path to the `INTEGRATE.LP` file.
        plot_type (str): Type of frame plot. Options:
            - "scale" for scale factor vs. frames.
            - "divergence" for divergence vs. frames.
            - "mosaicity" for mosaicity vs. frames.

    Returns:
        str: HTML string of the Plotly figure.

    Raises:
        ValueError: If an invalid `plot_type` is provided.
    """
    with open(integrate_lp, 'r') as f:
        lines = f.readlines()
    if plot_type == 'scale':
        data = load_scale_list(lines)
        title = 'Scale vs Frames'
        yaxis_title = 'Scale'
        line_color = 'rgb(77, 175, 74)'
    elif plot_type == 'divergence':
        data = load_divergence_list(lines)
        title = 'Divergence vs Frames'
        yaxis_title = 'Divergence'
        line_color = 'rgb(152, 78, 163)'
    elif plot_type == 'mosaicity':
        data = load_mosaicity_list(lines)
        title = 'Mosaicity vs Frames'
        yaxis_title = 'Mosaicity'
        line_color = 'rgb(255, 127, 0)'
    else:
        raise ValueError("Invalid plot type. Must be 'scale', 'divergence', or 'mosaicity'.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(data.keys()),
        y=list(data.values()),
        mode='lines',
        name=plot_type.capitalize(),
        hovertemplate='%{y}',
        line=dict(color=line_color, shape='hv')
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(title='Frames', gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black'),
        yaxis=dict(title=yaxis_title, gridcolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        spikedistance=-1,
        hovermode='x',
        margin=dict(r=20, l=20)
    )
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_html_plot_sec1(dir_path, mode="single"):
    """Generates the first section of the HTML report containing resolution-based statistics plots.

    Args:
        dir_path (str): Directory containing the XDS files.
        mode (str, optional): Mode of the report. Options are:
            - "single" for single datasets.
            - "cluster" for cluster datasets.
            Defaults to "single".

    Returns:
        str: HTML string for the first plot section.
    """
    if mode == "single":
        df = pd.DataFrame(extract_run_result(dir_path)["slice_report"])
    elif mode == "cluster":
        df = pd.DataFrame(extract_cluster_result(dir_path)["slice_report"])
    else:
        return
    html_plot1 = f"""
    <h2>Plot</h2>
    <div class="panel">
        <div class="panel-heading" data-toggle="collapse" data-target="#plot_reso">
            <h3>Statistics over Resolution</h3>
        </div>
        <div id="plot_reso" class="panel-collapse collapse in">
            <div class="panel-body">
                <div class="plot-container">
                    <div class="plot_one_line">{create_plotly_figure_cc12(df)}</div>
                </div>
                <div class="plot-container">
                    <div class="plot">{create_plotly_figure_R(df)}</div>
                    <div class="plot">{create_plotly_figure_reso('isa', df)}</div>
                </div>
                <div class="plot-container">
                    <div class="plot">{create_plotly_figure_reso('completeness', df)}</div>
                    <div class="plot">{create_plotly_figure_reso('multiplicity', df)}</div>
                </div>
            </div>
        </div>
    </div>"""
    return html_plot1


def create_html_plot_sec2_single(dir_path):
    """Generates the second section of the HTML report for single mode, including frame-based statistics plots.

    Args:
        dir_path (str): Directory containing the XDS files.

    Returns:
        str: HTML string for the second plot section.
    """
    integrate_lp = os.path.join(dir_path, "INTEGRATE.LP")
    spot_xds = os.path.join(dir_path, "SPOT.XDS")
    html_plot2 = f"""
    <div class="panel">
        <div class="panel-heading" data-toggle="collapse" data-target="#plot_frame">
            <h3>Statistics over Frames</h3>
        </div>
        <div id="plot_frame" class="panel-collapse collapse in">
            <div class="panel-body">
                <div class="plot-container">
                    <div class="plot">{create_plotly_spot(spot_xds)}</div>
                    <div class="plot">{create_plotly_figure_frame(integrate_lp, "scale")}</div>
                </div>
                <div class="plot-container">
                    <div class="plot">{create_plotly_figure_frame(integrate_lp, "divergence")}</div>
                    <div class="plot">{create_plotly_figure_frame(integrate_lp, "mosaicity")}</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>\n"""
    return html_plot2


def metadata_to_table(st, line):
    """Converts metadata into table format for inclusion in the HTML report.

    Args:
        st (dict): Dictionary containing metadata.
        line (int): Line number or identifier for the metadata entry.

    Returns:
        tuple: A tuple containing:
            - metadata (dict): Metadata formatted for the table.
            - overall (dict): Overall statistics formatted for the table.
            - raw_data (dict): Dictionary containing raw data paths.
    """
    try:
        output_cell = unit_cell_with_esd(st.get("unit_cell"), st.get("unit_cell_esd"))
        metadata = {
            "Data": f"data{line}",
            "#Frame": st.get("frames"),
            "Step (°)": round(st.get("step"), 3),
            "Start (°)": round(st.get("start_angle"), 2),
            "End (°)": round(st.get("end_angle"), 2),
            "Rot.(°)": round(np.degrees(np.arctan2(st.get("rotation_axis")[1],
                                                   st.get("rotation_axis")[0])), 1),
            "WL (Å)": st.get("wavelength"),
            "Camera_l (mm)": st.get("camera_length"),
            "Size1": st.get("input").get("NX")[0],
            "Size2": st.get("input").get("NY")[0],
            "Pixel Size (1/mm)": "{:.3f}".format(
                st.get("pixel_size") / st.get("camera_length") * 10 ** 4 / st.get("wavelength"))
        }
    except TypeError:
        output_cell = unit_cell_with_esd(st.get("unit_cell"), st.get("unit_cell_esd"))
        metadata = None

    overall = {
        "Data": f"data{line}",
        'Reso. Range': "{:.2f}–{:.2f}".format(st.get("max_res", 99), st.get("resolution")),
        "SG": "{} ({})".format(st.get("space_group_name"), st.get("space_group_number"))
        if "space_group_name" in st else st.get("space_group_number"),
        "a (Å)": output_cell[0],
        "b (Å)": output_cell[1],
        "c (Å)": output_cell[2],
        "α (°)": output_cell[3],
        "β (°)": output_cell[4],
        "γ (°)": output_cell[5],
        '#Refls': st.get("refls_reso") if "refls_reso" in st else st.get("N_obs"),
        '#Uniq.': st.get("uniq_reso") if "uniq_reso" in st else st.get("N_uni"),
        'Reso.': st.get("resolution"),
        'Comp.': st.get("completeness"),
        'ISa': st.get("ISa_model"),
        'Rmeas': st.get("rmeas") if "rmeas" in st else st.get("R_meas"),
        'CC1/2': st.get("cc12_reso") if "cc12_reso" in st else st.get("CC1/2"),
    }
    return metadata, overall, {"Data": f"data{line}", "Path": st.get("xds_dir")}


def create_html_table(dir_path, mode="single"):
    """Creates HTML tables summarizing metadata, overall statistics, and raw data paths.

    Args:
        dir_path (str): Directory containing the XDS files.
        mode (str, optional): Mode of the report. Options are:
            - "single" for single datasets.
            - "cluster" for cluster datasets.
            Defaults to "single".

    Returns:
        str: HTML string containing all the generated tables.
    """
    if mode == "single":
        result_dict = extract_run_result(dir_path)
        sta_list = [result_dict]
    elif mode == "cluster":
        result_dict = extract_cluster_result(dir_path, output=True)
        sta_list = list(result_dict['input_statistics'].values()) + [result_dict]
    else:
        return None
    raw_list = []
    metadata_list = []
    overall_list = []
    for i, statistics in enumerate(sta_list):
        metadata, overall, xds_dir = metadata_to_table(statistics, i + 1)
        if metadata:
            metadata_list.append(metadata)
        overall_list.append(overall)
        raw_list.append(xds_dir)
    if len(sta_list) > 1:
        overall_list[-1]["Data"] = "Merged"
        overall_list[-1]["ISa"] = "N/A"
        blank_line = {
            "Data": " ", 'Reso. Range': " ", "SG": " ", "a (Å)": "", "b (Å)": "", "c (Å)": "",
            "α (°)": "", "β (°)": "", "γ (°)": "", '#Refls': "", '#Uniq.': "", 'Reso.': "",
            'Comp.': "", 'ISa': "", 'Rmeas': "", 'CC1/2': "", }
        overall_list.insert(-1, blank_line)

    else:
        overall_list[0]["Reso. Range"] = ("{:.2f}–{:.2f}".format(result_dict["max_res"], result_dict["min_res"])
                                          if "max_res" in result_dict else "N/A")
    table_html1 = pd.DataFrame(metadata_list).to_html(header=True, index=False, )
    table_html2 = pd.DataFrame(overall_list).to_html(header=True, index=False, )
    table_html4 = pd.DataFrame(raw_list if len(raw_list) == 1 else raw_list[:-1]).to_html(header=True, index=False, )

    slice_report = pd.DataFrame(result_dict["slice_report"])
    slice_report.insert(0, 'Resolution', slice_report.apply(
        lambda row: f"{row['low_res']}–{row['high_res']}", axis=1))
    slice_report.rename(columns={'completeness': 'Comp.', 'multiplicity': 'Multi.', 'Isa_meas': 'I/Sigma'},
                        inplace=True)

    # Merge CC1/2 and CC_crit into CC_half and drop the original columns
    slice_report['CC_half'] = slice_report.apply(
        lambda row: f"{row['CC1/2']}*" if row['CC1/2'] > row['CC_crit'] else f"{row['CC1/2']}", axis=1)
    slice_report.drop(columns=['low_res', 'high_res', 'CC1/2', 'CC_crit'], inplace=True)

    # Add new rows
    new_row = {
        'Resolution': 'Inf–{}'.format(result_dict['resolution']) + ("*" if "merge_resolution" in result_dict else ""),
        'N_obs': result_dict['refls_reso'],
        'N_uni': result_dict['uniq_reso'],
        'ideal_N': result_dict['ideal_reso'],
        'Comp.': '{}'.format(result_dict['completeness']) + ("*" if "merge_resolution" in result_dict else ""),
        'Multi.': result_dict['multi_reso'],
        'I/Sigma': result_dict['isa'],
        'R_int': result_dict['rint'],
        'R_meas': result_dict['rmeas'],
        'R_exp': result_dict['rexp'],
        'CC_half': '{}{}'.format(
            result_dict['cc12_reso'], "*" if result_dict['cc12_reso'] > result_dict['cc12_crit'] else ""),
    }

    new_row_empty = {col: ' ' for col in slice_report.columns}
    slice_report.loc[len(slice_report)] = new_row_empty
    slice_report.loc[len(slice_report)] = new_row

    if "merge_resolution" in result_dict:
        complete_string = (f"* The completeness is calculated with "
                           f"resolution cut-off of {result_dict['merge_resolution']} Å.")
    else:
        complete_string = ''

    table_html3 = slice_report.to_html(header=True, index=False, justify='center')

    html_table = f"""
    <body>
    <div class="container-fluid">
        <div class="page-header"><h1>Data Reduction Report</h1></div>
        <h4>This report is for {mode} data in the directory {dir_path}.</h4>
        <h2>Table</h2>
        <div class="panel">
            <div class="panel-heading" data-toggle="collapse" data-target="#metadata"><h3>Metadata</h3></div>
            <div id="metadata" class="panel-collapse collapse in">
                <div class="panel-body"><div class="table-responsive">{table_html1}</div></div>
                <h5>  * The abbreviate parameters used in the metadata table are #Frame = number of frames, 
                Rot. =  the angle between the projection of rotation axis on the detector, 
                WL = wavelength, Camera_l = camera length, Size1/2 = number of pixels on x/y axis, 
                Pixel Size = pixel size in the reciprocal space.</h5>
            </div>
        </div>
        <div class="panel">
            <div class="panel-heading" data-toggle="collapse" data-target="#overall"><h3>Overall Statistics</h3></div>
            <div id="overall" class="panel-collapse collapse in">
                <div class="panel-body"><div class="table-responsive">{table_html2}</div></div>
                <h5>  * The abbreviate parameters used in the metadata table are 
                Reso. Range = the lowest and the highest resolution of raw / merged data, 
                SG =  space group, #Refls = number of reflections in the resolution range,	
                #Uniq. = number of unique reflections in the resolution range, 
                Comp. = Completeness with resolution cut-off, 
                Reso. = suggested resolution cut-off, ISa = Model ISa value reported by XDS.</h5>
            </div>
        </div>
        <div class="panel">
            <div class="panel-heading" data-toggle="collapse" data-target="#resolution"><h3>Resolution Shells</h3></div>
            <div id="resolution" class="panel-collapse collapse in">
                <div class="panel-body"><div class="table-responsive">{table_html3}</div></div>
                <h5>  {complete_string} </h5>
            </div>
        </div>
        <div class="panel">
            <div class="panel-heading" data-toggle="collapse" data-target="#rawdata"><h3>Rawdata Path List</h3></div>
            <div id="rawdata" class="panel-collapse collapse out">
                <div class="panel-body"><div class="table-responsive">{table_html4}</div></div>
            </div>
        </div>\n"""
    return html_table


def create_html_plot_sec2_cluster(dir_path):
    """Generates the second section of the HTML report for cluster mode, including dendrogram plots.

    Args:
        dir_path (str): Directory containing the XDS files.

    Returns:
        str: HTML string for the second plot section.
    """
    xscale_lp_path = os.path.join(dir_path, "XSCALE.LP")
    if os.path.exists(xscale_lp_path):
        ccs = parse_xscale_lp(xscale_lp_path)
        if not ccs:
            print("No correlation coefficients found in XSCALE.LP.")
            return
        z = calculate_dendrogram(ccs)

        fig, ax = plt.subplots(figsize=(9, 5))

        # Create the dendrogram
        dendrogram(z, ax=ax, no_labels=True, color_threshold=0.7)

        # Setting up the plot titles and labels
        ax.set_xlabel("Samples", fontsize=14)
        ax.set_ylabel("Distance", fontsize=14)
        ax.set_title("Dendrogram of Correlation Coefficients", fontsize=18, fontweight='bold')

        html_plot2 = """
        <div class="panel">
            <div class="panel-heading" data-toggle="collapse" data-target="#plot_cluster">
                <h3>Statistics over Clusters</h3>
            </div>
            <div id="plot_cluster" class="panel-collapse collapse in">
                <div class="plot-container">
                    <div class="plot_one_line">{}</div>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>""".format(mpld3.fig_to_html(fig))

        plt.close(fig)
        return html_plot2

    else:
        print(f"File {xscale_lp_path} does not exist.")
        return None


def create_html_file(report_path, mode="single"):
    """Generates an HTML report summarizing the XDS analysis and visualisations.

    Args:
        report_path (str): Directory where the report will be saved.
        mode (str, optional): Mode of the report. Options are:
            - "single" for single datasets.
            - "cluster" for cluster datasets.
            Defaults to "single".

    Returns:
        str: Path to the created HTML file.

    Raises:
        Exception: If an error occurs during HTML file creation.
    """
    print("Creating HTML file ... ... ... ", end="", flush=True)
    html_table = create_html_table(report_path, mode)
    html_plot1 = create_html_plot_sec1(report_path, mode)
    if mode == "single":
        html_plot2 = create_html_plot_sec2_single(report_path)
    elif mode == "cluster":
        html_plot2 = create_html_plot_sec2_cluster(report_path)
    else:
        return None
    html_file = os.path.join(report_path, 'autolei_report.html')
    with open(html_file, 'w') as file:
        file.write(html_head + html_table + html_plot1 + html_plot2)
    print("\rCreating HTML file ... ... ... OK\n")
    return html_file


def open_html_file(path, mode="single", open_html=True):
    """Opens the generated HTML report in the default web browser.

    Args:
        path (str): Directory containing the XDS files.
        mode (str, optional): Mode of the report. Options are:
            - "single" for single datasets.
            - "cluster" for cluster datasets.
            Defaults to "single".
        open_html (bool, optional): Whether to automatically open the report in the browser. Defaults to True.
    """
    if mode == "single":
        if not os.path.exists(os.path.join(path, 'XDS_ASCII.HKL')):
            print("XDS_ASCII.HKL file not found. You may need to run XDS first.")
            return
        file_path = create_html_file(path, mode="single")
    elif mode == "cluster":
        if not os.path.exists(os.path.join(path, 'all.HKL')):
            print("all.HKL file not found. You may need to run XSCALE first.")
            return
        file_path = create_html_file(path, mode="cluster")
    else:
        return None
    file_url = f'file://{file_path}'

    def open_file_in_windows(wsl_path):
        # Convert WSL path to Windows path
        windows_path = linux_to_windows_path(wsl_path)
        command = f'powershell.exe Start-Process "{windows_path}"'
        subprocess.run(command, shell=True)

    def open_url(url):
        webbrowser.open(url)

    if open_html:
        if is_wsl():
            thread = threading.Thread(target=open_file_in_windows, args=(file_path,))
        else:
            thread = threading.Thread(target=open_url, args=(file_url,))
        thread.start()
