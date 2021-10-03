def better_repr(self):
    return f"I'm a {type(self)}, with vars {vars(self)}"

def better_repr_wrapper(cls):
    cls.__repr__ = better_repr
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)
    return wrapper

@better_repr_wrapper
class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.circumference = 2 * 3.14 * radius

x = Circle(5)
print(x)