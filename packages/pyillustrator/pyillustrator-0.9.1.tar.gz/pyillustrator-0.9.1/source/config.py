# config.py
PHI = 1.61803398875
GOLDEN = 1/PHI
CM_TO_INCHES = 1/2.54

DEFAULT_CONFIG = {
    "style": "default",          # Matplotlib style
    "figwidth": 16,              # Figure width in centimeters
    "xlabel": "X-axis",          # X-axis label
    "ylabel": "Y-axis",          # Y-axis label
    "xlim": [0,1],               # X-axis limit
    "ylim": [0,1],               # Y-axis limit
    "labels":'Margins',          # Where the labels will be set ["Margins","All"]
    "grid": True,                # Enable/disable grid
    "grid_minor": False,         # Enable/disable minor grid
    "xticks": None,              # Custom xticks (None = auto)
    "yticks": None,              # Custom yticks (None = auto)
    "xticklabels": None,         # Custom xtick labels (None = auto)
    "yticklabels": None,         # Custom ytick labels (None = auto)
    "aspect": 'Golden',          # Aspect ratio ('Equal','Golden', 'Square', or numeric)
    "font_size": 8,              # Font size for labels, titles, etc.
    "text_usetex": True,         # Use LaTeX for text rendering
    "Margin":[1.8,1,1,1.8],      # Left, right, bottom and top margins [cm]
    "Gap":[0.5,0.5],             # x and y gaps between subplots [cm]
    "Box_width":1.2,             # Box Width
}