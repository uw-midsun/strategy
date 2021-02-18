import math


class Vector:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))

    # Cross product (@)
    def __matmul__(self, other):
        return Vector((self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x))

    # Dot product (*)
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Scalar multiply (put scalar on left)
    def __rmul__(self, other):
        return Vector((self.x * other, self.y * other, self.z * other))

    def print(self):
        print("({0}, {1}, {2})".format(self.x, self.y, self.z))

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def project_onto(self, rhs):
        return (self * rhs)/(rhs.magnitude() ** 2) * rhs

    def is_parallel(self, other):
        return (self * self) * (other * other) - (self * other) * (self * other) == 0


class Plane:
    def __init__(self, point: Vector, normal: Vector):
        self.pt = point
        self.normal = normal

    # Project a point (as a vector) onto the plane
    def project(self, point: Vector):
        plane_to_point = point - self.pt
        projection = plane_to_point.project_onto(self.normal)
        return point - projection


def area(point1: Vector, point2: Vector, point3: Vector, point4: Vector):
    vec_1_2 = point2 - point1
    vec_1_4 = point4 - point1
    vec_3_2 = point2 - point3
    vec_3_4 = point4 - point3

    return ((vec_1_2 @ vec_1_4).magnitude() + (vec_3_2 @ vec_3_4).magnitude()) / 2


if __name__ == "__main__":
    plane = Plane(Vector((500, 500, 500)), Vector((1, 1, 1)))
    point1 = plane.project(Vector((0, 0, 0)))
    point2 = plane.project(Vector((0, 2, 0)))
    point3 = plane.project(Vector((1, 2, 0)))
    point4 = plane.project(Vector((1, 0, 0)))

    print(area(point1, point2, point3, point4))
