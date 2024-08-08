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


AC:
- reading should have a sensor
- 

AC: Users should filter by sensor, start date and end date readings, and by unit of measure??

### Find sensor by id or name

### Filter readings by sensor

### Filter by dyke


### Filter and Retrieve Readings Data

**Title**: As a user, I want to filter and retrieve readings data so that I can analyze specific subsets of data based on various criteria.

#### Description:
Users need the ability to filter readings data by multiple criteria, including date range, sensor, sensor type, unit, and crossection. The readings data should contain comprehensive information including sensor details, unit of measurement, sensor type, reading value, timestamp, and associated crossection details.

### Acceptance Criteria:

1. **Filter Readings by Date Range**:
   - Users can specify a start date and an end date to filter readings within that range.
   - If no date range is specified, all available readings should be returned.

2. **Filter Readings by Sensor**:
   - Users can filter readings by specific sensors.
   - The system should allow selecting multiple sensors for filtering.

3. **Filter Readings by Sensor Type**:
   - Users can filter readings based on the sensor type.
   - The system should support filtering by multiple sensor types.

4. **Filter Readings by Unit of Measurement**:
   - Users can filter readings by specific units of measurement.
   - Multiple units can be selected for filtering.

5. **Filter Readings by Crossection**:
   - Users can filter readings associated with specific crossections.
   - Multiple crossections can be selected for filtering.

6. **Readings Data Fields**:
   - Each reading should include:
     - Sensor details
     - Unit of measurement
     - Sensor type
     - Reading value
     - Timestamp of the reading
     - Crossection details

7. **Retrieve Crossection Details**:
   - Users can retrieve detailed information about crossections.
   - Crossection details should include:
     - Name
     - ID
     - All associated crossection layers
     - Associated sensors

### Tasks

#### To Do List:

1. **Database Schema Updates**:
   - [x] Add necessary fields to the readings table if not already present (sensor, unit, sensor type, value, time, crossection).
   - [ ] Ensure proper indexing on columns to improve query performance.

2. **API Endpoint for Filtering Readings**:
   - [ ] Create a new API endpoint for retrieving readings with filters.
   - [ ] Implement filtering by date range (start date and end date).
   - [ ] Implement filtering by sensor.
   - [ ] Implement filtering by sensor type.
   - [ ] Implement filtering by unit of measurement.
   - [ ] Implement filtering by crossection.
   - [ ] Ensure the response includes all necessary readings data fields.

3. **API Endpoint for Retrieving Crossection Details**:
   - [ ] Create a new API endpoint for retrieving detailed information about crossections.
   - [ ] Include name, ID, all associated crossection layers, and associated sensors in the response.

4. **Testing**:
   - [ ] Write unit tests for the new filtering functionality.
   - [ ] Write integration tests to ensure the endpoints return correct data based on filters.
   - [ ] Perform manual testing to verify that the filtering works as expected.

5. **Documentation**:
   - [ ] Update API documentation to include the new endpoints and filtering options.
   - [ ] Provide examples of how to use the filtering options.

6. **Deployment**:
   - [ ] Deploy the updated API to the staging environment.
   - [ ] Conduct final round of testing in staging.
   - [ ] Deploy to production after successful testing.

### Example API Request and Response:

#### Request:
```http
GET /readings?start_date=2024-01-01&end_date=2024-01-31&sensor_id=1,2&sensor_type=temperature&unit=Celsius&crossection_id=3
```

#### Response:
```json
{
  "readings": [
    {
      "sensor": {
        "id": 1,
        "name": "Temperature Sensor A"
      },
      "unit": "Celsius",
      "sensor_type": "temperature",
      "value": 22.5,
      "time": "2024-01-15T10:00:00Z",
      "crossection": {
        "id": 3,
        "name": "Crossection 1-1"
      }
    },
    {
      "sensor": {
        "id": 2,
        "name": "Temperature Sensor B"
      },
      "unit": "Celsius",
      "sensor_type": "temperature",
      "value": 23.0,
      "time": "2024-01-20T12:00:00Z",
      "crossection": {
        "id": 3,
        "name": "Crossection 1-1"
      }
    }
  ]
}
```

This user story, acceptance criteria, and task list should help guide the implementation of the feature to filter and retrieve readings data with the specified details.