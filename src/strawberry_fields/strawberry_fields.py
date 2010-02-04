CELL_EMPTY = "."
CELL_BERRY = "@"
COST_GREENHOUSE = 10
COST_CELL = 1

class StrawberryField:

    def __init__( self, field ):
        self.field = field
        self.height = len( field )
        self.width = len( field[0] ) if field else 0

    def __str__( self ):
        return "\n".join( self.field )

    def __repr__( self ):
        return "StrawberryField(%s)" % ( self.field )

    def __getitem__( self, idx ):
        return self.field[idx]

    def find_cells( self, where_type=CELL_BERRY ):
        for i, row in enumerate( self.field ):
            for j, cell in enumerate( row ):
                if cell == where_type:
                    yield i, j

    def contains( self, x, y ):
        return x in xrange( self.height ) and \
               y in xrange( self.width )



class Greenhouse:
    def __init__( self, x1, y1, x2, y2, field ):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.field = field

    def area( self ):
        return ( ( self.x2 - self.x1 ) + 1 ) * ( ( self.y2 - self.y1 ) + 1 )

    def contains( self, x, y ):
        return x in xrange( self.x1, self.x2 + 1 ) and \
               y in xrange( self.y1, self.y2 + 1 )

    def cells( self ):
        for i in xrange( self.x1, self.x2 + 1 ):
            for j in xrange( self.y1, self.y2 + 1 ):
                yield i, j

    def inverted( self ):
        return self.x1 > self.x2 or self.y1 > self.y2

    def intersects( self, other ):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        if other.contains( x1, y1 ): return True
        if other.contains( x2, y2 ): return True
        if other.contains( x1, y2 ): return True
        if other.contains( x2, y1 ): return True
        return False

    def union( self, other ):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        return Greenhouse( min( x1, other.x1 ), \
                           min( y1, other.y1 ), \
                           min( x2, other.x2 ), \
                           min( y2, other.y2 ), self.field )



    def outside_the_lines( self ):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        if not self.field.contains( x1, y1 ): return True
        if not self.field.contains( x2, y2 ): return True
        if not self.field.contains( x1, y2 ): return True
        if not self.field.contains( x2, y1 ): return True
        return False


def unit_greenhouse( x, y, field ):
    return Greenhouse( x, y, x, y, field )
