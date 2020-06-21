#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtchunk.py
# CREATED BY : hjkim @IIS.2015-07-29 13:53:41.653761
# MODIFED BY :
#
# USAGE      : $ ./gtchunk.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


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
            __rawArray__, pos, size = args

        self.__rawArray__   = __rawArray__
        self.pos            = pos
        self.size           = size

        self.hdridx         = ( pos + 4, 
                                pos + self.hdrsize + 4 )

        self.datidx         = ( self.hdridx[-1] + 8,
                                pos + self.size - 4 )


    '''
    def __repr__(self):

        return self.header.__repr__()
    '''

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


    @property
    def header(self):

        sIdx, eIdx  = self.hdridx

        __header__      = self.__rawArray__[sIdx:eIdx]
        __header__.dtype= 'S16'

        return __gtHdr__( [__header__] )


    @property
    def data(self):

        sIdx, eIdx  = self.datidx

        data    = self.__rawArray__[sIdx:eIdx]

        # NEED to consider ASTR1 :: e.g.) self.header['AEND3'] - self.header['ASTR3'] +1
        shape   = ( int( self.header['AEND3'] ), 
                    int( self.header['AEND2'] ), 
                    int( self.header['AEND1'] ), 
                )
        # ------------------------------------------------------------------------------

        data.dtype  = {''   :np.dtype('>f4'),
                       'UR4':np.dtype('>f4'),
                       'UR8':np.dtype('>f8')}[ self.header['DFMT'].strip() ]

        data.shape  = shape

        return data


