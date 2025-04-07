# SPDX-FileCopyrightText: 2022-2023 LiBo libo_go@163.com
# SPDX-License-Identifier: Apache-2.0

import time
import logging
import pyvisa

class U3606B(object):
    ''' script for Multimeter DC Supply all in one GPIB control
    '''
    device_mng = None
    device_list = None
    def __init__(self, level=logging.INFO):
        self.device_mng = pyvisa.ResourceManager()
        pyvisa.log_to_screen(level)
        self.device_list = self.device_mng.list_resources()
        self.device_url = ""
        print(self.device_list)
        self.para_list = ['AUTO', 'MAX', 'MIN', 'DEF']
        self.num_list = [float, int]
        self.op_stat = "NONE"
        self.device = None
        
    def _open(self):
        '''open device by GPIB address'''
        for dev_n in self.device_list:
            if dev_n.find("GPIB") != -1:
                self.device_url = dev_n
                try:
                    self.device = self.device_mng.open_resource(self.device_url)
                    print("device name: " + self.device.query("*IDN?"))
                    print("device url: {}".format(self.device_url))
                    self.device.write("*rst; status:preset; *cls")
                    self.op_stat = "OPEN"
                    return True
                except Exception as e:
                    print(f"Error opening U3606B device: {e}")
                    self.op_stat = "ERROR"
                    return False
        print("U3606B Device Not Found")
        self.op_stat = "NOTFOUND"
        return False

    def _is_busy(self, timeout=100):
        '''checks if equip ready for use'''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return True
            
        for i in range(0, timeout):
            try:
                if self.device.query('*OPC?').strip() == "1":
                    return False
                time.sleep(1)
                if i % 10 == 0:  # Only print message every 10 seconds
                    print('U3606B operations are not complete\nWait another second')
            except Exception as e:
                print(f"Error checking if device is busy: {e}")
                return True
        return True

    def _wait(self):
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        self.device.write('*WAI')
        while self._is_busy() == True:
            print('U36068B is still operating...')
        return True

    def _clean(self, timeout=10):
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        self.device.write('*CLS')
        if False == self._is_busy(timeout):
            self.op_stat = 'OPEN'
            print('U3606B Error Queue clears')
            return True
        else:
            print('U3606B clean timeout %4.9f sec!' % timeout)
            self.op_stat = 'ERROR'
            return False

    def _reset(self, timeout=10):
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        self.device.write('*RST')
        if False == self._is_busy(timeout):
            self.op_stat = 'OPEN'
            print('U3606B Resets to factory default state')
            return True
        else:
            print('U3606B reset timeout %4.9f sec!' % timeout)
            self.op_stat = 'ERROR'
            return False
            
    def close(self):
        """Close the device connection properly"""
        if self.device is not None:
            try:
                self.device.close()
                self.device = None
                self.op_stat = "CLOSED"
                print("U3606B device connection closed")
                return True
            except Exception as e:
                print(f"Error closing device: {e}")
                return False
        return True

    def conf_meas(self, func='VOLT', rng='AUTO', f_type='DC'):
        '''configures equip measurement parameters

        - :param func:
            - VOLT: voltage mode
            - CURR: current mode
        - :param rng:
            - AUTO, MAX, MIN, DEF
            - numeric values are also supported
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if func in ['VOLT', 'CURR']:
            if rng in self.para_list or type(rng) in self.num_list:
                try:
                    self.device.write('CONF:%s:%s %s' % (func, f_type, rng))
                    print('U3606B MEAS CONF to: %s %s RNG: %r' %(f_type, func, rng))
                    return True
                except Exception as e:
                    print(f"Error configuring measurement: {e}")
                    self.op_stat = 'ERROR'
                    return False
            else:
                print('Command Error!\nRange parameter type not supported')
                return False
        else:
            print('Command Error!\nOnly "VOLT & CURR" are currently supported')
            return False

    def meas(self, func='VOLT', rng='AUTO', res='MIN', f_type='DC'):
        '''measures current or voltage

        - :param func: VOLT & CURR
        - :param rng: AUTO, MAX, MIN, DEF
        - :param res: AUTO, MAX, MIN, DEF
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return None
            
        if func in ['VOLT', 'CURR']:
            unit = 'V' if func == 'VOLT' else 'A'
            if (rng in self.para_list or type(rng) in self.num_list) and (res in self.para_list[1:] or type(res) in self.num_list):
                try:
                    val = float(self.device.query('MEAS:%s:%s? %s, %s' % (func, f_type, rng, res)))
                    print('U3606B Measures %s %s: %4.8f%s' % (f_type, func, val, unit))
                    return val
                except Exception as e:
                    print(f"Error measuring: {e}")
                    self.op_stat = 'ERROR'
                    return None
            else:
                print('Command Error!\nRange parameter type not supported')
                return None
        else:
            print('Command Error!\nOnly "VOLT & CURR" are currently supported')
            return None

    def conf_sens(self, src = 'EXT'):
        '''configures equip measurement parameters

        - :param src: 'EXT' or 'INT'
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if src in ['EXT', 'INT']:
            try:
                self.device.write('SENS %s' % (src))
                print('U3606B Sens source %s' % (src))
                return True
            except Exception as e:
                print(f"Error configuring sensitivity: {e}")
                self.op_stat = 'ERROR'
                return False
        else:
            print('Command Error!\nOnly "EXT & INT" are currently supported')
            return False

    def sens(self, func='VOLT'):
        '''sens current or voltage

        - :param func: VOLT & CURR
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return None
            
        if func in ['VOLT', 'CURR']:
            unit = 'V' if func == 'VOLT' else 'A'
            try:
                val = float(self.device.query('SENS:%s?' % (func)))
                print('U3606B Sens %s: %4.8f%s' % (func, val, unit))
                return val
            except Exception as e:
                print(f"Error sensing: {e}")
                self.op_stat = 'ERROR'
                return None
        else:
            print('Command Error!\nOnly "VOLT & CURR" are currently supported')
            return None

    def sour_vol_rng(self, rng='AUTO'):
        '''setup voltage range based on output function selected

        - :param rng: '30V', '8V', '1V ', 'AUTO', 'MAX', 'MIN', 'DEF'
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if rng in ['30V', '8V', '1V '] + self.para_list:
            # DEF is default value, which is 30V
            # output is open for configuration only in standby mode
            # ***************************************************************
            try:
                self.sour_out('OFF')
                self.device.write('SOUR:VOLT:RANG %s' % rng)
                print('U3606B VOLTAGE RANG sets to: %s' % rng)
                return True
            except Exception as e:
                print(f"Error setting voltage range: {e}")
                self.op_stat = 'ERROR'
                return False
        else:
            print('Command Error!\nOnly "30V,8V,1V,AUTO,MAX,MIN,DEF" allowed')
            return False

    def sour_cur_rng(self, rng='AUTO'):
        '''setup current range based on output function selected

        - :param rng: '3A', '1A', '100mA ', 'AUTO', 'MAX', 'MIN', 'DEF'
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if rng in ['3A', '1A', '100mA '] + self.para_list:
            # DEF is default value, which is 1A
            # output is open for configuration only in standby mode
            # ***************************************************************
            try:
                self.sour_out('OFF')
                self.device.write('SOUR:CURR:RANG %s' % rng)
                print('U3606B CURRENT RANG sets to: %s' % rng)
                return True
            except Exception as e:
                print(f"Error setting current range: {e}")
                self.op_stat = 'ERROR'
                return False
        else:
            print('Command Error!\nOnly "3A,1A,100mA,AUTO,MAX,MIN,DEF" allowed')
            return False

    def sour_ivlim(self,func='VOLT',iv_lim=3):
        '''setup current/voltage limit range based on output function selected

        - :param func: 'VOLT' or 'CURR'
        - :param iv_lim: limit value in A or V
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        lim_item = 'CURR' if func == 'VOLT' else 'VOLT'
        unit = 'A' if func == 'VOLT' else 'V'
        try:
            self.device.write('SOUR:%s:LIM %r'%(lim_item,iv_lim))
            lim_r = float(self.device.query('SOUR:%s:LIM?'%lim_item))
            print('U3606B CURRENT LIMIT sets to: %.2f%s' % (lim_r,unit))
            return True
        except Exception as e:
            print(f"Error setting limit: {e}")
            self.op_stat = 'ERROR'
            return False

    def sour_out(self, stat='OFF'):
        '''turn on/off output

        - :param stat: 'OFF', 'ON'
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if stat in [0, 1, 'OFF', 'ON']:
            try:
                self.device.write('OUTP:STAT %s' % stat)
                stat_info = stat
                if   stat == 1:   stat_info = 'ON'
                elif stat == 0: stat_info = 'OFF'
                print('U3606B OUTPUT: %s' % stat_info)
                return True
            except Exception as e:
                print(f"Error setting output state: {e}")
                self.op_stat = 'ERROR'
                return False
        else:
            print('Command Error!\nOnly "0,1,ON,OFF" allowed')
            return False

    def sour(self, func='VOLT', lvl=0, rng_auto=True, out='ON', iv_lim=None):
        '''constant voltage or current output

        - :param func: VOLT & CURR
        - :param lvl: level in V or A
        - :param iv_lim: setup current/voltage limit
        - :param rng_auto:
            - manually setup function range if has concern for required total power, see device screen for specs
        - :param out: output on/off
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if func in ['VOLT', 'CURR']:
            unit = 'V' if func == 'VOLT' else 'A'
            if type(lvl) in self.num_list:
                try:
                    range_set_success = True
                    if not rng_auto:
                        # use below commands will turn off power ouput first in
                        # order to configure range
                        if func == 'VOLT':
                            if lvl <= 1:
                                range_set_success = self.sour_vol_rng(rng='1V')
                            elif lvl <= 8:
                                range_set_success = self.sour_vol_rng(rng='8V')
                            elif lvl <= 30:
                                range_set_success = self.sour_vol_rng(rng='30V')
                            else:
                                print("Voltage level out of range (max 30V)")
                                return False
                        elif func == 'CURR':
                            if lvl <= 0.1:
                                range_set_success = self.sour_cur_rng(rng='100mA')
                            elif lvl <= 1:
                                range_set_success = self.sour_cur_rng(rng='1A')
                            elif lvl <= 3:
                                range_set_success = self.sour_cur_rng(rng='3A')
                            else:
                                print("Current level out of range (max 3A)")
                                return False
                    
                    if not range_set_success:
                        return False
                        
                    self.device.write('%s %r' % (func, lvl))
                    self.device.query('%s?' % func)
                    print('U3606B OUTPUT %s level sets to %r' % (func, lvl))
                    if iv_lim is not None:
                        self.sour_ivlim(func=func, iv_lim=iv_lim)
                    if out is not None:
                        return self.sour_out(out)
                    return True
                except Exception as e:
                    print(f"Error setting source: {e}")
                    self.op_stat = 'ERROR'
                    return False
            else:
                print('Command Error!\nRange parameter type not supported')
                return False
        else:
            print('Command Error!\nOnly "VOLT & CURR" are currently supported')
            return False

    def sour_scan(self, func='VOLT', lvl=0, step=10, dwe=2, rng_auto=True, out='ON', iv_lim=None):
        '''voltage or current output with step scan

        - :param func: VOLT & CURR
        - :param lvl: max level
        - :param iv_lim: setup current/voltage limit
        - :param rng_auto:
            - manually setup function range if has concern for required total power, see device screen for specs
        - :param step: total steps
        - :param dwe: dwell time for each step
        - :param out: output on/off
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        if func in ['VOLT', 'CURR']:
            unit = 'V' if func == 'VOLT' else 'A'
            if type(lvl) in self.num_list:
                try:
                    if not rng_auto:
                        # use below commands will turn off power ouput first in
                        # order to configure range
                        if func == 'VOLT' and lvl <= 1:
                            self.sour_vol_rng(rng='1V')
                        elif func == 'VOLT' and lvl <= 8:
                            self.sour_vol_rng(rng='8V')
                        elif func == 'VOLT' and lvl <= 30:
                            self.sour_vol_rng(rng='30V')
                        elif func == 'CURR' and lvl <= 0.1:
                            self.sour_cur_rng(rng='100mA')
                        elif func == 'CURR' and lvl <= 1:
                            self.sour_cur_rng(rng='1A')
                        elif func == 'CURR' and lvl <= 3:
                            self.sour_cur_rng(rng='3A')
                    self.device.query('%s?' % func)
                    self.device.write('%s:SCAN %r' % (func, lvl))
                    self.device.write('%s:SCAN:STEP %r' % (func, step))
                    self.device.write('%s:SCAN:DWEL %r' % (func, dwe))
                    print('U3606B OUTPUT %s SCAN 0-%r with STEP %r, each %rs' % (func, lvl, step, dwe))
                    if iv_lim is not None:
                        self.sour_ivlim(func=func, iv_lim=iv_lim)
                    if out is not None:
                        return self.sour_out(out)
                    return True
                except Exception as e:
                    print(f"Error setting scan: {e}")
                    self.op_stat = 'ERROR'
                    return False
            else:
                print('Command Error!\nRange parameter type not supported')
                return False
        else:
            print('Command Error!\nOnly "VOLT & CURR" are currently supported')
            return False

    def sour_scan_start(self, step=0, out='ON'):
        '''start scan from step

        - :param step: start point
        - :param out: output on/off
        '''
        if self.device is None:
            print("Device not opened. Call _open() first.")
            return False
            
        try:
            self.device.query('SST:STEP?')
            self.device.write('SST:STEP %r' % (step))
            print('U3606B SCAN START at STEP %r' % (step))
            if out != None:
                return self.sour_out(out)
            return True
        except Exception as e:
            print(f"Error starting scan: {e}")
            self.op_stat = 'ERROR'
            return False

if __name__ == "__main__":
    u3606b_dev = U3606B()
    if u3606b_dev._open():
        if u3606b_dev._reset():
            # Example operations can be performed here
            pass
        u3606b_dev.close()
