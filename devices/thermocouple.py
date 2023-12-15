import logging
import time
from numpy.polynomial.polynomial import polyval


logger = logging.getLogger(__name__)


def v2c(v, tc_type, temp_range):
    """Convert voltage reading to temperature in degrees Celcius.

    Polynomial coefficients given for the following temperature /
    voltage ranges:
        neg: -200 to 0 C / -5.891 to 0 mV
        low: 0 to 500 C / 0 to 20.644 mv
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

    coefs = coef_inv.get(tc_type, k_inv)
    coefs = coefs.get(temp_range, 'low')

    return polyval(v*1000, coefs)


def c_to_f(temps_c):
    """Convert Celcius to Fahrenheit.

    Args:
        temps_c (list of floats): temperature readings in Celcius
    """
    return [round(reading*1.8 + 32, 2) for reading in temps_c]


def read_temps(dev_dict, temp_range='low'):
    """

    This code separates the MCP9800 convert and read functions to
    allow for simultanoius conversion of the MCP9800 and MCP342x.

    Returns:
        (temperaturs returned as a list of [ambient, tc0, tc1, tc2, tc3])
        temps_c (list of floats): temperatures in Celcius.
        temps_f (list of floats): temperatures in Fahrenheit.
        dly (float): the maximum conversion period between devices.
    """

    amb = dev_dict.get('amb')
    tcs = dev_dict.get('tcs')
    used_tcs = [i for i in tcs if i is not None]

    tc_convert_time = len(used_tcs) * used_tcs[0].convert_time
    dly = max(amb.convert_time - tc_convert_time, 0)

    amb.one_shot_conversion()  # start the MCP9800 conversion first
    reads = [(dev.convert_and_read(), dev.tc_type) for dev in used_tcs]
    logger.debug(reads)
    if dly:
        time.sleep(dly)
    temp_amb = amb.read()  # read the MCP9800 register after sample period
    temps_c = [temp_amb]
    for j, tc in enumerate(tcs):
        if tc is not None:
            v, tc_type = reads[j]
            temps_c.append(round((v2c(v, tc_type, temp_range) + temp_amb), 4))
        else:
            temps_c.append(0)

    temps_f = c_to_f(temps_c)
    return temps_c, temps_f, dly
