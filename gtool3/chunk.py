import  os,sys

import  struct
import  numpy                   as  np

from    .gthdr                  import __gtHdr__
from    .config                 import __gtConfig__


class __gtChunk__( __gtConfig__ ):

    def __init__(self, *args, **kwargs):
        '''
        /* decodeing mode */
        args    = [ __rawArray__, self.curr, chunkSize ]    # __rawArray__: entire gtool file
        kwargs  = {}

        /* encoding mode */
        args    = [ __rawArray__ ]                          # __rawArray__: appended/extended chunk
        kwargs  = {'header': ... }
        '''

        # encoding mode
        if 'header' in kwargs:

            __rawArray__    = args[0]
            header          = kwargs['header']

            __rawArray__    = self.chunking( __rawArray__, header )
            pos             = 0
            size            = __rawArray__.size

        # decoding mode
        else:
            __rawArray__, __blk_idx__   = args

        self.__rawArray__   = __rawArray__
        self.__blk_idx__    = __blk_idx__

        print( self.__blk_idx__ )


    '''
    def __repr__(self):

        return self.header.__repr__()
    '''


    @property
    def header(self):

        sIdx, eIdx  = self.__blk_idx__[0]   # (start, length)
        eIdx       += sIdx

        __header__      = self.__rawArray__[sIdx:eIdx]
        __header__.dtype= 'S16'

        return __gtHdr__( [__header__] )


    @property
    def data(self):

        sIdx, eIdx  = self.__blk_idx__[-1]  # (start, length)
        eIdx       += sIdx

        data    = self.__rawArray__[sIdx:eIdx]

        print( data, data.dtype, data.shape )
        print( data.view( '>H' ), data.view( '>H' ).dtype, data.view('>H').shape )

        nbit    = int( self.header.DFMT[-2:] )
        print( nbit )

        sIdx, eIdx  = self.__blk_idx__[1]  # (start, length)
        eIdx       += sIdx

        data    = self.__rawArray__[sIdx:eIdx]
        minmax  = data.view( '>d' ).reshape(-1,2) 

        print( data.view( '>H' ) * minmax[0][1] ) 

        sys.exit()

        # NEED to consider ASTR1 :: e.g.) self.header['AEND3'] - self.header['ASTR3'] +1
        shape   = ( int( self.header['AEND3'] ), 
                    int( self.header['AEND2'] ), 
                    int( self.header['AEND1'] ), 
                )
        # ------------------------------------------------------------------------------
        data.dtype  = {''   :np.dtype('>f4'),
                       'UR4':np.dtype('>f4'),
                       'UR8':np.dtype('>f8')}[ self.header['DFMT'].strip() ]

        print( data.dtype, type( self.header['DFMT'].strip() ) );sys.exit()


        data.shape  = shape

        return data


    def chunking( self, data, header ):
        '''
        encoding header + data chunk
        '''

        data.dtype  = 'S1'

        header      = np.array( list( ''.join(header) ), 'S1' ) 

        hsize       = self.encode4b( self.hdrsize )
        dsize       = self.encode4b( data.size    )

        chunk       = np.concatenate( [ hsize, header,    hsize, 
                                        dsize, data.flat, dsize ] )

        return chunk


