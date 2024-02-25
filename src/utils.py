import logging
import time

logger = logging.getLogger(__name__)

def c_to_f(temp_c):
    """Convert Celcius to Fahrenheit.

    Args:
        temps_c (list of floats): temperature readings in Celcius
    """
    return round(temp_c*1.8 + 32, 2)


def read_temps(dev_dict):
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

    # start the MCP9800 conversion first
    amb.one_shot_conversion()
    reads = [dev.convert_and_read() for dev in used_tcs]
    
    if dly:
        time.sleep(dly)
    logger.debug('%s %s', reads, dly)
    temp_amb = amb.read()  # read the MCP9800 register after sample period
    temps_c = [temp_amb]
    temps_f = [temp_amb]
    j = 0  # iterating with external value for tcs[0] = None case
    for tc in tcs:
        if tc is not None:
            v = reads[j]
            temp_c = round((tc.voltage_to_celcius(v) + temp_amb), 4)
            temp_f = round(c_to_f(temp_c), 4)
            temps_c.append(temp_c)
            temps_f.append(temp_f)
            j += 1
        else:
            temps_c.append(0)
            temps_f.append(0)
    logger.debug('%s', temps_c)
    return temps_c, temps_f