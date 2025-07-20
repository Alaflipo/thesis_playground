from __future__ import annotations

from typing import overload

import math 
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF
from PySide6.QtCore import Qt, QPointF
from utils.vectors import Vector
import utils.colors as Colors 

class Point(Vector): 

    @overload
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None: ...
    
    @overload
    def __init__(self, qpoint: QPointF) -> None: ...

    @overload 
    def __init__(self, vector: Vector) -> None: ...

    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], QPointF)): 
            super().__init__([args[0].x(), args[0].y()])
        elif (len(args) == 1 and isinstance(args[0], Vector)): 
            super().__init__([args[0].data[0], args[0].data[1]])
        elif (len(args) == 2 and isinstance(args[0], (float, int)) and isinstance(args[1], (float, int))): 
            super().__init__([args[0], args[1]])
        else: 
            raise TypeError("Invalid arguments for Point")
            
    @classmethod
    def from_Q(cls, qpoint: QPointF): 
        return cls(qpoint.x(), qpoint.y())

    def bi_sector(self, other: Point) -> Line: 
        connection: Line = Line(self, other)
        midpoint: Point = connection.get_midpoint()
        secondpoint: Point = midpoint + connection.normal
        return Line(midpoint, secondpoint)

    def angle(self) -> float: 
        return math.atan2(self.y(), self.x())
    
    def draw(self, painter: QPainter): 
        radius = 3
        painter.setBrush(QBrush(Colors.MAROON))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(self.x() - radius, self.y() - radius, 2 * radius, 2 * radius)

    def __add__(self, other: Point) -> Point: 
        self.check_length_error(len(other))
        return Point(self.x() + other.x(), self.y() + other.y())
    
    def __sub__(self, other: Point) -> Point: 
        self.check_length_error(len(other))
        return Point(self.x() - other.x(), self.y() - other.y())
    
    def __mul__(self, other: Point) -> Point: 
        self.check_length_error(len(other))
        return Point(self.x() * other.x(), self.y() * other.y())
    
    def __repr__(self) -> str:
        return f'Point({self.x()}, {self.y()})'
    
    def __str__(self) -> str:
        return f'Point({self.x()}, {self.y()})'
    
    def __hash__(self):
        return hash((self.x, self.y))


