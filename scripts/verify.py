import os
import yaml
import numpy as np

from navdata import get_navdata
from checkers import FlightChecker

def _main():
    import logging
    logging.basicConfig(format='%(levelname)s %(name)s: %(message)s', level=logging.INFO)

    basedir = os.path.abspath(os.path.dirname(__file__))
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("-s", "--sonde_info", help="sonde info yaml file", default=os.path.join(basedir, "sondes.yaml"))
    args = parser.parse_args()

    mainlogger = logging.getLogger("main")
    flightlogger = logging.getLogger("flight")
    segmentlogger = logging.getLogger("segment")

    mainlogger.info("verifying %s", args.infile)

    flightdata = yaml.load(open(args.infile), Loader=yaml.SafeLoader)
    checker = FlightChecker(flightdata)

    flight_warnings = list(checker.check_flight(flightdata))
    for warning in flight_warnings:
        flightlogger.warn(warning)

    navdata = get_navdata(flightdata["platform"], flightdata["flight_id"]).load()

    sonde_info = yaml.load(open(args.sonde_info), Loader=yaml.SafeLoader)
    sonde_info = [s for s in sonde_info if s["platform"] == flightdata["platform"]]

    segment_warning_count = 0
    for seg in flightdata["segments"]:
        t_start = np.datetime64(seg["start"])
        t_end = np.datetime64(seg["end"])
        seg_navdata = navdata.sel(time=slice(t_start, t_end))

        sondes_in_segment = [s
                             for s in sonde_info
                             if s["launch_time"] >= seg["start"]
                             and s["launch_time"] < seg["end"]]
        sondes_by_flag = {f: [s for s in sondes_in_segment if s["flag"] == f]
                          for f in set(s["flag"] for s in sondes_in_segment)}

        warnings = list(checker.check_segment(seg, seg_navdata, sondes_by_flag))
        for warning in warnings:
            segmentlogger.warn(warning)

        segment_warning_count += len(warnings)

    mainlogger.info("%d flight warnings, %d segment warnings",
                    len(flight_warnings),
                    segment_warning_count)

    if len(flight_warnings) == 0 and segment_warning_count == 0:
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(_main())
