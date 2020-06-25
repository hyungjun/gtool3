#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtfile.py
# CREATED BY : hjkim @IIS.2015-07-29 11:19:30.645538
# MODIFED BY :
#
# USAGE      : $ ./gtfile.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401

import  os, sys, time

from    collections                 import OrderedDict

import  numpy                       as  np

from    .config                     import __gtConfig__
from    .chunk                      import __gtChunk__
from    .variable                   import __gtVar__
from    .header                     import __gtHdr__


class gtFile( __gtConfig__ ):
    '''
    gt=gtool(path, iomode,unit)

        * iomode : [
                    'r',    # read (native mode of numpy.memmap for existing file)
                    'r+',   # read and write (native mode of numpy.memmap for existing file)
                    'w',    # write
                    'ow'    # over write
                    ]

    # access ATTR
    >>> gt.variables[varName].DATE
    '19990101 000000'

    >>> gt.variables[varName].UTIM
    'HOUR'                                  # ['HOUR','DAY'] only

    >>> gt.variables[varName].TDUR
    24


    ******
    HEADER
    ******
    1  "IDFM":[int,"%16i",9010],                # req
    2  "DSET":[str,"%-16s",''],                 # req
    3  "ITEM":[str,"%-16s",''],                 # req
    4  "EDIT1":[str,"%-16s",''],
    5  "EDIT2":[str,"%-16s",''],
    6  "EDIT3":[str,"%-16s",''],
    7  "EDIT4":[str,"%-16s",''],
    8  "EDIT5":[str,"%-16s",''],
    9  "EDIT6":[str,"%-16s",''],
    10 "EDIT7":[str,"%-16s",''],
    11 "EDIT8":[str,"%-16s",''],
    12 "FNUM":[int,"%16i",1],
    13 "DNUM":[int,"%16i",1],
    14 "TITL1":[str,"%-16s",''],
    15 "TITL2":[str,"%-16s",''],
    16 "UNIT":[str,"%-16s",''],
    17 "ETTL1":[str,"%-16s",''],
    18 "ETTL2":[str,"%-16s",''],
    19 "ETTL3":[str,"%-16s",''],
    20 "ETTL4":[str,"%-16s",''],
    21 "ETTL5":[str,"%-16s",''],
    22 "ETTL6":[str,"%-16s",''],
    23 "ETTL7":[str,"%-16s",''],
    24 "ETTL8":[str,"%-16s",''],
    25 "TIME":[int,"%16i",0],
    26 "UTIM":[str,"%-16s",'HOUR'],
    27 "DATE":[str,"%-16s",'00000000 000000'],  # req
    28 "TDUR":[int,"%16i",0],
    29 "AITM1":[str,"%-16s",''],                # req
    30 "ASTR1":[int,"%16i",0],                  # req
    31 "AEND1":[int,"%16i",0],                  # req
    32 "AITM2":[str,"%-16s",''],                # req
    33 "ASTR2":[int,"%16i",0],                  # req
    34 "AEND2":[int,"%16i",0],                  # req
    35 "AITM3":[str,"%-16s",''],                # req
    36 "ASTR3":[int,"%16i",0],                  # req
    37 "AEND3":[int,"%16i",0],                  # req
    38 "DFMT":[str,"%-16s",''],
    39 "MISS":[float,"%16.7e",-999.],
    40 "DMIN":[float,"%16.7e",-999.],
    41 "DMAX":[float,"%16.7e",-999.],
    42 "DIVL":[float,"%16.7e",-999.],
    43 "DIVL":[float,"%16.7e",-999.],
    44 "STYP":[int,"%16i",1],
    45 "COPTN":[str,"%-16s",''],
    46 "IOPTN":[int,"%16i",0],
    47 "ROPTN":[float,"%16.7e",0.],
    48 "DATE1":[str,"%-16s",''],
    49 "DATE2":[str,"%-16s",''],
    50 "MEMO1":[str,"%-16s",''],
    51 "MEMO2":[str,"%-16s",''],
    52 "MEMO3":[str,"%-16s",''],
    53 "MEMO4":[str,"%-16s",''],
    54 "MEMO5":[str,"%-16s",''],
    55 "MEMO6":[str,"%-16s",''],
    56 "MEMO7":[str,"%-16s",''],
    57 "MEMO8":[str,"%-16s",''],
    58 "MEMO9":[str,"%-16s",''],
    59 "MEMO10":[str,"%-16s",''],
    60 "CDATE":[str,"%-16s",''],
    61 "CSIGN":[str,"%-16s",''],
    62 "MDATE":[str,"%-16s",''],
    63 "MSIGN":[str,"%-16s",''],
    64 "SIZE":[int,"%16i",0]
    '''

    def __init__(self, gtPath, mode='r', indexing=True):
        '''
        indexing  <bool>    True : scan entire file (e.g., for multiple vars & dims container)
                            False: scan first block only & uniform file structure (e.g., for ingel var container)
        '''

        if mode in ['r','c','r+']:
            self.__rawArray__   = np.memmap(gtPath, 'S1', mode)

        elif mode == 'w+':
            gtFile  = open(gtPath, 'w')
            gtFile.close()

            self.__rawArray__   = np.array([], 'S1')
            self.gtPath         = gtPath

        else:
            raise ValueError('%s is not supported option'%mode)

        self.pos        = 0
        self.size       = self.__rawArray__.size

        self.curr       = 0
        self.__blk_idx__= []            # indices of fortran IO blocks
        self.__chunks__ = []

        #self.__vars__   = OrderedDict()
        self.__pos__    = OrderedDict()

        #self.indexing     = indexing

        '''
        if indexing:
            s=time.time()
            self.indexing()
            print( time.time()-s)

        else:
            # cache varName for simple indexingure

            self.set_uniform_pos()

            size            = self.__pos__[0]
            self.varName    = __gtChunk__( self.__rawArray__, 0, size ).header['ITEM'].strip()
        '''

        self.iomode     = mode
        self.__version__= __gtConfig__.version


    def __getitem__(self, k):
        return self.__chunks__[k]


