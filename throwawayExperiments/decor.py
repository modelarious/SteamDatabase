def sayPhraseDecor(phrase):
    def sayHelloDecor(func):
        def inner(param2):
            func( phrase + ' ' + param2)
        return inner
    return sayHelloDecor

@sayPhraseDecor('hello')
def print_name(name):
    print(name)

print_name('mark')
