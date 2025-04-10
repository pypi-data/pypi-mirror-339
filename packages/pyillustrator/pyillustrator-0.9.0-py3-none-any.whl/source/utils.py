import matplotlib.pyplot as plt
import numpy as np

from .config import GOLDEN

def compute_ax_height(config, ax_width):
    aspect = config['aspect']
    if aspect == 'Golden':
        return ax_width * GOLDEN
    elif aspect == 'Square':
        return ax_width
    elif aspect == 'Equal':
        dx = config['xlim'][1] - config['xlim'][0]
        dy = config['ylim'][1] - config['ylim'][0]
        return ax_width * dy / dx
    elif isinstance(aspect, (int, float)):
        return ax_width * aspect
    else:
        raise ValueError(f"Invalid aspect ratio: {aspect}")

def set_config(axs, config=None):
    """
    Applies configuration settings to a Matplotlib Axes object.

    Args:
        axs (np.array(matplotlib.axes.Axes)): The Axes object to configure.
        config (dict): Configuration dictionary to override defaults.
    """
    # Set global font properties
    if config['text_usetex']:
        plt.rcParams["text.usetex"] = True
    plt.rcParams["font.size"] = config["font_size"]

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j].set_xlim(config["xlim"])
            axs[i, j].set_ylim(config["ylim"])

            # Set ticks
            dx = config["xlim"][1] - config["xlim"][0]
            dy = config["ylim"][1] - config["ylim"][0]

            axs[i, j].set_xticks(config["xticks"] if config["xticks"] is not None else np.linspace(config["xlim"][0] + dx * 0.05, config["xlim"][1] - dx * 0.05, 5))
            axs[i, j].set_yticks(config["yticks"] if config["yticks"] is not None else np.linspace(config["ylim"][0] + dy * 0.05, config["ylim"][1] - dy * 0.05, 5))

            # Apply labels based on config
            if config["labels"] == 'Margins':
                if j == 0:
                    axs[i, j].set_ylabel(config["ylabel"], fontsize=config["font_size"])
                    if config['yticklabels'] is not None:
                        axs[i, j].set_yticklabels(config["yticklabels"])
                else:
                    axs[i, j].set_yticklabels([])

                if i < axs.shape[0] - 1:
                    axs[i, j].set_xticklabels([])
                else:
                    axs[i, j].set_xlabel(config["xlabel"], fontsize=config["font_size"])
                    if config['xticklabels'] is not None:
                        axs[i, j].set_xticklabels(config["xticklabels"])
            elif config["labels"] == 'All':
                axs[i, j].set_xlabel(config["xlabel"], fontsize=config["font_size"])
                axs[i, j].set_ylabel(config["ylabel"], fontsize=config["font_size"])
                if config['yticklabels'] is not None:
                    axs[i, j].set_yticklabels(config["yticklabels"])
                if config['xticklabels'] is not None:
                    axs[i, j].set_xticklabels(config["xticklabels"])

            # Grid settings
            axs[i, j].grid(config["grid"], which="major")
            axs[i, j].minorticks_on()
            if config["grid_minor"]:
                axs[i, j].grid(which="minor", linestyle=":", alpha=0.7)

            axs[i, j].tick_params(axis="both", which="major", labelsize=config["font_size"], direction="in", top=True, right=True)
            axs[i, j].tick_params(axis="both", which="minor", labelsize=config["font_size"], direction="in", top=True, right=True)

            # Box thickness
            for spine in axs[i, j].spines.values():
                spine.set_linewidth(config["Box_width"])

    return axs

