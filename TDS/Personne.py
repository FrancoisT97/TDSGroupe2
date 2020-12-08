from random import randint

class MyPerson:
    # sauvegarde les positions
    tracks = []
    # definition de l'objet
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None

    def updateCoordonnees(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    # fin du traitement
    def setDone(self):
         self.done = True

    # self.tracks[-1[1], signifie que quand le point rouge est juste sous la ligne et croise la ligne cela signifie qu'une personne monte
    # self.tracks[-2[1], signifie que quand le point rouge est juste au desssus de la ligne et croise la ligne cela signifie qu'une personne descend
    def going_UP(self, mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                # self.tracks[-1][1] position actuelle, self.tracks[-2][1] position précedente
                # franchit la ligne
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end:
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    def going_DOWN(self, mid_start):
        if len(self.tracks) >= 2:
            if self.state == '0':
                # franchit la ligne
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start:
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False
    def temps_memoire(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True