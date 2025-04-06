import utime
import ustruct
import machine
 
from micropython import const


def get_cpu_temp():    
    cpu_temp = machine.ADC(4)
    
    adc_value = cpu_temp.read_u16()
    voltage = adc_value * 3.3 / 65535
    temperature_c = 27 - (voltage - 0.706)/0.001721
    return temperature_c


class Led():
    def __init__(self):
        self.__led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
    
    def on(self):
        self.__led.value(1)
        
    def off(self):
        self.__led.value(0)

    def toggle(self):
        self.__led.toggle()
    
    def state(self):
        return not self.__led.value()


class Illuminance:
    BH1750_ADDR = const(0x23)
    
    POWER_ON = const(b'\x01')
    POWER_OFF = const(b'\x00')
    RESET = const(b'\x07')
    
    CONTINUOUS_HIGH_RES = const(0x10)
    ONE_TIME_HIGH_RES = const(0x20)
    
    def __init__(self, adjusted_lux=0.75):
        self.adjusted_lux  = adjusted_lux 
                 
        self.__i2c = machine.I2C(0)
        
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.POWER_ON) 
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.RESET)
        
    def __del__(self):
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.POWER_OFF)

    def read(self, continuous=True):      
        mode = Illuminance.CONTINUOUS_HIGH_RES if continuous else Illuminance.ONE_TIME_HIGH_RES      
        self.__i2c.writeto(Illuminance.BH1750_ADDR, bytes([mode]))
        utime.sleep_ms(120 if continuous else 180)            
        
        data = self.__i2c.readfrom(Illuminance.BH1750_ADDR, 2)
        lux = int.from_bytes(data, 'big') * self.adjusted_lux
                  
        return round(lux)


