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
from    optparse                import OptionParser

import  struct
import  numpy                   as  np

from    .gthdr                  import __gtHdr__
from    .gtcfg                  import __gtConfig__


class __gtChunk__( __gtConfig__ ):

    def __init__(self, *args, **kwargs):
    #def __init__(self,  __rawArray__, header=None):
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

            #print( __rawArray__, type(__rawArray__), __rawArray__.dtype )
            #sys.exit()
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

        #self.hsize          = self.hdrsize


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

        hsize       = np.array( self.hdrsize.to_bytes( 4, 'big' ) ).view( '4S1' )
        dsize       = np.array( data.size.to_bytes( 4, 'big' ) ).view( '4S1' )

        chunk       = np.concatenate( [ hsize, header,    hsize, 
                                        dsize, data.flat, dsize ] )

        return chunk

    '''
    def chunking1( self, data, header ):

        chksumHdr   = __gtConfig__.chksumHdr
        header      = np.array( list( ''.join(header) ), 'S1' )
        #header      = ''.join(header) 

        #print( header )

        hr = 1024
        print( chksumHdr, type(chksumHdr) )
        print( hr.to_bytes(4, 'big') ) 

        #chksumHdr   = memoryview( struct.pack( '>i', hdrsize ) ).cast( 'c' ).tolist() # w/o checksum

        data.dtype  = 'S1'
        #chksumData  = list( struct.pack( '>i', data.size ) )
        chksumData  = memoryview( struct.pack( '>i', data.size ) ).cast( 'c' ).tolist() 

        #print( type( chksumHdr), chksumHdr )
        #print( type( chksumData ), chksumData )
        #print( type( header ), header )
        #print( type(  data ), data )
        #print( data.size )

        chunk       = np.concatenate( [ chksumHdr, header, chksumHdr,
                                     chksumData, data.flat, chksumData ] )
        return chunk
    '''



    @property
    def header(self):

        #sIdx    = self.pos + 4
        #eIdx    = self.pos + self.hsize + 4

        sIdx, eIdx  = self.hdridx

        __header__      = self.__rawArray__[sIdx:eIdx]

        __header__.dtype= 'S16'

        return __gtHdr__( [__header__] )


    @property
    def data(self):

        #sIdx    = self.pos + self.hsize + 12
        #eIdx    = self.pos + self.size - 4

        sIdx, eIdx  = self.datidx

        data    = self.__rawArray__[sIdx:eIdx]

        # NEED to consider ASTR1 :: e.g.) self.header['AEND3'] - self.header['ASTR3'] +1

        shape   = ( int( self.header['AEND3'] ), 
                    int( self.header['AEND2'] ), 
                    int( self.header['AEND1'] ), 
                )
                    
        '''
        shape       = list(map( int, [
                                 self.header['AEND3'],
                                 self.header['AEND2'],
                                 self.header['AEND1']] ))
        '''
        # ------------------------------------------------------------------------------

        data.dtype  = {''   :np.dtype('>f4'),
                       'UR4':np.dtype('>f4'),
                       'UR8':np.dtype('>f8')}[ self.header['DFMT'].strip() ]

        data.shape  = shape

        return data


def main(args,opts):
    print(args)
    print(opts)

    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


