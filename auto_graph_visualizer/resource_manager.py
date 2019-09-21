import json

# from .compatibility import importlib_resources
from importlib.resources import read_text

VISUAL_STYLE_FILE = 'cy_visual.json'
vs = read_text('auto_graph_visualizer', VISUAL_STYLE_FILE)
visualStyle = json.loads(vs)


def get_visual_style():
    return visualStyle
