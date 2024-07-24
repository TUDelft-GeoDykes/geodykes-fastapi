# Breakdown
This doc breaks down user stories and features into smaller tasks and acceptance criteria.

 
## User stories
### EPIC: List readings
- AC: A reading should include the following fields in the response body:
  - Dyke to which it belongs to
  - Location in the topology??
  - Sensor id
  - Sensor name??
  - Location in topology
  - Sensor type
  - Measurement unit
  - Timestamp

TASKS:
    - Schema specification
    - View (backend development)

### EPIC: filter readings according parameters
Filter readings according to different parameters:
- 

### Locate a sensor/or reading in a topology belonging to a crossection
- AC: You would like to provide a code-name convention for the sensor/reading point that describes the location of the sensor in the topology, something that relates the position of one sensor to the next one for example, in a measurement vertical.
Example:
  (The first section of this coding convention should idenfity a crossection, not just a dyke)
  HEN001-1-ST-4 (Code), name
  Name of dyke + ID + Measurement vertical + Sensor Type + location in sequence of measurement vertical

### Loading tabular the data into the database
- AC: Would like have the proper coding for each sensor located in the topology
- Tasks:
  - Assign the right number for the sensor in a measurement vertical
  - We could define this considering that currently the names of sensors have prepended the depth, for example: "duifpoloder_n_1_water_content_0.5" and "duifpoloder_n_1_water_content_0.2"
  - Redefine the names based on new convention


### Find sensor by id or name

### Filter readings by sensor

### Filter by dyke

### Load readings continuously from different sensors