class Line:
    def __init__(self, start: Point, end: Point):
        self.start: Point = start
        self.end: Point = end

        # direction
        self.direction: Vector = self.end - self.start
        self.normal: Vector = Point(-1 * self.direction.y(), self.direction.x())

        # representation as ax + by = c 
        self.a: float = end.y() - start.y()
        self.b: float = start.x() - end.x()
        self.c: float = (self.a * start.x()) + (self.b * start.y())

    def get_direction(self) -> Point:
        return self.direction

    def length(self) -> float:
        return self.direction.magnitude()
    
    def slope(self) -> float: 
        if self.direction.x() == 0: 
            return math.inf 
        return self.direction.x() / self.direction.y()
    
    def witihin_bound(self, point: Point): 
        # This assumes that we know the point already is on the infinite line 
        return point.x() >= min(self.start.x(), self.end.x()) and point.x() <= max(self.start.x(), self.end.x()) 
    
    def contains(self, point: Point) -> bool: 
        on_line: bool = self.a * point.x() + self.b * point.y() == self.c 
        within_bounds: bool = point >= self.start and point <= self.end 
        return on_line and within_bounds
    
    def contains_with_tol(self, point: Point, tol: float = 1e-9) -> bool: 
        correct_equation = self.a * point.x() + self.b * point.y()
        on_line = abs(correct_equation - self.c) < tol

        x_min = min(self.start.x(), self.end.x())
        x_max = max(self.start.x(), self.end.x())
        y_min = min(self.start.y(), self.end.y())
        y_max = max(self.start.y(), self.end.y())

        within_bounds = (x_min - tol <= point.x() <= x_max + tol and y_min - tol <= point.y() <= y_max + tol)
        return on_line and within_bounds
    
    def intersects(self, other: Line):
        # Here we handle both lines as being infinite
        det = self.a * other.b - other.a * self.b

        # Lines are parallel or coincident
        if abs(det) < 1e-9:
            return None  

        # Solve using Cramer's Rule
        x = (self.c * other.b - other.c * self.b) / det
        y = (self.a * other.c - other.a * self.c) / det

        return Point(x,y)

    def intersects_hor(self, line: Line) -> Point | None: 
        # We assume that line is horizontal
        if (abs(line.start.y() - line.end.y()) >= 1e-9):
            raise ValueError("The line is not horizontal!")  
        
        y = line.start.y()
        # self is a vertical line
        if (abs(self.b) < 1e-9): 
            return Point(self.c / self.a, y)
        
        if (abs(self.a) < 1e-9): 
            # lines are parralel 
            return None
        
        # calculate intersection at x 
        x = (self.c - self.b * y) / self.a

        # check if x is within the bounds 
        if (min(line.start.x(), line.end.x()) <= x <= max(line.start.x(), line.end.x())): 
            return Point(x,y)
        else: 
            None 

    def intersects_ver(self, line: Line): 
        # We assume that line is vertical 
        if (abs(line.start.x() - line.end.x()) >= 1e-9):
            raise ValueError("The line is not vertical!")  
        
        x = line.start.x()
        # self is a horizontal line
        if (abs(self.a) < 1e-9): 
            return Point(x, self.c / self.b)
        
        if (abs(self.b) < 1e-9): 
            # lines are parralel 
            return None
        
        # calculate intersection at y
        y = (self.c - self.a * x) / self.b 

        # check if y is within the bounds 
        if (min(line.start.y(), line.end.y()) <= y <= max(line.start.y(), line.end.y())): 
            return Point(x,y)
        else: 
            None 
    
    def clip_by_rect(self, rect: Rectangle) -> Line | None: 
        # rect contains up, down, left, right
        points = []
        for i, line in enumerate(rect.sides): 
            intersection: Point | None = None
            if i < 2: 
                intersection = self.intersects_hor(line)
            else: 
                intersection = self.intersects_ver(line)
            if intersection: 
                points.append(intersection)
        if len(points) >= 2: 
            return Line(points[0], points[1])
        else: 
            return None 

    def get_normal(self) -> Vector:
        return self.normal 
    
    def get_midpoint(self) -> Point: 
        midpoint: Point = self.start + self.end
        midpoint.scale(0.5)
        return midpoint
    
    def draw_arrow_head(self, painter: QPainter, size=3): 
        arrow_width: Point = self.normal.get_normalized()
        arrow_width.scale(size)
        bend_dir: Point = self.direction.get_normalized()
        bend_dir.scale(size)

        end_point_left: Point = (self.end + arrow_width)
        end_point_left.sub(bend_dir)
        end_point_right: Point = (self.end - arrow_width)
        end_point_right.sub(bend_dir)

        left = Line(self.end, end_point_left)
        right = Line(self.end, end_point_right)

        painter.drawLine(left.start.x(), left.start.y(), left.end.x(), left.end.y())
        painter.drawLine(right.start.x(), right.start.y(), right.end.x(), right.end.y())

    def draw(self, painter: QPainter, 
             thickness: float = 2, 
             color: QColor = Colors.TEAL, 
             pen_style: Qt.PenStyle = Qt.PenStyle.SolidLine, 
             cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
             arrow_head: bool = False
        ): 
        pen = QPen()
        pen.setWidth(thickness)
        pen.setColor(color)
        pen.setStyle(pen_style)
        pen.setCapStyle(cap_style)
        painter.setPen(pen)

        painter.drawLine(self.start.x(), self.start.y(), self.end.x(), self.end.y())
        if arrow_head: 
            self.draw_arrow_head(painter)

    def draw_inf(self, painter: QPainter, view_box: Rectangle,
             thickness: int = 2, 
             color: QColor = Colors.TEAL, 
             pen_style: Qt.PenStyle = Qt.PenStyle.SolidLine, 
             cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap
        ): 
        pen = QPen()
        pen.setWidth(thickness)
        pen.setColor(color)
        pen.setStyle(pen_style)
        pen.setCapStyle(cap_style)
        painter.setPen(pen)

        inf_line: Line| None = self.clip_by_rect(view_box)
        if inf_line: 
            painter.drawLine(inf_line.start.x(), inf_line.start.y(), inf_line.end.x(), inf_line.end.y()) 

    def __eq__(self, other: Line) -> bool:
        return self.start == other.start and self.end == other.end

    def __repr__(self) -> str:
        return f'Line({self.start}, {self.end})'

    def __str__(self) -> str:
        return f'Line from {self.start} to {self.end}'

