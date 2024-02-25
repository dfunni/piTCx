import logging
import time
from numpy.polynomial.polynomial import polyval
from .MCP342x import MCP342x


logger = logging.getLogger(__name__)

class TC(MCP342x):
    
    def __init__(self,
                 bus,
                 chan,
                 address=0x68,
                 res=16,
                 pga=8,
                 tc_type='k_type',
                 temp_range='low'):
        super().__init__(bus, address, chan, res, pga)
        self.tc_type = tc_type
        self.temp_range = temp_range        

    def voltage_to_celcius(self, v):
        """Convert voltage reading to temperature in degrees Celcius.

        Polynomial coefficients given for the following temperature /
        voltage ranges:
            neg: -200 to 0 C / -5.891 to 0 mV
            low: 0 to 500 C / 0 to 20.644 mV
            high: 500 to 1372 C / 20.644 to 54.886 mV
        (https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html)
        """
        k_inv = {
            'neg': [0,
                    2.5173462e1,
                    -1.1662878,
                    -1.0833638,
                    -8.9773540e-1,
                    -3.7342377e-1,
                    -8.6632643e-2,
                    -1.0450598e-2,
                    -5.1920577e-4],
            'low': [0,
                    2.508355e1,
                    7.860106e-2,
                    -2.503131e-1,
                    8.315270e-2,
                    -1.228034e-2,
                    9.804036e-4,
                    -4.413030e-5,
                    1.057734e-6,
                    -1.052755e-8],
            'high': [-1.318058e2,
                    4.830222e1,
                    -1.646031,
                    5.464731e-2,
                    -9.650715e-4,
                    8.802193e-6,
                    -3.110810e-8],
                }

        coef_inv = {'k_type': k_inv}

        coefs = coef_inv.get(self.tc_type, k_inv)
        coefs = coefs.get(self.temp_range, 'low')

        temp_c = polyval(v*1000, coefs)
        return round(temp_c, 4)
