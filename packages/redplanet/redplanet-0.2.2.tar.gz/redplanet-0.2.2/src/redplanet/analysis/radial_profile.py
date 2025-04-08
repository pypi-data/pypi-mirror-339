from collections.abc import Callable

import numpy as np

from redplanet.helper_functions import geodesy





def get_concentric_ring_coords(
    lon                 : float,
    lat                 : float,
    radius_km           : float,
    dist_btwn_rings_km  : float = ...,
    num_rings           : int   = None,
    dist_btwn_points_km : float = 5,
) -> tuple[ np.ndarray, tuple[np.ndarray] ]:
    """
    Generate concentric ring coordinates around a central point.

    This function computes the radii for a series of concentric rings centered at the specified location and then generates (longitude, latitude) coordinates for equally spaced points along each ring. The rings can be defined by either a fixed distance between rings or by specifying the total number of rings to generate.

    Parameters
    ----------
    lon : float
        Longitude coordinate of the center of the circle, in range [-180, 360].
    lat : float
        Latitude coordinate of the center of the circle, in range [-90, 90].
    radius_km : float
        Radius (in kilometers) of the largest/outermost ring.
    dist_btwn_rings_km : float, optional
        Distance (in kilometers) between consecutive rings. You can't provide both this and `num_rings`. Default is 5 km.
    num_rings : int, optional
        Total number of rings to generate. You can't provide both this and `dist_btwn_rings_km`. Default is None.
    dist_btwn_points_km : float, optional
        Desired spacing (in kilometers) between adjacent points on each ring. Default is 5.

    Returns
    -------
    ring_radius_km__per_ring : np.ndarray
        Ring radii (in kilometers) for each ring.
    ring_coords__per_ring : tuple[np.ndarray]
        A tuple of 2D numpy arrays, each containing the (longitude, latitude) coordinates of points on the corresponding ring (shape is `(num_points,2)`).

    Raises
    ------
    ValueError
        If either both or neither of `dist_btwn_rings_km` and `num_rings` are specified.

    Notes
    -----
    For examples, see ["Tutorials & Guides"](/redplanet/tutorials/){target="_blank"} on the RedPlanet documentation website.
    """

    ## Input validation and defaults — after this, we're guaranteed one of `dist_btwn_rings_km` or `num_rings` will be a float and the other will be None.
    if (dist_btwn_rings_km is not ...) and (num_rings is not None):
        raise ValueError('Cannot provide both `dist_btwn_rings_km` and `num_rings` — provide only one or neither.')

    if num_rings:
        dist_btwn_rings_km = None
    else:
        dist_btwn_rings_km = 5

    ## Get radii for a series of concentric rings, starting at the center and going up to a distance of `radius_km`.
    if dist_btwn_rings_km:
        ring_radius_km__per_ring = np.arange(0, radius_km, dist_btwn_rings_km)
    else:
        ring_radius_km__per_ring = np.linspace(0, radius_km, num_rings)

    ## Calculate the number of points that can fit in each ring such that each point is `dist_btwn_points_km` away from its neighbors.
    ## Given a circle with radius `r`, the number of points you could fit around the circumference (`2*pi*r`) such that every point is distance `x` from its neighbors is given by `2*pi*r/x`.
    num_points__per_ring = np.ceil(2 * np.pi * ring_radius_km__per_ring / dist_btwn_points_km).astype(int)
    ## note: we're using ceil here to ensure atleast 1 point per ring :)    (i think???)

    ## Enforce a minimum number of points per ring
    min_num_points = 10
    num_points__per_ring[num_points__per_ring < min_num_points] = min_num_points

    ## Generate (lon,lat) coordinates for each point on each ring.
    ring_coords__per_ring = []
    for (ring_radius_km, num_points) in zip(ring_radius_km__per_ring, num_points__per_ring):
        ## Generate the (lon,lat) coordinates of `num_points` points around the circle of radius `ring_radius_km`.
        ring_coords = geodesy.make_circle(
            lon       = lon,
            lat       = lat,
            radius    = ring_radius_km * 1e3,
            n_samples = num_points,
            endpoint  = False,
        )
        ring_coords__per_ring.append(ring_coords)

    return (
        ring_radius_km__per_ring,
        tuple(ring_coords__per_ring)
    )





def get_profile(
    ring_coords__per_ring : tuple[np.ndarray],
    accessor              : Callable[[float, float], float],
    return_stats          : bool = False,
) -> np.ndarray | tuple[ np.ndarray, np.ndarray, tuple[np.ndarray] ]:
    """
    Compute a radial profile using data extracted from concentric rings.

    This function computes a one-dimensional radial profile by applying an accessor function to a set of coordinates along each ring. For each ring, it averages the values returned by the accessor function. Optionally, the function can also return additional statistical information.


    Parameters
    ----------
    ring_coords__per_ring : tuple[np.ndarray]
        A tuple where each element is a numpy array containing (longitude, latitude) coordinate pairs for a ring. This corresponds to the second output of `get_concentric_ring_coords`.
    accessor : Callable[[float, float], float]
        A function that accepts two arguments (longitude and latitude), then returns a numerical value corresponding to a data point at those coordinates. See Notes for more information.
    return_stats : bool, optional
        If True, the function returns additional statistical data (standard deviation and raw values for each ring) along with the averaged values. Default is False.


    Returns
    -------
    avg_vals__per_ring : np.ndarray
        Averaged values per ring (starting with the smallest).

    sigma__per_ring : np.ndarray
        Only returned if `return_stats` is True.

        Standard deviations (sigma) per ring.

    vals__per_ring : tuple[np.ndarray]
        Only returned if `return_stats` is True.

        A tuple of 1D numpy arrays, each containing the data values extracted from each ring (shape is `(num_points,)`).

    Notes
    -----
    The input for the `accessor` parameter must be a function, which might be confusing. Here are two examples (assume datasets have already been loaded):

    - Example 1: For functions which only take longitude and latitude as arguments (e.g., topography), you can simply pass `accessor = redplanet.Crust.topo.get`.
    - Example 2: For functions which require additional arguments (e.g., vector components of the magnetic field or custom calculations), you should define a separate function that will only require longitude and latitude as arguments. There are two ways to do this:
        - Directly supply a lambda function like `accessor = lambda lon, lat: redplanet.Mag.sh.get(lon, lat, quantity='radial')` — this is ideal for simple one-line accessors.
        - Define a function separately like `def get_value(lon, lat): return redplanet.Mag.sh.get(lon, lat, quantity='radial')`, and then pass `accessor = get_value` — this is ideal when your implementation of the `get_value` function involves multiple steps, e.g. querying multiple datasets, performing calculations, conditional/loop blocks, etc.
    """

    vals__per_ring = []
    for ring_coords in ring_coords__per_ring:
        vals = []
        for (lon, lat) in ring_coords:
            vals.append(accessor(lon, lat))
        vals = np.array(vals)
        vals__per_ring.append(vals)

    avg_vals__per_ring = np.array([np.mean(vals) for vals in vals__per_ring])

    if not return_stats:
        return avg_vals__per_ring

    sigma__per_ring = np.array([np.std(vals) for vals in vals__per_ring])

    return (
        avg_vals__per_ring,
        sigma__per_ring,
        tuple(vals__per_ring),
    )
