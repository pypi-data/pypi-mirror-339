import unittest

from footprint_facility.footprint_facility import _inside


class TestIsInside(unittest.TestCase):
    def test_point_inside_polygon(self):
        polygon = [(0, 0), (5, 0), (5, 5), (0, 5)]  # Square with coordinates (0,0), (5,0), (5,5), (0,5)
        point = (3, 3)  # Point to test
        self.assertTrue(_inside(polygon, point))  # The point should be inside

    def test_point_outside_polygon(self):
        polygon = [(0, 0), (5, 0), (5, 5), (0, 5)]  # Square with coordinates (0,0), (5,0), (5,5), (0,5)
        point = (6, 3)  # Point to test
        self.assertFalse(_inside(polygon, point))  # The point should be outside

    def test_point_on_polygon_edge(self):
        polygon = [(0, 0), (5, 0), (5, 5), (0, 5)]  # Square with coordinates (0,0), (5,0), (5,5), (0,5)
        point = (5, 2)  # Point on the right edge of the square
        self.assertTrue(_inside(polygon, point))  # Point on an edge is considered inside

    def test_point_on_polygon_vertex(self):
        polygon = [(0, 0), (5, 0), (5, 5), (0, 5)]  # Square with coordinates (0,0), (5,0), (5,5), (0,5)
        point = (0, 0)  # Point on the polygon vertex
        self.assertTrue(_inside(polygon, point))  # Point on a vertex is considered inside

    def test_point_in_complex_polygon(self):
        polygon = [(0, 0), (2, 3), (4, 0), (3, -3), (1, -3)]  # Concave polygon
        point = (2, 0)  # Point to test
        self.assertTrue(_inside(polygon, point))  # The point is inside

    def test_point_in_complex_polygon_outside(self):
        polygon = [(0, 0), (2, 3), (4, 0), (3, -3), (1, -3)]  # Concave polygon
        point = (4, 3)  # Point to test
        self.assertFalse(_inside(polygon, point))  # The point is outside

    def test_point_on_polygon_ring(self):
        polygon = [(0, 0), (5, 0), (5, 5), (0, 5)]  # Square with coordinates (0,0), (5,0), (5,5), (0,5)
        point = (2, 5)  # Point on the top edge of the square
        self.assertTrue(_inside(polygon, point))  # Point on an edge is inside


if __name__ == "__main__":
    unittest.main()
