import utime
import ustruct
import machine

from micropython import const

def get_cpu_temp() -> int:    
    """
    Read the internal CPU temperature
    
    :return: The cpu temperature value 
    """
            
class Led():
    """
    The Led object is used to control the state of the LED.
    """
    
    def on(self) -> None:
        """
        light on the LED.
        """
        
    def off(self) -> None:
        """
        light off the LED.
        """
 
    def toggle(self) -> None:
        """
        Toggle the LED state.
        """
    
    def state(self) -> bool:
        """
        Return the state of the LED.
        
        :return: ``True`` if the LED is on, ``False`` if the LED is off.
        """

class Illuminance:
    """
    The illuminance sensor is a digital sensor that measures the illuminance in lux.
    """
        
    def __init__(self, adjusted_lux=0.75):
        """
        Initializes the illuminance sensor.
        
        :param adjusted_lux: The adjusted lux. default is 0.75
        """ 
        
    def read(self, continuous=True) -> int:            
        """
        Reads the illuminance value.
        
        :param continuous: If ``True`` the sensor is in continuous mode.
        
        :return: The illuminance value.
        """

class Tphg:
    """
    This object is used to read temperature, pressure, humidity and gas values.
    or to calculate the altitude and sea level pressure.
    and to calculate the IAQ index.
    """
    
    def __init__(self, temp_weighting:float=0.10, pressure_weighting:float=0.05, humi_weighting:float=0.20, gas_weighting:float=0.65, gas_ema_alpha:float=0.1, temp_baseline:float=23.0, pressure_baseline:float=1013.25, humi_baseline:float=45.0, gas_baseline:int=450_000) :
        """
        Initializes the Tphg sensor.        
              
        :param temp_weighting: Temperature weighting.
        :param pressure_weighting: Pressure weighting.        
        :param humi_weighting: Humidity weighting.
        :param gas_weighting: Gas weighting.
        :param gas_ema_alpha: Gas EMA alpha.
        :param temp_baseline: Temperature baseline.
        :param pressure_baseline: Pressure baseline.
        :param humi_baseline: Humidity baseline.
        :param gas_baseline: Gas baseline.
        """ 
        
    def set_temperature_correction(self, value:float) -> None:
        """
        Compensates for temperature.
        
        :param value: Temperature compensation value
        """


    def read(self, gas: bool=False) -> tuple:
        """
        Reads the temperature, pressure, humidity and gas values.
        
        :param gas: If ``True`` reads the gas value.
        
        :return: A tuple with temperature, pressure, and humidity values. However, if the parameter gas is True, gas is added.    
        """

        
    def sealevel(self, altitude:float) -> float:
        """
        calculates the pressure at sea level based on the altitude
        
        :param altitude: Altitude in meters.
        
        :return: The pressure at sea
        """
        
    def altitude(self, sealevel:float) -> float: 
        """
        calclates the altitude based on the sealevel pressure
        
        :param sealevel: Pressure at sea level.
        
        :return: The altitude in meters.
        """

    def iaq(self) -> tuple:
        """
        Reads the IAQ index.
        
        :return: Tuple with the IAQ index, temperature, pressure, humidity and gas.
        """

    def burnIn(self, threshold: float=0.01, count: int=10, timeout_sec: int=180) -> tuple:
        """
        Performs stabilization operations required for gas measurements.
        
        :param threshold: The threshold value.
        :param count: The number of measurements.
        :param timeout_sec: The timeout in seconds.
        
        :return: Tuple with the state, gas, deviation.
        """


class IMU:
    """
    Inertial Measurement Unit module control class.
    """
    
    ACCELERATION = const(0x08)
    MAGNETIC = const(0x0E)
    GYROSCOPE = const(0x14)
    EULER = const(0x1A)
    QUATERNION = const(0x20)
    ACCEL_LINEAR = const(0x28)
    ACCEL_GRAVITY = const(0x2E)
    TEMPERATURE = const(0x34)
    
    def __init__(self) -> None:
        """
        Initialize the IMU module.
        """
    
    def calibration(self) -> tuple:
        """
        Read the calibration status of the IMU.
        
        :return: Tuple of calibration status for system, gyroscope, accelerometer, and magnetometer.
        """

    def read(self, target:int) -> tuple | int:
        """
        Read the data from the IMU.
        
        :param target: The target of the data to be read. 
            One of ACCELERATION, MAGNETIC, GYROSCOPE, EULER, QUATERNION, ACCEL_LINEAR, ACCEL_GRAVITY, TEMPERATUR.
        
        :return: Tuple or integer data read from the target.
            ACCELERATION: (x, y, z) 
            MAGNETIC: (x, y, z)
            GYROSCOPE: (x, y, z)
            EULER: (heading, roll, pitch)
            QUATERNION: (w, x, y, z)
            ACCEL_LINEAR: (x, y, z)
            ACCEL_GRAVITY: (x, y, z)
            TEMPERATUR: temperature
        """