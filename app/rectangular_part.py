from math import ceil
from math import pi
from math import sqrt
from cadquery import Workplane

from part import Part

class RectangularPart(Part):
  @staticmethod
  def dimensions():
    return ['length', 'width', 'thickness']

  def part_type(self):
    return "rectangular"

  def length(self):
    return self.dimensions['length'].in_mm()

  def width(self):
    return self.dimensions['width'].in_mm()

  def area_removed(self):
    return self.length() * self.width() * self.volume_removed

  def total_radius(self):
    return sqrt(self.area_removed() / pi)

  def max_radius(self):
    return min(self.dimensions['length'].in_mm() / 2,
      self.dimensions['width'].in_mm() / 2,
      self.total_radius())

  def number_of_holes(self):
    return ceil(self.area_removed() / (self.max_radius()**2 * pi))

  def hole_radius(self):
    return self.total_radius() / sqrt(self.number_of_holes())

  def hole_diameter(self):
    return 2 * self.hole_radius()

  def box(self):
    return Workplane("XY").box(self.length(), # x
                               self.width(), # y
                               self.dimensions['thickness'].in_mm()) # z

  def box_with_holes(self):
    return self.box().faces(">Z").workplane().hole(self.hole_diameter())

  def shape(self):
    return self.box_with_holes()