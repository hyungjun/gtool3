import  os,sys

#from    numpy               import array, empty
import  numpy               as  np

from    .gthdr              import __gtHdr__
from    functools           import reduce


class __gtVar__( object ):

    def __init__(self, chunks ):


        __hdr0__        = chunks[0].header

        self.item       = __hdr0__['ITEM']
        self.size       = __hdr0__['SIZE']
        self.shape      = tuple( [len(chunks)] + list(__hdr0__.shape) )
        self.dtype      = chunks[0].data.dtype      # future performance boost

        self.chunks     = np.array( chunks )


    def __repr__(self):
        return '%s, %s : %s'%(self.item, self.shape, self.dtype)


    def __getitem__(self, k):

        if type( k ) is tuple:
            k0      = k[0]
            slc     = k[1:]

        else:
            k0      = k
            slc     = slice( None )


        if   type( k0 ) is int:
            return self.chunks[ k ].data[ slc ]

        elif type( k0 ) is list:
            return np.array( [ self.chunks[i].data[ slc ] for i in k0 ] )

        else:
            return np.array( [ c.data[ slc ] for c in self.chunks[ k0 ] ] )


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

        for c in self.chunks:
            print('+'*100)
            print( c.header )
            print('+'*100)

        sys.exit()
        headers     = [chunk.header.__headers__[0] for chunk in self.chunks]

        return __gtHdr__( np.array( headers ) )


    @property
    def data(self):
        return self.__getitem__


