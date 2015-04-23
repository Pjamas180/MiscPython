class Point:
    x = 0
    y = 0
    def move(self,dx,dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def jump(self,x,y):
        self.x = x
        self.y = y

    def __init__(self,x,y):
        self.jump(x,y)

    def __repr__(self):

    def __str__(self):
        return "x = " + str(self.x) + " y = " + str(self.y)


