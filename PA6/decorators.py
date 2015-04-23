from misc import Failure

class profiled(object):
    def __init__(self,f):
        self.__count=0
        self.__f=f
        self.__name__=f.__name__
    def __call__(self,*args,**dargs):
        self.__count+=1
        return self.__f(*args,**dargs)
    def count(self):
        return self.__count
    def reset(self):
        self.__count=0

class traced(object):
    """traced decorator class which traces the recursion levels of a function"""
    id_counter = 0
    def __init__(self,f):
        """Initializes the function as a decorator"""
        self.count = 0 # we will eventually use this to print the amount of bars "| "
        self.f = f
        self.__name__= f.__name__
        traced.id_counter = 0

    def __call__(self,*args,**kwargs):
        """Called when the decorator function is called"""
        count = traced.id_counter
        for x in range(count):
            print "|",  # Prints the correct amount of bars
        if len(args) != 0:
            print ",- " + self.__name__ + "(" + ", ".join([str(argu) for argu in args]) + ")" #prints the args
        if len(kwargs.keys()) != 0:
            #prints the kwargs
            print ",- " + self.__name__ + "(" + ", ".join([kw + "=" + str(kwargs[kw]) for kw in kwargs.keys()]) + ")"
        traced.id_counter += 1
        try:
            rv = self.f(*args,**kwargs)
        except Exception as inst:
            traced.id_counter = count
            # Raise an exception like it would normally
            raise inst
        else:
            traced.id_counter -= 1
            # Need to print number of pipes equivalent to original nesting level.
            for x in range(count):
                print "|",
            print "`- " + repr(rv)
            return rv

class memoized(object):
    """memoized decorator class which remembers the value a function with similar arguments returns"""
    def __init__(self,f):
        """Initializes the function as a memoize decorator"""
        # replace this and fill in the rest of the class
        self.__name__= f.__name__
        self.f = f
        self.memoryDict = {} # Used to remember functions that already have been called.

    def __call__(self,*args,**kwargs):
        """Called when the decorator function wrapped with memoized is called"""
        # Creating a string out of the function name to check if we already called it
        if len(args) != 0 and len(kwargs.keys()) != 0:
            funName = self.__name__ + "(" + ", ".join([str(argu) for argu in args]) + ", ".join([kw + "="
            + str(kwargs[kw]) for kw in kwargs.keys()]) + ")"
        elif len(args) != 0:
            funName = self.__name__ + "(" + ", ".join([str(argu) for argu in args]) + ")"
        elif len(kwargs.keys()) != 0:
            funName = self.__name__ + "(" + ", ".join([kw + "=" + str(kwargs[kw]) for kw in kwargs.keys()]) + ")"

        # Seeing if the function was already called, if not, put it into the dictionary
        if funName in self.memoryDict.keys():
            rv = self.memoryDict[funName]
        else:
            rv = self.f(*args,**kwargs)
            self.memoryDict[funName] = rv

        if isinstance(rv,Exception):
            raise rv
        else:
            return rv

# run some examples.  The output from this is in decorators.out
def run_examples():
    for f,a in [(fib_t,(7,)),
                (fib_mt,(7,)),
                (fib_tm,(7,)),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp.reset,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (even_t,(6,)),
                (quicksort_t,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (change_t,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                ]:
        print "RUNNING %s(%s):" % (f.__name__,", ".join([repr(x) for x in a]))
        rv=f(*a)
        print "RETURNED %s" % repr(rv)

@traced
def fib_t(x):
    if x<=1:
        return 1
    else:
        return fib_t(x-1)+fib_t(x-2)

@traced
@memoized
def fib_mt(x):
    if x<=1:
        return 1
    else:
        return fib_mt(x-1)+fib_mt(x-2)

@memoized
@traced
def fib_tm(x):
    if x<=1:
        return 1
    else:
        return fib_tm(x-1)+fib_tm(x-2)

@profiled
@memoized
def fib_mp(x):
    if x<=1:
        return 1
    else:
        return fib_mp(x-1)+fib_mp(x-2)

@traced
def even_t(x):
    if x==0:
        return True
    else:
        return odd_t(x-1)

@traced
def odd_t(x):
    if x==0:
        return False
    else:
        return even_t(x-1)

@traced
def quicksort_t(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_t([x for x in l[1:] if x<pivot])
    right=quicksort_t([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

@traced
@memoized
def quicksort_mt(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_mt([x for x in l[1:] if x<pivot])
    right=quicksort_mt([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

class ChangeException(Exception):
    pass

@traced
def change_t(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_t(l[1:],a)
    else:
        try:
            return [l[0]]+change_t(l,a-l[0])
        except ChangeException:
            return change_t(l[1:],a)

@traced
@memoized
def change_mt(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_mt(l[1:],a)
    else:
        try:
            return [l[0]]+change_mt(l,a-l[0])
        except ChangeException:
            return change_mt(l[1:],a)


