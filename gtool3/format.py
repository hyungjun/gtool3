import  datetime

from    collections         import OrderedDict

import  numpy               as  np

from    .config             import __gtConfig__

import warnings

class __gtHdrFmt__(object):
    b2s = bytes.decode
    fmt = OrderedDict([
("IDFM", [int,"%16i",9010]),     ("DSET",  [b2s,"%-16s",'']),      ("ITEM", [b2s,"%-16s",'']),      #00
("EDIT1",[b2s,"%-16s",'']),      ("EDIT2", [b2s,"%-16s",'']),      ("EDIT3",[b2s,"%-16s",'']),      #03
("EDIT4",[b2s,"%-16s",'']),      ("EDIT5", [b2s,"%-16s",'']),      ("EDIT6",[b2s,"%-16s",'']),      #06
("EDIT7",[b2s,"%-16s",'']),      ("EDIT8", [b2s,"%-16s",'']),      ("FNUM", [int,"%16i",1]),        #09
("DNUM", [int,"%16i",1]),        ("TITL1", [b2s,"%-16s",'']),      ("TITL2",[b2s,"%-16s",'']),      #12
("UNIT", [b2s,"%-16s",'']),      ("ETTL1", [b2s,"%-16s",'']),      ("ETTL2",[b2s,"%-16s",'']),      #15
("ETTL3",[b2s,"%-16s",'']),      ("ETTL4", [b2s,"%-16s",'']),      ("ETTL5",[b2s,"%-16s",'']),      #18
("ETTL6",[b2s,"%-16s",'']),      ("ETTL7", [b2s,"%-16s",'']),      ("ETTL8",[b2s,"%-16s",'']),      #21
("TIME", [int,"%16i",0]),        ("UTIM",  [b2s,"%-16s",'HOUR']),  ("DATE", [b2s,"%-16s",'00000000 000000']),#24
("TDUR", [int,"%16i",0]),        ("AITM1", [b2s,"%-16s",'']),      ("ASTR1",[int,"%16i",1]),        #27
("AEND1",[int,"%16i",0]),        ("AITM2", [b2s,"%-16s",'']),      ("ASTR2",[int,"%16i",1]),        #30
("AEND2",[int,"%16i",0]),        ("AITM3", [b2s,"%-16s",'']),      ("ASTR3",[int,"%16i",1]),        #33
("AEND3",[int,"%16i",0]),        ("DFMT",  [b2s,"%-16s",'UR4']),   ("MISS", [float,"%16.7e",-999.]),#36
("DMIN", [float,"%16.7e",-999.]),("DMAX",  [float,"%16.7e",-999.]),("DIVS", [float,"%16.7e",-999.]),#39
("DIVL", [float,"%16.7e",-999.]),("STYP",  [int,"%16i",1]),        ("COPTN",[b2s,"%-16s",'']),      #42
("IOPTN",[int,"%16i",0]),        ("ROPTN", [float,"%16.7e",0.]),   ("DATE1",[b2s,"%-16s",'']),      #45
("DATE2",[b2s,"%-16s",'']),      ("MEMO1", [b2s,"%-16s",'']),      ("MEMO2",[b2s,"%-16s",'']),      #48
("MEMO3",[b2s,"%-16s",'']),      ("MEMO4", [b2s,"%-16s",'']),      ("MEMO5",[b2s,"%-16s",'']),      #51
("MEMO6",[b2s,"%-16s",'']),      ("MEMO7", [b2s,"%-16s",'']),      ("MEMO8",[b2s,"%-16s",'']),      #54
("MEMO9",[b2s,"%-16s",'']),      ("MEMO10",[b2s,"%-16s",'']),      ("CDATE",[b2s,"%-16s",'']),      #57
("CSIGN",[b2s,"%-16s",'']),      ("MDATE", [b2s,"%-16s",'']),      ("MSIGN",[b2s,"%-16s",'']),      #60
("SIZE", [int,"%16i",0])                                                                            #63
    ])

    '''
    dictDFMT    = {'UR4':'>f4', dtype('>f4'):'UR4',
                   'UR8':'>f8', dtype('>f8'):'UR8',
                         }
    '''
    dfmt        = {'UR4':'>f4', 4:'UR4',
                   'UR8':'>f8', 8:'UR8',
                         }

    dictUTIM    = {'HOUR':datetime.timedelta(seconds=3600),
                   'SEC':datetime.timedelta(seconds=1),
                        }

    '''
    def __init__(self,header=None):
        if header != None:
            for (k,v),hdr in map(None,list(self.fmt.items()),header):
                self.__dict__[k]    = v[0](hdr.strip())

            self.dtype  = self.dictDFMT[self.DFMT]
            self.delT   = self.dictUTIM[self.UTIM] * self.TDUR
            self.dtime  = datetime.datetime.strptime(self.DATE,'%Y%m%d %H%M%S')
    '''


    def cast( self, k, values ):

        if len( np.unique( values ) ) == 1:
            try: 
                return self.fmt[ k ][0]( values[0].strip() )

            except:
                warnings.warn('cannot cast {}:{} to {}, replace with empty string.'.format(
                    k, values, self.fmt[k][0]))
                return ''

        else:
            l = []
            for b in values:
                try:
                    v = self.fmt[k][0](b.strip())
                except:
                    warnings.warn('cannot cast {}:{} to {}, replace with empty string.'.format(
                        k, b, self.fmt[k][0]))
                    v = ""
                l.append(v)
            return l


    @property
    def default_dict( self ):
        return OrderedDict( [ ( k, v[2] ) for k,v in list(self.fmt.items()) ] )


