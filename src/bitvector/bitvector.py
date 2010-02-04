import util

class BitVector:

    NUM_BITS = 500
    COUNTER = 0
    P_FLIP = 0.2
    P_SAME = 1 - P_FLIP

    def __init__( self, genome, parent=None, children=set() ):
        self.COUNTER += 1

        self.num_bits = len( genome )
        self.id = self.COUNTER
        self.genome = genome
        self.parent = parent
        self.children = children

    def __str__( self ):
        return "BitVector<%s>" % self.genome

    def add_child( self, bv ):
        self.children.add( bv )
        bv.parent = self

    def set_parent( self, bv ):
        self.parent = bv
        bv.children.add( self )

    def flip_diff( self, bv ):
        d = sum( ( self.genome[i] ^ bv.genome[i] ) for i in xrange( len( self.genome ) ) )
        return d

    def p_parent_of( self, bv ):
        return self.p_flipped( self.flip_diff( bv ), len( self.genome ) )

    def p_child_of( self, bv=None ):
        if not bv: bv = self.parent
        if bv:
            return self.p_flipped( self.flip_diff( self.parent ), len( self.genome ) )
        else:
            return 1

    @classmethod
    def p_flipped( self, flipped, total ):
        # util.choose( total, flipped ) * ( self.P_FLIP ** flipped * self.P_SAME ** ( total - flipped ) )
        return ( self.P_FLIP ** flipped * self.P_SAME ** ( total - flipped ) )


def p_lineage( population ):
    return c_lineage( population ) / float( util.factorial( len( population ) - 1 ) )

def c_lineage( population ):
    p = 1
    for bv in population:
        p *= bv.p_child_of()
    return p

if __name__ == "__main__":
    f = open( "/home/vishal/Workspace/ita-puzzles/src/bitvector/data/bitvectors-genes.data.small" )
    pop = [[int( i ) for i in l.rstrip()] for l in f if l]
    a = BitVector( [1] )
    b = BitVector( [0] )
    c = BitVector( [1] )
    a.set_parent( c )
    c.set_parent( b )
    print "lineage:", p_lineage( [a, b, c] )
