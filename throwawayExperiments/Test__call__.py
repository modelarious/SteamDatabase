class Hello:
    def __init__(self, a):
        self.a = a

    def print_something(self, text):
        print(self.a + text)

h = Hello('hola')
# class_method = getattr(Hello, "print_something")
# result = class_method(h, 'hi')



instance_method = getattr(h, 'print_something')
result = instance_method('hi')