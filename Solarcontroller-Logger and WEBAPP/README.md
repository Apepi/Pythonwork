# Solar Controller Data Logger

## Overview
This Python script is designed to retrieve data from a SRNE solar controller using Modbus communication, and log this data to an InfluxDB database. It serves as a practical example of interfacing with hardware devices, implementing data logging, and integrating with time-series databases.

## Key Features
- Modbus RTU communication with a solar controller
- Data retrieval from specific register addresses
- Integration with InfluxDB for time-series data storage
- Robust error handling and logging
- Configurable settings for easy deployment

## Technologies Used
- Python
- minimalmodbus library for Modbus communication
- InfluxDB client for data storage
- Logging module for error tracking and debugging

## Script Structure
1. **Modbus Communication Setup**: Configures serial communication parameters for the solar controller.
2. **InfluxDB Client Setup**: Establishes connection with InfluxDB for data storage.
3. **Data Reading Function**: Reads specific register addresses from the solar controller.
4. **Data Formatting Function**: Prepares data points for InfluxDB storage.
5. **Main Loop**: Continuously reads data and logs it to InfluxDB.

## Key Learnings
- Practical implementation of Modbus RTU protocol
- Real-time data logging from hardware devices
- Integration of IoT devices with cloud databases
- Error handling in long-running scripts
- Configuration management for deployable scripts

## Potential Applications
- Solar energy monitoring systems
- Industrial automation data logging
- IoT device data collection
- Energy consumption tracking

## Future Improvements
- Implement a retry mechanism for failed reads or writes
- Add data validation before storage
- Create a separate configuration file for easy customization
- Implement unit tests for key functions

## Running the Script
1. Install required dependencies: `pip install minimalmodbus influxdb-client`
2. Update the `config.py` file with your specific settings
3. Run the script: `python solarcontroller_logger.py`

## Note
This script is designed for a specific SRNE solar controller model. Modifications may be necessary for different controllers or Modbus devices.
