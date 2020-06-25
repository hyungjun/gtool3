import  os,sys

import  datetime

from    collections         import OrderedDict

import  numpy               as  np

from    .config             import __gtConfig__
from    .format             import __gtHdrFmt__


class __gtHdr__( __gtHdrFmt__ ):

    def __init__(self, headers=None, **kwargs):
        '''
        headers     None            for new __gtHdr__ instance
                    <memmap>        header array in 1024 bytes length
                    <__gtHdr__>     inherit given __gtHdr__

        kwargs      <dict>          attributes to override default or given __gtHdr__
        '''

        self.keys   = list( self.fmt.keys() )

        # when header == None (e.g., newly generated gtfile) -------------------
        # for self.iomode == 'w+':
        if headers is None or isinstance( headers, __gtHdr__ ):

            self.dict   = self.default_dict.copy() if headers is None  \
                     else headers.dict.copy()

            kwargs[ "CSIGN" ]   = 'cf.io.gtool %s'%__gtConfig__.version
            kwargs[ "CDATE" ]   = datetime.datetime.now().strftime('%Y%m%d %H%M%S')

            self.dict.update( kwargs )

            self.__headers__    = self.asarray
        # ----------------------------------------------------------------------

        else:
            self.__headers__    = headers

            self.dict   = OrderedDict( 
                                ( k, self.cast( k, v ) ) for k, v in self.asdict.items()
                        )

        self.curr   = 0


    def __getitem__(self,k):

        #ret     = self.asdict[ k ]
        ret     = self.dict[ k ]

        if ret.shape[0] == 1:
            return self.fmt[ k ][0]( ret[0].strip() ) 

        else:
            ret = list( self.fmt[ k ][0]( b.strip() ) for b in np.unique( ret ) )

            return ret  if len( ret ) > 1   \
              else ret[0]


    def __len__( self ):
        return self.__headers__.shape[0]


    @property
    def asarray( self ):

        maxlen  = max( [ 1        if type( v ) is not list 
                    else len( v ) for k,v in self.dict.items() ] )

        bytearr = np.array( list( [ str.encode( v[1]%self.dict[k] ) ] * maxlen 
                                                        for k,v in self.fmt.items() )
                    ).T

        return bytearr.flatten().view('S1').reshape(maxlen,1024)


    @property
    def asdict( self ):
        return OrderedDict( zip( self.keys, np.array( self.__headers__ ).view('S16').swapaxes(0,1) ) )


    @property
    def shape( self ):
        return ( self[ 'AEND3' ] - self[ 'ASTR3' ] + 1,
                 self[ 'AEND2' ] - self[ 'ASTR2' ] + 1, 
                 self[ 'AEND1' ] - self[ 'ASTR1' ] + 1
                )


    '''
    @property
    def __get_str__(self):

        chksumHdr   = list( struct.pack( '>i4', self.hdrBytes-8 ) ) # w/o checksum
        header      = list( ''.join(header) )

        [ list( ''.join( __header__ ) ) for __header__ in self.__headers__]

        return
    '''

    '''
    @property
    def __hdr__(self):


        __hdr__     = [ attr[0] if len(set( attr )) == 1 else
                        attr
                                    for attr in zip(*self.__headers__) ]

        return __hdr__
    '''


    #def template(self, **kwargs):
    #    __headers__ = array( self.__headers__[:] )

    #    return self.auto_fill(__headers__, **kwargs)


    def __repr__(self):

        hdict       = self.dict     # headers <OrderedDict>

        put2note    = [ k for k, v in hdict.items() if len( np.unique( v ) ) > 1 ]

        #print( self.__headers__.shape)
        #print( hdict )
        print(put2note)


        hdr0        = self.__headers__[0].view( 'S16' ).astype( 'U16' )
        nCol        = 3
        strOut      = []

        for i in range( 0, len( self.keys ), nCol ):
            strOut.append( '[%02d]  '%i
                         + ''.join( ['%-6s :%s:  '%(k, v if k not in put2note else
                                     '   ** NOTE **   ')
                                            for k, v  in zip( 
                                                            self.keys[i:i+nCol],
                                                            hdr0[i:i+nCol] )
                                      ] )
                          )


        if put2note == []:
            return '\n'+'\n'.join(strOut)+'\n'
 
        # when put2noet != [] --------------------------------------------------
        strNote     = ['\n   ** NOTE **   ',]
        noteFmt     = '[%02d]  %-6s :%s, (%i)'

        for k in put2note:
            idx = self.keys.index( k )
            v   = hdict[ k ]

            if not hasattr(v, '__iter__'):  v = [v]

            strNote.append( noteFmt%( idx, k, '[%s ... %s]'%(v[0], v[-1]), len(v) ) )

        return '\n'+'\n'.join(strOut + strNote)+'\n'
        # ----------------------------------------------------------------------

                       

    '''
    def __getattr__( self, k ):

        ret     = self.__headers__[ :, self.keys.index(k) ]

        return   self.fmt[ k ][0]( ret[0].strip() ) if np.unique( ret ).size == 1  \
          else [ self.fmt[ k ][0]( s.strip() ) for s in ret ]
    '''
    '''
        ret     = self.__hdr__[ self.keys.index(k) ] 

        if type( ret ) in [ tuple ]:
            return [ self.fmt[ k ][0]( b.strip() ) for b in ret ]
            #return [ self.fmt[ k ][0]( b.decode().strip() ) for b in ret ]

        else:
            #return self.fmt[ k ][0]( ret.decode().strip() )
            return self.fmt[ k ][0]( ret.strip() )
    '''


    def __getitem__(self,k):

        ret     = self.asdict[ k ]

        if ret.shape[0] == 1:
            return self.fmt[ k ][0]( ret[0].strip() ) 

        else:
            ret = list( self.fmt[ k ][0]( b.strip() ) for b in np.unique( ret ) )

            return ret  if len( ret ) > 1   \
              else ret[0]


    def __setitem__(self, k, v):

        fn, fmt, default    = self.fmt[k]
        idx                 = self.keys.index(k)

        if not hasattr(v, '__iter__') or type( v ) == str:
            v   = [v] * len( self.__headers__)


        for __header__, v in zip( self.__headers__, v ):
            __header__.view('S16')[idx] = fmt%v


    def __iter__(self):
        return self


    def __next__(self):

        if self.curr == len( self ):
            self.curr   = 0
            raise StopIteration

        header      = __gtHdr__( self.__headers__[ self.curr ][None,:] )

        self.curr  += 1

        return header
        

    '''
    def __setitem__(self,k,v):
#        if k not in ['TIME','dIdx','mIdx']: self.__dictHdr__[k]  = self.fmt[k][0](v)
        if k not in ['TIME','dIdx','mIdx']: self.__dictHdr__[k]  = self.fmt[k][1]%v
        else                              : self.__dictHdr__[k]  = v
    '''


    '''
    def __iter__(self):
        for key in self.__dictHdr__:
            yield key
    '''


    '''
    @property
    def template(self):
        Template    = []
        for _k,_v in self.header.items():
            if _k in ['dIdx','mIdx']:   continue    # skip records for file structure

            if type(_v) not in [list,tuple]:
                _v  = __gtHdrFmt__.fmt[_k][0](_v)   # convert back to defalut type
                Template.append(self.fmt[_k][1]%_v)

            else:
                Template.append(_v)

        return Template
    '''

    def auto_fill( self, data, header=None, **kwargs ):
        '''
        generate header

        IN
        ==
        Data    <nd-array>  data array in rank-4 (T, Z, Y, X)
        header  <__gtHdr__> gtool3 header instance to inherit

        kwargs  <dict>      attributes to override default or given header template

        OUT
        ===
        header  <__gtHdr__>
        '''

        if header is not None:

            # for self.iomode == 'r+':
            kwargs[ "MSIGN" ]   = 'cf.io.gtool %s'%__gtConfig__.version
            kwargs[ "MDATE" ]   = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
            # ------------------------

        zsize, ysize, xsize = data.shape[-3:]

        kwargs[ 'AEND1' ]   = self['ASTR1'] + xsize - 1
        kwargs[ 'AEND2' ]   = self['ASTR2'] + ysize - 1
        kwargs[ 'AEND3' ]   = self['ASTR3'] + zsize - 1
        kwargs[ 'SIZE'  ]   = zsize * ysize * xsize - 1

        kwargs[ 'DFMT'  ]   = self.dfmt[ data.itemsize ],

        self.dict.update( kwargs )

        self.__headers__    = self.asarray

        return self


