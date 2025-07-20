from __future__ import annotations

import random
from PySide6.QtGui import QPainter, QPen, QColor, Qt, QBrush

from utils.shapes import Point, Line, ComplexPolygon, HalfPlane
from utils.geometry import half_plane_intersection
import utils.colors as Colors


class Vertex: 

    def __init__(self, point: Point, label: int = 0):
        self.label: int = label
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
        

class VoronoiDiagram:

    def __init__(self, points: list[Point]):
        self.vertices = [Vertex(points[i], label=i) for i in range(len(points))]
        self.create_voronoi_cells()
    
    def create_voronoi_cells(self): 
        self.voronoi_cells: list[ComplexPolygon] = []
        # sorted_vertices = sorted(vertices, key=lambda vertex: vertex.point.angle())
        for i, vertex in enumerate(self.vertices): 
            others = self.vertices[:i] + self.vertices[i+1:]

            bisectors = [vertex.point.bi_sector(other.point) for other in others]
            half_planes = [HalfPlane(bisector, vertex.point - bisector.start) for bisector in bisectors]
            voronoi_cell: ComplexPolygon = half_plane_intersection(half_planes)
            self.voronoi_cells.append(voronoi_cell)
    
    def half_plane_intersection(self, half_planes: list[HalfPlane]) -> ComplexPolygon: 
        area: ComplexPolygon = ComplexPolygon([Point(-1000, 1000), Point(1000,1000), Point(1000,-1000), Point(-1000, -1000)]) 

        for i, half_plane in enumerate(half_planes): 
            area = area.clip_with_halfplane(half_plane)
        return area 
    
    def draw(self, painter: QPainter): 
        for voronoi_cell in self.voronoi_cells: 
            voronoi_cell.draw(painter, color=Colors.WHITE)
        for vertex in self.vertices: 
            vertex.point.draw(painter)
