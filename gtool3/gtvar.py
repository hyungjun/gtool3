import  os,sys

from    numpy               import arange, array, empty

from    .gthdr              import __gtHdr__
from    functools           import reduce


class __gtVar__( object ):

    def __init__(self, chunks ):

        self.chunks     = array( chunks )

        self.item       = chunks[0].header['ITEM'].strip()
        self.shape      = [len(chunks)] + list(self.chunks[0].data.shape)
        self.shape      = tuple( self.shape )
        self.size       = reduce( lambda x,y: x*y, self.shape )
        self.dtype      = chunks[0].data.dtype


    def __repr__(self):
        return '%s, %s : %s'%(self.item, self.shape, self.dtype)


    def __getitem__(self, k):

        Slice   = self.parse_slice( k )

        # assign to aOut -------------------------------------------------------
        chunks  = self.chunks[Slice[0]]

        outShp  = list( chunks[0].data[ Slice[1:] ].shape )

        if type( Slice[0] ) == slice:
            outShp  = [ len(chunks) ] + outShp

            aOut    = empty( outShp, self.dtype )

            for i,c in enumerate(chunks):
                aOut[i] = c.data[ Slice[1:] ]

        else:
            aOut    = empty( outShp, self.dtype )
            aOut[:] = chunks[0].data[ Slice[1:] ]

        #aOut    = array([ c.data[ Slice[1:] ] for c in self.chunks[Slice[0]] ])
        # ----------------------------------------------------------------------

        return aOut#.squeeze()


    def __setitem__(self, k, v):

        Slice   = self.parse_slice( k )

        # assign to self.chunks ------------------------------------------------
        chunks  = self.chunks[Slice[0]]

        for i,c in enumerate(chunks):

            if hasattr( v, '__iter__' ):    v = v[0]

            c.data [Slice[1:]] = v
        # ----------------------------------------------------------------------


    def parse_slice(self, k):
        # parse slice ----------------------------------------------------------
        if not hasattr(k, '__iter__'):  k = [k]

        if len(k) > len(self.shape):# and not Ellipsis in k:
            raise KeyError('shape %s does not match with slice %s'%(self.shape, k))

        Slice   = []

        for slc in k:

            if slc == Ellipsis:
                Slice.extend( [ slice(None,None,None) ]*(len(self.shape)-len(k)+1) )

            elif type(slc) == int:
                Slice.append([slc])

            else:
                Slice.append(slc)

        Slice.extend( [ slice(None,None,None) ]*(len(self.shape)-len(Slice)) )
        # ----------------------------------------------------------------------

        return tuple( Slice )


    @property
    def header(self):
        headers     = [chunk.header.__headers__[0] for chunk in self.chunks]

        return __gtHdr__( headers )


    @property
    def data(self):
        return self.__getitem__


