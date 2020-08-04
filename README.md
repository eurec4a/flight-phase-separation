## Segmentation of flights during EUREC4A

The Research Flights (RFs) during EUREC4A can be divided into different segments.
For example circles and straight legs were purposefully conducted maneuvers during which
a distinct sampling behaviour of the various instruments can be assumed. For future analyses
based on specific kinds of flight segments (e.g. only based on circles) it is desired to use a
common set of start- and end-times to assure consistency between the studies. This repository
provides the start- and end-times of the flight-segments for each RF together with some  very
general information about the RF or special events during the RF.

Flight segments need not be unique or complete: a given time during a flight may belong to
any number of segments or none at all. Segments may overlap (i.e. a segment of kind `circling`
may include several segments of kind `circle`).

Following are names of segments assembled from a range of platforms describing broad sampling strategies.
Data providers are encouraged to use these names, especially those in the first, where applicable.
Feel free to add the the list (e.g. with a Github pull request) if needed.

### Common vocabulary - broad sampling strategy
The following describe broad sampling goals. Many will contain subsets
e.g. `cloud` segments will likely contain `subcloud layer` and `cloud layer` segments.
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
* profile upward: provides further detail for `profile` segments
* profile downward: provides further detail for `profile` segments

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
_a time or time window should not belong to more than one segment of the same type_
