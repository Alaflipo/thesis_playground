
from PySide6.QtGui import QPainter
import random 

from canvas import Canvas
from network import Network
from utils.shapes import Point, Line


class BisectorScene(Canvas): 
    '''Draws the bisector of two random points in the plane'''

    def __init__(self, size, draw_axis = True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self): 
        self.p1: Point = Point(random.randint(1,100), random.randint(1,100))
        self.p2: Point = Point(random.randint(1,100), random.randint(1,100))
        self.bisector: Line = self.p1.bi_sector(self.p2)

    def render_scene(self, painter: QPainter): 
        self.p1.draw(painter)
        self.p2.draw(painter)
        self.bisector.draw_inf(painter, self.view_box)

class NetworkScene(Canvas): 
    '''Draws a network of vertices and edges of a random network'''

    def __init__(self, size, draw_axis = True):
        super().__init__(size, draw_axis)
    
    def set_up_scene(self): 
        self.network = Network.create_random()

    def render_scene(self, painter: QPainter): 
        self.network.draw(painter)
