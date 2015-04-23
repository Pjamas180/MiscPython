from misc import Failure

class Vector(object):
    """Vector class which creates a vector with a given size or argument list."""
    def __init__(self, length):
        """Constructor for a Vector Object. If the argument is a single int or long, then return a vector with length of argument.
        if the argument is a sequence, then create a Vector with the same argument list."""
        if isinstance(length,(int,long)):
            # Length is an int or long
            if length < 0:
                # return an exception ValueException
                raise ValueError("Vector length cannot be negative")
            else:
                self.length = length
                self.vector = [0.0 for item in range(length)]
        elif isinstance(length,(list,str,unicode,tuple,buffer,xrange)):
            # Length is a sequence
            self.length = len(length)
            self.vector = [x for x in length]
        else:
            raise TypeError("Vector length is not a valid type: Must be a positive int, long, or sequence")

    def __repr__(self):
        """Returns a string representation of the Vector"""
        vectRep = ""
        if self.length != 0:
            if isinstance(self.vector[0],str):
                vectRep = vectRep + "'" + self.vector[0] + "'"
            else:
                vectRep = vectRep + str(self.vector[0])
            for x in range(1,len(self.vector)):
                if isinstance(self.vector[x],str):
                    vectRep = vectRep + ", " + "'" + self.vector[x] + "'"
                else:
                    vectRep = vectRep + ", " + str(self.vector[x])
        return "Vector([" + vectRep + "])"

    def __len__(self):
        """Returns the length of the vector"""
        return self.length

    def __iter__(self):
        """Returns an object that can iterate over the elements of Vector."""
        curPos = 0
        while True:
            if curPos is self.length:
                raise StopIteration
            yield self.vector[curPos]
            curPos+=1

    def __add__(self,b):
        """Allows for addition of equal length lists or Vectors"""
        newList = list(b)
        newVector = self.length
        for i in range(self.length):
            newVector = [self.vector[i] + newList[i] for i in range(self.length)]
        return Vector(newVector)

    def __radd__(self,b):
        """Reverse add which is called when the original add cannot compute."""
        newList = list(b)
        newVector = self.length
        for i in range(self.length):
            newVector = [self.vector[i] + newList[i] for i in range(self.length)]
        return Vector(newVector)

    def dot(self,b):
        """Computes the dot product of the Vector"""
        dotProduct = 0
        # Checking to see if passed value is a Vector
        if isinstance(b,Vector):
            for i in range(len(self.vector)):
                dotProduct+=self.vector[i]*b.vector[i]
        elif isinstance(b,list):
            for i in range(len(self.vector)):
                dotProduct+=self.vector[i]*b[i]
        return dotProduct

    def __getitem__(self,i):
        """Gets the ith element of a Vector"""
        # Checking to see if passed in value is a slice
        if isinstance(i,slice):
            return Vector([x for x in self.vector[i]])
        else:
            if i <= self.length:
                if i < 0:
                    return self.vector[self.length + 1]
                else:
                    return self.vector[i]
                # Return IndexError
                raise IndexError("Vector index out of range")


    def __setitem__(self,i,val):
        """Sets the ith element of a Vector"""
        # Checking to see if passed in value is a slice
        if isinstance(i,slice):
            if len(val) is len(self.vector[i]):
                self.vector[i] = val
                return Vector(self.vector)
            else:
                # Raise a ValueError if the length of the slice modifies the length of the Vector
                raise ValueError("Cannot modify with argument - Vector length will be changed")
        else:
            if i <= self.length:
                if i < 0:
                    self.vector[self.length + 1] = val
                else:
                    self.vector[i] = val
            else:
                raise IndexError("Vector index out of range")

    def __lt__(a,b):
        """Operator for <"""
        return b.__gt__(a)

    def __le__(a,b):
        """Operator for <="""
        return b.__ge__(a)

    def __eq__(a,b):
        """Operator for ==. Vectors are equal if each element in one vector is equal to the respective element in the other Vector."""
        if isinstance(b,Vector):
            for i in range(len(a.vector)):
                if a.vector[i] != b.vector[i]:
                    return False
            return True
        else:
            return False

    def __ne__(a,b):
        """Operator for !=. True when the value is not a Vector."""
        if isinstance(b,Vector) is False:
            return True
        elif a.__eq__(b) is True:
            return False
        else:
            return True

    def __ge__(a,b):
        """Operator for >=. True if every pair of greatest values are equal."""
        boolean = False
        if len(a.vector) is 0 and len(b.vector) is 0:
            return True
        else:
            if len(a.vector) is 0 or len(b.vector) is 0:
                return False
            else:
                if max(a.vector) > max(b.vector):
                    return True
                elif max(a.vector) == max(b.vector):
                    a.vector.remove(max(a.vector))
                    b.vector.remove(max(b.vector))
                    boolean = a.__ge__(b)
        return boolean

    def __gt__(a,b):
        """Operator for >. True if the greatest value of the first Vector is greater than the greatest value of second Vector."""
        boolean = False
        if len(a.vector) > 0:
            if len(b.vector) is 0:
                return True
            elif max(a.vector) > max(b.vector):
                return True

            elif max(a.vector) == max(b.vector):
                # Check for next highest values
                a.vector.remove(max(a.vector))
                b.vector.remove(max(b.vector))
                boolean = a.__gt__(b)
        return boolean
    pass
