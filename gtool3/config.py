import  os,sys
import  struct

import  numpy                       as  np

class __gtConfig__(object):

    hdrsize     = 1024      # bytes

    version     = '0.6b'

    def encode4b( self, num ):
        '''
        convert one 4-byte number to (4) size 'S1' type np.array in big-endian seq.
        '''
        return np.array( num.to_bytes( 4, 'big' ) ).view( '4S1' )