class Tphg:
    BME688_ADDR = const(0x77)
    
    FORCED_MODE = const(0x01)
    SLEEP_MODE = const(0x00)
        
    def __set_power_mode(self, value):
        tmp = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x74, 1)[0] 
        tmp &= ~0x03
        tmp |= value
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x74, bytes([tmp]))
        utime.sleep_ms(1)
  
    def __perform_reading(self):
        self.__i2c.writeto_mem(self.BME688_ADDR, 0x71, bytes([(0b1 << 4) | 0x00]))
        self.__set_power_mode(Tphg.FORCED_MODE)
        """"     
        timeout_time = utime.ticks_add(utime.ticks_ms(), 150)
        while utime.ticks_diff(timeout_time, utime.ticks_ms()) > 0:
            status = self.__i2c.readfrom_mem(self.BME688_ADDR, 0x1D, 1)[0]
            gas_measuring = status & 0x20
            new_data_ready = status & 0x80
            if not gas_measuring and new_data_ready:
                break
            utime.sleep_ms(5)
            
        if not new_data_ready:
            raise OSError("BME688 sensor data not ready")
        """
        gas_measuring = True
        timeout_time = utime.ticks_add(utime.ticks_ms(), 150)
        while gas_measuring and utime.ticks_diff(timeout_time, utime.ticks_ms()) > 0:
            data = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x1D, 1)
            gas_measuring = data[0] & 0x20 != 0
            utime.sleep_ms(5)

        ready = False
        timeout_time = utime.ticks_add(utime.ticks_ms(), 150)
        while not ready and utime.ticks_diff(timeout_time, utime.ticks_ms()) > 0:
            data = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x1D, 1)
            ready = data[0] & 0x80 != 0
            utime.sleep_ms(5)

        if not ready:
            raise OSError("BME680 sensor data not ready")
                
        data = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x1D, 17)
        self._adc_pres = ((data[2] * 4096) + (data[3] * 16) + (data[4] / 16))
        self._adc_temp = ((data[5] * 4096) + (data[6] * 16) + (data[7] / 16))
        self._adc_hum = ustruct.unpack(">H", bytes(data[8:10]))[0]
        self._adc_gas = int(ustruct.unpack(">H", bytes(data[13:15]))[0] / 64)
        self._gas_range = data[14] & 0x0F
            
        var1 = (self._adc_temp / 8) - (self._temp_calibration[0] * 2)
        var2 = (var1 * self._temp_calibration[1]) / 2048
        var3 = ((var1 / 2) * (var1 / 2)) / 4096
        var3 = (var3 * self._temp_calibration[2] * 16) / 16384
        self._t_fine = int(var2 + var3)

    def __temperature(self):
        return ((((self._t_fine * 5) + 128) / 256) / 100) + self._temperature_correction
            
    def __pressure(self):
        var1 = (self._t_fine / 2) - 64000
        var2 = ((var1 / 4) * (var1 / 4)) / 2048
        var2 = (var2 * self._pressure_calibration[5]) / 4
        var2 = var2 + (var1 * self._pressure_calibration[4] * 2)
        var2 = (var2 / 4) + (self._pressure_calibration[3] * 65536)
        var1 = ((((var1 / 4) * (var1 / 4)) / 8192) * (self._pressure_calibration[2] * 32) / 8) + ((self._pressure_calibration[1] * var1) / 2)
        var1 = var1 / 262144
        var1 = ((32768 + var1) * self._pressure_calibration[0]) / 32768
        calc_pres = 1048576 - self._adc_pres
        calc_pres = (calc_pres - (var2 / 4096)) * 3125
        calc_pres = (calc_pres / var1) * 2
        var1 = (self._pressure_calibration[8] * (((calc_pres / 8) * (calc_pres / 8)) / 8192)) / 4096
        var2 = ((calc_pres / 4) * self._pressure_calibration[7]) / 8192
        var3 = (((calc_pres / 256) ** 3) * self._pressure_calibration[9]) / 131072
        calc_pres += (var1 + var2 + var3 + (self._pressure_calibration[6] * 128)) / 16
        return calc_pres / 100

    def __humidity(self):
        temp_scaled = ((self._t_fine * 5) + 128) / 256
        var1 = (self._adc_hum - (self._humidity_calibration[0] * 16)) - ((temp_scaled * self._humidity_calibration[2]) / 200)
        var2 = (self._humidity_calibration[1] * (((temp_scaled * self._humidity_calibration[3]) / 100) + 
                (((temp_scaled * ((temp_scaled * self._humidity_calibration[4]) / 100)) / 64) / 100) + 16384)) / 1024
        var3 = var1 * var2
        var4 = self._humidity_calibration[5] * 128
        var4 = (var4 + ((temp_scaled * self._humidity_calibration[6]) / 100)) / 16
        var5 = ((var3 / 16384) * (var3 / 16384)) / 1024
        var6 = (var4 * var5) / 2
        calc_hum = ((((var3 + var6) / 1024) * 1000) / 4096) / 1000
        return 100 if calc_hum > 100 else 0 if calc_hum < 0 else calc_hum
    
    def __gas(self):
        lookup_table_1 = {
            0: 2147483647.0, 1: 2126008810.0, 2: 2130303777.0, 3: 2147483647.0,
            4: 2143188679.0, 5: 2136746228.0, 6: 2126008810.0, 7: 2147483647.0
        }

        lookup_table_2 = {
            0: 4096000000.0, 1: 2048000000.0, 2: 1024000000.0, 3: 512000000.0,
            4: 255744255.0, 5: 127110228.0, 6: 64000000.0, 7: 32258064.0,
            8: 16016016.0, 9: 8000000.0, 10: 4000000.0, 11: 2000000.0,
            12: 1000000.0, 13: 500000.0, 14: 250000.0, 15: 125000.0
        }

        var1 = ((1340 + (5 * self._sw_err)) * lookup_table_1.get(self._gas_range, 2147483647.0)) / 65536 
        var2 = ((self._adc_gas * 32768) - 16777216) + var1
        var3 = (lookup_table_2.get(self._gas_range, 125000.0) * var1) / 512 
        return ((var3 + (var2 / 2)) / var2)

    def __init__(self, temp_weighting=0.10,  pressure_weighting=0.05, humi_weighting=0.20, gas_weighting=0.65, gas_ema_alpha=0.1, temp_baseline=23.0,  pressure_baseline=1013.25, humi_baseline=45.0, gas_baseline=450_000):
        self.__i2c = machine.I2C(0)
        
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0xE0, bytes([0xB6]))                         # Soft reset
        utime.sleep_ms(5)        
          
        self.__set_power_mode(Tphg.SLEEP_MODE)
        
        t_calibration = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x89, 25)
        t_calibration += self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0xE1, 16)
        
        self._sw_err = (self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x04, 1)[0] & 0xF0) / 16

        calibration = [float(i) for i in list(ustruct.unpack("<hbBHhbBhhbbHhhBBBHbbbBbHhbb", bytes(t_calibration[1:39])))]
        self._temp_calibration = [calibration[x] for x in [23, 0, 1]]
        self._pressure_calibration = [calibration[x] for x in [3, 4, 5, 7, 8, 10, 9, 12, 13, 14]]
        self._humidity_calibration = [calibration[x] for x in [17, 16, 18, 19, 20, 21, 22]]
        #self._gas_calibration = [calibration[x] for x in [25, 24, 26]]                        # res_heat_0, idac_heat_0, gas_wait_0
        
        self._humidity_calibration[1] *= 16
        self._humidity_calibration[1] += self._humidity_calibration[0] % 16
        self._humidity_calibration[0] /= 16

        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x72, bytes([0b001]))                        # Humidity oversampling x1
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x74, bytes([(0b010 << 5) | (0b011 << 2)]))  # Temperature oversampling x2, Pressure oversampling x4
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x75, bytes([0b001 << 2]))                   # Filter coefficient 3 (only to temperature and pressure data)
        
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x50, bytes([0x1F]))                         # idac_heat_0
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x5A, bytes([0x73]))                         # res_heat_0
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x64, bytes([0x64]))                         # gas_wait_0 is 100ms (1ms ~ 4032ms, 20ms ~ 30ms are neccessary)
                
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x71, bytes([(0b1 << 4) | (0b0000)]))        # run_gas(enable gas measurements), nv_conv (index of heater set-point 0)
        utime.sleep_ms(50)
        
        self._temperature_correction = -10
        self._t_fine = None
        self._adc_pres = None
        self._adc_temp = None
        self._adc_hum = None
        self._adc_gas = None
        self._gas_range = None
        
        self.temp_weighting = temp_weighting
        self.pressure_weighting = pressure_weighting
        self.humi_weighting = humi_weighting
        self.gas_weighting = gas_weighting
        self.gas_ema_alpha = gas_ema_alpha
        self.temp_baseline = temp_baseline
        self.pressure_baseline = pressure_baseline
        self.humi_baseline = humi_baseline
        self.gas_baseline = gas_baseline
        
        total_weighting = temp_weighting + pressure_weighting + humi_weighting + gas_weighting
        if abs(total_weighting - 1.0) > 0.001:
             raise ValueError("The sum of weightings is not equal to 1.  This may lead to unexpected IAQ results.")
            
    def set_temperature_correction(self, value):
        self._temperature_correction += value

    def read(self, gas=False):
        self.__perform_reading()
        if not gas:
            return self.__temperature(), self.__pressure(), self.__humidity(), None
        else:
            return self.__temperature(), self.__pressure(), self.__humidity(), self.__gas()
        
    def sealevel(self, altitude):
        self.__perform_reading()
        press = self.__pressure()  
        return press / pow((1-altitude/44330), 5.255), press
        
    def altitude(self, sealevel): 
        self.__perform_reading()
        press = self.__pressure()
        return 44330 * (1.0-pow(press/sealevel,1/5.255)), press

    def iaq(self):
        self.__perform_reading()
        temp = self.__temperature()
        pres = self.__pressure()
        humi = self.__humidity()
        gas = self.__gas()

        hum_offset = humi - self.humi_baseline
        hum_score = (1 - min(max(abs(hum_offset) / (self.humi_baseline * 2), 0), 1)) * (self.humi_weighting * 100)

        temp_offset = temp - self.temp_baseline
        temp_score = (1- min(max(abs(temp_offset) / 10, 0), 1)) * (self.temp_weighting * 100)

        self.gas_baseline = (self.gas_ema_alpha * gas) + ((1 - self.gas_ema_alpha) * self.gas_baseline) # EMA for gas_baseline
        gas_offset = self.gas_baseline - gas
        gas_score = (gas_offset / self.gas_baseline) * (self.gas_weighting * 100)
        gas_score = max(0, min(gas_score, self.gas_weighting * 100))
        
        pressure_offset = pres - self.pressure_baseline
        pressure_score =  (1 - min(max(abs(pressure_offset) / 50, 0), 1)) * (self.pressure_weighting * 100)

        iaq_score = round((hum_score + temp_score + gas_score + pressure_score) * 5)

        return iaq_score, temp, pres, humi, gas
        
    def burnIn(self, threshold=0.01, count=10, timeout_sec=180): 
        self.__perform_reading()
        prev_gas = self.__gas()
        
        counter  = 0
        timeout_time = utime.ticks_us()  
        interval_time = utime.ticks_us()
                 
        while True:
            if utime.ticks_diff(utime.ticks_us(), interval_time) > 1_000_000:
                self.__perform_reading()
                curr_gas = self.__gas()
                gas_change = abs((curr_gas - prev_gas) / prev_gas)
                yield False, curr_gas, gas_change

                counter  = counter + 1 if gas_change <= threshold else 0

                if counter > count:
                    yield True, curr_gas, 0.0
                    break
                else:
                    yield False, curr_gas, gas_change
                    
                prev_gas = curr_gas
                interval_time = utime.ticks_us()
            
            if utime.ticks_diff(utime.ticks_us(), timeout_time) > timeout_sec * 1_000_000:
                yield False, 0.0, 0.0
                break


