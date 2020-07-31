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
        _catalog_cache["HALO"] = open_catalog("https://raw.githubusercontent.com/d70-t/eurec4a-intake/HALO_QL/catalog.yml")

    catalog = _catalog_cache["HALO"]
    bahamas = catalog.halo.bahamas.ql.by_flight_id[flight].to_dask()
    ds = bahamas.rename({"tid": "time"})
    return xr.Dataset({
        "time": ds.TIME,
        "lat": ds.IRS_LAT,
        "lon": ds.IRS_LON,
        "altitude": ds.IRS_ALT,
        "roll": ds.IRS_PHI,
        "pitch": ds.IRS_THE,
        "heading": ds.IRS_HDG,
    })

NAVDATA_GETTERS = {
    "HALO": get_navdata_HALO,
}

def get_navdata(platform, flight):
    """
    :param platform: platform id
    :param flight: flight id
    """
    return NAVDATA_GETTERS[platform](flight)

__all__ = ["get_navdata"]
