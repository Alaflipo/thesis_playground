
from PySide6.QtGui import QPainter
import random 

from canvas import Canvas
from network import Network
from utils.shapes import Point, Line, HalfPlane


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