#    @property
#    def chunks(self):
#        '''
#        for delayed process
#        '''
#        if not hasattr( self, '__chunk__'):
#            self.__chunks__ = [ chunk for chunk in self ]
#
#        return self.__chunks__


    @property
    def variables( self ):
        return getattr( self, 'vars' )


    @property
    def vars(self):
        '''
        to be deprecated
        '''

        if not hasattr( self, '__vars__' ):

            self.__vars__   = OrderedDict()

            for chunk in self:#.__chunks__:

                varName     = chunk.header['ITEM'] 
                self.__vars__.setdefault( varName, [] ).append( chunk )

        return OrderedDict( [(k, __gtVar__(v) ) for k,v in list(self.__vars__.items())] )


    def indexing( self ):
        '''
        '''

        blk_idx = []            # indices of fortran IO blocks

        pos     = 0

        while pos < self.__rawArray__.size:

            blk_len = int.from_bytes( self.__rawArray__[ pos:pos+4 ].tostring(), 'big' )

            blk_idx.append( [ pos+4, pos+4 + blk_len ] )

            print( pos+4, blk_len, blk_idx[-1] )
            pos += blk_len + 8

        self.__blk_idx__    = blk_idx


    def get_block_len( self, pos ):
        return int.from_bytes( self.__rawArray__[ pos:pos+4 ].tostring(), 'big' )


    def __iter__(self):
        return self


    def __next__(self):

        if self.pos == self.size:
            self.pos    = 0
            self.curr   = 0
            raise StopIteration
        
        blk_idx = []

        pos     = self.pos

        DFMT    = self.__rawArray__[pos+596:pos+612].tostring().strip().decode()

        # header block
        blk_idx.append( ( pos+4, self.get_block_len( pos ) ) )
        pos += blk_idx[-1][-1] + 8      # block_length + 8

        # scale block
        if DFMT[1:3] in ['RY', 'RX']:       # [UM]R[XY]; ?RX will be deprecated
            blk_idx.append( ( pos+4, self.get_block_len( pos ) ) )
            pos += blk_idx[-1][-1] + 8  # block_length + 8

        # data block
        blk_idx.append( ( pos+4, self.get_block_len( pos ) ) )
        pos += blk_idx[-1][-1] + 8      # block_length + 8

        self.__blk_idx__.append( blk_idx )

        self.pos    = pos
        self.curr  += 1

        return __gtChunk__( self.__rawArray__, self.__blk_idx__[-1] )


    def append(self, Data, headers=None, **kwargs):
        '''
        append one chunk

        IN
        ==
        Data    <nd-array>  data array in rank-4 (T, Z, Y, X)
        header  <__gtHdr__> gtool3 header instance
                <memmap>

        kwargs  <dict>      attributes to override default or given header template

        OUT
        ===
        header  <__gtHdr__>
        '''


        if headers == None:
            native_code = sys.byteorder == 'little' and '<' or '>'
            byteorder   = Data.dtype.byteorder
            byteorder   = byteorder if byteorder != '=' else native_code


            if byteorder == '<':
                Data        = Data.byteswap()
                byteorder   = '>'

            dtypedescr  = byteorder + Data.dtype.kind + str(Data.dtype.itemsize)
            Data.dtype  = dtypedescr


        headers         = __gtHdr__( headers = headers ).auto_fill( Data, **kwargs )


        #for data, header in map(None, Data, headers):
        for data, header in zip( Data, headers):

            chunk       = __gtChunk__( data, header=header )
            self.__chunks__.append( chunk )

            varName     = header['ITEM']

            if not hasattr( self, '__vars__' ):
                self.__vars__           = OrderedDict()

            if not varName in self.__vars__:
                self.__vars__[varName] = []

            self.__vars__[varName].append( chunk )

            # write to memmap --------------------------------------------------
            pos         = self.__rawArray__.size
            __memmap__          = np.memmap( self.gtPath, 'S1', 'r+',
                                             shape=(self.__rawArray__.size+chunk.size)
                                        )
            __memmap__[pos:]    = chunk.__rawArray__
            self.__rawArray__   = __memmap__
            self.__rawArray__[pos:]     = chunk.__rawArray__

            # ------------------------------------------------------------------


