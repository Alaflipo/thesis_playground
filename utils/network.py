from __future__ import annotations

import random
from PySide6.QtGui import QPainter, QPen, QColor, Qt, QBrush, QPolygonF
from PySide6.QtCore import Qt, QPointF

from utils.shapes import Point, Line, ComplexPolygon, HalfPlane
from utils.geometry import half_plane_intersection
import utils.colors as Colors


class Vertex: 

    def __init__(self, point: Point, label: int = 0):
        self.label: int = label
        self.point: Point = point
        self.edges: list[Edge] = []

        self.radius = 2
    
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
        self.create_voronoi_cells_2()
    
    def create_voronoi_cells(self): 
        self.voronoi_cells: list[ComplexPolygon] = []
        # sorted_vertices = sorted(vertices, key=lambda vertex: vertex.point.angle())
        for i, vertex in enumerate(self.vertices): 
            others = self.vertices[:i] + self.vertices[i+1:]

            bisectors = [vertex.point.bi_sector(other.point) for other in others]
            half_planes = [HalfPlane(bisector, vertex.point - bisector.start) for bisector in bisectors]
            voronoi_cell: ComplexPolygon = half_plane_intersection(half_planes)
            self.voronoi_cells.append(voronoi_cell)

    def create_voronoi_cells_2(self): 
        self.vc = [VoronoiCell(vertex) for vertex in self.vertices]
        for i, cell in enumerate(self.vc): 
            others = self.vc[:i] + self.vc[i+1:]
            cell.generate_cell(others)

    def half_plane_intersection(self, half_planes: list[HalfPlane]) -> ComplexPolygon: 
        area: ComplexPolygon = ComplexPolygon([Point(-1000, 1000), Point(1000,1000), Point(1000,-1000), Point(-1000, -1000)]) 

        for i, half_plane in enumerate(half_planes): 
            area = area.clip_with_halfplane(half_plane)
        return area 
    
    def draw(self, painter: QPainter): 
        for voronoi_cell in self.vc: 
            voronoi_cell.draw(painter, color=Colors.WHITE)
        for vertex in self.vertices: 
            vertex.point.draw(painter)
        # for voronoi_cell in self.voronoi_cells: 
        #     voronoi_cell.draw(painter, color=Colors.WHITE)
        # for vertex in self.vertices: 
        #     vertex.point.draw(painter)

class VoronoiEdge:

    def __init__(self, c1: VoronoiCell, c2: VoronoiCell):
        self.cell1: Vertex = c1 
        self.cell2: Vertex = c2 
        bisector: Line = c1.vertex.point.bi_sector(c2.vertex.point) 
        self.halfplane: HalfPlane = HalfPlane(bisector, c1.vertex.point - bisector.start)

    def intersects(self, line: Line) -> Point | None: 
        return self.halfplane.line.intersects(line)
    
    def contains_with_tol(self, point: Point) -> bool: 
        return self.halfplane.line.contains_with_tol(point)
    
    def get_end(self) -> Point: 
        return self.halfplane.line.end
    
    def set_start(self, start: Point):
        self.halfplane.line.start = start
    
    def set_end(self, end: Point): 
        self.halfplane.line.end = end 

class VoronoiCell: 

    def __init__(self, vertex: Vertex):
        self.vertex: Vertex = vertex
        self.hull: list[Point] = [Point(-1000, 1000), Point(1000,1000), Point(1000,-1000), Point(-1000, -1000)]
        self.edges: list[VoronoiEdge | Line] = [Line(self.hull[i], self.hull[(i+1) % len(self.hull)]) for i in range(len(self.hull))]

        self.QPolygon: QPolygonF = QPolygonF([QPointF(point.x(), point.y()) for point in self.hull]) 

    def generate_cell(self, others: list[VoronoiCell]): 
        possible_edges = [VoronoiEdge(self, other) for other in others]

        for edge in possible_edges: 
            
            self.clip_with_vornoi_edge(edge)
            print(self.edges)
        
        self.hull = [edge.get_end() for edge in self.edges]
        self.QPolygon = QPolygonF([QPointF(point.x(), point.y()) for point in self.hull]) 
    
    def clip_with_vornoi_edge(self, ve: VoronoiEdge): 
        intersections: list[Point] = []
        intersections_i: list[int] = []

        # loop trough all edges and see if there is an intersection of the polygon with the half plane
        # self.edges here contains a combination of Lines and Voronoiedges
        for i, edge in enumerate(self.edges): 
            intersection: Point = edge.intersects(ve.halfplane.line)
            # we also ensure that we can not add the same end point twice (if it by coincidence goes trough a line endpoint)
            if intersection and edge.contains_with_tol(intersection) and not (intersection in intersections):
                intersections_i.append(i)
                intersections.append(intersection)
        
        # if there are intersections there must be 2 (property of polygon being convex)
        if len(intersections) == 2: 
            i1 = intersections_i[0]
            i2 = intersections_i[1]
            # split them up in two parts 
            first_part: list[VoronoiEdge | Line] = self.edges[i1 + 1: i2]
            second_part: list[VoronoiEdge | Line] = self.edges[i2 + 1:] + self.edges[:i1]
            # check which side of the polygon is contained in the polygon (both line and ve have the get_end command)
            if ve.halfplane.contains(self.edges[i1].get_end()): 
                self.edges[i1].set_start(intersections[0])
                self.edges[i2].set_end(intersections[1])
                ve.set_start(intersections[1])
                ve.set_end(intersections[0])
                self.edges = [ve, self.edges[i1]] + first_part + [self.edges[i2]]
            else: 
                self.edges[i2].set_start(intersections[1])
                self.edges[i1].set_end(intersections[0])
                ve.set_start(intersections[0])
                ve.set_end(intersections[1])
                self.edges = [ve, self.edges[i2]] + second_part + [self.edges[i1]]

    def draw(self, painter: QPainter, color: QColor = Colors.MAROON): 
        # for the inside
        brush = QBrush(color)
        painter.setBrush(brush)

        # for the outline
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Colors.GREY)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        painter.drawPolygon(self.QPolygon)
