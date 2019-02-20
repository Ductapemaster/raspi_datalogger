# Architecture
## Sensor(s)
Current one sensor developed using a Particle Photon gathers temperature, relative humidity, barometric pressure, and 
CO<sub>2</sub> from a location in my apartment.

These values are published to a MQTT broker, each with their own topic.

## MQTT Broker
A Raspberry Pi on my local network to acts as an MQTT broker (using mosquitto).

## Database Bridge
`Main.py` acts as a bridge to a database by subscribing to the topics published by the sensors. This runs locally on the Pi.

## Database
A cloud VPS instance is used to handle the database for this project.  Docker is used to manage the Influx instance.

## Webserver
`webserver.py` runs locally on the Pi to serve a page with graphs.  Eventually this will be migrated to the VPS, but
but proper authentication will be required.

# To Do
- [ ] Add additional hierarchy to the MQTT topics (location, sensor type, etc).  Database fields to support exist
- [ ] Consider splitting repo into MQTT-database bridge and webserver elements
    - [ ] Set scripts up with Docker for portability
- [ ] Use Python logging module instead of `print()`

