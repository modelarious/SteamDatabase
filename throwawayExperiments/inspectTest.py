import inspect
class X:
    def _determine_function_name(self):
        return inspect.stack()[1][3]

    def do_the_dance(self):
        queueName = self._determine_function_name()
    
    def im_a_silly_little_man(self):
        queueName = self._determine_function_name()
        

        
class Introspect:
    def __init__(self, memberobject):
        self.memberobject = memberobject
    
    def call_member_object_func(self):
        print(self.memberobject.do_the_dance())
        print(self.memberobject.im_a_silly_little_man())

v = X()
introspect = Introspect(v)
introspect.call_member_object_func()
