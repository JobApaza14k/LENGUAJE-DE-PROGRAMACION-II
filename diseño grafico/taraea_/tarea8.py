class ConversorTemperatura:
    def __init__(self, f):
        self.f = f

    @classmethod
    def desde_celsius(cls, c):
        return cls(cls.celsius_a_fahrenheit(c))

    @staticmethod
    def celsius_a_fahrenheit(c):
        return c * 9/5 + 32

obj = ConversorTemperatura.desde_celsius(25)
print(obj.f)
