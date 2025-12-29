class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Vector2D(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector2D(self.x - o.x, self.y - o.y)

    def __mul__(self, escalar):
        return Vector2D(self.x * escalar, self.y * escalar)

v1 = Vector2D(2, 3)
v2 = Vector2D(1, 1)
v3 = v1 + v2
v4 = v1 - v2
v5 = v1 * 3

print(v3.x, v3.y)
print(v4.x, v4.y)
print(v5.x, v5.y)
