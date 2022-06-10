# || Swami-Shriji ||

# ----------------- #
#     Libraries     #
# ----------------- #
import shapely.geometry as sg
import re
import math

# ----------------- #
#    Definitions    #
# ----------------- #
# Layer strings
TOP_SILK = ['F.SilkS', 'F.Silkscreen']
BOTTOM_SILK = ['B.SilkS', 'B.Silkscreen']
TOP_COPPER = ['F.Cu']
BOTTOM_COPPER = ['B.Cu']
BOARD_EDGE = ['Edge.Cuts']

# Common patterns
LAYER_STRING = '(layer '
LAYERS_STRING = '(layers\n'

# Graphical strings
GR_ARC = '(gr_arc '
GR_LINE = '(gr_line'

# Default values
DEFAULT_WIDTH = 0.254

# -------------------- #
#   Common Functions   #
# -------------------- #
def getLinesFromString (string, pattern):
  lines = []
  for line in string:
    if pattern in line:
      lines.append(line)

  return lines

def getContentsOfParentheses (string, pattern):
  # Attempt to find the pattern in the string
  try:
    openIndex = string.index(pattern)
  except:
    return -1

  openParentheses = 1
  closeIndex = openIndex

  # Iterate and record until the closing parentheses is found
  while openParentheses != 0:
    # Increment iterator
    closeIndex += 1

    # If an opening parentheses is found, increment openParentheses
    if string[closeIndex] == '(':
      openParentheses += 1
    # If an closing parentheses is found, decrement openParentheses
    if string[closeIndex] == ')':
      openParentheses -= 1

  # Return the contents within the parentheses
  return string[openIndex+1:closeIndex]

def getContentsOfQuote(string, pattern='"'):
  return (re.findall('"([^"]*)"', string))

def getInstancesOfPattern(string, pattern):
  lines = []
  for line in string:
    if pattern in line:
      lines.append(line)

  return lines

def getCoordinatesFromString(string, pattern):
  # Get the contents within the parentheses
  contents = getContentsOfParentheses(string,pattern)
  # If the contents are valid
  if contents != -1:
    # Split by a space
    splitContents = contents.split(" ")
    coords = splitContents[1:]
    # Convert to floats
    return [float(coord) for coord in coords]



# ----------------- #
#      Classes      #
# ----------------- #

# Geometric classes
class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def translate(self, dx, dy):
    self.x += dx
    self.y += dy

  def rotate(self, angle, origin='centroid', usingRadian=False):
    if origin == 'centroid':
      return

    # Convert angle to radian if necessary
    if usingRadian == False:
      angle = angle*math.pi/180

    # Get cosine and sine of angle in short form
    c = math.cos(angle)
    s = math.sin(angle)

    # Translate coordinate relative to given origin
    x = self.x - origin.x
    y = self.y - origin.y

    # Use rotation matrix to compute new point relative to origin
    nx = x*c - y*s
    ny = x*s + y*c

    # Translate coordinate back to absolute origin
    self.x = nx + origin.x
    self.y = ny + origin.y





# class KiArc:

class KiLine:

  def __init__(self, start, end, width=DEFAULT_WIDTH):
    self.start = start
    self.end = end

  def setWidth(self, width):
    self.width = width

  def translate(self, dx, dy):
    self.start.translate(dx,dy)
    self.end.translate(dx,dy)

  def getCentroid(self):
    cx = (start.x + end.x)/2
    cy = (start.y + end.y)/2
    return KiCoord(cx,cy)

  def rotate(self, angle, origin='centroid'):
    # If the origin is centroid, update origin
    if origin == 'centroid':
      origin = self.getCentroid()

    self.start.x



# class KiCirc

class BoardEdges:

  def __getBoardEdgeLineStrings (self, kicadS, layerPattern):
    lines = getInstancesOfPattern(kicadS, layerPattern)
    for line in lines:
      getCoordinatesFromString(line, '(start ')


  def __init__ (self, kicadS, layerPattern):
    lines = self.__getBoardEdgeLineStrings(kicadS, layerPattern)


class Pcb:

  def __getLayersFromKicadS(self, kicadS):
    # Parse the file and search for the layers string
    kicadS = " ".join(kicadS)
    layersS = (getContentsOfParentheses (kicadS, LAYERS_STRING))
    # Each line of layersS is a layer
    # Split by newline and remove the first and last entry in the list
    layers = layersS.split('\n')[1:-2]
    # Get contents of parentheses of all entries
    for i in range(0, len(layers)):
      layers[i] = getContentsOfParentheses(layers[i], '(')

    # Find each layer
    # Find top layer
    for layer in layers:
      # Find top silkscreen
      for string in TOP_SILK:
        if string in layer:
          topSilk = getContentsOfQuote(layer)[0]

      # Find top copper
      for string in TOP_COPPER:
        if string in layer:
          topCopper = getContentsOfQuote(layer)[0]

      # Find bottom silkscreen
      for string in BOTTOM_SILK:
        if string in layer:
          bottomSilk = getContentsOfQuote(layer)[0]

      # Find bottom copper
      for string in BOTTOM_COPPER:
        if string in layer:
          bottomCopper = getContentsOfQuote(layer)[0]

      # Find edge cuts
      for string in BOARD_EDGE:
        if string in layer:
          boardEdge = getContentsOfQuote(layer)[0]


    return [topSilk, topCopper, bottomSilk, bottomCopper, boardEdge]


  def __init__(self,kicadS):

    # Get layers of board
    [self.topSilk,
      self.topCopper,
      self.bottomSilk,
      self.bottomCopper,
      self.boardEdge] = self.__getLayersFromKicadS(kicadS)

    print(self.boardEdge)

    # Get edges of board
    BoardEdges(kicadS, self.boardEdge)























def getLayersFromKicadS (kicadS):
  # Parse the file and search for the layers string
  kicadS = " ".join(kicadS)
  layersS = (getContentsOfParentheses (kicadS, LAYERS_STRING))
  # Each line of layersS is a layer
  # Split by newline and remove the first and last entry in the list
  layers = layersS.split('\n')[1:-2]
  # Get contents of parentheses of all entries
  for i in range(0, len(layers)):
    layers[i] = getContentsOfParentheses(layers[i], '(')

  # Find each layer
  # Find top layer
  for layer in layers:
    # Find top silkscreen
    for string in TOP_SILK:
      if string in layer:
        topSilk = layer

    # Find top copper
    for string in TOP_COPPER:
      if string in layer:
        topCopper = layer

    # Find bottom silkscreen
    for string in BOTTOM_SILK:
      if string in layer:
        bottomSilk = layer

    # Find bottom copper
    for string in BOTTOM_COPPER:
      if string in layer:
        bottomCopper = layer

    # Find edge cuts
    for string in BOARD_EDGE:
      if string in layer:
        boardEdge = layer


  return [topSilk, topCopper, bottomSilk, bottomCopper, boardEdge]



