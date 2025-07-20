import unittest
import math 

from vectors import Vector, Matrix 

class TestVector(unittest.TestCase):

    def test_create_vector(self): 
        v1 = Vector([1, 2, 3])
        self.assertListEqual([1, 2, 3], v1.get_data())
        self.assertEqual(3, len(v1))

    def test_set_vector(self): 
        v1 = Vector([1, 2, 3])
        self.assertEqual(v1.get(1), 2)
        v1.set(1, 5)
        self.assertEqual(v1.get(1), 5)
        self.assertNotEqual(v1.get(1), 2)

    def test_dot_product(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        self.assertEqual(32, v1.dot_product(v2))

    def test_magnitude(self): 
        v1 = Vector([1, 2, 3])
        self.assertEqual(math.sqrt(14), v1.magnitude())
        self.assertEqual(math.sqrt(14), abs(v1))

    def test_L1_length(self): 
        v1 = Vector([1, 2, 3])
        self.assertEqual(6, v1.L1_length())

    def test_eq(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 3])
        self.assertEqual(v1, v2)

    def test_neq(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 4])
        self.assertNotEqual(v1, v2)

    def test_add(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        self.assertEqual(Vector([5, 7, 9]), v1 + v2)
        v1.add(v2)
        self.assertEqual(Vector([5, 7, 9]), v1)

    def test_sub(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        self.assertEqual(Vector([-3, -3, -3]), v1 - v2)
        v1.sub(v2)
        self.assertEqual(Vector([-3, -3, -3]), v1)

    def test_mul(self): 
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        self.assertEqual(Vector([4, 10, 18]), v1 * v2)
        v1.mul(v2)
        self.assertEqual(Vector([4, 10, 18]), v1)

    def test_scale(self): 
        v1 = Vector([1, 2, 3])
        scale_factor = 4
        self.assertEqual(Vector([1, 2, 3]), v1)
        v1.scale(scale_factor)
        self.assertEqual(Vector([4, 8, 12]), v1)

    def test_value_error(self): 
        v1 = Vector([1, 2, 3]) 
        v2 = Vector([1, 2, 3, 4])
        with self.assertRaises(ValueError): 
            v1.set(3, 12)
        with self.assertRaises(ValueError): 
            v1 == v2 
        with self.assertRaises(ValueError): 
            v1 != v2 
        with self.assertRaises(ValueError): 
            v3 = v1 + v2 
        with self.assertRaises(ValueError): 
            v3 = v1 - v2
        with self.assertRaises(ValueError): 
            v3 = v1 * v2
        with self.assertRaises(ValueError): 
            dp = v1.dot_product(v2)

    def test_create_matrix(self): 
        m0 = Matrix.zero(2, 2)
        self.assertEqual(Matrix([Vector([0, 0]), Vector([0, 0])]), m0)

    def test_determinant(self): 
        m1 = Matrix([Vector([4, 0]), Vector([0, 2])])
        self.assertEqual(8, m1.determinant())
    

if __name__ == '__main__':
    unittest.main()
