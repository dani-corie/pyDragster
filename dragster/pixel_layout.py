import numpy as np

def fit_panel_to_bounds(logical_size, bounding_box, gap):
  grid_step = (bounding_box + gap) // logical_size
  panel_size = grid_step * logical_size - gap
  margins = (bounding_box - panel_size) // 2
  return grid_step, margins

