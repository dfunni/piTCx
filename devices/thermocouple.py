import logging
import time
from numpy.polynomial.polynomial import polyval


logger = logging.getLogger(__name__)

temp_range = 'low'

def v2c(v, tc_type, T_range):

    K_inv = {
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

    coef_inv = {'k_type': K_inv}

    coefs = coef_inv.get(tc_type, K_inv)
    coefs = coefs.get(T_range, 'low')
    
    return polyval(v*1000, coefs)


def C_to_F(degCs):
    return [round(reading*1.8 + 32, 2) for reading in degCs]
    
def read_temps(dev_dict, T_range='low'): 

    amb = dev_dict.get('amb')
    tcs = dev_dict.get('tcs')
    used_tcs = [i for i in tcs if i != None]

    tc_convert_time = len(used_tcs) * used_tcs[0].convert_time
    dly = max(amb.convert_time - tc_convert_time, 0)

    amb.convert()
    reads = [(dev.convert_and_read(), dev.tc_type) for dev in used_tcs]
    if dly:
        time.sleep(dly)
    Tamb = amb.read()
    Ts_C = [Tamb]
    for i, tc in enumerate(tcs):
        j = 0
        if tc != None:
            v, t = reads[j]
            j += 1
            Ts_C.append(round((v2c(v, t, 'low') + Tamb), 4))
        else:
            Ts_C.append(0)

    Ts_F = C_to_F(Ts_C)
    return Ts_C, Ts_F, dly

