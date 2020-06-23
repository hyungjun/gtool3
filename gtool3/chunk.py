import  os,sys

import  struct
import  numpy                   as  np

from    .gthdr                  import  __gtHdr__
from    .config                 import  __gtConfig__

#from    .filters.nbit_unpack      import  nbit_unpack
from    .filters.nbit_codec     import  nbit_decoder


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

        #print( self.__blk_idx__ )


    '''
    def __repr__(self):

        return self.header.__repr__()
    '''

    @property
    def __header__( self ):
        sIdx, eIdx  = self.__blk_idx__[0]   # (start, length)
        eIdx       += sIdx

        return self.__rawArray__[sIdx:eIdx]
 

    @property
    def __data__( self ):
        sIdx, eIdx  = self.__blk_idx__[-1]   # (start, length)
        eIdx       += sIdx

        return self.__rawArray__[sIdx:eIdx]


    @property
    def header(self):

        return __gtHdr__( self.__header__[None,:] )

        '''
        __header__      = self.__rawArray__[sIdx:eIdx].view( 'S16' ).astype( 'U16' )

        return __gtHdr__( __header__[None,:] )
        '''


    @property
    def data(self):

        data    = self.__data__

        self.encdata    = data.view( '>H' )

        if self.header.DFMT[:3] == 'URY':

            nbit    = int( self.header.DFMT[-2:] )

            sIdx, eIdx  = self.__blk_idx__[1]  # (start, length)
            eIdx       += sIdx
            coef    = self.__rawArray__[sIdx:eIdx]

            data    = nbit_decoder( data, nbit, coef, self.header.shape[0] )

        # ------------------------------------------------------------------------------
        data.dtype  = {'URY':np.dtype('>f4'),
                       'UR4':np.dtype('>f4'),
                       'UR8':np.dtype('>f8')}[ self.header.DFMT[:3] ]

        data.shape  = self.header.shape

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


