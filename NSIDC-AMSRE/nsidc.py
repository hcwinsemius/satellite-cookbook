import pyproj
import xarray as xr

def proj_coord(coord, proj_in, proj_out):
    """
    Returns a packaged tuple (x, y) coordinate in projection proj_out
    from one packaged tuple (x, y) coordinat ein projection proj_in
    Inputs:
        coord: tuple (x, y)
        proj_in: pyproj.Proj format projection
        proj_out: pyproj.Proj format projection
    Outputs:
        tuple (x, y)
        
    """
    x, y = coord
    return pyproj.transform(proj_in, proj_out, x, y)

def proj_coords(coords, proj_in, proj_out):
    """
    project a list of coordinates, return a list.
    Inputs:
        coords: list of tuples (x, y)
        proj_in: pyproj.Proj format projection
        proj_out: pyproj.Proj format projection
    Outputs:
        list of tuples (x, y)
    
    """ 
    return [proj_coord(coord, proj_in, proj_out) for coord in coords]

def select_bounds(ds, bounds):
    """
    selects xarray ds along a provided bounding box
    assuming slicing should be done over coordinate axes x and y (hard coded, I was lazy....:-()
    """
    
    xs = slice(bounds[0][0], bounds[1][0])
    ys = slice(bounds[1][1], bounds[0][1])
    # select over x and y axis
    return ds.sel(x=xs, y=ys)

def make_measures_url(url_template, res, dt, freq, HV, AD):
    """
    Prepares a url for Measures data to download.
    url_template - str url with placeholders for date (%Y.%m.%d), resolution (:d, km), date (%Y%j),
        frequency (str), polarisation ('H'/'V'), ascending/descending path ('A', 'D')
    
    """
    datestr1 = dt.strftime('%Y%j')
    datestr2 = dt.strftime('%Y.%m.%d')
    if str(res) == '25':
        suffix = 'GRD-RSS'
    else:
        suffix = 'SIR-RSS'
    
    return url_template.format(datestr2, str(res), datestr1, freq, HV, AD, suffix)

def make_measures_download(download_template, url, username, password):
    return download_template.format(username, password, url)

def plot_points(ax, points, **kwargs):
    x_point, y_point = zip(*points)
    ax.plot(x_point, y_point, **kwargs)
    return ax

def correct_miss_fill(ds):
    """
    Returns a properly decoded Climate-and-Forecast conventional ds, after correction of a conflicting attribute (sjeez....)
    """
    for d in ds.data_vars:
        try:
            ds[d].attrs.update({'missing_value': ds[d]._FillValue})
        except:
            pass
    return xr.decode_cf(ds)
