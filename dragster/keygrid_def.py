from enum import Enum
import numpy as np

class _PadDims():
  entrypad_width = 3
  functions_width = 1
  height = 4

ENTRYPAD_DIMS = np.array((_PadDims.entrypad_width, _PadDims.height), dtype=np.uint16)
SINGLE_PANEL_WIDTH = np.array((_PadDims.entrypad_width + _PadDims.functions_width, _PadDims.height), dtype=np.uint16)
DOUBLE_PANEL_WIDTH = np.array((2 * _PadDims.entrypad_width + _PadDims.functions_width, _PadDims.height), dtype=np.uint16)

# note about tuples and lists... yes tuples would be slightly more efficient, but
# 1 - who cares
# 2 - a tuple can't have only one element
# so these are supposed to be lists, don't refactor

grid_numericpad_raw = [
  [ b'N1', b'N2', b'N3' ],
  [ b'N4', b'N5', b'N6' ],
  [ b'N7', b'N8', b'N9' ],
  [ (b'N0', (2, 1)), b'SPC' ]
]

grid_alphapad_raw = [
  [ b'A1', b'A2', b'A3' ],
  [ b'A4', b'A5', b'A6' ],
  [ b'A7', b'A8', b'A9' ],
  [ (b'SPC', (3, 1)) ]
]

# grid_functions_shortreturn_raw = [
#   [ b'FUN' ],         # tbd
#   [ b'LOK' ],         # 'shift / num lock'
#   [ b'BKS' ],         # backspace / (del?)
#   [ b'RET' ]          # return
# ]

grid_functions_tallreturn_raw = [
  [ b'LOK' ],         # 'shift / num lock'
  [ b'BKS' ],         # backspace
  [ (b'RET', (1, 2)) ],  # return
  [ None ]
]

# These are the sizes for the different keyboard layouts (mostly narrow for phone, wide for tablet)

supergrid_single_raw = [
  [
    ( b'WST', (_PadDims.entrypad_width, _PadDims.height) ),
    ( b'FNC', (_PadDims.functions_width, _PadDims.height) )
  ]
]

supergrid_double_raw = [
  [
    ( b'EST', (_PadDims.entrypad_width, _PadDims.height) ),
    ( b'WST', (_PadDims.functions_width, _PadDims.height) ),
    ( b'FNC', (_PadDims.entrypad_width, _PadDims.height) )
  ]
]

def compile_grid(grid):
  x = y = 0
  dims = []
  descriptors = []
  for row in grid:
    for cell in row:
      match cell:
        case (descriptor, (w, h)):
          dims.append([[x, y], [w, h]])
          descriptors.append(descriptor)
          x += w
        case None:
          # To skip a column 'below' double high buttons
          x += 1
        case descriptor:
          dims.append([[x, y], [1, 1]])
          descriptors.append(descriptor)
          x += 1
    y += 1
    x = 0
  return np.array(descriptors, dtype='S3'), np.array(dims, dtype=np.uint16)

grid_numericpad = compile_grid(grid_numericpad_raw)
grid_alphapad = compile_grid(grid_alphapad_raw)
grid_functions = compile_grid(grid_functions_tallreturn_raw)
#grid_functions_shortreturn = compile_grid(grid_functions_shortreturn_raw)

supergrid_single = compile_grid(supergrid_single_raw)
supergrid_double = compile_grid(supergrid_double_raw)