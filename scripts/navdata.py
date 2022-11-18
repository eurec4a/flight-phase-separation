# the individual loaders should import dependencies within the function
# that way it is possible to run the code for one platform if dependencies
# for another platform are not met

_catalog_cache = {}

def get_navdata_HALO(flight):
    """
    :param flight: flight id
    """
    import xarray as xr
    from intake import open_catalog
    if "HALO" not in _catalog_cache:
        _catalog_cache["HALO"] = open_catalog("https://raw.githubusercontent.com/eurec4a/eurec4a-intake/master/catalog.yml")

    catalog = _catalog_cache["HALO"]
    bahamas = catalog.HALO.BAHAMAS.QL[flight].to_dask()
    ds = bahamas.rename({"tid": "time"})
    return xr.Dataset({
        "time": ds.TIME,
        "lat": ds.IRS_LAT,
        "lon": ds.IRS_LON,
        "alt": ds.IRS_ALT,
        "roll": ds.IRS_PHI,
        "pitch": ds.IRS_THE,
        "heading": ds.IRS_HDG,
    })

def get_navdata_P3(flight):
    """
    :param flight: flight id
    """
    import xarray as xr
    from intake import open_catalog
    if "P3" not in _catalog_cache:
        _catalog_cache["P3"] = open_catalog("https://raw.githubusercontent.com/eurec4a/eurec4a-intake/master/catalog.yml")

    catalog = _catalog_cache["P3"]
    fl = catalog.P3.flight_level[flight].to_dask()
    return xr.Dataset({
        "time":    fl.time,
        "lat":     fl.lat,
        "lon":     fl.lon,
        "alt":     fl.alt,
        "roll":    fl.roll,
        "pitch":   fl.pitch,
        "heading": fl.cog,
    })

def get_navdata_TO(flight_id):
    """
    :param nav_data: flight id
    """
    import xarray as xr
    from intake import open_catalog
    import re
    match = re.match("TO-(\d+)", flight_id)
    if match is None:
        raise Exception(f"Malformed flight id {flight_id}")
    flight_number = int(match.groups()[0])

    if "TO" not in _catalog_cache:
        _catalog_cache["TO"] = open_catalog("https://raw.githubusercontent.com/leifdenby/eurec4a-intake/twinotter-masin/catalog.yml")

    catalog = _catalog_cache["TO"]

    ds = catalog.TO.MASIN[f"TO{flight_number}_1Hz"].to_dask()
    ds = ds.rename(dict(Time="time"))

    return xr.Dataset({
        "time": ds.time,
        "lat": ds.LAT_OXTS,
        "lon": ds.LON_OXTS,
        "alt": ds.ALT_OXTS,
        "roll": ds.ROLL_OXTS,
        "pitch": ds.PTCH_OXTS,
        "heading": ds.HDG_OXTS,
    })

NAVDATA_GETTERS = {
    "HALO": get_navdata_HALO,
    "P3":   get_navdata_P3,
    "TO": get_navdata_TO,
}

def get_navdata(platform, flight):
    """
    :param platform: platform id
    :param flight: flight id
    """
    return NAVDATA_GETTERS[platform](flight)

__all__ = ["get_navdata"]
