import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table, join, Column
import astropy.units as u 
from astropy.coordinates import SkyCoord
from astropy.io import ascii

import astroquery
from astroquery.mast import Catalogs
from astroquery.mast import Observations
from astroquery.mast import Tesscut


def has_data(catalog,raname='ra',decname='dec',namename='Name',verbose=True,cutout=1):
    indices = []

    for j, name in enumerate(catalog[namename]):
        ra, dec = catalog[j][raname,decname]
        coords = SkyCoord(ra,dec,unit=(u.hourangle,u.deg))
        try:
            hdulist = Tesscut.get_cutouts(coords, cutout) # actually downloads the FITS files! eep! 
            if len(hdulist) !=0:
                indices.append(j)
                if verbose:
                    print('%s %.3f %.3f\n' % (name,coords.ra.deg, coords.dec.deg))
        except:
            pass
    return indices

def find_in_tess(catalog,raname='ra',decname='dec',namename='Name',verbose=True):
    names = []
    for j, name in enumerate(catalog['Name']):
        ra, dec = catalog[j][raname,decname]
        obsTable = Observations.query_region("%s %s "  % (ra, dec),radius=10*u.arcsec)
        m = [obsTable['obs_collection']=='TESS']
        if np.sum(m) != 0:
            names.append(name)
            if verbose:
                print(name)
    in_tess = join(Table({namename:np.array(names)}),catalog,keys=namename)
    return in_tess