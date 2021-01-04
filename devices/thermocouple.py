import logging
from numpy.polynomial.polynomial import polyval


logger = logging.getLogger(__name__)

temp_range = 'low'

def v_to_C(v, temp_range):

    coef_inv = {
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

    return polyval(v*1000, coef_inv[temp_range])

def read_temp(adc, amb): 
    v = adc.convert_and_read()
    C = v_to_C(v, 'low')
    amb_temp = amb.read_temperature()
    logger.debug(f'voltage: {v}; temp: {C}, amb: {amb_temp}')

    return (C + amb_temp), amb_temp