class IMU:
    BNO055_ADDR = const(0x28)

    ACCELERATION = const(0x08)
    MAGNETIC = const(0x0E)
    GYROSCOPE = const(0x14)
    EULER = const(0x1A)
    QUATERNION = const(0x20)
    ACCEL_LINEAR = const(0x28)
    ACCEL_GRAVITY = const(0x2E)
    TEMPERATURE = const(0x34)
    
    def __init__(self):
        self.__i2c = machine.I2C(0)
        
        self.__scale = {self.ACCELERATION:1/100, self.MAGNETIC:1/16, self.GYROSCOPE:0.001090830782496456, self.EULER:1/16,  self.QUATERNION:1/(1<<14), self.ACCEL_LINEAR:1/100, self.ACCEL_GRAVITY:1/100}
        self.__call = {self.ACCELERATION:self.__read_other, self.MAGNETIC:self.__read_other, self.GYROSCOPE:self.__read_other, self.EULER:self.__read_other,  self.QUATERNION:self.__read_quaternion, self.ACCEL_LINEAR:self.__read_other, self.ACCEL_GRAVITY:self.__read_other, self.TEMPERATURE:self.__read_temperature}

        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3D, bytes([0x00])) #Mode Register, Enter configuration.
        utime.sleep_ms(20)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0x3F, bytes([0x20])) #Trigger Register, Reset
        utime.sleep_ms(650)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3E, bytes([0x00])) #Power Register, Set to normal power. cf) low power is 0x01
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X07, bytes([0x00])) #Page Register, Make sure we're in config mode and on page0(param, data), page1(conf)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3F, bytes([0x80])) #Trigger Register, External oscillator
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3F, bytes([0x00])) #Trigger Register,
        utime.sleep_ms(10)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3D, bytes([0x0C])) #Mode Register, Enter normal operation (NDOF)
        utime.sleep_ms(200)

    def __read_temperature(self, addr):
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 1)[0]
        return t - 256 if t > 127 else t

    def __read_quaternion(self, addr):
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 8)  
        return tuple(v * self.__scale[self.QUATERNION] for v in ustruct.unpack('hhhh', t))

    def __read_other(self, addr):
        if addr not in self.__scale:
            raise ValueError(f"Address {addr} not in scale mapping")
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 6)
        return tuple(v * self.__scale[addr] for v in ustruct.unpack('hhh', t))

    def calibration(self):
        data = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, 0x35, 1)[0] #Calibration Resiger, Read        
        return (data >> 6) & 0x03, (data >> 4) & 0x03, (data >> 2) & 0x03, data & 0x03  #Sys, Gyro, Accel, Mag

    def read(self, addr):
        return self.__call[addr](addr)


