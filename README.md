## Segmentation of flights during EUREC4A

The Research Flights (RFs) during EUREC4A can be divided into different segments.
For example circles and straight legs were purposefully conducted maneuvers during which
a distinct sampling behaviour of the various instruments can be assumed. For future analyses
based on specific kinds of flight segments (e.g. only based on circles) it is desired to use a
common set of start- and end-times to assure consistency between the studies. This repository
provides files listing the start- and end-times of  flight segments for each platform for each flight. The files also contain general information and/or notes about special events during the RF.

Flight segments need not be unique or complete: a given time during a flight may belong to
any number of segments or none at all. Segments may overlap (i.e. a segment of kind `circling`
may include several segments of kind `circle`). This allows flights to be segmented
in multiple ways and at multiple levels of granulatiry.


### Common vocabulary - broad sampling strategy
Following are names of segments assembled from a range of platforms describing broad sampling strategies. Many will contain subsets
e.g. `cloud` segments will likely contain `subcloud layer` and `cloud layer` segments.
Data providers are encouraged to use these names, especially those in the first, where applicable.
Feel free to add the the list (e.g. with a Github pull request) if needed.
* ground
* transit
* circle
* cloud
* calibration
* profile
* axbt
* rectangle
* sawtooth
* racetrack
* clover

### Common vocabulary - subsets/refinements and super-sets
* circling: describes multiple consecutive circles.
* upward: primarily ascending, could be used as further detail for `profile` segments
* downward: primarily descending, could be used as further detail for `profile` segments

The following kinds describe level flight legs sampling atmospheric structure:
* surface level
* subcloud layer
* cloud base level
* cloud layer
* inversion level
* above cloud
* in cloud (these may be many and short)

### Platform-specific subsets
Platforms are free to adopt other conventions exploiting the ability for a segment to have more than one kind associated with it.

The ATR uses the following sub-kinds of certain `level` segments:
* above inversion ferry leg
* below inversion ferry leg

HALO uses the following sub-kinds of the `calibration` kind:
* lidar_calibration
* radar_calibration_wiggle
* radar_calibration_tilted
* baccardi_calibration

## Conventions
Flight segmentation is designed to be flexible and unstructured, but we propose that data providers follow the convention that
_a time or time window may not belong to more than one segment of the same kind_

## Handling of time ranges

Time ranges are defined as semi-open intervals. So the start time is part of the time range while the end time is excluded from the range. This way, it is possible to define exactly consecutive segments without any ambiguities regarding the instance in between.

## Segment irregularities

If some irregularities are found within a segment (i.e. a diversion from the planned route, starting time of a circle not one minute before a sonde), these should be recorded in the `irregularities` field. In general, this field is meant to be a free text field, such that people using the dataset get a proper explanation. However, for automatic checking it may also be useful to have some standardized *irregularity tags* which can be interpreted by a script. These tags should be prepended to the explanatory string of the irregularity.

Currently the following *irregularity tags* are in use:

* `TTFS`: **T**ime **T**o **F**irst **S**onde is (on purpose) not one minute
* `SAM`: **S**onde **A**dded **M**anually: association of sondes to segments is (on purpose) not as suggested by launch time and segment times
* `NONSTD`: segment is not at its usual location or size (only added if there is a usual location or size for this segment `kind` on that `platform`)
