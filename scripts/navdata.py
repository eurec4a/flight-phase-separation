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

NAVDATA_GETTERS = {
    "HALO": get_navdata_HALO,
    "P3":   get_navdata_P3,
}

def get_navdata(platform, flight):
    """
    :param platform: platform id
    :param flight: flight id
    """
    return NAVDATA_GETTERS[platform](flight)

__all__ = ["get_navdata"]
