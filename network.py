from __future__ import annotations

import random
from PySide6.QtGui import QPainter, QPen, QColor, Qt, QBrush

from utils.shapes import Point, Line 
import utils.colors as Colors


class Vertex: 

    def __init__(self, point: Point, label: str = ""):
        self.label: str = label
        self.point: Point = point
        self.edges: list[Edge] = []

        self.radius = 8
    
    def draw(self, painter: QPainter): 
        painter.setBrush(QBrush(Colors.MAROON))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.point.x() - self.radius, self.point.y() - self.radius, 2 * self.radius, 2 * self.radius)


class Edge: 

    def __init__(self, v1: Vertex, v2: Vertex):
        self.vertices: tuple[Vertex] =  (v1, v2)
        self.line: Line = Line(v1.point, v2.point, thickness=3, color=Colors.TEAL)

    def draw(self, painter: QPainter): 
        self.line.draw(painter) 


class Network: 

    def __init__(self, vertices: list[Vertex], edges: list[Edge]):
        self.vertices: list[Vertex] = vertices
        self.edges: list[Edge] = edges

        self.n_vertices = len(vertices)
        self.n_edges = len(edges)

    @classmethod
    def create_random(cls, size: int = 20, max_range: int = 500, connectivity: int = 50):
        vertices = [Vertex(Point(random.randint(1, max_range), random.randint(1,max_range))) for _ in range(size)]
        edge_indices = random.sample([(i,j) for i in range(size) for j in range(size) if i < j], connectivity)
        edges = [ Edge(vertices[v1], vertices[v2]) for v1, v2 in edge_indices ]
        return Network(vertices, edges)
    
    def draw(self, painter: QPainter): 
        for edge in self.edges: 
            edge.draw(painter)
        for vertex in self.vertices: 
            vertex.draw(painter)
        
