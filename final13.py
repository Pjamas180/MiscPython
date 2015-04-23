def lookup(d,k):
    return [ x[1] for x in d if x[0] == k]

def cond(b,t,f):
    if b: return t
    else: return f

def update(d,k,v):
    return [cond(k==x[0],(x[0],v),(x[0],x[1])) for x in d]

def delete(d,k):
    return [(x[0],x[1]) for x in d if x[0] != k]

def add(d,k,v):
    return d+[(k,v)]

def update2(d,k,v):
    rv = []
    for x in d:
        if x[0] == k:
            rv.append((x[0],v))
        else:
            rv.append(x)
    return rv


def rev(l):
    return [l[-i] for i in range(1,len(l)+1)]


def rev2(l):
    def fold_fn(acc,elm): return [elm] + acc
    return reduce(fold_fn,l,[])


def print_some(l):
    def decorator(f):
        def g(*args):
            flag = 0
            for i in l:
                if i == -1:
                    flag = 1
                else:
                    print("Arg " + str(i) + ": " + str(args[i]))
            rv = f(*args)
            if flag == 1:
                print("Return: " + str(rv))
            return rv
        return g
    return decorator

@print_some([-1,1,0])
def plus(x,y):
    print "-- plus called --"
    return x+y