# TODO: Next time, use the same pin name as the DIO class.

class DIO:
    IN = machine.Pin.IN
    OUT = machine.Pin.OUT
    PULL_UP = machine.Pin.PULL_UP
    PULL_DOWN = machine.Pin.PULL_DOWN
    LOW = const(0)
    HIGH = const(1)

    
    P_RELAY = {0:'D0', 1:'D6', 2:'D5'} 
    
    @staticmethod
    def P18(): #Only Input of ActiveHigh(5V ~ 6V) Device(ex: GasDetector). It has a built-in divider resistor that halves the 12V.
        return machine.Pin('D7', machine.Pin.IN)
    
    @staticmethod
    def P17(): #Only Input of ActiveLow(GND) Device(ex:PIR, LimitSiwtch ...)
        return machine.Pin('P2', machine.Pin.IN) #D12
    
    @staticmethod
    def P8(mode, pull_value=None): #Operation 3V3 IN/OUT
        if mode == DIO.IN:
            p = machine.Pin('P0', mode, pull=pull_value)
        else:
            p = machine.Pin('P0', mode, value=pull_value)
        return p
    
    @staticmethod
    def P23(mode, pull_value=None): #Operation 3V3 IN/OUT
        if mode == DIO.IN:
            p = machine.Pin('D4', mode, pull=pull_value)
        else:
            p = machine.Pin('D4', mode, value=pull_value)
        return p


def Relay(pin, value=0): #value=0 is Normal open
    return machine.Pin(pin, machine.Pin.OUT, value=value)

class RelayTerminal:
    def __init__(self, *relays):
        self.__relays = relays
    
    def on(self, pos):
        self.__relays[pos].on()

    def off(self, pos):
        self.__relays[pos].off()
