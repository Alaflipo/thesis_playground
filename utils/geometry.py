from utils.shapes import HalfPlane, ComplexPolygon, Point

def half_plane_intersection(half_planes: list[HalfPlane]) -> ComplexPolygon: 
    area: ComplexPolygon = ComplexPolygon([Point(-1000, 1000), Point(1000,1000), Point(1000,-1000), Point(-1000, -1000)]) 

    for i, half_plane in enumerate(half_planes): 
        area = area.clip_with_halfplane(half_plane)
    return area 
