import requests
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import pandas
import geopandas

import cartopy
import cartopy.crs as ccrs                   
import cartopy.feature as cf
import cartopy.io.shapereader as shpreader                 

def find_poly(country):
    """ Find the country's polygon

    Parameters
    ----------
    country: alpha3 country code

    Returns
    -------
    poly: shapely polygon
    
    """
    countries = shpreader.natural_earth(resolution='50m',
                                        category='cultural',
                                        name='admin_0_countries')
    df = geopandas.read_file(countries)
    poly = df.loc[df['ADM0_A3'] == country]['geometry'].values
    return poly

def generate_map(country, lat, lon):
    """ Creates a figure of orthographic earth centered on one country

    Parameters
    ----------
    country: alpha3 country code
    lat: latitude in degrees
    lon: longitude in degrees

    Returns
    -------
    fig: matplotlib figure

    """

    # Extract country polygon(s)  
    country_poly = find_poly(country)

    # Create figure and axes
    fig = plt.figure(figsize = (6, 6))
    ax = plt.axes(projection = ccrs.Orthographic(central_latitude=lat, central_longitude=lon))  
    
    # Adds lands, oceans and borders
    ax.add_feature(cf.LAND.with_scale('50m'), color = 'aliceblue')
    ax.add_feature(cf.OCEAN.with_scale('50m'), color = 'lightsteelblue')
    ax.add_feature(cf.BORDERS, linestyle='-', lw=.2, edgecolor = 'lightsteelblue') 
    ax.outline_patch.set_edgecolor('lightsteelblue')

    # Adds country polygon
    ax.add_geometries(country_poly, crs=ccrs.PlateCarree(), facecolor='red', alpha = 0.5)  

    # Meridians and parallels  
    gl = ax.gridlines(dms=True, x_inline=False, y_inline=False, color = 'slategrey', lw=0.3, alpha = 0.2)
    
    # Red pointer centered on (lat, lon)
    pointer = ax.gridlines(dms=True, x_inline=False, y_inline=False, color = 'red', lw=0.3, alpha = 0.5)
    pointer.xlocator = mticker.FixedLocator([lon])
    pointer.ylocator = mticker.FixedLocator([lat])
                                   
    return fig

def get_countries():
    """ Get countries from restcountries api

    Returns
    -------
    countries: list of dict of countries

    """
    response = requests.get("https://restcountries.eu/rest/v2/all")
    countries = json.loads(response.text)
    return countries

def build_all_maps(countries):
    """ Generate maps and save figures for all countries

    Parameters
    ----------
    countries: list of dict of countries

    """

    for country in countries:
        try:
            plt.clf()
            plt.close()
            a3, name = country['alpha3Code'], country['name']
            lat, lon = country['latlng'][0], country['latlng'][1]
            f = generate_map(a3, lat, lon)
        except:
            plt.clf()
            plt.close()
        else:
            plt.savefig(f'maps/{a3}', dpi = 300)

if __name__ == '__main__':
    build_all_maps(get_countries())