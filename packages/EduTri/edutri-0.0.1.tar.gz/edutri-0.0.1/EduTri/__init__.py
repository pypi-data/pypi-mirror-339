from math import sin, radians

class Triangle:
    def __init__(self, sides: list[3],
                 angles: list[3], unit: str):
        self.sides = sides
        self.angles = angles
        self.unit = unit

    def findAngleType(self):
        if self.angles[0] == self.angles[1] == self.angles[2]:
            return "Equiangular"
        for angle in self.angles:
            if angle == 90:
                return "Right"
            elif angle > 90:
                return "Obtuse"
        else:
            return "Acute"

    def findSideType(self):
        if self.sides[0] != self.sides[1] != self.sides[2]:
            return "Scalene"

        if (self.sides[0] == self.sides[1] or
            self.sides[1] == self.sides[2] or
            self.sides[0] == self.sides[2]):
            if self.sides[0] == self.sides[1] == self.sides[2]:
                return "Equilateral"
            else:
                return "Isoceles"

    def findArea(self):
        s = sum(self.sides) / 2
        area = (s * (s - self.sides[0]) * (s - self.sides[1]) * (s - self.sides[2])) ** 0.5

        return (str(area) +
                "sq. " + self.unit)

    def findPerimeter(self):
        return str(sum(self.sides)) + self.unit