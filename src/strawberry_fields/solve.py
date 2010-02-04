import sys
import string
import random
import itertools
import time
import utils
import strawberry_fields as sf
from aima import search

def strawberries_uncovered( n ):
    total = 0
    for _ in n.state.find_uncovered( where_type=sf.CELL_BERRY ):
        total += 1
    return total


def astar_solve( field, N, repeat=1 ):
    """
    1. Create a greenhouse for each strawberry
    2. Shuffle greenhouses
    3. Go pairwise and join if resulting cost is < previous cost
    """
    prev_sol = None
    for _ in xrange( repeat if N > 1 else 1 ):
        print "solving for N =", N
        sol = Solution( field, N )
        # initialize greenhouses if empty
        for x, y in random.sample( list( sol.field.find_cells( where_type=sf.CELL_BERRY ) ), N ):
            sol.greenhouses.append( sf.unit_greenhouse( x, y, field ) )
        print "initial"
        print sol
        sol = search.astar_search( Solver( sol ), h=strawberries_uncovered ).state
        #sol = search.simulated_annealing( Solver( sol ), schedule=search.exp_schedule( limit=1000 ) ).state
        if ( not prev_sol ) or ( prev_sol and prev_sol.cost() > sol.cost() ):
            prev_sol = sol
    return prev_sol



class Solver( search.Problem ):

    def successor( self, state ):
        #print "expanding..."
        #print state
        for i, greenhouse in enumerate( state.greenhouses ):
            for new_greenhouse in itertools.chain( self.translations( greenhouse ),
                                                   self.growth_spurts( greenhouse ) ):
                greenhouses_copy = state.greenhouses[:]
                greenhouses_copy[i] = new_greenhouse
                sol = Solution( state.field, state.N, greenhouses_copy )
                if sol.is_valid():
                    yield sol, sol
        for i in range( len( state.greenhouses ) ):
            for j in range( i + 1, len( state.greenhouses ) ):
                gh1 = state.greenhouses[i]
                gh2 = state.greenhouses[j]
                new_greenhouse = gh1.union( gh2 )
                greenhouses_copy = [gh for ( k, gh ) in enumerate( state.greenhouses ) if ( k != i ) and ( k != j )]
                greenhouses_copy.append( new_greenhouse )
                sol = Solution( state.field, state.N, greenhouses_copy )
                if sol.is_valid():
                    yield sol, sol


    def goal_test( self, state ):
        return state.is_complete() and state.is_valid()

    def translations( self, gh ):
        x1, y1, x2, y2 = gh.x1, gh.y1, gh.x2, gh.y2
        field = gh.field
        # up
        yield sf.Greenhouse( x1 - 1, y1, x2 - 1, y2, field )
        # down
        yield sf.Greenhouse( x1 + 1, y1, x2 + 1, y2, field )
        # left
        yield sf.Greenhouse( x1, y1 - 1, x2, y2 - 1, field )
        # right
        yield sf.Greenhouse( x1, y1 + 1, x2, y2 + 1, field )

    def path_cost( self, c, state1, action, state2 ):
        return state2.cost() + 1

    def growth_spurts( self, gh ):
        x1, y1, x2, y2 = gh.x1, gh.y1, gh.x2, gh.y2
        field = gh.field
        # up
        yield sf.Greenhouse( x1 - 1, y1, x2, y2, field )
        #gh = sf.Greenhouse( x1, y1, x2 - 1, y2, field )
        #yield gh, gh
        # down
        #gh = sf.Greenhouse( x1 + 1, y1, x2, y2, field )
        #yield gh, gh
        yield sf.Greenhouse( x1, y1, x2 + 1, y2, field )
        # left
        yield sf.Greenhouse( x1, y1 - 1, x2, y2, field )
        #gh = sf.Greenhouse( x1, y1, x2, y2 - 1, field )
        #yield gh, gh
        # right
        #gh = sf.Greenhouse( x1, y1 + 1, x2, y2, field )
        #yield gh, gh
        yield sf.Greenhouse( x1, y1, x2, y2 + 1, field )



class Solution:
    def __init__( self, field, N, greenhouses=None ):
        self.N = N
        self.field = field
        self.greenhouses = greenhouses or []

    def cost( self ):
        total = 0
        for greenhouse in self.greenhouses:
            area = greenhouse.area()
            total += sf.COST_GREENHOUSE + area
        return total

    def covered( self, x, y ):
        for greenhouse in self.greenhouses:
            if greenhouse.contains( x, y ):
                return True
        return False

    def find_uncovered( self, where_type=sf.CELL_BERRY ):
        for cell in self.field.find_cells( where_type=where_type ):
            if not self.covered( *cell ):
                yield cell

    def is_complete( self ):
        return len( self.greenhouses ) <= self.N and \
               all( self.covered( *cell ) for cell in self.field.find_cells( where_type=sf.CELL_BERRY ) )

    def is_valid( self ):
        n = len( self.greenhouses )
        for i in range( n ):
            if self.greenhouses[i].outside_the_lines():
                return False
            if self.greenhouses[i].inverted():
                return False
            for j in range( i + 1, n ):
                if self.greenhouses[i].intersects( self.greenhouses[j] ): return False
                if self.greenhouses[j].intersects( self.greenhouses[i] ): return False
        return True

    def __str__( self ):
        field = [list( l ) for l in self.field]
        for greenhouse, id in zip( self.greenhouses,
                          itertools.cycle( string.uppercase ) ):
            for x, y in greenhouse.cells():
                field[x][y] = id
        return "\n".join( "".join( l ) for l in field )


if __name__ == "__main__":
    puzzles = utils.read_puzzles( sys.argv[1] )
    index = None
    if len( sys.argv ) > 2: index = int( sys.argv[2] )
    for i, ( N, puzzle ) in enumerate( puzzles ):
        if index is not None and i != index:
                continue
        t1 = time.time()
        print puzzle
        sol = astar_solve( puzzle, N )
        print "solution"
        print sol.cost()
        print sol
        print time.time() - t1, "seconds elapsed"

