import matplotlib.pyplot as plt
import numpy as np
from .config import DEFAULT_CONFIG, GOLDEN, CM_TO_INCHES
from .utils import set_config, set_config_double, compute_ax_height

def grid_plot(nrows: int, ncols: int, config: dict = None):
    '''
    Create a grid of subplots with customizable layout and configuration.

    Args:
        nrows: Number of rows.
        ncols: Number of columns.
        config: Dictionary of config overrides.

    Returns:
        (fig, axs): Matplotlib figure and array of Axes.
    '''
    config = {**DEFAULT_CONFIG, **(config or {})}
    config["nrows"] = nrows  # Used in position computation

    with plt.style.context(config["style"]):
        ax_width = config["figwidth"] - config["Margin"][0] - config["Margin"][1]
        ax_width -= (ncols - 1) * config['Gap'][0]
        ax_width /= ncols
        ax_height = compute_ax_height(config, ax_width)

        fig_height = ax_height * nrows + (nrows - 1) * config['Gap'][1] + config["Margin"][2] + config["Margin"][3]

        fig, axs = plt.subplots(nrows, ncols, figsize=(config["figwidth"] * CM_TO_INCHES, fig_height * CM_TO_INCHES))
        axs = axs.reshape((nrows, ncols))

        axs = set_config(axs, config)

        for i in range(nrows):
            for j in range(ncols):
                pos_x = (config["Margin"][0] + j * (ax_width + config['Gap'][0])) / config["figwidth"]
                pos_y = (config["Margin"][2] + (nrows - 1 - i) * (ax_height + config['Gap'][1])) / fig_height
                axs[i, j].set_position([pos_x, pos_y, ax_width / config["figwidth"], ax_height / fig_height])

    return fig, axs

def grid_plot_double(nrows: int, ncols: int, config: dict = None, pair: str = 'Horizontal'):
    '''
    Create a grid of double subplots with optional horizontal or vertical pairing.

    Args:
        nrows: Number of rows.
        ncols: Number of columns.
        config: Dictionary of config overrides.
        pair: 'Horizontal' or 'Vertical' to define the pairing layout.

    Returns:
        (fig, axs): Matplotlib figure and 3D array of Axes.
    '''
    config = {**DEFAULT_CONFIG, **(config or {})}
    config["nrows"] = nrows

    with plt.style.context(config["style"]):
        ax_width = config["figwidth"] - config["Margin"][0] - config["Margin"][1]
        ax_width -= (ncols - 1) * config['Gap'][0]
        ax_width /= ncols
        ax_height = compute_ax_height(config, ax_width)

        fig_height = ax_height * nrows + (nrows - 1) * config['Gap'][1] + config["Margin"][2] + config["Margin"][3]

        fig, axs = plt.subplots(nrows * 2, ncols, figsize=(config["figwidth"] * CM_TO_INCHES, fig_height * CM_TO_INCHES))
        axs = axs.reshape((nrows, ncols, 2))

        axs = set_config_double(axs, config, pair)

        for i in range(nrows):
            for j in range(ncols):
                pos_x = (config["Margin"][0] + j * (ax_width + config['Gap'][0])) / config["figwidth"]
                pos_y = (config["Margin"][2] + (nrows - 1 - i) * (ax_height + config['Gap'][1])) / fig_height

                if pair == 'Horizontal':
                    axs[i, j, 0].set_position([pos_x, pos_y, 0.5 * ax_width / config["figwidth"], ax_height / fig_height])
                    axs[i, j, 1].set_position([pos_x + 0.5 * ax_width / config["figwidth"], pos_y, 0.5 * ax_width / config["figwidth"], ax_height / fig_height])
                elif pair == 'Vertical':
                    axs[i, j, 0].set_position([pos_x, pos_y, ax_width / config["figwidth"], 0.5 * ax_height / fig_height])
                    axs[i, j, 1].set_position([pos_x, pos_y + 0.5 * ax_height / fig_height, ax_width / config["figwidth"], 0.5 * ax_height / fig_height])
                else:
                    raise ValueError(f"Invalid pair option: {pair}")

    return fig, axs