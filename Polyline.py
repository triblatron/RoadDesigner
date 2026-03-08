from pyglm import glm

class Polyline:
    def __init__(self, num_points: int):
        self.points = [glm.vec3()] * (num_points+1)

    def num_points(self):
        return len(self.points)

    def add_point(self, point):
        self.points.append(point)

    points : list[glm.vec3]