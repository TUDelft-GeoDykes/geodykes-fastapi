# Acceptance criteria to guide testing and development of the Geodykes app

## Timeseries data
- [ ] Subsets of timeseries should be easily queried and or indexed around one single location within a crossection.
- [ ] A user should be able to load a full timeseries dataset.
- [ ] Duplicate timeseries data should be handled gracefully (How should we handle it, by providing a check of the latest data in the dataset that matches the latest reading in the specific location).


### Implementation notes
- [ ] One table for all timeseries data


## Sensors
In the field timeseries are actually collected with one specific sensor. This sensors should be identifiable and potentially monitored??