class Rectangle: 

    @overload
    def __init__(self, top: Line, bottom: Line, left: Line, right: Line) -> None: ...
    
    @overload
    def __init__(self, points: list[Point]) -> None: ...

    def __init__(self, *args):
        if len(args) == 4 and all(isinstance(arg, Line) for arg in args):
            self.top: Line = args[0]
            self.bottom: Line = args[1] 
            self.left: Line = args[2] 
            self.right: Line = args[3] 
            self.sides: list[Line] = [self.top, self.bottom, self.left, self.right]
        elif len(args) == 1 and isinstance(args[0], list): 
            self.points: list[Point] = args[0]
            self.top: Line = Line(self.points[0], self.points[1])
            self.right: Line = Line(self.points[1], self.points[2])
            self.bottom: Line = Line(self.points[2], self.points[3])
            self.left: Line = Line(self.points[3], self.points[0])
            self.sides: list[Line] = [self.top, self.bottom, self.left, self.right]
        else: 
            raise TypeError("Invalid arguments for Point")
    
    def draw(self, painter: QPainter): 
        for side in self.sides: 
            side.draw(painter)

class HalfPlane: 

    def __init__(self, line: Line, normal: Point):
        self.line: Line = line
        self.normal: Point = normal

    def contains(self, point: Point): 
        delta = point - self.line.start
        return delta.dot_product(self.normal) >= 0 
    
    def draw(self, painter: QPainter, view_box: Rectangle): 
        normal_line: Line = Line(self.line.end, self.line.end + self.normal.get_normalized().get_scaled(10))
        normal_line.draw(painter, thickness=2, color=Colors.MAROON, pen_style=Qt.PenStyle.DashLine, arrow_head=True)
        self.line.draw_inf(painter, view_box)

class ComplexPolygon: 

    def __init__(self, hull: list[Point]):
        if len(hull) < 3:
            raise ValueError("Polygon shell must have at least 3 points.")
        self.hull: list[Point] = hull
        self.size: int = len(hull)
        self.edges: list[Line] = []

        for i in range(self.size): 
            self.edges.append(Line(self.hull[i], self.hull[(i+1) % self.size]))

        self.QPolygon: QPolygonF = QPolygonF([QPointF(point.x(), point.y()) for point in self.hull]) 

    def clip_with_halfplane(self, halfplane: HalfPlane) -> ComplexPolygon: 
        # A few assumptions I will make:
        # 1. The polygon is convex
        # 2. The list of edges (or points) is defined as clockwise in my polygon
        intersections: list[Point] = []
        intersections_i: list[int] = []
        new_hull: list[Point] = []

        # loop trough all edges and see if there is an intersection with the half plane
        for i, edge in enumerate(self.edges): 
            intersection: Point = edge.intersects(halfplane.line)
            if intersection and edge.contains_with_tol(intersection) and not (intersection in intersections):
                intersections_i.append(i)
                intersections.append(intersection)
        
        # if there are intersections there must be 2 (property of polygon being convex)
        if len(intersections) == 2: 
            # split them up in two parts 
            first_part: list[Point] = self.hull[intersections_i[0] + 1: intersections_i[1] + 1]
            second_part: list[Point] = self.hull[intersections_i[1] + 1:] + self.hull[:intersections_i[0] + 1]
            # check which side of the polygon is contained in the polygon
            if halfplane.contains(second_part[0]): 
                new_hull =  [intersections[1]] + second_part + [intersections[0]]
            else: 
                new_hull = [intersections[0]] + first_part + [intersections[1]]
        else: # there is no intersection with the polygon 
            return self 
        return ComplexPolygon(new_hull)
    
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

    def __str__(self): 
        return f'{self.hull}'


