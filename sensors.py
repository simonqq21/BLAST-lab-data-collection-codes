try:
    try:
        from adafruit_bme280 import basic as adafruit_bme280
    except:
        print('BME280 Library not installed')
    try:
        import adafruit_bh1750
    except:
        print('BH1750 Library not installed')
    try:
        import board
    except:
        print('i2c Library not installed')
    try:
        from picamera import PiCamera
    except:
        print('piCamera Library not installed')


except:
    print("Not running on a Raspberry Pi, using dummy sensor values")
    pass
from io import BytesIO

def BME280init():
    try:
        i2c = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        bme280.sea_level_pressure = 1013.25
    except:
        return None
    return bme280

def BH1750init():
    try:
        i2c = board.I2C()
        bh1750 = adafruit_bh1750.BH1750(i2c)
    except:
        return None
    return bh1750

def piCameraInit():
    try:
        camera = PiCamera()
    except:
        return None
    # set picamera resolution to 5mp if 8mp is not supported
    try:
        camera.resolution = (3280, 2464)
    except Exception as err:
        camera.resolution = (2592, 1944)
    return camera

def BME280Read(bme280):
    temperature, pressure, humidity = 999, -1, -1
    if bme280 is not None:
        temperature = bme280.temperature
        pressure = bme280.pressure
        humidity = bme280.relative_humidity
    return (temperature, pressure, humidity)

def BH1750Read(bh1750):
    lightintensity = -1
    if bh1750 is not None:
        lightintensity = bh1750.lux
    return lightintensity

def piCameraCapture(camera, filepath):
    # BytesIO for pi camera image
    imageStream = BytesIO()
    if camera is not None:
        camera.capture(imageStream, 'jpeg')
        with open(filepath, "wb") as f:
            f.write(imageStream.read())
    return imageStream
