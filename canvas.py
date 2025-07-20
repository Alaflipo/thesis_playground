from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter, QColor, QPen, QMouseEvent, QWheelEvent
from PySide6.QtCore import Qt, QSize
import random

from utils.shapes import Line, Point, Rectangle
import utils.colors as Color

class Canvas(QWidget): 

    def __init__(self, size: QSize, draw_axis = True): 
        super().__init__()

        self.size: QSize = size 
        self.pixmap = QPixmap(size) 
        self.pixmap.fill(QColor('white'))

        self.pan_offset: Point = Point(0, 0)
        self.last_mouse_pos: Point | None = None
        self.zoom: float = 1.0

        self.draw_axis: bool = draw_axis
        self.x_axis: Line = Line(Point(-1, 0), Point(1, 0))
        self.y_axis: Line = Line(Point(0, -1), Point(0, 1))

        self.create_viewbox()
        # For each scene this can be edited
        self.set_up_scene()
    
    def set_up_scene(self): 
        pass 

    def render_scene(self, painter: QPainter): 
        pass 

    def create_viewbox(self): 
        # We calculate the bounds of the viewbox after transformation to world coordinates
        # Convert screen pixels to world units using zoom
        half_width = self.size.width() / (2 * self.zoom)
        half_height = self.size.height() / (2 * self.zoom)

        # In world coordinates, pan_offset moves the center
        center_x = -1 * self.pan_offset.x() / self.zoom
        center_y = self.pan_offset.y() / self.zoom  # flipped because y-axis is scaled by -zoom

        left_x = center_x - half_width
        right_x = center_x + half_width
        bottom_y = center_y - half_height
        top_y = center_y + half_height

        points = [Point(left_x, top_y), Point(right_x, top_y), Point(right_x, bottom_y), Point(left_x, bottom_y)]
        self.view_box = Rectangle(points)
    
    def to_view_coordinates(self, painter: QPainter): 
        # Translate to center plus the current pan offset
        new_center = Point(self.size.width() / 2, self.size.height() / 2) + self.pan_offset
        painter.translate(new_center.x(), new_center.y())
        # Flip y-axis 
        painter.scale(self.zoom, -self.zoom)

    def draw_axis_lines(self, painter: QPainter):    
        self.x_axis.draw_inf(painter, self.view_box, thickness=1, color=Color.GREY, pen_style=Qt.PenStyle.DashLine)
        self.y_axis.draw_inf(painter, self.view_box, thickness=1, color=Color.GREY, pen_style=Qt.PenStyle.DashLine)

    def render(self): 
        self.pixmap.fill(QColor('white'))
        painter = QPainter(self.pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Transform from world to view coordinates (based on current panning and zooming info)
        self.to_view_coordinates(painter)
        self.create_viewbox()
        
        # Draw the x and y axis 
        if self.draw_axis: 
            self.draw_axis_lines(painter)

        # Draw the current scene 
        self.render_scene(painter)

        # Triggers the PaintEvent 
        self.update()

    def wheelEvent(self, event: QWheelEvent):
        # Zoom toward mouse position
        angle = event.angleDelta().y()
        zoom_factor = 1.01 if angle > 0 else 0.99

        # Update zoom
        self.zoom *= zoom_factor
        # Clamp the zoom such that it can not go forever small or large
        self.zoom = max(0.1, min(self.zoom, 10.0))

        self.render()

    def paintEvent(self, event):
        painter = QPainter(self)
        # We draw the pixmap onto the QWidget canvas 
        painter.drawPixmap(0, 0, self.pixmap)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = Point(event.position())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos is not None:
            current_pos: Point = Point(event.position())
            delta: Point = current_pos - self.last_mouse_pos
            self.pan_offset += delta
            self.last_mouse_pos = current_pos
            self.render()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
