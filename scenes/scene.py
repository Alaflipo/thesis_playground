
from PySide6.QtGui import QPainter
from PySide6.QtCore import QTimer
import random 
import time

from canvas import Canvas
from utils.network import Network, Vertex, VoronoiDiagram
from utils.shapes import Point, Line, HalfPlane, ComplexPolygon
import utils.colors as Colors
from utils.geometry import half_plane_intersection


class BisectorScene(Canvas): 
    '''Draws the bisector of two random points in the plane'''

    def __init__(self, size, draw_axis = True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self): 
        self.p1: Point = Point(random.randint(1,100), random.randint(1,100))
        self.p2: Point = Point(random.randint(1,100), random.randint(1,100))
        self.bisector: Line = self.p1.bi_sector(self.p2)
        midpoint = self.bisector.start 
        normal_p1 = self.p1 - midpoint
        normal_p2 = self.p2 - midpoint
        self.half_p1: HalfPlane = HalfPlane(self.bisector, normal_p1)
        self.half_p2: HalfPlane = HalfPlane(self.bisector, normal_p2)

    def render_scene(self, painter: QPainter): 
        self.p1.draw(painter)
        self.p2.draw(painter)
        self.half_p1.draw(painter, self.view_box)
        self.half_p2.draw(painter, self.view_box)

class NetworkScene(Canvas): 
    '''Draws a network of vertices and edges of a random network'''

    def __init__(self, size, draw_axis = True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self): 
        self.network = Network.create_random()

    def render_scene(self, painter: QPainter): 
        self.network.draw(painter)

class ClipPolygonScene(Canvas): 

    def __init__(self, size, draw_axis=True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self):
        hull: list[Point] = [
            Point(10,20), Point(20,40), Point(40,70), Point(70,60), Point(80,30), Point(60,10), Point(40,10)
        ]
        self.polygon: ComplexPolygon = ComplexPolygon(hull)
        self.halfplane: HalfPlane = HalfPlane(Line(Point(10,10), Point(30,20)), Point(10, -20))
        self.polygon = self.polygon.clip_with_halfplane(self.halfplane)

    def render_scene(self, painter):
        self.polygon.draw(painter)
        self.halfplane.draw(painter, self.view_box)

class VoronoiCellScene(Canvas): 

    def __init__(self, size, draw_axis=True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self):
        self.middle_point: Point = Point(60,30)
        self.others: list[Point] = [Point(20,30), Point(40,60), Point(80,50), Point(90,20), Point(40,10)]
        self.bisectors = [self.middle_point.bi_sector(other) for other in self.others]
        self.half_planes = [HalfPlane(bisector, self.middle_point - bisector.start) for bisector in self.bisectors]
        self.voronoi_cell: ComplexPolygon = half_plane_intersection(self.half_planes)

    def render_scene(self, painter):
        self.voronoi_cell.draw(painter, color=Colors.GREY)
        self.middle_point.draw(painter)
        for point in self.others: 
            point.draw(painter)
        for half_plane in self.half_planes: 
            half_plane.draw(painter, self.view_box)

class VoronoiDiagramScene(Canvas): 

    def __init__(self, size, draw_axis=True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self):
        self.points: list[Point] = [Point(random.randint(-800, 800), random.randint(-800, 800)) for _ in range(100)]
        self.voronoi_diagram = VoronoiDiagram(self.points)
        
    def render_scene(self, painter):
        self.voronoi_diagram.draw(painter)
        
        
