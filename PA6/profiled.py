class profiled:
    def __init__(self,f):
        self.count=0
        self.f=f
        self.__name__=f.__name__
    def __call__(self,*args):
        self.count += 1
        return self.f(*args)

class logged:
    def __init__(self,f):
        self.f = f
    def __call__(self,*args):
        print("Call " + f.__name__ + " arg: " + str(args))
        rv = self.f(*args)
        print("Returns " + str(rv))
        return rv

def logged(f):
    def g(*args):
        print("Call " + f.__name__ + " arg: " + str(args))
        rv = f(*args)
        print("Returns " + str(rv))
        return rv
    g.__name__ = f.__name__
    g.f = f
    return g

def checkargtype(id,type):
    def decorator(f):
        def decorated(*args):
            if not(isinstance(args[id],type)):
                raise Exception("Arg %d (%s) not of type %s" % (id,repr(args[id]),repr(type)))
            return f(*args)
        decorated.__name__ = f.__name__
        return decorated
    return decorator

def test_args(*args,**kwargs):
    if not args:
        print repr(str(args))
    if kwargs != {}:
        print repr(str(kwargs))

@logged
@profiled
def fac(n):
    if n <= 0: return 1
    else: return n*fac(n-1)

