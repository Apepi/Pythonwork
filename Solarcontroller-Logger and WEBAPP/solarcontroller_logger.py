"""
 _____  ____  _____ ____  _____ 
|  _  ||  _ \|  ___|  _ \|_   _|
| |_| || |_) | |__ | |_) | | |  
|  _  ||  __/|  __||  __/  | |  
| | | || |   | |___| |    _| |_  
|_| |_||_|   |_____|_|   |_____|
This is a script to retrieve certain data from specific register addresses of the SRNE solar controller. Please keep this in mind when using this on your own project.
As different controllers have diffrent communication protocols. Im busy working on making a library containing the communication protocols for various makes of
inverters and solar controllers.

"""


import minimalmodbus
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
from logging.handlers import RotatingFileHandler
from config import *

# Set up logging with rotation to ensure files dont get too big and take up too much space more info can be found here: https://docs.python.org/3/howto/logging.html#
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    filename='YOUR/PATH/HERE/solar_controller.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5 # 5 backup log files before overwriting
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Defining the serial communication parameters according my device. !PLEASE EDIT ACCORDINGLY!
def setup_modbus_instrument():
    instrument = minimalmodbus.Instrument(SERIAL_PORT, MODBUS_ADDRESS)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 0.5
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.clear_buffers_before_each_transaction = True
    return instrument


# Setup client to connect to your InfluxDB 
def setup_influxdb_client():
    return influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)


# Function to return data requested from predetermind register addresses
def read_modbus_data(instrument):
    try:
        return {
            'battery_voltage': instrument.read_register(0x101, 1),
            'battery_soc': instrument.read_register(0x100),
            'pv_power': instrument.read_register(0x109),
            'pv_power_genofday': instrument.read_register(0x113),
            'power_consumption': instrument.read_register(0x114)
        }
    except minimalmodbus.ModbusException as e:
        logger.error(f"Modbus read error: {e}")
        return None


# Function to create list with formatted data points to be sent to your InfluxDB
def create_influxdb_points(data):
    return [
        influxdb_client.Point("battery_voltage").tag("location", "South Africa").field("voltage", data['battery_voltage']),
        influxdb_client.Point("battery_soc").tag("location", "South Africa").field("voltage", data['battery_soc']),
        influxdb_client.Point("pv_power").tag("location", "South Africa").field("power", data['pv_power']),
        influxdb_client.Point("pvpower_generated").tag("location", "South Africa").field("power_generated_today", data['pv_power_genofday']),
        influxdb_client.Point("power_consumption").tag("location", "South Africa").field("power_consumption", data['power_consumption'])
    ]


# Write data points to InfluxDB
def write_to_influxdb(write_api, points):
    try:
        write_api.write(bucket=INFLUXDB_BUCKET, record=points)
    except influxdb_client.InfluxDBError as e:
        logger.error(f"InfluxDB write error: {e}")


# Main function to run the entire script
def main():
    logger.info("Starting Solar Controller script")
    instrument = setup_modbus_instrument()
    influx_client = setup_influxdb_client()
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    while True:
        try:
            data = read_modbus_data(instrument)
            if data:
                points = create_influxdb_points(data)
                write_to_influxdb(write_api, points)
                logger.info("Data successfully logged")
            time.sleep(10)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
