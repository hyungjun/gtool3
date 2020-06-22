import  numpy                       as  np


def ipack32len( nbit, datalen, ibit=32 ):
    '''
    calculate length of nd-array (dtype='uint32') requried to contain encoded data
    ---------------------------------------------------------------------------
    
    nbit        <int>       n-bit of encoded data
    datalen     <int>       data length of input data array (default: 32-bit) 
    ibit        <int>       n-bit of input data
    '''
    return nbit * datalen//ibit + (nbit * datalen%ibit + ibit-1 ) // ibit


def nbit_encoder( __rawArray__, nbit, ibit=32 ):
    '''
    obit        <int>       unpact np.array (dtype=S1) to np.array (dtype=I)
    
    '''

    nr      = 1 << nbit         # resolution
    miss    = nr - 1            # biggest value of nintXX (XX = nbit)
    
    return


def unpack_bits_from32( __rawArray__, nbit ):
    '''
    np.array(dtype=S1) to np.array( 'uint32' ) 
    ---------------------------------------------------------------------------

    __rawArray__    <1d-array>      np.array (dtype=S1)
    nbit            <int>           bit size of an encoded data element
    '''
    #print( data.view( '>H' )[4000:4100], data.view( '>H' ).dtype, data.view('>H').shape )

    bitsize     = __rawArray__.size * 8
    outsize     = bitsize - bitsize % nbit 

    npad        = 32 - nbit

    bitarray    = np.unpackbits( __rawArray__.view( 'B' ) )[ :outsize ]
    bitarray    = np.pad( bitarray.reshape( -1, nbit ), ((0,0),(npad,0)), 'constant' )

    return np.packbits( bitarray, bitorder='big' ).view( '>I' )


def nbit_decoder( __rawArray__, nbit, coef, nlayer, missing=1E20 ):
    '''
    coef    <nd-array>      : <'float64'> ( nlayer, i ); i=[0, 1]; 0: min, 1:max-min 

    * return in 'float32'
    * URX is not supported yet
    '''

    miss    = ( 1 << nbit ) - 1     # e.g., 65535 if nbit == 16
    nr      = 1                     # resolution
                                    # for URX: nr = max( miss-1, 1 ) 

    data    = unpack_bits_from32( __rawArray__, nbit ).reshape( nlayer, -1 ).astype( '>d' )

    offset, scale   = coef.view( '>d' ).reshape(-1,2).T

    scale   = scale[:,None] #/ nr
    offset  = offset[:,None]

    print( data.dtype, scale.dtype, offset.dtype )

    return np.where( data != miss, data * scale + offset, missing ).astype( '>f4' )
    


