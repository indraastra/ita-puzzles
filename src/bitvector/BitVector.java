/**
 * 
 */
package bitvector;

import java.util.ArrayList;

/**
 * @author vishal
 * 
 */
public class BitVector {

    public int                  generation;
    public BitVector            parent;
    public ArrayList<BitVector> children;
    public byte[]               genome = new byte[Common.NUM_BITS];

    public BitVector( byte[] genome ) {
        this.genome = genome;
    }

    public BitVector( byte[] genome, int generation ) {
        this( genome );
        this.generation = generation;
    }

    public BitVector( byte[] genome, int generation, BitVector parent ) {
        this( genome, generation );
        this.parent = parent;
    }

    public BitVector( byte[] genome, int generation, BitVector parent,
                      ArrayList<BitVector> children ) {
        this( genome, generation, parent );
        this.children = children;
    }

    public int diff( BitVector bv ) {
        int c = 0;
        for ( int i = 0; i < this.genome.length; i++ ) {
            c += this.genome[i] ^ bv.genome[i];
        }
        return c;
    }

    public int diff() {
        return this.diff( this.parent );
    }

    public double probability( BitVector bv ) {
        int d = this.diff( bv );
        return Common.choose( Common.NUM_BITS, d )
               * Math.pow( Common.P_FLIP, d )
               * Math.pow( Common.P_SAME, ( Common.NUM_BITS - d ) );
    }

    public double probability() {
        return this.probability( this.parent );
    }

    /**
     * @param args
     */
    public static void main( String[] args ) {
        // TODO Auto-generated method stub
        System.out.println( "foo!" );
    }

}