#class __gtDim__(gtFile):
#    '''
#    TODO
#    i. to be integrated into class __gtHdr__
#    ii. fix a bug for reading wrong value
#    '''
#
#    def __init__(self,crdNAME):
#        '''
#        crdNAME: list of pre-defined coordination name [AITM1, AITM2, AITM3]
#        '''
#
#        AITM1, AITM2, AITM3     = crdNAME
#
#        self.__dictDim__        = OrderedDict()
#        self.__dictDim__[ 'z' ] = array( self.get_coord( AITM3 )[1].flatten() )
#        self.__dictDim__[ 'y' ] = array( self.get_coord( AITM2 )[1].flatten() )
#        self.__dictDim__[ 'x' ] = array( self.get_coord( AITM1 )[1].flatten() )
#
#        self.names  = (AITM3, AITM2, AITM1)
#
#
#    def get_coord(self,crdName):
#        srcFName    = 'GTAXLOC.%s'%crdName
#        srcPath     = os.path.join(GTOOL_DIR,srcFName)
#
#        self.curr       = 0
#        self.hdrsize   = 1032      # = 4+1024+4
#        self.__rawArray__  = memmap(srcPath, 'S1', 'r')
#
#        Headers, Vars   = self.scan_indexingure()
#
#        crdName         = list(Vars.keys())[0]
#
#        return crdName, Vars[crdName][0][:]
#
#
#    def __getitem__(self,k):
#        return self.__dictDim__[k]
#
#
#    def __repr__(self):
#
#        strDim      = ['\n   ** DIMENSIONS **   ',]
#        dimFmt      = '[ %s]  %-16s :%s, (%i)'
#
#        for crdName, axName in map( None, self.names, list(self.__dictDim__.keys()) ):
#            aCrd    = self.__dictDim__[axName]
#            strDim.append( dimFmt%(axName, crdName, '[%s ... %s]'%(aCrd[0],aCrd[-1]) if aCrd != [] else '[]', len(aCrd)) )
##            print '[%s ... %s]'%(str(aCrd[0]),str(aCrd[0])),  array([0.0])==[]
#
#        return '\n'.join(strDim)


