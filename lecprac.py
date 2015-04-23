

def in_range(i,range):
    def decorator(f):
        def g(*args):
            if (i != -1):
                ith = args[i]
                if (ith < range[0]):
                    raise Exception(str(i) + "th arg " + str(ith) + "is too small")
                elif (ith > range[1]):
                    raise Exception(str(i) + "th arg " + str(ith) + "is too big")

            rv = f(*args)
            if (i == -1):
                if (rv < range[0]):
                    raise Exception("Return value " + str(rv) + "is too small")
                if (rv > range[1]):
                    raise Exception("Return value " + str(rv) + "is too big")
            return rv
        return g
    return decorator
