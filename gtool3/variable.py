import  os,sys
import  numpy               as  np

from    .header             import __gtHdr__


class __gtVar__( object ):

    def __init__(self, chunks ):

        header          = __gtHdr__( [ chunk.__header__ for chunk in chunks ] )
        super().__setattr__( 'header', header )

        self.item       = header['ITEM']
        self.size       = header['SIZE']
        self.shape      = tuple( [len(chunks)] + list(header.shape) )
        self.dtype      = chunks[0].data.dtype      # future performance boost

        self.chunks     = chunks


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
            return self.chunks[ k0 ].data[ slc ]

        elif type( k0 ) is list:
            return np.array( [ self.chunks[i].data[ slc ] for i in k0 ] )

        else:
            return np.array( [ c.data[ slc ] for c in self.chunks[ k0 ] ] )


    def __setitem__(self, k, v):

        if type( k ) is tuple:
            k0      = k[0]
            slc     = k[1:]

        else:
            k0      = k
            slc     = slice( None )

        # assign to self.chunks ------------------------------------------------
        if   type( k0 ) is int:
            self.chunks[ k0 ].data[ slc ]    = v

        elif type( k0 ) is list:
            if not hasattr( v, '__iter__' ) or v.size == 1:
                v   = [ v ] * len( self.chunks )

            for i in k0:    
                self.chunks[i].data[ slc ]  = v[i] 

        else:
            if not hasattr( v, '__iter__' ) or v.size == 1:
                v   = [ v ] * len( self.chunks )

            for i, c in enumerate( self.chunks[ k0 ] ):
                c.data[ slc ]   = v[i]
        # ----------------------------------------------------------------------


    def __getattr__( self, k ):

        header  = self.__dict__[ 'header' ]

        if   k in header.keys:
            return header[ k ]

        elif k in self.__dict__:
            return self.__dict__[ k ]

        else:
            #return 0
            raise KeyError( '{} does not exist.'.format( k ) )


    def __setattr__( self, k, v ):

        if k in self.__dict__[ 'header'].keys:
            self.__dict__[ 'header' ][ k ]  = v

        else:
            self.__dict__[ k ]  = v


    #@property
    #def header(self):
    #    headers     = [ chunk.__header__ for chunk in self.chunks ]
    #    return __gtHdr__( headers )


    #@property
    #def data(self):
    #    return self.__getitem__


