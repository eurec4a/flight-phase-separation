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
    bahamas = catalog.halo.bahamas.ql.by_flight_id[flight].to_dask()
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

def get_navdata_TO(nav_data):
    """
    :param nav_data: flight id
    """
    import pathlib
    import xarray as xr
    import twinotter

    ds = twinotter.load_flight(nav_data)
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
    "TO": get_navdata_TO,
}

def get_navdata(platform, flight):
    """
    :param platform: platform id
    :param flight: flight id
    """
    return NAVDATA_GETTERS[platform](flight)

__all__ = ["get_navdata"]
