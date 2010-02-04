package bitvector;

public class Common {
    public static final int    NUM_BITS        = 500;
    public static final int    NUM_GENERATIONS = 500;
    public static final double P_FLIP          = .2;
    public static final double P_SAME          = 1 - P_FLIP;


    public static long factorial( int n ) {
        long result = 1;
        for ( int i = 2; i <= n; i++ ) {
            result *= i;
        }
        return result;
    }

    public static long choose( int n, int k ) {
        System.out.println( factorial( n ) );
        System.out.println( factorial( k ) );
        return factorial( n ) / ( factorial( k ) * factorial( n - k ) );
    }
}
