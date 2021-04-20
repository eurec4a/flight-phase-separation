import yaml
import numpy as np
import xarray as xr


def _main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input flight segment file (yaml)")
    parser.add_argument("outfile", help="output netcdf file")
    parser.add_argument("-n",
                        "--ncfile",
                        help="read timeline from this netcdf file")
    parser.add_argument("-v",
                        "--ncvar",
                        default="time",
                        help="netcdf time variable (default: time)")

    args = parser.parse_args()

    if args.ncfile:
        time = xr.open_dataset(args.ncfile)[args.ncvar].load().data
    else:
        raise ValueError("timeline must be supplied as netCDF")

    with open(args.infile) as infile:
        flightdata = yaml.load(infile, Loader=yaml.SafeLoader)

    kinds = list(sorted({k
                         for s in flightdata.get("segments", [])
                         for k in s.get("kinds", [])}))
    part_of_kind = np.zeros((len(time), len(kinds)), dtype="bool")
    for s in flightdata.get("segments", []):
        m = (time >= np.datetime64(s["start"])) \
          & (time < np.datetime64(s["end"]))
        for k in s.get("kinds", []):
            part_of_kind[m, kinds.index(k)] = True

    segment_ids = list(sorted({s["segment_id"]
                               for s in flightdata.get("segments", [])}))
    part_of_segment = np.zeros((len(time), len(segment_ids)), dtype="bool")
    for s in flightdata.get("segments", []):
        m = (time >= np.datetime64(s["start"])) \
          & (time < np.datetime64(s["end"]))
        part_of_segment[m, segment_ids.index(s["segment_id"])] = True

    ds = xr.Dataset({
        "time": (("time",), time),
        "kind": (("kind",), kinds),
        "segment": (("segment",), segment_ids),
        "part_of_kind": (("time", "kind"), part_of_kind),
        "part_of_segment": (("time", "segment"), part_of_segment),
    })

    ds.to_netcdf(args.outfile)

    return 0


if __name__ == "__main__":
    exit(_main())
