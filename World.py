#!/usr/bin/python

class Cell(object):
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.color = 'green'
        self.background_color = 'yellow'
        self.text = '.'
        self.visible = False

    def __sub__(self, other):
        """ Return shortest (wrappable) Manhattan distance """
        xdiff = min((self.x - other.x) % self.world.MAX_X,
                    (other.x - self.x) % self.world.MAX_X)
        ydiff = min((self.y - other.y) % self.world.MAX_Y,
                    (other.y - self.y) % self.world.MAX_Y)
        return xdiff + ydiff

    def __str__(self):
        return ('<span style="color:{} background-color:{}">{}</span>'
                .format(self.color, self.background_color, self.text))

    def render(self):
        if self - self.world.ME == 0:
            return str(self.world.ME)
        if self.world.isnight and (self - self.world.ME) > self.world.nsight:
            return '<span style="background-color:black">&nbsp;</span>'
        if not self.visible:
            return '&nbsp;'
        return self.__str__()

class World(object):
    DAY_LENGTH = 12  ## arbitrary
    def __init__(self, rows=10, cols=10):
        self.MAX_X = cols
        self.MAX_Y = rows
        self.nsight = 2 ## default visibility length
        ## initialize empty cell grid
        ##@TODO: eventually need some more variety in here...
        self.grid = [[Cell(x, y, self) for x in range(self.MAX_X)]
                        for y in range(self.MAX_Y)]
        ## deal with ME
        self.ME = Cell(int(self.MAX_X/2), int(self.MAX_Y/2), self)
        self.ME.text = 'i'
        self.grid[self.ME.y][self.ME.x].visible = True
        self._add_visible() ## fill in initial view

        ## other details about the world
        self.isnight = False
        self.nmove = 0

    def _add_visible(self):
        """ POST-move, add new visibility. redundant, but oh well """
        ## if arriving in new areas with nsight > 2,
        ## may need to loop over range(dist)...
        for dist in range(self.nsight):
            for dir_x, dir_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                edge_x = self.ME.x + (dir_x * dist)
                edge_y = self.ME.y + (dir_y * dist)
                for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx = (edge_x + x) % self.MAX_X
                    ny = (edge_y + y) % self.MAX_Y
                    self.grid[ny][nx].visible = True

    def move(self, x, y):
        self.ME.x = (self.ME.x + x) % self.MAX_X
        self.ME.y = (self.ME.y + y) % self.MAX_Y
        self._add_visible()
        self.nmove += 1
        if (self.nmove % self.DAY_LENGTH) >= int(self.DAY_LENGTH/4):
            self.isnight = False
        else:
            self.isnight = True

    def get_view(self):
        s = ""
        for y in range(self.MAX_Y):
            for x in range(self.MAX_X):
                s += self.grid[y][x].render()
            s += '<br>'
        return s