def set_config_double(axs, config=None, pair='Horizontal'):
    """
    Applies configuration settings to a Matplotlib Axes object.

    Args:
        axs (np.array(matplotlib.axes.Axes)): The Axes object to configure.
        config (dict): Configuration dictionary to override defaults.
        pair (str): orientation of the double plots
    """


    # Apply font configuration
    if config['text_usetex']:
        plt.rcParams["text.usetex"] = True
    plt.rcParams["font.size"] = config["font_size"]

    # Set X and Y axis labels
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            # Set limits
            if pair == 'Horizontal':
                axs[i,j,0].set_xlim([config["xlim"][0],config["xlim"][1]/2])
                axs[i,j,1].set_xlim([config["xlim"][1]/2,config["xlim"][1]])
                axs[i,j,0].set_ylim([config["ylim"][0],config["ylim"][1]])
                axs[i,j,1].set_ylim([config["ylim"][0],config["ylim"][1]])
            elif pair == 'Vertical':
                axs[i,j,0].set_xlim([config["xlim"][0],config["xlim"][1]])
                axs[i,j,1].set_xlim([config["xlim"][0],config["xlim"][1]])
                axs[i,j,0].set_ylim([config["ylim"][0],config["ylim"][1]/2])
                axs[i,j,1].set_ylim([config["ylim"][1]/2,config["ylim"][1]])

            # Set xticks and yticks if specified
            if config["xticks"] is not None:
                axs[i,j,0].set_xticks(config["xticks"])
                axs[i,j,1].set_xticks(config["xticks"])
            else:
                dx = config['xlim'][1]-config['xlim'][0]
                if pair == 'Horizontal':
                    axs[i,j,0].set_xticks(np.linspace(config['xlim'][0]+dx*0.05,config['xlim'][1]/2,3)[:-1])
                    axs[i,j,1].set_xticks(np.linspace(config['xlim'][1]/2,config['xlim'][1]-dx*0.05,3))
                elif pair == 'Vertical':
                    axs[i,j,0].set_xticks(np.linspace(config['xlim'][0]+dx*0.05,config['xlim'][1]-dx*0.05,5))
                    axs[i,j,1].set_xticks(np.linspace(config['xlim'][0]+dx*0.05,config['xlim'][1]-dx*0.05,5))
            
            if config["yticks"] is not None:
                axs[i,j,0].set_yticks(config["yticks"])
                axs[i,j,1].set_yticks(config["yticks"])
            else:
                dy = config['ylim'][1]-config['ylim'][0]
                if pair == 'Vertical':
                    axs[i,j,0].set_yticks(np.linspace(config['ylim'][0]+dy*0.05,config['ylim'][1]/2,3)[:-1])
                    axs[i,j,1].set_yticks(np.linspace(config['ylim'][1]/2,config['ylim'][1]-dy*0.05,3))
                elif pair == 'Horizontal':
                    axs[i,j,0].set_yticks(np.linspace(config['ylim'][0]+dy*0.05,config['ylim'][1]-dy*0.05,5))
                    axs[i,j,1].set_yticks(np.linspace(config['ylim'][0]+dy*0.05,config['ylim'][1]-dy*0.05,5))

            if config["labels"] == 'Margins':
                if pair == 'Horizontal':
                    if j==0:
                        axs[i,j,0].set_ylabel(config["ylabel"], fontsize=config["font_size"])
                    if j>0:
                        axs[i,j,0].set_yticklabels([])
                    axs[i,j,1].set_yticklabels([])

                    if i<(axs.shape[0]-1):
                        axs[i,j,0].set_xticklabels([])
                        axs[i,j,1].set_xticklabels([])

                    if i==(axs.shape[0]-1):
                        axs[i,j,0].set_xlabel(config["xlabel"], fontsize=config["font_size"])
                        coords = axs[i,j,0].xaxis.label.get_position()
                        axs[i,j,0].xaxis.set_label_coords(1,-0.12)
                elif pair == 'Vertical':
                    if j==0:
                        axs[i,j,0].set_ylabel(config["ylabel"], fontsize=config["font_size"])
                        axs[i,j,0].yaxis.set_label_coords(-0.18,1)
                    if j>0:
                        axs[i,j,0].set_yticklabels([])
                        axs[i,j,1].set_yticklabels([])

                    if i<(axs.shape[0]-1):
                        axs[i,j,0].set_xticklabels([])
                    axs[i,j,1].set_xticklabels([])

                    if i==(axs.shape[0]-1):
                        axs[i,j,0].set_xlabel(config["xlabel"], fontsize=config["font_size"])

            elif config['labels']=='All':
                axs[i,j,0].set_xlabel(config["xlabel"], fontsize=config["font_size"])
                axs[i,j,0].set_ylabel(config["ylabel"], fontsize=config["font_size"])

            # Apply grid settings
            axs[i,j,0].grid(config["grid"], which="major")
            axs[i,j,1].grid(config["grid"], which="major")
            # Always enable minor ticks
            axs[i,j,0].minorticks_on()
            axs[i,j,1].minorticks_on()
            if config["grid_minor"]:
                axs[i,j,0].grid(which="minor", linestyle=":", alpha=0.7)
                axs[i,j,1].grid(which="minor", linestyle=":", alpha=0.7)

            # Set tick labels font size
            axs[i,j,0].tick_params(axis="both", which="major", labelsize=config["font_size"], direction="in", top=True, right=True)
            axs[i,j,0].tick_params(axis="both", which="minor", labelsize=config["font_size"], direction="in", top=True, right=True)
            axs[i,j,1].tick_params(axis="both", which="major", labelsize=config["font_size"], direction="in", top=True, right=True)
            axs[i,j,1].tick_params(axis="both", which="minor", labelsize=config["font_size"], direction="in", top=True, right=True)

            # Make the axes box thicker
            for spine in axs[i,j,0].spines.values():
                spine.set_linewidth(config["Box_width"])  # Adjust thickness here
            for spine in axs[i,j,1].spines.values():
                spine.set_linewidth(config["Box_width"])  # Adjust thickness here


    return axs