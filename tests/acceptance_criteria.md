# Acceptance criteria to guide testing and development of the Geodykes app

## Timeseries data
- [ ] Subsets of timeseries should be easily queried and or indexed around one single location within a crossection.
- [ ] A user should be able to load a full timeseries dataset.
- [ ] Duplicate timeseries data should be handled gracefully (How should we handle it, by providing a check of the latest data in the dataset that matches the latest reading in the specific location).


### Implementation notes
- [ ] One table for all timeseries data


## Sensors
In the field timeseries are actually collected with one specific sensor. This sensors should be identifiable and potentially monitored??

- [ ] A sensor should be identifiable by a unique ID.
- [ ] A sensor should be reported as failing after if it doesnt send back data continuosly for 24 hours.
- [ ] This should be displayed in the dashboard.
- [ ] A sensor is defined as working or failing, which could then be listed in an API endpoint and queried easily in SQL.

### Implementation notes

## Pipeline for loading data
- [ ] Should automatically load readings every day at 00:00.
- [ ] Configuration of the loading timerange should be flexible, every day, or every hour....
- [ ] Already existing data will uploaded using the ORM SQLAlchemy models. 



