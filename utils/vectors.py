from __future__ import annotations

from functools import reduce
import math 
import numpy as np  
    
class Vector: 

    def __init__(self, data: list[float]): 
        if (not data or len(data) < 1): 
            raise ValueError("There must atleast be one value in the vector")

        self.data: list[float] = data
        self.length: int = len(data) 

    def set(self, index: int, value: float): 
        if (index < 0 or index >= self.length): 
            raise ValueError(f"The index must be > 0 and < {self.length}")
        
        self.data[index] = value
    
    def get(self, index: int) -> float: 
        if (index < 0 or index >= self.length): 
            raise ValueError(f"The index must be > 0 and < {self.length}")

        return self.data[index]
    
    def x(self): 
        return self.data[0] 
    
    def y(self): 
        return self.data[1]

    def get_data(self) -> list[float]:
        return self.data
    
    def copy(self) -> Vector: 
        return Vector(self.get_data())
    
    def add(self, other: Vector):
        self.check_length_error(len(other))
        for i in range(self.length): 
            self.data[i] += other.data[i] 
    
    def sub(self, other: Vector):
        self.check_length_error(len(other))
        for i in range(self.length): 
            self.data[i] -= other.data[i] 
    
    def mul(self, other: Vector):
        self.check_length_error(len(other))
        for i in range(self.length): 
            self.data[i] *= other.data[i] 
    
    def scale(self, number: float): 
        for i in range(self.length): 
            self.data[i] *= number 
    
    def get_scaled(self, number: float) -> Vector: 
        scaled: Vector = self.copy()
        scaled.scale(number)
        return scaled

    def normalize(self):
        self.scale(1 / self.magnitude())

    def get_normalized(self) -> Vector: 
        normalized: Vector = self.copy() 
        normalized.scale(1 / self.magnitude())
        return normalized
    
    def dot_product(self, other: Vector) -> float: 
        self.check_length_error(len(other))
        dp = 0 
        for i in range(self.length): 
            dp += self.data[i] * other.data[i]
        return dp 
    
    def magnitude(self) -> float: 
        # does not work correctly for sum reason??? 
        # sum1 = reduce(lambda acc, number: acc + (number * number), self.data)
        sum_of_squares = 0 
        for i in range(self.length): 
            sum_of_squares += self.data[i] * self.data[i]
        return math.sqrt(sum_of_squares)
    
    def L1_length(self) -> float: 
        return reduce(lambda acc, number: acc + number, self.data)
    
    def __abs__(self) -> float: 
        return self.magnitude()
    
    def __add__(self, other: Vector) -> Vector: 
        self.check_length_error(len(other))
        return Vector([self.data[i] + other.data[i] for i in range(self.length)])
    
    def __sub__(self, other: Vector) -> Vector: 
        self.check_length_error(len(other))
        return Vector([self.data[i] - other.data[i] for i in range(self.length)])
    
    def __mul__(self, other: Vector) -> Vector: 
        self.check_length_error(len(other))
        return Vector([self.data[i] * other.data[i] for i in range(self.length)])
    
    def __eq__(self, other: Vector) -> bool: 
        self.check_length_error(len(other))
        for i in range(self.length): 
            if self.data[i] != other.data[i]: 
                return False 
        return True  
    
    def __ne__(self, other: Vector) -> bool: 
        return not self == other
    
    def __lt__(self, other: Vector) -> bool: 
        self.check_length_error(len(other))
        for i in range(self.length): 
            if self.data[i] >= other.data[i]: 
                return False 
        return True 

    def __le__(self, other: Vector) -> bool: 
        return self == other or self < other
    
    def __gt__(self, other: Vector) -> bool: 
        self.check_length_error(len(other))
        for i in range(self.length): 
            if self.data[i] <= other.data[i]: 
                return False 
        return True 

    def __ge__(self, other: Vector) -> bool: 
        return self == other or self > other 
    
    def __len__(self) -> int: 
        return self.length

    def __repr__(self) -> str:
        return f'{self.data}'
    
    def __str__(self) -> str:
        return f'{self.data}'
    
    def check_length_error(self, other_length: int): 
        if (self.length != other_length): 
            raise ValueError(f"Both vectors must be of the same length")

    
class Matrix: 

    def __init__(self, data: list[Vector]): 

        if (not all([len(row) == len(data[0]) for row in data])): 
            raise ValueError("All rows must have the same number as columns") 
        
        self.rows = len(data)
        self.cols = len(data[0])
        self.data: list[Vector] = data
        self.data_t: list[Vector] = [Vector(list(column)) for column in zip(*[row.get_data() for row in data])]

    @classmethod
    def from_list(cls, data: list[list[float]]): 
        return cls([Vector(row) for row in data])
    
    @classmethod
    def zero(cls, rows: int, cols: int): 
        return cls([Vector([0] * cols) for _ in range(rows)])
    
    def get_data(self) -> list[list[float]]: 
        return [row.get_data() for row in self.data]
        
    def get(self, row: int, col: int) -> float: 
        self.raise_col_error()
        self.raise_row_error()
        return self.data[row].get(col)
    
    def get_row(self, row: int) -> Vector: 
        self.raise_row_error()
        return self.data[row]
    
    def get_col(self, col: int) -> Vector: 
        self.raise_col_error()
        return self.data_t[col]
    
    def set(self, row: int, col: int, value: float): 
        self.raise_col_error()
        self.raise_row_error()
        self.data[row].set(col, value)
    
    def transpose(self) -> Matrix: 
        return Matrix(self.data_t)
    
    def determinant(self) -> float: 
        if self.rows != self.cols: 
            raise ValueError("Rows should be equal to the columns to take a determinant")
        
        if (self.rows == 2): 
            return (self.data[0].get(0) * self.data[1].get(1)) - (self.data[0].get(1) * self.data[1].get(0))

        return np.linalg.det([row.get_data() for row in self.data]) 

    def __abs__(self) -> float: 
        pass
    
    def __add__(self, other: Matrix) -> Matrix: 
        self.raise_same_size(other)
        new_data = [self.data[i] + self.data[i] for i in range(self.rows)]
        return Matrix(new_data) 
    
    def __sub__(self, other: Matrix) -> Matrix: 
        self.raise_same_size(other)
        new_data = [self.data[i] - self.data[i] for i in range(self.rows)]
        return Matrix(new_data)
    
    def __mul__(self, other: Matrix) -> Matrix: 
        self.raise_same_size(other)
        new_data = [self.data[i] * self.data[i] for i in range(self.rows)]
        return Matrix(new_data)
    
    def __eq__(self, other: Matrix) -> bool: 
        for i in range(self.rows): 
            if self.data[i] != other.data[i]: 
                return False 
        else: 
            return True 
    
    def __ne__(self, other: Matrix) -> bool: 
        return not self == other
    
    def __len__(self) -> int: 
        return self.rows

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        output = '\n'
        for row in range(self.rows): 
            output += str(self.data[row])
            output += '\n'
        return output

    def raise_row_error(self, row: int): 
        if (row < 0 or row >= self.rows): 
            raise ValueError(f"The row index must be > 0 and < {self.rows}") 

    def raise_col_error(self, col: int): 
        if (col < 0 or col >= self.cols): 
            raise ValueError(f"The column index must be > 0 and < {self.cols}") 
        
    def raise_same_size(self, other: Matrix): 
        if (self.cols != other.cols): 
            raise ValueError(f"The matrices don't have the same amount of columns")
        if (self.rows != other.rows):  
            raise ValueError(f"The matrices don't have the same amount of rows")

    


    
