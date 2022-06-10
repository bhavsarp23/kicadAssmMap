# || Swami-Shriji ||

# ----------------- #
#     Libraries     #
# ----------------- #
import math
import scipy.spatial as ss
import numpy as np
import lxml.etree as et

DEFAULT_WIDTH = 1

# ----------------- #
#      Classes      #
# ----------------- #
# Geometric classes
class GeometricClass:

  stroke = 'black'
  fill = 'transparent'
  width = '1'

  def setStroke(self, stroke):
    self.stroke = stroke

  def setFill(self, fill):
    self.fill = fill

  def setWidth(self, width):
    self.width = str(width)

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

  def scale(self, sx, sy, origin):
    # Translate coordinate relative to given origin
    x = self.x - origin.x
    y = self.y - origin.y

    # Scale
    nx = sx*x
    ny = sy*y

    # Translate coordinate back to absolute origin
    self.x = nx + origin.x
    self.y = ny + origin.y

class LineSegment(GeometricClass):

  def __init__(self, start, end, width=DEFAULT_WIDTH):
    self.start = start
    self.end = end

  def setWidth(self, width):
    self.width = width

  def translate(self, dx, dy):
    self.start.translate(dx,dy)
    self.end.translate(dx,dy)

  def getCentroid(self):
    cx = (self.start.x + self.end.x)/2
    cy = (self.start.y + self.end.y)/2
    return Point(cx,cy)

  def rotate(self, angle, origin='centroid'):
    # If the origin is centroid, update origin
    if origin == 'centroid':
      origin = self.getCentroid()

    self.start.rotate(angle, origin)
    self.end.rotate(angle, origin)

  def scale(self, sx, sy):
    centroid = self.getCentroid()
    # Scale based on centroid
    self.start.scale(sx, sy, centroid)
    self.end.scale(sx, sy, centroid)

  def getSvgElement(self):
    element = et.Element('path')
    element.set('d', 'M{} {} L{} {}'.format(self.start.x, self.start.y, self.end.x, self.end.y))
    element.set('stroke', self.stroke)
    element.set('stroke-width',str(self.width))
    return element

class Text(GeometricClass):

  def __init__(self, string, startPoint=Point(0,0), fontSize=1):
    self.string = string
    self.fontSize = fontSize
    self.startPoint = startPoint
    self.angle = 0

  def translate(self, dx, dy):
    self.startPoint.translate(dx,dy)

  def rotate(self, angle, origin='centroid'):
    self.startPoint.rotate(angle, origin)
    self.angle += angle

  def scale(self, scale):
    self.fontSize = self.fontSize * scale

  def getSvgElement(self):
    element = et.Element('text')
    element.set('x',str(self.startPoint.x))
    element.set('y',str(self.startPoint.y))
    element.text = self.string
    return element

class Arc(GeometricClass):

  def __init__(self, start, mid, end):
    self.start = start
    self.mid = mid
    self.end = end

  def translate(self, dx, dy):
    self.start.translate(dx,dy)
    self.mid.translate(dx,dy)
    self.end.translate(dx,dy)

  def rotate(self, angle, origin='centroid'):

    if origin == 'centroid':
      origin = self.mid

    self.start.rotate(angle, origin)
    self.mid.rotate(angle, origin)
    self.end.rotate(angle, origin)

  def scale(self, sx, sy):
    self.start.scale(sx, sy, self.mid)
    self.end.scale(sx, sy, self.mid)

class Circle(GeometricClass):

  def __init__(self, center, diameter):
    self.center = center
    self.diameter = diameter

  def translate(self, dx, dy):
    self.center.translate(dx, dy)

  def rotate(self, angle, origin='centroid'):
    self.center.rotate(angle, origin)

  def scale(self, scale):
    self.diameter = scale*self.diameter

  def getSvgElement(self):
    element = et.Element('circle')
    element.set('cx', str(self.center.x))
    element.set('cy', str(self.center.y))
    element.set('r', str(self.diameter/2))
    element.set('stroke-width',self.width)
    element.set('fill',self.fill)
    element.set('stroke',self.stroke)
    return element


# class Polygon:

#   def __init__(self, points):
#     self.points = points

# def getConvexHull(points):

#   # Convert points into numpy array
