# InfluxDB Pack (CPU measurements)

Run a query on InfluxDB to alert on CPU

## Configuration

Copy the example configuration in **influxdb.yaml.example** to */opt/stackstorm/configs/influxdb.yaml* and edit as required.

Example configuration:

## Using the pack

See my blog post

## Actions

Currently, the following sensors are implemented:
- gaia: "select * from cpu;" and find max per series
- panos: "select * from cpu_load;" and find max per series

